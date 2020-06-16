from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(cfg_name):
    app = Flask(__name__)
    # The config settings from the object of class Config are imported to the app
    app.config.from_object(config[cfg_name])
    config[cfg_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_Blueprint
    app.register_blueprint(main_Blueprint)

    return app
