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
    "ai_analiz_sonuclari": "## 🔍 Aciliyet Seviyesi\n\nDüşük (1/5)\nHayvanınızın ses kaydında acil bir durum belirtisi bulunmamaktadır. Rahat ve sakin bir ses tonu hakim.\n\n## ❤️ Tespit Edilen Duygu Durumu\n\nMemnuniyet\nSes kaydında memnuniyet belirtileri açıkça görülmektedir. Hayvanınız rahat ve huzurlu görünmektedir.",
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

# Test data URI creation (simplified)
data_uri = "data:text/json;charset=utf-8," + json_str
print("\nData URI (first 100 chars):")
print(data_uri[:100] + "...")