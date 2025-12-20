from app import db
from app.models.penalty import Penalty
from typing import Optional, List

class PenaltyRepository:
    
    @staticmethod
    def find_by_id(penalty_id: int) -> Optional[Penalty]:
        return Penalty.query.get(penalty_id)
    
    @staticmethod
    def find_by_user(user_id: int) -> List[Penalty]:
        return Penalty.query.filter_by(KullaniciID=user_id).all()
    
    @staticmethod
    def find_pending_by_user(user_id: int) -> List[Penalty]:
        return Penalty.query.filter_by(KullaniciID=user_id, Durum='Beklemede').all()
    
    @staticmethod
    def find_all() -> List[Penalty]:
        return Penalty.query.all()
    
    @staticmethod
    def create(penalty: Penalty) -> Penalty:
        db.session.add(penalty)
        db.session.commit()
        # commit() sonrası refresh() gerekmez, MSSQL IDENTITY için refresh() hata verebilir
        return penalty
    
    @staticmethod
    def update(penalty: Penalty) -> Penalty:
        db.session.commit()
        return penalty
    
    @staticmethod
    def delete(penalty_id: int) -> bool:
        penalty = PenaltyRepository.find_by_id(penalty_id)
        if penalty:
            db.session.delete(penalty)
            db.session.commit()
            return True
        return False

