import settings

from urls import routing
from flask import Flask

application = Flask(__name__)
application.debug = settings.DEBUG
application.secret_key = settings.SECRET_KEY

routing(application)    

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)