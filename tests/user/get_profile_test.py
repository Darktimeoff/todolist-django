import pytest
from django.test import RequestFactory

@pytest.mark.django_db
def test_success(client, cookies, user):
    client.cookies = cookies

    expected_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

    response = client.get('/core/profile')

    assert response.status_code == 200
    assert response.json() == expected_data

@pytest.mark.django_db
def test_unauthorized(client):
    response = client.get('/core/profile')

    assert response.status_code == 401