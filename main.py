import scraper
import database
import time

if __name__ == "__main__":

    print("--- BKM Kitap Scraper Başlatıldı ---")

    print("\n[1/3] Veritabanı kontrol ediliyor/hazırlanıyor...")
    database.init_db()

    print("\n[2/3] Web sitesinden veriler çekiliyor...")
    tum_kitaplar = []

    for sayfa_numarasi in range(1, 13):
        print(f"Şimdiye kadar toplam {len(tum_kitaplar)} adet kitap çekildi.")
        url = f"https://www.bkmkitap.com/kitap/cok-satan-kitaplar?ps={sayfa_numarasi}"
        print(f"-> Sayfa {sayfa_numarasi} taranıyor...")
        kitaplar_bu_sayfadan = scraper.scrape_bkm_kitap(url)

        if kitaplar_bu_sayfadan:
            tum_kitaplar.extend(kitaplar_bu_sayfadan)

        time.sleep(1)

    print(f"Toplam {len(tum_kitaplar)} adet kitap çekildi.")

    if tum_kitaplar:
        print("\n[3/3] Veriler veritabanına kaydediliyor...")
        database.save_books(tum_kitaplar)
    else:
        print("\n[3/3] Kaydedilecek yeni veri bulunamadı.")

    print("\n--- Operasyon Başarıyla Tamamlandı! ---")