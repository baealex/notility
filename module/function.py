import random
import requests as req

from . import settings

def randstr(length):
    rstr = '0123456789abcdefghijklnmopqrstuvwxyz'
    rstr_len = len(rstr) - 1
    result = ''
    for i in range(length):
        result += rstr[random.randint(0, rstr_len)]
    return result

def parsedown(text):
    data = {'md': text.encode('utf-8')}
    res = req.post(settings.API_URL + '/api/parsedown/get.php', data=data)
    if res.status_code == 200:
        return res.text
    else:
        return 'Temporary error'