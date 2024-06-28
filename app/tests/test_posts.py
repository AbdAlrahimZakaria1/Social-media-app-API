def test_get_posts(authorized_client):
    posts = authorized_client.get("/api/v1/posts/")
    print(posts.json())
