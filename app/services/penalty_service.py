from app.repositories.penalty_repository import PenaltyRepository
from app.repositories.user_repository import UserRepository
from typing import List, Dict

class PenaltyService:
    
    @staticmethod
    def get_user_penalties(user_id: int) -> List[Dict]:
        penalties = PenaltyRepository.find_by_user(user_id)
        return [penalty.to_dict(include_borrow=True) for penalty in penalties]
    
    @staticmethod
    def get_pending_penalties(user_id: int) -> List[Dict]:
        penalties = PenaltyRepository.find_pending_by_user(user_id)
        return [penalty.to_dict(include_borrow=True) for penalty in penalties]
    
    @staticmethod
    def get_total_debt(user_id: int) -> Dict:
        penalties = PenaltyRepository.find_pending_by_user(user_id)
        total = sum(float(p.CezaMiktari) for p in penalties)
        
        return {
            'kullaniciID': user_id,
            'toplamBorc': total,
            'cezaSayisi': len(penalties)
        }
    
    @staticmethod
    def pay_penalty(penalty_id: int, user_id: int = None) -> Dict:
        penalty = PenaltyRepository.find_by_id(penalty_id)
        if not penalty:
            return {'success': False, 'message': 'Ceza bulunamadı'}
        
        # Yetki kontrolü
        if user_id and penalty.KullaniciID != user_id:
            return {'success': False, 'message': 'Bu işlemi yapmaya yetkiniz yok'}
        
        if penalty.Durum == 'Odendi':
            return {'success': False, 'message': 'Ceza zaten ödenmiş'}
        
        from datetime import datetime
        penalty.Durum = 'Odendi'
        penalty.OdemeTarihi = datetime.utcnow()
        penalty = PenaltyRepository.update(penalty)
        
        return {
            'success': True,
            'message': 'Ceza ödendi',
            'penalty': penalty.to_dict(include_borrow=True)
        }
    
    @staticmethod
    def get_all_penalties() -> List[Dict]:
        penalties = PenaltyRepository.find_all()
        return [penalty.to_dict(include_borrow=True) for penalty in penalties]

