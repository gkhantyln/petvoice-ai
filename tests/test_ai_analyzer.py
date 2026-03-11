# tests/test_ai_analyzer.py
# AI analiz fonksiyonları için birim testleri

import unittest
from unittest.mock import patch, mock_open
import numpy as np
from app.utils.ai_analyzer import create_advanced_analysis_prompt, get_cached_analysis, cache_analysis

class AIAnalyzerTestCase(unittest.TestCase):
    def setUp(self):
        """Test öncesi hazırlık"""
        pass

    def tearDown(self):
        """Test sonrası temizlik"""
        pass

    def test_create_advanced_analysis_prompt(self):
        """Gelişmiş analiz prompt'u oluşturma testi"""
        # Test verileri
        pet_data = type('Pet', (), {
            'species': 'Kedi',
            'age': 2,
            'gender': 'Erkek',
            'health_conditions': 'Sağlıklı'
        })()
        
        context_data = "Oyun oynarken"
        audio_features = {
            'duration': 5.0,
            'frequency_range': (0, 22050),
            'intensity': 0.5,
            'dominant_freq': 1000.0
        }
        
        # Prompt oluştur
        prompt = create_advanced_analysis_prompt(pet_data, context_data, audio_features)
        
        # Testler
        self.assertIn('Kedi', prompt)
        self.assertIn('Oyun oynarken', prompt)
        self.assertIn('5.0', prompt)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='{"analysis_text": "Test result"}')
    def test_get_cached_analysis(self, mock_file, mock_exists):
        """Önbellekten analiz sonucu alma testi"""
        # Dosya mevcut gibi davran
        mock_exists.return_value = True
        
        # Test verileri
        audio_features = {'duration': 5.0}
        pet_data = type('Pet', (), {'species': 'Kedi', 'age': 2})()
        context_data = "Oyun oynarken"
        
        # Önbellekten sonuç al
        result = get_cached_analysis(audio_features, pet_data, context_data)
        
        # Testler
        self.assertEqual(result, {"analysis_text": "Test result"})

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_cache_analysis(self, mock_file, mock_makedirs):
        """Analiz sonucunu önbelleğe alma testi"""
        # Test verileri
        audio_features = {'duration': 5.0}
        pet_data = type('Pet', (), {'species': 'Kedi', 'age': 2})()
        context_data = "Oyun oynarken"
        result = {"analysis_text": "Test result"}
        
        # Önbelleğe al
        cache_analysis(audio_features, pet_data, context_data, result)
        
        # open fonksiyonunun çağrıldığını kontrol et
        mock_file.assert_called()

if __name__ == '__main__':
    unittest.main()