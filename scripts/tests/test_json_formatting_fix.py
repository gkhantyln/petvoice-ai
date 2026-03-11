import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Test the JSON formatting function with the data you provided
from app.utils.format_utils import format_json_as_markdown, is_json_data

# Sample JSON data similar to what comes from AI analysis
test_json_string = '''{
    "analiz_basligi": "Kedi Vocalizasyon Analizi - Oyun Oynarken",
    "hayvan_bilgileri": {
        "tur": "Kedi",
        "yas": "4",
        "cinsiyet": "Erkek",
        "saglik_durumu": "Sağlıklı"
    },
    "ses_verileri": {
        "sure": "2.95 saniye",
        "frekans_araligi": "(0, 22050.0) Hz",
        "yogunluk": "51.08 dB",
        "dominant_frekans": "3056.16 Hz"
    },
    "baglam": "Oyun Oynarken",
    "profesyonel_analiz": {
        "aciliyet_seviyesi": 1,
        "tespit_edilen_duygu_durumu": "Bu ses, kedilerin avlanma içgüdüsü tetiklendiğinde veya oyuncak/av hedefine odaklandığında çıkardığı 'chattering' veya 'trilling' (çatırdayan veya titrek ses) olarak bilinen tipik bir vokalizasyondur.",
        "olasi_ihtiyac_veya_sorun": {
            "ihtiyac": "Kedinin avlanma içgüdüsünü tatmin etme, zihinsel ve fiziksel uyarım.",
            "sorun": "Bu vokalizasyonun kendisi bir sorun değildir; aksine sağlıklı bir kedinin doğal ve içgüdüsel bir davranışıdır."
        },
        "sahibe_tavsiyeler": [
            "**Davranışı Anlayın:** Kedinizin bu sesi çıkarması tamamen doğal ve sağlıklı bir avlanma davranışıdır.",
            "**Etkileşimli Oyunları Sürdürün:** Kedinizin avlanma içgüdülerini tatmin edecek oyunlar oynamaya devam edin."
        ],
        "veteriner_kontrolu_gerekli_mi": "Hayır. Mevcut bilgiler ve bağlam göz önüne alındığında, bu ses tamamen normal bir davranıştır.",
        "guven_skoru": 98
    }
}'''

print("Testing JSON detection and formatting...")
print("Is JSON data:", is_json_data(test_json_string))
formatted = format_json_as_markdown(test_json_string)
print("\nFormatted Markdown output:")
print(formatted)