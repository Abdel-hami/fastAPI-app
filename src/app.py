from fastapi import FastAPI, HTTPException 
from src.schema import PostCreate, PostResponse
from src.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(src: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
text_posts =  {
        1: {"title": "First Post", "content": "This is the first post."},
        2: {"title": "Second Post", "content": "This is the second post."},
        3: {"title": "Third Post", "content": "This is the third post."},
        4: {"title": "Fourth Post", "content": "This is the fourth post."},
        5: {"title": "Fifth Post", "content": "This is the fifth post."},
        6: {"title": "Sixth Post", "content": "This is the sixth post."},
        7: {"title": "Seventh Post", "content": "This is the seventh post."},
        8: {"title": "Eighth Post", "content": "This is the eighth post."},
        9: {"title": "Ninth Post", "content": "This is the ninth post."},
        10: {"title": "Tenth Post", "content": "This is the tenth post."}
}
#Query Parammetrs are optional key-value pairs that can be added to the end of a URL to filter or sort data.
@app.get("/posts")
def get_all_posts(limit: int = None): #limit: int now it is manatory to pass an integer value as limit
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id: int) -> PostResponse: #output type
    if id not in text_posts:
        # raising errors (HTTPException) in FastAPI
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)
# @app.get() is a fastapi decorator that defines a GET endpoint at the specified path.
# a decorator is a special type of function that modifies the behavior of another function.

#FastAPI: it automaticlly validates all data goinin into and coming out of the function 


@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse: #output type 
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post
    # we do ax(text_posts.keys()) + 1 cause we want to add new post with new id and not overwrite existing one

#output type and pydanti models are used to validate and serialize the response data from an endpoint.