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


    print("\n--- Arama Adımı ---")

    while True:
        arama_terimi = input("Aramak istediğiniz kelimeyi girin (Çıkmak için 'q'): ")
        if arama_terimi.lower() == 'q':
            break

        print("Arama yapılacak alanlar:")
        print("1: Kitap Adı")
        print("2: Kitap Yazarı")
        print("3: Yayınevi")
        secim = input("Lütfen arama yapmak istediğiniz alanın numarasını girin (Varsayılan: 1): ")

        arama_alani = "[Kitap Adı]"  # Varsayılan
        if secim == '2':
            arama_alani = "[Kitap Yazarı]"
        elif secim == '3':
            arama_alani = "[Yayınevi]"

        # database modülümüzdeki yeni arama fonksiyonunu çağırıyoruz.
        arama_sonuclari = database.search_books(search_term=arama_terimi, search_field=arama_alani)

        # Sonuçları yazdıralım
        if arama_sonuclari:
            print(f"\n--- '{arama_terimi}' için bulunan sonuçlar ({arama_alani}) ---")
            from pprint import pprint

            for kitap in arama_sonuclari:
                pprint(kitap)
                print("-" * 20)
        else:
            print(f"'{arama_terimi}' için '{arama_alani}' alanında sonuç bulunamadı.")

        print("\n" + "=" * 40 + "\n")  # Yeni arama için ayraç

    print("\n--- Operasyon Başarıyla Tamamlandı! ---")  # Bu satır en sonda kalacak.