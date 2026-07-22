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

def update_todo_status_tool(todo_id: int, is_done: bool) -> str:
    """Mengubah status selesai/belum selesai dari sebuah todo berdasarkan ID.
    Gunakan ini ketika user bilang sudah menyelesaikan tugas ternetu,
    atau ingin ulang tugas sebagai belum selesai"""
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            return f"Todo dengan ID {todo_id} tidak ditemukan"
        todo.is_done = is_done
        session.add(todo)
        session.commit()
        status = "selesai" if is_done else "belum selesai"
        return f"Todo {todo.title} ditandai sebagai {status}"
    
# def list_all_todos_tool() -> str:
#     """Menampilkan semua todo (baik yang sudah maupun belum selesai),
#     lebgkap dengan ID-nya. Gunakan ini ketika user inging melihat daftar tugas lengkap
#     mereka, atau butuh tahu ID todo tertentu."""
#     with Session(engine) as session:
#         todos = session.exec(select(Todo)).all()
#         if not todos:
#             return "Belum ada todo sama sekali"
#         result = "\n".join(
#             [f"- ID {t.id}: {t.title} (prioritas: {t.priority}, selesai: {t.is_done})" for t in todos]
#         )

#         return result

def update_todo_status_tool(todo_id: int, is_done: bool) -> str:
    """Mengubah status selesai/belum selesai dari sebuah todo berdasarkan ID.
    Gunakan ini ketika user bilang sudah menyesaikan tugas tertentu,
    atau ingin menandai ulang tugas sebagai belum selesai."""
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            return f"Todo dengan id {todo_id} tidak ditemukan"
        todo.is_done = is_done
        session.add(todo)
        session.commit()
        status = "selesai" if is_done else "belum selesai"
        return f"Todo {todo.title} ditandai sebagai {status}"


def list_all_todos_tool() -> str:
    """Menampilkan SEMUA todo (baik yang sudah maupun belum selesai) lengkap dengan ID-nya. Gunakan ini ketika user
    ingin melihat daftar lengkap tugas mereka, atau butuh tahu ID todo tertentu."""
    with Session(engine) as session:
        todos = session.exec(select(Todo)).all()
        if not todos:
            return "Belum ada todo sama sekali"
        
        result = "\n".join(
            [f"- ID {t.id}: {t.title} (prioritas: {t.priority}, selesai: {t.is_done})"for t in todos]
        )

        return result