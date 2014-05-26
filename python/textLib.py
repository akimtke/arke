# -*- coding: utf-8 -*-

from serialDriver import serialDriver

class textLib(object):
    def __new__(cls, sd):
        if sd is None:
            raise ValueError
        else:
            return super(textLib, cls).__new__(cls)

    def __init__(self, sd):
        self.sd = sd

    def sendText(self, text):
        self.sd.send("AT+CMGF=1\r\n")
        if self.sd.checkSuccess():
            self.sd.send("AT+CMGS=\"" + text.number + "\"\r\n")
            if self.sd.checkForPrompt():
                self.sd.send(text + "\x1A\r\n")
                if self.sd.checkSuccess():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
