from fastapi.testclient import TestClient
from login_api.app import app


client = TestClient(app)


def test_sample_workflow():
    # validation error at registration
    user_nok_1 = {
        "name": "ciccio",
        "surname": "pippo",
        "username": "marcolini",
        "email": "marcolini.alfieri@gmail.com",
        "password": "AXpv5Ts9le6zz",
        "secure_auth": True
    }
    response = client.post(
        "/v1/login_api/register/user",
        json=user_nok_1,
    )
    assert response.status_code == 422

    # workflow without 2fa
    user_1 = {
        "name": "nicco",
        "surname": "Saralli",
        "username": "xunggin",
        "email": "xunggin123@gmail.com",
        "password": "ZZpv5Td9!le6zz",
        "secure_auth": False
    }
    response = client.post(
        f"/v1/login_api/register/user",
        json=user_1,
    )
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["name"] == user_1["name"]
    assert json_response["surname"] == user_1["surname"]
    assert json_response["username"] == user_1["username"]
    assert json_response["email"] == user_1["email"]
    assert json_response["password"] == user_1["password"]
    assert json_response["secure_auth"] == user_1["secure_auth"]
    # login error
    login_data_err = {
        "username": "xunggin",
        "password": "ZZpv5Td9!le6za"
    }
    response = client.post(
        f"/v1/login_api/login",
        json=login_data_err,
    )
    assert response.status_code == 401
    # login succeded
    login_data = {
        "username": "xunggin",
        "password": "ZZpv5Td9!le6zz"
    }
    response = client.post(
        f"/v1/login_api/login",
        json=login_data,
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["access_token"] != ""
    assert json_response["token_type"] == "JWT"

    # workflow with 2fa
    user_2 = {
        "name": "ciccio",
        "surname": "pippo",
        "username": "marcolini",
        "email": "marcolini.alfieri@gmail.com",
        "password": "AXpv5Ts9!le6zz",
        "secure_auth": True
    }
    response = client.post(
        f"/v1/login_api/register/user",
        json=user_2,
    )
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["name"] == user_2["name"]
    assert json_response["surname"] == user_2["surname"]
    assert json_response["username"] == user_2["username"]
    assert json_response["email"] == user_2["email"]
    assert json_response["password"] == user_2["password"]
    assert json_response["secure_auth"] == user_2["secure_auth"]
    login_data = {
        "username": "marcolini",
        "password": "AXpv5Ts9!le6zz"
    }
    response = client.post(
        f"/v1/login_api/login",
        json=login_data,
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["access_token"] == ""
    assert json_response["token_type"] == "2FA"
    login_2fa_data = {
        "username": "marcolini",
        "password": "My-Otp"
    }
    response = client.post(
        f"/v1/login_api/login2fa",
        json=login_2fa_data,
    )
    assert response.status_code == 401
