from sqlmodel import SQLModel, Field as SQLField
from typing import Literal

# base field common use
class TodoBase(SQLModel):
    title: str
    priority: str = "medium"
    is_done: bool = False

# table field in database
class Todo(TodoBase, table=True):
    id: int | None = SQLField(default=None, primary_key=True)

# request body field
class TodoCreate(TodoBase):
    pass

# response body field with id
class TodoRead(TodoBase):
    id: int


class TodoUpdate(SQLModel):
    title: str | None = None
    priority: Literal["low", "medium", "high"] | None = None
    is_done: bool | None = None

class AskRequest(SQLModel):
    question: str = SQLField(min_length=1, max_length=1000)

class AskResponse(SQLModel):
    question: str
    answer: str

class ChatRequest(SQLModel):
    session_id: str = SQLField(min_length=1)
    message: str = SQLField(min_length=1, max_length=1000)


class ChatResponse(SQLModel):
    session_id: str
    message: str
    reply: str