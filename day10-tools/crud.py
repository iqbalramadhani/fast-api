from fastapi import HTTPException
from sqlmodel import Session
from models import Todo

def get_todo_or_404(todo_id: int, session: Session):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo dengan id {todo_id} not found")
    return todo