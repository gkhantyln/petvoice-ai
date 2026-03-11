# app/views/auth.py
# Kimlik doğrulama view'ları
# Bu dosya, kullanıcı kayıt, giriş, çıkış ve profil işlemlerini içerir

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import re

# Blueprint oluştur
auth_bp = Blueprint('auth', __name__)

# Rate limiting uygulandı
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Kullanıcı kayıt sayfası"""
    # Rate limiting - view fonksiyonu içinde uygula
    from app import limiter
    limiter.limit("5 per minute")(lambda: None)()
    
    if request.method == 'POST':
        # Form verilerini al
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validasyon
        if not username or not email or not password:
            flash('Tüm alanlar zorunludur.', 'error')
            return render_template('auth/register.html')
        
        if len(username) < 3:
            flash('Kullanıcı adı en az 3 karakter olmalıdır.', 'error')
            return render_template('auth/register.html')
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Geçerli bir e-posta adresi girin.', 'error')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('Şifre en az 6 karakter olmalıdır.', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Şifreler eşleşmiyor.', 'error')
            return render_template('auth/register.html')
        
        # Kullanıcı adı veya e-posta zaten var mı kontrol et
        if User.query.filter_by(username=username).first():
            flash('Bu kullanıcı adı zaten kullanımda.', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Bu e-posta adresi zaten kullanımda.', 'error')
            return render_template('auth/register.html')
        
        # Yeni kullanıcı oluştur
        new_user = User(
            username=username,
            email=email,
            first_name=request.form.get('first_name', ''),
            last_name=request.form.get('last_name', ''),
            country=request.form.get('country', ''),
            city=request.form.get('city', '')
        )
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Kayıt sırasında bir hata oluştu.', 'error')
            current_app.logger.error(f"Kullanıcı kayıt hatası: {e}")
    
    return render_template('auth/register.html')

# Rate limiting uygulandı
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Kullanıcı giriş sayfası"""
    # Rate limiting - view fonksiyonu içinde uygula
    from app import limiter
    limiter.limit("10 per minute")(lambda: None)()
    
    if request.method == 'POST':
        # Form verilerini al
        username_or_email = request.form.get('username_or_email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        # Validasyon
        if not username_or_email or not password:
            flash('E-posta ve şifre alanları zorunludur.', 'error')
            return render_template('auth/login.html')
        
        # Kullanıcıyı e-posta veya kullanıcı adı ile bul
        user = User.query.filter(
            (User.email == username_or_email) | (User.username == username_or_email)
        ).first()
        
        # Kullanıcı yoksa veya şifre yanlışsa
        if not user or not user.check_password(password):
            flash('Geçersiz e-posta veya şifre.', 'error')
            return render_template('auth/login.html')
        
        # Kullanıcıyı oturum aç
        login_user(user, remember=remember)
        flash('Giriş başarılı!', 'success')
        
        # Yönlendirme
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Kullanıcı çıkış"""
    logout_user()
    flash('Çıkış yapıldı.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Kullanıcı profil sayfası"""
    if request.method == 'POST':
        # Form verilerini al
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        country = request.form.get('country')
        city = request.form.get('city')
        
        # E-posta benzersizliği kontrolü (kendisi hariç)
        if email != current_user.email:
            existing_user = User.query.filter(User.email == email, User.id != current_user.id).first()
            if existing_user:
                flash('Bu e-posta adresi zaten kullanımda.', 'error')
                return render_template('auth/profile.html')
        
        # Kullanıcı bilgilerini güncelle
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.email = email
        current_user.phone = phone
        current_user.country = country
        current_user.city = city
        
        try:
            db.session.commit()
            flash('Profil bilgileri güncellendi.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Profil güncelleme sırasında bir hata oluştu.', 'error')
            current_app.logger.error(f"Profil güncelleme hatası: {e}")
    
    return render_template('auth/profile.html')