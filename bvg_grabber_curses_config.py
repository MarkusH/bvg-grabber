# This file is part of BVG Grabber (3-clause BSD), see LICENSE

# BVG Grabber TUI display configuration
# See `bvg_grabber_curses.py` for more info.

import curses


# COLOR_BLACK   0
# COLOR_RED     1
# COLOR_GREEN   2
# COLOR_YELLOW  3
# COLOR_BLUE    4
# COLOR_MAGENTA 5
# COLOR_CYAN    6
# COLOR_WHITE   7
if curses.has_colors():
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # for headers
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # for content, normal
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK) # for content, a lot of attention
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK) # for content, less then normal attention
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK) # for content, more then normal attention
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_RED) # for global errors

# A_BLINK 	Blinking text (NOTE Not supported by many terminals!)
# A_BOLD 	Extra bright or bold text
# A_DIM 	Half bright text (NOTE Not supported by most terminals!)
# A_REVERSE 	Reverse-video text
# A_STANDOUT 	The best highlighting mode available
# A_UNDERLINE 	Underlined text
global statusAttribs
global errorStatusAttribs
global headerAttribs
global contentAttribs
global uninterestingContAttribs
global interestingContAttribs
global footerAttribs
statusAttribs = curses.color_pair(2) | curses.A_BLINK | curses.A_BOLD
errorStatusAttribs = curses.color_pair(7) | curses.A_BLINK | curses.A_BOLD
headerAttribs = curses.color_pair(1)
contentAttribs = curses.color_pair(2)
uninterestingContAttribs = contentAttribs | curses.A_DIM
interestingContAttribs = contentAttribs | curses.A_BOLD
footerAttribs = headerAttribs


# data fetch/grab interval in seconds
# NOTE that the display will be updated even if no new data is available,
#   simply to update the time-relevant values.
# default: 60  # = 1min
global update_interval
update_interval = 60


# Whether to use a compact display, or the whole space available on the terminal
compact_display = False

global header_rows
global footer_rows
header_rows = 0
footer_rows = 0

global nCols # number of chars the table should occupy
global nRows # number of rows the table should occupy
nCols = curses.COLS - 1 # all available columns
if compact_display:
    if len(stations) == 1:
        nCols = min(nCols, 40)
    else:
        nCols = min(nCols, 60)

nRows = curses.LINES - 1 # all available lines
if compact_display:
    if len(stations) == 1:
        nRows = min(nRows - header_rows - footer_rows, 10)
    else:
        nRows = min(nRows - header_rows - footer_rows, 15)
