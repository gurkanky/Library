from flask import Blueprint, request, jsonify
from app.repositories.user_repository import UserRepository
from app.services.penalty_service import PenaltyService
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Kullanıcı profil bilgilerini getir"""
    try:
        # Düzeltme: ID'yi int'e çevir
        user_id = int(get_jwt_identity())
        user = UserRepository.find_by_id(user_id)

        if user:
            return jsonify({'success': True, 'user': user.to_dict()}), 200
        else:
            return jsonify({'success': False, 'message': 'Kullanıcı bulunamadı'}), 404

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@user_bp.route('/penalties', methods=['GET'])
@jwt_required()
def get_penalties():
    """Kullanıcının cezalarını listele"""
    try:
        # Düzeltme: ID'yi int'e çevir
        user_id = int(get_jwt_identity())
        penalties = PenaltyService.get_user_penalties(user_id)

        return jsonify({'success': True, 'penalties': penalties, 'count': len(penalties)}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@user_bp.route('/debt', methods=['GET'])
@jwt_required()
def get_debt():
    """Kullanıcının toplam borcunu getir"""
    try:
        # Düzeltme: ID'yi int'e çevir
        user_id = int(get_jwt_identity())
        debt = PenaltyService.get_total_debt(user_id)

        return jsonify({'success': True, **debt}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@user_bp.route('/penalties/<int:penalty_id>/pay', methods=['POST'])
@jwt_required()
def pay_penalty(penalty_id):
    """Ceza öde"""
    try:
        # --- KRİTİK DÜZELTME BURADA ---
        # Token'dan gelen ID string olabilir, int'e çeviriyoruz.
        user_id = int(get_jwt_identity())

        result = PenaltyService.pay_penalty(penalty_id, user_id)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        # Hata detayını terminalde görebilmek için:
        print(f"HATA (Pay Penalty): {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@user_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Kullanıcı şifresini değiştir"""
    try:
        # Düzeltme: ID'yi int'e çevir
        user_id = int(get_jwt_identity())

        data = request.get_json()
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not old_password or not new_password:
            return jsonify({'success': False, 'message': 'Eski ve yeni şifre gereklidir'}), 400

        user = UserRepository.find_by_id(user_id)

        if not user or not user.check_password(old_password):
            return jsonify({'success': False, 'message': 'Eski şifre hatalı'}), 400

        # Yeni şifreyi ayarla ve kaydet
        user.set_password(new_password)
        UserRepository.update(user)

        return jsonify({'success': True, 'message': 'Şifre başarıyla güncellendi'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@user_bp.route('/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    """Hesabı sil (Borç/Kitap kontrolü ile)"""
    try:
        # Düzeltme: ID'yi int'e çevir
        user_id = int(get_jwt_identity())

        # 1. Kontrol: Üzerinde kitap veya borç var mı?
        if UserRepository.check_has_debt_or_loans(user_id):
            return jsonify({
                'success': False,
                'message': 'Üzerinizde iade edilmemiş kitap veya ödenmemiş ceza varken hesabınızı silemezsiniz.'
            }), 400

        # 2. Silme işlemi
        if UserRepository.delete(user_id):
            return jsonify({'success': True, 'message': 'Hesabınız başarıyla silindi'}), 200
        else:
            return jsonify({'success': False, 'message': 'Silme işlemi başarısız'}), 400

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@user_bp.route('/favorites', methods=['GET'])
@jwt_required()
def get_user_favorites():
    """Favori kitapları getir"""
    try:
        # Düzeltme: ID'yi int'e çevir
        user_id = int(get_jwt_identity())
        favorites = UserRepository.get_favorites(user_id)
        return jsonify({
            'success': True,
            'favorites': [f.to_dict() for f in favorites]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@user_bp.route('/favorites/<int:book_id>', methods=['POST', 'DELETE'])
@jwt_required()
def toggle_favorite(book_id):
    """Favoriye ekle veya çıkar"""
    try:
        # Düzeltme: ID'yi int'e çevir
        user_id = int(get_jwt_identity())

        if request.method == 'POST':
            if UserRepository.add_favorite(user_id, book_id):
                return jsonify({'success': True, 'message': 'Kitap favorilere eklendi'}), 200
            return jsonify({'success': False, 'message': 'Kitap zaten favorilerde'}), 400

        elif request.method == 'DELETE':
            if UserRepository.remove_favorite(user_id, book_id):
                return jsonify({'success': True, 'message': 'Kitap favorilerden çıkarıldı'}), 200
            return jsonify({'success': False, 'message': 'Favorilerde bulunamadı'}), 400

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500