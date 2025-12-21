from app import db
from datetime import datetime


class Review(db.Model):
    __tablename__ = 'KitapYorumlari'

    YorumID = db.Column(db.Integer, primary_key=True)
    KullaniciID = db.Column(db.Integer, db.ForeignKey('Kullanıcılar.KullaniciID', ondelete='CASCADE'), nullable=False)
    KitapID = db.Column(db.Integer, db.ForeignKey('Kitaplar.KitapID', ondelete='CASCADE'), nullable=False)
    Puan = db.Column(db.Integer, nullable=False)
    Yorum = db.Column(db.String(1000))
    OlusturmaTarihi = db.Column(db.DateTime, default=datetime.utcnow)

    # İlişkiler
    user = db.relationship('User', backref='reviews', lazy=True)

    def to_dict(self, include_user=False):
        data = {
            'yorumID': self.YorumID,
            'kullaniciID': self.KullaniciID,
            'kitapID': self.KitapID,
            'puan': self.Puan,
            'yorum': self.Yorum,
            'tarih': self.OlusturmaTarihi.strftime('%d.%m.%Y %H:%M')
        }

        if include_user and self.user:
            data['kullaniciAdi'] = f"{self.user.Ad} {self.user.Soyad}"

        return data