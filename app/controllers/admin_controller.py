from flask import Blueprint, request, jsonify
from app.repositories.user_repository import UserRepository
from app.services.penalty_service import PenaltyService
from flask_jwt_extended import jwt_required, get_jwt

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Admin yetkisi kontrolü decorator"""
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('rol') != 'Admin':
            return jsonify({'success': False, 'message': 'Yetkisiz erişim'}), 403
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    """Tüm kullanıcıları listele"""
    try:
        users = UserRepository.find_all()
        return jsonify({
            'success': True,
            'users': [user.to_dict() for user in users],
            'count': len(users)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    """Kullanıcı güncelle"""
    try:
        user = UserRepository.find_by_id(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'Kullanıcı bulunamadı'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Veri gerekli'}), 400
        
        if 'ad' in data:
            user.Ad = data['ad']
        if 'soyad' in data:
            user.Soyad = data['soyad']
        if 'telefon' in data:
            user.Telefon = data['telefon']
        if 'adres' in data:
            user.Adres = data['adres']
        if 'aktif' in data:
            user.Aktif = data['aktif']
        
        user = UserRepository.update(user)
        
        return jsonify({'success': True, 'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    """Kullanıcı sil"""
    try:
        success = UserRepository.delete(user_id)
        
        if success:
            return jsonify({'success': True, 'message': 'Kullanıcı silindi'}), 200
        else:
            return jsonify({'success': False, 'message': 'Kullanıcı bulunamadı'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/penalties', methods=['GET'])
@jwt_required()
@admin_required
def get_all_penalties():
    """Tüm cezaları listele"""
    try:
        penalties = PenaltyService.get_all_penalties()
        
        return jsonify({
            'success': True,
            'penalties': penalties,
            'count': len(penalties)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/statistics', methods=['GET'])
@jwt_required()
@admin_required
def get_statistics():
    """İstatistikleri getir"""
    try:
        from app.repositories.book_repository import BookRepository
        from app.repositories.borrow_repository import BorrowRepository
        from app.repositories.category_repository import CategoryRepository
        
        total_books = len(BookRepository.find_all())
        total_users = len(UserRepository.find_all())
        total_borrows = len(BorrowRepository.find_all())
        active_borrows = len([b for b in BorrowRepository.find_all() if b.Durum == 'Aktif'])
        overdue_borrows = len(BorrowRepository.find_overdue())
        total_categories = len(CategoryRepository.find_all())
        
        return jsonify({
            'success': True,
            'statistics': {
                'totalBooks': total_books,
                'totalUsers': total_users,
                'totalBorrows': total_borrows,
                'activeBorrows': active_borrows,
                'overdueBorrows': overdue_borrows,
                'totalCategories': total_categories
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

