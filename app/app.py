from fastapi import FastAPI, HTTPException
from app.models import TodoCreate
from app.schemas import PostCreate
from typing import Literal


app = FastAPI()

# text_post = {
#     1: {"title": "Understanding FastAPI Routers", "content": "FastAPI routers allow you to split your API into multiple files, making your project more organized and scalable."},
#     2: {"title": "Dependency Injection in FastAPI", "content": "FastAPI's dependency injection system makes it easy to reuse code, manage database sessions, and handle authentication across your endpoints."},
#     3: {"title": "Pydantic Models for Data Validation", "content": "Pydantic models provide automatic data validation and serialization, ensuring your API requests and responses conform to your expected schemas."},
#     4: {"title": "Async and Await Support", "content": "FastAPI supports async def handlers, allowing you to write non-blocking code that can handle thousands of concurrent connections efficiently."},
#     5: {"title": "Automatic Interactive API Docs", "content": "FastAPI automatically generates Swagger UI and ReDoc documentation for your API endpoints, making it easy to test and explore your endpoints in a browser."},
#     6: {"title": "Database Integration with SQLAlchemy", "content": "Combining FastAPI with SQLAlchemy provides a powerful ORM for interacting with relational databases like PostgreSQL, SQLite, and MySQL."},
#     7: {"title": "Authentication with OAuth2 and JWT", "content": "FastAPI integrates seamlessly with OAuth2 and JSON Web Tokens to secure your API endpoints and manage user sessions."},
#     8: {"title": "Error Handling Best Practices", "content": "Proper error handling in FastAPI involves using HTTPException for expected errors and custom exception handlers for a consistent API response format."},
#     9: {"title": "Background Tasks and Celery", "content": "FastAPI supports background tasks for lightweight workloads, and integrates with Celery for heavy, asynchronous processing like sending emails or generating reports."},
#     10: {"title": "Testing FastAPI Applications", "content": "FastAPI works well with pytest and httpx, making it straightforward to write unit and integration tests for your API endpoints and dependencies."},
# }

# @app.get("/hello-world")
# def hello_world():
#     return {"message": "Hello World"}

# @app.get("/posts")
# def get_all_posts(limit:int):
#     if limit:
#         return list(text_post.values())[:limit]
#     return text_post

# @app.get("/posts/{id}")
# def get_post(id:int):
#     if id not in text_post:
#         raise HTTPException(status_code=404,detail="post not found")

#     return text_post.get(id)

# @app.post("/post")
# def create_post(post:PostCreate):
#     new_post = {"title":post.title,"content":post.content}
#     text_post[max(text_post.keys()) + 1] = new_post
#     return new_post

# @app.get("/todos/{todo_id}")
# def get_todo(todo_id: int):
#     return {"todo_id": todo_id, "type": str(type(todo_id))}

# @app.get("/users/{user_id}/todos/{todo_id}")
# def get_user_todo(user_id: int, todo_id: int):
#     return {"user_id": user_id, "todo_id": todo_id, "type": str(type(todo_id))}


# @app.get("/search-v2")
# def search_v2(query: str | None = None):
#     return {"query": query}


# @app.get("/users/{user_id}/todos")
# def get_user_todos(
#     user_id: int,
#     done: bool | None = None,
#     priority: str | None = None,
#     limit: int = 10
# ):
#     filters = {"user_id": user_id}
#     if done is not None:
#         filters["done"] = done
#     if priority is not None:
#         filters["priority"] = priority
#     filters["limit"] = limit


#     return filters

# database sementara
todos_db: dict[int,dict] = {}
next_id = 1

@app.post("/todos")
def create_todo(todo: TodoCreate):
    global next_id
    new_todo = {"id": next_id, **todo.model_dump()}
    todos_db[next_id] = new_todo
    next_id += 1
    return new_todo


@app.get('/todos')
def list_todos():
    return list(todos_db.values())

@app.get('/todos/{todo_id}')
def get_todo(todo_id:int):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos_db[todo_id]

@app.put('/todos/{todo_id}')
def update_todo(todo_id: int, todo: TodoCreate):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    stored = todos_db[todo_id]
    update_data = todo.model_dump(exclude_unset=True)
    stored.update(update_data)


@app.delete('/todos/{todo_id}')
def delete_todo(todo_id: int):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    del todos_db[todo_id]
    return {"status": "deleted", "id": todo_id}

@app.get('/todos/filter/done')
def get_done_todos():
    return [t for t in todos_db.values() if t["is_done"]]

@app.get('/todos/filter/priority/{level}')
def get_by_priority(level: Literal["low", "medium","hight"]):
    return [t for t in todos_db.values() if t['priority'] == level]