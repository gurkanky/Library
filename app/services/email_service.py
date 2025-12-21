from flask_mail import Message
from flask import current_app
from app.extensions import mail
from threading import Thread


class EmailService:
    @staticmethod
    def send_async_email(app, msg):
        """Maili arka planda (asenkron) gönderir, böylece site donmaz."""
        with app.app_context():
            try:
                mail.send(msg)
                print(f"Mail gönderildi: {msg.subject}")
            except Exception as e:
                print(f"Mail gönderme hatası: {e}")

    @staticmethod
    def send_email(to, subject, body):
        """Genel mail gönderme fonksiyonu"""
        app = current_app._get_current_object()
        msg = Message(subject, recipients=[to])
        msg.body = body
        # HTML desteği isterseniz: msg.html = render_template(...) kullanabilirsiniz

        # Thread kullanarak işlemi hızlandır (kullanıcıyı bekletme)
        thr = Thread(target=EmailService.send_async_email, args=(app, msg))
        thr.start()

    # --- ÖZEL SENARYOLAR ---

    @staticmethod
    def send_welcome_email(user):
        """Yeni üye olan kullanıcıya gider"""
        subject = "Aramıza Hoş Geldiniz! 📚"
        body = f"""Merhaba {user.Ad},

Akıllı Kütüphane Sistemine üye olduğunuz için teşekkür ederiz.
Artık kütüphanemizdeki binlerce kitaba erişebilir, ödünç alabilir ve yorum yapabilirsiniz.

İyi okumalar dileriz!
"""
        EmailService.send_email(user.EPosta, subject, body)

    @staticmethod
    def send_borrow_notification(user, book, due_date):
        """Kitap ödünç alındığında gider"""
        tarih_str = due_date.strftime('%d.%m.%Y')
        subject = f"Kitap Ödünç Alındı: {book.Baslik}"
        body = f"""Merhaba {user.Ad},

'{book.Baslik}' isimli kitabı başarıyla ödünç aldınız.

Son Teslim Tarihi: {tarih_str}

Lütfen kitabı zamanında iade etmeyi unutmayın, aksi takdirde günlük gecikme cezası uygulanacaktır.

Keyifli okumalar!
"""
        EmailService.send_email(user.EPosta, subject, body)

    @staticmethod
    def send_reservation_notification(user, book):
        """Rezervasyon sırası geldiğinde gider"""
        subject = f"Müjde! {book.Baslik} Artık Müsait"
        body = f"""Merhaba {user.Ad},

Sırada beklediğiniz '{book.Baslik}' kitabı şu an kütüphaneye iade edildi.
Hemen giriş yapıp kitabı ödünç alabilirsiniz!
"""
        EmailService.send_email(user.EPosta, subject, body)