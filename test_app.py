"""
Basic tests for the audio processing application.
Note: These tests require the dependencies from requirements.txt to be installed.
Run: pip install -r requirements.txt
Then: python -m pytest test_app.py
"""

import pytest
import os
import tempfile
from app import app, allowed_file

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test that the index route returns successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Audio Processing' in response.data

def test_allowed_file():
    """Test file extension validation."""
    assert allowed_file('test.mp3') == True
    assert allowed_file('test.aac') == True
    assert allowed_file('test.ac3') == True
    assert allowed_file('test.wav') == False
    assert allowed_file('test.txt') == False
    assert allowed_file('test') == False

def test_upload_no_file(client):
    """Test upload endpoint with no file."""
    response = client.post('/upload')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_upload_empty_filename(client):
    """Test upload endpoint with empty filename."""
    data = {'file': (None, '')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400

def test_upload_invalid_extension(client):
    """Test upload endpoint with invalid file extension."""
    data = {'file': (tempfile.NamedTemporaryFile(suffix='.txt'), 'test.txt')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    data = response.get_json()
    assert 'Invalid file type' in data['error']

def test_process_invalid_file_id(client):
    """Test process endpoint with invalid file ID."""
    response = client.post('/process',
                          json={'file_id': 'invalid-id', 'operation': 'compressor'})
    assert response.status_code == 404

def test_process_invalid_operation(client):
    """Test process endpoint with invalid operation."""
    # This would require a valid file_id, but we can't easily create one without audio processing libs
    # In a real test, you'd upload a file first, then test processing
    pass

def test_download_invalid_file_id(client):
    """Test download endpoint with invalid file ID."""
    response = client.get('/download/invalid-id')
    assert response.status_code == 404

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
