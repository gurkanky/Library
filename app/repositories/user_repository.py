from app import db
from app.models.user import User
from typing import Optional, List

class UserRepository:
    
    @staticmethod
    def find_by_id(user_id: int) -> Optional[User]:
        return User.query.get(user_id)
    
    @staticmethod
    def find_by_email(email: str) -> Optional[User]:
        return User.query.filter_by(EPosta=email).first()
    
    @staticmethod
    def find_all() -> List[User]:
        return User.query.all()
    
    @staticmethod
    def find_by_role(role: str) -> List[User]:
        return User.query.filter_by(Rol=role).all()
    
    @staticmethod
    def create(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        # MSSQL IDENTITY için refresh() gerekmez
        return user
    
    @staticmethod
    def update(user: User) -> User:
        db.session.commit()
        return user
    
    @staticmethod
    def delete(user_id: int) -> bool:
        user = UserRepository.find_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

