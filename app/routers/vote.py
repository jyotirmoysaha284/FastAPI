from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, oauth2, models
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/")
def vote(vote: schemas.Vote, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    find_post = db.query(models.Post).filter(models.Post.id==vote.post_id)
    if not find_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {vote.post_id} doesn't exist")

    found_vote_query = db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id==user_id.id)
    found_vote = found_vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Post of id {vote.post_id} has already been voted by User {user_id.id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = user_id.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No vote found for post {vote.post_id} for user {user_id.id}")
        found_vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Successfully deleted vote"}

