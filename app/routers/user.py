from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUser)    # Returns 201 HTTP status code after creating
def create_user(user: schemas.CreateUser, response: Response, db: Session = Depends(get_db)):            # Validates created user using the specified schema

    # Hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())           # Can automatically unpack the user content
    db.add(new_user)            # Staging the new inserts into the Database Table
    db.commit()                 # Pushing the Changes into PostGRESQL Database Table
    db.refresh(new_user)                # Returning the newly inserted table row 

    return new_user

@router.get("/{id}", response_model=schemas.ResponseUser)
def get_User(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with {id} doesn't exist")
    
    return user