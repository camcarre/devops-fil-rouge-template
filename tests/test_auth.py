from sqlalchemy import text


def test_register_creates_user(client):
    resp = client.post(
        "/auth/register",
        json={"username": "alice", "email": "alice@example.com", "password": "pw123456"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "alice@example.com"
    assert body["username"] == "alice"
    # Le mot de passe ne doit jamais ressortir.
    assert "password" not in body
    assert "password_hash" not in body


def test_register_duplicate_email(client):
    payload = {"username": "bob", "email": "bob@example.com", "password": "pw123456"}
    assert client.post("/auth/register", json=payload).status_code == 201
    resp = client.post("/auth/register", json={**payload, "username": "bob2"})
    assert resp.status_code == 400


def test_login_returns_token(client):
    client.post(
        "/auth/register",
        json={"username": "carol", "email": "carol@example.com", "password": "pw123456"},
    )
    resp = client.post(
        "/auth/login",
        data={"username": "carol@example.com", "password": "pw123456"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={"username": "dave", "email": "dave@example.com", "password": "pw123456"},
    )
    resp = client.post(
        "/auth/login",
        data={"username": "dave@example.com", "password": "wrong"},
    )
    assert resp.status_code == 401


def test_login_unknown_email(client):
    resp = client.post(
        "/auth/login",
        data={"username": "ghost@example.com", "password": "whatever"},
    )
    assert resp.status_code == 401


def test_password_stored_hashed_not_plain(client, db_engine):
    client.post(
        "/auth/register",
        json={"username": "erin", "email": "erin@example.com", "password": "plaintextpw"},
    )
    with db_engine.connect() as conn:
        row = conn.execute(
            text("SELECT password_hash FROM users WHERE email = 'erin@example.com'")
        ).first()
    assert row is not None
    assert row[0] != "plaintextpw"
    assert row[0].startswith("$2")  # préfixe bcrypt
