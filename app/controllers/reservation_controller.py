from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.reservation_service import ReservationService

reservation_bp = Blueprint('reservation', __name__)


@reservation_bp.route('', methods=['POST'])
@jwt_required()
def create_reservation():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data or 'kitapID' not in data:
            return jsonify({'success': False, 'message': 'Kitap ID gerekli'}), 400

        result = ReservationService.create_reservation(user_id, data['kitapID'])
        status_code = 201 if result['success'] else 400
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@reservation_bp.route('/my-reservations', methods=['GET'])
@jwt_required()
def get_my_reservations():
    try:
        user_id = int(get_jwt_identity())
        reservations = ReservationService.get_user_reservations(user_id)
        return jsonify({'success': True, 'reservations': reservations}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500