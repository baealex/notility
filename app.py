import module.function as fn
import module.google.analytics as ga

from module import settings

from flask import (
    Flask, request, render_template, send_file, make_response, session, abort)

application = Flask(__name__)
application.debug = settings.DEBUG
application.secret_key = settings.SECRET_KEY

def read_content(m_file):
    with open(m_file, 'r') as read_file:
        return fn.parsedown(read_file.read())

index_list = [
    ['/', '😀 노션 도우미'],
    ['/docs/guide', '📒 노션 가이드'],
    ['/docs/google-analytics', '🌈 노션 구글 애널리틱스']
]

@application.route("/")
def docs_main():
    title = index_list[0][1]
    content = read_content('README.md')
    return render_template('docs.html', title=title, content=content, index_list=index_list)

@application.route("/docs/<name>")
def docs_basic(name):
    docs = {
        'guide': {
            'title': index_list[1][1],
            'file': 'docs/guide.md',
        },
        'google-analytics': {
            'title': index_list[2][1],
            'file': 'docs/google-analytics.md',
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

@application.route("/ga", methods=['HEAD', 'GET'])
def google_analytics():
    try:
        request.args['id']
        request.args['host']
        request.args['path']
    except:
        print('Request - Invalid Parameter')
        return 'Invalid Parameter'

    if not request.method == 'GET':
        print('Request - Invalid Method')
        return 'Invalid Method'
    
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    blacklist = """
    52.36.186.228|
    """

    if user_ip in blacklist:
        print('Request : Blacklist User')
        return send_file('assets/blank.png', mimetype='image/png')

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
    hide = request.args.get('hide', False)
    if hide == 'true':
        return send_file('assets/blank.png', mimetype='image/png', cache_timeout=-1)
    return send_file('assets/ga.png', mimetype='image/png', cache_timeout=-1)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=15000)