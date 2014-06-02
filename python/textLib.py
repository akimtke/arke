# -*- coding: utf-8 -*-

from serialDriver import serialDriver
from text import text

class textLib(object):
    def __new__(cls, sd):
        if sd is None:
            raise ValueError
        else:
            return super(textLib, cls).__new__(cls)

    def __init__(self, sd):
        self.sd = sd

    def sendText(self, text):
        status = False
        while not status:
            self.sd.send("AT+CSCA?\r\n")
            status = self.sd.checkSuccess()
        self.sd.send("AT+CMGF=1\r\n")
        if self.sd.checkSuccess():
            self.sd.send("AT+CMGS=\"" + text.number + "\"\r\n")
            if self.sd.checkForPrompt():
                self.sd.send(text.message +chr(26) + "\r\n")
                if self.sd.checkSuccess():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
