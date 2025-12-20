from flask import current_app
from flask_mail import Message
from app.extensions import mail  # extensions.py kullanıyorsan
# Eğer extensions.py yoksa: from app import mail
from typing import Optional


class EmailService:

    @staticmethod
    def send_email(to: str, subject: str, body: str) -> bool:
        """Güvenli e-posta gönderme"""
        try:
            if not current_app.config.get('MAIL_USERNAME'):
                print("[Email] Mail ayarları yok, atlandı.")
                return False

            # Subject ve To kesinlikle string olsun
            safe_subject = str(subject) if subject else "Bildirim"
            safe_to = str(to) if to else ""

            if not safe_to:
                return False

            msg = Message(
                subject=safe_subject,
                recipients=[safe_to],
                body=str(body) if body else "",
                html=str(body) if body else ""
            )
            mail.send(msg)
            return True
        except Exception as e:
            # Hata olsa bile sistemi durdurma
            print(f"[Email Hatası] Gönderilemedi: {str(e)}")
            return False

    # Diğer metodlar (send_late_return vb.) aynı kalabilir,
    # çünkü hepsi sonunda send_email'i çağırıyor.
    @staticmethod
    def send_late_return_notification(borrow, gecikme):
        return EmailService.send_email(borrow.user.EPosta, "Geç İade", f"{gecikme} gün gecikti.")

    @staticmethod
    def send_overdue_notification(borrow, gecikme):
        return EmailService.send_email(borrow.user.EPosta, "Gecikme", f"{gecikme} gün geçti.")