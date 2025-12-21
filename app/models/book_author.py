from app import db


class BookAuthor(db.Model):
    __tablename__ = 'KitapYazarlar'

    KitapYazarID = db.Column(db.Integer, primary_key=True)
    # ondelete='CASCADE' veritabanı bütünlüğü için önemli
    KitapID = db.Column(db.Integer, db.ForeignKey('Kitaplar.KitapID', ondelete='CASCADE'), nullable=False)
    YazarID = db.Column(db.Integer, db.ForeignKey('Yazarlar.YazarID', ondelete='CASCADE'), nullable=False)

    # --- İLİŞKİLER BURADA TANIMLANIYOR ---
    # 1. Book ilişkisi: Book modeline 'authors' (backref) ekler
    book = db.relationship('Book', backref=db.backref('authors', lazy=True, cascade='all, delete-orphan'))

    # 2. Author ilişkisi: Author modeline 'books' (backref) ekler
    author = db.relationship('Author', backref=db.backref('books', lazy=True, cascade='all, delete-orphan'))

    __table_args__ = (db.UniqueConstraint('KitapID', 'YazarID', name='uq_kitap_yazar'),)

    def to_dict(self):
        return {
            'kitapYazarID': self.KitapYazarID,
            'kitapID': self.KitapID,
            'yazarID': self.YazarID,
            # Opsiyonel: Yazar/Kitap isimlerini de döndürebilirsiniz
            'yazarAd': self.author.Ad if self.author else None,
            'yazarSoyad': self.author.Soyad if self.author else None
        }

    def __repr__(self):
        return f'<BookAuthor KitapID={self.KitapID} YazarID={self.YazarID}>'