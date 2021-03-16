import os
import json
import urllib
import datetime

import settings
import module.function as fn
import module.google.analytics as ga

from module import hcaptcha

from flask import (
    request, render_template, send_file,
    make_response, session, abort, redirect)

def index():
    return redirect('https://www.notion.so/28dc1eb045974dab998c40c11f85c2aa')

def google_analytics_creator():
    return render_template('creator.html')

def google_analytics():
    try:
        request.args['id']
        request.args['host']
        request.args['path']
    except:
        return send_file('assets/blank.png', mimetype='image/png')

    if not request.method == 'GET':
        return send_file('assets/blank.png', mimetype='image/png')

    uip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    cid = None
    if not 'cid' in session:
        session['cid'] = fn.make_cid()
    cid = session['cid']
    
    ga.measurement_protocol(
        tid = request.args['id'],
        cid = cid,
        host = request.args['host'],
        path = request.args['path'],
        uip = uip,
        agent = request.headers.get('User-Agent', None),
    )
    hide = request.args.get('hide', False)
    if hide == 'true':
        return send_file('assets/blank.png', mimetype='image/png', cache_timeout=-1)
    return send_file('assets/ga.png', mimetype='image/png', cache_timeout=-1)

def utterances(username, repository, pk):
    theme = request.args.get('theme', 'light')
    parameter = {
        'src': 'https://utteranc.es/client.js',
        'repo': f'{username}/{repository}',
        'issue-term': 'pathname',
        'theme': f'github-{theme}',
        'origin': 'https://www.notion.so',
        'crossorigin': 'anonymous',
        'pathname': pk,
        'url': request.base_url
    }
    return redirect(f'https://utteranc.es/utterances.html?{urllib.parse.urlencode(parameter)}')

def light_comment(pk):
    print(pk)
    file_name = f'data/{pk}.json'
    file_data = []

    if os.path.isfile(file_name): 
        with open(file_name, 'r', encoding='utf-8') as read_file:
            file_data = json.load(read_file)
            if not file_data:
                file_data = []
    
    if request.method == 'POST':
        captcha = request.form['captcha']
        is_vaild = hcaptcha.verify(captcha)
        if not is_vaild:
            return 'TOKEN VERIFY FAIL'

        file_data.append({
            'nickname': request.form['nickname'],
            'content': request.form['content'],
            'created': str(datetime.datetime.now()),
        })
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(file_data, json_file)

    return render_template('comment/index.html', comments=reversed(file_data), pk=pk, client_key=settings.HCAPTCHA_CLIENT_KEY)