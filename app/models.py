from pydantic import BaseModel, Field
from typing import Literal

class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    priority: Literal["low", "medium", "hight"] = "medium"
    is_done: bool = False
