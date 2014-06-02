# -*- coding: utf-8 -*-

class text(object):
    def __new__(cls, number, message):
        try:
            number = text.checkLength(str(number.strip()))
        except Exception as e:
            raise e
        return super(text, cls).__new__(cls)

    def __init__(self, number, message):
        self.number = number
        self.message = message.strip()

    @staticmethod
    def checkLength(number):
        if len(number) < 11:
            if len(number) == 10:
                number = '1' + number
            else:
                raise ValueError
