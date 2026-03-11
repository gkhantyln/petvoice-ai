# simple_init_db.py
# Basit veritabanı başlatıcı
# Bu dosya, veritabanını oluşturur ve örnek verileri ekler

import os
import sys
from app import create_app, db

def init_database():
    """Veritabanını başlatır ve örnek verileri ekler"""
    # Uygulamayı oluştur
    os.environ.setdefault('FLASK_CONFIG', 'development')
    app = create_app()
    
    with app.app_context():
        # Modelleri içe aktar (app context içinde olmalı)
        from app.models.models import User, Pet, SoundAnalysis, AdminUser, SubscriptionPlan, SystemSetting
        
        # Tüm tabloları oluştur
        db.create_all()
        print("Veritabanı tabloları oluşturuldu.")
        
        # Örnek abonelik planları ekle
        if not SubscriptionPlan.query.first():
            free_plan = SubscriptionPlan(
                name='Ücretsiz',
                price=0.00,
                currency='USD',
                duration_months=1,
                max_analyses_per_month=5,
                features={
                    'max_pets': 1,
                    'ai_analysis': True,
                    'report_export': False,
                    'priority_support': False
                },
                is_active=True
            )
            
            premium_plan = SubscriptionPlan(
                name='Premium',
                price=9.99,
                currency='USD',
                duration_months=1,
                max_analyses_per_month=50,
                features={
                    'max_pets': 5,
                    'ai_analysis': True,
                    'report_export': True,
                    'priority_support': True
                },
                is_active=True
            )
            
            pro_plan = SubscriptionPlan(
                name='Profesyonel',
                price=29.99,
                currency='USD',
                duration_months=1,
                max_analyses_per_month=-1,  # Sınırsız
                features={
                    'max_pets': -1,  # Sınırsız
                    'ai_analysis': True,
                    'report_export': True,
                    'priority_support': True,
                    'veterinary_consultation': True
                },
                is_active=True
            )
            
            db.session.add_all([free_plan, premium_plan, pro_plan])
            print("Abonelik planları eklendi.")
        
        # Örnek sistem ayarları ekle
        if not SystemSetting.query.first():
            settings = [
                SystemSetting(
                    setting_key='site_name',
                    setting_value='PetVoice AI',
                    description='Site adı'
                ),
                SystemSetting(
                    setting_key='site_description',
                    setting_value='Hayvan ses analizi platformu',
                    description='Site açıklaması'
                ),
                SystemSetting(
                    setting_key='max_file_size',
                    setting_value='16777216',  # 16MB
                    description='Maksimum dosya boyutu (byte)'
                ),
                SystemSetting(
                    setting_key='supported_formats',
                    setting_value='wav,mp3,ogg,flac',
                    description='Desteklenen ses formatları'
                )
            ]
            
            db.session.add_all(settings)
            print("Sistem ayarları eklendi.")
        
        # Örnek yönetici kullanıcı ekle
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                email='admin@petvoice.ai',
                first_name='Admin',
                last_name='Kullanıcı'
            )
            admin_user.set_password('admin123')
            
            db.session.add(admin_user)
            db.session.flush()  # ID'yi almak için
            
            # Yönetici kullanıcıyı oluştur
            admin = AdminUser(
                user_id=admin_user.id,
                role='super_admin',
                permissions={
                    'manage_users': True,
                    'manage_content': True,
                    'manage_settings': True,
                    'view_reports': True
                }
            )
            
            db.session.add(admin)
            print("Yönetici kullanıcı eklendi.")
        
        # Değişiklikleri kaydet
        try:
            db.session.commit()
            print("Veritabanı başlatıldı ve örnek veriler eklendi.")
        except Exception as e:
            db.session.rollback()
            print(f"Veritabanı başlatılırken hata oluştu: {e}")

if __name__ == '__main__':
    init_database()