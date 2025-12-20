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
    
    # Relationships
    penalty = db.relationship('Penalty', backref='borrow', uselist=False, lazy=True)
    
    def __init__(self, kullanici_id, kitap_id, odunc_gun_sayisi=21):
        self.KullaniciID = kullanici_id
        self.KitapID = kitap_id
        self.OduncAlmaTarihi = datetime.utcnow()
        self.BeklenenIadeTarihi = datetime.utcnow() + timedelta(days=odunc_gun_sayisi)
        self.Durum = 'Aktif'
    
    def to_dict(self, include_book=False, include_user=False):
        try:
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
                try:
                    # Lazy loading ile book ilişkisini yükle
                    if self.book:
                        data['kitap'] = self.book.to_dict()
                    else:
                        data['kitap'] = {'baslik': 'Bilinmeyen Kitap', 'kitapID': self.KitapID}
                except Exception as e:
                    print(f"Error loading book for borrow {self.OduncID}: {str(e)}")
                    data['kitap'] = {'baslik': 'Bilinmeyen Kitap', 'kitapID': self.KitapID}
            
            if include_user:
                try:
                    if self.user:
                        data['kullanici'] = {
                            'ad': self.user.Ad,
                            'soyad': self.user.Soyad,
                            'eposta': self.user.EPosta
                        }
                except Exception as e:
                    print(f"Error loading user for borrow {self.OduncID}: {str(e)}")
            
            # Gecikme kontrolü
            try:
                if self.Durum == 'Aktif' and datetime.utcnow() > self.BeklenenIadeTarihi:
                    data['gecikmeGunu'] = (datetime.utcnow() - self.BeklenenIadeTarihi).days
                elif self.Durum == 'IadeEdildi' and self.IadeTarihi and self.IadeTarihi > self.BeklenenIadeTarihi:
                    data['gecikmeGunu'] = (self.IadeTarihi - self.BeklenenIadeTarihi).days
                else:
                    data['gecikmeGunu'] = 0
            except Exception as e:
                print(f"Error calculating delay for borrow {self.OduncID}: {str(e)}")
                data['gecikmeGunu'] = 0
            
            return data
        except Exception as e:
            print(f"Error in to_dict for borrow {self.OduncID}: {str(e)}")
            import traceback
            print(traceback.format_exc())
            # En azından temel bilgileri döndür
            return {
                'oduncID': getattr(self, 'OduncID', None),
                'kullaniciID': getattr(self, 'KullaniciID', None),
                'kitapID': getattr(self, 'KitapID', None),
                'durum': getattr(self, 'Durum', 'Bilinmiyor'),
                'kitap': {'baslik': 'Bilinmeyen Kitap'}
            }
    
    def __repr__(self):
        return f'<Borrow ID={self.OduncID} Durum={self.Durum}>'

