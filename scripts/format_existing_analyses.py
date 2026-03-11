import sys
import os

# Proje yolunu Python path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Flask uygulamasını başlat
from app import create_app
from app.models.models import db, SoundAnalysis
from app.utils.format_utils import format_json_as_markdown, is_json_data

def format_existing_analyses():
    """Veritabanındaki mevcut analiz sonuçlarını formatla"""
    app = create_app()
    
    with app.app_context():
        # Tüm analizleri al
        analyses = SoundAnalysis.query.all()
        
        print(f"Toplam {len(analyses)} analiz bulundu.")
        
        for analysis in analyses:
            if analysis.ai_analysis and is_json_data(analysis.ai_analysis):
                print(f"Analiz ID {analysis.id} için JSON veri formatlanıyor...")
                try:
                    # JSON veriyi Markdown formatına çevir
                    formatted_content = format_json_as_markdown(analysis.ai_analysis)
                    analysis.ai_analysis = formatted_content
                    
                    # Değişiklikleri kaydet
                    db.session.commit()
                    print(f"Analiz ID {analysis.id} başarıyla formatlandı.")
                except Exception as e:
                    print(f"Analiz ID {analysis.id} formatlanırken hata oluştu: {e}")
                    db.session.rollback()
            else:
                print(f"Analiz ID {analysis.id} zaten formatlanmış veya boş.")
        
        print("Tüm analizler işlendi.")

if __name__ == "__main__":
    format_existing_analyses()