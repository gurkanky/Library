from app import db
from datetime import datetime
import bcrypt

class User(db.Model):
    __tablename__ = 'Kullanıcılar'
    
    KullaniciID = db.Column(db.Integer, primary_key=True)
    Ad = db.Column(db.String(50), nullable=False)
    Soyad = db.Column(db.String(50), nullable=False)
    EPosta = db.Column(db.String(100), nullable=False, unique=True)
    Sifre = db.Column(db.String(255), nullable=False)
    Rol = db.Column(db.String(20), nullable=False)
    Telefon = db.Column(db.String(20))
    Adres = db.Column(db.String(500))
    Aktif = db.Column(db.Boolean, default=True)
    OlusturmaTarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    borrows = db.relationship('Borrow', backref='user', lazy=True, cascade='all, delete-orphan')
    penalties = db.relationship('Penalty', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, ad, soyad, eposta, sifre, rol='Uye', telefon=None, adres=None):
        self.Ad = ad
        self.Soyad = soyad
        self.EPosta = eposta
        self.Sifre = self.hash_password(sifre)
        self.Rol = rol
        self.Telefon = telefon
        self.Adres = adres
    
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.Sifre.encode('utf-8'))
    
    def to_dict(self):
        return {
            'kullaniciID': self.KullaniciID,
            'ad': self.Ad,
            'soyad': self.Soyad,
            'eposta': self.EPosta,
            'rol': self.Rol,
            'telefon': self.Telefon,
            'adres': self.Adres,
            'aktif': bool(self.Aktif),
            'olusturmaTarihi': self.OlusturmaTarihi.isoformat() if self.OlusturmaTarihi else None
        }
    
    def __repr__(self):
        return f'<User {self.Ad} {self.Soyad} ({self.Rol})>'

