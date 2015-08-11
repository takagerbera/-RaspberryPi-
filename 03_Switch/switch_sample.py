#!/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

led_port = 24
btn_port = 18

if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(led_port, GPIO.OUT)
    GPIO.setup(btn_port, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    print "Hello, World!"
    print "push to Switch..."

    while True:
        try:
            if GPIO.input(btn_port):
                GPIO.output(led_port, 1)
            else:
                GPIO.output(led_port, 0)
        except KeyboardInterrupt:
            print "\nbyebye."
            break

    GPIO.cleanup()
