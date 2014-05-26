# -*- coding: utf-8 -*-

class text(object):
    def __new__(self, number, message):
        try:
            number = checkLength(str(number))
        except Exception as e:
            raise e

    def __init__(self, number, message):
        self.number = self.checkLength(str(number))
        self.message = message

    @staticmethod
    def checkLength(number):
        if len(number) < 11:
            if len(number) == 10:
                number = '1' + number
            else:
                raise ValueError
