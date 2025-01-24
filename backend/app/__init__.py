from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)

    # App Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Update for production
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Flask-Mail Configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'yourapp.bot@gmail.com'  # Replace with your email
    app.config['MAIL_PASSWORD'] = 'your_email_password'    # Use environment variable in production

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)

    # Register Blueprints
    from app.routes import main, auth, test
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(test)

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
