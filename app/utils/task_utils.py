# app/utils/task_utils.py
# Görev yardımcı fonksiyonları
# Bu dosya, arka plan görevlerinin sonuçlarını işlemek için yardımcı fonksiyonları içerir

from app.models.models import db, SoundAnalysis
from app.utils.format_utils import format_json_as_markdown, is_json_data

def update_analysis_result(analysis_id, result):
    """
    Analiz sonucunu veritabanında günceller
    """
    try:
        # Uygulama context'i içinde çalış
        from flask import current_app
        with current_app.app_context():
            # Analizi veritabanından getir
            analysis = SoundAnalysis.query.get(analysis_id)
            if not analysis:
                return False
            
            # Sonuçları güncelle
            if result['status'] == 'Tamamlandı':
                ai_result = result['ai_analysis']
                
                # AI analiz sonucunu al - string veya dict olabilir
                if isinstance(ai_result, str):
                    # Eğer string ise doğrudan kullan
                    ai_analysis_content = ai_result
                    analysis.ai_analysis = ai_analysis_content
                    analysis.confidence_score = None
                    analysis.emotion_detected = None
                    analysis.urgency_level = None
                    analysis.veterinary_recommendation = None
                elif isinstance(ai_result, dict):
                    # Eğer dict ise içinden değerleri al
                    ai_analysis_content = ai_result.get('ai_analysis') or ai_result.get('analysis_text', '')
                    
                    # Eğer içerik JSON formatındaysa, Markdown formatına çevir
                    if ai_analysis_content and is_json_data(ai_analysis_content):
                        analysis.ai_analysis = format_json_as_markdown(ai_analysis_content)
                    else:
                        analysis.ai_analysis = ai_analysis_content
                        
                    analysis.confidence_score = ai_result.get('confidence_score')
                    analysis.emotion_detected = ai_result.get('emotion_detected', ai_result.get('emotion'))
                    analysis.urgency_level = ai_result.get('urgency_level')
                    analysis.veterinary_recommendation = ai_result.get('veterinary_recommendation')
                else:
                    # Bilinmeyen tip
                    analysis.ai_analysis = str(ai_result)
                    analysis.confidence_score = None
                    analysis.emotion_detected = None
                    analysis.urgency_level = None
                    analysis.veterinary_recommendation = None
                    
                analysis.spectrogram_path = result.get('spectrogram_path')
                analysis.json_spectrogram_path = result.get('json_spectrogram_path')
                analysis.analysis_status = 'completed'
            else:
                # Hata durumu
                analysis.analysis_status = 'failed'
                analysis.ai_analysis = result.get('error', 'Bilinmeyen hata')
            
            # Veritabanını güncelle
            db.session.commit()
            return True
            
    except Exception as e:
        db.session.rollback()
        print(f"Analiz sonucu güncelleme hatası: {e}")
        return False