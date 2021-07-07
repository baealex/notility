import express from 'express'
import cookieParser from 'cookie-parser'

import logging from './modules/logging'
import asyncWrap from './modules/async-wrap'
import * as views from './views'

express()
    .use(logging())
    .use(cookieParser())
    .get('/', (_, res) => res.redirect('https://www.notion.so/28dc1eb045974dab998c40c11f85c2aa'))
    .get('/ga', asyncWrap(views.googleAnalytics))
    .listen(3000, () => console.log('http server listen on :3000'))