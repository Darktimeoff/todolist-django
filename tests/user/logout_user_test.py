import pytest
from django.http import HttpResponse

@pytest.mark.django_db
def test_success(client, cookies):
    client.cookies = cookies

    response: HttpResponse = client.delete(
        '/core/profile'
    ) 

    assert response.status_code == 204

@pytest.mark.django_db
def test_unauthorized(client):
    response = client.delete(
        '/core/profile',
    ) 

    assert response.status_code == 403