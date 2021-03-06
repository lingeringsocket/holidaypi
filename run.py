#!/usr/bin/python
# Adapted from https://bitbucket.org/MattHawkinsUK/rpispy-video-capture-unit

import os
import time
import datetime
import RPi.GPIO as GPIO
import picamera

import config

def GetFileName():
    filename = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    return filename


print "Holiday Pi"

ButtonCounter = 0

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(config.BUTTONGPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Create camera object and setup
camera = picamera.PiCamera()
camera.framerate  = config.VIDEO_FRAMERATE
camera.resolution = config.VIDEO_RESOLUTION
camera.led = False
camera.vflip = config.VIDEO_VFLIP
camera.rotation = config.VIDEO_ROTATE

print "Camera ready"

debounce = False
recording = False
need_thumbnail = True
poll_interval = 0.2

# Run until Control-C
try:
    while True:
        if recording:
            if debounce or (GPIO.input(config.BUTTONGPIO)==1):
                debounce = False
                camera.wait_recording(poll_interval)
            else:
                print "  Stop recording"
                debounce = True
                recording = False
                camera.led = False
                camera.stop_recording()
        else:
            if debounce or (GPIO.input(config.BUTTONGPIO)==0):
                debounce = False
                time.sleep(poll_interval)
            else:
                debounce = True
                recording = True
                filename = GetFileName()
                start_time = time.time()
                camera.led = True
                if need_thumbnail:
                    need_thumbnail = False
                    camera.capture(os.path.join(config.VIDEO_PATH,'thumbnail.jpg'), use_video_port=True)
                stamp = datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S')
                print 'Start recording : ' + stamp + ' : ' + filename + '.h264'
                camera.start_recording(os.path.join(config.VIDEO_PATH,filename + '.h264'))
except KeyboardInterrupt:
    camera.led = False
    camera.close()
    print "Camera closed"
