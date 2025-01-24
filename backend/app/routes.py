from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from app import db, mail
from app.models import User, Dog

# Blueprints
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
test = Blueprint('test', __name__)

# Home Route
@main.route('/')
def home():
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

# Register Route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        if User.query.filter_by(email=email).first():
            flash('Email is already registered.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(name=name, email=email, password=password, phone=phone, is_active=False)
        db.session.add(new_user)
        db.session.commit()

        # Notify Admin
        admin_email = "admin@example.com"
        msg = Message(
            subject="New User Approval Needed",
            sender="yourapp.bot@gmail.com",
            recipients=[admin_email],
            body=f"A new user has signed up:\nName: {name}\nEmail: {email}\nPhone: {phone}"
        )
        mail.send(msg)

        flash('Your account is pending admin approval.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

# Login Route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:  # Replace with hashed password check
            if user.is_active:
                login_user(user)
                if user.is_admin:
                    return redirect(url_for('auth.admin_dashboard'))
                return redirect(url_for('main.home'))
            else:
                flash("Your account is not approved yet.", "warning")
                return redirect(url_for('auth.login'))
        else:
            flash("Invalid credentials.", "danger")

    return render_template('login.html')

# Logout Route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for('auth.login'))

# Admin Dashboard
@auth.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return "Access Denied", 403

    if request.method == 'POST':
        user_id = request.form['user_id']
        action = request.form['action']

        user = User.query.get(user_id)
        if action == 'approve':
            user.is_active = True
            db.session.commit()
            flash(f"User {user.name} approved.", 'success')
        elif action == 'reject':
            db.session.delete(user)
            db.session.commit()
            flash(f"User {user.name} rejected.", 'info')

    users = User.query.filter_by(is_active=False).all()
    return render_template('admin_dashboard.html', users=users)

# Test Email Route
@test.route('/send-test-email')
def send_test_email():
    msg = Message(
        subject="Test Email",
        sender="yourapp.bot@gmail.com",
        recipients=["recipient@example.com"],
        body="This is a test email from Flask!"
    )
    try:
        mail.send(msg)
        return "Test email sent!"
    except Exception as e:
        return f"Failed to send email: {e}"
