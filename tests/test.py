import requests
from src.config import Config


class JsonTestData:
    add_data = {
        "user": {
            "login": "nnnekr",
            "last_name": "Nekrasov",
            "first_name": "Nikolay",
            "second_name": "Nikolaevich",
            "snils": "127-001",
        },
        "specs": [
            {
                "spec_code": 10,
                "spec_name": "Терапевт",
            },
            {
                "spec_code": 11,
                "spec_name": "Онколог",
            },
        ],
    }

    test_mess = {"message": "Hello, DIT!"}

    user_founded = {"message": "User founded!"}
    user_not_founded = {"message": "User not founded!"}
    user_added = {"message": "User added!"}
    user_deleted = {"message": "User deleted!"}

    spec_added = {"message": "Spec added!"}
    spec_deleted = {"message": "Spec deleted!"}
    spec_founded = {"message": "Spec founded!"}
    spec_not_founded = {"message": "Spec not founded!"}

    user_spec_added = {"message": "User to spec added!"}
    user_spec_not_founded = {"message": "User spec not founded!"}
    user_spec_founded = {"message": "User spec founded!"}


def test_hello_world():
    response = requests.get(f"{Config.BASE_URL}/user/test")
    assert response.json() == JsonTestData.test_mess
    assert response.status_code == Config.ResponseStatusCode.OK


def test_add_and_delete_user():
    response = requests.post(
        f"{Config.BASE_URL}/user",
        json=JsonTestData.add_data["user"],
    )
    assert response.status_code == Config.ResponseStatusCode.OK
    json_response = response.json()
    user_id = json_response["user_id"]
    assert json_response["message"] == JsonTestData.user_added["message"]

    response = requests.get(f"{Config.BASE_URL}/user/{user_id}")
    assert response.status_code == Config.ResponseStatusCode.OK
    json_response = response.json()
    assert json_response["message"] == JsonTestData.user_founded["message"]
    assert json_response["user"] == JsonTestData.add_data["user"]

    response = requests.delete(f"{Config.BASE_URL}/user/{user_id}")
    assert response.status_code == Config.ResponseStatusCode.OK
    assert response.json() == JsonTestData.user_deleted

    response = requests.get(f"{Config.BASE_URL}/user/{user_id}")
    assert response.status_code == Config.ResponseStatusCode.NOT_FOUND
    assert response.json() == JsonTestData.user_not_founded


def test_cascade_delete():
    response = requests.post(
        f"{Config.BASE_URL}/user",
        json=JsonTestData.add_data["user"],
    )
    assert response.status_code == Config.ResponseStatusCode.OK
    json_response = response.json()
    user_id = json_response["user_id"]
    assert json_response["message"] == JsonTestData.user_added["message"]

    response = requests.post(
        f"{Config.BASE_URL}/fill/spec",
        json=JsonTestData.add_data["specs"][0],
    )
    assert response.status_code == Config.ResponseStatusCode.OK
    json_response = response.json()
    spec_id = json_response["spec_id"]
    assert json_response["message"] == JsonTestData.spec_added["message"]

    response = requests.get(
        f"{Config.BASE_URL}/fill/spec/{spec_id}",
    )
    assert response.status_code == Config.ResponseStatusCode.OK
    json_response = response.json()
    assert json_response["message"] == JsonTestData.spec_founded["message"]
    assert json_response["spec"] == JsonTestData.add_data["specs"][0]

    response = requests.post(
        f"{Config.BASE_URL}/user/spec/{user_id}/{spec_id}",
    )
    assert response.status_code == Config.ResponseStatusCode.OK
    assert response.json() == JsonTestData.user_spec_added

    response = requests.get(
        f"{Config.BASE_URL}/user/spec/{user_id}",
    )
    assert response.status_code == Config.ResponseStatusCode.OK
    json_response = response.json()
    assert json_response["message"] == JsonTestData.user_spec_founded["message"]
    assert json_response["spec_id"] == spec_id

    response = requests.delete(f"{Config.BASE_URL}/user/{user_id}")
    assert response.status_code == Config.ResponseStatusCode.OK
    assert response.json() == JsonTestData.user_deleted

    response = requests.get(f"{Config.BASE_URL}/user/{user_id}")
    assert response.status_code == Config.ResponseStatusCode.NOT_FOUND
    assert response.json() == JsonTestData.user_not_founded

    response = requests.get(
        f"{Config.BASE_URL}/user/spec/{user_id}",
    )
    assert response.status_code == Config.ResponseStatusCode.NOT_FOUND
    assert response.json() == JsonTestData.user_spec_not_founded

    response = requests.delete(
        f"{Config.BASE_URL}/fill/spec/{spec_id}",
    )
    assert response.status_code == Config.ResponseStatusCode.OK
    assert response.json() == JsonTestData.spec_deleted

    response = requests.get(
        f"{Config.BASE_URL}/fill/spec/{spec_id}",
    )
    assert response.status_code == Config.ResponseStatusCode.NOT_FOUND
    assert response.json() == JsonTestData.spec_not_founded
