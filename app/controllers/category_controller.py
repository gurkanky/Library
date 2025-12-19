from flask import Blueprint, request, jsonify
from app.services.category_service import CategoryService
from flask_jwt_extended import jwt_required, get_jwt

category_bp = Blueprint('category', __name__)

@category_bp.route('', methods=['GET'])
def get_categories():
    """Tüm kategorileri listele"""
    try:
        categories = CategoryService.get_all()
        return jsonify({'success': True, 'categories': categories, 'count': len(categories)}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Kategori detayını getir"""
    try:
        category = CategoryService.get_by_id(category_id)
        
        if category:
            return jsonify({'success': True, 'category': category}), 200
        else:
            return jsonify({'success': False, 'message': 'Kategori bulunamadı'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@category_bp.route('', methods=['POST'])
@jwt_required()
def create_category():
    """Yeni kategori ekle (Admin only)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'Admin':
            return jsonify({'success': False, 'message': 'Yetkisiz erişim'}), 403
        
        data = request.get_json()
        if not data or 'kategoriAdi' not in data:
            return jsonify({'success': False, 'message': 'Kategori adı gerekli'}), 400
        
        result = CategoryService.create(data)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@category_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    """Kategori güncelle (Admin only)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'Admin':
            return jsonify({'success': False, 'message': 'Yetkisiz erişim'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Veri gerekli'}), 400
        
        result = CategoryService.update(category_id, data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@category_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    """Kategori sil (Admin only)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'Admin':
            return jsonify({'success': False, 'message': 'Yetkisiz erişim'}), 403
        
        result = CategoryService.delete(category_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

