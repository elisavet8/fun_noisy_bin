#!/usr/bin/env python
# ---------------------------------------------------------
# Filename: multilineMAX7219_demo.py
# ---------------------------------------------------------
# Demonstration of the features in the multilineMAX7219 library
#
# v1.0
# F.Stern 2014
# ---------------------------------------------------------
# improved and extended version of JonA1961's MAX7219array
# ( https://github.com/JonA1961/MAX7219array )
# ---------------------------------------------------------
# See multilineMAX7219.py library file for more details
# ---------------------------------------------------------
# This demo script is intended to run on an array of 9 (3x3)
#   MAX7219 boards, connected as described in the library
#   script. 
# The variables MATRIX_WIDTH and MATRIX_HEIGHT, defined in the 
#	multilineMAX7219.py library script, should always be set to be 
#	consistent with the actual hardware setup in use.  If it is 
#	not set correctly, then the functions will not work as
#   intended
# ---------------------------------------------------------

    LEDMatrix.clear_all()
