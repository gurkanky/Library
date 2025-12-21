from app.repositories.review_repository import ReviewRepository
from app.models.review import Review
from typing import Dict, List

class ReviewService:
    @staticmethod
    def add_review(user_id: int, book_id: int, score: int, comment: str) -> Dict:
        # Puan kontrolü
        if not (1 <= score <= 5):
            return {'success': False, 'message': 'Puan 1 ile 5 arasında olmalıdır.'}

        # Mükerrer yorum kontrolü
        existing = ReviewRepository.get_by_user_and_book(user_id, book_id)
        if existing:
            return {'success': False, 'message': 'Bu kitaba daha önce puan verdiniz.'}

        try:
            review = Review(KullaniciID=user_id, KitapID=book_id, Puan=score, Yorum=comment)
            ReviewRepository.create(review)
            return {'success': True, 'message': 'Yorumunuz eklendi.'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def get_book_reviews(book_id: int) -> List[Dict]:
        reviews = ReviewRepository.get_by_book(book_id)
        # Ortalama puanı da hesaplayabiliriz
        return [r.to_dict(include_user=True) for r in reviews]

    @staticmethod
    def delete_review(review_id: int, user_id: int, is_admin: bool = False) -> Dict:
        review = ReviewRepository.get_by_id(review_id)
        if not review:
            return {'success': False, 'message': 'Yorum bulunamadı.'}

        # Sadece yorum sahibi veya admin silebilir
        if review.KullaniciID != user_id and not is_admin:
            return {'success': False, 'message': 'Bu işlem için yetkiniz yok.'}

        try:
            ReviewRepository.delete(review)
            return {'success': True, 'message': 'Yorum silindi.'}
        except Exception as e:
            return {'success': False, 'message': str(e)}