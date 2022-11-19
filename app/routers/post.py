from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# Getting all posts
# @router.get("/", response_model=List[schemas.ResponsePost]) 
@router.get("/", response_model=List[schemas.ResponsePostWithVote])       # List of ResponsePost model will be needed to serialize all the posts
def get_post(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), 
                limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # ------------Working with RAW SQL command------------------
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # ----------Fetching Votes using Raw SQL-------------
    # select posts.*, count(votes.user_id) from posts LEFT join votes ON votes.post_id = posts.id group by posts.id;

    # --------------------Working with SQLAlchemy ORM------------------------
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(posts)

    posts = db.query(models.Post, func.count(models.Vote.user_id).label("vote_count")).join(
                        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
                        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    return posts

# Creating a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)    # Returns 201 HTTP status code after creating
def create_post(post: schemas.CreatePost, response: Response, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):            # Validates created post using the specified schema
                                                            # Response returns the status code, replaced with status_code in decorator
    
    # --------------Working with RAW SQL Commands-----------------------------
    # Code Vulnerable to SQL Injection
    # cursor.execute(f "INSERT INTO posts (title, content, is_published, rating) VALUES 
    #                 ({post.title}, {post.content}, {post.published}, {post.rating})" )

    # cursor.execute(""" INSERT INTO posts (title, content, is_published, rating) VALUES (%s, %s, %s, %s) RETURNING *""", 
    #                     (post.title, post.content, post.published, post.rating))
    # new_post = cursor.fetchone()
    
    # conn.commit()               # To push the changes into PostGRESQL Database

    # -----------------------Working with SQLAlchemy ORM------------------------
    # new_post = models.Post(title=post.title, content=post.content, is_published=post.is_published, rating=post.rating)

    # modified_post = post.dict()
    # modified_post.update({"owner_id": user_id.id})
    new_post = models.Post(owner_id=user_id.id, **post.dict())           # Can automatically unpack the user content
    db.add(new_post)            # Staging the new inserts into the Database Table
    db.commit()                 # Pushing the Changes into PostGRESQL Database Table
    db.refresh(new_post)                # Returning the newly inserted table row 

    # ----------------------Working with Traditional Array------------------------
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,10)
    # my_posts.append(post_dict)
    # response.status_code = status.HTTP_201_CREATED

    return new_post


@router.get("/{id}", response_model=schemas.ResponsePostWithVote)
def get_one_post(id: int, response: Response, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # post = find_post(id)

    # ----------------Working with RAW SQL Commands----------------------
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id), ))        # id needs to be converted into a string else give error
    # post = cursor.fetchone()

    # ---------------Working with SQLAlchemy ORM-------------------------
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, 
                             detail = f"Post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} not found"}

    post_vote = db.query(models.Post, func.count(models.Vote.user_id).label("vote_count")).join(
                models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
                models.Post.id == id).first()
    return post_vote


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # ----------------Working with RAW SQL Commands----------------------
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str(id), ))
    # deleted_post = cursor.fetchone()
    # conn.commit()                   # To push the changes into PostGRESQL Database

    # ---------------Working with SQLAlchemy ORM-------------------------
    post = db.query(models.Post).filter(models.Post.id == id)

    # index = find_post_index(id)
    if post.first() == None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, 
                             detail= f"Post with id {id} not found")
    # my_posts.pop(index)

    if post.first().owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="You do not have permission to perform requested action")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.ResponsePost)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    # ----------------Working with RAW SQL Commands----------------------
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, is_published=%s, rating=%s WHERE id=%s RETURNING * """, 
    #                 (post.title, post.content, post.published, post.rating, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()

    # index = find_post_index(id)

    # ---------------Working with SQLAlchemy ORM-------------------------
    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, 
                             detail= f"Post with id {id} not found")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict

    if post_query.first().owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="You do not have permission to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()