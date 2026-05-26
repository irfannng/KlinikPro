# 🏥 Çevrimiçi (Online) Doktor Randevu Sistemi

Bu proje, Python programlama dili kullanılarak **Nesne Yönelimli Programlama (OOP)** prensiplerine uygun olarak geliştirilmiş bir **Online Doktor Randevu Sistemi** konsol uygulamasıdır. Proje; hastaların, doktorların ve randevu süreçlerinin dinamik olarak yönetimini sağlar.

## ✨ Özellikler

* **Hasta Yönetimi:** Hasta kaydı oluşturma, TC Kimlik ve ad/telefon doğrulaması, hastaya ait randevu geçmişini tutma.
* **Doktor Yönetimi:** Doktor kaydı oluşturma, uzmanlık alanı belirleme ve doktor bazlı dinamik çalışma saatleri (takvim) yönetimi.
* **Akıllı Randevu Sistemi:** * Doktorun müsaitlik durumuna göre dinamik randevu oluşturma.
    * Randevu alındığında ilgili saatin doktorun takviminden otomatik olarak düşülmesi.
    * Randevu iptal edildiğinde saatin doktora otomatik olarak geri iade edilmesi ve hastanın geçmişinden silinmesi.
* **Raporlama:** Belirli bir tarihe ait tüm aktif randevuları saat sıralı ve okunaklı bir şekilde konsolda listeleme.
* **Konsol Menüsü:** Kullanıcı dostu, yönlendirmeli ve hata kontrolleri yapılmış interaktif terminal arayüzü.

---

## 🛠️ Kullanılan Teknolojiler ve Modüller

* **Dil:** Python 3.10+
* **Yerleşik Modüller:**
    * `datetime` (`date`, `datetime`): Tarih ve saat manipülasyonları için.
    * `typing` (`Optional`): Tip ipuçları (Type Hinting) ile daha güvenli bir kod yapısı için.

---

## 🏗️ Kod Yapısı ve Sınıflar (Architecture)

Proje, sorumlulukların ayrılması (Separation of Concerns) prensibine uygun olarak 4 temel sınıftan oluşur:

1.  **`Hasta`**: Hastanın kişisel bilgilerini tutar ve randevu alma süreçlerini yönetir.
2.  **`Doktor`**: Doktorun uzmanlık ve müsait olduğu tarih/saat bilgilerini saklar, takvim güncellemelerini yapar.
3.  **`Randevu`**: Hasta ve doktor arasındaki eşleşmeyi, randevunun aktiflik durumunu kontrol eder. İptal ve oluşturma lojistiğini yönetir.
4.  **`RandevuSistemi`**: Tüm sistemi birbirine bağlayan, veri tabanı gibi davranan ve yönetimsel (kayıt, listeleme) fonksiyonları barındıran ana yöneticidir.

---

## 🚀 Başlangıç ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları takip edebilirsiniz.

### Gereksinimler
Proje herhangi bir harici kütüphaneye ihtiyaç duymaz, standart Python yüklemesi yeterlidir.

### Çalıştırma Adımları

1. Proje dosyalarının bulunduğu dizine gidin:
   ```bash
   cd /proje-yolu/
