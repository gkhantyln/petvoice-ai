# app/views/admin.py
# Yönetici paneli view'ları
# Bu dosya, yönetici işlemlerini içerir

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models.models import db, User, Pet, SoundAnalysis, AdminUser, SubscriptionPlan, SystemSetting
from datetime import datetime
from functools import wraps

# Blueprint oluştur
admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Yönetici kullanıcı kontrol decorator'ı"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Kullanıcının admin olup olmadığını kontrol et
        admin_user = AdminUser.query.filter_by(user_id=current_user.id).first()
        if not admin_user:
            flash('Bu sayfaya erişim izniniz yok.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin')
@login_required
@admin_required
def dashboard():
    """Yönetici dashboard"""
    # İstatistikleri hesapla
    stats = {
        'total_users': User.query.count(),
        'total_pets': Pet.query.count(),
        'total_analyses': SoundAnalysis.query.count(),
        'active_users': User.query.filter_by(is_active=True).count()
    }
    
    # Son kullanıcıları getir
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', stats=stats, recent_users=recent_users)

@admin_bp.route('/admin/users')
@login_required
@admin_required
def users():
    """Kullanıcı yönetimi"""
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/admin/users/<int:user_id>/toggle-active', methods=['POST'])
@login_required
@admin_required
def toggle_user_active(user_id):
    """Kullanıcı aktif/pasif durumunu değiştir"""
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    status = "aktif" if user.is_active else "pasif"
    flash(f'Kullanıcı {status} duruma getirildi.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/admin/subscription-plans')
@login_required
@admin_required
def subscription_plans():
    """Abonelik planları yönetimi"""
    plans = SubscriptionPlan.query.all()
    return render_template('admin/subscription_plans.html', plans=plans)

@admin_bp.route('/admin/subscription-plans/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_subscription_plan():
    """Yeni abonelik planı ekle"""
    if request.method == 'POST':
        # Form verilerini al
        name = request.form.get('name')
        price = float(request.form.get('price'))
        currency = request.form.get('currency', 'USD')
        duration_months = int(request.form.get('duration_months'))
        max_analyses = int(request.form.get('max_analyses'))
        is_active = bool(request.form.get('is_active'))
        
        # Yeni plan oluştur
        plan = SubscriptionPlan(
            name=name,
            price=price,
            currency=currency,
            duration_months=duration_months,
            max_analyses_per_month=max_analyses,
            is_active=is_active
        )
        
        try:
            db.session.add(plan)
            db.session.commit()
            flash('Abonelik planı eklendi.', 'success')
            return redirect(url_for('admin.subscription_plans'))
        except Exception as e:
            db.session.rollback()
            flash('Abonelik planı eklenirken bir hata oluştu.', 'error')
            current_app.logger.error(f"Abonelik planı ekleme hatası: {e}")
    
    return render_template('admin/add_subscription_plan.html')

@admin_bp.route('/admin/system-settings')
@login_required
@admin_required
def system_settings():
    """Sistem ayarları"""
    settings = SystemSetting.query.all()
    return render_template('admin/system_settings.html', settings=settings)

@admin_bp.route('/admin/system-settings/update', methods=['POST'])
@login_required
@admin_required
def update_system_settings():
    """Sistem ayarlarını güncelle"""
    # Tüm ayarları güncelle
    for key, value in request.form.items():
        if key.startswith('setting_'):
            setting_key = key.replace('setting_', '')
            setting = SystemSetting.query.filter_by(setting_key=setting_key).first()
            if setting:
                setting.setting_value = value
                setting.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        flash('Sistem ayarları güncellendi.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ayarlar güncellenirken bir hata oluştu.', 'error')
        current_app.logger.error(f"Sistem ayarları güncelleme hatası: {e}")
    
    return redirect(url_for('admin.system_settings'))

@admin_bp.route('/admin/ai-providers')
@login_required
@admin_required
def ai_providers():
    """AI Provider durumlarını gösterir"""
    from app.utils.ai_providers import get_ai_manager
    
    manager = get_ai_manager()
    status = manager.get_provider_status()
    
    return render_template('admin/ai_providers.html', status=status)
