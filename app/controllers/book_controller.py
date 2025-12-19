from flask import Blueprint, request, jsonify
from app.services.book_service import BookService
from flask_jwt_extended import jwt_required, get_jwt

book_bp = Blueprint('book', __name__)

@book_bp.route('', methods=['GET'])
def get_books():
    """Tüm kitapları listele veya arama yap"""
    try:
        title = request.args.get('title')
        category_id = request.args.get('category_id', type=int)
        available_only = request.args.get('available_only', 'false').lower() == 'true'
        include_authors = request.args.get('include_authors', 'true').lower() == 'true'
        
        if title or category_id or available_only:
            books = BookService.search(title=title, category_id=category_id, available_only=available_only)
        else:
            books = BookService.get_all(include_authors=include_authors)
        
        return jsonify({'success': True, 'books': books, 'count': len(books)}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Kitap detayını getir"""
    try:
        book = BookService.get_by_id(book_id, include_authors=True)
        
        if book:
            return jsonify({'success': True, 'book': book}), 200
        else:
            return jsonify({'success': False, 'message': 'Kitap bulunamadı'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@book_bp.route('', methods=['POST'])
@jwt_required()
def create_book():
    """Yeni kitap ekle (Admin only)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'Admin':
            return jsonify({'success': False, 'message': 'Yetkisiz erişim'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Veri gerekli'}), 400
        
        result = BookService.create(data)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@book_bp.route('/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    """Kitap güncelle (Admin only)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'Admin':
            return jsonify({'success': False, 'message': 'Yetkisiz erişim'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Veri gerekli'}), 400
        
        result = BookService.update(book_id, data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@book_bp.route('/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    """Kitap sil (Admin only)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'Admin':
            return jsonify({'success': False, 'message': 'Yetkisiz erişim'}), 403
        
        result = BookService.delete(book_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

