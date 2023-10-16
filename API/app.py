from fastapi import FastAPI
from databases import Database
from typing import List

from API.model import Book
from API.setup_db import books



app = FastAPI()

DATABASE_URL = "sqlite:///./books.db"
database = Database(DATABASE_URL)

@app.on_event("startup")
async def database_connect():
    await database.connect()


@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()

# def custom_openapi():
#     with open("openapi.json", "r") as openapi:
#         return json.load(openapi)

# app.openapi = custom_openapi

    title="BooksAPI",
    description="A books api to store books data.",
    version="0.0.1",
    docs_url = '/doc',
    # read_openapi_json='/openapi.json',
    contact={
        "name": "Abdul Rehman",
        "url": "http://booksapi.com/contact/",
        "email": "support@booksapi.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },

# @app.get('/books/', summary='All books',
#                     description="Get a list of all books objects.",
#                     response_model= List[Book])


# @app.delete("/books/{id}", summary="Get a book by Book ID",
#                            description="Returns the message from the server.", response_model=Book)                


@app.get('/books/', response_model= List[Book])
async def list_books():
    query = books.select()
    return await database.fetch_all(query)


@app.post("/books/", response_model=Book)
async def add_book(book: Book):
    query = books.insert().values(
        name=book.name, author=book.author,
        link=book.link, pages=book.pages)
    last_record_id = await database.execute(query)
    return {**book.dict(), "book_id": last_record_id}


@app.get("/books/{id}")
async def get_single_book(id: int):
    query = "SELECT * FROM books WHERE book_id = :book_id"
    result = await database.fetch_one(query=query, values={"book_id": id})
    return result

@app.delete("/books/{id}", response_model=str)
async def get_single_book(id: int):
    query = "DELETE FROM books WHERE book_id = :id"
    result = await database.execute(query=query, values={"id": id})
    return f'Book with the id: {id} deleted successfully!'
