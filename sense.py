#!/usr/bin/env python

from datetime import datetime, timedelta
from time import sleep
import RPi.GPIO as GPIO
import sys

def forever(): return sys.float_info.max

def motion_pin(): return 18
def door_pin(): return 23
def light_pin(): return 25

def motion_callback(channel):
    now = datetime.utcnow()
    print '%s motion channel=%s' % (now.isoformat(), channel)

def door_callback(channel):
    now = datetime.utcnow()
    sleep(0.1)
    rd = GPIO.input(channel)
    print '%s door %s channel=%s' % (
        now.isoformat(), 'open' if rd else 'closed', channel)

def light_changed(channel):
    sleep(0.1)
    rd = GPIO.input(channel)
    now = datetime.utcnow()
    print '%s light turned %s (channel=%s)' % (
        now.isoformat(), 'on' if rd else 'off', channel)

print 'GPIO setup...'
GPIO.setmode(GPIO.BCM)
GPIO.setup(motion_pin(), GPIO.IN) # activate input
GPIO.setup(door_pin(), GPIO.IN, pull_up_down=GPIO.PUD_UP) # activate input with PullUp
GPIO.setup(light_pin(), GPIO.IN)

print 'GPIO init readings...'
print 'light is %s' % ('on' if GPIO.input(light_pin()) else 'off')
print 'door is %s' % ('open' if GPIO.input(door_pin()) else 'closed')

print 'GPIO listening...'
GPIO.add_event_detect(motion_pin(), GPIO.BOTH, callback=motion_callback, bouncetime=500)
GPIO.add_event_detect(door_pin(), GPIO.RISING, callback=door_callback, bouncetime=500)
GPIO.add_event_detect(light_pin(),
                      GPIO.BOTH,
                      callback=light_changed,
                      bouncetime=200)

print 'waiting...'

try:
    sleep(forever())
except KeyboardInterrupt:
    pass
except Exception as e:
    # unexpected
    print e
finally:
    GPIO.cleanup()
    print 'done.'

