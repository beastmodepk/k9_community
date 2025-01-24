from flask import Blueprint, render_template
from app.models import User, Dog  # Import the models

main = Blueprint('main', __name__)

@main.route('/')
def home():
    # Dynamic data
    total_dogs = Dog.query.count()
    total_providers = User.query.filter_by(is_admin=False).count()
    total_reviews = 20 
    featured_dogs = Dog.query.limit(3).all()

    return render_template(
        'index.html',
        total_dogs=total_dogs,
        total_providers=total_providers,
        total_reviews=total_reviews,
        featured_dogs=featured_dogs
    )
