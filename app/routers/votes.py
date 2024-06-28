from fastapi import status, HTTPException, Depends, APIRouter, Response

from .. import models, schemas, oauth2, database
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    # Check if post already exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} doesn not exist!",
        )

    # Check if the post is already voted for by the same user
    post_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id
    )

    found_post = post_query.first()
    if vote.vote_dir > 0:
        if found_post:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                detail=f"This post with id {vote.post_id} is already upvoted by user {current_user.id}",
            )

        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"status": "success", "message": "The post is upvoted!"}
    else:
        if not found_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote does not exist!",
            )

        post_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
