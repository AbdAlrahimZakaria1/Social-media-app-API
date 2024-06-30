def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/api/v1/posts/")

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 201  # changed from 200


def test_unauthorized_user_get_all_posts(client):
    res = client.get("/api/v1/posts")
    assert res.status_code == 401


def test_get_one_posts(authorized_client, test_posts):
    res = authorized_client.get(f"/api/v1/posts/{test_posts[0].id}")
    post = res.json()["Post"]
    assert res.status_code == 200
    assert test_posts[0].id == post["id"]
    assert test_posts[0].title == post["title"]
    assert test_posts[0].content == post["content"]


def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/api/v1/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_posts_not_exist(client):
    res = client.get("/api/v1/posts/999")
    assert res.status_code == 401


def test_create_post(authorized_client):
    res = authorized_client.post(
        "/api/v1/posts/",
        json={"title": "nice title", "content": "nice content", "published": False},
    )

    post = res.json()
    assert res.status_code == 201
    assert post["title"] == "nice title"
    assert post["content"] == "nice content"
    assert post["published"] == False


def test_create_post_default(authorized_client):
    res = authorized_client.post(
        "/api/v1/posts/",
        json={"title": "nice title", "content": "nice content"},
    )

    post = res.json()
    assert res.status_code == 201
    assert post["title"] == "nice title"
    assert post["content"] == "nice content"
    assert post["published"] == True


def test_unauthorized_user_create_post(client):
    res = client.post(
        "/api/v1/posts/",
        json={"title": "nice title", "content": "nice content"},
    )
    assert res.status_code == 401


def test_unathorized_user_delete_post(client, test_posts):
    res = client.delete(f"/api/v1/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_user_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/api/v1/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_user_delete_post_non_exist(authorized_client):
    res = authorized_client.delete("/api/v1/posts/9999")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_user2, test_posts):
    res = authorized_client.delete(f"/api/v1/posts/{test_posts[2].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    res = authorized_client.put(f"/api/v1/posts/{test_posts[0].id}", json=data)
    post = res.json()

    assert res.status_code == 200
    assert post["title"] == data["title"]
    assert post["content"] == data["content"]


def test_update_other_user_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[2].id,
    }
    res = authorized_client.put(f"/api/v1/posts/{test_posts[2].id}", json=data)
    assert res.status_code == 403


def test_user_update_post_non_exist(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    res = authorized_client.put("/api/v1/posts/9999", json=data)
    assert res.status_code == 404


def test_unathorized_user_update_post(client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    res = client.put(f"/api/v1/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401
