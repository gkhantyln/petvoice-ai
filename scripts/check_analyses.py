import sys
import os
import json

# Proje yolunu Python path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Flask uygulamasını başlat
from app import create_app
from app.models.models import db, SoundAnalysis

def check_analyses():
    """Veritabanındaki analiz sonuçlarını kontrol et"""
    app = create_app()
    
    with app.app_context():
        # Tüm analizleri al
        analyses = SoundAnalysis.query.all()
        
        print(f"Toplam {len(analyses)} analiz bulundu.")
        
        for analysis in analyses:
            print(f"\n--- Analiz ID: {analysis.id} ---")
            print(f"Durum: {analysis.analysis_status}")
            print(f"AI Analiz (ilk 200 karakter):")
            
            if analysis.ai_analysis:
                # İlk 200 karakteri göster
                preview = analysis.ai_analysis[:200]
                print(preview)
                
                # JSON formatında mı kontrol et
                try:
                    # JSON olarak parse etmeyi dene
                    if analysis.ai_analysis.strip().startswith('{') and analysis.ai_analysis.strip().endswith('}'):
                        json_data = json.loads(analysis.ai_analysis)
                        print("✓ Bu veri JSON formatında")
                        print(f"JSON anahtarları: {list(json_data.keys())}")
                    else:
                        print("× Bu veri JSON formatında değil")
                except json.JSONDecodeError:
                    print("× Bu veri JSON formatında değil")
            else:
                print("Boş veya None")

if __name__ == "__main__":
    check_analyses()