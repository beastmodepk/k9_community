import os
from app import db, create_app
from app.models import User

# Initialize Flask application
app = create_app()
app.app_context().push()

# Delete the existing database file
if os.path.exists("app.db"):
    os.remove("app.db")
    print("Old database removed.")

# Recreate the database
db.create_all()
print("New database created.")

# Seed the database with an admin user
admin = User(
    name="Admin User",
    email="admin@eg.com",
    password="admin",  # Replace with hashed password in production
    phone="1234567890",
    is_admin=True,
    is_active=True  # Mark admin as active
)
db.session.add(admin)
db.session.commit()
print("Admin created. email-admin@eg.com and pass-admin")
