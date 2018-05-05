#!/usr/bin/env python3


import RPi.GPIO as GPIO
import subprocess
import multilineMAX7219 as LEDMatrix

GPIO.setmode(GPIO.BOARD)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(5, GPIO.FALLING)

GPIO.cleanup()
LEDMatrix.clear_all()
subprocess.call(['shutdown', '-h', 'now'], shell=False)
