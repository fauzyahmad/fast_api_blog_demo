from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette import status
from starlette.responses import Response
import database
import schemas
import models

router = APIRouter()

get_db = database.get_db


@router.get('/blog')
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return {
        'message': 'Data retreive successfully',
        'blogs': blogs
    }


@router.post('/blog',  status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/blog/{id_blog}', response_model=schemas.ShowBlog, status_code=status.HTTP_200_OK)
def get_blog(id_blog: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id_blog).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': 'data not found'}
        raise HTTPException(status_code=404, detail='Data not found')
    return blog


@router.delete('/blog/{id_blog}')
def delete_blog(id_blog: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id_blog)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='data not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'delete'


@router.put('/blog/{id_blog}')
def update_blog(id_blog: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id_blog)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='data not found')
    blog.update(request.dict())
    db.commit()
    return 'updated'
