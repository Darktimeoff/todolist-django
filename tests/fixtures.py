import pytest
import json
from django.http import HttpResponse

@pytest.fixture
def login_cread(user):
    return {
        'username': user.username,
        'password': user.username
    }

@pytest.mark.django_db
@pytest.fixture
def cookies(client, login_cread):
    response: HttpResponse = client.post(
        '/core/login', 
        data=json.dumps(login_cread),
        content_type='application/json'
    )

    print('cookies', response.json())

    return response.cookies
    