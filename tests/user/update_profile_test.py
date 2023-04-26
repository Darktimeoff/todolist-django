import pytest
import json

@pytest.mark.django_db
def test_success(client, cookies, user):
    request_data = {
        "username": user.username,
        "email": 'test@gmail.com',
        "first_name": "Yevhenii",
        "last_name": "Korolikhin"
    }

    expected_data = {
        "id": user.id,
        **request_data
    }

    client.cookies = cookies

    response = client.put('/core/profile', 
        data=json.dumps(request_data), 
        content_type='application/json'
    )

    print('response: ', response.json())

    assert response.status_code == 200
    assert response.json() == expected_data

@pytest.mark.django_db
def test_unauthorized(client):
    response = client.put('/core/profile')
    assert response.status_code == 401

@pytest.mark.django_db
def test_blank_email(client, cookies, user):
    request_data = {
        "username": user.username,
        "email": 'test@gmail.com',
        "first_name": "Yevhenii",
        "last_name": "Korolikhin"
    }

    expected_data = {
        "email": ["This field may not be blank."]
    }

    client.cookies = cookies

    response = client.put('/core/profile', 
        data=json.dumps(request_data), 
        content_type='application/json'
    )

    print('response: ', response.json())

    assert response.status_code == 400
    assert response.json() == expected_data

@pytest.mark.django_db
def test_without_username(client, cookies, user):
    request_data = {
        "email": 'test@gmail.com',
        "first_name": "Yevhenii",
        "last_name": "Korolikhin"
    }

    expected_data = {
        "id": user.id,
        "username": user.username,
        **request_data,
    }

    client.cookies = cookies

    response = client.put('/core/profile', 
        data=json.dumps(request_data), 
        content_type='application/json'
    )


    assert response.status_code == 200
    assert response.json() == expected_data

@pytest.mark.django_db
def test_without_firstname(client, cookies, user):
    request_data = {
        "email": 'test@gmail.com',
        "last_name": "Korolikhin"
    }

    expected_data = {
        "id": user.id,
        "username": user.username,
        **request_data,
        "first_name": user.first_name
    }

    client.cookies = cookies

    response = client.put('/core/profile', 
        data=json.dumps(request_data), 
        content_type='application/json'
    )


    assert response.status_code == 200
    assert response.json() == expected_data

@pytest.mark.django_db
def test_without_lastname(client, cookies, user):
    request_data = {
        "email": 'test@gmail.com'
    }

    expected_data = {
        "id": user.id,
        "username": user.username,
        **request_data,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

    client.cookies = cookies

    response = client.put('/core/profile', 
        data=json.dumps(request_data), 
        content_type='application/json'
    )


    assert response.status_code == 200
    assert response.json() == expected_data