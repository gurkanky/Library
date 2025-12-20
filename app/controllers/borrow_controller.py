from flask import Blueprint, request, jsonify
from app.services.borrow_service import BorrowService
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

borrow_bp = Blueprint('borrow', __name__)

@borrow_bp.route('', methods=['POST'])
@jwt_required()
def borrow_book():
    """Kitap ödünç al"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'kitapID' not in data:
            return jsonify({'success': False, 'message': 'Kitap ID gerekli'}), 400
        
        odunc_gun_sayisi = data.get('oduncGunSayisi', 21)
        
        result = BorrowService.borrow_book(
            user_id=user_id,
            book_id=data['kitapID'],
            odunc_gun_sayisi=odunc_gun_sayisi
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@borrow_bp.route('/<int:borrow_id>/return', methods=['POST'])
@jwt_required()
def return_book(borrow_id):
    """Kitap iade et"""
    try:
        user_id = get_jwt_identity()
        claims = get_jwt()
        
        # Admin tüm iadeleri yapabilir, kullanıcı sadece kendi iadelerini
        if claims.get('rol') == 'Admin':
            user_id = None
        
        result = BorrowService.return_book(borrow_id, user_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@borrow_bp.route('/my-books', methods=['GET'])
@jwt_required()
def get_my_borrows():
    """Kullanıcının ödünç aldığı kitapları listele"""
    try:
        # Debug: Authorization header'ı kontrol et
        auth_header = request.headers.get('Authorization', None)
        print(f"[DEBUG] Authorization Header: {auth_header}")
        
        user_id = get_jwt_identity()
        print(f"[DEBUG] User ID from token: {user_id}")
        
        borrows = BorrowService.get_user_borrows(user_id)
        
        return jsonify({'success': True, 'borrows': borrows, 'count': len(borrows)}), 200
        
    except Exception as e:
        import traceback
        print(f"Error in get_my_borrows: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'message': str(e)}), 500

@borrow_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_borrows():
    """Tüm ödünç işlemlerini listele (Admin only)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'Admin':
            return jsonify({'success': False, 'message': 'Yetkisiz erişim'}), 403
        
        borrows = BorrowService.get_all_borrows()
        
        return jsonify({'success': True, 'borrows': borrows, 'count': len(borrows)}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@borrow_bp.route('/overdue', methods=['GET'])
@jwt_required()
def get_overdue_borrows():
    """Geç iade edilen kitapları listele (Admin only)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'Admin':
            return jsonify({'success': False, 'message': 'Yetkisiz erişim'}), 403
        
        borrows = BorrowService.get_overdue_borrows()
        
        return jsonify({'success': True, 'borrows': borrows, 'count': len(borrows)}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@borrow_bp.route('/check-overdue', methods=['POST'])
@jwt_required()
def check_overdue():
    """Geç iade kontrolü yap ve bildirim gönder (Admin only)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'Admin':
            return jsonify({'success': False, 'message': 'Yetkisiz erişim'}), 403
        
        result = BorrowService.check_overdue_borrows()
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

