import views

def routing(app):
    @app.route("/")
    def rt(**arg): return views.index(**arg)

    @app.route("/ga/creator")
    def gc(**arg): return views.google_analytics_creator(**arg)

    @app.route("/ga", methods=['HEAD', 'GET'])
    def ga(**arg): return views.google_analytics(**arg)

    @app.route("/ut/<username>/<repository>/<pk>", methods=['GET'])
    def ut(**arg): return views.utterances(**arg)

    @app.route("/lc/<pk>", methods=['GET', 'POST'])
    def lc(**arg): return views.light_comment(**arg)