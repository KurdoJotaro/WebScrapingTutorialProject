import requests
import csv
from bs4 import BeautifulSoup

def scrape_bkm_kitap(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers) #İstek
        response.raise_for_status() #Kontrol
        soup = BeautifulSoup(response.content, 'html.parser') #Veri İşleme
        booksDataList = []
        book_containers = soup.find_all(class_='product-item')
        print(f"Veri Çekimi Başarılı. Sayfada {len(book_containers)} adet kitap bulundu. Veriler İşleniyor...")

        for container in book_containers:
            kitap_adi= container.find(class_='product-title')
            kitapAdi = kitap_adi.text.strip() if kitap_adi else 'Kitap İsmi Bulunamadı.'

            kitap_yazari = container.find(class_='model-title')
            yazar = kitap_yazari.text.strip() if kitap_yazari else 'Kitap Yazari Bulunamadı.'

            kitap_yayinevi = container.find(class_='brand-title')
            yayinevi = kitap_yayinevi.text.strip() if kitap_yayinevi else 'Kitap Yayinevi Bulunamadı.'

            kitap_indirimsizFiyati = container.find(class_='product-price-not-discounted')
            indirimsizFiyat = kitap_indirimsizFiyati.text.strip() if kitap_indirimsizFiyati else 'İndirimsiz Fiyat Bulunamadi.'
            indirimsizFiyat_Temizlik =indirimsizFiyat.replace(',', '.')

            kitap_indirimOrani = container.find(class_='product-discount')
            indirimOrani = kitap_indirimOrani.text.strip() if kitap_indirimOrani else 'İndirim Orani Bulunamadi.'
            indirimOrani_Temizlik =indirimOrani.replace('%', '')

            kitap_indirimliSonFiyati = container.find(class_='product-price')
            indirimliFiyat = kitap_indirimliSonFiyati.text.strip() if kitap_indirimliSonFiyati else 'İndirimli Fiyat Bulunamadi.'
            indirimliFiyat_Temizlik =indirimliFiyat.replace(',', '.')

            kitap_bilgileri = {
                'Kitap Adı': kitapAdi,
                'Kitap Yazarı': yazar,
               'Yayınevi': yayinevi,
               'İndirimsiz Fiyat': indirimsizFiyat_Temizlik,
               'İndirim Oranı': indirimOrani_Temizlik,
               'İndirimli Fiyat': indirimliFiyat_Temizlik
            }

            booksDataList.append(kitap_bilgileri)
        return booksDataList

    except requests.exceptions.RequestException as e:
        print(f"Siteye bağlanırken bir hata oluştu: {e}")
        return []


"""--- TEST BLOĞU ---"""
# --- scraper.py dosyasının en altına eklenecek YENİ TEST BLOĞU ---

# time modülünü ekliyoruz. Sayfalar arasında küçük bir bekleme yapmak için.
import time

if __name__ == "__main__":

    # 1. Adım: Tüm sayfalardan gelen kitapları toplayacağımız ana listeyi oluşturalım.
    tum_kitaplar = []

    # 2. Adım: 1'den 12'ye kadar olan tüm sayfa numaraları için bir döngü başlatalım.
    # range(1, 13) 1'den başlar, 13'e kadar gider (13 dahil değil).
    for sayfa_numarasi in range(1, 13):

        # 3. Adım: O anki sayfa numarasına göre doğru URL'i oluşturalım.
        url = f"https://www.bkmkitap.com/kitap/cok-satan-kitaplar?ps={sayfa_numarasi}"
        print(f"\n---> Sayfa {sayfa_numarasi} taranıyor: {url}")

        # 4. Adım: Scraper fonksiyonumuzu bu URL ile çağıralım.
        kitaplar_bu_sayfadan = scrape_bkm_kitap(url)

        # 5. Adım: Eğer o sayfadan kitap geldiyse, ana listemize ekleyelim.
        if kitaplar_bu_sayfadan:
            # .extend(), bir listeyi diğerinin sonuna ekler.
            tum_kitaplar.extend(kitaplar_bu_sayfadan)
            print(
                f"Bu sayfadan {len(kitaplar_bu_sayfadan)} kitap bulundu. Ana listede toplam {len(tum_kitaplar)} kitap var.")
        else:
            print("Bu sayfadan veri çekilemedi. Döngü devam ediyor...")

        # 6. Adım: Sunucuyu yormamak için her istek arasında 1 saniye bekleyelim.
        # Bu, "kibar bir scraper" olmanın en önemli kuralıdır.
        time.sleep(1)

    # 7. Adım: Döngü bittikten sonra genel sonucu yazdıralım.
    if tum_kitaplar:
        print(f"\n\n---> TARAMA TAMAMLANDI! TOPLAM {len(tum_kitaplar)} KİTAP BİLGİSİ ÇEKİLDİ! <---")
        from pprint import pprint

        print("\n--- İlk Kitabın Bilgileri ---")
        pprint(tum_kitaplar[0])
        print("\n--- Son Kitabın Bilgileri ---")
        pprint(tum_kitaplar[-1])
    else:
        print("\n\n---> TARAMA BAŞARISIZ! Hiçbir sayfadan veri çekilemedi. <---")

with open("bkm_kitaplar.csv", "w", newline="", encoding="utf-8-sig") as f:
    basliklar = tum_kitaplar[0].keys()
    writer = csv.DictWriter(f, fieldnames=basliklar, delimiter=';')
    writer.writeheader()
    writer.writerows(tum_kitaplar)

print("\nVeriler 'bkm_kitaplar.csv' dosyasına kaydedildi.")