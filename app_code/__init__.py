from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
def create_app(cfg_name):
    app = Flask(__name__)
    # The config settings from the object of class Config are imported to the app
    app.config.from_object(config[cfg_name])
    config[cfg_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    login_manager.init_app(app)

    from .auth import auth as auth_Blueprint
    app.register_blueprint(auth_Blueprint, url_prefix='/auth')

    from .main import main as main_Blueprint
    app.register_blueprint(main_Blueprint)

    return app
