"""
Tests for general API endpoints
"""
import json
import pytest


def test_api_root(client):
    """Test the API root endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'api_version' in data
    assert 'resources' in data
    assert 'companies' in data['resources']
    assert 'stores' in data['resources']
    assert 'documentation' in data['resources']


def test_not_found(client):
    """Test the 404 error handler"""
    response = client.get('/nonexistent-endpoint')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data
    assert 'message' in data
    assert data['error'] == 'Not found' 