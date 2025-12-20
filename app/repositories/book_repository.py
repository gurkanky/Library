from app import db
from app.models.book import Book
from app.models.book_author import BookAuthor
from typing import Optional, List

class BookRepository:
    
    @staticmethod
    def find_by_id(book_id: int) -> Optional[Book]:
        return Book.query.get(book_id)
    
    @staticmethod
    def find_all() -> List[Book]:
        return Book.query.all()
    
    @staticmethod
    def find_by_title(title: str) -> List[Book]:
        return Book.query.filter(Book.Baslik.like(f'%{title}%')).all()
    
    @staticmethod
    def find_by_isbn(isbn: str) -> Optional[Book]:
        return Book.query.filter_by(ISBN=isbn).first()
    
    @staticmethod
    def find_by_category(category_id: int) -> List[Book]:
        return Book.query.filter_by(KategoriID=category_id).all()
    
    @staticmethod
    def find_available() -> List[Book]:
        return Book.query.filter(Book.MevcutKopyaSayisi > 0).all()
    
    @staticmethod
    def create(book: Book) -> Book:
        db.session.add(book)
        db.session.commit()
        # MSSQL IDENTITY için refresh() gerekmez
        return book
    
    @staticmethod
    def update(book: Book) -> Book:
        db.session.commit()
        return book
    
    @staticmethod
    def delete(book_id: int) -> bool:
        book = BookRepository.find_by_id(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def add_author(book_id: int, author_id: int) -> BookAuthor:
        book_author = BookAuthor(KitapID=book_id, YazarID=author_id)
        db.session.add(book_author)
        db.session.commit()
        return book_author
    
    @staticmethod
    def remove_author(book_id: int, author_id: int) -> bool:
        book_author = BookAuthor.query.filter_by(
            KitapID=book_id, 
            YazarID=author_id
        ).first()
        if book_author:
            db.session.delete(book_author)
            db.session.commit()
            return True
        return False

