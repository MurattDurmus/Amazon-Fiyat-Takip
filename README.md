# 🛒 E-Ticaret Fiyat ve Ürün Takip Botu (Selenium)

Bu proje, Python ve Selenium kütüphanesi kullanılarak geliştirilmiş, anti-bot korumalarını minimize eden ve aranan ürünlerin verilerini toplayıp tablo (CSV) formatında dışa aktaran bir web scraping aracıdır.

## 🚀 Özellikler

* **Anti-Detection (Stealth):** `navigator.webdriver` bayrağını kapatır, özel User-Agent başlığı tanımlar ve otomasyon bayraklarını gizler.
* **Dinamik Bekleme (Explicit Waits):** `time.sleep` bağımlılığı olmadan, DOM elemanlarının yüklenmesini `WebDriverWait` ve `expected_conditions` ile takip eder.
* **Çerez Yönetimi:** Açılışta beliren çerez/izin bildirimlerini dinamik olarak saptayıp onaylar.
* **Veri Aktarımı:** Toplanan ürün adı, fiyat ve bağlantı verilerini `pandas` kullanarak UTF-8 formatında `.csv` dosyası olarak kaydeder.

## 🛠️ Kurulum

1. Projeyi bilgisayarınıza klonlayın:
   ```bash
   git clone [https://github.com/KULLANICI_ADINIZ/selenium-fiyat-botu.git](https://github.com/KULLANICI_ADINIZ/selenium-fiyat-botu.git)
   cd selenium-fiyat-botu