from app.repositories.reservation_repository import ReservationRepository
from app.repositories.book_repository import BookRepository
from app.models.reservation import Reservation
from app import db

class ReservationService:
    @staticmethod
    def create_reservation(user_id, book_id):
        # 1. Kitap kontrolü
        book = BookRepository.find_by_id(book_id)
        if not book:
            return {'success': False, 'message': 'Kitap bulunamadı'}

        # 2. Stok kontrolü: Eğer stok varsa rezervasyona gerek yok
        if book.MevcutKopyaSayisi > 0:
            return {'success': False, 'message': 'Kitap şu an stokta mevcut, doğrudan ödünç alabilirsiniz.'}

        # 3. Mükerrer kayıt kontrolü
        existing = ReservationRepository.check_user_has_active_reservation(user_id, book_id)
        if existing:
            return {'success': False, 'message': 'Bu kitap için zaten aktif bir rezervasyonunuz var.'}

        try:
            reservation = Reservation(KullaniciID=user_id, KitapID=book_id)
            ReservationRepository.create(reservation)
            return {'success': True, 'message': 'Rezervasyon başarıyla oluşturuldu. Kitap geldiğinde size haber verilecek.'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def get_user_reservations(user_id):
        reservations = ReservationRepository.find_by_user(user_id)
        return [res.to_dict(include_book=True) for res in reservations]

    @staticmethod
    def cancel_reservation(reservation_id, user_id):
        # İptal mantığı buraya eklenebilir
        pass