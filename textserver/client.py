# -*- coding: utf-8 -*-

import pyjsonrpc

http_client = pyjsonrpc.HttpClient(
        url = "http://localhost:8081"
)

try:
    print http_client.text("number", "Teswtingergb")
except Exception as e:
    print str(e)
