import sys
import os
import json
import re

# Proje yolunu Python path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Flask uygulamasını başlat
from app import create_app
from app.models.models import db, SoundAnalysis
from app.utils.format_utils import format_json_as_markdown

def extract_json_from_markdown(text):
    """Markdown içinden JSON veriyi çıkar"""
    # ```json ... ``` arasında kalan kısmı bul
    match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        return match.group(1)
    return None

def is_json_data(data):
    """Verinin JSON formatında olup olmadığını kontrol et"""
    try:
        if isinstance(data, dict):
            return True
        json.loads(data)
        return True
    except (ValueError, TypeError):
        return False

def fix_analyses_format():
    """Veritabanındaki analiz sonuçlarını düzelt"""
    app = create_app()
    
    with app.app_context():
        # Tüm analizleri al
        analyses = SoundAnalysis.query.all()
        
        print(f"Toplam {len(analyses)} analiz bulundu.")
        
        for analysis in analyses:
            print(f"\n--- Analiz ID: {analysis.id} ---")
            
            if not analysis.ai_analysis:
                print("Boş analiz, atlanıyor.")
                continue
                
            # JSON veriyi çıkar
            json_content = None
            
            # Önce markdown içinden JSON çıkar
            if '```json' in analysis.ai_analysis:
                json_content = extract_json_from_markdown(analysis.ai_analysis)
                print("Markdown içinden JSON çıkarıldı.")
            
            # Eğer hala yoksa, doğrudan JSON olabilir
            if not json_content:
                # Başında ve sonundaki boşlukları temizle
                cleaned_content = analysis.ai_analysis.strip()
                # ```json ve ``` işaretlerini kaldır
                cleaned_content = cleaned_content.replace('```json', '').replace('```', '').strip()
                
                # JSON olarak parse etmeyi dene
                try:
                    json.loads(cleaned_content)
                    json_content = cleaned_content
                    print("JSON doğrudan çıkarıldı.")
                except json.JSONDecodeError:
                    print("JSON veri bulunamadı veya geçersiz.")
                    continue
            
            # JSON veriyi Markdown formatına çevir
            if json_content:
                try:
                    print("JSON veri formatlanıyor...")
                    formatted_content = format_json_as_markdown(json_content)
                    analysis.ai_analysis = formatted_content
                    
                    # Değişiklikleri kaydet
                    db.session.commit()
                    print(f"Analiz ID {analysis.id} başarıyla formatlandı.")
                except Exception as e:
                    print(f"Analiz ID {analysis.id} formatlanırken hata oluştu: {e}")
                    db.session.rollback()
            else:
                print("JSON veri bulunamadı.")
        
        print("\nTüm analizler işlendi.")

if __name__ == "__main__":
    fix_analyses_format()