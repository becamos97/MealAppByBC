def test_edit_profile(client, sample_user):
    with client.session_transaction() as sess:
        sess["user_id"] = sample_user.id
    resp = client.post("/profile", data={
        "username": "newname",
        "email": "new@example.com"
    }, follow_redirects=True)
    assert b"profile updated" in resp.data