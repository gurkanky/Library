from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from flasgger import Swagger
from config import Config

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
swagger = Swagger()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    mail.init_app(app)
    swagger.init_app(app)
    
    # Register blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.book_controller import book_bp
    from app.controllers.user_controller import user_bp
    from app.controllers.borrow_controller import borrow_bp
    from app.controllers.admin_controller import admin_bp
    from app.controllers.category_controller import category_bp
    from app.controllers.author_controller import author_bp
    
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
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

