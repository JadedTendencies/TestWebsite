import os
from flask import Flask
from flask_login import LoginManager
from application.db import User, get_db  # Ensure these are correctly defined in db.py
from bson.objectid import ObjectId

# Initialize Flask-Login's LoginManager
login_manager = LoginManager()

# Specify the login view. This is the view users are redirected to if they need to log in.
login_manager.login_view = 'signin_bp.login'

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    user_doc = db.UserInfoTest.find_one({"_id": ObjectId(user_id)})
    if user_doc:
        return User(user_doc)  # This should return an instance of the User class
    return None

def create_app():
    app = Flask(__name__)

    # Flask app configuration
    app.config.from_object('config.Config')

    # Initialize LoginManager with the app instance
    login_manager.init_app(app)

    # Import and register blueprints
    from application.homepage.homepage import homepage_bp
    from application.user.user import signin_bp
    app.register_blueprint(homepage_bp, url_prefix='')
    app.register_blueprint(signin_bp, url_prefix='/user')

    return app
