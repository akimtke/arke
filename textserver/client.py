# -*- coding: utf-8 -*-

import pyjsonrpc

http_client = pyjsonrpc.HttpClient(
        url = "http://localhost:8080"
)

#print http_client.add(1, 2)
#print http_client.call("text", '9705811816', 'Testing server')
try:
    print http_client.text("7209846289", "Check it out! I got the texting working through a network connection!")
except Exception as e:
    print str(e)
