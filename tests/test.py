import requests
from src.config import Config


def test_hello_world():
    response = requests.get(f"{Config.BASE_URL}/")
    assert response.text == "<p>Hello, DIT!</p>"
    assert response.status_code == Config.ResponseStatusCode.OK


def test_add_and_delete_user():
    response = requests.post(f"{Config.BASE_URL}/Kolya")
    assert response.text == "<p>User was added!</p>"
    assert response.status_code == Config.ResponseStatusCode.OK

    response = requests.get(f"{Config.BASE_URL}/Kolya")
    assert response.json() == {"username": "Kolya"}
    assert response.status_code == Config.ResponseStatusCode.OK

    response = requests.delete(f"{Config.BASE_URL}/Kolya")
    assert response.text == "<p>User was deleted!</p>"
    assert response.status_code == Config.ResponseStatusCode.OK

    response = requests.get(f"{Config.BASE_URL}/1")
    assert response.text == "<p>User not found!</p>"
    assert response.status_code == Config.ResponseStatusCode.NOT_FOUND
