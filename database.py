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
                [İndirimli Fiyat] REAL
            )
        """)
        conn.commit()
        conn.close()
        print("Veritabanı 'kitaplar.db' başarıyla oluşturuldu/düzenlendi.")
    except sqlite3.Error as e:
        print(f"Veritabanı hatası oluştu: {e}")

def save_books(kitap_listesi):
    conn = sqlite3.connect('kitaplar.db')
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO kitaplar (
            [Kitap Adı], 
            [Kitap Yazarı], 
            [Yayınevi], 
            [İndirimsiz Fiyat], 
            [İndirim Oranı], 
            [İndirimli Fiyat]
        ) VALUES (?, ?, ?, ?, ?, ?)
    """
    for kitap in kitap_listesi:

        veri_demeti = (
            kitap['kitap_adi'],
            kitap['yazar'],
            kitap['yayinevi'],
            kitap['fiyat'],
            kitap['indirimsiz_fiyat'],
            kitap['indirim_orani']
        )
        print("Hazırlandı.")
        cursor.execute(insert_query, veri_demeti)

    print(f"Döngü tamamlandı. {len(kitap_listesi)} adet kitap veritabanına eklenmek üzere hazırlandı.")
    conn.commit()
    print("Tüm kitaplar eklendi.")
    conn.close()
    print("Veriler başarıyla kaydedildi ve veritabanı bağlantısı kapatıldı.")


# --- TEST BLOĞU ---
if __name__ == "__main__":
    print("1. AŞAMA: Veritabanı kurulum modülü test ediliyor...")
    init_db()
    print("2. AŞAMA: Veritabanının kitaplar.db'e aktarımı test ediliyor...")
    save_books(kitap_listesi=[])
