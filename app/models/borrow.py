from app import db
from datetime import datetime, timedelta


class Borrow(db.Model):
    __tablename__ = 'OduncIslemleri'

    OduncID = db.Column(db.Integer, primary_key=True)
    KullaniciID = db.Column(db.Integer, db.ForeignKey('Kullanıcılar.KullaniciID', ondelete='CASCADE'), nullable=False)
    KitapID = db.Column(db.Integer, db.ForeignKey('Kitaplar.KitapID', ondelete='CASCADE'), nullable=False)

    OduncAlmaTarihi = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    IadeTarihi = db.Column(db.DateTime)
    BeklenenIadeTarihi = db.Column(db.DateTime, nullable=False)
    Durum = db.Column(db.String(20), default='Aktif')
    Notlar = db.Column(db.String(500))

    # İLİŞKİLER (Burada tanımlı)
    # Book modeline 'borrows' adında bir özellik ekler
    book = db.relationship('Book', backref='borrows', lazy=True)
    penalty = db.relationship('Penalty', backref='borrow', uselist=False, lazy=True)

    def __init__(self, kullanici_id, kitap_id, odunc_gun_sayisi=21):
        self.KullaniciID = kullanici_id
        self.KitapID = kitap_id
        self.OduncAlmaTarihi = datetime.utcnow()
        self.BeklenenIadeTarihi = datetime.utcnow() + timedelta(days=odunc_gun_sayisi)
        self.Durum = 'Aktif'

    def to_dict(self, include_book=False, include_user=False):
        data = {
            'oduncID': self.OduncID,
            'kullaniciID': self.KullaniciID,
            'kitapID': self.KitapID,
            'oduncAlmaTarihi': self.OduncAlmaTarihi.isoformat() if self.OduncAlmaTarihi else None,
            'iadeTarihi': self.IadeTarihi.isoformat() if self.IadeTarihi else None,
            'beklenenIadeTarihi': self.BeklenenIadeTarihi.isoformat() if self.BeklenenIadeTarihi else None,
            'durum': self.Durum,
            'notlar': self.Notlar
        }

        if include_book:
            if self.book:
                data['kitap'] = self.book.to_dict()
            else:
                data['kitap'] = {'baslik': 'Bilinmeyen Kitap', 'kitapID': self.KitapID}

        # Gecikme hesaplama
        if self.Durum == 'Aktif' and datetime.utcnow() > self.BeklenenIadeTarihi:
            data['gecikmeGunu'] = (datetime.utcnow() - self.BeklenenIadeTarihi).days
        elif self.Durum == 'IadeEdildi' and self.IadeTarihi and self.IadeTarihi > self.BeklenenIadeTarihi:
            data['gecikmeGunu'] = (self.IadeTarihi - self.BeklenenIadeTarihi).days
        else:
            data['gecikmeGunu'] = 0

        return data