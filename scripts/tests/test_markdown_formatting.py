import os
import sys
import traceback

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    from utils.ai_analyzer import format_ai_response_as_markdown
    
    # Test the markdown formatting function
    test_response = """1. Aciliyet Seviyesi: Düşük (1/5)
    Hayvanınızın ses kaydında acil bir durum belirtisi bulunmamaktadır. Rahat ve sakin bir ses tonu hakim.

    2. Tespit Edilen Duygu Durumu: Memnuniyet
    Ses kaydında memnuniyet belirtileri açıkça görülmektedir. Hayvanınız rahat ve huzurlu görünmektedir.

    3. Olası İhtiyaç veya Sorun: Oyun ve etkinlik ihtiyacı
    Hayvanınızın enerji seviyesi yüksek görünmektedir. Oyun ve etkileşim ihtiyacı olabilir.

    4. Sahibe Tavsiyeler:
    - Hayvanınızla oyun zamanı planlayın
    - Yeni oyuncaklarla ilgisini çekmeyi deneyin
    - Günlük rutin aktivitelerinizi sürdürün

    5. Veteriner Kontrolü Gerekli mi?: Hayır
    Şu an için veteriner kontrolü gerekli değildir. Hayvanınız sağlıklı ve huzurlu görünmektedir.

    6. Güven Skoru: 95.5%"""

    print("Original response:")
    print(test_response)
    print("\n" + "="*50 + "\n")

    formatted = format_ai_response_as_markdown(test_response)
    print("Formatted response:")
    print(formatted)
    
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()