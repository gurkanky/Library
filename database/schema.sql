-- Akıllı Kütüphane Yönetim Sistemi Veritabanı Şeması
-- MSSQL Database Schema

-- Veritabanı oluştur
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'KutuphaneDB')
BEGIN
    CREATE DATABASE KutuphaneDB;
END
GO

USE KutuphaneDB;
GO

-- Kategoriler Tablosu
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Kategoriler]') AND type in (N'U'))
BEGIN
    CREATE TABLE Kategoriler (
        KategoriID INT PRIMARY KEY IDENTITY(1,1),
        KategoriAdi NVARCHAR(100) NOT NULL UNIQUE,
        Aciklama NVARCHAR(500),
        OlusturmaTarihi DATETIME DEFAULT GETDATE()
    );
END
GO

-- Yazarlar Tablosu
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Yazarlar]') AND type in (N'U'))
BEGIN
    CREATE TABLE Yazarlar (
        YazarID INT PRIMARY KEY IDENTITY(1,1),
        Ad NVARCHAR(50) NOT NULL,
        Soyad NVARCHAR(50) NOT NULL,
        DogumTarihi DATE,
        Ulke NVARCHAR(50),
        Biyografi NVARCHAR(1000),
        OlusturmaTarihi DATETIME DEFAULT GETDATE()
    );
END
GO

-- Kullanıcılar Tablosu (Admin ve Üye için ortak tablo)
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Kullanıcılar]') AND type in (N'U'))
BEGIN
    CREATE TABLE Kullanıcılar (
        KullaniciID INT PRIMARY KEY IDENTITY(1,1),
        Ad NVARCHAR(50) NOT NULL,
        Soyad NVARCHAR(50) NOT NULL,
        EPosta NVARCHAR(100) NOT NULL UNIQUE,
        Sifre NVARCHAR(255) NOT NULL, -- Hash'lenmiş şifre
        Rol NVARCHAR(20) NOT NULL CHECK (Rol IN ('Admin', 'Uye')),
        Telefon NVARCHAR(20),
        Adres NVARCHAR(500),
        Aktif BIT DEFAULT 1,
        OlusturmaTarihi DATETIME DEFAULT GETDATE()
    );
END
GO

-- Kitaplar Tablosu
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Kitaplar]') AND type in (N'U'))
BEGIN
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
        FOREIGN KEY (KategoriID) REFERENCES Kategoriler(KategoriID) ON DELETE SET NULL
    );
END
GO

-- Kitap-Yazar İlişki Tablosu (Çoktan-Çoğa)
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[KitapYazarlar]') AND type in (N'U'))
BEGIN
    CREATE TABLE KitapYazarlar (
        KitapYazarID INT PRIMARY KEY IDENTITY(1,1),
        KitapID INT NOT NULL,
        YazarID INT NOT NULL,
        FOREIGN KEY (KitapID) REFERENCES Kitaplar(KitapID) ON DELETE CASCADE,
        FOREIGN KEY (YazarID) REFERENCES Yazarlar(YazarID) ON DELETE CASCADE,
        UNIQUE(KitapID, YazarID)
    );
END
GO

-- Ödünç Verme İşlemleri Tablosu
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[OduncIslemleri]') AND type in (N'U'))
BEGIN
    CREATE TABLE OduncIslemleri (
        OduncID INT PRIMARY KEY IDENTITY(1,1),
        KullaniciID INT NOT NULL,
        KitapID INT NOT NULL,
        OduncAlmaTarihi DATETIME NOT NULL DEFAULT GETDATE(),
        IadeTarihi DATETIME,
        BeklenenIadeTarihi DATETIME NOT NULL,
        Durum NVARCHAR(20) DEFAULT 'Aktif' CHECK (Durum IN ('Aktif', 'IadeEdildi', 'Gecikmis')),
        Notlar NVARCHAR(500),
        FOREIGN KEY (KullaniciID) REFERENCES Kullanıcılar(KullaniciID) ON DELETE CASCADE,
        FOREIGN KEY (KitapID) REFERENCES Kitaplar(KitapID) ON DELETE CASCADE
    );
END
GO

-- Ceza Tablosu
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Cezalar]') AND type in (N'U'))
BEGIN
    CREATE TABLE Cezalar (
        CezaID INT PRIMARY KEY IDENTITY(1,1),
        KullaniciID INT NOT NULL,
        OduncID INT,
        CezaMiktari DECIMAL(10,2) NOT NULL DEFAULT 0,
        CezaNedeni NVARCHAR(200),
        Durum NVARCHAR(20) DEFAULT 'Beklemede' CHECK (Durum IN ('Beklemede', 'Odendi', 'Iptal')),
        OlusturmaTarihi DATETIME DEFAULT GETDATE(),
        OdemeTarihi DATETIME,
        FOREIGN KEY (KullaniciID) REFERENCES Kullanıcılar(KullaniciID) ON DELETE CASCADE,
        FOREIGN KEY (OduncID) REFERENCES OduncIslemleri(OduncID) ON DELETE SET NULL
    );
END
GO

-- İndeksler
CREATE NONCLUSTERED INDEX IX_Kitaplar_KategoriID ON Kitaplar(KategoriID);
CREATE NONCLUSTERED INDEX IX_OduncIslemleri_KullaniciID ON OduncIslemleri(KullaniciID);
CREATE NONCLUSTERED INDEX IX_OduncIslemleri_KitapID ON OduncIslemleri(KitapID);
CREATE NONCLUSTERED INDEX IX_OduncIslemleri_Durum ON OduncIslemleri(Durum);
CREATE NONCLUSTERED INDEX IX_Cezalar_KullaniciID ON Cezalar(KullaniciID);
GO

-- TRIGGER: Geç iade edilen kitaplar için otomatik ceza hesaplama
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[TRG_GecikmeCezaHesapla]') AND type = 'TR')
    DROP TRIGGER TRG_GecikmeCezaHesapla;
GO

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
        AND IadeTarihi > BeklenenIadeTarihi
        AND Durum = 'IadeEdildi'
    )
    BEGIN
        DECLARE @OduncID INT;
        DECLARE @KullaniciID INT;
        DECLARE @GecikmeGunu INT;
        DECLARE @CezaMiktari DECIMAL(10,2);
        DECLARE @GunlukCeza DECIMAL(10,2) = 0.50; -- Günlük ceza miktarı
        
        DECLARE ceza_cursor CURSOR FOR
        SELECT 
            i.OduncID,
            i.KullaniciID,
            DATEDIFF(DAY, i.BeklenenIadeTarihi, i.IadeTarihi) AS GecikmeGunu
        FROM inserted i
        WHERE i.IadeTarihi IS NOT NULL 
        AND i.IadeTarihi > i.BeklenenIadeTarihi
        AND i.Durum = 'IadeEdildi'
        AND NOT EXISTS (
            SELECT 1 FROM Cezalar c 
            WHERE c.OduncID = i.OduncID
        );
        
        OPEN ceza_cursor;
        FETCH NEXT FROM ceza_cursor INTO @OduncID, @KullaniciID, @GecikmeGunu;
        
        WHILE @@FETCH_STATUS = 0
        BEGIN
            SET @CezaMiktari = @GecikmeGunu * @GunlukCeza;
            
            INSERT INTO Cezalar (KullaniciID, OduncID, CezaMiktari, CezaNedeni, Durum)
            VALUES (@KullaniciID, @OduncID, @CezaMiktari, 
                    'Geç iade: ' + CAST(@GecikmeGunu AS NVARCHAR) + ' gün gecikme', 
                    'Beklemede');
            
            FETCH NEXT FROM ceza_cursor INTO @OduncID, @KullaniciID, @GecikmeGunu;
        END;
        
        CLOSE ceza_cursor;
        DEALLOCATE ceza_cursor;
    END;
END;
GO

-- TRIGGER: Kitap ödünç alındığında mevcut kopya sayısını azalt
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[TRG_KitapOduncAlindi]') AND type = 'TR')
    DROP TRIGGER TRG_KitapOduncAlindi;
GO

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

-- TRIGGER: Kitap iade edildiğinde mevcut kopya sayısını artır
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[TRG_KitapIadeEdildi]') AND type = 'TR')
    DROP TRIGGER TRG_KitapIadeEdildi;
GO

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

-- STORED PROCEDURE: Geç iade edilen kitapları kontrol et ve güncelle
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[SP_GecikmisOduncKontrol]') AND type = 'P')
    DROP PROCEDURE SP_GecikmisOduncKontrol;
GO

CREATE PROCEDURE SP_GecikmisOduncKontrol
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Gecikmiş işlemleri güncelle
    UPDATE OduncIslemleri
    SET Durum = 'Gecikmis'
    WHERE Durum = 'Aktif'
    AND GETDATE() > BeklenenIadeTarihi;
    
    -- Gecikmiş işlemlerin sayısını döndür
    SELECT COUNT(*) AS GecikmisSayisi
    FROM OduncIslemleri
    WHERE Durum = 'Gecikmis';
END;
GO

-- STORED PROCEDURE: Kullanıcının ödünç aldığı kitapları listele
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[SP_KullaniciOduncListesi]') AND type = 'P')
    DROP PROCEDURE SP_KullaniciOduncListesi;
GO

CREATE PROCEDURE SP_KullaniciOduncListesi
    @KullaniciID INT
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        o.OduncID,
        k.KitapID,
        k.Baslik,
        k.ISBN,
        o.OduncAlmaTarihi,
        o.BeklenenIadeTarihi,
        o.IadeTarihi,
        o.Durum,
        CASE 
            WHEN o.Durum = 'Aktif' AND GETDATE() > o.BeklenenIadeTarihi 
            THEN DATEDIFF(DAY, o.BeklenenIadeTarihi, GETDATE())
            ELSE 0
        END AS GecikmeGunu
    FROM OduncIslemleri o
    INNER JOIN Kitaplar k ON o.KitapID = k.KitapID
    WHERE o.KullaniciID = @KullaniciID
    ORDER BY o.OduncAlmaTarihi DESC;
END;
GO

-- STORED PROCEDURE: Kullanıcının toplam borcunu hesapla
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[SP_KullaniciToplamBorc]') AND type = 'P')
    DROP PROCEDURE SP_KullaniciToplamBorc;
GO

CREATE PROCEDURE SP_KullaniciToplamBorc
    @KullaniciID INT,
    @ToplamBorc DECIMAL(10,2) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT @ToplamBorc = ISNULL(SUM(CezaMiktari), 0)
    FROM Cezalar
    WHERE KullaniciID = @KullaniciID
    AND Durum = 'Beklemede';
END;
GO

-- Varsayılan veriler ekle
-- Varsayılan Admin kullanıcı (şifre: admin123 - hash'lenmiş olmalı)
IF NOT EXISTS (SELECT 1 FROM Kullanıcılar WHERE EPosta = 'admin@kutuphane.com')
BEGIN
    INSERT INTO Kullanıcılar (Ad, Soyad, EPosta, Sifre, Rol)
    VALUES ('Admin', 'Kullanıcı', 'admin@kutuphane.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqB5J5X5X2', 'Admin');
    -- Şifre: admin123 (bcrypt hash)
END
GO

-- Örnek kategoriler
IF NOT EXISTS (SELECT 1 FROM Kategoriler WHERE KategoriAdi = 'Roman')
BEGIN
    INSERT INTO Kategoriler (KategoriAdi, Aciklama) VALUES
    ('Roman', 'Roman türü kitaplar'),
    ('Bilim Kurgu', 'Bilim kurgu türü kitaplar'),
    ('Tarih', 'Tarih kitapları'),
    ('Biyografi', 'Biyografi kitapları'),
    ('Felsefe', 'Felsefe kitapları');
END
GO

