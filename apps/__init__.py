from flask import Flask
from apps.account.views import account
from apps.ext import init_ext


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = 'sadasdasd1213231123'
    init_ext(app)
    register_bp(app)
    return app


def register_bp(app):
    app.register_blueprint(account)
