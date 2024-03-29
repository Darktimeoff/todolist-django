import pytest
from core.message import VALIDATION_REQUIRED_FIELD, VALIDATION_UNIQUE_USERNAME
from core.container import user_dao

@pytest.mark.django_db
def test_success(client):
    request_data = {
        'username': 'test',
        'password': 'asdsad213213123@',
        'password_repeat': 'asdsad213213123@',
    }

    expected_data = {
        "id": 3,
        "username": request_data['username'],
        "first_name": "",
        "last_name": "",
        "email": "",
    }

    response = client.post('/core/signup', request_data, format='json')
   
    expected_data['id'] = response.json().get('id')

    print('test_success', response.json(), expected_data)

    assert response.status_code == 201
    assert response.json() == expected_data

@pytest.mark.django_db
def test_username_already_exists(client):
    request_data = {
        'username': 'test',
        'password': 'asdsad213213123@',
        'password_repeat': 'asdsad213213123@',
    }

    expected_data = {
        "username": [VALIDATION_UNIQUE_USERNAME]
    }

    user_dao.create({
        'username': request_data['username'],
        'password': request_data['password']
    })

    response = client.post('/core/signup', request_data, format='json')

    assert response.status_code == 400
    assert response.json() == expected_data

@pytest.mark.django_db
def test_weak_password(client):
    request_data = {
        'username': 'test',
        'password': 'test',
        'password_repeat': 'test',
    }

    response = client.post('/core/signup', request_data, format='json')

    assert response.status_code == 400
    assert set(response.json().keys()) == {'password', 'password_repeat'}
    assert len(response.json().values()) > 0 

@pytest.mark.django_db
def test_without_password_repeat(client):
    request_data = {
        'username': 'test',
        'password': 'asdsad213213123@'
    }

    expected_data = {
        'password_repeat': [VALIDATION_REQUIRED_FIELD]
    }

    response = client.post('/core/signup', request_data, format='json')


    assert response.status_code == 400
    assert response.json() == expected_data

@pytest.mark.django_db
def test_without_username(client):
    request_data = {
        'password': 'asdsad213213123@',
        'password_repeat': 'asdsad213213123@'
    }

    expected_data = {
        'username': [VALIDATION_REQUIRED_FIELD]
    }

    response = client.post('/core/signup', request_data, format='json')


    assert response.status_code == 400
    assert response.json() == expected_data

@pytest.mark.django_db
def test_without_password(client):
    request_data = {
        'username': 'test',
        'password_repeat': 'asdsad213213123@',
    }

    expected_data = {
        'password': [VALIDATION_REQUIRED_FIELD]
    }

    response = client.post('/core/signup', request_data, format='json')


    assert response.status_code == 400
    assert response.json() == expected_data

@pytest.mark.django_db
def test_empty_request(client):
    request_data = {
    }

    expected_data = {
        "password": [VALIDATION_REQUIRED_FIELD],
        "username": [VALIDATION_REQUIRED_FIELD],
        'password_repeat': [VALIDATION_REQUIRED_FIELD]
    }

    response = client.post('/core/signup', request_data, format='json')


    assert response.status_code == 400
    assert response.json() == expected_data