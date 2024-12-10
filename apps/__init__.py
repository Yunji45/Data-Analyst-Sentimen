# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# from flask import Flask
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy
# from importlib import import_module


# db = SQLAlchemy()
# login_manager = LoginManager()


# def register_extensions(app):
#     db.init_app(app)
#     login_manager.init_app(app)


# def register_blueprints(app):
#     for module_name in ('authentication', 'home'):
#         module = import_module('apps.{}.routes'.format(module_name))
#         app.register_blueprint(module.blueprint)


# def configure_database(app):

#     @app.before_first_request
#     def initialize_database():
#         try:
#             db.create_all()
#         except Exception as e:

#             print('> Error: DBMS Exception: ' + str(e) )

#             # fallback to SQLite
#             basedir = os.path.abspath(os.path.dirname(__file__))
#             app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

#             print('> Fallback to SQLite ')
#             db.create_all()

#     @app.teardown_request
#     def shutdown_session(exception=None):
#         db.session.remove()

# from apps.authentication.oauth import github_blueprint

# def create_app(config):
#     app = Flask(__name__)
#     app.config.from_object(config)
#     register_extensions(app)

#     app.register_blueprint(github_blueprint, url_prefix="/login")
    
#     register_blueprints(app)
#     configure_database(app)
#     return app


import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module

db = SQLAlchemy()
login_manager = LoginManager()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module(f'apps.{module_name}.routes')
        app.register_blueprint(module.blueprint)

def configure_database(app):
    # Ambil pengaturan database dari konfigurasi atau environment variables
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri(app)

    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:
            print('> Error: DBMS Exception: ' + str(e))
            # Fallback to SQLite jika ada error dengan MySQL
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
            print('> Fallback to SQLite')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def get_database_uri(app):
    # Mendapatkan koneksi database MySQL dari environment variable
    db_host = os.getenv('DB_HOST', 'localhost')
    db_name = os.getenv('DB_NAME', 'flask')
    db_user = os.getenv('DB_USERNAME', 'root')
    db_pass = os.getenv('DB_PASS', '')
    db_port = os.getenv('DB_PORT', '3306')

    # Konstruksi URI untuk MySQL dengan PyMySQL
    return f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

from apps.authentication.oauth import github_blueprint

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)

    app.register_blueprint(github_blueprint, url_prefix="/login")
    
    register_blueprints(app)
    configure_database(app)
    return app
