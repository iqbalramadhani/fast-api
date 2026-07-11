from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from models import Todo, TodoCreate, TodoRead, TodoUpdate
from database import create_db_and_tables, get_session

# --- Lifespan (pengganti on_event) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

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
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put('/todos/{todo_id}', response_model=TodoRead)
def update_todo(todo_id: int, todo: TodoUpdate, session: Session = Depends(get_session)):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    update_data = todo.model_dump(exclude_unset=True)
    db_todo.sqlmodel_update(update_data)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@app.delete('/todos/{todo_id}')
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return {"status":"deleted", "id": todo_id}