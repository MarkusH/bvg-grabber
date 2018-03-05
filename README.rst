.. image:: https://img.shields.io/pypi/dm/bvg-grabber.svg
    :target: https://pypi.python.org/pypi/bvg-grabber/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/v/bvg-grabber.svg
    :target: https://pypi.python.org/pypi/bvg-grabber/
    :alt: Latest Version

.. image:: https://travis-ci.org/MarkusH/bvg-grabber.svg?branch=develop
    :target: https://travis-ci.org/MarkusH/bvg-grabber
    :alt: Development branch


===========
bvg-grabber
===========

Showing BVG Departures In Your Office
=====================================

Blog post:
  https://markusholtermann.eu/2013/06/showing-bvg-departures-in-your-office/
  
Slides:
  https://speakerdeck.com/markush/showing-bvg-departures-in-your-office

Pictures:
  .. image:: https://markusholtermann.eu/images/BVG-Grabber-LightningTalk-installation1tb.jpg
      :alt: Installation 1
    
  .. image:: https://markusholtermann.eu/images/BVG-Grabber-LightningTalk-installation2tb.jpg
      :alt: Installation 2


Installation
============

Requires Python 3!

To use *bvg-grabber* go and install it as you do with every Python package::

    $ pip install bvg-grabber

or::

    $ pip install --user bvg-grabber


Usage
=====

*bvg-grabber* comes with a simple command line tool ``bvg-grabber.py``::

    $ bvg-grabber.py --help
    usage: bvg-grabber.py [-h]
                        [--vehicle [{S,U,TRAM,BUS,FERRY,RB,IC} [{S,U,TRAM,BUS,FERRY,RB,IC} ...]]]
                        [--limit LIMIT]
                        station file

    Query the BVG-website for departures

    positional arguments:
    station               The station to query
    file                  Path to file. Use - for stdout

    optional arguments:
    -h, --help            show this help message and exit
    --vehicle [{S,U,TRAM,BUS,FERRY,RB,IC} [{S,U,TRAM,BUS,FERRY,RB,IC} ...]]
                            Vehicles which shall be queried, if non given
                            actualdepartue (bus) will be used
    --limit LIMIT         Max departures to query. Default: 9


Example::

    $ bvg-grabber.py "U Ernst-Reuter-Platz (Berlin)" - --vehicle U --limit 2 | json_pp
    [
       [
          "U Ernst-Reuter-Platz (Berlin)",
          [
             {
                "line" : "U2",
                "end" : "U Ruhleben (Berlin)",
                "remaining" : 12180,
                "start" : "U Ernst-Reuter-Platz (Berlin)"
             },
             {
                "line" : "U2",
                "start" : "U Ernst-Reuter-Platz (Berlin)",
                "remaining" : 12600,
                "end" : "S+U Pankow (Berlin)"
             }
          ]
       ]
    ]
