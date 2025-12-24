from app import db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from flask_jwt_extended import create_access_token
from app.services.email_service import EmailService
import random


class AuthService:
    @staticmethod
    def register_user(data):
        """Yeni kullanıcı kaydeder ve doğrulama kodu gönderir"""
        # 1. Validasyonlar
        if not data.get('eposta') or not data.get('sifre'):
            return {'success': False, 'message': 'E-posta ve şifre zorunludur'}

        if UserRepository.find_by_email(data['eposta']):
            return {'success': False, 'message': 'Bu e-posta adresi zaten kayıtlı'}

        # 2. Rastgele 6 haneli doğrulama kodu üret
        verification_code = str(random.randint(100000, 999999))

        # 3. Kullanıcı Oluşturma
        # Not: User modelinin __init__ metodunda varsayılan olarak Aktif=False ayarlandığını varsayıyoruz.
        new_user = User(
            ad=data.get('ad'),
            soyad=data.get('soyad'),
            eposta=data['eposta'],
            sifre=data['sifre'],  # Ham şifre (Model hashleyecek)
            telefon=data.get('telefon'),
            adres=data.get('adres'),
            rol='Uye',
            dogrulama_kodu=verification_code
        )

        # Garanti olsun diye tekrar pasif yapalım
        new_user.Aktif = False

        try:
            db.session.add(new_user)
            db.session.commit()

            # E-posta ile doğrulama kodunu gönder
            try:
                EmailService.send_verification_code(new_user, verification_code)
            except Exception as e:
                print(f"Mail gönderme hatası: {e}")

            return {
                'success': True,
                'message': 'Kayıt başarılı! Lütfen e-posta adresinize gönderilen doğrulama kodunu giriniz.',
                'require_verification': True,
                'email': new_user.EPosta
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Kayıt hatası: {str(e)}'}

    @staticmethod
    def verify_email(data):
        """Kullanıcının girdiği kodu doğrular ve hesabı aktif eder"""
        email = data.get('eposta')
        code = data.get('kod')

        if not email or not code:
            return {'success': False, 'message': 'E-posta ve kod gereklidir'}

        user = UserRepository.find_by_email(email)

        if not user:
            return {'success': False, 'message': 'Kullanıcı bulunamadı'}

        if user.Aktif:
            return {'success': False, 'message': 'Bu hesap zaten doğrulanmış'}

        # Kod kontrolü
        if user.DogrulamaKodu == code:
            user.Aktif = True
            user.DogrulamaKodu = None  # Güvenlik için kodu temizle

            try:
                db.session.commit()

                # Hoş geldin maili gönder
                try:
                    EmailService.send_welcome_email(user)
                except Exception:
                    pass

                return {'success': True, 'message': 'Hesabınız başarıyla doğrulandı. Artık giriş yapabilirsiniz.'}
            except Exception as e:
                db.session.rollback()
                return {'success': False, 'message': f'Doğrulama sırasında hata oluştu: {str(e)}'}
        else:
            return {'success': False, 'message': 'Geçersiz doğrulama kodu!'}

    @staticmethod
    def login_user(email, password):
        """Kullanıcı girişi yapar"""
        user = UserRepository.find_by_email(email)

        if not user:
            return {'success': False, 'message': 'Geçersiz e-posta veya şifre'}

        # Şifre kontrolü
        if not user.check_password(password):
            return {'success': False, 'message': 'Geçersiz e-posta veya şifre'}

        # Aktiflik kontrolü
        if not user.Aktif:
            return {'success': False,
                    'message': 'Hesabınız henüz doğrulanmamış veya pasif durumda. Lütfen e-postanızı kontrol edin.'}

        # Token oluştur
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

    @staticmethod
    def forgot_password(data):
        """Şifre sıfırlama kodu üretir ve mail atar"""
        email = data.get('eposta')
        if not email:
            return {'success': False, 'message': 'E-posta adresi gereklidir'}

        user = UserRepository.find_by_email(email)

        # Güvenlik notu: Kullanıcı yoksa bile 'gönderildi' demek daha güvenlidir ama
        # şimdilik geliştirme aşamasında net hata dönüyoruz.
        if not user:
            return {'success': False, 'message': 'Bu e-posta adresi ile kayıtlı kullanıcı bulunamadı'}

        # 6 haneli kod üret
        reset_code = str(random.randint(100000, 999999))

        # Kodu kullanıcıya kaydet
        user.DogrulamaKodu = reset_code

        try:
            db.session.commit()

            # Mail gönder
            EmailService.send_password_reset_code(user, reset_code)
            return {'success': True, 'message': 'Sıfırlama kodu e-posta adresinize gönderildi.'}

        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'İşlem sırasında hata oluştu: {str(e)}'}

    @staticmethod
    def reset_password(data):
        """Kodu doğrular ve şifreyi değiştirir"""
        email = data.get('eposta')
        code = data.get('kod')
        new_password = data.get('yeni_sifre')

        if not all([email, code, new_password]):
            return {'success': False, 'message': 'Tüm alanlar zorunludur'}

        user = UserRepository.find_by_email(email)
        if not user:
            return {'success': False, 'message': 'Kullanıcı bulunamadı'}

        # Kod kontrolü
        if user.DogrulamaKodu != code:
            return {'success': False, 'message': 'Geçersiz doğrulama kodu'}

        try:
            # Şifreyi güncelle (Model içindeki set_password hashleme yapar)
            user.set_password(new_password)
            user.DogrulamaKodu = None  # Kodu temizle
            db.session.commit()

            return {'success': True, 'message': 'Şifreniz başarıyla güncellendi. Giriş yapabilirsiniz.'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Şifre güncellenirken hata oluştu: {str(e)}'}