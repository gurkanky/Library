from app import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'Kitaplar'
    
    KitapID = db.Column(db.Integer, primary_key=True)
    Baslik = db.Column(db.String(200), nullable=False)
    ISBN = db.Column(db.String(20), unique=True)
    YayinYili = db.Column(db.Integer)
    SayfaSayisi = db.Column(db.Integer)
    MevcutKopyaSayisi = db.Column(db.Integer, default=0)
    ToplamKopyaSayisi = db.Column(db.Integer, default=0)
    KategoriID = db.Column(db.Integer, db.ForeignKey('Kategoriler.KategoriID', ondelete='SET NULL'))
    YayinEvi = db.Column(db.String(100))
    Dil = db.Column(db.String(20), default='Türkçe')
    Aciklama = db.Column(db.String(1000))
    OlusturmaTarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    authors = db.relationship('BookAuthor', backref='book', lazy=True, cascade='all, delete-orphan')
    borrows = db.relationship('Borrow', backref='book', lazy=True)
    
    def to_dict(self, include_authors=False):
        data = {
            'kitapID': self.KitapID,
            'baslik': self.Baslik,
            'isbn': self.ISBN,
            'yayinYili': self.YayinYili,
            'sayfaSayisi': self.SayfaSayisi,
            'mevcutKopyaSayisi': self.MevcutKopyaSayisi,
            'toplamKopyaSayisi': self.ToplamKopyaSayisi,
            'kategoriID': self.KategoriID,
            'kategoriAdi': self.category.KategoriAdi if self.category else None,
            'yayinEvi': self.YayinEvi,
            'dil': self.Dil,
            'aciklama': self.Aciklama,
            'olusturmaTarihi': self.OlusturmaTarihi.isoformat() if self.OlusturmaTarihi else None
        }
        
        if include_authors:
            data['yazarlar'] = [
                {'yazarID': ba.author.YazarID, 'ad': ba.author.Ad, 'soyad': ba.author.Soyad}
                for ba in self.authors
            ]
        
        return data
    
    def __repr__(self):
        return f'<Book {self.Baslik}>'

