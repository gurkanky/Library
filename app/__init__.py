from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from flasgger import Swagger
from config import Config
import os

# Eklentileri extensions dosyasından çekiyoruz
# (Önceki adımda extensions.py oluşturduysanız oradan çekin, yoksa buradaki gibi kalsın)
# Eğer extensions.py oluşturmadıysanız bu blok kalsın:
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
swagger = Swagger()


# Eğer extensions.py oluşturduysanız üstteki 4 satırı silip şunu açın:
# from app.extensions import db, jwt, mail, swagger

def create_app(config_class=Config):
    # DÜZELTME 1: Statik dosyaların (css/js) ve HTML'lerin yerini bir üst klasör (..) olarak gösteriyoruz
    app = Flask(__name__, static_folder='../static', static_url_path='/static')

    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    # CORS ayarları - Authorization header'ına izin ver
    CORS(app, supports_credentials=True, allow_headers=['Content-Type', 'Authorization'])
    mail.init_app(app)
    swagger.init_app(app)

    # Register blueprints
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

    # Swagger configuration
    app.config['SWAGGER'] = {
        'title': 'Akıllı Kütüphane Yönetim Sistemi API',
        'uiversion': 3,
        'specs_route': '/api/docs'
    }

    # DÜZELTME 2: Ana Sayfa Yönlendirmesi (Frontend Bağlantısı)
    # Siteye girildiğinde (/) ana dizindeki index.html dosyasını gönderir
    @app.route('/')
    def index():
        return send_from_directory('..', 'index.html')

    # DÜZELTME 3: Diğer HTML Sayfaları için Yönlendirme
    # Örn: /login.html veya /dashboard.html denildiğinde o dosyayı bulup gönderir
    @app.route('/<path:filename>')
    def serve_html(filename):
        # Sadece .html dosyalarına izin ver (Güvenlik için)
        if filename.endswith('.html'):
            return send_from_directory('..', filename)
        return "Sayfa bulunamadı", 404

    # Create tables (eğer yoksa)
    with app.app_context():
        try:
            # Veritabanı bağlantısını test et
            db.engine.connect()
            print("✓ Veritabanı bağlantısı başarılı")
            # Tabloları oluştur (zaten varsa bir şey yapmaz)
            db.create_all()
            print("✓ Tablolar hazır")
        except Exception as e:
            print(f"⚠ Veritabanı hatası: {str(e)}")
            print("⚠ Lütfen veritabanı bağlantı ayarlarını kontrol edin (config.py)")

    return app