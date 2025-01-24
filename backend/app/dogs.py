from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import db, Dog

dogs_bp = Blueprint('dogs', __name__)

@dogs_bp.route('/dogs')
def list_dogs():
    """Display all dogs in the system."""
    dogs = Dog.query.all()
    return render_template('dogs.html', dogs=dogs)

@dogs_bp.route('/dogs/add', methods=['GET', 'POST'])
@login_required
def add_dog():
    """Allow a user to add a dog."""
    if request.method == 'POST':
        name = request.form['name']
        breed = request.form['breed']
        age = int(request.form['age'])
        temperament_with_kids = request.form['temperament_with_kids']
        temperament_with_dogs = request.form['temperament_with_dogs']
        temperament_with_pets = request.form['temperament_with_pets']
        weight = float(request.form['weight'])

        new_dog = Dog(
            name=name,
            breed=breed,
            age=age,
            temperament_with_kids=temperament_with_kids,
            temperament_with_dogs=temperament_with_dogs,
            temperament_with_pets=temperament_with_pets,
            weight=weight,
            owner_id=current_user.id
        )
        db.session.add(new_dog)
        db.session.commit()
        return redirect(url_for('dogs.list_dogs'))

    return render_template('add_dog.html')
