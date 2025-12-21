from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.review_service import ReviewService

review_bp = Blueprint('review', __name__)


@review_bp.route('/book/<int:book_id>', methods=['GET'])
@jwt_required()
def get_reviews(book_id):
    """Bir kitabın yorumlarını getir"""
    reviews = ReviewService.get_book_reviews(book_id)
    return jsonify({'success': True, 'reviews': reviews})


@review_bp.route('', methods=['POST'])
@jwt_required()
def add_review():
    """Yeni yorum ekle"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()

        if not data or 'kitapID' not in data or 'puan' not in data:
            return jsonify({'success': False, 'message': 'Eksik veri'}), 400

        result = ReviewService.add_review(
            user_id,
            data['kitapID'],
            data['puan'],
            data.get('yorum', '')
        )
        status_code = 201 if result['success'] else 400
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@review_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """Yorum sil"""
    try:
        user_id = int(get_jwt_identity())
        claims = get_jwt()
        is_admin = claims.get('rol') == 'Admin'

        result = ReviewService.delete_review(review_id, user_id, is_admin)
        status_code = 200 if result['success'] else 403
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500