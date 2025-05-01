from flask import Flask, render_template
import time
import board
import busio
import adafruit_bmp280
import adafruit_dht
import adafruit_ads1x15.ads1115 as ADS
from datetime import datetime, timedelta, timezone
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO

# Flask uygulama nesnesi tanimlanir
app = Flask(__name__)

# --- Sensor Ayarlari ---
# I2C protokolunu kullanarak sensorler icin baglanti olusturulur
i2c = board.I2C()

# BMP280 sensoru icin baglanti olusturulur, eger 0x76 adresinde baglanamazsa 0x77 adresini dener
try:
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
except ValueError:
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)

# Deniz seviyesindeki basinc degeri ayarlanir
bmp280.sea_level_pressure = 1025

# DHT22 sicaklik ve nem sensoru icin baglanti olusturulur
dht = adafruit_dht.DHT22(board.D27)

# Yagmur sensori icin GPIO ayarlari yapilir
RAIN_SENSOR_PIN = 17  # Yagmur sensorunun bagli oldugu GPIO pini
GPIO.setmode(GPIO.BCM)
GPIO.setup(RAIN_SENSOR_PIN, GPIO.IN)  # GPIO pini giris olarak ayarlanir

# Anemometre verilerini okumak icin bir sinif tanimlanir
class AnemometerReader:
    def __init__(self):
        # I2C baglantisi ve ADS1115 ADC modulu tanimlanir
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        # Anemometre verisi ADC modulu uzerinden okunur
        self.anemometer = AnalogIn(self.ads, ADS.P0)
        self.wind_direction = AnalogIn(self.ads, ADS.P1)

    def read_wind_speed(self):
        # Anemometre voltaj degerine gore ruzgar hizi hesaplanir
        wind_speed_mps = self.anemometer.voltage * 8  # Voltaj * 8 m/s
        wind_speed_kph = wind_speed_mps * 3.6  # m/s degerini km/h'ye cevirme
        return round(wind_speed_kph, 3)  # 3 ondalikli basamakla dondurulur

    def read_wind_direction(self):
        voltage = self.wind_direction.voltage
        angle = (voltage / 3.3) * 270  # 270 derece donen potansiyometre icin
        return angle

    def determine_direction(self, angle):
        if 0 <= angle < 67.5:
            return "East"
        elif 67.5 <= angle < 135:
            return "North"
        elif 135 <= angle < 202.5:
            return "West"
        else:
            return "South"

# Anemometre okuyucusu icin bir nesne olusturulur
anemometer_reader = AnemometerReader()

# --- Ana Sayfa (/) ---
# Ana sayfa istegine yanit verir
@app.route('/')
def home():
    return render_template('index.html')  # index.html sayfasini dondurur

# --- Hava Durumu API (/api/weather) ---
# Hava durumu verilerini saglayan API
@app.route('/api/weather')
def weather_data():
    try:
        # BMP280 sensorunden basinc ve yukseklik verileri okunur
        pressure = round(bmp280.pressure, 3)
        altitude = round(bmp280.altitude, 3)
        pressure_atm = round(pressure / 1025, 3) 
    except:
        # Sensor verisi okunamazsa None dondurulur
        temp_bmp, pressure, altitude = None, None, None

    try:
        # DHT22 sensorunden sicaklik ve nem verileri okunur
        temp_dht = round(dht.temperature, 3)
        humidity = round(dht.humidity, 3)
    except:
        # Sensor verisi okunamazsa None dondurulur
        temp_dht, humidity = None, None

    # Anemometreden ruzgar hizi okunur
    wind_speed = anemometer_reader.read_wind_speed()
    wind_angle = anemometer_reader.read_wind_direction()
    wind_direction = anemometer_reader.determine_direction(wind_angle)

    # Yagmur durumu GPIO pininden okunur
    rain_status = "Rain" if GPIO.input(RAIN_SENSOR_PIN) == GPIO.LOW else "No Rain"

    # Veriler JSON formatinda dondurulur
    return {
        "pressure": pressure_atm,
        "altitude": altitude,
        "temp_dht": temp_dht,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "wind_direction": wind_direction,
        "rain_status": rain_status,
        "update_time" : (datetime.utcnow() + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
        
    }

# Flask uygulamasi calistirilir
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Uygulama tum IP adreslerinden erisilebilir ve 5000 portunda calisir
S
