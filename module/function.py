import random
import requests as req

from . import settings

def randstr(length):
    rstr = '0123456789abcdef'
    rstr_len = len(rstr) - 1
    result = ''
    for i in range(length):
        result += rstr[random.randint(0, rstr_len)]
    return result

def make_cid():
    return randstr(8) + '-' + randstr(4) + '-' + randstr(4) + '-' + randstr(4) + '-' + randstr(12)