from app import db
from app.models.user import User
# ÖNEMLİ: Yeni oluşturduğumuz modeli import etmeliyiz
from app.models.favorite import Favorite
from app.models.borrow import Borrow
from app.models.penalty import Penalty
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

    # --- EKSİK OLAN KISIMLAR ---

    @staticmethod
    def add_favorite(user_id: int, book_id: int) -> bool:
        """Kullanıcının favorilerine kitap ekler"""
        # Önce var mı diye kontrol et
        existing = Favorite.query.filter_by(KullaniciID=user_id, KitapID=book_id).first()
        if not existing:
            fav = Favorite(KullaniciID=user_id, KitapID=book_id)
            db.session.add(fav)
            db.session.commit()
            return True
        return False

    @staticmethod
    def remove_favorite(user_id: int, book_id: int) -> bool:
        """Kullanıcının favorilerinden kitap çıkarır"""
        fav = Favorite.query.filter_by(KullaniciID=user_id, KitapID=book_id).first()
        if fav:
            db.session.delete(fav)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_favorites(user_id: int) -> List[Favorite]:
        """Kullanıcının tüm favorilerini getirir"""
        return Favorite.query.filter_by(KullaniciID=user_id).all()

    @staticmethod
    def check_has_debt_or_loans(user_id: int) -> bool:
        active_loans = Borrow.query.filter_by(KullaniciID=user_id, Durum='Aktif').count()
        unpaid_penalties = Penalty.query.filter_by(KullaniciID=user_id, Durum='Beklemede').count()
        return active_loans > 0 or unpaid_penalties > 0