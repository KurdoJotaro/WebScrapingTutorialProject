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
        print(f"Veri hatası: Beklenen {e} anahtarı sözlükte bulunamadı. Lütfen scraper.py dosyasını kontrol edin."),

def search_books(search_term, search_field="Kitap Adı"):

    conn = None  # Bağlantıyı başta None olarak tanımlamak iyi bir pratiktir.
    try:
        conn = sqlite3.connect('kitaplar.db')
        cursor = conn.cursor()

        # SQL Injection'a karşı KESİNLİKLE parametreli sorgu kullanmalıyız!
        # Sütun adını doğrudan sorguya eklemek tehlikelidir, bu yüzden kontrol listesi yapıyoruz.
        allowed_fields = ["[Kitap Adı]", "[Kitap Yazarı]", "[Yayınevi]"]
        if search_field not in allowed_fields:
            print(
                f"Hata: Geçersiz arama alanı '{search_field}'. Sadece {allowed_fields} alanlarında arama yapılabilir.")
            return []

        # Arama teriminin başına ve sonuna % ekleyerek kısmi eşleşmeleri sağlıyoruz.
        query_term = f"%{search_term}%"

        # Sütun adını güvenli bir şekilde sorguya ekliyoruz (f-string burada riskli olabilir,
        # ama kontrol listesi ile riski azalttık). Daha güvenli yöntemler de var
        # ama bu seviye için bu kontrol yeterli.
        # ÖNEMLİ: f-string içine doğrudan kullanıcı girdisi koymak normalde GÜVENLİK RİSKİDİR.
        # Burada sadece izin verilen 3 sütun adından biri olduğu için kullanıyoruz.
        query = f"SELECT * FROM kitaplar WHERE LOWER({search_field}) LIKE LOWER(?) ORDER BY id DESC"

        cursor.execute(query, (query_term,))

        rows = cursor.fetchall()

        # Sütun isimlerini alıyoruz (boşluklu isimlerle çalışacak)
        columns = [description[0] for description in cursor.description]

        conn.close()

        books_list = []
        for row in rows:
            books_list.append(dict(zip(columns, row)))

        print(f"'{search_term}' araması için '{search_field}' alanında {len(books_list)} sonuç bulundu.")
        return books_list

    except sqlite3.Error as e:
        print(f"Veritabanında arama sırasında hata oluştu: {e}")
        return []
    finally:
        # Hata olsa bile bağlantı açıksa kapatılmalı
        if conn:
            conn.close()