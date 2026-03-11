#!/usr/bin/env python3
"""
Google Gemini API Key Test Script (Güncel Sürüm)
Bu script, Google Generative AI API anahtarınızın geçerli olup olmadığını test eder.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_api_key():
    """Google API key'i test eder"""

    # .env dosyasından ortam değişkenlerini yükle
    load_dotenv()
    
    # Ortam değişkeninden API anahtarını al
    api_key = "AIzaSyDyGvRUJDd34R5iTj1ME_0HTSjGOVVLknc" ##os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("❌ Hata: GOOGLE_API_KEY ortam değişkeni bulunamadı!")
        print("Lütfen projenizin kök dizininde bir .env dosyası oluşturun ve içine GOOGLE_API_KEY='AIzaSy...' şeklinde kendi API anahtarınızı ekleyin.")
        return False

    print(f"🔍 API anahtarı okunuyor (uzunluk: {len(api_key)}).")

    try:
        # API key'i yapılandır
        genai.configure(api_key=api_key)
        
        # Sohbet modeli oluşturma ve test mesajı gönderme
        # Güncel yöntem: GenerativeModel kullanarak model oluşturulur.
        print("🚀 Model ile iletişim kuruluyor...")
        model = genai.GenerativeModel('gemini-2.5-flash') # Model adını direkt kullanıyoruz
        chat = model.start_chat(history=[]) # Sohbet başlatma

        response = chat.send_message("Merhaba! Bu bir test mesajıdır.") # Mesaj gönderme

        # Yanıtı kontrol et ve içeriği yazdır
        if response and response.text:
            print("📝 Test yanıtı:", response.text)
            return True
        else:
            print("📝 Test yanıtı alınamadı veya boş.")
            return False

    except Exception as e:
        print(f"❌ API Key testi başarısız oldu: {e}")
        print("\nOlası nedenler:")
        print("1. API key süresi dolmuş, geçersiz veya yetkilendirilmemiş.")
        print("2. Google Generative Language API projeniz için etkin değil.")
        print("3. Kota limitini aşmış olabilirsiniz.")
        print("4. Ağ veya proxy bağlantı sorunları.")
        print("5. Kullandığınız model adı geçersiz olabilir veya erişiminiz olmayabilir.")
        return False

if __name__ == "__main__":
    print("🧪 Google Gemini API Key Test Scripti")
    print("=" * 40)

    success = test_api_key()

    print("\n" + "=" * 40)
    if success:
        print("🎉 Tebrikler! API anahtarınız başarılı bir şekilde çalışıyor.")
    else:
        print("💥 API anahtarınız ile ilgili bir sorun var. Lütfen yukarıdaki hata mesajlarını kontrol edin.")