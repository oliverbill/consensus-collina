#!/usr/bin/python
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

######################################## ATENÇÃO ##########################################

# executar no MYSQL:
# ALTER DATABASE consensus-collina CHARACTER SET utf8 COLLATE utf8_general_ci;
# para aceitar caracteres pt_br

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    ADMIN_USER = os.environ.get('ADMIN_USER')
    ALLOWED_EXTENSIONS = set(['pdf', 'jpeg', 'bmp', 'jpg', 'png', 'gif', 'txt', 'doc', 'docx', 'xls', 'xlsx'])
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = os.environ.get('CONSENSUS_UPLOAD_FOLDER')
    THUMBNAIL_FOLDER = str(UPLOAD_FOLDER) + '/thumbnail/'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    MAX_FILE_SIZE = 500000000  # 5 MB

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SERVER_NAME = "localhost:5000" # em desenv, rodar serv do Flask, nao gunicorn
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:postgres@localhost/consensus'

class TestingConfig(Config):
    TESTING = True
    LOGIN_DISABLED = True
    SERVER_NAME = "localhost:5000"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '/tests/data-test.sqlite')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    app = Flask(__name__)
    db = SQLAlchemy(app)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') # var de amb criada auto pelo Heroku

config_map = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig
}