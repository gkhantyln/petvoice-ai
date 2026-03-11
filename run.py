# run.py
# Uygulama giriş noktası
# Bu dosya, Flask uygulamasını başlatır

import os
from app import create_app, socketio  # socketio eklendi

# Uygulamayı oluştur
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    # Geliştirme ortamında uygulamayı çalıştır
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)  # socketio.run kullanılıyor
