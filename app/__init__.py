from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
# ÖNEMLİ: Eklentileri artık extensions.py'dan çekiyoruz
from app.extensions import db, jwt, mail, swagger


def create_app(config_class=Config):
    # Statik dosyalar ve şablonlar için yol ayarı
    app = Flask(__name__, static_folder='../static', static_url_path='/static')
    app.config.from_object(config_class)

    # Eklentileri başlat
    db.init_app(app)
    jwt.init_app(app)
    # CORS ayarları
    CORS(app, supports_credentials=True, allow_headers=['Content-Type', 'Authorization'])
    mail.init_app(app)
    swagger.init_app(app)

    # Blueprint kayıtları (Controller'lar)
    from app.controllers.health_controller import health_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.book_controller import book_bp
    from app.controllers.user_controller import user_bp
    from app.controllers.borrow_controller import borrow_bp
    from app.controllers.admin_controller import admin_bp
    from app.controllers.category_controller import category_bp
    from app.controllers.author_controller import author_bp

    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(book_bp, url_prefix='/api/books')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(borrow_bp, url_prefix='/api/borrow')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(category_bp, url_prefix='/api/categories')
    app.register_blueprint(author_bp, url_prefix='/api/authors')

    # Swagger ayarları
    app.config['SWAGGER'] = {
        'title': 'Akıllı Kütüphane Yönetim Sistemi API',
        'uiversion': 3,
        'specs_route': '/api/docs'
    }

    # Ana Sayfa Yönlendirmesi
    @app.route('/')
    def index():
        return send_from_directory('..', 'index.html')

    # Diğer HTML Sayfaları
    @app.route('/<path:filename>')
    def serve_html(filename):
        if filename.endswith('.html'):
            return send_from_directory('..', filename)
        return "Sayfa bulunamadı", 404

    # Veritabanı tablolarını oluştur
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Veritabanı uyarısı: {e}")

    return app