from fastapi import FastAPI
import models
from database import engine
from routers import user, blog

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(
    blog.router,
    prefix='/blog',
    tags=['Blog']
)

app.include_router(
    user.router,
    prefix='/user',
    tags=['User']
)
