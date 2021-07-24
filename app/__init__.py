from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'ZvM2cym'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:2019@localhost/test?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=60)
    db.init_app(app)
    login_manager.init_app(app)

    # blueprint for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    # blueprint for main routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app