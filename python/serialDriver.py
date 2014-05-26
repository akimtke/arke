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
            while (to > 0) and not stat:
                stat = self.readState()
                time.sleep(1)

            if not stat:
                self.err = True
                self.errMessage = "Something went wrong when initializing the GSM module"
            else:
                self.ser.write("AT+SBAND=8\r\n")
        except Exception as e:
            self.err = True
            self.errMessage = str(e)

    def close(self)):
        self.ser.close()

    def sendText(self, text):
        if ser.isOpen():
            ser.write('AT+CMGF=1\r\n')
            to = 5
            while(to > 0):
                to = to - 1
                res = ser.readline()
                if "OK" in res:
                    break
            if to > 0:
                return False

            ser.write('AT+CMSG="' + text.number + '"\r\n' + text.message + '\x1A\r\n')
            to = 5
            while(to > 0):
                to = to - 1
                res = ser.readline()
                if "OK" in res:
                    break
            if to > 0:
                return False

            return True

    # This function should not execute if the error condition is set.
    def send(self, command):
        if not self.err:
            if self.ser.isOpen():
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

                if "OK" in res:
                    return True
                else
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

    def readState():
        sIn = False
        sRdy = False
        net = False
        cRdy = False
        mRdy = False

        res = self.ser.read(self.ser.inWaiting())

        res = res.strip()
        res = res.replace("\r\n\r\n", "\r\n")

        results = res.split("\r\n")

        for code in results:
            if code == '+SIND: 1':
                sIn = True
            elif code == '+SIND: 10,"SM",1,"FD",1,"LD",1,"MC",1,"RC",1,"ME",1':
                sRdy = True
            elif code == '+SIND: 11':
                net = True
            elif code == '+SIND: 3':
                cRdy = True
            elif code == '+SIND: 4':
                mRdy = True

        return (sIn and sRdy and net and cRdy and mRdy)
