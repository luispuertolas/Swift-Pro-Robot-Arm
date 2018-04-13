#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2017, UFactory, Inc.
# All rights reserved.
#
# Author: Duke Fong <duke@ufactory.cc>


import sys, os, serial
from time import sleep

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *

ser = serial.Serial('COM5', baudrate=115200)

#logger_init(logging.VERBOSE)
#logger_init(logging.DEBUG)
logger_init(logging.INFO)

print('setup swift ...')

#swift = SwiftAPI(dev_port = '/dev/ttyACM0')
#swift = SwiftAPI(filters = {'hwid': 'USB VID:PID=2341:0042'})
swift = SwiftAPI() # default by filters: {'hwid': 'USB VID:PID=2341:0042'}


print('sleep 2 sec ...')
sleep(2)

print('device info: ')
swift.set_position(150, 0, 150, speed = 5000, timeout = 20)
swift.flush_cmd()
# wait all async cmd return before send sync cmd
y=0
x=150
while True:
    line = ser.readline()
    try:
        line = line.decode()
        for w in range(len(line)):
            if line[w] == ",":
                xpos = line[:w]
                ypos = line[w+2:len(line)]
                print(xpos,",", ypos)
                if int(xpos) < 159:
                    y = y - 1
                    swift.set_position(150, int(y), 150, speed = 5000)       
                if int(xpos) > 161:
                    y = y + 1
                    swift.set_position(150, int(y), 150, speed = 5000)                
                if int(xpos) > 159 and int(xpos) < 161:
                    exitloop=0
                    while exitloop == 0:
                            line = ser.readline()
                            try:
                                line = line.decode()
                                for w in range(len(line)):
                                    if line[w] == ",":
                                        xpos = line[:w]
                                        ypos = line[w+2:len(line)]
                                        print(xpos,",", ypos)
                                        if int(ypos) < 119:
                                            x = x - 1
                                            swift.set_position(int(x), int(y), 150, speed = 5000)       
                                        if int(ypos) > 121:
                                            x = x + 1
                                            swift.set_position(int(x), int(y), 150, speed = 5000)                            
                                        if int(ypos) > 119 and int(ypos) < 121:
                                            swift.set_position(int(x), int(y), -112, speed = 5000)
                                            exitloop = 1
                            except:
                                x=x                    
    except:
        x=x


