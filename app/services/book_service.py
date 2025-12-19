from app.repositories.book_repository import BookRepository
from app.repositories.category_repository import CategoryRepository
from app.models.book import Book
from typing import List, Optional, Dict

class BookService:
    
    @staticmethod
    def get_all(include_authors: bool = False) -> List[Dict]:
        books = BookRepository.find_all()
        return [book.to_dict(include_authors=include_authors) for book in books]
    
    @staticmethod
    def get_by_id(book_id: int, include_authors: bool = True) -> Optional[Dict]:
        book = BookRepository.find_by_id(book_id)
        if book:
            return book.to_dict(include_authors=include_authors)
        return None
    
    @staticmethod
    def search(title: str = None, category_id: int = None, available_only: bool = False) -> List[Dict]:
        if title:
            books = BookRepository.find_by_title(title)
        elif category_id:
            books = BookRepository.find_by_category(category_id)
        elif available_only:
            books = BookRepository.find_available()
        else:
            books = BookRepository.find_all()
        
        if available_only and not title and not category_id:
            books = [b for b in books if b.MevcutKopyaSayisi > 0]
        elif available_only:
            books = [b for b in books if b.MevcutKopyaSayisi > 0]
        
        return [book.to_dict(include_authors=True) for book in books]
    
    @staticmethod
    def create(book_data: Dict) -> Dict:
        # Kategori kontrolü
        if book_data.get('kategoriID'):
            category = CategoryRepository.find_by_id(book_data['kategoriID'])
            if not category:
                return {'success': False, 'message': 'Kategori bulunamadı'}
        
        book = Book(
            Baslik=book_data['baslik'],
            ISBN=book_data.get('isbn'),
            YayinYili=book_data.get('yayinYili'),
            SayfaSayisi=book_data.get('sayfaSayisi'),
            MevcutKopyaSayisi=book_data.get('mevcutKopyaSayisi', book_data.get('toplamKopyaSayisi', 0)),
            ToplamKopyaSayisi=book_data.get('toplamKopyaSayisi', book_data.get('mevcutKopyaSayisi', 0)),
            KategoriID=book_data.get('kategoriID'),
            YayinEvi=book_data.get('yayinEvi'),
            Dil=book_data.get('dil', 'Türkçe'),
            Aciklama=book_data.get('aciklama')
        )
        
        book = BookRepository.create(book)
        
        # Yazarları ekle
        if book_data.get('yazarIDler'):
            for yazar_id in book_data['yazarIDler']:
                BookRepository.add_author(book.KitapID, yazar_id)
        
        return {'success': True, 'book': book.to_dict(include_authors=True)}
    
    @staticmethod
    def update(book_id: int, book_data: Dict) -> Dict:
        book = BookRepository.find_by_id(book_id)
        if not book:
            return {'success': False, 'message': 'Kitap bulunamadı'}
        
        # Güncelleme
        if 'baslik' in book_data:
            book.Baslik = book_data['baslik']
        if 'isbn' in book_data:
            book.ISBN = book_data['isbn']
        if 'yayinYili' in book_data:
            book.YayinYili = book_data['yayinYili']
        if 'sayfaSayisi' in book_data:
            book.SayfaSayisi = book_data['sayfaSayisi']
        if 'toplamKopyaSayisi' in book_data:
            fark = book_data['toplamKopyaSayisi'] - book.ToplamKopyaSayisi
            book.ToplamKopyaSayisi = book_data['toplamKopyaSayisi']
            book.MevcutKopyaSayisi += fark
        if 'kategoriID' in book_data:
            book.KategoriID = book_data['kategoriID']
        if 'yayinEvi' in book_data:
            book.YayinEvi = book_data['yayinEvi']
        if 'dil' in book_data:
            book.Dil = book_data['dil']
        if 'aciklama' in book_data:
            book.Aciklama = book_data['aciklama']
        
        book = BookRepository.update(book)
        
        # Yazarları güncelle
        if 'yazarIDler' in book_data:
            # Mevcut yazarları sil
            for ba in book.authors:
                BookRepository.remove_author(book.KitapID, ba.YazarID)
            # Yeni yazarları ekle
            for yazar_id in book_data['yazarIDler']:
                BookRepository.add_author(book.KitapID, yazar_id)
        
        return {'success': True, 'book': book.to_dict(include_authors=True)}
    
    @staticmethod
    def delete(book_id: int) -> Dict:
        success = BookRepository.delete(book_id)
        if success:
            return {'success': True, 'message': 'Kitap silindi'}
        return {'success': False, 'message': 'Kitap bulunamadı'}

