import pytest
import json
from core.user.message import VALIDAITON_NEW_PASSWORD, VALIDATION_OLD_PASSWORD

@pytest.mark.django_db
def test_success(client, cookies, login_cread):
    requested_data = {
        "old_password": login_cread.get('password'),
        "new_password": "test@ssss@3434",
    }

    client.cookies = cookies

    response = client.put(
        '/core/update_password', 
        data=json.dumps(requested_data), 
        content_type='application/json'
    )

    print('change_password response', response.json())

    assert response.status_code == 200
    assert response.json() == requested_data

@pytest.mark.django_db
def test_unauthorized(client):
    response = client.put(
        '/core/update_password', 
        data=json.dumps({}), 
        content_type='application/json'
    )


    assert response.status_code == 401

@pytest.mark.django_db
def test_same_new_and_old_password(client, cookies, login_cread):
    requested_data = {
        "old_password": 'test@ssss@3434',
        "new_password": 'test@ssss@3434',
    }

    expected_data = {
        "new_password": [VALIDAITON_NEW_PASSWORD]
    }

    client.cookies = cookies

    response = client.put(
        '/core/update_password', 
        data=json.dumps(requested_data), 
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.json() == expected_data

@pytest.mark.django_db
def test_old_password_incorrect(client, cookies):
    requested_data = {
        "old_password": 'test@ssss@343',
        "new_password": 'test@ssss@3434',
    }

    expected_data = {
        "old_password": [VALIDATION_OLD_PASSWORD]
    }

    client.cookies = cookies

    response = client.put(
        '/core/update_password', 
        data=json.dumps(requested_data), 
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.json() == expected_data

@pytest.mark.django_db
def test_new_password_weak(client, cookies, login_cread):
    requested_data = {
        "old_password": login_cread.get('password'),
        "new_password": 'asdad',
    }

    client.cookies = cookies

    response = client.put(
        '/core/update_password', 
        data=json.dumps(requested_data), 
        content_type='application/json'
    )

    assert response.status_code == 400
    assert set(response.json().keys()) == {'new_password'}
    assert len(response.json().values()) > 0