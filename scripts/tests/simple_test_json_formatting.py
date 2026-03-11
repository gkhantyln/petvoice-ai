import json
import re

def is_json_data(data):
    """
    Verinin JSON formatında olup olmadığını kontrol eder
    """
    try:
        if isinstance(data, dict):
            return True
        json.loads(data)
        return True
    except (ValueError, TypeError):
        return False

def format_json_as_markdown(json_data):
    """
    JSON verisini daha okunabilir bir Markdown formatına dönüştürür
    """
    try:
        # Eğer json_data zaten bir dict ise, doğrudan kullan
        if isinstance(json_data, dict):
            data = json_data
        else:
            # Değilse, JSON string olarak parse et
            data = json.loads(json_data)
        
        # Markdown formatında çıktı oluştur
        markdown_output = ""
        
        # Analiz başlığı
        if "analiz_basligi" in data:
            markdown_output += f"## 📊 {data['analiz_basligi']}\n\n"
        
        # Hayvan bilgileri
        if "hayvan_bilgileri" in data:
            markdown_output += "## 🐾 Hayvan Bilgileri\n\n"
            hayvan = data["hayvan_bilgileri"]
            markdown_output += f"- **Tür:** {hayvan.get('tur', 'Belirtilmemiş')}\n"
            markdown_output += f"- **Yaş:** {hayvan.get('yas', 'Belirtilmemiş')}\n"
            markdown_output += f"- **Cinsiyet:** {hayvan.get('cinsiyet', 'Belirtilmemiş')}\n"
            markdown_output += f"- **Sağlık Durumu:** {hayvan.get('saglik_durumu', 'Belirtilmemiş')}\n\n"
        
        # Ses verileri
        if "ses_verileri" in data:
            markdown_output += "## 🎵 Ses Verileri\n\n"
            ses = data["ses_verileri"]
            markdown_output += f"- **Süre:** {ses.get('sure', 'Belirtilmemiş')}\n"
            markdown_output += f"- **Frekans Aralığı:** {ses.get('frekans_araligi', 'Belirtilmemiş')}\n"
            markdown_output += f"- **Yoğunluk:** {ses.get('yogunluk', 'Belirtilmemiş')}\n"
            markdown_output += f"- **Dominant Frekans:** {ses.get('dominant_frekans', 'Belirtilmemiş')}\n\n"
        
        # Bağlam
        if "baglam" in data:
            markdown_output += f"## 📍 Bağlam\n\n{data['baglam']}\n\n"
        
        # Profesyonel analiz
        if "profesyonel_analiz" in data:
            analiz = data["profesyonel_analiz"]
            markdown_output += "## 🧠 Profesyonel Analiz\n\n"
            
            # Aciliyet seviyesi
            if "aciliyet_seviyesi" in analiz:
                markdown_output += f"### 🔴 Aciliyet Seviyesi: {analiz['aciliyet_seviyesi']}\n\n"
            
            # Tespit edilen duygu durumu
            if "tespit_edilen_duygu_durumu" in analiz:
                markdown_output += f"### ❤️ Tespit Edilen Duygu Durumu\n\n{analiz['tespit_edilen_duygu_durumu']}\n\n"
            
            # Olası ihtiyaç veya sorun
            if "olasi_ihtiyac_veya_sorun" in analiz:
                markdown_output += "### 📋 Olası İhtiyaç veya Sorun\n\n"
                ihtiyac_sorun = analiz["olasi_ihtiyac_veya_sorun"]
                
                if "ihtiyac" in ihtiyac_sorun:
                    markdown_output += f"**İhtiyaç:** {ihtiyac_sorun['ihtiyac']}\n\n"
                
                if "sorun" in ihtiyac_sorun:
                    markdown_output += f"**Sorun:** {ihtiyac_sorun['sorun']}\n\n"
            
            # Sahibe tavsiyeler
            if "sahibe_tavsiyeler" in analiz:
                markdown_output += "### 💡 Sahibe Tavsiyeler\n\n"
                for tavsiye in analiz["sahibe_tavsiyeler"]:
                    markdown_output += f"- {tavsiye}\n"
                markdown_output += "\n"
            
            # Veteriner kontrolü
            if "veteriner_kontrolu_gerekli_mi" in analiz:
                markdown_output += f"### 🏥 Veteriner Kontrolü Gerekli mi?\n\n{analiz['veteriner_kontrolu_gerekli_mi']}\n\n"
            
            # Güven skoru
            if "guven_skoru" in analiz:
                markdown_output += f"### 📊 Güven Skoru: {analiz['guven_skoru']}%\n\n"
        
        return markdown_output
        
    except Exception as e:
        # Hata durumunda, orijinal veriyi döndür
        return f"## Hata\n\nVeri formatlanırken bir hata oluştu: {str(e)}\n\nOrijinal veri:\n\n```json\n{json_data}\n```"

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