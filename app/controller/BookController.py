import uuid
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.connection import connect
from app.model.bookModel import BookCreate, BookRead, BookUpdate
from app.repository.BookRepo import BookRepository
from app.schemas.Book import Book



router = APIRouter(prefix="/books", tags=["Books"])

class BookController:
    @router.get("/v1",response_model=List[BookRead],status_code=status.HTTP_200_OK)
    def get_all(db: Session = Depends(connect)):
        return BookRepository(db).get_all()
    
    @router.get("/v1/{Id}",response_model=BookRead,status_code=status.HTTP_200_OK)
    def get_by_id(Id: uuid.UUID, db: Session = Depends(connect)):
        repo = BookRepository(db).get_by_id(Id)

        if not repo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )

        return repo


    @router.post("/v1",response_model=BookRead,status_code=status.HTTP_201_CREATED)
    def create_book(body: BookCreate, db: Session = Depends(connect)):
        return BookRepository(db).create(Book(**body.model_dump()))


    @router.put("/v1/{Id}",response_model=BookRead,status_code=status.HTTP_200_OK)
    def update_book(Id: uuid.UUID,body: BookUpdate,db: Session = Depends(connect)):
        repo = BookRepository(db)

        if not BookRepository(db).get_by_id(Id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
            
        return BookRepository(db).update(Id, Book(**body.model_dump(exclude_unset=True)))


    @router.delete("/v1/{Id}",status_code=status.HTTP_204_NO_CONTENT)
    def delete(Id: uuid.UUID, db: Session = Depends(connect)):
        if not BookRepository(db).delete(Id):
            return None