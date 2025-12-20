from app.repositories.borrow_repository import BorrowRepository
from app.repositories.book_repository import BookRepository
from app.repositories.user_repository import UserRepository
from app.models.borrow import Borrow
from app.services.email_service import EmailService
from app import db  # db nesnesini ekledik
from datetime import datetime
from typing import List, Dict


class BorrowService:

    @staticmethod
    def borrow_book(user_id: int, book_id: int, odunc_gun_sayisi: int = 21) -> Dict:
        # Kitap kontrolü
        book = BookRepository.find_by_id(book_id)
        if not book:
            return {'success': False, 'message': 'Kitap bulunamadı'}

        if book.MevcutKopyaSayisi <= 0:
            return {'success': False, 'message': 'Kitap stokta yok'}

        # Kullanıcı kontrolü
        user = UserRepository.find_by_id(user_id)
        if not user:
            return {'success': False, 'message': 'Kullanıcı bulunamadı'}

        # Aktif ödünç sayısı kontrolü (max 5 kitap)
        active_borrows = BorrowRepository.find_active_by_user(user_id)
        if len(active_borrows) >= 5:
            return {'success': False, 'message': 'Maksimum 5 kitap ödünç alabilirsiniz'}

        try:
            # 1. Ödünç işlemini oluştur
            borrow = Borrow(kullanici_id=user_id, kitap_id=book_id, odunc_gun_sayisi=odunc_gun_sayisi)
            db.session.add(borrow)

            # 2. MANUEL STOK GÜNCELLEME (Trigger yerine Python ile)
            book.MevcutKopyaSayisi -= 1
            db.session.add(book)

            # 3. Hepsini tek seferde kaydet
            db.session.commit()

            # E-posta gönder (İsteğe bağlı)
            try:
                EmailService.send_email(user.EPosta, "Kitap Ödünç Alındı", f"'{book.Baslik}' kitabını ödünç aldınız.")
            except:
                pass

            return {
                'success': True,
                'message': 'Kitap başarıyla ödünç alındı',
                'borrow': borrow.to_dict(include_book=True)
            }
        except Exception as e:
            db.session.rollback()  # Hata olursa işlemleri geri al
            return {'success': False, 'message': f'Hata oluştu: {str(e)}'}

    @staticmethod
    def return_book(borrow_id: int, user_id: int = None) -> Dict:
        borrow = BorrowRepository.find_by_id(borrow_id)
        if not borrow:
            return {'success': False, 'message': 'Ödünç kaydı bulunamadı'}

        # Yetki kontrolü
        if user_id and borrow.KullaniciID != user_id:
            return {'success': False, 'message': 'Bu işlemi yapmaya yetkiniz yok'}

        if borrow.Durum == 'IadeEdildi':
            return {'success': False, 'message': 'Kitap zaten iade edilmiş'}

        try:
            # 1. İade işlemini güncelle
            borrow.IadeTarihi = datetime.utcnow()
            borrow.Durum = 'IadeEdildi'

            # 2. MANUEL STOK GÜNCELLEME (Stok arttır)
            book = BookRepository.find_by_id(borrow.KitapID)
            if book:
                book.MevcutKopyaSayisi += 1
                db.session.add(book)

            db.session.add(borrow)
            db.session.commit()

            # Geç iade kontrolü ve E-posta
            try:
                if borrow.IadeTarihi > borrow.BeklenenIadeTarihi:
                    gecikme_gunu = (borrow.IadeTarihi - borrow.BeklenenIadeTarihi).days
                    EmailService.send_late_return_notification(borrow, gecikme_gunu)
            except Exception as e:
                print(f"[BorrowService] E-posta hatası: {str(e)}")

            return {
                'success': True,
                'message': 'Kitap iade edildi',
                'borrow': borrow.to_dict(include_book=True)
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'İade hatası: {str(e)}'}

    @staticmethod
    def get_user_borrows(user_id: int) -> List[Dict]:
        borrows = BorrowRepository.find_by_user(user_id)
        return [borrow.to_dict(include_book=True) for borrow in borrows]

    @staticmethod
    def get_all_borrows() -> List[Dict]:
        borrows = BorrowRepository.find_all()
        return [borrow.to_dict(include_book=True, include_user=True) for borrow in borrows]

    @staticmethod
    def get_overdue_borrows() -> List[Dict]:
        borrows = BorrowRepository.find_overdue()
        return [borrow.to_dict(include_book=True, include_user=True) for borrow in borrows]

    @staticmethod
    def check_overdue_borrows() -> Dict:
        """Geç iade edilen kitapları kontrol et"""
        overdue = BorrowRepository.find_overdue()
        count = 0

        for borrow in overdue:
            if borrow.Durum == 'Aktif':
                borrow.Durum = 'Gecikmis'
                db.session.add(borrow)
                count += 1
                # E-posta bildirimi
                try:
                    gecikme_gunu = (datetime.utcnow() - borrow.BeklenenIadeTarihi).days
                    EmailService.send_overdue_notification(borrow, gecikme_gunu)
                except:
                    pass

        if count > 0:
            db.session.commit()

        return {
            'success': True,
            'overdue_count': len(overdue),
            'overdue_borrows': [b.to_dict(include_book=True, include_user=True) for b in overdue]
        }