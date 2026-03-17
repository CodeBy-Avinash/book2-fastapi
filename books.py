from fastapi import Body, FastAPI, Path
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: str
    publish_date: int

    def __init__(self, id, title, author, description, rating, publish_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date


class BookRequest(BaseModel):
    id: int
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int
    publish_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "a new book",
                "author": "codingwithnash",
                "description": "a new description",
                "rating": 5,
                "publish_date": 2029
            }
        }
    }


BOOKS = [
    Book(1, "Programing with python", "codewithavi",
         "A very nice book", 10, 2011),
    Book(2, "Computer Science Pro ", "codenash", "A very nice book", 8, 2025),
    Book(3, "Atomix Habits", "HendryCavil", "one of best", 10, 2029),
    Book(4, "Ikigai", "mushami", "super book", 9, 2000),
    Book(5, "master emotions", "author5", "A very nice book", 7, 2027)
]


@app.get("/books/endpoint")
async def read_all_books():
    return BOOKS


@app.get("books/book_id")
async def get_book_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books/")
async def read_book_by_rating(book_rating: int):
    read_book_rating = []
    for book in BOOKS:
        if book.rating == book_rating:
            read_book_rating.append(book)
    return read_book_rating


@app.get("/books/publish")
async def get_publish_book(publish_book: int):
    books_to_return = []
    for book in BOOKS:
        if book.publish_date == publish_book:
            books_to_return.append(book)
    return books_to_return


@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/book/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.delete("/book/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
