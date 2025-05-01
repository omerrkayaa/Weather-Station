# Hava Durumu İstasyonu Flask Uygulaması Dökümantasyonu

## Genel Bakış

Bu proje, Raspberry Pi üzerinde çalışan Flask tabanlı bir hava durumu istasyonu uygulamasıdır. Uygulama, sıcaklık, nem, atmosfer basıncı, rüzgar hızı ve yağmur tespiti gibi çevresel verileri ölçmek ve göstermek için çeşitli sensörleri entegre eder.

## Proje Yapısı

```
/proje_dizini
|-- app.py                # Ana Flask uygulaması
|-- templates
|   |-- index.html        # Ana sayfa şablonu (özelleştirilebilir)
|-- static                # CSS, JS veya resimler (gerekirse)
|-- requirements.txt      # Gerekli Python paketleri listesi
|-- my_env/               # Python sanal ortamı
```

---

## Kurulum Talimatları

### 1. Donanım Gereksinimleri

- Raspberry Pi 4 (veya benzeri)
- DHT22 Sensörü (Sıcaklık ve Nem)
- BMP280 Sensörü (Basınç ve İrtifa)
- ADS1115 ADC Modülü
- Anemometre (Rüzgar Hızı Sensörü)
- Yağmur Sensörü

### 2. Yazılım Gereksinimleri

- Python 3.7+
- Flask (web uygulaması için)
- Adafruit Sensör Kütüphaneleri
- RPi.GPIO (GPIO işlemleri için)
- Sanal ortam (bağımlılıkları izole etmek için önerilir)

---

## Sanal Ortam Nedir ve Neden Kullanılır?

Sanal ortam (virtual environment), Python projeleri için bağımsız bir çalışma alanıdır. Her sanal ortam, projenizin ihtiyaç duyduğu bağımlılıkları sistem genelinden izole eder ve yalnızca bu ortamda geçerli olan bir Python kurulumu sağlar.

### Sanal Ortam Kullanmanın Avantajları

- **Bağımsızlık**: Farklı projelerde farklı Python kütüphaneleri veya sürümleri kullanabilirsiniz.
- **Uyumluluk**: Projeniz, belirli bir Python sürümü veya kütüphane sürümüne bağlıysa, sanal ortamlar uyumsuzlukları önler.
- **Güvenlik**: Sistemdeki ana Python kurulumuna müdahale etmeden, yalnızca projeniz için gerekli olan kütüphaneleri yüklersiniz.
- **Kolay Yönetim**: Projenize ait bağımlılıkları kolayca yükleyebilir, kaldırabilir veya güncelleyebilirsiniz.

---

### 3. Sanal Ortam Kurulumu

```bash
sudo apt update
sudo apt install python3-venv python3-pip
python3 -m venv my_env
source my_env/bin/activate
pip install -r requirements.txt
```

Yukarıdaki komutlar, `my_env` adında bir sanal ortam oluşturur ve etkinleştirir. Bu ortam etkin olduğunda terminal satırında `(my_env)` ibaresi görünecektir. Ortamı devre dışı bırakmak için:

```bash
deactivate
```

---

### 4. Gerekli Kütüphanelerin Kurulumu

Aşağıdaki komutlarla gerekli kütüphaneleri tek tek kurabilirsiniz:
```bash
pip install Flask
pip install adafruit-circuitpython-dht
pip install adafruit-circuitpython-bmp280
pip install adafruit-circuitpython-ads1x15
pip install RPi.GPIO
```

---

## I2C ve GPIO Nedir?

- **I2C (Inter-Integrated Circuit)**: Birden fazla cihazın tek bir veri hattı (SDA) ve saat hattı (SCL) üzerinden haberleşmesini sağlayan bir protokoldür. Sensörler, ekranlar ve diğer modüller Raspberry Pi ile bu protokol aracılığıyla iletişim kurabilir.
- **GPIO (General Purpose Input Output)**: Raspberry Pi'nin dış dünya ile iletişim kurmasını sağlayan genel amaçlı giriş/çıkış pinleridir. Bu pinler, anahtarlar, sensörler ve diğer bileşenlerle etkileşim sağlar. Pinler giriş (input) veya çıkış (output) olarak yapılandırılabilir.

---

## Kod Açıklamaları (app.py)

### 1. İçe Aktarmalar

- **Flask**: Web sunucusu oluşturmak için çerçeve.
- **board** ve **busio**: Raspberry Pi'deki I2C ve GPIO pinlerini kullanmak için.
- **Adafruit kütüphaneleri**: BMP280, DHT22 ve ADS1115 sensörleriyle çalışmak için.
- **RPi.GPIO**: Yağmur sensöründen veri okumak için.

### 2. Sensör Başlatma

- **BMP280 (Basınç Sensörü)**:
  - Kod, sensörü iki olası I2C adresinde (0x76 veya 0x77) başlatmayı dener.
  - Deniz seviyesindeki basınç 1013.25 hPa olarak ayarlanır.
- **DHT22 (Sıcaklık ve Nem Sensörü)**: GPIO 27 pinine bağlanmıştır.
- **Yağmur Sensörü**: GPIO 17 pininde giriş olarak yapılandırılmıştır.
- **ADS1115 ve Anemometre**: Anemometreden gelen analog giriş ADS1115 üzerinden (P0 pini) okunur.

---

## Uygulamayı Çalıştırma

```bash
source my_env/bin/activate
python app.py
```

Web arayüzüne şu adresten erişin:

```
http://<raspberry_pi_ip>:5000/
```

Hava durumu API'sine şu adresten erişebilirsiniz:

```
http://<raspberry_pi_ip>:5000/api/weather
```
