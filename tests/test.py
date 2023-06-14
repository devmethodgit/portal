import requests
from src.config import Config


class JsonTestData:
    add_data = {
        "message": "User founded!",
        "data": {
            "login": "nnnekr",
            "last_name": "Nekrasov",
            "first_name": "Nikolay",
            "second_name": "Nikolaevich",
            "snils": "127-001",
        },
    }

    not_found = {"message": "User not founded!"}

    test_mess = {"message": "Hello, DIT!"}

    added = {"message": "User added!"}

    deleted = {"message": "User deleted!"}


def test_hello_world():
    response = requests.get(f"{Config.BASE_URL}/user/test")
    assert response.json() == JsonTestData.test_mess
    assert response.status_code == Config.ResponseStatusCode.OK


def test_add_and_delete_user():
    response = requests.post(
        f"{Config.BASE_URL}/user",
        json=JsonTestData.add_data["data"],
    )
    assert response.status_code == Config.ResponseStatusCode.OK
    json_response = response.json()
    login_id = json_response["login_id"]
    assert json_response["message"] == JsonTestData.added["message"]

    response = requests.get(f"{Config.BASE_URL}/user/{login_id}")
    assert response.json() == JsonTestData.add_data
    assert response.status_code == Config.ResponseStatusCode.OK

    response = requests.delete(f"{Config.BASE_URL}/user/{login_id}")
    assert response.json() == JsonTestData.deleted
    assert response.status_code == Config.ResponseStatusCode.OK

    response = requests.get(f"{Config.BASE_URL}/user/{login_id}")
    assert response.json() == JsonTestData.not_found
    assert response.status_code == Config.ResponseStatusCode.NOT_FOUND
