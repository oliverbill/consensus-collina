#!/usr/bin/python
from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config_map

db = SQLAlchemy()
login_manager = LoginManager()
## keep track of the client’s IP address and browser agent and will log the user out if it detects a change
login_manager.session_protection = 'strong'
## sets the endpoint for the login page
login_manager.login_view = 'auth.login'
moment = Moment()
admin = Admin()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])
    config_map[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

# inicializa Flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    admin.init_app(app)
# retorna app configurada
    return app