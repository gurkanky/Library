from app import db
from datetime import datetime

class Reservation(db.Model):
    __tablename__ = 'Rezervasyonlar'

    RezervasyonID = db.Column(db.Integer, primary_key=True)
    KullaniciID = db.Column(db.Integer, db.ForeignKey('Kullanıcılar.KullaniciID', ondelete='CASCADE'), nullable=False)
    KitapID = db.Column(db.Integer, db.ForeignKey('Kitaplar.KitapID', ondelete='CASCADE'), nullable=False)
    RezervasyonTarihi = db.Column(db.DateTime, default=datetime.utcnow)
    Durum = db.Column(db.String(20), default='Aktif')  # Aktif, Tamamlandi, Iptal
    Notlar = db.Column(db.String(500))

    # İlişkiler (Optional: join sorguları için)
    user = db.relationship('User', backref='reservations', lazy=True)
    book = db.relationship('Book', backref='reservations', lazy=True)

    def to_dict(self, include_book=False):
        data = {
            'rezervasyonID': self.RezervasyonID,
            'kullaniciID': self.KullaniciID,
            'kitapID': self.KitapID,
            'rezervasyonTarihi': self.RezervasyonTarihi.isoformat() if self.RezervasyonTarihi else None,
            'durum': self.Durum
        }
        if include_book and self.book:
            data['kitap'] = {
                'baslik': self.book.Baslik,
                'isbn': self.book.ISBN
            }
        return data