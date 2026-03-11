# tests/test_sound_processor.py
# Ses işleme fonksiyonları için birim testleri

import unittest
from unittest.mock import patch, mock_open
import numpy as np
from app.utils.sound_processor import get_audio_features

class SoundProcessorTestCase(unittest.TestCase):
    def setUp(self):
        """Test öncesi hazırlık"""
        pass

    def tearDown(self):
        """Test sonrası temizlik"""
        pass

    def test_get_audio_features(self):
        """Ses özelliklerini çıkarma testi"""
        # Test verileri
        data = np.array([1, 2, 3, 4, 5])
        sample_rate = 44100
        
        # Özellikleri çıkar
        features = get_audio_features(data, sample_rate)
        
        # Testler
        self.assertIn('duration', features)
        self.assertIn('frequency_range', features)
        self.assertIn('intensity', features)
        self.assertIn('dominant_freq', features)
        self.assertGreaterEqual(features['duration'], 0)
        self.assertEqual(features['frequency_range'], (0, sample_rate / 2))

if __name__ == '__main__':
    unittest.main()