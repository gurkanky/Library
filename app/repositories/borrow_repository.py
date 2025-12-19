from app import db
from app.models.borrow import Borrow
from typing import Optional, List
from datetime import datetime

class BorrowRepository:
    
    @staticmethod
    def find_by_id(borrow_id: int) -> Optional[Borrow]:
        return Borrow.query.get(borrow_id)
    
    @staticmethod
    def find_by_user(user_id: int) -> List[Borrow]:
        return Borrow.query.filter_by(KullaniciID=user_id).order_by(Borrow.OduncAlmaTarihi.desc()).all()
    
    @staticmethod
    def find_active_by_user(user_id: int) -> List[Borrow]:
        return Borrow.query.filter_by(KullaniciID=user_id, Durum='Aktif').all()
    
    @staticmethod
    def find_by_book(book_id: int) -> List[Borrow]:
        return Borrow.query.filter_by(KitapID=book_id).all()
    
    @staticmethod
    def find_overdue() -> List[Borrow]:
        return Borrow.query.filter(
            Borrow.Durum == 'Aktif',
            Borrow.BeklenenIadeTarihi < datetime.utcnow()
        ).all()
    
    @staticmethod
    def find_all() -> List[Borrow]:
        return Borrow.query.order_by(Borrow.OduncAlmaTarihi.desc()).all()
    
    @staticmethod
    def create(borrow: Borrow) -> Borrow:
        db.session.add(borrow)
        db.session.commit()
        db.session.refresh(borrow)
        return borrow
    
    @staticmethod
    def update(borrow: Borrow) -> Borrow:
        db.session.commit()
        db.session.refresh(borrow)
        return borrow
    
    @staticmethod
    def delete(borrow_id: int) -> bool:
        borrow = BorrowRepository.find_by_id(borrow_id)
        if borrow:
            db.session.delete(borrow)
            db.session.commit()
            return True
        return False

