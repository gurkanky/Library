from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Kullanıcı kayıt endpoint'i"""
    try:
        data = request.get_json()

        # Zorunlu alan kontrolü
        required_fields = ['ad', 'soyad', 'eposta', 'sifre']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Eksik alanlar var'}), 400

        # DÜZELTME: Metod adı 'register_user' ve parametre olarak tüm 'data' gönderiliyor
        result = AuthService.register_user(data)

        status_code = 201 if result['success'] else 400
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Kullanıcı giriş endpoint'i"""
    try:
        data = request.get_json()

        if not data or 'eposta' not in data or 'sifre' not in data:
            return jsonify({'success': False, 'message': 'E-posta ve şifre gerekli'}), 400

        # DÜZELTME: Metod adı 'login_user' olarak güncellendi
        result = AuthService.login_user(
            email=data['eposta'],
            password=data['sifre']
        )

        status_code = 200 if result['success'] else 401
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Mevcut kullanıcı bilgilerini getir"""
    try:
        user_id = get_jwt_identity()

        # Bu metodun serviste tanımlı olduğundan emin olacağız (2. Adım)
        user = AuthService.get_user(int(user_id))

        if user:
            return jsonify({'success': True, 'user': user.to_dict()}), 200
        else:
            return jsonify({'success': False, 'message': 'Kullanıcı bulunamadı'}), 404

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500