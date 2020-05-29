import module.function as fn
import module.google.analytics as ga

from module import settings

from flask import (
    Flask, request, render_template, send_file, session, abort)

application = Flask(__name__)
application.debug = settings.DEBUG
application.secret_key = settings.SECRET_KEY

def read_content(m_file):
    with open(m_file, 'r') as read_file:
        return fn.parsedown(read_file.read())

index_list = [
    ['/', '😀 Notion Doumi'],
    ['/docs/guide', '📒 Notion Guide'],
    ['/docs/google-analytics', '🌈 Google Analytics']
]

@application.route("/")
def docs_main():
    title = 'Notion Doumi'
    content = read_content('README.md')
    return render_template('docs.html', title=title, content=content, index_list=index_list)

@application.route("/docs/<name>")
def docs_basic(name):
    docs = {
        'guide': {
            'title': 'Notion Guide',
            'file': 'docs/guide.md',
        },
        'google-analytics': {
            'title': 'Notion Analytics',
            'file': 'docs/google_analytics.md',
        }
    }
    if name in docs:
        title = docs[name]['title']
        content = read_content(docs[name]['file'])
        return render_template('docs.html', title=title, content=content, index_list=index_list)
    abort(404)

@application.route("/ga/creator")
def google_analytics_creator():
    return render_template('creator.html')

@application.route("/ga")
def google_analytics():
    try:
        request.args['id']
        request.args['host']
        request.args['path']
    except:
        return 'Invalid Parameter'

    cid = fn.randstr(10)
    if 'cid' in session:
        cid = session['cid']
    else:
        session['cid'] = cid

    ga.measurement_protocol(
        tid = request.args['id'],
        cid = cid,
        host = request.args['host'],
        path = request.args['path'],
        agent = request.headers.get('User-Agent', None),
    )
    return send_file('assets/ga.png', mimetype='image/png', cache_timeout=-1)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=15000)