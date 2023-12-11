from pydantic import BaseModel
from datetime import datetime


class NewLineOfBook(BaseModel):
    datetime: datetime
    title: str
    text: str


class BookInfo(BaseModel):
    datetime: datetime
    title: str
    x_avg_count_in_line: float
