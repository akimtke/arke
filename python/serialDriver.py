# -*- coding: utf-8 -*-

import serial
import time

class serialDriver(object):
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.err = False
        self.errMessage = ""

    def open(self):
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=1)

            stat = False
            time.sleep(15)
            to = 10
            self.sIn = False
            self.sRdy = False
            self.net = False
            self.cRdy = False
            self.mRdy = False

            while (to > 0) and not stat:
                stat = self.readState()
                to = to - 1
                time.sleep(1)

            if not stat:
                self.err = True
                self.errMessage = "Something went wrong when initializing the GSM module"
            else:
                time.sleep(2)
                self.send("AT+SBAND=8\r\n")
                if not self.checkSuccess():
                    self.err = True
                    self.errMessage = "Failed to set the frequency of the module"
        except Exception as e:
            self.err = True
            self.errMessage = str(e)

    def close(self):
        self.ser.close()

    # This function should not execute if the error condition is set.
    def send(self, command):
        if not self.err:
            if self.ser.isOpen():
                print "Sending: " + command
                self.ser.write(command)
                return True
            else:
                self.err = True
                self.errMessage = "Serial port was not opened. Try reopening."
                return False
        else:
            return False

    # Reads the receiving buffer and splits it into a list. Use this if more information is needed instead of a pass/fail.
    def readIntoArr(self):
        if not self.err:
            results = ""
            if self.ser.isOpen():
                res = self.ser.read(self.ser.inWaiting())
                res = res.strip()
                res = res.replace("\r\n\r\n", "\r\n")

                results = res.split("\r\n")

            else:
                self.err = True
                self.errMessage = "Serial port was not opened. Try reopening."
                results = False

            return results
        else:
            return False

    # This function checks the receiving buffer for an OK message sent back from the GSM module. If it is found, then
    # True is returned. Make sure to also check the error flag when checking the output of this data as the meaning can
    # change.
    def checkSuccess(self):
        if not self.err:
            if self.ser.isOpen():
                res = self.ser.read(self.ser.inWaiting())

                print res

                if "OK" in res:
                    return True
                else:
                    return False
            else:
                self.err = True
                self.errMessage = "Serial port was not open. Try reopening."
                return False
        else:
            return False

    def checkForPrompt(self):
        if not self.err:
            if self.ser.isOpen():
                res = self.ser.read(self.ser.inWaiting())
                res = res.strip()
                if ">" in res:
                    return True
                else:
                    return False
            else:
                self.err = True
                self.errMessage = "Serial port got closed. Try reopening."
                return False
        else:
            return False

    def reset(self):
        self.err = False
        self.errMessage = ""
        if self.ser.isClosed():
            self.open()

    def readState(self):

        res = self.ser.read(self.ser.inWaiting())

        res = res.strip()
        res = res.replace("\r\n\r\n", "\r\n")

        results = res.split("\r\n")

        for code in results:
            if code == '+SIND: 1':
                self.sIn = True
            elif code == '+SIND: 10,"SM",1,"FD",1,"LD",1,"MC",1,"RC",1,"ME",1':
                self.sRdy = True
            elif code == '+SIND: 11':
                self.net = True
            elif code == '+SIND: 3':
                self.cRdy = True
            elif code == '+SIND: 4':
                self.mRdy = True

        return (self.sIn and self.sRdy and self.net and self.cRdy and self.mRdy)
