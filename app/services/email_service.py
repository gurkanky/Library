from flask import current_app
from flask_mail import Message
from app import mail
from app.models.borrow import Borrow
from typing import Optional

class EmailService:
    
    @staticmethod
    def send_email(to: str, subject: str, body: str) -> bool:
        """Genel e-posta gönderme fonksiyonu"""
        try:
            # E-posta ayarları kontrolü
            if not current_app.config.get('MAIL_USERNAME') or not current_app.config.get('MAIL_PASSWORD'):
                # E-posta ayarları yapılmamış, sessizce devam et
                print("[EmailService] E-posta ayarları yapılmamış, e-posta gönderilmedi")
                return False
            
            # Subject ve to kontrolü
            if not subject or not isinstance(subject, str):
                print(f"[EmailService] Geçersiz subject: {subject}")
                return False
            
            if not to or not isinstance(to, str):
                print(f"[EmailService] Geçersiz recipient: {to}")
                return False
            
            msg = Message(
                subject=str(subject),
                recipients=[str(to)],
                body=str(body) if body else "",
                html=str(body) if body else ""
            )
            mail.send(msg)
            print(f"[EmailService] E-posta gönderildi: {to}")
            return True
        except Exception as e:
            # Hata olsa bile uygulama çalışmaya devam etsin
            print(f"[EmailService] E-posta gönderme hatası (sessizce devam ediliyor): {str(e)}")
            if current_app:
                current_app.logger.error(f"E-posta gönderme hatası: {str(e)}")
            return False
    
    @staticmethod
    def send_late_return_notification(borrow: Borrow, gecikme_gunu: int) -> bool:
        """Geç iade bildirimi"""
        try:
            if not borrow:
                return False
            
            user = borrow.user
            book = borrow.book
            
            if not user or not book:
                print(f"[EmailService] User veya book None, e-posta gönderilemedi (Borrow ID: {borrow.OduncID})")
                return False
            
            subject = "Geç İade Bildirimi - Kütüphane Yönetim Sistemi"
            body = f"""
            <html>
            <body>
                <h2>Geç İade Bildirimi</h2>
                <p>Sayın {user.Ad} {user.Soyad},</p>
                <p>"{book.Baslik}" adlı kitabı {gecikme_gunu} gün geç iade ettiniz.</p>
                <p>Geç iade cezası otomatik olarak hesabınıza eklenecektir.</p>
                <p>Ceza miktarı: {gecikme_gunu * 0.50} TL (Günlük 0.50 TL)</p>
                <br>
                <p>İyi günler dileriz.</p>
                <p>Kütüphane Yönetim Sistemi</p>
            </body>
            </html>
            """
            
            return EmailService.send_email(user.EPosta, subject, body)
        except Exception as e:
            print(f"[EmailService] send_late_return_notification hatası: {str(e)}")
            return False
    
    @staticmethod
    def send_overdue_notification(borrow: Borrow, gecikme_gunu: int) -> bool:
        """Gecikme bildirimi (henüz iade edilmemiş)"""
        try:
            if not borrow:
                return False
            
            user = borrow.user
            book = borrow.book
            
            if not user or not book:
                print(f"[EmailService] User veya book None, e-posta gönderilemedi (Borrow ID: {borrow.OduncID})")
                return False
            
            subject = "Gecikme Uyarısı - Kütüphane Yönetim Sistemi"
            body = f"""
            <html>
            <body>
                <h2>Gecikme Uyarısı</h2>
                <p>Sayın {user.Ad} {user.Soyad},</p>
                <p>"{book.Baslik}" adlı kitabın iade tarihi {gecikme_gunu} gün önce geçti.</p>
                <p>Lütfen en kısa sürede kitabı iade ediniz.</p>
                <p>Gecikme süresi uzadıkça ceza miktarı artacaktır (Günlük 0.50 TL).</p>
                <br>
                <p>İyi günler dileriz.</p>
                <p>Kütüphane Yönetim Sistemi</p>
            </body>
            </html>
            """
            
            return EmailService.send_email(user.EPosta, subject, body)
        except Exception as e:
            print(f"[EmailService] send_overdue_notification hatası: {str(e)}")
            return False
    
    @staticmethod
    def send_reminder_notification(borrow: Borrow, kalan_gun: int) -> bool:
        """Yaklaşan iade tarihi hatırlatması"""
        try:
            if not borrow:
                return False
            
            user = borrow.user
            book = borrow.book
            
            if not user or not book:
                print(f"[EmailService] User veya book None, e-posta gönderilemedi (Borrow ID: {borrow.OduncID})")
                return False
            
            subject = "İade Tarihi Hatırlatması - Kütüphane Yönetim Sistemi"
            body = f"""
            <html>
            <body>
                <h2>İade Tarihi Hatırlatması</h2>
                <p>Sayın {user.Ad} {user.Soyad},</p>
                <p>"{book.Baslik}" adlı kitabın iade tarihi {kalan_gun} gün sonra.</p>
                <p>Lütfen zamanında iade ediniz.</p>
                <br>
                <p>İyi günler dileriz.</p>
                <p>Kütüphane Yönetim Sistemi</p>
            </body>
            </html>
            """
            
            return EmailService.send_email(user.EPosta, subject, body)
        except Exception as e:
            print(f"[EmailService] send_reminder_notification hatası: {str(e)}")
            return False

