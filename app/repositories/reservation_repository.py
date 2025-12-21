from app.models.reservation import Reservation
from app import db

class ReservationRepository:
    @staticmethod
    def create(reservation):
        db.session.add(reservation)
        db.session.commit()
        return reservation

    @staticmethod
    def find_active_by_book(book_id):
        # Bir kitap için bekleyen en eski rezervasyonu getirir (FIFO - İlk gelen ilk alır)
        return Reservation.query.filter_by(KitapID=book_id, Durum='Aktif')\
            .order_by(Reservation.RezervasyonTarihi.asc()).first()

    @staticmethod
    def find_by_user(user_id):
        return Reservation.query.filter_by(KullaniciID=user_id).order_by(Reservation.RezervasyonTarihi.desc()).all()

    @staticmethod
    def check_user_has_active_reservation(user_id, book_id):
        return Reservation.query.filter_by(KullaniciID=user_id, KitapID=book_id, Durum='Aktif').first()