from app import db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from flask_jwt_extended import create_access_token
from app.services.email_service import EmailService


class AuthService:
    @staticmethod
    def register_user(data):
        # 1. Validasyonlar
        if not data.get('eposta') or not data.get('sifre'):
            return {'success': False, 'message': 'E-posta ve şifre zorunludur'}

        if UserRepository.find_by_email(data['eposta']):
            return {'success': False, 'message': 'Bu e-posta adresi zaten kayıtlı'}

        # 2. Kullanıcı Oluşturma
        # ÖNEMLİ DÜZELTME: Parametre isimleri küçük harf yapıldı (ad=, soyad=...)
        # ve şifre ham haliyle gönderildi (Model kendi içinde hashliyor).
        new_user = User(
            ad=data.get('ad'),
            soyad=data.get('soyad'),
            eposta=data['eposta'],
            sifre=data['sifre'],  # Ham şifre gönderiyoruz
            telefon=data.get('telefon'),
            adres=data.get('adres'),
            rol='Uye'
        )

        try:
            db.session.add(new_user)
            db.session.commit()

            # E-posta gönderimi
            try:
                EmailService.send_welcome_email(new_user)
            except Exception as e:
                print(f"Mail gönderme hatası: {e}")

            # Token üretimi
            access_token = create_access_token(identity=str(new_user.KullaniciID),
                                               additional_claims={'rol': new_user.Rol})

            return {
                'success': True,
                'message': 'Kayıt başarılı',
                'access_token': access_token,
                'user': new_user.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Kayıt hatası: {str(e)}'}

    @staticmethod
    def login_user(email, password):
        user = UserRepository.find_by_email(email)

        if not user:
            return {'success': False, 'message': 'Geçersiz e-posta veya şifre'}

        # Şifre kontrolü (Model içindeki check_password kullanılır)
        # Not: User modelinizde 'bcrypt' kütüphanesi kullanılıyor.
        # Eğer yüklü değilse: pip install bcrypt
        if not user.check_password(password):
            return {'success': False, 'message': 'Geçersiz e-posta veya şifre'}

        if not user.Aktif:
            return {'success': False, 'message': 'Hesabınız pasif durumda'}

        access_token = create_access_token(identity=str(user.KullaniciID), additional_claims={'rol': user.Rol})

        return {
            'success': True,
            'message': 'Giriş başarılı',
            'access_token': access_token,
            'user': user.to_dict()
        }

    @staticmethod
    def get_user(user_id):
        return UserRepository.find_by_id(user_id)