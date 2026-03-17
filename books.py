from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: str

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: int
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "a new book",
                "author": "codingwithnash",
                "description": "a new description",
                "rating": 5
            }
        }
    }


BOOKS = [
    Book(1, "Programing with python", "codewithavi", "A very nice book", 10),
    Book(2, "Computer Science Pro ", "codenash", "A very nice book", 8),
    Book(3, "Atomix Habits", "HendryCavil", "one of best", 10),
    Book(4, "Ikigai", "mushami", "super book", 9),
    Book(5, "master emotions", "author5", "A very nice book", 7)
]


@app.get("/books/endpoint")
async def read_all_books():
    return BOOKS


@app.get("/book_id")
async def get_book_id(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
