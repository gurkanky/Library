from app import create_app, db
from app.models.category import Category
from app.models.author import Author
from app.models.book import Book
from app.models.book_author import BookAuthor
from datetime import date
import random

app = create_app()


def get_or_create_category(name, desc):
    cat = Category.query.filter_by(KategoriAdi=name).first()
    if not cat:
        cat = Category(KategoriAdi=name, Aciklama=desc)
        db.session.add(cat)
        db.session.commit()
    return cat


def get_or_create_author(ad, soyad, ulke='Türkiye', dogum=None):
    author = Author.query.filter_by(Ad=ad, Soyad=soyad).first()
    if not author:
        author = Author(Ad=ad, Soyad=soyad, Ulke=ulke, DogumTarihi=dogum)
        db.session.add(author)
        db.session.commit()
    return author


with app.app_context():
    print("🇹🇷 Türk Edebiyatı eserleri ekleniyor...")

    # Kategorileri Hazırla
    cat_roman = get_or_create_category('Roman', 'Edebi kurgu eserleri')
    cat_siir = get_or_create_category('Şiir', 'Şiir kitapları')
    cat_deneme = get_or_create_category('Deneme', 'Düşünce ve eleştiri yazıları')
    cat_tarih = get_or_create_category('Tarih', 'Tarihsel incelemeler')

    # Kitap Listesi (Yazar Adı, Yazar Soyadı, Kitap Adı, ISBN, Yıl, Sayfa, Tür Kategorisi)
    # Not: ISBN'ler çakışmaması için rastgele üretilmiş veya son haneleri değiştirilmiştir.
    books_data = [
        # Yaşar Kemal
        ('Yaşar', 'Kemal', 'İnce Memed 1', '9789750807084', 1955, 436, cat_roman),
        ('Yaşar', 'Kemal', 'İnce Memed 2', '9789750807091', 1969, 465, cat_roman),
        ('Yaşar', 'Kemal', 'İnce Memed 3', '9789750807107', 1984, 520, cat_roman),
        ('Yaşar', 'Kemal', 'İnce Memed 4', '9789750807114', 1987, 580, cat_roman),
        ('Yaşar', 'Kemal', 'Yer Demir Gök Bakır', '9789750807121', 1963, 380, cat_roman),

        # Oğuz Atay
        ('Oğuz', 'Atay', 'Tutunamayanlar', '9789754700114', 1972, 724, cat_roman),
        ('Oğuz', 'Atay', 'Tehlikeli Oyunlar', '9789754700541', 1973, 470, cat_roman),
        ('Oğuz', 'Atay', 'Bir Bilim Adamının Romanı', '9789754700558', 1975, 280, cat_roman),

        # Ahmet Hamdi Tanpınar
        ('Ahmet Hamdi', 'Tanpınar', 'Saatleri Ayarlama Enstitüsü', '9789759950262', 1961, 382, cat_roman),
        ('Ahmet Hamdi', 'Tanpınar', 'Huzur', '9789759950279', 1949, 412, cat_roman),
        ('Ahmet Hamdi', 'Tanpınar', 'Beş Şehir', '9789759950286', 1946, 210, cat_deneme),

        # Orhan Pamuk
        ('Orhan', 'Pamuk', 'Benim Adım Kırmızı', '9789754707113', 1998, 450, cat_roman),
        ('Orhan', 'Pamuk', 'Kara Kitap', '9789754707120', 1990, 480, cat_roman),
        ('Orhan', 'Pamuk', 'Masumiyet Müzesi', '9789754707137', 2008, 590, cat_roman),

        # İhsan Oktay Anar
        ('İhsan Oktay', 'Anar', 'Puslu Kıtalar Atlası', '9789754704785', 1995, 238, cat_roman),
        ('İhsan Oktay', 'Anar', 'Suskunlar', '9789754704792', 2007, 260, cat_roman),
        ('İhsan Oktay', 'Anar', 'Amat', '9789754704808', 2005, 230, cat_roman),

        # Reşat Nuri Güntekin
        ('Reşat Nuri', 'Güntekin', 'Çalıkuşu', '9789751020024', 1922, 540, cat_roman),
        ('Reşat Nuri', 'Güntekin', 'Yeşil Gece', '9789751020031', 1928, 280, cat_roman),
        ('Reşat Nuri', 'Güntekin', 'Yaprak Dökümü', '9789751020048', 1930, 160, cat_roman),

        # Peyami Safa
        ('Peyami', 'Safa', 'Dokuzuncu Hariciye Koğuşu', '9789754370423', 1930, 120, cat_roman),
        ('Peyami', 'Safa', 'Fatih-Harbiye', '9789754370430', 1931, 140, cat_roman),
        ('Peyami', 'Safa', 'Yalnızız', '9789754370447', 1951, 360, cat_roman),

        # Yusuf Atılgan
        ('Yusuf', 'Atılgan', 'Aylak Adam', '9789750807664', 1959, 150, cat_roman),
        ('Yusuf', 'Atılgan', 'Anayurt Oteli', '9789750807671', 1973, 110, cat_roman),

        # Halide Edip Adıvar
        ('Halide Edip', 'Adıvar', 'Sinekli Bakkal', '9789750719875', 1936, 420, cat_roman),
        ('Halide Edip', 'Adıvar', 'Ateşten Gömlek', '9789750719882', 1922, 230, cat_roman),

        # Yakup Kadri Karaosmanoğlu
        ('Yakup Kadri', 'Karaosmanoğlu', 'Yaban', '9789754700145', 1932, 215, cat_roman),
        ('Yakup Kadri', 'Karaosmanoğlu', 'Kiralık Konak', '9789754700152', 1922, 240, cat_roman),

        # Nazım Hikmet
        ('Nazım', 'Hikmet', 'Memleketimden İnsan Manzaraları', '9789750803109', 1966, 540, cat_siir),
        ('Nazım', 'Hikmet', 'Henüz Vakit Varken Gülüm', '9789750803116', 2008, 180, cat_siir)
    ]

    added_count = 0
    for ad, soyad, kitap_adi, isbn, yil, sayfa, kategori in books_data:
        # Kitap daha önce eklenmiş mi kontrol et (ISBN'e göre)
        existing_book = Book.query.filter_by(ISBN=isbn).first()
        if existing_book:
            print(f"⚠️  Atlandı (Zaten var): {kitap_adi}")
            continue

        # Yazarı bul veya oluştur
        author = get_or_create_author(ad, soyad)

        # Stok durumunu rastgele belirle
        stock = random.randint(3, 10)

        # Kitabı oluştur
        new_book = Book(
            Baslik=kitap_adi,
            ISBN=isbn,
            YayinYili=yil,
            SayfaSayisi=sayfa,
            MevcutKopyaSayisi=stock,
            ToplamKopyaSayisi=stock,
            YayinEvi='Türk Klasikleri Yayınları',
            Aciklama=f'{ad} {soyad} tarafından kaleme alınan, Türk edebiyatının önemli eserlerinden biri.',
            Dil='Türkçe',
            category=kategori
        )

        db.session.add(new_book)
        db.session.flush()  # ID almak için

        # Yazar-Kitap ilişkisini kur
        relation = BookAuthor(KitapID=new_book.KitapID, YazarID=author.YazarID)
        db.session.add(relation)

        added_count += 1
        print(f"✅ Eklendi: {kitap_adi}")

    db.session.commit()
    print(f"\nToplam {added_count} yeni Türkçe kitap başarıyla eklendi!")