from app import db
from datetime import datetime

class Penalty(db.Model):
    __tablename__ = 'Cezalar'
    
    CezaID = db.Column(db.Integer, primary_key=True)
    KullaniciID = db.Column(db.Integer, db.ForeignKey('Kullanıcılar.KullaniciID', ondelete='CASCADE'), nullable=False)
    OduncID = db.Column(db.Integer, db.ForeignKey('OduncIslemleri.OduncID', ondelete='SET NULL'))
    CezaMiktari = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    CezaNedeni = db.Column(db.String(200))
    Durum = db.Column(db.String(20), default='Beklemede')
    OlusturmaTarihi = db.Column(db.DateTime, default=datetime.utcnow)
    OdemeTarihi = db.Column(db.DateTime)
    
    def to_dict(self, include_borrow=False):
        data = {
            'cezaID': self.CezaID,
            'kullaniciID': self.KullaniciID,
            'oduncID': self.OduncID,
            'cezaMiktari': float(self.CezaMiktari),
            'cezaNedeni': self.CezaNedeni,
            'durum': self.Durum,
            'olusturmaTarihi': self.OlusturmaTarihi.isoformat() if self.OlusturmaTarihi else None,
            'odemeTarihi': self.OdemeTarihi.isoformat() if self.OdemeTarihi else None
        }
        
        if include_borrow and self.borrow:
            data['odunc'] = self.borrow.to_dict(include_book=True)
        
        return data
    
    def __repr__(self):
        return f'<Penalty ID={self.CezaID} Miktar={self.CezaMiktari}>'

