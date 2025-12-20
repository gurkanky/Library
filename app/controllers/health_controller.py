from flask import Blueprint, jsonify
from app import db

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Sistem sağlık kontrolü"""
    try:
        # Veritabanı bağlantısını test et
        db.engine.connect()
        return jsonify({
            'success': True,
            'status': 'healthy',
            'database': 'connected',
            'message': 'Sistem çalışıyor'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'database': 'disconnected',
            'message': f'Veritabanı bağlantı hatası: {str(e)}'
        }), 503

