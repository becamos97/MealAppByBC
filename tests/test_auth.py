def test_register(client):
    resp = client.post("/register", data={
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "secret"
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Hello, testuser2" in resp.data

def test_login_logout(client, sample_user):
    resp = client.post("/login", data={
        "username": "testuser",
        "password": "password"
    }, follow_redirects=True)
    assert b"Welcome" in resp.data

    resp = client.get("/logout", follow_redirects=True)
    assert b"Login" in resp.data