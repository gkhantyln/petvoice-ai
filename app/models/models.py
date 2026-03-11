# app/models/models.py
# Veritabanı modelleri
# Bu dosya, PostgreSQL şemasına göre oluşturulmuştur

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

# app modülünden db örneğini import et
from app import db

class User(UserMixin, db.Model):
    """Kullanıcılar tablosu"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    country = db.Column(db.String(50))
    city = db.Column(db.String(100))
    subscription_type = db.Column(db.String(20), default='free')  # free, premium, pro
    subscription_end_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    profile_image_url = db.Column(db.String(255))
    
    # İlişkiler
    pets = db.relationship('Pet', backref='owner', lazy=True, cascade='all, delete-orphan')
    analyses = db.relationship('SoundAnalysis', backref='user', lazy=True, cascade='all, delete-orphan')
    stats = db.relationship('AnalysisStat', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Şifreyi hash'ler"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Şifre doğrulama"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Pet(db.Model):
    """Evcil hayvan profilleri"""
    __tablename__ = 'pets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)  # cat, dog, bird, etc.
    breed = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    weight = db.Column(db.Numeric(5,2))
    health_conditions = db.Column(db.Text)
    behavioral_notes = db.Column(db.Text)
    profile_image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # İlişkiler
    analyses = db.relationship('SoundAnalysis', backref='pet', lazy=True, cascade='all, delete-orphan')
    stats = db.relationship('AnalysisStat', backref='pet', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Pet {self.name}>'

class SoundAnalysis(db.Model):
    """Ses kayıtları ve analizler"""
    __tablename__ = 'sound_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    unique_id = db.Column(db.String(50), unique=True, nullable=False)
    original_filename = db.Column(db.String(255))
    file_path = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)
    duration_seconds = db.Column(db.Numeric(6,2))
    sample_rate = db.Column(db.Integer)
    context_situation = db.Column(db.String(100))
    custom_context = db.Column(db.Text)
    ai_analysis = db.Column(db.Text)
    confidence_score = db.Column(db.Numeric(5,2))
    emotion_detected = db.Column(db.String(50))
    urgency_level = db.Column(db.String(20))  # low, medium, high, emergency
    veterinary_recommendation = db.Column(db.Text)
    spectrogram_path = db.Column(db.String(255))
    json_spectrogram_path = db.Column(db.String(255))  # Yeni eklenen alan
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    analysis_status = db.Column(db.String(20), default='processing')  # processing, completed, failed
    
    def __repr__(self):
        return f'<SoundAnalysis {self.unique_id}>'

class AnalysisStat(db.Model):
    """Analiz geçmişi istatistikleri"""
    __tablename__ = 'analysis_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    analysis_date = db.Column(db.Date)
    total_analyses = db.Column(db.Integer, default=0)
    emotion_breakdown = db.Column(db.JSON)  # {"happy": 5, "stressed": 2, "hungry": 3}
    average_confidence = db.Column(db.Numeric(5,2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AnalysisStat {self.analysis_date}>'

class AdminUser(db.Model):
    """Yönetici kullanıcıları"""
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(50), default='admin')  # admin, super_admin, moderator
    permissions = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AdminUser {self.user_id}>'

class SystemSetting(db.Model):
    """Sistem ayarları"""
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.Text)
    description = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SystemSetting {self.setting_key}>'

class SubscriptionPlan(db.Model):
    """Abonelik planları"""
    __tablename__ = 'subscription_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(8,2), nullable=False)
    currency = db.Column(db.String(3), default='USD')
    duration_months = db.Column(db.Integer, default=1)
    max_analyses_per_month = db.Column(db.Integer)
    features = db.Column(db.JSON)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SubscriptionPlan {self.name}>'