from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field,computed_field,field_validator,model_validator
from typing import Optional,Annotated,Literal
import json

app=FastAPI()

class Book(BaseModel):
    id:Annotated[str,Field(...,min_length=4,max_length=6,description="Id of the book")]
    title:Annotated[str,Field(...,min_length=2,max_length=100,description="Title of the book")]
    author:Annotated[str,Field(...,min_length=2,description="Author of the book")]
    category:Literal[ "Programming","Novel","Science","History","Self Help","Business"]
    price:Annotated[float,Field(gt=0)]
    quantity:Annotated[int,Field(ge=1)]
    language:Literal["English","urdu","Arabic"]

    @computed_field
    @property
    def inventory_value(self)->str:
        return self.price *self.quantity
    
    @field_validator("title")
    @classmethod
    def valid_name(cls,value):
        if len(value)==1:
            raise ValueError(detail="Title can't contain 1 number")
        
        return value
    
    @model_validator(mode="after")
    def valid(self):
        if self.category=='Programming' and self.language=='Urdu':
            raise ValueError("Invalid information")
        
        return self
    

class BookUpdate(BaseModel):
    title:Optional[Annotated[str,Field(min_length=2,max_length=100,description="Title of the book")]]=None
    author:Optional[Annotated[str,Field(min_length=2,description="Author of the book")]]=None
    category:Optional[Literal[ "Programming","Novel","Science","History","Self Help","Business"]]=None
    price:Optional[Annotated[float,Field(gt=0)]]=None
    quantity:Optional[Annotated[int,Field(ge=1)]]=None
    language:Optional[Literal["English","urdu","Arabic"]]=None

class BookResponse(BaseModel):
    title: str
    author: str
    category: str
    price: float
    quantity: int
    language: str
    

def load_data():
    with open("books.json","r") as f:
        data=json.load(f)
        return data
    
def save_data(data):
    with open("books.json","w") as f:
        json.dump(data,f,indent=4)
        
#POST request
@app.post("/books")
def add_books(book: Book):
    data = load_data()

    # Check if the book already exists (same title and author)
    for key, val in data.items():
        if val["title"] == book.title and val["author"] == book.author:
            data[key]["quantity"] += book.quantity
            save_data(data)

            return {
                "message": "Book already exists. Quantity updated successfully.",
                "book": data[key]
            }

    # Check if the new ID is already in use
    if book.id in data:
        raise HTTPException(
            status_code=400,
            detail="Book ID already exists."
        )

    # Add a new book
    data[book.id] = book.model_dump(exclude={"id"})
    save_data(data)

    return {
        "message": "New book added successfully.",
        "book": data[book.id]
    }

#GET all books
@app.get('/books',response_model=dict[str, BookResponse])
def return_all_Books():
    data=load_data()
    return data

#GET one book
@app.get('/books/{book_id}',response_model=BookResponse)
def return_all_Books(book_id:str):
    data=load_data()
    if not book_id in data:
         raise HTTPException(status_code=404,detail="Book not found")
    return data[book_id]

#Update book (PATCH)
@app.patch('/books/{book_id}')
def update_Books(book_id:str,book:BookUpdate):
    data=load_data()
    if book_id not in data:
        raise HTTPException(status_code=404,detail="Book not found")
    
    if book.title is not None:
        data[book_id]['title']=book.title

    if book.author is not None:
        data[book_id]['author']=book.author
    
    if book.category is not None:
       data[book_id]["category"] = book.category

    if book.price is not None:
        data[book_id]['price']=book.price

    if book.quantity is not None:
        data[book_id]['quantity']=book.quantity

    if book.language is not None:
       data[book_id]["language"] = book.language
    
    save_data(data)

    return{"message":"Book Updated successfully"}


#Update book (PATCH)
@app.put('/books/{book_id}')
def update_Books2(book_id:str,book:Book):
    data=load_data()
    if book_id not in data:
        raise HTTPException(status_code=404,detail="Book not found")
    
    data[book_id]=book.model_dump(exclude={"id"})
    save_data(data)
    return{"message":"Book Updated successfully"}


#Delete books 
@app.delete('/books/{book_id}')
def remove_Books(book_id:str):
    data=load_data()
    if book_id not in data:
        raise HTTPException(status_code=404,detail="Book not found")
    
    del data[book_id]

    save_data(data)
    return{"message":"Book Deleted successfully"}
    
#Delete ALL books 
@app.delete('/books')
def remove_Books_all():
    data={}
    save_data(data)
    return {"Message":"All books deleted"}
    
#Search books by Author
@app.get("/books/search/author",response_model=dict[str, BookResponse])
def search_by_author(author: str):
    data = load_data()
    results = {}

    for key, val in data.items():
        if val["author"] == author:
            results[key] = val

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No books found by this author"
        )

    return results

#Search books by Category
@app.get("/books/search/category",response_model=dict[str, BookResponse])
def search_by_category(category: str):
    data = load_data()
    results = {}

    for key, val in data.items():
        if val["category"] == category:
            results[key] = val

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No books found in this category"
        )

    return results


#Search books by Language
@app.get("/books/search/language",response_model=dict[str, BookResponse])
def search_by_language(language: str):
    data = load_data()
    results = {}

    for key, val in data.items():
        if val["language"] == language:
            results[key] = val

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No books found in this language"
        )

    return results

#Return count of books
@app.get('/count')
def search_book():
    data=load_data()
    return {
        'count':len(data)
    }
    

@app.get("/books/quantity")
def total_quantity():
    data = load_data()

    total = 0

    for value in data.values():
        total += value["quantity"]

    return {
        "total_books": total
    }
    
@app.get("/books/stats/value")
def inventory_value():
    data = load_data()

    total = 0

    for value in data.values():
        total += value["price"] * value["quantity"]

    return {
        "inventory_value": total
    }

@app.get("/books/stats/most-expensive")
def expensive_book():
    data = load_data()

    expensive = None

    for value in data.values():

        if expensive is None:
            expensive = value

        elif value["price"] > expensive["price"]:
            expensive = value

    return expensive

@app.get("/books/stats/cheapest")
def cheapest_book():
    data = load_data()

    cheapest = None

    for value in data.values():

        if cheapest is None:
            cheapest = value

        elif value["price"] < cheapest["price"]:
            cheapest = value

    return cheapest

@app.get("/books/stats/average-price")
def average_price():
    data = load_data()

    total = 0

    for value in data.values():
        total += value["price"]

    average = total / len(data)

    return {
        "average_price": average
    }

@app.get("/books/stats/categories")
def category_stats():
    data = load_data()

    result = {}

    for value in data.values():

        category = value["category"]

        if category in result:
            result[category] += 1
        else:
            result[category] = 1

    return result

@app.get("/books/stats/languages")
def language_stats():
    data = load_data()

    result = {}

    for value in data.values():

        language = value["language"]

        if language in result:
            result[language] += 1
        else:
            result[language] = 1

    return result

from fastapi.responses import FileResponse

@app.get("/books/download")
def download_books():
    return FileResponse(
        path="books.json",
        filename="books.json",
        media_type="application/json"
    )


