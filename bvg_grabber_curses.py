# This file is part of BVG Grabber (3-clause BSD), see LICENSE

# BVG Grabber TUI display
# This provides a (Curses based) textual/graphical display for grabbed BVG info,
# very similar to beamer-info, but with much lower system requirements
# and slightly different funcionality.
# It displays info in a human readable way on practically all systems
# that can run `bvg-grapper.py`, while beamer-info requires more recent systems
# and OpenGL v3+.
# To use this, edit the two files `bvg_grabber_*_config.py`,
# and then run with `python3 bvg_grabber_curses.py`.

import curses

from bvggrabber.api import Response
from bvggrabber.utils.format import timeformat, durationformat
from datetime import datetime
from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty
from math import floor
from inspect import getmembers
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectionError
from socket import gaierror
from bvg_grabber_extended import *


ORIG_HEADERS = ['From', 'To', 'At', 'Fetch-Time', 'In', 'Line', 'Scheduled', 'Too-Soon', 'Too-Late']
ORIG_COL_FROM = 0
ORIG_COL_TO = 1
ORIG_COL_AT = 2
ORIG_COL_FETCH_TIME = 3
ORIG_COL_IN = 4
ORIG_COL_LINE = 5
ORIG_COL_SCHEDULED = 6
ORIG_COL_TOO_SOON = 7
ORIG_COL_TOO_LATE = 8


class TableCellAlignment():

    LEFT = 0
    CENTER = 1
    RIGHT = 2


def curses_draw_table_cell(cont, line, colStart, colWidth, text, attribs = 0, alignment = TableCellAlignment.LEFT):

    if alignment == TableCellAlignment.LEFT:
        colText = colStart
    elif alignment == TableCellAlignment.CENTER:
        colText = colStart + max(0, floor((colWidth - len(text)) / 2))
    elif alignment == TableCellAlignment.RIGHT:
        colText = colStart + max(0, (colWidth - len(text)))
    else:
        raise ValueError('invalid alignment value: ' + str(alignment))

    cont.addstr(line, colText, text, attribs)


def curses_draw_status(msg, container = None, error = False):
    global screen
    global nCols
    global statusAttribs
    global errorStatusAttribs

    if container == None:
        container = screen
    if error:
        attribs = errorStatusAttribs
    else:
        attribs = statusAttribs

    # draw centered on line 0
    container.addstr(0, floor((nCols - len(msg)) / 2), msg, attribs)
    container.refresh()


class TableData(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def nCols(self):
        pass

    @abstractproperty
    def nRows(self):
        pass

    @abstractmethod
    def header_at(self, col):
        pass

    @abstractmethod
    def header_index(self, headerName):
        pass

    @abstractmethod
    def value_at(self, row, col):
        pass

    @abstractmethod
    def merge(self, other):
        pass


class MatrixTableData(object):

    def __init__(self, headers, content):
        """
        :param list(str) headers: table header texts
        :param list(list(object)) content: table content (x,y indexed)
        """

        self._headers = headers
        self._content = content
        if len(headers) != len(content[0]):
            raise ValueError("Headers and content disagree in the number of columns")

    @property
    def nCols(self):
        return len(self.content[0])

    @property
    def nRows(self):
        return len(self.content)

    def header_at(self, col):
        return self._headers[col]

    def header_index(self, headerName):
        return self._headers.index(headerName)

    def value_at(self, row, col):
        return self._content[row][col]

    def merge(self, other):
        """ Appends ``other``s content, if headers match. """
        if not isinstance(other, MatrixTableData):
            raise TypeError("The given object is not of type MatrixTableData")
        if self.headers != other.headers:
            # Comparing lists - if you compare two lists
            # in Python, they will be considered to be equal
            # if both lists have the same number of elements,
            # and each element of the first list is equal to
            # the element at the same position in the second list.
            raise ValueError("The given table data object has a different set of headers")

        self._content.extend(other._content)


class DeparturesTableData(object):

    def __init__(self, departures):
        """
        :param list(list(object)) departures: table content (x,y indexed)
        """

        self._headers = ORIG_HEADERS
        self._departures = departures

    @property
    def nCols(self):
        return len(self._headers)

    @property
    def nRows(self):
        return len(self._departures)

    def header_at(self, col):
        return self._headers[col]

    def header_index(self, headerName):
        return self._headers.index(headerName)

    def value_at(self, row, col):
        dep = self._departures[row]
        return { # switch statement
            0: dep.start,
            1: dep.end,
            2: dep.when,
            3: dep.now,
            4: dep.remaining,
            5: dep.line,
            6: dep.scheduled,
            7: leaves_too_soon(dep),
            8: leaves_too_late(dep),
        }.get(col, None) # value to check and default return

    def merge(self, other):
        """ Appends ``other``s content, if headers match. """
        if not isinstance(other, DeparturesTableData):
            raise TypeError("The given object is not of type DeparturesTableData")

        self._departures.extend(other._departures)


class CursesTable(object):

    def __init__(self, data, container, colSizes = None, colAlignments = None, colRenderers = None, colAttribs = None, colIndices = None, headerAttribs = None):
        """
        :param TableData data:
        :param object container: curses container to draw to (screen, window or pad)
        :param list(double/int) : either as percentage (0.0 - 1.0) or absolute (in #chars), relates to original/data indices, not displayed ones
        :param list(TableCellAlignment) colAlignments: relates to original/data indices, not displayed ones
        :param list(function(object)->str) colRenderers: relates to original/data indices, not displayed ones
        :param list(int/bitfield) colAttribs: see curses.A_*, relates to original/data indices, not displayed ones
        :param list(int) colIndices: displayed indices (order matters), converts indices form data to display, and thus may exclude data columns
        :param int/bitfield headerAttribs: see curses.A_*
        """

        self._data = data
        self._container = container

        if colSizes == None:
            self._colSizes = [1.0 / data.nCols] * data.nCols
        elif not isinstance(colSizes, list):
            raise TypeError("Unsupported type for colSizes: " + type(colSizes))
        elif len(colSizes) != data.nCols:
            raise ValueError("colSizes and content disagree in the number of columns")
        elif isinstance(colSizes[0], float):
            self._colSizes = colSizes
        elif isinstance(colSizes[0], int):
            self._colSizes = [(cs / sum(colSizes)) for cs in colSizes]
        else:
            raise TypeError("Unsupported type for colSizes[0]: " + type(colSizes[0]))

        if colAlignments == None:
            self._colAlignments = [TableCellAlignment.LEFT] * data.nCols
        elif len(colAlignments) != data.nCols:
            raise ValueError("colAlignments and content disagree in the number of columns")
        else:
            notNones = []
            for colAlignment in colAlignments:
                if colAlignment == None:
                    notNone = TableCellAlignment.LEFT
                else:
                    notNone = colAlignment
                notNones.append(notNone)
            self._colAlignments = notNones

        if colRenderers == None:
            self._colRenderers = [str] * data.nCols
        elif not isinstance(colRenderers, list):
            raise TypeError("Unsupported type for colRenderers: " + type(colRenderers))
        elif len(colRenderers) != data.nCols:
            raise ValueError("colRenderers and content disagree in the number of columns")
        else:
            notNones = []
            for colRenderer in colRenderers:
                if colRenderer == None:
                    notNone = str
                else:
                    notNone = colRenderer
                notNones.append(notNone)
            self._colRenderers = notNones

        if colAttribs == None:
            self._colAttribs = [0] * data.nCols
        elif not isinstance(colAttribs, list):
            raise TypeError("Unsupported type for colAttribs: " + type(colAttribs))
        elif len(colAttribs) != data.nCols:
            raise ValueError("colAttribs and content disagree in the number of columns")
        else:
            self._colAttribs = colAttribs

        if colIndices == None:
            self._colIndices = list(range(len(data.nCols)))
        elif not isinstance(colIndices, list):
            raise TypeError("Unsupported type for colIndices: " + type(colIndices))
        elif isinstance(colIndices[0], int):
            self._colIndices = colIndices
        elif isinstance(colIndices[0], str):
            colIndicesInt = []
            for colChosenHeader in colIndices:
                colIndicesInt.append(data.header_index(colChosenHeader))
            self._colIndices = colIndicesInt
        else:
            raise TypeError("Unsupported type for colIndices[0]: " + type(colIndices[0]))

        if headerAttribs == None:
            self._headerAttribs = 0
        else:
            self._headerAttribs = headerAttribs


    def draw(self, y = None, x = None, h = None, w = None):

        if y == None:
            y = 0
        if x == None:
            x = 0
        if h == None:
            [maxH, maxW] = self._container.getmaxyx()
            h = maxH - y
            # Use this alternatively, for a (potentially) more compact table (+),
            # where the footer might change position on every update (-).
            #h = self._data.nRows + 2
        if w == None:
            [maxH, maxW] = self._container.getmaxyx()
            w = maxW - x - 1
        contCols = w

        # The actual sizes of selected table columns in curses columns (chars)
        colSelectedSizes = []
        nSelCols = len(self._colIndices)
        for colIndex in self._colIndices:
            colSelectedSizes.append(self._colSizes[colIndex])
        colSelectedSizes = [floor(css * contCols / sum(colSelectedSizes)) for css in colSelectedSizes]

        # The (starting/left margin) x positions of selected table columns in curses columns (chars)
        colSelectedXs = []
        curX = 0
        for colSelectedSize in colSelectedSizes:
            colSelectedXs.append(curX)
            curX += colSelectedSize

        # due to floor in the previous line, we likely ended up one or two chars short,
        # so we fill up with the last table column
        colSelectedSizes[nSelCols - 1] = contCols - colSelectedXs[nSelCols - 1]

        line = 0

        # draw header
        # clear the line (and in doing so, apply the background color)
        self._container.addstr(y + line, x, ' ' * contCols, self._headerAttribs)
        colInd = 0
        for origInd in self._colIndices:
            #attribs = self._colAttribs[origInd] # same as content
            attribs = self._headerAttribs

            #alignment = self._colAlignments[origInd] # same as content
            alignment = TableCellAlignment.CENTER

            curses_draw_table_cell(self._container, y + line, x + colSelectedXs[colInd], colSelectedSizes[colInd], self._data.header_at(origInd), attribs, alignment)
            colInd += 1
        line += 1

        # draw content
        for rowInd in range(self._data.nRows):
            if rowInd >= h - 2: # do not write more lines then we are allowed to
                break
            colInd = 0
            for origInd in self._colIndices:
                cont = self._data.value_at(rowInd, origInd)
                attribs = self._colAttribs[origInd]
                if isinstance(attribs, int):
                    pass
                elif callable(attribs): # check if it is a function pointer
                    argCont = getmembers(attribs)[4][1].co_argcount # see https://docs.python.org/2/library/inspect.html
                    if argCont == 1:
                         attribs = attribs(cont) # this could be for example the str(int) function
                    else:
                         attribs = attribs(cont, self._data, rowInd) # call with the content of the cell and of the whole data-point
                else:
                    raise TypeError('Unsupported type for colAttribs{origInd}: ' + type(colAttribs))
                curses_draw_table_cell(self._container, y + line, x + colSelectedXs[colInd], colSelectedSizes[colInd], self._colRenderers[origInd](cont), attribs, self._colAlignments[origInd])
                colInd += 1
            line += 1

        # draw footer
        line = h - 1
        # clear the line (and in doing so, apply the background color)
        footerAttribs = self._headerAttribs
        self._container.addstr(y + line, x, ' ' * contCols, footerAttribs)
        halfCols = floor(contCols / 2)
        partCols = [halfCols, contCols - halfCols]
        if len(stations) == 1:
            footerInfo1 = location_simplifier(stations[0][0])
        else:
            footerInfo1 = '' # TODO What info could we show here in this case?
        curses_draw_table_cell(self._container, y + line, x, partCols[0], footerInfo1, footerAttribs, TableCellAlignment.LEFT)
        fetchTime = self._data.value_at(0, 3)
        fetchTimeStr = timeformat(fetchTime)
        curses_draw_table_cell(self._container, y + line, x + partCols[0], partCols[1], fetchTimeStr, footerAttribs, TableCellAlignment.RIGHT)
        line += 1


def response_to_table(response):

    departures = []
    for station in response._departures:
        for dep in station[1]:
            departures.append(dep)

    return DeparturesTableData(departures)


def line_simplifier(line):
    return line.replace('Bus  ', '')


def location_simplifier(location):
    return location.replace(' (Berlin)', '').replace('S+U ', '').replace('S ', '').replace('U ', '')


def duration_attribs(seconds, data, row):
    global contentAttribs
    global uninterestingContAttribs
    global interestingContAttribs
    if data.value_at(row, ORIG_COL_TOO_SOON):
        attribs = contentAttribs
    elif data.value_at(row, ORIG_COL_TOO_LATE):
        attribs = contentAttribs
    else:
        attribs = interestingContAttribs
    return attribs


def duration_renderer(seconds):
    return(duration_humanizer(seconds))


def new_curses_response_table(tableData, cont, colIndices = None, headerAttribs = None):
    global contentAttribs

    colSizes = [0.25, 0.25, 0.1, 0.1, 0.15, 0.1, 0.02, 0.02, 0.02]
    colAlignments = [TableCellAlignment.LEFT, TableCellAlignment.LEFT, TableCellAlignment.RIGHT, TableCellAlignment.RIGHT, TableCellAlignment.RIGHT, TableCellAlignment.LEFT, TableCellAlignment.RIGHT, TableCellAlignment.RIGHT, TableCellAlignment.RIGHT]
    colRenderers = [location_simplifier, location_simplifier, timeformat, timeformat, duration_renderer, line_simplifier, str, str, str]
    colAttribs = [duration_attribs, duration_attribs, duration_attribs, duration_attribs, duration_attribs, duration_attribs, duration_attribs, duration_attribs, duration_attribs]
    if colIndices == None:
        if len(stations) == 1:
            colIndices = ["Line", "To", "In"]
        else:
            colIndices = ["Line", "From", "To", "In"]

    return CursesTable(tableData, cont, colSizes, colAlignments, colRenderers, colAttribs, colIndices, headerAttribs)


def main(win):

    # we know that the first argument from curses.wrapper() is screen.
    # Initialize it globally for convenience.
    global screen
    screen = win

    # load the settings
    exec(open('bvg_grabber_curses_config.py').read())
    # defined in the config file:
    global header_rows
    global footer_rows
    global nCols
    global nRows

    curses.nl()
    curses.noecho()
    # XXX curs_set() always returns ERR
    # curses.curs_set(0)
    screen.timeout(0)

    screen.clear()

    dispLoopIt = 0
    data = None
    while 1: # main display loop

        curses_draw_status('updating...', screen)

        try:
            data = get_data()
            last_update_time = datetime.now()
        except(gaierror, MaxRetryError, ConnectionError):
            if data == None:
                curses_draw_status('failed to grab data!', screen, error=True)
                curses.napms(3000)
                raise
            curses_draw_status('failed to grab data! using data from ' + timeformat(last_update_time), screen)
            curses.napms(3000)

        tableData = response_to_table(data)

        screen.clear()

        curses_table = new_curses_response_table(tableData, screen, None, headerAttribs)

        # wait a few seconds, but react fast to user input
        waitMoments = 0
        while waitMoments < (update_interval * 10):

            curses_table.draw(header_rows, 0, nRows, nCols)

            screen.refresh()

            ch = screen.getch()
            if ch == ord('q') or ch == ord('Q'): # quit
                return 0
            elif ch == ord('s'):
                screen.nodelay(0)
            elif ch == ord('u'): # update
                break
            elif ch == ord(' '):
                screen.nodelay(1)

            curses.napms(100)
            waitMoments += 1

        dispLoopIt += 1

curses.wrapper(main)

