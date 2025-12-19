from flask import Blueprint, request, jsonify
from app.services.author_service import AuthorService
from flask_jwt_extended import jwt_required, get_jwt

author_bp = Blueprint('author', __name__)

@author_bp.route('', methods=['GET'])
def get_authors():
    """Tüm yazarları listele veya arama yap"""
    try:
        ad = request.args.get('ad')
        soyad = request.args.get('soyad')
        
        if ad:
            authors = AuthorService.search(ad, soyad)
        else:
            authors = AuthorService.get_all()
        
        return jsonify({'success': True, 'authors': authors, 'count': len(authors)}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@author_bp.route('/<int:author_id>', methods=['GET'])
def get_author(author_id):
    """Yazar detayını getir"""
    try:
        author = AuthorService.get_by_id(author_id)
        
        if author:
            return jsonify({'success': True, 'author': author}), 200
        else:
            return jsonify({'success': False, 'message': 'Yazar bulunamadı'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@author_bp.route('', methods=['POST'])
@jwt_required()
def create_author():
    """Yeni yazar ekle (Admin only)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'Admin':
            return jsonify({'success': False, 'message': 'Yetkisiz erişim'}), 403
        
        data = request.get_json()
        if not data or 'ad' not in data or 'soyad' not in data:
            return jsonify({'success': False, 'message': 'Ad ve soyad gerekli'}), 400
        
        result = AuthorService.create(data)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@author_bp.route('/<int:author_id>', methods=['PUT'])
@jwt_required()
def update_author(author_id):
    """Yazar güncelle (Admin only)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'Admin':
            return jsonify({'success': False, 'message': 'Yetkisiz erişim'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Veri gerekli'}), 400
        
        result = AuthorService.update(author_id, data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@author_bp.route('/<int:author_id>', methods=['DELETE'])
@jwt_required()
def delete_author(author_id):
    """Yazar sil (Admin only)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'Admin':
            return jsonify({'success': False, 'message': 'Yetkisiz erişim'}), 403
        
        result = AuthorService.delete(author_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

