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
            msg = Message(
                subject=subject,
                recipients=[to],
                body=body,
                html=body
            )
            mail.send(msg)
            return True
        except Exception as e:
            current_app.logger.error(f"E-posta gönderme hatası: {str(e)}")
            return False
    
    @staticmethod
    def send_late_return_notification(borrow: Borrow, gecikme_gunu: int) -> bool:
        """Geç iade bildirimi"""
        user = borrow.user
        book = borrow.book
        
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
    
    @staticmethod
    def send_overdue_notification(borrow: Borrow, gecikme_gunu: int) -> bool:
        """Gecikme bildirimi (henüz iade edilmemiş)"""
        user = borrow.user
        book = borrow.book
        
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
    
    @staticmethod
    def send_reminder_notification(borrow: Borrow, kalan_gun: int) -> bool:
        """Yaklaşan iade tarihi hatırlatması"""
        user = borrow.user
        book = borrow.book
        
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

