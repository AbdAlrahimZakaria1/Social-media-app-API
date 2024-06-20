from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    # Here's how to do it using psycopg2
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # connection.commit()

    # Get the pydantic model
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    # Add to DB
    db.add(new_post)
    # Save changes to DB
    db.commit()
    # Get inserted row from DB
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=List[schemas.Post])
async def get_posts(
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


@router.get("/{id}", response_model=schemas.Post)
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid document id!"
        )
    return post


@router.put("/{id}", response_model=schemas.Post)
async def update_post(
    id: int,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform requested action.",
        )

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid post id."
        )

    post_query.update(post.model_dump())
    db.commit()

    return post_query.first()


@router.delete("/{id}")
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform requested action.",
        )

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid post id."
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
