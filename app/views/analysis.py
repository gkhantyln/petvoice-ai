# app/views/analysis.py
# Ses analizi view'ları
# Bu dosya, ses yükleme, analiz ve sonuç görüntüleme işlemlerini içerir

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from app.models.models import db, Pet, SoundAnalysis
from app.utils.sound_processor import process_sound_file, generate_spectrogram
from app.utils.ai_analyzer import analyze_with_gemini
# Task import'unu fonksiyon içine taşı
import os
from datetime import datetime
import uuid

# Blueprint oluştur
analysis_bp = Blueprint('analysis', __name__)

def get_analyze_sound_task():
    """Analiz görevini döndürür"""
    from app.tasks import analyze_sound_task
    return analyze_sound_task

def get_socketio():
    """SocketIO nesnesini döndürür"""
    from app import socketio
    return socketio

@analysis_bp.route('/pets')
@login_required
def pets():
    """Kullanıcının evcil hayvanları sayfası"""
    pets = Pet.query.filter_by(user_id=current_user.id, is_active=True).all()
    return render_template('analysis/pets.html', pets=pets)

@analysis_bp.route('/pets/add', methods=['GET', 'POST'])
@login_required
def add_pet():
    """Yeni evcil hayvan ekleme"""
    if request.method == 'POST':
        # Form verilerini al
        name = request.form.get('name')
        species = request.form.get('species')
        breed = request.form.get('breed')
        age = request.form.get('age')
        gender = request.form.get('gender')
        weight = request.form.get('weight')
        health_conditions = request.form.get('health_conditions')
        behavioral_notes = request.form.get('behavioral_notes')
        
        # Yeni pet oluştur
        new_pet = Pet(
            user_id=current_user.id,
            name=name,
            species=species,
            breed=breed,
            age=int(age) if age else None,
            gender=gender,
            weight=float(weight) if weight else None,
            health_conditions=health_conditions,
            behavioral_notes=behavioral_notes
        )
        
        try:
            db.session.add(new_pet)
            db.session.commit()
            flash(f'{name} adlı evcil hayvan eklendi.', 'success')
            return redirect(url_for('analysis.pets'))
        except Exception as e:
            db.session.rollback()
            flash('Evcil hayvan eklenirken bir hata oluştu.', 'error')
            current_app.logger.error(f"Evcil hayvan ekleme hatası: {e}")
    
    return render_template('analysis/add_pet.html')

@analysis_bp.route('/pets/edit/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def edit_pet(pet_id):
    """Evcil hayvan düzenleme"""
    # Pet'i veritabanından getir ve kullanıcının olup olmadığını kontrol et
    pet = Pet.query.filter_by(id=pet_id, user_id=current_user.id, is_active=True).first()
    
    if not pet:
        flash('İstenen evcil hayvan bulunamadı.', 'error')
        return redirect(url_for('analysis.pets'))
    
    if request.method == 'POST':
        # Form verilerini al
        name = request.form.get('name')
        species = request.form.get('species')
        breed = request.form.get('breed')
        age = request.form.get('age')
        gender = request.form.get('gender')
        weight = request.form.get('weight')
        health_conditions = request.form.get('health_conditions')
        behavioral_notes = request.form.get('behavioral_notes')
        
        # Pet bilgilerini güncelle
        pet.name = name
        pet.species = species
        pet.breed = breed
        pet.age = int(age) if age else None
        pet.gender = gender
        pet.weight = float(weight) if weight else None
        pet.health_conditions = health_conditions
        pet.behavioral_notes = behavioral_notes
        
        try:
            db.session.commit()
            flash(f'{name} adlı evcil hayvan güncellendi.', 'success')
            return redirect(url_for('analysis.pets'))
        except Exception as e:
            db.session.rollback()
            flash('Evcil hayvan güncellenirken bir hata oluştu.', 'error')
            current_app.logger.error(f"Evcil hayvan güncelleme hatası: {e}")
    
    return render_template('analysis/edit_pet.html', pet=pet)

@analysis_bp.route('/analysis/upload', methods=['GET', 'POST'])
@login_required
def upload_sound():
    """Ses dosyası yükleme ve analiz"""
    # Rate limiting - view fonksiyonu içinde uygula
    from app import limiter
    limiter.limit("10 per minute")(lambda: None)()
    
    # Kullanıcının evcil hayvanlarını getir
    pets = Pet.query.filter_by(user_id=current_user.id, is_active=True).all()
    
    if request.method == 'POST':
        try:
            # Form verilerini al
            pet_id = request.form.get('pet_id')
            context_situation = request.form.get('context_situation')
            custom_context = request.form.get('custom_context')
            
            # Validasyon
            if not pet_id:
                flash('Lütfen bir evcil hayvan seçin.', 'error')
                return render_template('analysis/upload.html', pets=pets)
            
            # Ses dosyasını al
            if 'sound_file' not in request.files:
                flash('Lütfen bir ses dosyası seçin.', 'error')
                return render_template('analysis/upload.html', pets=pets)
            
            sound_file = request.files['sound_file']
            if sound_file.filename == '':
                flash('Lütfen bir ses dosyası seçin.', 'error')
                return render_template('analysis/upload.html', pets=pets)
            
            # Dosya uzantısı kontrolü
            allowed_extensions = {'wav', 'mp3', 'ogg', 'flac'}
            if '.' not in sound_file.filename or \
               sound_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                flash('Lütfen geçerli bir ses dosyası seçin (wav, mp3, ogg, flac).', 'error')
                return render_template('analysis/upload.html', pets=pets)
            
            # Dosya boyutu kontrolü (16MB)
            sound_file.seek(0, os.SEEK_END)
            file_size = sound_file.tell()
            sound_file.seek(0)
            
            if file_size > 16 * 1024 * 1024:
                flash('Dosya boyutu 16MB\'dan büyük olamaz.', 'error')
                return render_template('analysis/upload.html', pets=pets)
            
            # Benzersiz ID oluştur
            unique_id = str(uuid.uuid4())[:8] + datetime.now().strftime('%Y%m%d%H%M%S')
            
            # Dosya yollarını oluştur - Windows uyumlu hale getirildi
            upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sounds')
            # Windows'ta dizin yollarını doğru şekilde oluşturmak için
            upload_dir = os.path.abspath(upload_dir)
            os.makedirs(upload_dir, exist_ok=True)
            
            filename = f"sound_{unique_id}.{sound_file.filename.rsplit('.', 1)[1].lower()}"
            file_path = os.path.join(upload_dir, filename)
            # Windows uyumluluğu için tam yol kullan
            file_path = os.path.abspath(file_path)
            
            # Dosyayı kaydet
            sound_file.save(file_path)
            
            # Veritabanına kaydet (analiz durumu: processing)
            analysis = SoundAnalysis(
                user_id=current_user.id,
                pet_id=int(pet_id),
                unique_id=unique_id,
                original_filename=sound_file.filename,
                file_path=file_path,
                file_size=file_size,
                context_situation=context_situation,
                custom_context=custom_context,
                analysis_status='processing'
            )
            
            db.session.add(analysis)
            db.session.commit()
            
            # Doğrudan analiz yap (senkron)
            try:
                from app.utils.sound_processor import process_sound_file, generate_interactive_spectrogram, is_ffmpeg_available
                from app.utils.ai_analyzer import analyze_with_gemini
                from app.utils.task_utils import update_analysis_result
                import traceback
                
                current_app.logger.info(f"Analiz başlatılıyor: {file_path}")
                
                # Ses dosyasını işle
                current_app.logger.info("Ses dosyası işleniyor...")
                try:
                    processed_data = process_sound_file(file_path)
                    current_app.logger.info(f"İşlenen veri: {processed_data.keys() if processed_data else 'None'}")
                except Exception as e:
                    current_app.logger.error(f"Ses işleme hatası: {e}")
                    current_app.logger.error(traceback.format_exc())
                    raise Exception(f"Ses dosyası işlenemedi: {str(e)}")
                
                # Spektrogram oluştur
                current_app.logger.info("Spektrogram oluşturuluyor...")
                spectrogram_dir = os.path.join(os.path.dirname(file_path), '..', 'spectrograms')
                # Windows uyumluluğu için tam yol kullan
                spectrogram_dir = os.path.abspath(spectrogram_dir)
                os.makedirs(spectrogram_dir, exist_ok=True)
                unique_id = os.path.basename(file_path).split('_')[1].split('.')[0]
                spectrogram_path = os.path.join(spectrogram_dir, f"spectrogram_{unique_id}.png")
                # Windows uyumluluğu için tam yol kullan
                spectrogram_path = os.path.abspath(spectrogram_path)
                
                # Spektrogram oluşturma işlemini try-except bloğuna al
                try:
                    basic_spectrogram_path, json_spectrogram_path = generate_interactive_spectrogram(
                        processed_data['data'], processed_data['sample_rate'], spectrogram_path
                    )
                    current_app.logger.info(f"Spektrogram oluşturuldu: {basic_spectrogram_path}, {json_spectrogram_path}")
                except Exception as e:
                    current_app.logger.error(f"Spektrogram oluşturma hatası: {e}")
                    current_app.logger.error(traceback.format_exc())
                    basic_spectrogram_path = None
                    json_spectrogram_path = None
                
                # AI analizi yap - WAV dosyasını kullan
                current_app.logger.info("AI analizi yapılıyor...")
                try:
                    # processed_data['file_path'] zaten WAV formatında
                    ai_result = analyze_with_gemini(processed_data['file_path'], int(pet_id), context_situation, custom_context)
                    current_app.logger.info(f"AI analizi tamamlandı: {type(ai_result)}")
                    
                    # AI sonucunu string olarak al (dictionary ise 'ai_analysis' anahtarını kullan)
                    if isinstance(ai_result, dict):
                        ai_analysis_text = ai_result.get('ai_analysis', str(ai_result))
                    else:
                        ai_analysis_text = str(ai_result)
                except Exception as e:
                    current_app.logger.error(f"AI analizi hatası: {e}")
                    
                    # Kullanıcı dostu hata mesajı
                    error_str = str(e)
                    if "API_KEY_INVALID" in error_str or "API key not valid" in error_str:
                        ai_analysis_text = """## ⚠️ API Anahtarı Hatası

Google Gemini API anahtarınız geçersiz veya süresi dolmuş.

### Çözüm:
1. [Google AI Studio](https://aistudio.google.com/app/apikey) adresinden yeni bir API anahtarı alın
2. `.env` dosyasındaki `GOOGLE_API_KEY` değerini güncelleyin
3. Uygulamayı yeniden başlatın

Lütfen sistem yöneticinizle iletişime geçin."""
                        flash('API anahtarı geçersiz. Lütfen sistem yöneticisiyle iletişime geçin.', 'error')
                    elif "quota" in error_str.lower() or "limit" in error_str.lower():
                        ai_analysis_text = """## ⚠️ API Kullanım Limiti Aşıldı

Google Gemini API kullanım limitiniz dolmuş.

### Çözüm:
- Birkaç dakika bekleyip tekrar deneyin
- Veya API kotanızı artırın

Lütfen sistem yöneticinizle iletişime geçin."""
                        flash('API kullanım limiti aşıldı. Lütfen daha sonra tekrar deneyin.', 'error')
                    else:
                        ai_analysis_text = f"""## ⚠️ Analiz Hatası

Ses analizi sırasında bir hata oluştu.

### Hata Detayı:
{error_str[:200]}...

Lütfen daha sonra tekrar deneyin veya sistem yöneticinizle iletişime geçin."""
                        flash('Ses analizi sırasında bir hata oluştu. Lütfen tekrar deneyin.', 'error')
                
                # Sonuçları veritabanında güncelle
                result_data = {
                    'status': 'Tamamlandı',
                    'analysis_id': analysis.id,
                    'ai_analysis': ai_analysis_text,
                    'spectrogram_path': basic_spectrogram_path,
                    'json_spectrogram_path': json_spectrogram_path
                }
                
                update_analysis_result(analysis.id, result_data)
                current_app.logger.info("Veritabanı güncellendi")
                
                flash('Ses analizi tamamlandı.', 'success')
            except Exception as e:
                error_msg = f'Ses analizi sırasında bir hata oluştu: {str(e)}'
                current_app.logger.error(error_msg)
                current_app.logger.error(traceback.format_exc())
                
                # Analiz durumunu hata olarak güncelle
                try:
                    analysis.analysis_status = 'failed'
                    analysis.ai_analysis = f"## ⚠️ Analiz Başarısız\n\n{error_msg}"
                    db.session.commit()
                except:
                    db.session.rollback()
                
                # FFmpeg yoksa özel hata mesajı
                if "FFmpeg" in str(e) or "ffmpeg" in str(e).lower():
                    flash('MP3 ve diğer formatları işlemek için FFmpeg gerekli. Lütfen FFmpeg yükleyin veya doğrudan WAV dosyası kullanın.', 'error')
                else:
                    flash(error_msg, 'error')
            
            return redirect(url_for('analysis.analysis_result', analysis_id=analysis.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Ses analizi başlatılırken bir hata oluştu: {str(e)}', 'error')
            current_app.logger.error(f"Ses analizi başlatma hatası: {e}")
            return render_template('analysis/upload.html', pets=pets)
    
    return render_template('analysis/upload.html', pets=pets)

@analysis_bp.route('/analysis/task-status/<task_id>')
@login_required
def task_status(task_id):
    """Arka plan görevi durumunu kontrol eder"""
    # Celery görevini al
    task = get_analyze_sound_task().AsyncResult(task_id)
    
    if task.state == 'PENDING':
        # Görev bekliyor
        response = {
            'state': task.state,
            'status': 'Analiz bekleniyor...'
        }
    elif task.state == 'PROGRESS':
        # Görev devam ediyor
        response = {
            'state': task.state,
            'status': task.info.get('status', '')
        }
    elif task.state == 'SUCCESS':
        # Görev tamamlandı
        response = {
            'state': task.state,
            'result': task.info
        }
    else:
        # Görev hata ile tamamlandı
        response = {
            'state': task.state,
            'error': str(task.info)
        }
    
    return jsonify(response)

@analysis_bp.route('/analysis/<int:analysis_id>')
@login_required
def analysis_result(analysis_id):
    """Analiz sonucu görüntüleme"""
    try:
        # Analizi veritabanından getir
        analysis = SoundAnalysis.query.filter_by(id=analysis_id, user_id=current_user.id).first()
        
        if not analysis:
            flash('İstenen analiz bulunamadı.', 'error')
            return redirect(url_for('analysis.analysis_history'))
        
        # İlgili pet'i getir
        pet = Pet.query.get(analysis.pet_id)
        
        if not pet:
            flash('İlgili evcil hayvan bulunamadı.', 'error')
            return redirect(url_for('analysis.analysis_history'))
        
        # AI analiz sonucunu formatla (geriye dönük uyumluluk için)
        from app.utils.format_utils import format_json_as_markdown, is_json_data
        if analysis.ai_analysis and is_json_data(analysis.ai_analysis):
            analysis.ai_analysis = format_json_as_markdown(analysis.ai_analysis)
        
        return render_template('analysis/result.html', analysis=analysis, pet=pet)
    except Exception as e:
        current_app.logger.error(f"Analiz sonucu görüntüleme hatası: {e}")
        flash('Analiz sonucu görüntülenirken bir hata oluştu.', 'error')
        return redirect(url_for('analysis.analysis_history'))

@analysis_bp.route('/analysis/history')
@login_required
def analysis_history():
    """Analiz geçmişi"""
    # Kullanıcının tüm analizlerini getir
    analyses = SoundAnalysis.query.filter_by(user_id=current_user.id)\
        .order_by(SoundAnalysis.created_at.desc()).all()
    
    return render_template('analysis/history.html', analyses=analyses)

@analysis_bp.route('/analysis/delete/<int:analysis_id>', methods=['POST'])
@login_required
def delete_analysis(analysis_id):
    """Analiz silme"""
    # Analizi veritabanından getir
    analysis = SoundAnalysis.query.filter_by(id=analysis_id, user_id=current_user.id).first()
    
    if not analysis:
        flash('İstenen analiz bulunamadı.', 'error')
        return redirect(url_for('analysis.analysis_history'))
    
    try:
        # Dosyaları sil
        if analysis.file_path and os.path.exists(analysis.file_path):
            os.remove(analysis.file_path)
        
        if analysis.spectrogram_path and os.path.exists(analysis.spectrogram_path):
            os.remove(analysis.spectrogram_path)
        
        if analysis.json_spectrogram_path and os.path.exists(analysis.json_spectrogram_path):
            os.remove(analysis.json_spectrogram_path)
        
        # Veritabanından sil
        db.session.delete(analysis)
        db.session.commit()
        flash('Analiz başarıyla silindi.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Analiz silinirken bir hata oluştu: {str(e)}', 'error')
        current_app.logger.error(f"Analiz silme hatası: {e}")
    
    return redirect(url_for('analysis.analysis_history'))

# Yeni eklenen WebSocket olayları
@analysis_bp.route('/analysis/socket')
def socket_test():
    """WebSocket test endpoint"""
    return "WebSocket endpoint"

def on_join(data):
    """Analiz odasına katılır"""
    socketio = get_socketio()
    analysis_id = data['analysis_id']
    room = f'analysis_{analysis_id}'
    socketio.join_room(room)
    socketio.emit('status', {'msg': f'{room} odasına katıldınız'})

def on_leave(data):
    """Analiz odasından ayrılır"""
    socketio = get_socketio()
    analysis_id = data['analysis_id']
    room = f'analysis_{analysis_id}'
    socketio.leave_room(room)
    socketio.emit('status', {'msg': f'{room} odasından ayrıldınız'})