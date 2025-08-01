def test_add_favorite(client, sample_user):
    with app.app_context():
    meal = Meal(id=1111, name="Fake Meal")
    db.session.add(meal)
    db.session.commit()

    with client.session_transaction() as sess:
    sess["user_id"] = sample_user.id

    resp = client.post("/favorites/1111", follow_redirects=True)
    assert b"added to favorites" in resp.data