from app import db

class BookAuthor(db.Model):
    __tablename__ = 'KitapYazarlar'
    
    KitapYazarID = db.Column(db.Integer, primary_key=True)
    KitapID = db.Column(db.Integer, db.ForeignKey('Kitaplar.KitapID', ondelete='CASCADE'), nullable=False)
    YazarID = db.Column(db.Integer, db.ForeignKey('Yazarlar.YazarID', ondelete='CASCADE'), nullable=False)
    
    __table_args__ = (db.UniqueConstraint('KitapID', 'YazarID', name='uq_kitap_yazar'),)
    
    def to_dict(self):
        return {
            'kitapYazarID': self.KitapYazarID,
            'kitapID': self.KitapID,
            'yazarID': self.YazarID
        }
    
    def __repr__(self):
        return f'<BookAuthor KitapID={self.KitapID} YazarID={self.YazarID}>'

