from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Kullanıcı kayıt endpoint'i"""
    try:
        data = request.get_json()
        
        required_fields = ['ad', 'soyad', 'eposta', 'sifre']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Eksik alanlar var'}), 400
        
        result = AuthService.register(
            ad=data['ad'],
            soyad=data['soyad'],
            eposta=data['eposta'],
            sifre=data['sifre'],
            telefon=data.get('telefon'),
            adres=data.get('adres')
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Kullanıcı giriş endpoint'i"""
    try:
        data = request.get_json()
        
        if not data or 'eposta' not in data or 'sifre' not in data:
            return jsonify({'success': False, 'message': 'E-posta ve şifre gerekli'}), 400
        
        result = AuthService.login(
            eposta=data['eposta'],
            sifre=data['sifre']
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Mevcut kullanıcı bilgilerini getir"""
    try:
        user_id = get_jwt_identity()
        user = AuthService.get_user(user_id)
        
        if user:
            return jsonify({'success': True, 'user': user.to_dict()}), 200
        else:
            return jsonify({'success': False, 'message': 'Kullanıcı bulunamadı'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

