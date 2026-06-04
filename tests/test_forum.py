def test_list_categories_public_empty(client):
    resp = client.get("/categories/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_category_requires_auth(client):
    resp = client.post("/categories/", json={"name": "General"})
    assert resp.status_code == 401


def test_create_category_with_auth(client, auth_headers):
    resp = client.post(
        "/categories/",
        json={"name": "General", "description": "Discussions générales"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "General"
    assert body["description"] == "Discussions générales"


def test_topics_404_unknown_category(client):
    assert client.get("/categories/999/topics").status_code == 404


def test_topic_create_and_list(client, auth_headers):
    cat = client.post("/categories/", json={"name": "Cat"}, headers=auth_headers).json()
    resp = client.post(
        f"/categories/{cat['id']}/topics",
        json={"title": "Hello"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["title"] == "Hello"

    listing = client.get(f"/categories/{cat['id']}/topics")
    assert listing.status_code == 200
    assert len(listing.json()) == 1


def test_topic_create_requires_auth(client, auth_headers):
    cat = client.post("/categories/", json={"name": "Cat2"}, headers=auth_headers).json()
    resp = client.post(f"/categories/{cat['id']}/topics", json={"title": "X"})
    assert resp.status_code == 401


def test_topic_create_404_unknown_category(client, auth_headers):
    resp = client.post(
        "/categories/999/topics", json={"title": "X"}, headers=auth_headers
    )
    assert resp.status_code == 404


def test_posts_404_unknown_topic(client):
    assert client.get("/topics/999/posts").status_code == 404


def test_post_create_and_list(client, auth_headers):
    cat = client.post("/categories/", json={"name": "Cat3"}, headers=auth_headers).json()
    topic = client.post(
        f"/categories/{cat['id']}/topics", json={"title": "T"}, headers=auth_headers
    ).json()
    resp = client.post(
        f"/topics/{topic['id']}/posts",
        json={"content": "first post"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["content"] == "first post"

    listing = client.get(f"/topics/{topic['id']}/posts")
    assert listing.status_code == 200
    assert len(listing.json()) == 1


def test_post_create_requires_auth(client, auth_headers):
    cat = client.post("/categories/", json={"name": "Cat4"}, headers=auth_headers).json()
    topic = client.post(
        f"/categories/{cat['id']}/topics", json={"title": "T2"}, headers=auth_headers
    ).json()
    resp = client.post(f"/topics/{topic['id']}/posts", json={"content": "x"})
    assert resp.status_code == 401
