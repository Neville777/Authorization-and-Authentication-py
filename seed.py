# seed.py

import os
from faker import Faker
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Profile, Collection
from main import app


# Initialize Faker
fake = Faker()

# Function to populate the database with fake data
def seed_database():
    with app.app_context():
        # Drop all existing tables (optional)
        db.drop_all()
        db.create_all()
        
        # Create fake users with profiles and collections
        for _ in range(10):  # Creating 10 users for example
            user = User(email=fake.email(), password=fake.password())
            profile = Profile(first_name=fake.first_name(), last_name=fake.last_name(),
                              photo_url=fake.image_url(), location=fake.city())
            collection = Collection(name=fake.word(), photo_url=fake.image_url())
            
            # Associate profile and collection with user
            user.profile = profile
            user.collections.append(collection)
            
            # Add to session
            db.session.add(user)
            db.session.commit()

if __name__ == "__main__":
    seed_database()
