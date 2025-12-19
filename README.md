# Akıllı Kütüphane Yönetim Sistemi

Flask (Python) ve MSSQL kullanılarak geliştirilmiş kapsamlı bir kütüphane yönetim sistemi.

## Özellikler

- ✅ **Katmanlı Mimari**: Entity, Repository, Service, Controller katmanları
- ✅ **JWT Kimlik Doğrulama**: Güvenli token tabanlı kimlik doğrulama
- ✅ **REST API**: Tam CRUD işlemleri için RESTful API endpoints
- ✅ **Veritabanı**: MSSQL ile ilişkisel veritabanı tasarımı
- ✅ **Trigger ve Stored Procedure**: Otomatik ceza hesaplama ve veri kontrolü
- ✅ **E-posta Bildirimleri**: Geç iade için otomatik e-posta bildirimleri
- ✅ **Modern Frontend**: HTML/CSS/JavaScript ile responsive arayüz
- ✅ **Admin Paneli**: Kapsamlı yönetim paneli

## Teknolojiler

- **Backend**: Flask (Python)
- **Veritabanı**: MSSQL Server
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Kimlik Doğrulama**: JWT (JSON Web Token)
- **ORM**: SQLAlchemy

## Kurulum

### 1. Gereksinimler

- Python 3.8+
- MSSQL Server
- ODBC Driver 17 for SQL Server

### 2. Veritabanı Kurulumu

1. MSSQL Server'ı başlatın
2. `database/schema.sql` dosyasını SQL Server Management Studio'da çalıştırın
3. Veritabanı bağlantı bilgilerini `.env` dosyasına ekleyin

### 3. Python Bağımlılıkları

```bash
pip install -r requirements.txt
```

### 4. Ortam Değişkenleri

`.env.example` dosyasını `.env` olarak kopyalayın ve gerekli bilgileri doldurun:

```bash
cp .env.example .env
```

### 5. Uygulamayı Çalıştırma

```bash
python app.py
```

Uygulama `http://localhost:5000` adresinde çalışacaktır.

## API Endpoints

### Kimlik Doğrulama
- `POST /api/auth/register` - Kullanıcı kaydı
- `POST /api/auth/login` - Giriş
- `GET /api/auth/me` - Mevcut kullanıcı bilgisi

### Kitaplar
- `GET /api/books` - Tüm kitapları listele
- `GET /api/books/<id>` - Kitap detayı
- `POST /api/books` - Yeni kitap ekle (Admin)
- `PUT /api/books/<id>` - Kitap güncelle (Admin)
- `DELETE /api/books/<id>` - Kitap sil (Admin)

### Ödünç İşlemleri
- `POST /api/borrow` - Kitap ödünç al
- `POST /api/borrow/<id>/return` - Kitap iade et
- `GET /api/borrow/my-books` - Kullanıcının ödünç kitapları
- `GET /api/borrow/all` - Tüm ödünç işlemleri (Admin)
- `GET /api/borrow/overdue` - Geç iade kitaplar (Admin)

### Kategoriler
- `GET /api/categories` - Tüm kategoriler
- `POST /api/categories` - Yeni kategori ekle (Admin)
- `PUT /api/categories/<id>` - Kategori güncelle (Admin)
- `DELETE /api/categories/<id>` - Kategori sil (Admin)

### Yazarlar
- `GET /api/authors` - Tüm yazarlar
- `POST /api/authors` - Yeni yazar ekle (Admin)
- `PUT /api/authors/<id>` - Yazar güncelle (Admin)
- `DELETE /api/authors/<id>` - Yazar sil (Admin)

### Kullanıcı İşlemleri
- `GET /api/users/profile` - Kullanıcı profili
- `GET /api/users/penalties` - Kullanıcı cezaları
- `GET /api/users/debt` - Toplam borç
- `POST /api/users/penalties/<id>/pay` - Ceza öde

### Admin İşlemleri
- `GET /api/admin/users` - Tüm kullanıcılar
- `PUT /api/admin/users/<id>` - Kullanıcı güncelle
- `DELETE /api/admin/users/<id>` - Kullanıcı sil
- `GET /api/admin/penalties` - Tüm cezalar
- `GET /api/admin/statistics` - İstatistikler

## Veritabanı Yapısı

### Tablolar
- **Kullanıcılar**: Kullanıcı bilgileri (Admin ve Üye)
- **Kitaplar**: Kitap bilgileri
- **Kategoriler**: Kitap kategorileri
- **Yazarlar**: Yazar bilgileri
- **KitapYazarlar**: Kitap-Yazar ilişkisi (Çoktan-Çoğa)
- **OduncIslemleri**: Ödünç verme işlemleri
- **Cezalar**: Geç iade cezaları

### Trigger'lar
- `TRG_GecikmeCezaHesapla`: Geç iade için otomatik ceza hesaplama
- `TRG_KitapOduncAlindi`: Ödünç alındığında stok azaltma
- `TRG_KitapIadeEdildi`: İade edildiğinde stok artırma

### Stored Procedure'lar
- `SP_GecikmisOduncKontrol`: Geç iade kontrolü
- `SP_KullaniciOduncListesi`: Kullanıcı ödünç listesi
- `SP_KullaniciToplamBorc`: Toplam borç hesaplama

## Frontend Sayfaları

- `index.html` - Ana sayfa
- `login.html` - Giriş sayfası
- `register.html` - Kayıt sayfası
- `dashboard.html` - Kullanıcı dashboard'u
- `books.html` - Kitap listesi ve arama
- `my-books.html` - Ödünç kitaplar ve cezalar
- `admin.html` - Admin paneli

## Varsayılan Kullanıcı

- **E-posta**: admin@kutuphane.com
- **Şifre**: admin123

## Test

API'leri test etmek için Postman veya Swagger kullanabilirsiniz. Tüm endpoint'ler JWT token gerektirir (login ve register hariç).

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

