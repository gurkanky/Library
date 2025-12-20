from app.repositories.borrow_repository import BorrowRepository
from app.repositories.book_repository import BookRepository
from app.repositories.user_repository import UserRepository
from app.repositories.penalty_repository import PenaltyRepository
from app.models.borrow import Borrow
from app.models.penalty import Penalty
from app.services.email_service import EmailService
from datetime import datetime, timedelta
from typing import List, Dict, Optional

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
        
        # Ödünç işlemi oluştur
        borrow = Borrow(kullanici_id=user_id, kitap_id=book_id, odunc_gun_sayisi=odunc_gun_sayisi)
        borrow = BorrowRepository.create(borrow)
        
        # Kitap stok güncellemesi trigger ile yapılacak
        
        return {
            'success': True,
            'message': 'Kitap ödünç alındı',
            'borrow': borrow.to_dict(include_book=True)
        }
    
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
        
        # İade işlemi
        borrow.IadeTarihi = datetime.utcnow()
        borrow.Durum = 'IadeEdildi'
        borrow = BorrowRepository.update(borrow)
        
        # Geç iade kontrolü (trigger ile ceza hesaplanacak)
        # E-posta bildirimi gönder (hata olsa bile devam et)
        try:
            if borrow.IadeTarihi > borrow.BeklenenIadeTarihi:
                gecikme_gunu = (borrow.IadeTarihi - borrow.BeklenenIadeTarihi).days
                EmailService.send_late_return_notification(borrow, gecikme_gunu)
        except Exception as e:
            print(f"[BorrowService] E-posta gönderme hatası (devam ediliyor): {str(e)}")
        
        return {
            'success': True,
            'message': 'Kitap iade edildi',
            'borrow': borrow.to_dict(include_book=True)
        }
    
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
        """Geç iade edilen kitapları kontrol et ve güncelle"""
        overdue = BorrowRepository.find_overdue()
        
        for borrow in overdue:
            if borrow.Durum == 'Aktif':
                borrow.Durum = 'Gecikmis'
                BorrowRepository.update(borrow)
                # E-posta bildirimi (hata olsa bile devam et)
                try:
                    gecikme_gunu = (datetime.utcnow() - borrow.BeklenenIadeTarihi).days
                    EmailService.send_overdue_notification(borrow, gecikme_gunu)
                except Exception as e:
                    print(f"[BorrowService] E-posta gönderme hatası (devam ediliyor): {str(e)}")
        
        return {
            'success': True,
            'overdue_count': len(overdue),
            'overdue_borrows': [b.to_dict(include_book=True, include_user=True) for b in overdue]
        }

