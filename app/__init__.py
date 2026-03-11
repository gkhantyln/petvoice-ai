# app/__init__.py
# Uygulama factory ve uzantı yapılandırması
# Bu dosya, Flask uygulamasını oluşturur ve yapılandırır

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import config
import os
import re

# FFmpeg ayarlarını yap
def setup_ffmpeg():
    """FFmpeg ayarlarını yapar"""
    if os.name == 'nt':  # Windows
        ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"
        if os.path.exists(ffmpeg_path):
            # Ortam değişkenlerini ayarla
            os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"
            os.environ["FFMPEG_PATH"] = ffmpeg_path
            
            # PyDub ayarlarını yap
            try:
                from pydub import AudioSegment
                AudioSegment.ffmpeg = ffmpeg_path
                AudioSegment.converter = ffmpeg_path
            except ImportError:
                pass

# FFmpeg ayarlarını uygula
setup_ffmpeg()

# Uzantıları başlat
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
socketio = SocketIO()

# Limiter'ı uyarıları bastırarak başlat
import warnings
warnings.filterwarnings('ignore', message='Using the in-memory storage for tracking rate limits')
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://"  # Açıkça belirt
)

def markdown_to_html(markdown_text):
    """
    Basit Markdown metnini HTML'e dönüştürür
    """
    if not markdown_text:
        return ""
    
    # HTML output
    html_output = ""
    
    # Split text into lines
    lines = markdown_text.split('\n')
    
    # Process each line
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            i += 1
            continue
        
        # Handle H2 headings (##)
        if line.startswith('## ') and not line.startswith('###'):
            content = line[3:].strip()  # Remove '## ' prefix
            html_output += f"<h2>{content}</h2>\n"
        
        # Handle H3 headings (###)
        elif line.startswith('### '):
            content = line[4:].strip()  # Remove '### ' prefix
            html_output += f"<h3>{content}</h3>\n"
        
        # Handle bullet lists
        elif line.startswith('- '):
            html_output += "<ul>\n"
            # Process all consecutive list items
            while i < len(lines) and lines[i].strip().startswith('- '):
                list_item = lines[i].strip()[2:]  # Remove '- ' prefix
                # Handle bold text in list items
                list_item = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', list_item)
                html_output += f"<li>{list_item}</li>\n"
                i += 1
            html_output += "</ul>\n"
            continue  # Skip incrementing i since we already did it in the loop
        
        # Handle paragraphs (lines that don't match other patterns)
        else:
            # Collect consecutive non-empty lines as a paragraph
            paragraph_lines = []
            while i < len(lines) and lines[i].strip() and not (
                lines[i].strip().startswith('##') or 
                lines[i].strip().startswith('-')):
                paragraph_lines.append(lines[i].strip())
                i += 1
            
            if paragraph_lines:
                paragraph = ' '.join(paragraph_lines)
                # Handle bold text (**text**)
                paragraph = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', paragraph)
                html_output += f"<p>{paragraph}</p>\n"
            continue  # Skip incrementing i since we already did it in the loop
        
        i += 1
    
    return html_output

def initialize_upload_directories(app):
    """Upload dizinlerini başlatır"""
    with app.app_context():
        # Upload klasörünü al
        upload_folder = app.config['UPLOAD_FOLDER']
        
        # Upload klasörünün tam yolunu al
        upload_folder = os.path.abspath(upload_folder)
        
        # Gerekli alt dizinleri oluştur
        sounds_dir = os.path.join(upload_folder, 'sounds')
        spectrograms_dir = os.path.join(upload_folder, 'spectrograms')
        
        # Windows uyumluluğu için tam yolları kullan
        sounds_dir = os.path.abspath(sounds_dir)
        spectrograms_dir = os.path.abspath(spectrograms_dir)
        
        # Dizinleri oluştur
        os.makedirs(sounds_dir, exist_ok=True)
        os.makedirs(spectrograms_dir, exist_ok=True)
        
        # Sadece debug modunda log göster
        if app.debug:
            app.logger.debug(f"Upload dizinleri hazır: sounds, spectrograms")

def create_app(config_name=None):
    # Yapılandırma adı belirtilmemişse environment variable kullan
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')
    
    # Flask uygulamasını oluştur
    app = Flask(__name__)
    
    # Yapılandırmayı yükle
    app.config.from_object(config[config_name])
    
    # Uzantıları başlat
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)
    limiter.init_app(app)
    
    # Upload dizinlerini başlat
    initialize_upload_directories(app)
    
    # Custom filter ekle
    app.jinja_env.filters['markdown_to_html'] = markdown_to_html
    
    # Login manager ayarları
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Bu sayfaya erişmek için lütfen giriş yapın.'
    login_manager.login_message_category = 'info'
    
    # Kullanıcı loader fonksiyonu
    from app.models.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Loglama yapılandırması
    from app.utils.logger import setup_logging
    setup_logging(app)
    
    # Blueprint'leri kaydet
    from app.views.main import main_bp
    from app.views.auth import auth_bp
    from app.views.analysis import analysis_bp
    from app.views.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(analysis_bp, url_prefix='/analysis')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Ana sayfa yönlendirmesi
    @app.route('/test')
    def test():
        return '<h1>PetVoice AI çalışıyor!</h1>'
    
    return app