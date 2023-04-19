from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..schemas import schemas
from ..model import models
from .. import oauth2
from .. import db

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)


@router.post("", status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote, db: Session = Depends(db.get_db), current_user : int = Depends(oauth2.get_current_user)):
    print(vote.post_id)
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post Found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id) 
    found_vote = vote_query.first()
    if not found_vote:
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"success": True,  "msg" : "post liked"}
    else:
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"success": True, "msg" : "post un-liked"}