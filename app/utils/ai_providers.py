# app/utils/ai_providers.py
# Multi-provider AI analiz sistemi
# Bu dosya, farklı AI provider'ları destekler ve failover mekanizması sağlar

import os
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class AIProvider(ABC):
    """AI Provider için temel sınıf"""
    
    def __init__(self, api_key: str, name: str):
        self.api_key = api_key
        self.name = name
        self.is_available = False
        
    @abstractmethod
    def configure(self) -> bool:
        """Provider'ı yapılandırır"""
        pass
    
    @abstractmethod
    def analyze_audio(self, audio_path: str, prompt: str) -> Dict[str, Any]:
        """Ses dosyasını analiz eder"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """API bağlantısını test eder"""
        pass


class GeminiProvider(AIProvider):
    """Google Gemini AI Provider"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "Google Gemini")
        self.model_name = "gemini-2.5-flash"
        self.model = None
        
    def configure(self) -> bool:
        """Gemini'yi yapılandırır"""
        try:
            if not self.api_key or self.api_key in ["YOUR_API_KEY", "BURAYA_YENİ_API_ANAHTARINIZI_YAPIŞTIRIN"]:
                return False
                
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            self.is_available = True
            return True
        except Exception as e:
            print(f"Gemini yapılandırma hatası: {e}")
            self.is_available = False
            return False
    
    def analyze_audio(self, audio_path: str, prompt: str) -> Dict[str, Any]:
        """Gemini ile ses analizi yapar"""
        try:
            # Ses dosyasını oku
            with open(audio_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Analiz yap
            response = self.model.generate_content([
                prompt,
                {
                    'mime_type': 'audio/wav',
                    'data': audio_data
                }
            ])
            
            return {
                'success': True,
                'provider': self.name,
                'analysis': response.text
            }
        except Exception as e:
            return {
                'success': False,
                'provider': self.name,
                'error': str(e)
            }
    
    def test_connection(self) -> bool:
        """Gemini bağlantısını test eder"""
        try:
            if not self.model:
                return False
            # Basit bir test isteği
            response = self.model.generate_content("Test")
            return True
        except Exception as e:
            print(f"Gemini bağlantı testi başarısız: {e}")
            return False


class OpenAIProvider(AIProvider):
    """OpenAI Provider (GPT-4 Audio)"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "OpenAI")
        self.model_name = "gpt-4o-audio-preview"
        self.client = None
        
    def configure(self) -> bool:
        """OpenAI'yi yapılandırır"""
        try:
            if not self.api_key or self.api_key in ["YOUR_API_KEY", "BURAYA_YENİ_API_ANAHTARINIZI_YAPIŞTIRIN"]:
                return False
            
            # OpenAI client'ı import et
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                self.is_available = True
                return True
            except ImportError:
                print("OpenAI kütüphanesi yüklü değil. 'pip install openai' ile yükleyin.")
                return False
        except Exception as e:
            print(f"OpenAI yapılandırma hatası: {e}")
            self.is_available = False
            return False
    
    def analyze_audio(self, audio_path: str, prompt: str) -> Dict[str, Any]:
        """OpenAI ile ses analizi yapar"""
        try:
            # Ses dosyasını oku
            with open(audio_path, 'rb') as audio_file:
                # OpenAI Audio API kullanımı
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "input_audio",
                                    "input_audio": {
                                        "data": audio_file.read(),
                                        "format": "wav"
                                    }
                                }
                            ]
                        }
                    ]
                )
            
            return {
                'success': True,
                'provider': self.name,
                'analysis': response.choices[0].message.content
            }
        except Exception as e:
            return {
                'success': False,
                'provider': self.name,
                'error': str(e)
            }
    
    def test_connection(self) -> bool:
        """OpenAI bağlantısını test eder"""
        try:
            if not self.client:
                return False
            # Basit bir test isteği
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            print(f"OpenAI bağlantı testi başarısız: {e}")
            return False


class AnthropicProvider(AIProvider):
    """Anthropic Claude Provider"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "Anthropic Claude")
        self.model_name = "claude-3-5-sonnet-20241022"
        self.client = None
        
    def configure(self) -> bool:
        """Anthropic'i yapılandırır"""
        try:
            if not self.api_key or self.api_key in ["YOUR_API_KEY", "BURAYA_YENİ_API_ANAHTARINIZI_YAPIŞTIRIN"]:
                return False
            
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=self.api_key)
                self.is_available = True
                return True
            except ImportError:
                print("Anthropic kütüphanesi yüklü değil. 'pip install anthropic' ile yükleyin.")
                return False
        except Exception as e:
            print(f"Anthropic yapılandırma hatası: {e}")
            self.is_available = False
            return False
    
    def analyze_audio(self, audio_path: str, prompt: str) -> Dict[str, Any]:
        """Claude ile ses analizi yapar"""
        try:
            import base64
            
            # Ses dosyasını base64'e çevir
            with open(audio_path, 'rb') as audio_file:
                audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
            
            # Claude API çağrısı
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "document",
                                "source": {
                                    "type": "base64",
                                    "media_type": "audio/wav",
                                    "data": audio_data
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )
            
            return {
                'success': True,
                'provider': self.name,
                'analysis': response.content[0].text
            }
        except Exception as e:
            return {
                'success': False,
                'provider': self.name,
                'error': str(e)
            }
    
    def test_connection(self) -> bool:
        """Claude bağlantısını test eder"""
        try:
            if not self.client:
                return False
            # Basit bir test isteği
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=10,
                messages=[{"role": "user", "content": "Test"}]
            )
            return True
        except Exception as e:
            print(f"Claude bağlantı testi başarısız: {e}")
            return False


class MultiProviderManager:
    """Çoklu AI provider yöneticisi - Failover desteği ile"""
    
    def __init__(self):
        self.providers: List[AIProvider] = []
        self.active_provider: Optional[AIProvider] = None
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Tüm provider'ları başlatır"""
        # Gemini provider
        gemini_keys = self._get_api_keys('GOOGLE_API_KEY')
        for i, key in enumerate(gemini_keys):
            provider = GeminiProvider(key)
            if provider.configure():
                self.providers.append(provider)
                print(f"✓ Gemini Provider #{i+1} aktif")
        
        # OpenAI provider
        openai_keys = self._get_api_keys('OPENAI_API_KEY')
        for i, key in enumerate(openai_keys):
            provider = OpenAIProvider(key)
            if provider.configure():
                self.providers.append(provider)
                print(f"✓ OpenAI Provider #{i+1} aktif")
        
        # Anthropic provider
        anthropic_keys = self._get_api_keys('ANTHROPIC_API_KEY')
        for i, key in enumerate(anthropic_keys):
            provider = AnthropicProvider(key)
            if provider.configure():
                self.providers.append(provider)
                print(f"✓ Anthropic Provider #{i+1} aktif")
        
        # İlk aktif provider'ı seç
        if self.providers:
            self.active_provider = self.providers[0]
            print(f"\n🎯 Aktif Provider: {self.active_provider.name}")
        else:
            print("\n⚠️ Hiçbir AI provider yapılandırılamadı!")
    
    def _get_api_keys(self, key_prefix: str) -> List[str]:
        """Ortam değişkenlerinden API anahtarlarını alır (çoklu destekli)"""
        keys = []
        
        # Tek anahtar
        single_key = os.getenv(key_prefix)
        if single_key and single_key not in ["YOUR_API_KEY", "BURAYA_YENİ_API_ANAHTARINIZI_YAPIŞTIRIN", ""]:
            keys.append(single_key)
        
        # Çoklu anahtarlar (KEY_1, KEY_2, ...)
        i = 1
        while True:
            multi_key = os.getenv(f"{key_prefix}_{i}")
            if multi_key and multi_key not in ["YOUR_API_KEY", "BURAYA_YENİ_API_ANAHTARINIZI_YAPIŞTIRIN", ""]:
                keys.append(multi_key)
                i += 1
            else:
                break
        
        return keys
    
    def analyze_with_fallback(self, audio_path: str, prompt: str) -> Dict[str, Any]:
        """
        Ses analizini yapar, hata durumunda otomatik olarak diğer provider'a geçer
        """
        if not self.providers:
            return {
                'success': False,
                'error': 'Hiçbir AI provider yapılandırılmamış',
                'provider': None
            }
        
        # Tüm provider'ları dene
        errors = []
        for provider in self.providers:
            try:
                print(f"🔄 {provider.name} ile analiz deneniyor...")
                result = provider.analyze_audio(audio_path, prompt)
                
                if result['success']:
                    print(f"✓ {provider.name} ile analiz başarılı!")
                    self.active_provider = provider
                    return result
                else:
                    error_msg = f"{provider.name}: {result.get('error', 'Bilinmeyen hata')}"
                    errors.append(error_msg)
                    print(f"✗ {error_msg}")
            except Exception as e:
                error_msg = f"{provider.name}: {str(e)}"
                errors.append(error_msg)
                print(f"✗ {error_msg}")
        
        # Hiçbir provider çalışmadı
        return {
            'success': False,
            'error': 'Tüm AI provider\'lar başarısız oldu',
            'provider': None,
            'details': errors
        }
    
    def get_available_providers(self) -> List[str]:
        """Kullanılabilir provider'ların listesini döndürür"""
        return [p.name for p in self.providers if p.is_available]
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Tüm provider'ların durumunu döndürür"""
        return {
            'total': len(self.providers),
            'active': len([p for p in self.providers if p.is_available]),
            'current': self.active_provider.name if self.active_provider else None,
            'providers': [
                {
                    'name': p.name,
                    'available': p.is_available
                }
                for p in self.providers
            ]
        }


# Global manager instance
_manager_instance = None


def get_ai_manager() -> MultiProviderManager:
    """Global AI manager instance'ını döndürür"""
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = MultiProviderManager()
    return _manager_instance
