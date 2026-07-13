from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from models import Todo, TodoCreate, TodoRead, TodoUpdate, AskRequest, AskResponse
from database import create_db_and_tables, get_session
from crud import get_todo_or_404
from ai_client import ask_gemini

# --- Lifespan (pengganti on_event) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error":True,
            "message": exc.detail,
            "path": str(request.url)
        }
    )

@app.post("/todos")
def create_todo(todo: TodoCreate, session: Session = Depends(get_session)):
    print("DEBUG - data diterima:", todo)  # tambahin baris ini
    db_todo = Todo(**todo.model_dump())
    print("DEBUG - sebelum simpan:", db_todo)  # tambahin ini juga
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

@app.get("/todos", response_model=list[TodoRead])
def list_todos(session: Session = Depends(get_session)):
    return session.exec(select(Todo)).all()

@app.get('/todos/{todo_id}', response_model=TodoRead)
def get_todo(todo_id: int, session: Session = Depends(get_session)):
    return get_todo_or_404(todo_id, session)

@app.put('/todos/{todo_id}', response_model=TodoRead)
def update_todo(todo_id: int, todo: TodoUpdate, session: Session = Depends(get_session)):
    db_todo = get_todo_or_404(todo_id, session)
    update_data = todo.model_dump(exclude_unset=True)
    db_todo.sqlmodel_update(update_data)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@app.delete('/todos/{todo_id}')
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = get_todo_or_404(todo_id, session)
    session.delete(todo)
    session.commit()
    return {"status":"deleted", "id": todo_id}


@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    answer = ask_gemini(request.question)
    return AskResponse(question=request.question, answer=answer)


@app.post('/todos/summary')
def summarize_todos(session: Session=Depends(get_session)):
    todos = session.exec(select(Todo)).all()

    if not todos:
        return {"summary": "No todos available."}
    
    