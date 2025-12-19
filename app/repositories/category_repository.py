from app import db
from app.models.category import Category
from typing import Optional, List

class CategoryRepository:
    
    @staticmethod
    def find_by_id(category_id: int) -> Optional[Category]:
        return Category.query.get(category_id)
    
    @staticmethod
    def find_all() -> List[Category]:
        return Category.query.all()
    
    @staticmethod
    def find_by_name(name: str) -> Optional[Category]:
        return Category.query.filter_by(KategoriAdi=name).first()
    
    @staticmethod
    def create(category: Category) -> Category:
        db.session.add(category)
        db.session.commit()
        db.session.refresh(category)
        return category
    
    @staticmethod
    def update(category: Category) -> Category:
        db.session.commit()
        db.session.refresh(category)
        return category
    
    @staticmethod
    def delete(category_id: int) -> bool:
        category = CategoryRepository.find_by_id(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return True
        return False

