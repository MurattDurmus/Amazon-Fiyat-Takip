import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def tarayiciyi_hazirla():
    """Gerçek kullanıcıyı taklit eden Chrome tarayıcısı başlatır."""
    chrome_ayarlari = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    chrome_ayarlari.add_argument(f"user-agent={user_agent}")
    chrome_ayarlari.add_argument("--start-maximized")
    chrome_ayarlari.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_ayarlari.add_experimental_option('useAutomationExtension', False)
    chrome_ayarlari.add_argument("--disable-blink-features=AutomationControlled")
    
    servis = Service(ChromeDriverManager().install())
    tarayici = webdriver.Chrome(service=servis, options=chrome_ayarlari)
    tarayici.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return tarayici


def cerezleri_kabul_et(driver):
    """Ekranda çerez onay penceresi çıkarsa tıklar, çıkmazsa devam eder."""
    try:
        cerez_butonu = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "sp-cc-accept"))
        )
        cerez_butonu.click()
        print("-> Çerez bildirimi onaylandı.")
    except Exception:
        # Çerez penceresi çıkmadıysa hata vermeden devam etsin
        pass


def amazon_urun_topla(arama_kelimesi, max_sayfa=1):
    """
    Amazon'da arama yapar, ürünlerin adını, fiyatını ve linkini toplayıp
    bir CSV dosyasına kaydeder.
    """
    driver = tarayiciyi_hazirla()
    bekle = WebDriverWait(driver, 10)
    toplanan_urunler = []

    try:
        print(f"'{arama_kelimesi}' için arama başlatılıyor...")
        driver.get("https://www.amazon.com.tr")
        
        # 1. Çerezleri temizle
        cerezleri_kabul_et(driver)
        
        # 2. Arama kutusunu bul, kelimeyi yaz ve Enter'a bas
        arama_kutusu = bekle.until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        arama_kutusu.clear()
        arama_kutusu.send_keys(arama_kelimesi)
        arama_kutusu.send_keys(Keys.RETURN)
        
        # 3. Sayfadaki ürün kartlarını topla
        print("Arama sonuçları taranıyor...")
        time.sleep(2) # Sayfanın oturması için kısa bir bekleme
        
        # Ürün kutuları genellikle bu veri niteliğine (data-component-type) sahiptir
        urun_kartlari = bekle.until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
        )
        
        print(f"Toplam bulunan ürün kartı sayısı: {len(urun_kartlari)}")
        
        for kart in urun_kartlari:
            # Ürün Adı
            try:
                baslik_etiketi = kart.find_element(By.XPATH, ".//h2//span")
                urun_adi = baslik_etiketi.text.strip()
            except Exception:
                urun_adi = "Başlık Yok"
                
            # Ürün Fiyatı
            try:
                # Amazon'da fiyat tam kısım ve kuruş kısmı ayrı tutulabilir
                fiyat_tam = kart.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
                fiyat_kesir = kart.find_element(By.XPATH, ".//span[@class='a-price-fraction']").text
                fiyat = f"{fiyat_tam},{fiyat_kesir} TL"
            except Exception:
                # Fiyatı olmayan veya stokta tükenmiş ürünler
                fiyat = "Fiyat Belirtilmemiş"

            # Ürün Linki
            try:
                link_etiketi = kart.find_element(By.XPATH, ".//h2/a")
                urun_linki = link_etiketi.get_attribute("href")
            except Exception:
                urun_linki = "Link Yok"
            
            # Eğer ürün adı varsa listemize ekleyelim
            if urun_adi != "Başlık Yok":
                toplanan_urunler.append({
                    "Ürün Adı": urun_adi,
                    "Fiyat": fiyat,
                    "Ürün Linki": urun_linki
                })

        print(f"\nBaşarıyla toplanan ürün sayısı: {len(toplanan_urunler)}")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

    finally:
        # Tarayıcıyı mutlaka güvenli şekilde kapat
        driver.quit()
        print("Tarayıcı kapatıldı.")

    # 4. Verileri DataFrame yapıp CSV'ye dökme
    if toplanan_urunler:
        df = pd.DataFrame(toplanan_urunler)
        dosya_adi = f"{arama_kelimesi}_fiyatlari.csv"
        df.to_csv(dosya_adi, index=False, encoding="utf-8-sig")
        print(f"\nVeriler başarıyla kaydedildi: '{dosya_adi}'")
    else:
        print("Kaydedilecek ürün bulunamadı.")


if __name__ == "__main__":
    # Test için aranacak kelime:
    ARANACAK_URUN = "python programlama"
    amazon_urun_topla(ARANACAK_URUN)