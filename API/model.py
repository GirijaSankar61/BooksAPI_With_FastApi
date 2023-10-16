from pydantic import BaseModel


class Book(BaseModel):
    book_id: int
    name: str
    author: str 
    link: str 
    pages: int

    class Config:
        orm_mode = True