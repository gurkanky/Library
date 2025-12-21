import os
from dotenv import load_dotenv

# .env dosyasını yükle (varsa)
load_dotenv()


class Config:
    # MSSQL Veritabanı Bağlantı Ayarları
    # Şifreniz: 123456 olarak ayarlandı
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'mssql+pyodbc://sa:123456@localhost:1433/KutuphaneDB?driver=ODBC+Driver+17+for+SQL+Server')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT (Kimlik Doğrulama) Ayarları
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '27360e82b95fc439d56610ba42c9a253')
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 saat

    # Flask-Mail (E-posta) Ayarları
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '')

    # Genel Uygulama Güvenlik Anahtarı
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')