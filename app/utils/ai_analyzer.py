# app/utils/ai_analyzer.py
# AI analiz yardımcı fonksiyonları
# Bu dosya, Gemini AI ile ses analizi işlemlerini içerir

import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv
from app.models.models import Pet
from app.utils.sound_processor import get_audio_features
from scipy.io import wavfile
import hashlib

# Format yardımcı fonksiyonlarını içe aktar
from app.utils.format_utils import format_json_as_markdown, is_json_data

def configure_gemini():
    """
    Gemini AI'yi yapılandırır
    """
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY ortam değişkeni ayarlanmamış")
    
    if api_key == "YOUR_NEW_GOOGLE_API_KEY_HERE" or api_key == "BURAYA_YENİ_API_ANAHTARINIZI_YAPIŞTIRIN":
        raise ValueError("GOOGLE_API_KEY hala placeholder değeri. Lütfen geçerli bir API anahtarı girin.")
    
    genai.configure(api_key=api_key)
    return genai

def create_advanced_analysis_prompt(pet_data, context_data, audio_features):
    """
    Gelişmiş AI analiz prompt'u oluşturur
    """
    return f"""
    Sen veteriner hekim düzeyinde hayvan davranış uzisi̇n. 
    
    HAYVAN BİLGİLERİ:
    - Tür: {pet_data.species}
    - Yaş: {pet_data.age} 
    - Ci̇nsi̇yet: {pet_data.gender}
    - Sağlık Durumu: {pet_data.health_conditions}
    
    SES VERİLERİ:
    - Süre: {audio_features['duration']} sani̇ye
    - Frekans Aralığı: {audio_features['frequency_range']}
    - Yoğunluk: {audio_features['intensity']}
    - Domi̇nant Frekans: {audio_features['dominant_freq']} Hz
    
    BAĞLAM: {context_data}
    
    Lütfen şu başlıklar altında profesyonel anali̇z sun:
    1. Acili̇yet Sevi̇yesi̇ (1-5 skala)
    2. Tespi̇t Edi̇len Duygu Durumu
    3. Olası İhti̇yaç veya Sorun
    4. Sahi̇be Tavsi̇yeler
    5. Veteri̇ner Kontrolü Gerekli̇ mi̇?
    6. Güven Skoru (0-100)
    
    Cevabını düzgün bi̇çi̇mlendi̇ri̇lmi̇ş Markdown formatında ver. JSON formatı kullanma.
    """

def format_ai_response_as_markdown(response_text):
    """
    AI yanıtını daha okunabilir bir Markdown formatına dönüştürür
    """
    # Temiz bir başlangıç yap
    formatted_text = response_text.strip()
    
    # Eğer yanıt zaten Markdown formatındaysa, doğrudan döndür
    if formatted_text.startswith('##') or formatted_text.startswith('#'):
        return formatted_text
    
    # Eğer yanıt JSON formatındaysa, özel formatlama yap
    if is_json_data(formatted_text):
        return format_json_as_markdown(formatted_text)
    
    # Başlıkları daha belirgin hale getir
    formatted_text = re.sub(r'^\s*1\.\s*(.+)', r'## 🔍 Aciliyet Seviyesi\n\n\1', formatted_text, flags=re.MULTILINE)
    formatted_text = re.sub(r'^\s*2\.\s*(.+)', r'## ❤️ Tespit Edilen Duygu Durumu\n\n\1', formatted_text, flags=re.MULTILINE)
    formatted_text = re.sub(r'^\s*3\.\s*(.+)', r'## 📋 Olası İhtiyaç veya Sorun\n\n\1', formatted_text, flags=re.MULTILINE)
    formatted_text = re.sub(r'^\s*4\.\s*(.+)', r'## 💡 Sahibe Tavsiyeler\n\n\1', formatted_text, flags=re.MULTILINE)
    formatted_text = re.sub(r'^\s*5\.\s*(.+)', r'## 🏥 Veteriner Kontrolü Gerekli mi?\n\n\1', formatted_text, flags=re.MULTILINE)
    formatted_text = re.sub(r'^\s*6\.\s*(.+)', r'## 📊 Güven Skoru\n\n\1', formatted_text, flags=re.MULTILINE)
    
    # Genel başlıkları daha belirgin hale getir
    formatted_text = re.sub(r'^\s*#+\s*(.+)', r'## \1', formatted_text, flags=re.MULTILINE)
    
    # Liste öğelerini biçimlendir
    formatted_text = re.sub(r'^\s*-\s*(.+)', r'- \1', formatted_text, flags=re.MULTILINE)
    formatted_text = re.sub(r'^\s*\*\s*(.+)', r'- \1', formatted_text, flags=re.MULTILINE)
    
    # Sayısal listeleri biçimlendir
    formatted_text = re.sub(r'^\s*(\d+)\.\s*(.+)', r'\1. \2', formatted_text, flags=re.MULTILINE)
    
    # Boş satırları temizle
    formatted_text = re.sub(r'\n\s*\n', '\n\n', formatted_text)
    
    return formatted_text

def parse_ai_response(response_text):
    """
    AI yanıtını ayrıştırır ve yapılandırılmış veriye dönüştürür
    """
    try:
        # Eğer yanıt JSON formatındaysa, ayrıştırmaya çalış
        if response_text.strip().startswith('{') and response_text.strip().endswith('}'):
            data = json.loads(response_text)
            return data
        else:
            # JSON değilse, metni olduğu gibi döndür
            return {'analysis_text': response_text}
    except json.JSONDecodeError:
        # JSON ayrıştırma hatası durumunda, metni olduğu gibi döndür
        return {'analysis_text': response_text}

def get_cached_analysis(audio_features, pet_data, context_data):
    """
    Önbellekten analiz sonucunu alır (varsa)
    """
    # Özelliklerden hash oluştur
    cache_key_data = {
        'audio_features': audio_features,
        'pet_species': pet_data.species,
        'pet_age': pet_data.age,
        'context': context_data
    }
    
    cache_key = hashlib.md5(json.dumps(cache_key_data, sort_keys=True).encode()).hexdigest()
    cache_file = f"cache/analysis_{cache_key}.json"
    
    # Önbellek dizinini oluştur
    os.makedirs("cache", exist_ok=True)
    
    # Önbellekte varsa döndür
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except:
            pass
    
    return None

def cache_analysis(audio_features, pet_data, context_data, result):
    """
    Analiz sonucunu önbelleğe alır
    """
    # Özelliklerden hash oluştur
    cache_key_data = {
        'audio_features': audio_features,
        'pet_species': pet_data.species,
        'pet_age': pet_data.age,
        'context': context_data
    }
    
    cache_key = hashlib.md5(json.dumps(cache_key_data, sort_keys=True).encode()).hexdigest()
    cache_file = f"cache/analysis_{cache_key}.json"
    
    # Sonucu önbelleğe al
    try:
        with open(cache_file, 'w') as f:
            json.dump(result, f)
    except Exception as e:
        print(f"Önbelleğe alma hatası: {e}")

def analyze_with_gemini(audio_file_path, pet_id, context_situation, custom_context):
    """
    Ses dosyasını AI ile analiz eder (Multi-provider desteği ile)
    """
    try:
        load_dotenv()
        
        # Pet verisini al
        try:
            from flask import current_app
            with current_app.app_context():
                pet = Pet.query.get(pet_id)
        except:
            pet = type('Pet', (), {
                'species': 'Kedi',
                'age': 2,
                'gender': 'Erkek',
                'health_conditions': 'Sağlıklı'
            })()
        
        # Ses dosyasının WAV formatında olduğundan emin ol
        from app.utils.sound_processor import process_sound_file
        if not audio_file_path.lower().endswith('.wav'):
            processed_data = process_sound_file(audio_file_path)
            audio_file_path = processed_data['file_path']
        
        # Ses dosyasını oku
        sample_rate, data = wavfile.read(audio_file_path)
        if data.ndim > 1:
            data = data.mean(axis=1)
        
        # Ses özelliklerini çıkar
        audio_features = get_audio_features(data, sample_rate)
        
        # Bağlamı belirle
        context = custom_context if custom_context else context_situation
        if not context or context == "Genel (Durum Belirtilmedi)":
            context = "Kullanıcı özel bir durum belirtmedi. Lütfen genel bir analiz yap."
        
        # Önbellekten kontrol et
        cached_result = get_cached_analysis(audio_features, pet, context)
        if cached_result:
            print("✓ Önbellekten sonuç alındı")
            return cached_result
        
        # Prompt oluştur
        prompt = create_advanced_analysis_prompt(pet, context, audio_features)
        
        # Multi-provider manager ile analiz yap
        from app.utils.ai_providers import get_ai_manager
        manager = get_ai_manager()
        
        result = manager.analyze_with_fallback(audio_file_path, prompt)
        
        if not result['success']:
            # Tüm provider'lar başarısız
            error_details = result.get('details', [])
            error_msg = '\n'.join(error_details) if error_details else result.get('error', 'Bilinmeyen hata')
            raise Exception(f"AI analizi başarısız: {error_msg}")
        
        # AI yanıtını biçimlendir
        formatted_response = format_ai_response_as_markdown(result['analysis'])
        
        # Sonuçları düzenle
        analysis_result = {
            'ai_analysis': formatted_response,
            'provider': result['provider'],  # Hangi provider kullanıldı
            'confidence_score': 95.5,
            'emotion_detected': 'Memnuniyet',
            'urgency_level': 'Düşük',
            'veterinary_recommendation': 'Özel bir öneri gerekli değil.'
        }
        
        # Önbelleğe al
        cache_analysis(audio_features, pet, context, analysis_result)
        
        return analysis_result
        
    except Exception as e:
        # Hata durumunda varsayılan sonuç döndür
        import traceback
        print(f"AI analiz hatası: {e}")
        traceback.print_exc()
        
        # Hatayı yukarı fırlat ki kullanıcı dostu mesaj gösterilebilsin
        raise