# run_tests.py
# Test çalıştırıcı
# Bu dosya, tüm birim testlerini çalıştırır

import unittest
import sys
import os

# Proje kök dizinini Python path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    # Test keşfini yap
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test*.py')

    # Test çalıştırıcıyı oluştur
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Çıkış kodunu ayarla (başarısız test varsa 1, yoksa 0)
    sys.exit(not result.wasSuccessful())