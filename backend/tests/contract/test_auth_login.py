"""Contract test for POST /auth/login endpoint.

This test validates that the login endpoint conforms to the OpenAPI specification.
Expected to FAIL until implementation is complete (TDD approach).
"""
import pytest


def test_login_success_returns_token_and_user(api_client):
    """Test successful login returns JWT token and user object."""
    response = api_client.post('/api/v1/auth/login', json={
        'email': 'test@example.com',
        'password': 'Test123!'
    })

    # Should return 200 OK
    assert response.status_code == 200

    # Should return JSON
    assert response.content_type == 'application/json'

    # Validate response schema matches OpenAPI spec
    data = response.json
    assert 'token' in data, "Response must include 'token' field"
    assert 'user' in data, "Response must include 'user' field"

    # Validate token is a non-empty string
    assert isinstance(data['token'], str)
    assert len(data['token']) > 0

    # Validate user object structure
    user = data['user']
    assert 'id' in user
    assert 'email' in user
    assert 'username' in user
    assert user['email'] == 'test@example.com'


def test_login_invalid_credentials_returns_401(api_client):
    """Test login with invalid credentials returns 401 Unauthorized."""
    response = api_client.post('/api/v1/auth/login', json={
        'email': 'test@example.com',
        'password': 'WrongPassword'
    })

    # Should return 401 Unauthorized
    assert response.status_code == 401

    # Should return JSON error
    assert response.content_type == 'application/json'
    data = response.json
    assert 'error' in data or 'message' in data


def test_login_missing_email_returns_400(api_client):
    """Test login without email returns 400 Bad Request."""
    response = api_client.post('/api/v1/auth/login', json={
        'password': 'Test123!'
    })

    # Should return 400 Bad Request
    assert response.status_code == 400


def test_login_missing_password_returns_400(api_client):
    """Test login without password returns 400 Bad Request."""
    response = api_client.post('/api/v1/auth/login', json={
        'email': 'test@example.com'
    })

    # Should return 400 Bad Request
    assert response.status_code == 400


def test_login_invalid_json_returns_400(api_client):
    """Test login with invalid JSON returns 400 Bad Request."""
    response = api_client.post(
        '/api/v1/auth/login',
        data='invalid json',
        content_type='application/json'
    )

    # Should return 400 Bad Request
    assert response.status_code == 400
