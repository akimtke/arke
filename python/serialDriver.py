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
                while self.ser.inWaiting() == 0:
                    time.sleep(1)
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
                while self.ser.inWaiting() == 0:
                    time.sleep(1)
                res = self.ser.read(self.ser.inWaiting())

                print repr(res)

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
                while self.ser.inWaiting() == 0:
                    time.sleep(1)
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
        to = 10
        ret = False
        running = ""

        while to < 10 and not ret:
            if self.ser.inWaiting() > 0:
                res = self.ser.read(self.ser.inWaiting())
                running = running + res
                if "+SIND: 4" in res:
                    ret = True

        if not ret:
            self.err = True
            self.errMessage = "DUMP: " + running
        return ret
