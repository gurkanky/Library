from app import db
from datetime import datetime

class Author(db.Model):
    __tablename__ = 'Yazarlar'
    
    YazarID = db.Column(db.Integer, primary_key=True)
    Ad = db.Column(db.String(50), nullable=False)
    Soyad = db.Column(db.String(50), nullable=False)
    DogumTarihi = db.Column(db.Date)
    Ulke = db.Column(db.String(50))
    Biyografi = db.Column(db.String(1000))
    OlusturmaTarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    books = db.relationship('BookAuthor', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'yazarID': self.YazarID,
            'ad': self.Ad,
            'soyad': self.Soyad,
            'dogumTarihi': self.DogumTarihi.isoformat() if self.DogumTarihi else None,
            'ulke': self.Ulke,
            'biyografi': self.Biyografi,
            'olusturmaTarihi': self.OlusturmaTarihi.isoformat() if self.OlusturmaTarihi else None
        }
    
    def __repr__(self):
        return f'<Author {self.Ad} {self.Soyad}>'

