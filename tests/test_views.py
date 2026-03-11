# tests/test_views.py
# View fonksiyonları için birim testleri

import unittest
from app import create_app, db
from app.models.models import User

class ViewTestCase(unittest.TestCase):
    def setUp(self):
        """Test öncesi hazırlık"""
        self.app = create_app('testing')
        self.app.config['WTF_CSRF_ENABLED'] = False  # CSRF korumasını devre dışı bırak
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Test sonrası temizlik"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_page(self):
        """Ana sayfa testi"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('PetVoice AI', response.get_data(as_text=True))

    def test_register_page(self):
        """Kayıt sayfası testi"""
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Kayıt Ol', response.get_data(as_text=True))

    def test_register_user(self):
        """Kullanıcı kayıt testi"""
        response = self.client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Kayıt başarılı!', response.get_data(as_text=True))
        
        # Kullanıcının veritabanına eklendiğini kontrol et
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')

    def test_login_page(self):
        """Giriş sayfası testi"""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Giriş Yap', response.get_data(as_text=True))

    def test_login_user(self):
        """Kullanıcı giriş testi"""
        # Önce kullanıcı oluştur
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # Kullanıcı ile giriş yap
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Giriş başarılı!', response.get_data(as_text=True))

    def test_protected_page_redirect(self):
        """Korunmuş sayfaya yönlendirme testi"""
        # Giriş yapmadan korunmuş bir sayfaya erişmeye çalış
        response = self.client.get('/analysis/upload', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Giriş Yap', response.get_data(as_text=True))  # Giriş sayfasına yönlendirilmeli

if __name__ == '__main__':
    unittest.main()