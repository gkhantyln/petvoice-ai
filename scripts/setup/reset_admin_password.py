# reset_admin_password.py
# Admin şifresini sıfırlamak için yardımcı script

import os
from app import create_app, db
from app.models.models import User

def reset_admin_password():
    """Admin kullanıcısının şifresini sıfırlar"""
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    
    with app.app_context():
        # Admin kullanıcısını bul
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("❌ Admin kullanıcısı bulunamadı!")
            print("Mevcut kullanıcılar:")
            users = User.query.all()
            for user in users:
                print(f"  - {user.username} ({user.email})")
            return
        
        # Yeni şifre iste
        print(f"✓ Admin kullanıcısı bulundu: {admin.username} ({admin.email})")
        print("\nYeni şifre belirleyin:")
        new_password = input("Yeni şifre: ")
        
        if len(new_password) < 6:
            print("❌ Şifre en az 6 karakter olmalıdır!")
            return
        
        # Şifreyi güncelle
        admin.set_password(new_password)
        db.session.commit()
        
        print(f"\n✓ Şifre başarıyla güncellendi!")
        print(f"Kullanıcı adı: {admin.username}")
        print(f"Yeni şifre: {new_password}")

if __name__ == '__main__':
    reset_admin_password()
