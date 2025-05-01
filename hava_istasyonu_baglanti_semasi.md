
# **Hava İstasyonu - Bağlantı Şeması**  

## **1. Anemometre (Rüzgar Hız Sensörü)**  
- **Mavi kablo (GND)** → **ADS1115'in GND pini (Breadboard ortak GND hattı üzerinden)**  
- **Kahverengi kablo (Sinyal)** → **ADS1115'in A0 pini**  

## **2. Yağmur Sensörü**  
- **Beyaz kablo (VCC)** → **Raspberry Pi 4, 5V (Pin 2)**  
- **Siyah kablo (GND)** → **Raspberry Pi 4, GND (Pin 9)**  
- **Dijital sinyal kablosu** → **Raspberry Pi 4, GPIO17 (Pin 11)**  

## **3. DHT22 (Sıcaklık ve Nem Sensörü)**  
- **Gri kablo (GND)** → **Raspberry Pi 4, GND (Pin 14)**  
- **Beyaz kablo (OUT)** → **Raspberry Pi 4, GPIO27 (Pin 13)**  
- **Mor kablo (VCC)** → **Raspberry Pi 4, 3.3V (Pin 17)**  

## **4. BMP280 (Basınç Sensörü)**  
- **SDA pini** → **Raspberry Pi 4, SDA (Pin 3)**  
- **SCL pini** → **Raspberry Pi 4, SCL (Pin 5)**  
- **GND pini** → **Breadboard ortak GND hattı (ADS1115 ile paylaşılıyor)**  
- **VCC pini** → **Raspberry Pi 4, 3.3V (Pin 1)**  

## **5. ADS1115 (Analog-Dijital Dönüştürücü)**  
- **VDD pini** → **Raspberry Pi 4, 3.3V (Pin 1)**  
- **GND pini** → **Breadboard ortak GND hattı (BMP280 ile paylaşılıyor)**  
- **SDA pini (Breadboard üzerinden)** → **BMP280 SDA pini**  
- **SCL pini (Breadboard üzerinden)** → **BMP280 SCL pini**  

## **Breadboard Üzerindeki Ortak Bağlantılar:**  
- **BMP280 SDA** → **ADS1115 SDA (Breadboard ortak hattı üzerinden)**  
- **BMP280 SCL** → **ADS1115 SCL (Breadboard ortak hattı üzerinden)**  
- **ADS1115 VDD** → **BMP280 VCC (Breadboard ortak hattı üzerinden)**  
- **ADS1115 GND** → **BMP280 GND (Breadboard ortak GND hattı üzerinden)**  
