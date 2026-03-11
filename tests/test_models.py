# tests/test_models.py
# Veritabanı modelleri için birim testleri

import unittest
from app import create_app, db
from app.models.models import User, Pet, SoundAnalysis

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        """Test öncesi hazırlık"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Test sonrası temizlik"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_model(self):
        """Kullanıcı modeli testi"""
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('password')
        
        db.session.add(user)
        db.session.commit()
        
        # Kullanıcıyı veritabanından al
        retrieved_user = User.query.filter_by(username='testuser').first()
        
        # Testler
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, 'test@example.com')
        self.assertTrue(retrieved_user.check_password('password'))
        self.assertFalse(retrieved_user.check_password('wrongpassword'))

    def test_pet_model(self):
        """Evcil hayvan modeli testi"""
        # Önce kullanıcı oluştur
        user = User(username='petowner', email='owner@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        # Evcil hayvan oluştur
        pet = Pet(
            user_id=user.id,
            name='Fluffy',
            species='Cat',
            breed='Persian',
            age=3,
            gender='Female'
        )
        
        db.session.add(pet)
        db.session.commit()
        
        # Evcil hayvanı veritabanından al
        retrieved_pet = Pet.query.filter_by(name='Fluffy').first()
        
        # Testler
        self.assertIsNotNone(retrieved_pet)
        self.assertEqual(retrieved_pet.species, 'Cat')
        self.assertEqual(retrieved_pet.owner.username, 'petowner')

    def test_sound_analysis_model(self):
        """Ses analizi modeli testi"""
        # Önce kullanıcı ve evcil hayvan oluştur
        user = User(username='analyst', email='analyst@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        pet = Pet(user_id=user.id, name='Buddy', species='Dog')
        db.session.add(pet)
        db.session.commit()
        
        # Ses analizi oluştur
        analysis = SoundAnalysis(
            user_id=user.id,
            pet_id=pet.id,
            unique_id='test123',
            file_path='/path/to/file.wav',
            analysis_status='processing'
        )
        
        db.session.add(analysis)
        db.session.commit()
        
        # Ses analizini veritabanından al
        retrieved_analysis = SoundAnalysis.query.filter_by(unique_id='test123').first()
        
        # Testler
        self.assertIsNotNone(retrieved_analysis)
        self.assertEqual(retrieved_analysis.analysis_status, 'processing')
        self.assertEqual(retrieved_analysis.pet.name, 'Buddy')
        self.assertEqual(retrieved_analysis.user.username, 'analyst')

if __name__ == '__main__':
    unittest.main()