from app import db
from datetime import datetime, timedelta
from app.models.borrow import Borrow
from app.models.penalty import Penalty
from app.repositories.borrow_repository import BorrowRepository
from app.repositories.book_repository import BookRepository
from app.repositories.user_repository import UserRepository
from app.repositories.reservation_repository import ReservationRepository
from app.services.email_service import EmailService


class BorrowService:
    @staticmethod
    def borrow_book(user_id, book_id, odunc_gun_sayisi=15):
        # 1. Kitap Kontrolü
        book = BookRepository.find_by_id(book_id)
        if not book:
            return {'success': False, 'message': 'Kitap bulunamadı'}

        if book.MevcutKopyaSayisi <= 0:
            return {'success': False, 'message': 'Kitap stokta yok (Tükendi)'}

        # 2. Kullanıcı Kontrolü
        user = UserRepository.find_by_id(user_id)
        if not user:
            return {'success': False, 'message': 'Kullanıcı bulunamadı'}

        # 3. Aktif ödünç sayısı kontrolü
        active_borrows = BorrowRepository.find_active_by_user(user_id)
        if len(active_borrows) >= 3:
            return {'success': False, 'message': 'Aynı anda en fazla 3 kitap ödünç alabilirsiniz.'}

        try:
            # 4. Stok Düşür
            book.MevcutKopyaSayisi -= 1
            db.session.add(book)

            # 5. Ödünç Kaydı Oluştur (DÜZELTME: Sadece init'in istediği parametreleri gönderiyoruz)
            # Modelinizdeki __init__ metodu tarihleri kendi hesaplıyor.
            borrow = Borrow(
                kullanici_id=user_id,
                kitap_id=book_id,
                odunc_gun_sayisi=odunc_gun_sayisi
            )

            db.session.add(borrow)
            db.session.commit()

            # --- E-POSTA GÖNDERİMİ ---
            try:
                # Erişimde Modeldeki sütun adını kullanıyoruz (BeklenenIadeTarihi)
                EmailService.send_borrow_notification(user, book, borrow.BeklenenIadeTarihi)
            except Exception as e:
                print(f"Ödünç maili hatası: {e}")
            # -------------------------

            return {
                'success': True,
                'message': 'Kitap başarıyla ödünç alındı.',
                'borrow': borrow.to_dict(include_book=True)
            }

        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f"Hata: {str(e)}"}

    @staticmethod
    def return_book(borrow_id, user_id=None):
        borrow = BorrowRepository.find_by_id(borrow_id)
        if not borrow:
            return {'success': False, 'message': 'Kayıt bulunamadı'}

        # Yetki kontrolü (Modelde KullaniciID büyük harf)
        if user_id and borrow.KullaniciID != user_id:
            return {'success': False, 'message': 'Bu işlem için yetkiniz yok'}

        # Durum ve IadeTarihi kontrolü
        if borrow.Durum == 'IadeEdildi' or borrow.IadeTarihi:
            return {'success': False, 'message': 'Bu kitap zaten iade edilmiş'}

        try:
            current_time = datetime.utcnow()
            borrow.IadeTarihi = current_time
            borrow.Durum = 'IadeEdildi'

            # Gecikme Cezası Hesaplama (Modelde BeklenenIadeTarihi büyük harf)
            if current_time > borrow.BeklenenIadeTarihi:
                delta = current_time - borrow.BeklenenIadeTarihi
                late_days = delta.days
                if late_days > 0:
                    penalty_amount = late_days * 1.5

                    # Penalty modeli
                    penalty = Penalty(
                        UyeID=borrow.KullaniciID,
                        OduncID=borrow.OduncID,
                        Tutar=penalty_amount,
                        Aciklama=f"{late_days} gün gecikme"
                    )
                    db.session.add(penalty)

            # Kitap Stoğunu Artır
            book = BookRepository.find_by_id(borrow.KitapID)
            if book:
                book.MevcutKopyaSayisi += 1
                db.session.add(book)

            # --- REZERVASYON KONTROLÜ ---
            next_reservation = ReservationRepository.find_active_by_book(borrow.KitapID)

            if next_reservation:
                reserver_user = UserRepository.find_by_id(next_reservation.KullaniciID)
                if reserver_user:
                    try:
                        EmailService.send_reservation_notification(reserver_user, book)
                        next_reservation.Durum = 'Tamamlandi'
                        db.session.add(next_reservation)
                    except Exception as email_err:
                        print(f"Rezervasyon mail hatası: {email_err}")
            # ---------------------------

            db.session.add(borrow)
            db.session.commit()

            return {'success': True, 'message': 'Kitap iade alındı.'}

        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    @staticmethod
    def get_user_borrows(user_id):
        borrows = BorrowRepository.find_by_user(user_id)
        return [b.to_dict(include_book=True) for b in borrows]

    @staticmethod
    def get_all_borrows():
        borrows = BorrowRepository.find_all()
        return [b.to_dict(include_book=True, include_user=True) for b in borrows]

    @staticmethod
    def get_overdue_borrows():
        borrows = BorrowRepository.find_overdue()
        return [b.to_dict(include_book=True, include_user=True) for b in borrows]

    @staticmethod
    def check_overdue_borrows():
        overdue_list = BorrowRepository.find_overdue()
        return {'success': True, 'count': len(overdue_list)}