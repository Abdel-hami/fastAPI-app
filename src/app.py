from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Form    
from src.schema import PostCreate, PostResponse
from src.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select


@asynccontextmanager
async def lifespan(src: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# creating post and saving to database
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...), # this line is used to specify that the file parameter is required and should be provided as a file upload.
    caption: str = Form(""), # this line is used to specify that the caption parameter should be provided as form data.
    session: AsyncSession = Depends(get_async_session) # this means that the sessioon parameter will be automatically provided by FastAPI using the get_async_session dependency. wich means that an instance of AsyncSession will be created and passed to the upload_file function whenever it is called.
):
    post = Post(
        caption=caption,
        url="dummy url",
        file_type="photo",
        file_name="dummy file name"
    )
    # adding the post to the session (database transaction)
    session.add(post)
    await session.commit()  # committing the transaction to save the post to the database
    # session is asynchronous context manager that manages the database connection and transaction. and asynchronous is a programming paradigm that allows multiple tasks to run concurrently without blocking each other.
    await session.refresh(post)  # refreshing the post instance to get the updated values from the database (like id and created_at)
    return post


# retrieving posts from database


@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
    # we did that because we need to access the database to retrieve the posts, so we need to bring this as a dependency injection.
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]  # extracting Post instances from the result, row[0] because each row is a tuple with one element (the Post instance)
    post_data = []
    for post in posts:
        post_data.append({
            "id": str(post.id),
            "caption": post.caption,
            "url": post.url,
            "file_type": post.file_type,
            "file_name": post.file_name,
            "created_at": post.created_at.isoformat()
        })

        return {"posts": post_data}































# text_posts =  {
#         1: {"title": "First Post", "content": "This is the first post."},
#         2: {"title": "Second Post", "content": "This is the second post."},
#         3: {"title": "Third Post", "content": "This is the third post."},
#         4: {"title": "Fourth Post", "content": "This is the fourth post."},
#         5: {"title": "Fifth Post", "content": "This is the fifth post."},
#         6: {"title": "Sixth Post", "content": "This is the sixth post."},
#         7: {"title": "Seventh Post", "content": "This is the seventh post."},
#         8: {"title": "Eighth Post", "content": "This is the eighth post."},
#         9: {"title": "Ninth Post", "content": "This is the ninth post."},
#         10: {"title": "Tenth Post", "content": "This is the tenth post."}
# }
# #Query Parammetrs are optional key-value pairs that can be added to the end of a URL to filter or sort data.
# @app.get("/posts")
# def get_all_posts(limit: int = None): #limit: int now it is manatory to pass an integer value as limit
#     if limit:
#         return list(text_posts.values())[:limit]
#     return text_posts

# @app.get("/posts/{id}")
# def get_post(id: int) -> PostResponse: #output type
#     if id not in text_posts:
#         # raising errors (HTTPException) in FastAPI
#         raise HTTPException(status_code=404, detail="Post not found")
#     return text_posts.get(id)
# # @app.get() is a fastapi decorator that defines a GET endpoint at the specified path.
# # a decorator is a special type of function that modifies the behavior of another function.

# #FastAPI: it automaticlly validates all data goinin into and coming out of the function 


# @app.post("/posts")
# def create_post(post: PostCreate) -> PostResponse: #output type 
#     new_post = {"title": post.title, "content": post.content}
#     text_posts[max(text_posts.keys()) + 1] = new_post
#     return new_post
#     # we do ax(text_posts.keys()) + 1 cause we want to add new post with new id and not overwrite existing one

# #output type and pydanti models are used to validate and serialize the response data from an endpoint.