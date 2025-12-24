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

    # İLİŞKİLER
    book = db.relationship('Book', backref='borrows', lazy=True)
    penalty = db.relationship('Penalty', backref='borrow', uselist=False, lazy=True)

    def __init__(self, kullanici_id, kitap_id, odunc_gun_sayisi=21):
        self.KullaniciID = kullanici_id
        self.KitapID = kitap_id
        self.OduncAlmaTarihi = datetime.utcnow()
        # Varsayılan hesaplama (Servis katmanında bu değer eziliyor olabilir)
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

        # --- GECİKME HESAPLAMA DÜZELTMESİ ---
        # Test ortamında dakika bazlı gecikmeleri de yakalamak için mantığı güncelliyoruz.

        gecikme = 0
        if self.Durum == 'Aktif' and datetime.utcnow() > self.BeklenenIadeTarihi:
            diff = datetime.utcnow() - self.BeklenenIadeTarihi
            # Eğer fark pozitifse ama 1 günden azsa (örn: 5 dakika), days 0 döner.
            # Bu durumda en az 1 yazalım ki arayüzde 'Gecikme' olarak görünsün.
            gecikme = diff.days if diff.days > 0 else 1

        elif self.Durum == 'IadeEdildi' and self.IadeTarihi and self.IadeTarihi > self.BeklenenIadeTarihi:
            diff = self.IadeTarihi - self.BeklenenIadeTarihi
            gecikme = diff.days if diff.days > 0 else 1

        data['gecikmeGunu'] = gecikme
        # ------------------------------------

        return data