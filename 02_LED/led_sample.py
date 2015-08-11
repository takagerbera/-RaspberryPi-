#!/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time

port = 18

if __name__ == "__main__":

  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)

  GPIO.setup(port, GPIO.OUT)

  print "Hello, World!\nPress Ctrl+C to Exit"

  while True:
    try:      
      GPIO.output(port, 1)
      time.sleep(1)
      GPIO.output(port, 0)
      time.sleep(1)
    except:
      print "\nbyebye."
      break

  GPIO.cleanup()

