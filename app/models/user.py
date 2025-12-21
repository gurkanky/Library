from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'Kullanıcılar'

    KullaniciID = db.Column(db.Integer, primary_key=True)
    Ad = db.Column(db.String(50), nullable=False)
    Soyad = db.Column(db.String(50), nullable=False)
    EPosta = db.Column(db.String(100), nullable=False, unique=True)
    Sifre = db.Column(db.String(255), nullable=False)
    Rol = db.Column(db.String(20), nullable=False, default='Uye')
    Telefon = db.Column(db.String(20))
    Adres = db.Column(db.String(500))
    Aktif = db.Column(db.Boolean, default=True)
    OlusturmaTarihi = db.Column(db.DateTime, default=datetime.utcnow)

    # İlişkiler
    borrows = db.relationship('Borrow', backref='user', lazy=True, cascade='all, delete-orphan')
    penalties = db.relationship('Penalty', backref='user', lazy=True, cascade='all, delete-orphan')
    # Favoriler ilişkisi eklendi
    favorites = db.relationship('Favorite', backref='user', lazy=True, cascade='all, delete-orphan')

    def __init__(self, ad, soyad, eposta, sifre, rol='Uye', telefon=None, adres=None):
        self.Ad = ad
        self.Soyad = soyad
        self.EPosta = eposta
        self.set_password(sifre)  # Şifreyi güvenli hale getir
        self.Rol = rol
        self.Telefon = telefon
        self.Adres = adres
        self.Aktif = True
        self.OlusturmaTarihi = datetime.utcnow()

    def set_password(self, password):
        """Şifreyi güvenli bir hash formatına dönüştürür."""
        self.Sifre = generate_password_hash(password)

    def check_password(self, password):
        """Girilen şifrenin doğruluğunu kontrol eder."""
        # Eğer veritabanındaki şifre hash'lenmemişse (eski kayıtlar için)
        if not self.Sifre.startswith('pbkdf2:') and not self.Sifre.startswith('scrypt:'):
            if self.Sifre == password:
                self.set_password(password) # Güncelle
                db.session.commit()
                return True
            return False

        return check_password_hash(self.Sifre, password)

    def to_dict(self):
        return {
            'kullaniciID': self.KullaniciID,
            'ad': self.Ad,
            'soyad': self.Soyad,
            'eposta': self.EPosta,
            'rol': self.Rol,
            'telefon': self.Telefon,
            'adres': self.Adres,
            'aktif': self.Aktif,
            'olusturmaTarihi': self.OlusturmaTarihi.isoformat() if self.OlusturmaTarihi else None
        }

    def __repr__(self):
        return f'<User {self.Ad} {self.Soyad}>'