# Weather-Station

Raspberry Pi 4 üzerinde çalışan bir hava istasyonu. Sıcaklık, nem, basınç, yükseklik, rüzgâr hızı ve yönü ile yağmur durumunu sensörlerden okuyor, Flask ile yerel ağda bir web arayüzünde ve JSON API'de gösteriyor.

## Donanım

| Sensör | Ölçtüğü | Bağlantı |
|---|---|---|
| DHT22 | Sıcaklık, nem | GPIO27 |
| BMP280 | Basınç, yükseklik | I2C (0x76, olmazsa 0x77) |
| ADS1115 | Analog → dijital dönüştürücü | I2C |
| Anemometre | Rüzgâr hızı | ADS1115 A0 |
| Rüzgâr yönü potansiyometresi | Rüzgâr yönü | ADS1115 A1 |
| Yağmur sensörü | Yağmur var / yok | GPIO17 |

Kablo kablo bağlantı şeması: [hava_istasyonu_baglanti_semasi.md](hava_istasyonu_baglanti_semasi.md)

## Nasıl çalışıyor

- `app.py` sensörleri başlatır. Her `/api/weather` isteğinde sensörleri okuyup JSON döner.
- Okunamayan sensörün değeri `null` gelir, diğer ölçümler etkilenmez. DHT22 okumaları ara sıra başarısız olur, bu normaldir.
- `templates/index.html` bu API'yi 5 saniyede bir çağırıp kartlarda gösterir.
- Rüzgâr hızı, anemometrenin çıkış voltajından doğrusal olarak hesaplanır (1 V = 8 m/s). Rüzgâr yönü 270° dönen bir potansiyometrenin voltajından dört ana yöne çevrilir.

Örnek yanıt:

```json
{
  "temp_dht": 21.4, "humidity": 48.2,
  "pressure": 0.998, "altitude": 74.3,
  "wind_speed": 12.672, "wind_direction": "North",
  "rain_status": "No Rain",
  "update_time": "2025-05-01 14:03:12"
}
```

`pressure` atm cinsindendir. `wind_speed` km/sa cinsindendir.

## Kurulum ve çalıştırma

Raspberry Pi üzerinde, I2C açıkken (`sudo raspi-config` → Interface Options → I2C):

```bash
sudo apt install python3-venv python3-pip
python3 -m venv my_env
source my_env/bin/activate
pip install -r requirements.txt
python app.py
```

Arayüz: `http://<raspberry_pi_ip>:5000/` · API: `http://<raspberry_pi_ip>:5000/api/weather`

## Güvenlik notu

Sunucu `0.0.0.0` üzerinde dinler, yani yerel ağdaki herkes erişebilir. Kimlik doğrulama yoktur ve Flask'ın geliştirme sunucusu kullanılır. Bu yüzden istasyon yalnızca güvenilen yerel ağda çalıştırılmalı, modemden port yönlendirmesiyle internete açılmamalıdır. Dışarıdan erişim gerekirse önüne kimlik doğrulamalı bir ters vekil (ör. nginx) ya da VPN konmalıdır.
