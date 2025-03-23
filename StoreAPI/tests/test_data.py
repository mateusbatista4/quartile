"""
Populate the database with test data
"""
from resources.models.company import Company
from resources.models.store import Store


def populate_test_data(db):
    db.session.query(Store).delete()
    db.session.query(Company).delete()
    db.session.commit()
    
    # Create test companies
    test_companies = [
        Company(
            name="Test Company 1",
            document_number="12345678901234",
            country="Brazil",
            address="Av. Test 123",
            contact_email="test1@example.com",
            contact_phone="+55 11 1234-5678"
        ),
        Company(
            name="Test Company 2",
            document_number="98765432109876",
            country="USA",
            address="Test St 456",
            contact_email="test2@example.com",
            contact_phone="+1 555-123-4567"
        ),
        Company(
            name="Test Company 3",
            document_number="11112222333344",
            country="Canada",
            address="Test Ave 789",
            contact_email="test3@example.com",
            contact_phone="+1 555-987-6543"
        )
    ]
    
    for company in test_companies:
        db.session.add(company)
    
    db.session.commit()
    
    # Create test stores
    test_stores = [
        Store(
            name="Store 1 Company 1",
            address="Rua Test 100",
            city="São Paulo",
            state="SP",
            postal_code="01234-567",
            phone="+55 11 9876-5432",
            company_id=1
        ),
        Store(
            name="Store 2 Company 1",
            address="Rua Test 200",
            city="Rio de Janeiro",
            state="RJ",
            postal_code="20000-000",
            phone="+55 21 8765-4321",
            company_id=1
        ),
        Store(
            name="Store 1 Company 2",
            address="Test Road 300",
            city="New York",
            state="NY",
            postal_code="10001",
            phone="+1 212-555-1234",
            company_id=2
        ),
        Store(
            name="Store 1 Company 3",
            address="Test Blvd 400",
            city="Toronto",
            state="ON",
            postal_code="M5V 2A8",
            phone="+1 416-555-7890",
            company_id=3
        )
    ]
    
    for store in test_stores:
        db.session.add(store)
    
    db.session.commit()
    
    return {
        'companies': test_companies,
        'stores': test_stores
    } 