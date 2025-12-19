from app.repositories.category_repository import CategoryRepository
from app.models.category import Category
from typing import List, Dict, Optional

class CategoryService:
    
    @staticmethod
    def get_all() -> List[Dict]:
        categories = CategoryRepository.find_all()
        return [category.to_dict() for category in categories]
    
    @staticmethod
    def get_by_id(category_id: int) -> Optional[Dict]:
        category = CategoryRepository.find_by_id(category_id)
        if category:
            return category.to_dict()
        return None
    
    @staticmethod
    def create(category_data: Dict) -> Dict:
        # İsim kontrolü
        existing = CategoryRepository.find_by_name(category_data['kategoriAdi'])
        if existing:
            return {'success': False, 'message': 'Bu kategori zaten mevcut'}
        
        category = Category(
            KategoriAdi=category_data['kategoriAdi'],
            Aciklama=category_data.get('aciklama')
        )
        category = CategoryRepository.create(category)
        
        return {'success': True, 'category': category.to_dict()}
    
    @staticmethod
    def update(category_id: int, category_data: Dict) -> Dict:
        category = CategoryRepository.find_by_id(category_id)
        if not category:
            return {'success': False, 'message': 'Kategori bulunamadı'}
        
        if 'kategoriAdi' in category_data:
            # İsim değişikliği kontrolü
            existing = CategoryRepository.find_by_name(category_data['kategoriAdi'])
            if existing and existing.KategoriID != category_id:
                return {'success': False, 'message': 'Bu kategori adı zaten kullanılıyor'}
            category.KategoriAdi = category_data['kategoriAdi']
        
        if 'aciklama' in category_data:
            category.Aciklama = category_data['aciklama']
        
        category = CategoryRepository.update(category)
        return {'success': True, 'category': category.to_dict()}
    
    @staticmethod
    def delete(category_id: int) -> Dict:
        success = CategoryRepository.delete(category_id)
        if success:
            return {'success': True, 'message': 'Kategori silindi'}
        return {'success': False, 'message': 'Kategori bulunamadı'}

