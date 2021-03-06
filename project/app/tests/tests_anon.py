# Django
# Third-Party
import pytest
from django.urls import reverse


def test_deploy():
    assert True


@pytest.mark.django_db
def test_index(anon_client):
    path = reverse('index')
    response = anon_client.get(path)
    assert response.status_code == 200

def test_about(anon_client):
    path = reverse('about')
    response = anon_client.get(path)
    assert response.status_code == 200

def test_privacy(anon_client):
    path = reverse('privacy')
    response = anon_client.get(path)
    assert response.status_code == 200

def test_terms(anon_client):
    path = reverse('terms')
    response = anon_client.get(path)
    assert response.status_code == 200

def test_support(anon_client):
    path = reverse('support')
    response = anon_client.get(path)
    assert response.status_code == 200

def test_dashboard(anon_client):
    path = reverse('dashboard')
    response = anon_client.get(path)
    assert response.status_code == 302
