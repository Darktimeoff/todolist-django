import pytest
import json

@pytest.mark.django_db
def test_success(client, cookies):
    client.cookies = cookies

    response = client.delete(
        '/core/profile'
    ) 

    assert response.status_code == 204
    assert response.data == None

@pytest.mark.django_db
def test_unauthorized(client):
    response = client.delete(
        '/core/profile',
    ) 

    assert response.status_code == 401