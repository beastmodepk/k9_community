from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register Blueprints
    from app.routes import main
    from app.auth import auth
    from app.dogs import dogs_bp  # Import the new Blueprint

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(dogs_bp)  # Register the new dogs Blueprint

    return app


@login_manager.user_loader
def load_user(user_id):
    # Lazy import to avoid circular dependency
    from app.models import User
    return User.query.get(int(user_id))
