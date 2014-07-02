# -*- coding: utf-8 -*-

import pyjsonrpc
from gsmmodem.modem import GsmModem, SentSms, Sms
from gsmmodem.exceptions import TimeoutException, PinRequiredError, IncorrectPinError

def text(number, message, key):
    if key.strip() == '9703BB8D5A':
        print "Creating modem instance"
        modem = GsmModem('/dev/ttyUSB0', 9600)

        try:
            print "Connecting modem"
            modem.connect()
        except PinRequiredError:
            print "Pin required"

        try:
            print "Waiting for Network coverage info"
            modem.waitForNetworkCoverage(5)
        except TimeoutException:
            print "Signal strength not strong enough"
            return "No signal"
        else:
            try:
                print "Sending %s to %s" % (message, number)
                sms = modem.sendSms(number, message)
            except TimeoutException:
                print "Failed to send message"
                return 'Error encountered'
            print "Closing modem"
            modem.close()
            return True
    else:
        return 'Key is not correct'

def getUnreadText(key):
    if key.strip() == '9703BB8D5A':
        modem = GsmModem('/dev/ttyUSB0', 9600)

        try:
            print "Connecting mode"
            modem.connect()
        except:
            return "Error connecting"

        try:
            messages = modem.listStoredSms(status=Sms.STATUS_RECEIVED_UNREAD)
        except Exception as e:
            return str(e)

        modem.close()

        retString = ""
        print "Got %d messages" % len(messages)
        for message in messages:
            retString = retString + "%s : %s" % (message.number, message.text)

        return retString
    else:
        return "Incorrect key"

def getAllText(key):
    if key.strip() == '9703BB8D5A':
        modem = GsmModem('/dev/ttyUSB0', 9600)

        try:
            print "Connecting modem"
            modem.connect()
        except Exception as e:
            return str(e)

        try:
            messages = modem.listStoredSms()
        except Exception as e:
            return str(e)

        modem.close()

        retString = ""
        print "Got %d messages" % len(messages)
        for message in messages:
            retString = retString + "%s : %s" % (message.number, message.text) + "\n"

        return retString
    else:
        return "Incorrect key"

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    methods = {
            "text": text,
            "getUnreadText": getUnreadText,
            "getAllText": getAllText
            }

http_server = pyjsonrpc.ThreadingHttpServer(
        server_address = ('192.168.0.20', 8081),
        RequestHandlerClass = RequestHandler
        )
print "Starting HTTP Server..."
http_server.serve_forever()
