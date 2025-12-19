from app import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'Kategoriler'
    
    KategoriID = db.Column(db.Integer, primary_key=True)
    KategoriAdi = db.Column(db.String(100), nullable=False, unique=True)
    Aciklama = db.Column(db.String(500))
    OlusturmaTarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    books = db.relationship('Book', backref='category', lazy=True)
    
    def to_dict(self):
        return {
            'kategoriID': self.KategoriID,
            'kategoriAdi': self.KategoriAdi,
            'aciklama': self.Aciklama,
            'olusturmaTarihi': self.OlusturmaTarihi.isoformat() if self.OlusturmaTarihi else None
        }
    
    def __repr__(self):
        return f'<Category {self.KategoriAdi}>'

