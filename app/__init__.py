"""create app"""
import os
from datetime import timedelta
from flask import Flask, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
dirname = os.path.dirname(__file__)

def internal_server_error(e):
    """Handle internal server error."""
    flash('Internal Server Error - 500', 'danger')
    return render_template('notification.html'), 500
def page_not_found(e):
    """Handle page not found error."""
    flash('This Page Not Found - 404', 'danger')
    return render_template('notification.html'), 404
def method_not_allowed(e):
    """Handle method not allowed error."""
    flash('Method Not Allowed - 405', 'danger')
    return render_template('notification.html'), 405

def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'ZvM2cym'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:2019@localhost/test?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_PATH'] = dirname + '/static/images/uploads'
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
    app.register_error_handler(405, method_not_allowed)
    return app
