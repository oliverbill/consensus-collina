#!/usr/bin/python
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    ADMIN_USER = os.environ.get('ADMIN_USER')
    ALLOWED_EXTENSIONS = set(['pdf', 'jpeg', 'bmp', 'jpg', 'png', 'gif', 'txt', 'doc', 'docx', 'xls', 'xlsx'])

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SERVER_NAME = "localhost:5000"
# Sugerir Item Pauta - upload de anexos
    UPLOAD_FOLDER = os.environ.get('CONSENSUS_UPLOAD_FOLDER')
    THUMBNAIL_FOLDER = str(UPLOAD_FOLDER) + '/thumbnail/'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    MAX_FILE_SIZE = 500000000  # 5 MB
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/consensus'


class TestingConfig(Config):
    TESTING = True
    LOGIN_DISABLED = True
    SERVER_NAME = "localhost:5000"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False


# DEFINIR VARIAVEL DE AMBIENTE $HOST
class ProductionConfig(Config):
    SERVER_NAME = os.environ.get('HOST')
    app = Flask(__name__)
    db = SQLAlchemy(app)
    if SERVER_NAME:
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@' + SERVER_NAME + '/consensus'
    else:
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/consensus'

config_map = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig
}