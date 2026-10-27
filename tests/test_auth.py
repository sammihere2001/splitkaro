def test_register_login_and_me(client, make_user):
    user_id, headers = make_user("Ali", "ali@example.com")

    res = client.get("/auth/me", headers=headers)

    assert res.status_code == 200
    assert res.json() == {"id": user_id, "name": "Ali", "email": "ali@example.com"}


def test_password_is_not_returned(client):
    res = client.post(
        "/auth/register", json={"name": "Ali", "email": "ali@example.com", "password": "password123"}
    )
    assert "password" not in res.text
    assert "password_hash" not in res.json()


def test_duplicate_email_is_rejected_case_insensitively(client, make_user):
    make_user("Ali", "ali@example.com")

    res = client.post(
        "/auth/register", json={"name": "Ali 2", "email": "ALI@example.com", "password": "password123"}
    )

    assert res.status_code == 409


def test_short_password_is_rejected(client):
    res = client.post("/auth/register", json={"name": "Ali", "email": "ali@example.com", "password": "123"})
    assert res.status_code == 422


def test_wrong_password_is_rejected(client, make_user):
    make_user("Ali", "ali@example.com")

    res = client.post("/auth/login", data={"username": "ali@example.com", "password": "wrong-password"})

    assert res.status_code == 401


def test_protected_route_needs_a_valid_token(client):
    assert client.get("/auth/me").status_code == 401
    assert client.get("/auth/me", headers={"Authorization": "Bearer not-a-token"}).status_code == 401
