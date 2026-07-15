from sqlmodel import Session, select
from database import engine
from models import Todo

def create_todo_tools(title:str, priority: str="medium") -> str:
    """Membuat todo baru dengan judul dan prioritas tertentu.
    Prioritas  harus salah satu dari: low, medium, high.
    Gunakan ini ketika user meminta untuk membuat / menambah tugas baru."""
    with Session(engine) as session:
        todo = Todo(title=title, priority=priority)
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return f"Todo {title} berhasil dibuat dengan id {todo.id} dan prioritas {priority}"
    

def list_pending_todos_tool() -> str:
    """Menampilkan semua todo yang belum selesai.
    Gunakan ini ketika user bertanya tentang tugas yang belum di kerjakan."""
    with Session(engine) as session:
        todos = session.exec(select(Todo).where(Todo.is_done == False)).all()
        if not todos:
            return "Tidak ada todo yang pending, semua sudah sekesai!"
        result = "\n".join([f"- {t.title} (prioritas : {t.priority})" for t in todos])

        return result