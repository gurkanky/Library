from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # SQL Server bağlantısı üzerinden triggerları siliyoruz
        with db.engine.connect() as conn:
            print("Triggerlar siliniyor...")
            conn.execute(text("DROP TRIGGER IF EXISTS TRG_KitapOduncAlindi"))
            conn.execute(text("DROP TRIGGER IF EXISTS TRG_KitapIadeEdildi"))
            conn.commit()
            print("BAŞARILI: Sorunlu triggerlar veritabanından temizlendi.")
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")