# generate_docs.py
# API dökümantasyonu oluşturucu
# Bu dosya, API dökümantasyonunu otomatik olarak oluşturur

import os
import json
from datetime import datetime

def generate_api_docs():
    """API dökümantasyonu oluşturur"""
    # API endpoint bilgileri
    api_endpoints = [
        {
            "endpoint": "POST /api/auth/register",
            "method": "POST",
            "path": "/api/auth/register",
            "description": "Yeni kullanıcı kaydı",
            "request_body": {
                "username": "string (zorunlu)",
                "email": "string (zorunlu)",
                "password": "string (zorunlu)",
                "first_name": "string (isteğe bağlı)",
                "last_name": "string (isteğe bağlı)"
            },
            "response": {
                "success": "boolean",
                "message": "string",
                "data": "object (kullanıcı bilgileri)"
            },
            "authentication": "Gerekmez"
        },
        {
            "endpoint": "POST /api/auth/login",
            "method": "POST",
            "path": "/api/auth/login",
            "description": "Kullanıcı girişi",
            "request_body": {
                "username_or_email": "string (zorunlu)",
                "password": "string (zorunlu)"
            },
            "response": {
                "success": "boolean",
                "message": "string",
                "token": "string (JWT token)",
                "user": "object (kullanıcı bilgileri)"
            },
            "authentication": "Gerekmez"
        },
        {
            "endpoint": "GET /api/user/profile",
            "method": "GET",
            "path": "/api/user/profile",
            "description": "Kullanıcı profili bilgileri",
            "response": {
                "success": "boolean",
                "data": "object (kullanıcı bilgileri)"
            },
            "authentication": "Bearer Token"
        },
        {
            "endpoint": "PUT /api/user/profile",
            "method": "PUT",
            "path": "/api/user/profile",
            "description": "Kullanıcı profili güncelleme",
            "request_body": {
                "first_name": "string",
                "last_name": "string",
                "email": "string",
                "phone": "string",
                "country": "string",
                "city": "string"
            },
            "response": {
                "success": "boolean",
                "message": "string",
                "data": "object (güncellenmiş kullanıcı bilgileri)"
            },
            "authentication": "Bearer Token"
        },
        {
            "endpoint": "GET /api/pets",
            "method": "GET",
            "path": "/api/pets",
            "description": "Kullanıcının evcil hayvanları",
            "response": {
                "success": "boolean",
                "data": "array (evcil hayvan listesi)"
            },
            "authentication": "Bearer Token"
        },
        {
            "endpoint": "POST /api/pets",
            "method": "POST",
            "path": "/api/pets",
            "description": "Yeni evcil hayvan ekleme",
            "request_body": {
                "name": "string (zorunlu)",
                "species": "string (zorunlu)",
                "breed": "string",
                "age": "integer",
                "gender": "string",
                "weight": "number",
                "health_conditions": "string",
                "behavioral_notes": "string"
            },
            "response": {
                "success": "boolean",
                "message": "string",
                "data": "object (eklenen evcil hayvan bilgileri)"
            },
            "authentication": "Bearer Token"
        },
        {
            "endpoint": "POST /api/analysis",
            "method": "POST",
            "path": "/api/analysis",
            "description": "Ses analizi yapma",
            "request_body": {
                "pet_id": "integer (zorunlu)",
                "sound_file": "file (zorunlu)",
                "context_situation": "string",
                "custom_context": "string"
            },
            "response": {
                "success": "boolean",
                "message": "string",
                "data": "object (analiz bilgileri)"
            },
            "authentication": "Bearer Token"
        },
        {
            "endpoint": "GET /api/analysis/{id}",
            "method": "GET",
            "path": "/api/analysis/{id}",
            "description": "Analiz sonucu detayları",
            "response": {
                "success": "boolean",
                "data": "object (analiz detayları)"
            },
            "authentication": "Bearer Token"
        },
        {
            "endpoint": "GET /api/analysis/history",
            "method": "GET",
            "path": "/api/analysis/history",
            "description": "Analiz geçmişi",
            "response": {
                "success": "boolean",
                "data": "array (analiz listesi)"
            },
            "authentication": "Bearer Token"
        }
    ]
    
    # Dokümantasyon içeriği
    docs_content = f"""# 🐾 PetVoice AI API Dokümantasyonu

Bu döküman, PetVoice AI uygulamasının REST API'sini açıklar.

## 📋 Genel Bilgiler

- **API Sürümü**: v1
- **Temel URL**: `http://localhost:5000/api`
- **İstek Formatı**: `application/json`
- **Yanıt Formatı**: `application/json`

## 🔐 Kimlik Doğrulama

API'ye erişim için JWT (JSON Web Token) kullanılır. Kimlik doğrulaması gerektiren endpoint'ler için `Authorization` header'ına `Bearer <token>` eklenmelidir.

### Token Alma

```bash
curl -X POST http://localhost:5000/api/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{{
    "username_or_email": "kullanici@example.com",
    "password": "sifre123"
  }}'
```

## 📡 API Endpoint'leri

"""
    
    # Her bir endpoint için dökümantasyon ekle
    for endpoint in api_endpoints:
        docs_content += f"""### {endpoint['endpoint']}

**Açıklama**: {endpoint['description']}

**HTTP Metodu**: `{endpoint['method']}`

**Yol**: `{endpoint['path']}`

**Kimlik Doğrulama**: {endpoint['authentication']}

"""
        
        if 'request_body' in endpoint:
            docs_content += "**İstek Gövdesi**:\n```json\n"
            docs_content += json.dumps(endpoint['request_body'], indent=2, ensure_ascii=False)
            docs_content += "\n```\n\n"
        
        if 'response' in endpoint:
            docs_content += "**Yanıt**:\n```json\n"
            docs_content += json.dumps(endpoint['response'], indent=2, ensure_ascii=False)
            docs_content += "\n```\n\n"
        
        docs_content += "---\n\n"
    
    # Ek bilgiler
    docs_content += """## 📤 Dosya Yükleme

Ses dosyası yüklemek için `multipart/form-data` formatı kullanılır.

Örnek:
```bash
curl -X POST http://localhost:5000/api/analysis \\
  -H "Authorization: Bearer <token>" \\
  -F "pet_id=1" \\
  -F "sound_file=@ses_dosyasi.wav" \\
  -F "context_situation=Oyun oynarken"
```

## 📈 Hata Kodları

| Kod | Açıklama |
|-----|----------|
| 200 | Başarılı istek |
| 400 | Geçersiz istek |
| 401 | Yetkisiz erişim |
| 404 | Kaynak bulunamadı |
| 500 | Sunucu hatası |

## 🔄 Rate Limiting

API, kullanıcı başına saatte 1000 istek ile sınırlıdır.

## 📞 Destek

Sorularınız için GitHub issues bölümünü kullanabilirsiniz.

*Dökümantasyon oluşturulma tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}*
"""
    
    # Dosyayı yaz
    docs_dir = 'docs'
    os.makedirs(docs_dir, exist_ok=True)
    
    docs_file = os.path.join(docs_dir, 'api_docs.md')
    with open(docs_file, 'w', encoding='utf-8') as f:
        f.write(docs_content)
    
    print(f"API dökümantasyonu oluşturuldu: {docs_file}")

def main():
    """Ana fonksiyon"""
    print("API dökümantasyonu oluşturuluyor...")
    generate_api_docs()
    print("Tamamlandı!")

if __name__ == '__main__':
    main()