from flask import Blueprint, request, jsonify
from app.repositories.user_repository import UserRepository
from app.services.penalty_service import PenaltyService
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Kullanıcı profil bilgilerini getir"""
    try:
        user_id = get_jwt_identity()
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
        user_id = get_jwt_identity()
        penalties = PenaltyService.get_user_penalties(user_id)
        
        return jsonify({'success': True, 'penalties': penalties, 'count': len(penalties)}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@user_bp.route('/debt', methods=['GET'])
@jwt_required()
def get_debt():
    """Kullanıcının toplam borcunu getir"""
    try:
        user_id = get_jwt_identity()
        debt = PenaltyService.get_total_debt(user_id)
        
        return jsonify({'success': True, **debt}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@user_bp.route('/penalties/<int:penalty_id>/pay', methods=['POST'])
@jwt_required()
def pay_penalty(penalty_id):
    """Ceza öde"""
    try:
        user_id = get_jwt_identity()
        result = PenaltyService.pay_penalty(penalty_id, user_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

