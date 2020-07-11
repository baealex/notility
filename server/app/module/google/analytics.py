import requests as req

def measurement_protocol(tid, cid, host, path, uip=None, agent=None, referer=None):
    data = {
        'v': '1',
        'tid': tid,
        'cid': cid,
        't': 'pageview',
        'dh': host,
        'dp': path
    }

    if uip:
        data.update({'uip': uip})

    if agent:
        data.update({'ua': agent})
    
    if referer:
        data.update({'dr': referer})
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    res = req.post('http://www.google-analytics.com/collect', data=data, headers=headers)
    return res