#from app.main import *

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import model, schema, utils
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/posts")
async def root():
    return {"message": "welcome to my api"}

@router.get("/", response_model=List[schema.Post])
def get_post(db:Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return posts

'''
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    #print(posts)
    return posts
'''



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db:Session = Depends(get_db)):
    
    '''
    # sql statement
    cursor.execute("""INSERT INTO post (title, contents, published) VALUES (%s, %s, %s) RETURNING 
    * """,
                    (post.title, post.contents, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    '''
    """
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    """
    new_post = model.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}")
def get_post(id: int, response:Response, db:Session = Depends(get_db)):
    post=db.query(model.Post).filter(model.Post.id==id).first()

    '''
    # sql statement
    cursor.execute("""SELECT * FROM post WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    '''
    #post = find_post(int(id))
    if not post:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} not found")
    #response.status_code = status.HTTP_404_NOT_FOUND
    #return {"details": f"post with id {id} not found"}
    return post


@router.put("/{id}", response_model=schema.Post)
def update_posts(id: int, updated_post:schema.PostCreate, db:Session=Depends(get_db)):

    query_posts = db.query(model.Post).filter(model.Post.id==id)
    posts = query_posts.first()

    '''
    cursor.execute("""UPDATE post SET title = %s, contents = %s, published = %s WHERE id = %s 
    RETURNING *""", 
                    (post.title, post.contents, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    '''
    #index = find_index_post(id)
    if posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found")

    query_posts.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    #db.refresh(update_post)
    """
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    """
    return query_posts.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int, db:Session = Depends(get_db)):

    post=db.query(model.Post).filter(model.Post.id==id)
    '''
    # sql statement
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id)))
    del_post = cursor.fetchone()
    conn.commit()
    '''
    #index = find_index_post(id)  
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found")
    #my_posts.pop(index)

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)