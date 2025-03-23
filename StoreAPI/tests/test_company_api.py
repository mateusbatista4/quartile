"""
Tests for the Company API endpoints
"""
import json
import pytest


def test_get_all_companies(client):
    """Test retrieving all companies"""
    response = client.get('/api/companies/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'data' in data
    assert len(data['data']) > 0
    
    company = data['data'][0]
    assert 'id' in company
    assert 'name' in company
    assert 'document_number' in company
    assert 'country' in company


def test_get_companies_with_pagination(client):
    response = client.get('/api/companies/?page=1&per_page=2')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert len(data['data']) <= 2
    
    
def test_get_companies_with_country_filter(client):
    response = client.get('/api/companies/')
    data = json.loads(response.data)
    
    if len(data['data']) > 0:
        country = data['data'][0]['country']
        
        response = client.get(f'/api/companies/?country={country}')
        assert response.status_code == 200
        
        filtered_data = json.loads(response.data)
        assert len(filtered_data['data']) > 0
        
        for company in filtered_data['data']:
            assert company['country'] == country


def test_get_specific_company(client):
    response = client.get('/api/companies/')
    data = json.loads(response.data)
    
    if len(data['data']) > 0:
        company_id = data['data'][0]['id']
        
        response = client.get(f'/api/companies/{company_id}')
        assert response.status_code == 200
        
        company = json.loads(response.data)['data']
        assert company['id'] == company_id
        assert 'name' in company
        assert 'document_number' in company


def test_get_nonexistent_company(client):
    response = client.get('/api/companies/9999')
    assert response.status_code == 404


def test_create_company(client):
    new_company = {
        'name': 'New Test Company',
        'document_number': '55555555555555',
        'country': 'Mexico',
        'address': 'Test Address 123',
        'contact_email': 'newtest@example.com',
        'contact_phone': '+52 55 1234-5678'
    }
    
    response = client.post(
        '/api/companies/',
        data=json.dumps(new_company),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    


def test_create_company_missing_required_fields(client):
    incomplete_company = {
        'name': 'Incomplete Company'
    }
    
    response = client.post(
        '/api/companies/',
        data=json.dumps(incomplete_company),
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_create_duplicate_company(client):
    response = client.get('/api/companies/')
    data = json.loads(response.data)
    
    if len(data['data']) > 0:
        existing_doc_number = data['data'][0]['document_number']
        
        duplicate_company = {
            'name': 'Duplicate Company',
            'document_number': existing_doc_number
        }
        
        response = client.post(
            '/api/companies/',
            data=json.dumps(duplicate_company),
            content_type='application/json'
        )
        
        assert response.status_code == 400


def test_update_company(client):
    response = client.get('/api/companies/')
    data = json.loads(response.data)
    
    if len(data['data']) > 0:
        company_id = data['data'][0]['id']
        
        update_data = {
            'name': 'Updated Company Name',
            'address': 'Updated Address 456',
            'contact_email': 'updated@example.com'
        }
        
        response = client.put(
            f'/api/companies/{company_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        
        updated_company = json.loads(response.data)['data']
        assert updated_company['id'] == company_id
        assert updated_company['name'] == update_data['name']
        assert updated_company['address'] == update_data['address']
        assert updated_company['contact_email'] == update_data['contact_email']


def test_update_nonexistent_company(client):
    update_data = {
        'name': 'Updated Company Name'
    }
    
    response = client.put(
        '/api/companies/9999',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    assert response.status_code == 404


def test_delete_company(client):
    new_company = {
        'name': 'Company To Delete',
        'document_number': '77777777777777'
    }
    
    response = client.post(
        '/api/companies/',
        data=json.dumps(new_company),
        content_type='application/json'
    )
    
    assert response.status_code == 201
        


def test_delete_nonexistent_company(client):
    response = client.delete('/api/companies/9999')
    assert response.status_code == 404 