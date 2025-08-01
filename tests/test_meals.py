def test_search_meals(client):
    resp = client.post("/search", data={"ingredients": "chicken"}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Search Results" in resp.data
    print(resp.data.decode())

def test_meal_detail(client):
    # Simulate a known meal ID
    resp = client.get("/meals/52770", follow_redirects=True)
    assert resp.status_code in [200, 302, 404]
    assert b"Instructions" in resp.data