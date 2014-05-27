# -*- coding: utf-8 -*-

from serialDriver import serialDriver
from text import text
from textLib import textLib
from sys import argv

script, number, message = argv

print "Number: " + number
print "Message: " + message

serD = serialDriver("/dev/ttyUSB0", 9600)
serD.open()
if serD.err:
    print serD.errMessage
else:
    texter = textLib(serD)

    t1 = text(number, message)

    res = texter.sendText(t1)

    if not res:
        print "Error texting"

    if serD.err:
        print serD.errMessage
