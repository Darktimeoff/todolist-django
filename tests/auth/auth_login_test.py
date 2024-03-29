import pytest
import json
from django.http import HttpResponse
from core.message import VALIDATION_REQUIRED_FIELD

@pytest.mark.django_db
def test_success(client, user, login_cread):
    expected_data = {
        'username': user.username,
        'password': user.password
    }

    response: HttpResponse = client.post('/core/login', data=json.dumps(login_cread), content_type='application/json')

    assert response.status_code == 201
    assert response.json() == expected_data

@pytest.mark.django_db
def test_invalid_username(client, ):
    # Test case: User with this username doesn't exist
    request_data = {
        'username': 'invalid_username',
        'password': 'test_password'
    }

    expected_data = {
        "detail": "Incorrect authentication credentials."
    }

    response = client.post('/core/login', data=json.dumps(request_data), content_type='application/json')

    assert response.status_code == 403
    assert response.json() == expected_data

@pytest.mark.django_db
def test_missing_username(client):
    # Test case: Username not passed
    request_data = {
        'password': 'test_password'
    }

    expected_data = {
        'username': [VALIDATION_REQUIRED_FIELD]
    }

    response = client.post('/core/login', data=json.dumps(request_data), content_type='application/json')
    assert response.status_code == 400
    assert response.json() == expected_data

@pytest.mark.django_db
def test_missing_password(client):
    # Test case: Username not passed
    request_data = {
        "username": "test"
    }

    expected_data = {
        'password': [VALIDATION_REQUIRED_FIELD]
    }

    response = client.post('/core/login', data=json.dumps(request_data), content_type='application/json')
    assert response.status_code == 400
    assert response.json() == expected_data

@pytest.mark.django_db
def test_incorrect_password(client, user):
    # Test case: Password not correct
    request_data = {
        'username': user.username,
        'password': 'wrong_password'
    }

    expected_data = {
        "detail": "Incorrect authentication credentials."
    }

    response = client.post('/core/login', data=json.dumps(request_data), content_type='application/json')
    assert response.status_code == 403
    assert response.json() == expected_data
   
@pytest.mark.django_db
def test_empty_data(client, user):
    # Test case: Password not correct
    request_data = {
    }

    expected_data = {
        'username': [VALIDATION_REQUIRED_FIELD],
        'password': [VALIDATION_REQUIRED_FIELD]
    }

    response = client.post('/core/login', data=json.dumps(request_data), content_type='application/json')
    assert response.status_code == 400
    assert response.json() == expected_data
   