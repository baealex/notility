import axios from 'axios'
import { Request, Response } from 'express'
import syspath from 'path'
import { v4 } from 'uuid'

export function serialize(obj: {
    [key: string]: any
}) {
    return Object.keys(obj).reduce((acc, cur) => {
        return acc += `${cur}=${obj[cur] === undefined ? '' : encodeURIComponent(obj[cur])}&`;
    }, '').slice(0, -1)
}

export async function googleAnalytics(req: Request, res: Response) {
    const {
        id = '',
        host = '',
        path = '',
    } = req.query;

    if (!id || !host || !path) {
        res.send('unvalid requests.').end()
    }

    const uuid = req.cookies?.uuid || v4();
    if (!req.cookies?.uuid) {
        res.cookie('uuid', uuid, {
            expires: new Date(Date.now() + 1000 * 3600 * 24 * 7),
            httpOnly: true,
        })
    } 

    res.set({'Content-Type': 'image/png'})
    if (req.query.hide) {
        res.sendFile(syspath.resolve('./assets/hide.png'))
    }
    res.sendFile(syspath.resolve('./assets/show.png'))

    const referer = req.headers['referer']
    const userAgent = req.headers['user-agent']
    const userAddress = req.headers['x-forwarded-for'] || req.connection.remoteAddress

    await axios.request({
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        url: 'http://www.google-analytics.com/collect',
        data: serialize({
            'v': '1',
            'tid': id,
            'cid': uuid,
            't': 'pageview',
            'dh': host,
            'dp': path,
            'uip': userAddress, 
            'ua': userAgent,
            'dr': referer, 
        })
    })
}