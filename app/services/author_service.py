from app.repositories.author_repository import AuthorRepository
from app.models.author import Author
from typing import List, Dict, Optional

class AuthorService:
    
    @staticmethod
    def get_all() -> List[Dict]:
        authors = AuthorRepository.find_all()
        return [author.to_dict() for author in authors]
    
    @staticmethod
    def get_by_id(author_id: int) -> Optional[Dict]:
        author = AuthorRepository.find_by_id(author_id)
        if author:
            return author.to_dict()
        return None
    
    @staticmethod
    def search(ad: str, soyad: str = None) -> List[Dict]:
        authors = AuthorRepository.find_by_name(ad, soyad)
        return [author.to_dict() for author in authors]
    
    @staticmethod
    def create(author_data: Dict) -> Dict:
        author = Author(
            Ad=author_data['ad'],
            Soyad=author_data['soyad'],
            DogumTarihi=author_data.get('dogumTarihi'),
            Ulke=author_data.get('ulke'),
            Biyografi=author_data.get('biyografi')
        )
        author = AuthorRepository.create(author)
        
        return {'success': True, 'author': author.to_dict()}
    
    @staticmethod
    def update(author_id: int, author_data: Dict) -> Dict:
        author = AuthorRepository.find_by_id(author_id)
        if not author:
            return {'success': False, 'message': 'Yazar bulunamadı'}
        
        if 'ad' in author_data:
            author.Ad = author_data['ad']
        if 'soyad' in author_data:
            author.Soyad = author_data['soyad']
        if 'dogumTarihi' in author_data:
            author.DogumTarihi = author_data['dogumTarihi']
        if 'ulke' in author_data:
            author.Ulke = author_data['ulke']
        if 'biyografi' in author_data:
            author.Biyografi = author_data['biyografi']
        
        author = AuthorRepository.update(author)
        return {'success': True, 'author': author.to_dict()}
    
    @staticmethod
    def delete(author_id: int) -> Dict:
        success = AuthorRepository.delete(author_id)
        if success:
            return {'success': True, 'message': 'Yazar silindi'}
        return {'success': False, 'message': 'Yazar bulunamadı'}

