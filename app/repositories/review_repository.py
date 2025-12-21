from app.models.review import Review
from app import db

class ReviewRepository:
    @staticmethod
    def create(review):
        db.session.add(review)
        db.session.commit()
        return review

    @staticmethod
    def get_by_book(book_id):
        return Review.query.filter_by(KitapID=book_id).order_by(Review.OlusturmaTarihi.desc()).all()

    @staticmethod
    def get_by_id(review_id):
        return Review.query.get(review_id)

    @staticmethod
    def get_by_user_and_book(user_id, book_id):
        return Review.query.filter_by(KullaniciID=user_id, KitapID=book_id).first()

    @staticmethod
    def delete(review):
        db.session.delete(review)
        db.session.commit()