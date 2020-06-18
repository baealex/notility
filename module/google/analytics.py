import requests as req

def measurement_protocol(tid, uid, uip, host, path, agent=None, referer=None):
    data = {
        'v': '1',
        'tid': tid,
        'uid': uid,
        'uip': uip,
        't': 'pageview',
        'dh': host,
        'dp': path
    }

    if agent:
        data.update({'ua': agent})
    
    if referer:
        data.update({'dr': referer})
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    res = req.post('http://www.google-analytics.com/collect', data=data, headers=headers)
    return res