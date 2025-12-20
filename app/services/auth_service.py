from app.repositories.user_repository import UserRepository
from app.models.user import User
from flask_jwt_extended import create_access_token
from typing import Dict, Optional


class AuthService:

    @staticmethod
    def register(ad: str, soyad: str, eposta: str, sifre: str, telefon: str = None, adres: str = None) -> Dict:
        existing_user = UserRepository.find_by_email(eposta)
        if existing_user:
            return {'success': False, 'message': 'Bu e-posta adresi zaten kullanılıyor'}

        user = User(ad=ad, soyad=soyad, eposta=eposta, sifre=sifre, rol='Uye', telefon=telefon, adres=adres)
        user = UserRepository.create(user)

        # ID'yi String'e çevir (Garanti çözüm)
        access_token = create_access_token(
            identity=str(user.KullaniciID),
            additional_claims={'rol': user.Rol}
        )

        return {
            'success': True,
            'message': 'Kayıt başarılı',
            'user': user.to_dict(),
            'access_token': access_token
        }

    @staticmethod
    def login(eposta: str, sifre: str) -> Dict:
        user = UserRepository.find_by_email(eposta)

        if not user:
            return {'success': False, 'message': 'E-posta veya şifre hatalı'}

        if not user.check_password(sifre):
            return {'success': False, 'message': 'E-posta veya şifre hatalı'}

        if not user.Aktif:
            return {'success': False, 'message': 'Hesabınız pasif durumda'}

        # ID'yi String'e çevir
        access_token = create_access_token(
            identity=str(user.KullaniciID),
            additional_claims={'rol': user.Rol}
        )

        return {
            'success': True,
            'message': 'Giriş başarılı',
            'user': user.to_dict(),
            'access_token': access_token
        }

    @staticmethod
    def get_user(user_id: int) -> Optional[User]:
        return UserRepository.find_by_id(user_id)