import os
import json
import datetime

import module.function as fn
import module.google.analytics as ga

from module.google.spreadb import GspreaDB
from module import settings

from flask import (
    Flask, request, render_template, send_file, make_response, session, abort, redirect)

application = Flask(__name__)
application.debug = settings.DEBUG
application.secret_key = settings.SECRET_KEY

@application.route("/")
def docs_main():
    return redirect('https://www.notion.so/28dc1eb045974dab998c40c11f85c2aa')

@application.route("/ga/creator")
def google_analytics_creator():
    return render_template('creator.html')

@application.route("/ga", methods=['HEAD', 'GET'])
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

@application.route("/ut/<username>/<repository>/<pk>", methods=['GET'])
def utterances(username, repository, pk):
    theme = request.args.get('theme', 'light')
    return render_template('utterances.html', username=username, repository=repository, pk=pk, theme=theme)

@application.route("/lc/<pk>", methods=['GET', 'POST'])
def light_comment(pk):
    db = GspreaDB()
    comments_data = db.get_value(pk)
    if comments_data:
        comments_data = json.loads(comments_data)
    else:
        comments_data = list()
    
    if request.method == 'POST':
        uip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        primary_key = fn.hashing(request.form['content'].encode())
        has_key = False
        for comment in comments_data:
            if comment['pk'] == primary_key:
                has_key = True
                break
        if not has_key:
            comments_data.append({
                'pk': primary_key,
                'nickname': request.form['nickname'],
                'content': request.form['content'],
                'created': str(datetime.datetime.now()),
                'uip': uip
            })
            db.update_value(pk, json.dumps(comments_data))

    return render_template('comment.html', comments=reversed(comments_data), pk=pk)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)