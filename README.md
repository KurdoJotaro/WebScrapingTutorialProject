# BKM Kitap - Çok Satanlar Scraper Projesi

KESİNLİKLEYAPAYZEKATARAFINDANYAZILMIŞTIR

Bu proje, Python kullanılarak BKM Kitap web sitesinin "Çok Satanlar" bölümünden kitap verilerini çekmek için geliştirilmiştir. Proje, sitenin sayfalandırma (pagination) yapısını takip ederek birden fazla sayfayı tarayabilir ve topladığı verileri temizleyerek yapılandırılmış bir formatta sunar.

## Temel Yetenekler

Bu proje aşağıdaki yetenekleri sergilemektedir:

- requests ve BeautifulSoup ile web scraping.

- Birden fazla sayfayı tarayabilen bir scraper mantığı.

- Çekilen ham veriyi (fiyat, indirim oranı vb.) temizleme ve işleme.

- Hata yönetimi (try...except).

- Modüler ve test edilebilir bir yapı (scraper.py).

- Proje bağımlılıklarını requirements.txt ile yönetme.

## Kurulum ve Çalıştırma

1. Bu depoyu bilgisayarınıza klonlayın (git clone).

2. Proje klasöründe bir sanal ortam (venv) oluşturup aktif hale getirin.

3. Aşağıdaki komut ile gerekli kütüphaneleri kurun:

  ```bash

  pip install -r requirements.txt

  ```

4. scraper.py modülünü doğrudan çalıştırarak veri çekme ve CSV'ye kaydetme işlemini test edebilirsiniz:

  ```bash

  python scraper.py

  ```

  Bu komut, verileri çekecek ve proje klasöründe bkm\_kitaplar.csv adında bir dosya oluşturacaktır.
