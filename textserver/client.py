# -*- coding: utf-8 -*-

import pyjsonrpc

http_client = pyjsonrpc.HttpClient(
        url = "http://akim-RLE:8081"
)

try:
    print http_client.text("9705811816", "Teswtingergb")
except Exception as e:
    print str(e)
