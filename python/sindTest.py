# -*- coding: utf-8 -*-

import serial

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)

while(1):
    ser.write("AT+SIND?\r\n")
    if ser.inWaiting() > 0:
        res = ser.read(ser.inWaiting())
        print "res: " + repr(res)
        fp = open('sindTest.txt', 'a')

        fp.write(repr(res) + "\n")
        fp.close()
