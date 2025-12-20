from app import db
from app.models.author import Author
from typing import Optional, List

class AuthorRepository:
    
    @staticmethod
    def find_by_id(author_id: int) -> Optional[Author]:
        return Author.query.get(author_id)
    
    @staticmethod
    def find_all() -> List[Author]:
        return Author.query.all()
    
    @staticmethod
    def find_by_name(ad: str, soyad: str = None) -> List[Author]:
        query = Author.query.filter(Author.Ad.like(f'%{ad}%'))
        if soyad:
            query = query.filter(Author.Soyad.like(f'%{soyad}%'))
        return query.all()
    
    @staticmethod
    def create(author: Author) -> Author:
        db.session.add(author)
        db.session.commit()
        # MSSQL IDENTITY için refresh() gerekmez
        return author
    
    @staticmethod
    def update(author: Author) -> Author:
        db.session.commit()
        return author
    
    @staticmethod
    def delete(author_id: int) -> bool:
        author = AuthorRepository.find_by_id(author_id)
        if author:
            db.session.delete(author)
            db.session.commit()
            return True
        return False

