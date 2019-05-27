#!/bin/bash

source /home/pi/.profile
workon cv
python3 /home/pi/Desktop/PersonalizedGreeter/src/decider.py #>> /home/pi/bootlogs.txt 2>&1
