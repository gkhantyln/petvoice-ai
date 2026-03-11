# app/views/main.py
# Ana view'lar ve dashboard
# Bu dosya, ana sayfa, dashboard ve genel uygulama view'larını içerir

from flask import Blueprint, render_template, current_app, redirect, url_for, send_from_directory
from flask_login import login_required, current_user
from app.models.models import db, Pet, SoundAnalysis
import os

# Blueprint oluştur
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Ana sayfa"""
    # Kullanıcı giriş yapmışsa dashboard'a yönlendir
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    return render_template('main/index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Kullanıcı dashboard sayfası"""
    # Kullanıcının evcil hayvanlarını getir
    pets = Pet.query.filter_by(user_id=current_user.id, is_active=True).all()
    
    # Son analizleri getir
    recent_analyses = SoundAnalysis.query.filter_by(user_id=current_user.id)\
        .order_by(SoundAnalysis.created_at.desc()).limit(5).all()
    
    # Dashboard verilerini hazırla
    dashboard_data = {
        'total_pets': len(pets),
        'total_analyses': SoundAnalysis.query.filter_by(user_id=current_user.id).count(),
        'recent_analyses': recent_analyses
    }
    
    return render_template('main/dashboard.html', pets=pets, dashboard_data=dashboard_data)

@main_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Upload edilen dosyaları serve eder"""
    # Upload klasörünü al ve absolute path yap
    upload_folder = current_app.config['UPLOAD_FOLDER']
    upload_folder = os.path.abspath(upload_folder)
    
    # Normalize the filename to handle both forward slashes and backslashes
    normalized_filename = filename.replace('/', os.sep).replace('\\', os.sep)
    
    # Tam dosya yolunu oluştur
    file_path = os.path.join(upload_folder, normalized_filename)
    
    # Debug logging
    current_app.logger.info(f"Trying to serve file: {filename}")
    current_app.logger.info(f"Upload folder: {upload_folder}")
    current_app.logger.info(f"Normalized filename: {normalized_filename}")
    current_app.logger.info(f"Full file path: {file_path}")
    current_app.logger.info(f"File exists: {os.path.exists(file_path)}")
    
    # Dosya var mı kontrol et
    if not os.path.exists(file_path):
        # Dosya bulunamadı hatası döndür
        current_app.logger.error(f"File not found: {file_path}")
        return "File not found", 404
    
    # Send the file directly using send_file
    from flask import send_file
    current_app.logger.info(f"Serving file with send_file: {file_path}")
    return send_file(file_path)

@main_bp.route('/about')
def about():
    """Hakkında sayfası"""
    return render_template('main/about.html')

@main_bp.route('/contact')
def contact():
    """İletişim sayfası"""
    return render_template('main/contact.html')