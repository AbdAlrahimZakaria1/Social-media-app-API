import pytest
from app import models


@pytest.fixture
def test_vote(session, test_posts, test_user):
    voted_post = models.Vote(post_id=test_posts[0].id, user_id=test_user["id"])
    session.add(voted_post)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/api/v1/votes/", json={"post_id": test_posts[0].id, "vote_dir": 1}
    )
    assert res.status_code == 201


def test_vote_twice_on_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/api/v1/votes/", json={"post_id": test_posts[0].id, "vote_dir": 1}
    )
    assert res.status_code == 409


def test_delete_vote_on_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/api/v1/votes/", json={"post_id": test_posts[0].id, "vote_dir": 0}
    )
    assert res.status_code == 204


def test_delete_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/api/v1/votes/", json={"post_id": test_posts[0].id, "vote_dir": 0}
    )
    assert res.status_code == 404


def test_vote_twice_on_post_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/api/v1/votes/", json={"post_id": "9999", "vote_dir": 1}
    )
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    res = client.post(
        "/api/v1/votes/", json={"post_id": test_posts[0].id, "vote_dir": 1}
    )
    assert res.status_code == 401
