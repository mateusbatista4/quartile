#!/usr/bin/env python3
"""
Database Initialization Script

This script initializes the database and populates it with sample data.
It's useful for setting up a new deployment or resetting an existing database.
"""

import os
import sys
import time
from flask import Flask
from resources.database import db, init_app, reset_db
from resources.models.company import Company
from resources.models.store import Store
from resources.models.consult import Consult
from resources import constants

# Create a minimal Flask app for initializing the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = constants.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_app(app)

def create_sample_data():
    """Create sample data for testing"""
    print("Creating sample data...")
    
    # Create sample companies
    companies = [
        Company(
            name="PicPay Tech",
            document_number="00.000.000/0001-00",
            country="Brazil",
            address="Av. Brigadeiro Faria Lima, 3000, São Paulo, SP",
            contact_email="contact@picpay.com",
            contact_phone="+55 11 9999-8888"
        ),
        Company(
            name="American Tech Corp",
            document_number="123456789",
            country="United States",
            address="1 Infinite Loop, Cupertino, CA",
            contact_email="contact@americantech.com",
            contact_phone="+1 408 555 1234"
        ),
        Company(
            name="European Solutions",
            document_number="EU12345678",
            country="Germany",
            address="Unter den Linden 10, Berlin",
            contact_email="contact@europeansolutions.eu",
            contact_phone="+49 30 1234567"
        )
    ]
    
    for company in companies:
        db.session.add(company)
    
    # Need to commit to get company IDs
    db.session.commit()
    
    # Create sample stores
    stores = [
        # PicPay stores
        Store(
            name="PicPay HQ",
            address="Av. Brigadeiro Faria Lima, 3000",
            city="São Paulo",
            state="SP",
            postal_code="01452-000",
            phone="+55 11 9999-8888",
            company_id=companies[0].id
        ),
        Store(
            name="PicPay Rio",
            address="Av. Atlântica, 500",
            city="Rio de Janeiro",
            state="RJ",
            postal_code="22021-000",
            phone="+55 21 8888-7777",
            company_id=companies[0].id
        ),
        # American Tech stores
        Store(
            name="American Tech HQ",
            address="1 Infinite Loop",
            city="Cupertino",
            state="CA",
            postal_code="95014",
            phone="+1 408 555 1234",
            company_id=companies[1].id
        ),
        Store(
            name="American Tech NYC",
            address="5th Avenue",
            city="New York",
            state="NY",
            postal_code="10001",
            phone="+1 212 555 5678",
            company_id=companies[1].id
        ),
        # European Solutions stores
        Store(
            name="European Solutions Berlin",
            address="Unter den Linden 10",
            city="Berlin",
            state="",
            postal_code="10117",
            phone="+49 30 1234567",
            company_id=companies[2].id
        )
    ]
    
    for store in stores:
        db.session.add(store)
    
    # Create sample consults
    consults = [
        Consult(
            source_address="São Paulo, SP, Brazil",
            destination_address="Rio de Janeiro, RJ, Brazil",
            distance=429.0,  # km
            source="São Paulo, SP, Brazil",
            destination="Rio de Janeiro, RJ, Brazil"
        ),
        Consult(
            source_address="New York, NY, USA",
            destination_address="Los Angeles, CA, USA",
            distance=3944.0,  # km
            source="New York, NY, USA",
            destination="Los Angeles, CA, USA"
        ),
        Consult(
            source_address="Berlin, Germany",
            destination_address="Paris, France",
            distance=1054.0,  # km
            source="Berlin, Germany",
            destination="Paris, France"
        )
    ]
    
    for consult in consults:
        db.session.add(consult)
    
    db.session.commit()
    print("Sample data created successfully!")

if __name__ == "__main__":
    print("Initializing database...")
    
    # Check if the database already exists
    db_exists = os.path.exists("picpay.db")
    
    if db_exists:
        print("Database already exists.")
        response = input("Do you want to reset the database? (y/n): ")
        
        if response.lower() == 'y':
            print("Resetting database...")
            with app.app_context():
                reset_db()
                create_sample_data()
        else:
            print("Database reset cancelled.")
            sys.exit(0)
    else:
        print("Creating new database...")
        with app.app_context():
            db.create_all()
            create_sample_data()
    
    print("Database initialization complete!") 