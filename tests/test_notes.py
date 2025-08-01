def test_add_note(client, sample_user):
    with client.session_transaction() as sess:
        sess["user_id"] = sample_user.id
    resp = client.post("/meals/52772/notes/add", data={"content": "Yummy!"}, follow_redirects=True)
    assert b"Note added" in resp.data