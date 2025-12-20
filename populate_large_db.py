from app import create_app, db
from app.models.category import Category
from app.models.author import Author
from app.models.book import Book
from app.models.book_author import BookAuthor
from datetime import date
import random

app = create_app()

with app.app_context():
    print("🧹 Veritabanı temizleniyor...")
    # Önce tabloları temizle (Sıralama önemli: Önce ilişkiler, sonra ana tablolar)
    BookAuthor.query.delete()
    Book.query.delete()
    Author.query.delete()
    Category.query.delete()
    db.session.commit()

    print("📚 Kategoriler oluşturuluyor...")
    # --- KATEGORİLER ---
    cats = {
        'roman': Category(KategoriAdi='Roman', Aciklama='Edebi kurgu romanları'),
        'bilim': Category(KategoriAdi='Bilim Kurgu', Aciklama='Gelecek, uzay ve teknoloji'),
        'tarih': Category(KategoriAdi='Tarih', Aciklama='Tarihsel olaylar ve incelemeler'),
        'felsefe': Category(KategoriAdi='Felsefe', Aciklama='Düşünce ve varlık üzerine'),
        'cocuk': Category(KategoriAdi='Çocuk', Aciklama='Çocuk ve gençlik edebiyatı'),
        'kisisel': Category(KategoriAdi='Kişisel Gelişim', Aciklama='Kendini geliştirme rehberleri'),
        'polisiye': Category(KategoriAdi='Polisiye', Aciklama='Suç ve gizem romanları')
    }

    db.session.add_all(cats.values())
    db.session.commit()

    print("✍️ Yazarlar oluşturuluyor...")
    # --- YAZARLAR ---
    authors = [
        Author(Ad='George', Soyad='Orwell', Ulke='İngiltere', DogumTarihi=date(1903, 6, 25)),
        Author(Ad='J.K.', Soyad='Rowling', Ulke='İngiltere', DogumTarihi=date(1965, 7, 31)),
        Author(Ad='Sabahattin', Soyad='Ali', Ulke='Türkiye', DogumTarihi=date(1907, 2, 25)),
        Author(Ad='Fyodor', Soyad='Dostoyevski', Ulke='Rusya', DogumTarihi=date(1821, 11, 11)),
        Author(Ad='Stefan', Soyad='Zweig', Ulke='Avusturya', DogumTarihi=date(1881, 11, 28)),
        Author(Ad='Jules', Soyad='Verne', Ulke='Fransa', DogumTarihi=date(1828, 2, 8)),
        Author(Ad='Zülfü', Soyad='Livaneli', Ulke='Türkiye', DogumTarihi=date(1946, 6, 20)),
        Author(Ad='Dan', Soyad='Brown', Ulke='ABD', DogumTarihi=date(1964, 6, 22)),
        Author(Ad='Victor', Soyad='Hugo', Ulke='Fransa', DogumTarihi=date(1802, 2, 26)),
        Author(Ad='Yuval Noah', Soyad='Harari', Ulke='İsrail', DogumTarihi=date(1976, 2, 24)),
        Author(Ad='Mustafa Kemal', Soyad='Atatürk', Ulke='Türkiye', DogumTarihi=date(1881, 5, 19)),
        Author(Ad='Paulo', Soyad='Coelho', Ulke='Brezilya', DogumTarihi=date(1947, 8, 24))
    ]

    # Yazarları sözlüğe çevir (Erişim kolaylığı için)
    # authors[0] -> Orwell, authors[1] -> Rowling vb.
    db.session.add_all(authors)
    db.session.commit()

    # Yazar referanslarını al
    a_orwell = authors[0]
    a_rowling = authors[1]
    a_ali = authors[2]
    a_dosto = authors[3]
    a_zweig = authors[4]
    a_verne = authors[5]
    a_livaneli = authors[6]
    a_brown = authors[7]
    a_hugo = authors[8]
    a_harari = authors[9]
    a_ataturk = authors[10]
    a_coelho = authors[11]

    print("📖 Kitaplar ekleniyor (30+ adet)...")

    # Kitap Listesi
    books_data = [
        # George Orwell
        ('1984', '9789750718533', 1949, 352, 'roman', a_orwell),
        ('Hayvan Çiftliği', '9789750719387', 1945, 152, 'roman', a_orwell),

        # J.K. Rowling
        ('Harry Potter ve Felsefe Taşı', '9789750802942', 1997, 276, 'cocuk', a_rowling),
        ('Harry Potter ve Sırlar Odası', '9789750802959', 1998, 315, 'cocuk', a_rowling),
        ('Harry Potter ve Azkaban Tutsağı', '9789750802966', 1999, 396, 'cocuk', a_rowling),

        # Sabahattin Ali
        ('Kürk Mantolu Madonna', '9789753638029', 1943, 160, 'roman', a_ali),
        ('Kuyucaklı Yusuf', '9789753638036', 1937, 220, 'roman', a_ali),
        ('İçimizdeki Şeytan', '9789753638043', 1940, 268, 'roman', a_ali),

        # Dostoyevski
        ('Suç ve Ceza', '9789750719318', 1866, 687, 'roman', a_dosto),
        ('Karamazov Kardeşler', '9789750736865', 1880, 840, 'roman', a_dosto),
        ('Yeraltından Notlar', '9789750736889', 1864, 140, 'felsefe', a_dosto),

        # Stefan Zweig
        ('Satranç', '9786053320777', 1941, 84, 'roman', a_zweig),
        ('Bilinmeyen Bir Kadının Mektubu', '9786053321033', 1922, 68, 'roman', a_zweig),
        ('Olağanüstü Bir Gece', '9786053324621', 1922, 80, 'roman', a_zweig),
        ('Amok Koşucusu', '9786053326175', 1922, 90, 'roman', a_zweig),

        # Jules Verne
        ('Denizler Altında 20000 Fersah', '9789750742118', 1870, 400, 'bilim', a_verne),
        ('Seksen Günde Devrialem', '9789750742125', 1873, 280, 'cocuk', a_verne),
        ('Dünyanın Merkezine Yolculuk', '9789750742132', 1864, 250, 'bilim', a_verne),

        # Zülfü Livaneli
        ('Serenad', '9786050900132', 2011, 484, 'roman', a_livaneli),
        ('Kardeşimin Hikayesi', '9786050914191', 2013, 330, 'roman', a_livaneli),
        ('Huzursuzluk', '9786050939880', 2017, 160, 'roman', a_livaneli),

        # Dan Brown
        ('Da Vinci Şifresi', '9789752933453', 2003, 520, 'polisiye', a_brown),
        ('Melekler ve Şeytanlar', '9789752934009', 2000, 580, 'polisiye', a_brown),
        ('Cehennem', '9789752934016', 2013, 490, 'polisiye', a_brown),

        # Victor Hugo
        ('Sefiller', '9789750736933', 1862, 1400, 'roman', a_hugo),
        ('Notre Dame\'ın Kamburu', '9789750736940', 1831, 520, 'roman', a_hugo),

        # Yuval Noah Harari
        ('Sapiens', '9786054729074', 2011, 412, 'tarih', a_harari),
        ('Homo Deus', '9786054729869', 2015, 450, 'bilim', a_harari),

        # Mustafa Kemal Atatürk
        ('Nutuk', '9789751020086', 1927, 650, 'tarih', a_ataturk),
        ('Geometri', '9789751020093', 1937, 80, 'bilim', a_ataturk),

        # Paulo Coelho
        ('Simyacı', '9789750726439', 1988, 188, 'kisisel', a_coelho),
        ('Veronika Ölmek İstiyor', '9789750726446', 1998, 220, 'roman', a_coelho),

        # Ekstra Karışık (Aynı yazarlardan)
        ('Bir İdam Mahkumunun Son Günü', '9789750736957', 1829, 110, 'roman', a_hugo),
        ('Korku', '9786053326182', 1920, 75, 'roman', a_zweig),
        ('Ay\'a Yolculuk', '9789750742149', 1865, 200, 'bilim', a_verne)
    ]

    # Kitapları Veritabanına Ekle
    for title, isbn, year, pages, cat_key, author in books_data:
        # Rastgele stok (3 ile 15 arası)
        stock = random.randint(3, 15)

        new_book = Book(
            Baslik=title,
            ISBN=isbn,
            YayinYili=year,
            SayfaSayisi=pages,
            MevcutKopyaSayisi=stock,
            ToplamKopyaSayisi=stock,
            YayinEvi='Kültür Yayınları',  # Örnek yayınevi
            Aciklama=f'{author.Ad} {author.Soyad} tarafından yazılmış muazzam bir eser.',
            Dil='Türkçe',
            category=cats[cat_key]
        )

        db.session.add(new_book)
        db.session.flush()  # ID almak için flush

        # Yazar ilişkisini kur
        relation = BookAuthor(KitapID=new_book.KitapID, YazarID=author.YazarID)
        db.session.add(relation)

    db.session.commit()
    print(f"✅ İŞLEM TAMAMLANDI! Toplam {len(books_data)} kitap başarıyla eklendi.")