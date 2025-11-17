"""
Unit tests for the security demo application
Tests basic functionality and endpoints
"""
import pytest
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app import app

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Test home endpoint returns correct message"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == "Security Vulnerability Demo App"

def test_health_check(client):
    """Test health endpoint returns healthy status"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_process_data_with_valid_input(client):
    """Test process endpoint with valid JSON data"""
    test_data = {"test": "data", "number": 123}
    response = client.post('/process',
                          json=test_data,
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['processed'] == True
    assert 'urllib3_version' in data

def test_process_data_with_no_input(client):
    """Test process endpoint with no data returns error"""
    response = client.post('/process',
                           content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == "No data provided"

def test_process_data_with_empty_json(client):
    """Test process endpoint with empty JSON"""
    response = client.post('/process',
                           json={},
                           content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['processed'] == True

class TestSecurityContext:
    """Test security-related functionality"""
    
    def test_app_not_in_debug_mode(self, client):
        """Ensure app doesn't run in debug mode"""
        assert app.debug == False
    
    def test_requests_library_available(self):
        """Test that requests library is importable"""
        import requests
        assert requests.__version__ is not None
    
    def test_urllib3_library_available(self):
        """Test that urllib3 library is importable"""
        import urllib3
        assert urllib3.__version__ is not None
