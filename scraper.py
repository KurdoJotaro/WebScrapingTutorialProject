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