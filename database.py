# database.py (NİHAİ VE DOĞRU HALİ)
import sqlite3


def init_db():
    try:
        conn = sqlite3.connect('kitaplar.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kitaplar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                [Kitap Adı] TEXT NOT NULL,
                [Kitap Yazarı] TEXT,
                [Yayınevi] TEXT,
                [İndirimsiz Fiyat] REAL,
                [İndirim Oranı] INTEGER,
                [İndirimli Fiyat] REAL,
                UNIQUE([Kitap Adı], [Kitap Yazarı])
            )
        """)
        conn.commit()
        conn.close()
        print("Veritabanı 'kitaplar.db' başarıyla oluşturuldu/kontrol edildi.")
    except sqlite3.Error as e:
        print(f"Veritabanı hatası oluştu: {e}")


def save_books(kitap_listesi):
    try:
        conn = sqlite3.connect('kitaplar.db')
        cursor = conn.cursor()

        insert_query = """
            INSERT OR IGNORE INTO kitaplar (
                [Kitap Adı], 
                [Kitap Yazarı], 
                [Yayınevi], 
                [İndirimsiz Fiyat], 
                [İndirim Oranı], 
                [İndirimli Fiyat]
            ) VALUES (?, ?, ?, ?, ?, ?)
        """

        data_to_insert = [
            (
                kitap['Kitap Adı'],
                kitap['Kitap Yazarı'],
                kitap['Yayınevi'],
                kitap['İndirimsiz Fiyat'],
                kitap['İndirim Oranı'],
                kitap['İndirimli Fiyat']
            )
            for kitap in kitap_listesi
        ]

        cursor.executemany(insert_query, data_to_insert)

        eklenen_kitap_sayisi = cursor.rowcount
        conn.commit()
        conn.close()

        print(f"İşlem tamamlandı. Veritabanına {eklenen_kitap_sayisi} yeni kitap eklendi.")

    except sqlite3.Error as e:
        print(f"Veritabanına kaydetme sırasında hata oluştu: {e}")
    except KeyError as e:
        print(f"Veri hatası: Beklenen {e} anahtarı sözlükte bulunamadı. Lütfen scraper.py dosyasını kontrol edin.")