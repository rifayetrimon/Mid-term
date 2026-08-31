def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={"username": "sadia", "email": "sadia@mail.com", "password": "123456"},
    )
    assert response.status_code == 201
    assert response.json()["username"] == "sadia"
    assert "hashed_password" not in response.json()


def test_login_user(client, headers):
    assert headers["Authorization"].startswith("Bearer ")


def test_login_with_wrong_password(client, headers):
    response = client.post(
        "/auth/login", json={"username": "rifayet", "password": "wrong"}
    )
    assert response.status_code == 401


def test_transactions_without_token(client):
    response = client.get("/transactions")
    assert response.status_code == 401
