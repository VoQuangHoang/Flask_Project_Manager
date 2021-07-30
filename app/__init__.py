from flask import Flask, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect
from flask import send_from_directory
import os


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def internal_server_error(e):
    flash('Internal server error - 500', 'danger')
    return render_template('notification.html'), 500
def page_not_found(e):
    flash('This page not found - 404', 'danger')
    return render_template('notification.html'), 404

def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'ZvM2cym'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:2019@localhost/test?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # time to live for session
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=60)

    with app.app_context():
        db.init_app(app)
        login_manager.init_app(app)
        csrf.init_app(app)
 
        # blueprint for auth routes
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)
        
        # blueprint for main routes
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    
    return app