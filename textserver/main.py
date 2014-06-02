# -*- coding: utf-8 -*-

import pyjsonrpc
from gsmmodem.modem import GsmModem, SentSms
from gsmmodem.exceptions import TimeoutException, PinRequiredError, IncorrectPinError

def text(number, message):
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
        return False
    else:
        try:
            print "Sending sms"
            sms = modem.sendSms(number, message)
        except TimeoutException:
            print "Failed to send message"
            return False
        else:
            print "Closing modem"
            modem.close()
            return True

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    methods = {
            "text": text
            }

http_server = pyjsonrpc.ThreadingHttpServer(
        server_address = ('localhost', 8080),
        RequestHandlerClass = RequestHandler
        )
print "Starting HTTP Server..."
http_server.serve_forever()
