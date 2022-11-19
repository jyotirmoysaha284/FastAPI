from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine)

# print(settings.database_password)

app = FastAPI()          # Creating the FastAPI Instance and store it inside app variable

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# my_posts = [{"id": 1, "title": "My Love", "content": "Car is my love", "published": True, "rating": 3}]

# # Finding any post using id
# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# # Finding the index of the post in my_posts dictionary
# def find_post_index(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}





