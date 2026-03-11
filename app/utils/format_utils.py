# app/utils/format_utils.py
# Format yardımcı fonksiyonları
# Bu dosya, verilerin farklı formatlara dönüştürülmesi için yardımcı fonksiyonları içerir

import json
import re

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
                    # Markdown listesi olarak formatla
                    tavsiye_text = tavsiye
                    markdown_output += f"- {tavsiye_text}\n"
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

def is_json_data(data):
    """
    Verinin JSON formatında olup olmadığını kontrol eder
    """
    try:
        if isinstance(data, dict):
            return True
        # Önce başındaki ve sonundaki boşlukları temizle
        cleaned_data = data.strip()
        # ```json ve ``` işaretlerini kaldır
        if cleaned_data.startswith('```json'):
            cleaned_data = cleaned_data[7:]  # ```json kısmını kaldır
        if cleaned_data.endswith('```'):
            cleaned_data = cleaned_data[:-3]  # ``` kısmını kaldır
        cleaned_data = cleaned_data.strip()
        
        json.loads(cleaned_data)
        return True
    except (ValueError, TypeError):
        return False