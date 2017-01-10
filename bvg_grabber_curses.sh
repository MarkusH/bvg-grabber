#!/bin/sh
# Starts the BVG grabber TUI in a suitable terminal emulator.

xterm \
	+dc \
	-b 0 \
	-bc \
	+cm \
	+hold \
	+l \
	-lc \
	+nul \
	-pc \
	-ulc \
	-ulit \
	-fullscreen \
	-font -*-fixed-medium-r-*-*-40-*-*-*-*-*-iso8859-* \
	-geometry 60x20 \
	-e python3 bvg_grabber_curses.py $*

