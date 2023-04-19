from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from ..model import models
from ..schemas import schemas
from .. import oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Post']
)

# get all post of logged in user 
@router.get("", response_model=List[schemas.PostOut])
async def get_user_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute('''SELECT * FROM posts''')
    # posts =  cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    # return posts
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.user_id == current_user.id).all()
    print(posts)
    results = []
    for post in posts:
        new_dict = {}
        new_dict["Post"] = post[0].__dict__
        new_dict["Post"]["user"] = {
            "id" : current_user.id,
            "email" : current_user.email,
            "created_at": current_user.created_at
        }
        new_dict["votes"] = post[1]
        results.append(new_dict)
    return results

# get all posts
@router.get("/all", response_model=List[schemas.PostOut])
async def get_all_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit : int = 10, skip : int = 0, search : Optional[str] = ""):
    # cursor.execute('''SELECT * FROM posts''')
    # posts =  cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # return posts
    # posts = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = []
    for post in posts:
        new_dict = {}
        new_dict["Post"] = post[0].__dict__
        new_dict["Post"]["user"] = db.query(models.User).filter(models.User.id == new_dict["Post"]["user_id"]).first()
        new_dict["votes"] = post[1]
        results.append(new_dict)
    return results

# create post
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResp)
async def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)) :
    # cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''', (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print("Satyam")
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get post by post id
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute('''SELECT * FROM posts where id = %s''', (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    post = {
        "Post" : post[0].__dict__,
        "votes" : post[1]
    }
    post["Post"]["user"] = db.query(models.User).filter(models.User.id == post["Post"]["user_id"]).first()
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post Found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : "No post Found"}
    # if post.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this post")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id : int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # cursor.execute('''DELETE FROM posts where id = %s RETURNING *''', (str(id)))
    # deleted_post = cursor.fetchone()  
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")
    # conn.commit()

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this post")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}",  response_model=schemas.PostResp)
async def update_post(id: int, post : schemas.PostCreate,  db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s where id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_be_update = post_query.first()

    if post_to_be_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")

    if post_to_be_update.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this post")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()