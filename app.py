import os
import json
import datetime

import module.function as fn
import module.google.analytics as ga

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

@application.route("/comment/<pk>", methods=['GET', 'POST'])
def comment(pk):
    file_name = 'data/' + pk + '.json'
    file_data = list()

    if os.path.isfile(file_name): 
        with open(file_name, 'r') as read_file:
            file_data = json.load(read_file)
    
    if request.method == 'POST':
        file_data.append({
            'nickname': request.form['nickname'],
            'content': request.form['content'],
            'created': str(datetime.datetime.now()),
        })
        with open(file_name, "w") as json_file:
            json.dump(file_data, json_file)

    return render_template('comment.html', comments=reversed(file_data))

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=15000)