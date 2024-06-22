from typing import List
from .. import models, schemas, utils, oauth2
from ..database import get_db
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import json

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists.
    user_data = db.query(models.User).filter(models.User.email == user.email).first()
    if user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already used.",
        )

    # Hash password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # Get the pydantic model
    new_user = models.User(**user.model_dump())
    # Add to DB
    db.add(new_user)
    # Save changes to DB
    db.commit()
    # Get inserted row from DB
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=List[schemas.UserOut])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/currentUser", response_model=schemas.UserOut)
async def get_users(
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    users = (
        db.query(models.User).filter(models.Post.owner_id == current_user.id).first()
    )
    return users


@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid document id!"
        )
    return user
