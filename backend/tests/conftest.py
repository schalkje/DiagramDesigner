"""Pytest configuration and fixtures for DiagramDesigner tests."""
import pytest
from typing import Generator


@pytest.fixture
def api_client() -> Generator:
    """Provide a test client for API contract tests.

    Note: This will fail until Flask app is implemented.
    This is intentional for TDD - tests must fail first.
    """
    # This will fail until we implement the Flask app in Phase 3.6
    try:
        from src.api.app import create_app
        app = create_app()
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    except ImportError:
        pytest.fail("Flask app not yet implemented - this is expected for TDD")


@pytest.fixture
def auth_headers(api_client) -> dict:
    """Provide authentication headers with valid JWT token.

    Note: This will fail until auth is implemented.
    """
    # Login to get token (will fail until implemented)
    response = api_client.post('/api/v1/auth/login', json={
        'email': 'test@example.com',
        'password': 'Test123!'
    })

    if response.status_code == 200:
        token = response.json['token']
        return {'Authorization': f'Bearer {token}'}

    return {}


@pytest.fixture
def sample_superdomain_id() -> int:
    """Return a sample superdomain ID for testing."""
    return 1


@pytest.fixture
def sample_domain_id() -> int:
    """Return a sample domain ID for testing."""
    return 1


@pytest.fixture
def sample_entity_id() -> int:
    """Return a sample entity ID for testing."""
    return 1
