-- Akıllı Kütüphane Yönetim Sistemi - DÜZELTİLMİŞ ŞEMA
-- Bu script, Python koduyla tam uyumlu ve döngüsel (cycle) hatalarından arındırılmıştır.

USE master;
GO

-- Eğer veritabanı varsa önce bağlantıları kopar, sonra sil (Temiz başlangıç için)
IF EXISTS (SELECT * FROM sys.databases WHERE name = 'KutuphaneDB')
BEGIN
    ALTER DATABASE KutuphaneDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE KutuphaneDB;
END
GO

CREATE DATABASE KutuphaneDB;
GO

USE KutuphaneDB;
GO

-- 1. KATEGORİLER TABLOSU
CREATE TABLE Kategoriler (
    KategoriID INT PRIMARY KEY IDENTITY(1,1),
    KategoriAdi NVARCHAR(100) NOT NULL UNIQUE,
    Aciklama NVARCHAR(500),
    OlusturmaTarihi DATETIME DEFAULT GETDATE()
);
GO

-- 2. YAZARLAR TABLOSU
CREATE TABLE Yazarlar (
    YazarID INT PRIMARY KEY IDENTITY(1,1),
    Ad NVARCHAR(50) NOT NULL,
    Soyad NVARCHAR(50) NOT NULL,
    DogumTarihi DATE,
    Ulke NVARCHAR(50),
    Biyografi NVARCHAR(1000),
    OlusturmaTarihi DATETIME DEFAULT GETDATE()
);
GO

-- 3. KULLANICILAR TABLOSU
CREATE TABLE Kullanıcılar (
    KullaniciID INT PRIMARY KEY IDENTITY(1,1),
    Ad NVARCHAR(50) NOT NULL,
    Soyad NVARCHAR(50) NOT NULL,
    EPosta NVARCHAR(100) NOT NULL UNIQUE,
    Sifre NVARCHAR(255) NOT NULL,
    Rol NVARCHAR(20) NOT NULL CHECK (Rol IN ('Admin', 'Uye')),
    Telefon NVARCHAR(20),
    Adres NVARCHAR(500),
    Aktif BIT DEFAULT 1,
    OlusturmaTarihi DATETIME DEFAULT GETDATE()
);
GO

-- 4. KİTAPLAR TABLOSU
CREATE TABLE Kitaplar (
    KitapID INT PRIMARY KEY IDENTITY(1,1),
    Baslik NVARCHAR(200) NOT NULL,
    ISBN NVARCHAR(20) UNIQUE,
    YayinYili INT,
    SayfaSayisi INT,
    MevcutKopyaSayisi INT DEFAULT 0,
    ToplamKopyaSayisi INT DEFAULT 0,
    KategoriID INT,
    YayinEvi NVARCHAR(100),
    Dil NVARCHAR(20) DEFAULT 'Türkçe',
    Aciklama NVARCHAR(1000),
    OlusturmaTarihi DATETIME DEFAULT GETDATE(),
    -- Kategori silinirse kitap silinmesin, KategoriID NULL olsun
    FOREIGN KEY (KategoriID) REFERENCES Kategoriler(KategoriID) ON DELETE SET NULL
);
GO

-- 5. KİTAP-YAZAR İLİŞKİ TABLOSU
CREATE TABLE KitapYazarlar (
    KitapYazarID INT PRIMARY KEY IDENTITY(1,1),
    KitapID INT NOT NULL,
    YazarID INT NOT NULL,
    FOREIGN KEY (KitapID) REFERENCES Kitaplar(KitapID) ON DELETE CASCADE,
    FOREIGN KEY (YazarID) REFERENCES Yazarlar(YazarID) ON DELETE CASCADE,
    UNIQUE(KitapID, YazarID)
);
GO

-- 6. ÖDÜNÇ İŞLEMLERİ TABLOSU (Python modeliyle uyumlu isimler)
CREATE TABLE OduncIslemleri (
    OduncID INT PRIMARY KEY IDENTITY(1,1),
    KullaniciID INT NOT NULL,
    KitapID INT NOT NULL,

    -- İsim düzeltmeleri:
    OduncTarihi DATETIME NOT NULL DEFAULT GETDATE(),  -- Eskisi: OduncAlmaTarihi
    IadeTarihi DATETIME,
    SonTeslimTarihi DATETIME NOT NULL,                -- Eskisi: BeklenenIadeTarihi

    Durum NVARCHAR(20) DEFAULT 'Aktif' CHECK (Durum IN ('Aktif', 'IadeEdildi', 'Gecikmis')),

    FOREIGN KEY (KullaniciID) REFERENCES Kullanıcılar(KullaniciID) ON DELETE CASCADE,
    FOREIGN KEY (KitapID) REFERENCES Kitaplar(KitapID) ON DELETE CASCADE
);
GO

-- 7. CEZALAR TABLOSU (Cycle Hatası Düzeltildi)
CREATE TABLE Cezalar (
    CezaID INT PRIMARY KEY IDENTITY(1,1),
    KullaniciID INT NOT NULL,
    OduncID INT,

    -- İsim düzeltmeleri:
    Tutar DECIMAL(10,2) NOT NULL DEFAULT 0, -- Eskisi: CezaMiktari
    Aciklama NVARCHAR(200),                 -- Eskisi: CezaNedeni

    Durum NVARCHAR(20) DEFAULT 'Beklemede' CHECK (Durum IN ('Beklemede', 'Odendi', 'Iptal')),
    OlusturmaTarihi DATETIME DEFAULT GETDATE(),
    OdenenTarih DATETIME,                   -- Eskisi: OdemeTarihi

    -- CRITICAL FIX: Cycle hatasını önlemek için Kullanıcı silindiğinde Ceza silinmesin (NO ACTION)
    -- Mantık: Zaten kullanıcıyı silmeden önce borçlarını kontrol etmeliyiz.
    FOREIGN KEY (KullaniciID) REFERENCES Kullanıcılar(KullaniciID) ON DELETE NO ACTION,

    -- Ödünç kaydı silinirse cezadaki OduncID NULL olsun ama ceza kaydı kalsın
    FOREIGN KEY (OduncID) REFERENCES OduncIslemleri(OduncID) ON DELETE SET NULL
);
GO

-- 8. REZERVASYONLAR TABLOSU (Eksikti, eklendi)
CREATE TABLE Rezervasyonlar (
    RezervasyonID INT PRIMARY KEY IDENTITY(1,1),
    KullaniciID INT NOT NULL,
    KitapID INT NOT NULL,
    RezervasyonTarihi DATETIME DEFAULT GETDATE(),
    Durum NVARCHAR(20) DEFAULT 'Aktif', -- Aktif, Tamamlandi, Iptal

    FOREIGN KEY (KullaniciID) REFERENCES Kullanıcılar(KullaniciID) ON DELETE CASCADE,
    FOREIGN KEY (KitapID) REFERENCES Kitaplar(KitapID) ON DELETE CASCADE
);
GO

-- İNDEKSLER
CREATE NONCLUSTERED INDEX IX_Kitaplar_KategoriID ON Kitaplar(KategoriID);
CREATE NONCLUSTERED INDEX IX_OduncIslemleri_KullaniciID ON OduncIslemleri(KullaniciID);
CREATE NONCLUSTERED INDEX IX_OduncIslemleri_Durum ON OduncIslemleri(Durum);
CREATE NONCLUSTERED INDEX IX_Cezalar_KullaniciID ON Cezalar(KullaniciID);
GO

-- --- TRIGGERLAR (Yeni Sütun İsimlerine Göre Güncellendi) ---

-- TRIGGER 1: Gecikme Cezası Hesapla
CREATE TRIGGER TRG_GecikmeCezaHesapla
ON OduncIslemleri
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Sadece iade edilen ve gecikmiş işlemler için
    IF UPDATE(IadeTarihi) AND EXISTS (
        SELECT 1 FROM inserted
        WHERE IadeTarihi IS NOT NULL
        AND IadeTarihi > SonTeslimTarihi -- İsim düzeltildi
        AND Durum = 'IadeEdildi'
    )
    BEGIN
        DECLARE @OduncID INT;
        DECLARE @KullaniciID INT;
        DECLARE @GecikmeGunu INT;
        DECLARE @Tutar DECIMAL(10,2);
        DECLARE @GunlukCeza DECIMAL(10,2) = 1.50; -- Günlük ceza miktarı (TL)

        DECLARE ceza_cursor CURSOR FOR
        SELECT
            i.OduncID,
            i.KullaniciID,
            DATEDIFF(DAY, i.SonTeslimTarihi, i.IadeTarihi) AS GecikmeGunu
        FROM inserted i
        WHERE i.IadeTarihi IS NOT NULL
        AND i.IadeTarihi > i.SonTeslimTarihi
        AND i.Durum = 'IadeEdildi'
        AND NOT EXISTS (
            SELECT 1 FROM Cezalar c
            WHERE c.OduncID = i.OduncID
        );

        OPEN ceza_cursor;
        FETCH NEXT FROM ceza_cursor INTO @OduncID, @KullaniciID, @GecikmeGunu;

        WHILE @@FETCH_STATUS = 0
        BEGIN
            SET @Tutar = @GecikmeGunu * @GunlukCeza;

            -- Yeni sütun isimleri kullanıldı (Tutar, Aciklama)
            INSERT INTO Cezalar (KullaniciID, OduncID, Tutar, Aciklama, Durum)
            VALUES (@KullaniciID, @OduncID, @Tutar,
                    'Geç iade: ' + CAST(@GecikmeGunu AS NVARCHAR) + ' gün gecikme',
                    'Beklemede');

            FETCH NEXT FROM ceza_cursor INTO @OduncID, @KullaniciID, @GecikmeGunu;
        END;

        CLOSE ceza_cursor;
        DEALLOCATE ceza_cursor;
    END;
END;
GO

-- TRIGGER 2: Kitap Ödünç Alındığında Stok Düşür
CREATE TRIGGER TRG_KitapOduncAlindi
ON OduncIslemleri
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Kitaplar
    SET MevcutKopyaSayisi = MevcutKopyaSayisi - 1
    WHERE KitapID IN (SELECT KitapID FROM inserted WHERE Durum = 'Aktif');
END;
GO

-- TRIGGER 3: Kitap İade Edildiğinde Stok Artır
CREATE TRIGGER TRG_KitapIadeEdildi
ON OduncIslemleri
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    IF UPDATE(Durum) AND EXISTS (SELECT 1 FROM inserted WHERE Durum = 'IadeEdildi')
    BEGIN
        UPDATE Kitaplar
        SET MevcutKopyaSayisi = MevcutKopyaSayisi + 1
        WHERE KitapID IN (
            SELECT i.KitapID
            FROM inserted i
            INNER JOIN deleted d ON i.OduncID = d.OduncID
            WHERE i.Durum = 'IadeEdildi' AND d.Durum = 'Aktif'
        );
    END;
END;
GO

-- --- VERİLER ---

-- Varsayılan Admin (Şifre: admin123 - Werkzeug/pbkdf2 uyumlu hash)
-- Not: create_admin.py çalıştırırsanız bu güncellenir, ama başlangıç için çalışsın diye ekliyoruz.
INSERT INTO Kullanıcılar (Ad, Soyad, EPosta, Sifre, Rol)
VALUES ('Süper', 'Admin', 'admin@kutuphane.com', 'pbkdf2:sha256:600000$Yq... (create_admin.py calistiriniz)', 'Admin');

-- Kategoriler
INSERT INTO Kategoriler (KategoriAdi, Aciklama) VALUES
('Roman', 'Roman türü kitaplar'),
('Bilim Kurgu', 'Bilim kurgu ve fantastik'),
('Tarih', 'Tarih kitapları'),
('Kişisel Gelişim', 'Kişisel gelişim kitapları');
GO