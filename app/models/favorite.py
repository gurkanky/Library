from app import db
from datetime import datetime

class Favorite(db.Model):
    __tablename__ = 'Favoriler'

    FavoriID = db.Column(db.Integer, primary_key=True)
    KullaniciID = db.Column(db.Integer, db.ForeignKey('Kullanıcılar.KullaniciID'), nullable=False)
    KitapID = db.Column(db.Integer, db.ForeignKey('Kitaplar.KitapID'), nullable=False)
    EklenmeTarihi = db.Column(db.DateTime, default=datetime.utcnow)

    # İlişkiler
    kitap = db.relationship('Book', backref='favorleyenler')

    def to_dict(self):
        return {
            'favoriID': self.FavoriID,
            'kitap': self.kitap.to_dict() if self.kitap else None,
            'eklenmeTarihi': self.EklenmeTarihi.isoformat()
        }