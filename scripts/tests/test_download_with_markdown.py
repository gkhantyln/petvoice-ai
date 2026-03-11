import json

# Test data similar to what would be used in the download function
analysis_data = {
    "analiz_bilgileri": {
        "analiz_id": 12345,
        "hayvan_adi": "Karabaş",
        "hayvan_turu": "Köpek",
        "kayit_tarihi": "03.09.2025 14:30",
        "dosya_adi": "karabas_ses_kaydi.wav",
        "durum": "completed"
    },
    "ai_analiz_sonuclari": "## 📊 Kedi Vocalizasyon Analizi - Oyun Oynarken\n\n## 🐾 Hayvan Bilgileri\n\n- **Tür:** Kedi\n- **Yaş:** 4\n- **Cinsiyet:** Erkek\n- **Sağlık Durumu:** Sağlıklı\n\n## 🎵 Ses Verileri\n\n- **Süre:** 2.95 saniye\n- **Frekans Aralığı:** (0, 22050.0) Hz\n- **Yoğunluk:** 51.08 dB\n- **Dominant Frekans:** 3056.16 Hz\n\n## 📍 Bağlam\n\nOyun Oynarken\n\n## 🧠 Profesyonel Analiz\n\n### 🔴 Aciliyet Seviyesi: 1\n\n### ❤️ Tespit Edilen Duygu Durumu\n\nBu ses, kedilerin avlanma içgüdüsü tetiklendiğinde veya oyuncak/av hedefine odaklandığında çıkardığı 'chattering' veya 'trilling' (çatırdayan veya titrek ses) olarak bilinen tipik bir vokalizasyondur.",
    "ozel_bilgiler": {
        "guven_skoru": "95.5%",
        "tespit_edilen_duygu": "Memnuniyet",
        "aciliyet_seviyesi": "Düşük",
        "veteriner_onerisi": "Özel bir öneri gerekli değil."
    }
}

# Test JSON creation
json_str = json.dumps(analysis_data, indent=2, ensure_ascii=False)
print("JSON output:")
print(json_str)

# Test that the Markdown content is properly preserved in JSON
print("\nAI Analysis Results (first 200 chars):")
print(analysis_data["ai_analiz_sonuclari"][:200] + "...")