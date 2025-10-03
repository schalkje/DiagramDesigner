"""Contract test for POST /entities/{entityId}/attributes endpoint.

Validates AttributeCreate schema with dataType enum.
Expected to FAIL until implementation (TDD).
"""
import pytest


def test_create_attribute_success(api_client, auth_headers, sample_entity_id):
    """Test POST /entities/{entityId}/attributes creates attribute and returns 201."""
    response = api_client.post(
        f'/api/v1/entities/{sample_entity_id}/attributes',
        headers=auth_headers,
        json={
            'name': 'email',
            'dataType': 'String',
            'isNullable': False,
            'description': 'User email address'
        }
    )

    # Should return 201 Created
    assert response.status_code == 201
    assert response.content_type == 'application/json'

    # Validate response matches Attribute schema
    data = response.json
    assert 'id' in data
    assert 'entityId' in data
    assert 'name' in data
    assert 'dataType' in data
    assert 'isNullable' in data
    assert 'createdAt' in data
    assert 'updatedAt' in data

    # Validate values
    assert data['entityId'] == sample_entity_id
    assert data['name'] == 'email'
    assert data['dataType'] == 'String'
    assert data['isNullable'] is False


def test_create_attribute_missing_name_returns_400(api_client, auth_headers, sample_entity_id):
    """Test POST /entities/{entityId}/attributes without required name returns 400."""
    response = api_client.post(
        f'/api/v1/entities/{sample_entity_id}/attributes',
        headers=auth_headers,
        json={
            'dataType': 'String',
            'isNullable': True
        }
    )

    # Should return 400 Bad Request
    assert response.status_code == 400


def test_create_attribute_missing_data_type_returns_400(api_client, auth_headers, sample_entity_id):
    """Test POST /entities/{entityId}/attributes without required dataType returns 400."""
    response = api_client.post(
        f'/api/v1/entities/{sample_entity_id}/attributes',
        headers=auth_headers,
        json={
            'name': 'email',
            'isNullable': True
        }
    )

    # Should return 400 Bad Request
    assert response.status_code == 400


def test_create_attribute_invalid_data_type_returns_400(api_client, auth_headers, sample_entity_id):
    """Test POST /entities/{entityId}/attributes with invalid dataType enum returns 400."""
    response = api_client.post(
        f'/api/v1/entities/{sample_entity_id}/attributes',
        headers=auth_headers,
        json={
            'name': 'email',
            'dataType': 'InvalidType',
            'isNullable': True
        }
    )

    # Should return 400 Bad Request (dataType not in enum)
    assert response.status_code == 400


def test_create_attribute_all_valid_data_types(api_client, auth_headers, sample_entity_id):
    """Test POST /entities/{entityId}/attributes with all valid dataType values."""
    valid_types = [
        'String', 'Text', 'Integer', 'BigInteger', 'Float', 'Decimal',
        'Boolean', 'Date', 'DateTime', 'Time', 'UUID', 'JSON'
    ]

    for data_type in valid_types:
        response = api_client.post(
            f'/api/v1/entities/{sample_entity_id}/attributes',
            headers=auth_headers,
            json={
                'name': f'test_{data_type.lower()}',
                'dataType': data_type,
                'isNullable': True
            }
        )

        # Should return 201 Created for all valid types
        assert response.status_code == 201
        assert response.json['dataType'] == data_type


def test_create_attribute_with_constraints_jsonb(api_client, auth_headers, sample_entity_id):
    """Test POST /entities/{entityId}/attributes with constraints JSONB field."""
    response = api_client.post(
        f'/api/v1/entities/{sample_entity_id}/attributes',
        headers=auth_headers,
        json={
            'name': 'age',
            'dataType': 'Integer',
            'isNullable': False,
            'constraints': {
                'min': 0,
                'max': 120
            }
        }
    )

    # Should return 201 Created
    assert response.status_code == 201
    data = response.json
    assert 'constraints' in data
    assert isinstance(data['constraints'], dict)


def test_create_attribute_duplicate_name_returns_400(api_client, auth_headers, sample_entity_id):
    """Test POST /entities/{entityId}/attributes with duplicate name returns 400."""
    # Create first attribute
    api_client.post(
        f'/api/v1/entities/{sample_entity_id}/attributes',
        headers=auth_headers,
        json={
            'name': 'unique_attr',
            'dataType': 'String',
            'isNullable': True
        }
    )

    # Try to create duplicate
    response = api_client.post(
        f'/api/v1/entities/{sample_entity_id}/attributes',
        headers=auth_headers,
        json={
            'name': 'unique_attr',
            'dataType': 'Integer',
            'isNullable': False
        }
    )

    # Should return 400 Bad Request (unique constraint: entity_id, name)
    assert response.status_code == 400


def test_create_attribute_invalid_entity_returns_404(api_client, auth_headers):
    """Test POST /entities/{entityId}/attributes with invalid entity returns 404."""
    response = api_client.post(
        '/api/v1/entities/99999/attributes',
        headers=auth_headers,
        json={
            'name': 'email',
            'dataType': 'String',
            'isNullable': True
        }
    )

    # Should return 404 Not Found
    assert response.status_code == 404


def test_create_attribute_requires_auth(api_client, sample_entity_id):
    """Test POST /entities/{entityId}/attributes without auth returns 401."""
    response = api_client.post(
        f'/api/v1/entities/{sample_entity_id}/attributes',
        json={
            'name': 'email',
            'dataType': 'String'
        }
    )

    # Should return 401 Unauthorized
    assert response.status_code == 401
