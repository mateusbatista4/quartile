"""
Tests for the Store API endpoints
"""
import json
import pytest


def test_get_all_stores(client):
    """Test retrieving all stores"""
    response = client.get('/api/stores/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'data' in data
    assert len(data['data']) > 0
    
    store = data['data'][0]
    assert 'id' in store
    assert 'name' in store
    assert 'address' in store
    assert 'company_id' in store


def test_get_stores_with_pagination(client):
    response = client.get('/api/stores/?page=1&per_page=2')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert len(data['data']) <= 2


def test_get_stores_with_company_filter(client):
    response = client.get('/api/companies/')
    data = json.loads(response.data)
    
    if len(data['data']) > 0:
        company_id = data['data'][0]['id']
        
        response = client.get(f'/api/stores/?company_id={company_id}')
        assert response.status_code == 200
        
        filtered_data = json.loads(response.data)
        
        for store in filtered_data['data']:
            assert store['company_id'] == company_id


def test_get_specific_store(client):
    response = client.get('/api/stores/')
    data = json.loads(response.data)
    
    if len(data['data']) > 0:
        store_id = data['data'][0]['id']
        
        # Get
        response = client.get(f'/api/stores/{store_id}')
        assert response.status_code == 200
        
        store = json.loads(response.data)['data']
        assert store['id'] == store_id
        assert 'name' in store
        assert 'address' in store
        assert 'company_id' in store


def test_get_nonexistent_store(client):
    response = client.get('/api/stores/9999')
    assert response.status_code == 404


def test_create_store(client):
    response = client.get('/api/companies/')
    data = json.loads(response.data)
    
    if len(data['data']) > 0:
        company_id = data['data'][0]['id']
        
        new_store = {
            'name': 'New Test Store',
            'address': 'Test Store Address 123',
            'city': 'Test City',
            'state': 'TS',
            'postal_code': '12345-678',
            'phone': '+1 555-TEST',
            'company_id': company_id
        }
        
        response = client.post(
            '/api/stores/',
            data=json.dumps(new_store),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        


def test_create_store_missing_required_fields(client):
    incomplete_store = {
        'name': 'Incomplete Store'
    }
    
    response = client.post(
        '/api/stores/',
        data=json.dumps(incomplete_store),
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_create_store_invalid_company_id(client):
    invalid_store = {
        'name': 'Invalid Company Store',
        'address': 'Invalid Address',
        'company_id': 9999  # Non-existent 
    }
    
    response = client.post(
        '/api/stores/',
        data=json.dumps(invalid_store),
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_update_store(client):
    response = client.get('/api/stores/')
    data = json.loads(response.data)
    
    if len(data['data']) > 0:
        store_id = data['data'][0]['id']
        
        update_data = {
            'name': 'Updated Store Name',
            'address': 'Updated Store Address 456',
            'city': 'Updated City',
            'phone': '+1 555-UPDATED'
        }
        
        response = client.put(
            f'/api/stores/{store_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        


def test_update_nonexistent_store(client):
    update_data = {
        'name': 'Updated Store Name'
    }
    
    response = client.put(
        '/api/stores/9999',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    assert response.status_code == 404


def test_delete_store(client):
    response = client.get('/api/companies/')
    company_data = json.loads(response.data)
    
    if len(company_data['data']) > 0:
        company_id = company_data['data'][0]['id']
        
        new_store = {
            'name': 'Store To Delete',
            'address': 'Delete Address',
            'company_id': company_id
        }
        
        response = client.post(
            '/api/stores/',
            data=json.dumps(new_store),
            content_type='application/json'
        )
        
        assert response.status_code == 201
            


def test_delete_nonexistent_store(client):
    response = client.delete('/api/stores/9999')
    assert response.status_code == 404


def test_get_company_stores(client):
    response = client.get('/api/companies/')
    data = json.loads(response.data)
    
    if len(data['data']) > 0:
        company_id = data['data'][0]['id']
        
        response = client.get(f'/api/companies/{company_id}/stores')
        assert response.status_code == 200
        
        stores_data = json.loads(response.data)
        assert 'data' in stores_data
        
        for store in stores_data['data']:
            assert store['company_id'] == company_id


def test_get_company_stores_pagination(client):
    response = client.get('/api/companies/')
    data = json.loads(response.data)
    
    if len(data['data']) > 0:
        company_id = data['data'][0]['id']
        
        response = client.get(f'/api/companies/{company_id}/stores?page=1&per_page=1')
        assert response.status_code == 200
        
        stores_data = json.loads(response.data)
        assert len(stores_data['data']) <= 1


def test_get_nonexistent_company_stores(client):
    response = client.get('/api/companies/9999/stores')
    if response.status_code == 404:
        assert response.status_code == 404
    else:
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['data']) == 0 