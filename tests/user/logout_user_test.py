import pytest
import json
from django.http import HttpResponse
from todolist.settings import SIMPLE_JWT

@pytest.mark.django_db
def test_success(client, cookies):
    client.cookies = cookies

    response: HttpResponse = client.delete(
        '/core/profile'
    ) 

    assert response.status_code == 204
    assert SIMPLE_JWT['AUTH_COOKIE'] in response.cookies
    assert response.cookies.get(SIMPLE_JWT['AUTH_COOKIE']).value == ''

@pytest.mark.django_db
def test_unauthorized(client):
    response = client.delete(
        '/core/profile',
    ) 

    assert response.status_code == 401