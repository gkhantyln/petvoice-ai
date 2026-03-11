from flask import Flask, render_template_string

app = Flask(__name__)

# Test route to verify our upload page fixes work
@app.route('/')
def test():
    # Simple HTML template that mimics the base.html structure but with our fixed upload.html
    template = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Upload Page</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* Upload page specific styles */
        .upload-header {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .upload-card {
            border-radius: 15px;
            border: none;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            margin-bottom: 1.5rem;
            overflow: hidden;
        }
        
        .upload-card:hover {
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            transform: translateY(-3px);
        }
        
        .upload-card-header {
            background: linear-gradient(90deg, #667eea, #764ba2);
            color: white;
            border-radius: 15px 15px 0 0 !important;
            border: none;
            padding: 1.25rem;
        }
        
        .form-control, .form-select {
            border-radius: 10px;
            padding: 12px 15px;
            border: 2px solid #e9ecef;
            transition: all 0.3s ease;
        }
        
        .form-control:focus, .form-select:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.25rem rgba(135, 206, 235, 0.25);
        }
        
        .btn-record {
            border-radius: 12px;
            padding: 15px 25px;
            font-weight: 700;
            background: linear-gradient(135deg, #ff4757, #fa5252);
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(255, 71, 87, 0.3);
            color: white;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .btn-record:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 25px rgba(255, 71, 87, 0.4);
            background: linear-gradient(135deg, #fa5252, #ff4757);
        }
        
        .btn-record:active {
            transform: translateY(-2px);
        }
        
        .btn-record.recording {
            background: linear-gradient(135deg, #ff6b6b, #fa5252);
            animation: pulse 1.5s infinite;
            box-shadow: 0 8px 20px rgba(255, 107, 107, 0.4);
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(255, 107, 107, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0); }
        }
        
        .btn-submit-analysis {
            border-radius: 10px;
            padding: 12px 25px;
            font-weight: 600;
            background: linear-gradient(135deg, #4dabf7, #3b5bdb);
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .btn-submit-analysis:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            background: linear-gradient(135deg, #3b5bdb, #4dabf7);
        }
        
        .btn-submit-analysis:disabled {
            background: #adb5bd;
            transform: none;
            box-shadow: none;
        }
        
        .btn-outline-primary {
            border-radius: 10px;
            padding: 8px 15px;
            font-weight: 600;
            transition: all 0.3s ease;
            background: linear-gradient(135deg, #3bc9db, #15aabf);
            color: white !important;
            border: none;
        }
        
        .btn-outline-primary:hover {
            background: linear-gradient(135deg, #15aabf, #3bc9db);
            color: white;
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(21, 170, 191, 0.3);
        }
        
        .recording-status {
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .recording-status.recording {
            color: #ff6b6b;
            animation: blink 1s infinite;
        }
        
        @keyframes blink {
            50% { opacity: 0.5; }
        }
        
        .progress {
            border-radius: 10px;
            height: 10px;
            background-color: #e9ecef;
        }
        
        .progress-bar {
            border-radius: 10px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
        
        .info-card {
            border-radius: 15px;
            border: none;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            margin-bottom: 1.5rem;
        }
        
        .info-card:hover {
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            transform: translateY(-3px);
        }
        
        .info-card-header {
            background: linear-gradient(90deg, #cc5de8, #8435b5);
            color: white;
            border-radius: 15px 15px 0 0 !important;
            border: none;
            padding: 1.25rem;
        }
        
        .info-item {
            border-radius: 10px;
            transition: all 0.3s ease;
            border-left: 4px solid #667eea;
            margin-bottom: 0.5rem;
            padding: 0.75rem 1rem;
        }
        
        .info-item:hover {
            background-color: rgba(135, 206, 235, 0.1);
            transform: translateX(5px);
        }
        
        .section-header {
            position: relative;
            padding-bottom: 15px;
            margin-bottom: 25px;
        }
        
        .section-header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 60px;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 2px;
        }
        
        .file-upload-area {
            border: 2px dashed #e9ecef;
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
            background-color: #f8f9fa;
            cursor: pointer;
            position: relative;
        }
        
        .file-upload-area:hover {
            border-color: #667eea;
            background-color: rgba(135, 206, 235, 0.05);
        }
        
        .file-upload-area.active {
            border-color: #667eea;
            background-color: rgba(135, 206, 235, 0.1);
        }
        
        .input-group-text {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-left: none;
            border-radius: 0 10px 10px 0;
        }
        
        .input-group .form-control {
            border-radius: 10px 0 0 10px;
            border-right: none;
        }
        
        /* Hidden file inputs for audio files */
        .audio-file-input {
            position: absolute;
            left: -9999px;
            top: -9999px;
            width: 1px;
            height: 1px;
        }
        
        /* Recording indicator */
        .recording-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            background-color: #ff4757;
            border-radius: 50%;
            margin-right: 8px;
            vertical-align: middle;
        }
        
        .recording-indicator.active {
            animation: blink 1s infinite;
        }
        
        /* File info display */
        .file-info {
            margin-top: 15px;
            padding: 10px;
            background-color: #e8f5e9;
            border-radius: 8px;
            display: none;
        }
        
        .file-info.visible {
            display: block;
        }
        
        /* Loading spinner */
        .spinner-border-sm {
            width: 1rem;
            height: 1rem;
            border-width: 0.2em;
        }
        
        /* Debug info for troubleshooting */
        .debug-info {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 10px;
            font-size: 12px;
            max-height: 100px;
            overflow-y: auto;
            z-index: 9999;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container py-4">
        <!-- Upload Header -->
        <div class="upload-header">
            <div class="row align-items-center">
                <div class="col-lg-9">
                    <h1 class="mb-3">Ses Analizi Yap</h1>
                    <p class="mb-0 lead">Evcil hayvanınızın sesini kaydedin veya yükleyin ve AI ile analiz edin.</p>
                </div>
                <div class="col-lg-3 text-center d-none d-lg-block">
                    <i class="fas fa-microphone-alt fa-4x opacity-50"></i>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-8">
                <div class="section-header">
                    <h3>Ses Kaydı veya Yükleme</h3>
                </div>
                <div class="card upload-card">
                    <div class="card-body">
                        <form method="POST" enctype="multipart/form-data" id="analysis-form">
                            <div class="mb-4">
                                <label for="pet_id" class="form-label fw-bold">Evcil Hayvan</label>
                                <div class="input-group">
                                    <span class="input-group-text">
                                        <i class="fas fa-paw"></i>
                                    </span>
                                    <select class="form-select" id="pet_id" name="pet_id" required>
                                        <option value="">Seçiniz</option>
                                        <option value="1">Max (Köpek)</option>
                                        <option value="2">Maviş (Kedi)</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="mb-4">
                                <label for="context_situation" class="form-label fw-bold">Durum</label>
                                <div class="input-group">
                                    <span class="input-group-text">
                                        <i class="fas fa-info-circle"></i>
                                    </span>
                                    <select class="form-select" id="context_situation" name="context_situation">
                                        <option value="Genel (Durum Belirtilmedi)">Genel (Durum Belirtilmedi)</option>
                                        <option value="Oyun Oynarken">Oyun Oynarken</option>
                                        <option value="Yemek Beklerken / Açken">Yemek Beklerken / Açken</option>
                                        <option value="Tuvaletteyken">Tuvaletteyken</option>
                                        <option value="Korkmuş / Stresliyken">Korkmuş / Stresliyken</option>
                                        <option value="Hastayken / Acı Çekerken">Hastayken / Acı Çekerken</option>
                                        <option value="Uykudan Önce / Uyanırken">Uykudan Önce / Uyanırken</option>
                                        <option value="Diğer Hayvanlarla İletişim Kurarken">Diğer Hayvanlarla İletişim Kurarken</option>
                                        <option value="Diğer...">Diğer...</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="mb-4">
                                <label for="custom_context" class="form-label fw-bold">Özel Durum Açıklaması</label>
                                <textarea class="form-control" id="custom_context" name="custom_context" rows="3" placeholder="Örn: Veterinere giderken arabada..."></textarea>
                                <div class="form-text text-muted">Durum seçeneğinde "Diğer..." seçtiyseniz buraya açıklama yazın.</div>
                            </div>
                            
                            <div class="mb-4">
                                <label class="form-label fw-bold">Ses Kaydı</label>
                                <div class="border rounded p-3 file-upload-area" id="recording-area">
                                    <div class="d-flex justify-content-between align-items-center mb-3">
                                        <button type="button" class="btn btn-record" id="record-btn">
                                            <i class="fas fa-microphone me-2 fa-lg"></i>Kaydı Başlat
                                        </button>
                                        <div class="recording-status" id="recording-status">
                                            <span class="recording-indicator" id="recording-indicator"></span>
                                            <span id="status-text">Kayıt durduruldu</span>
                                        </div>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <div class="progress">
                                            <div class="progress-bar" id="recording-progress" role="progressbar" style="width: 0%"></div>
                                        </div>
                                    </div>
                                    
                                    <div class="d-flex justify-content-between">
                                        <small class="text-muted">0:00</small>
                                        <small class="text-muted" id="recording-timer">0:00</small>
                                        <small class="text-muted">1:00</small>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mb-4">
                                <label class="form-label fw-bold">Veya Ses Dosyası Yükle</label>
                                <div class="file-upload-area" id="file-drop-area">
                                    <i class="fas fa-cloud-upload-alt fa-3x mb-3 text-muted"></i>
                                    <p class="mb-2">Dosyaları buraya sürükleyin veya seçmek için tıklayın</p>
                                    <p class="text-muted small">Desteklenen formatlar: WAV, MP3, OGG, FLAC (Maksimum 16MB)</p>
                                    <input type="file" class="form-control audio-file-input" id="sound_file" name="sound_file" accept="audio/*">
                                    <button type="button" class="btn btn-outline-primary mt-2" id="browse-files-btn">
                                        <i class="fas fa-folder-open me-2"></i>Dosya Seç
                                    </button>
                                    <!-- File info display -->
                                    <div class="file-info" id="file-info"></div>
                                </div>
                            </div>
                            
                            <div class="d-grid">
                                <button type="submit" class="btn btn-submit-analysis btn-lg" id="submit-btn">
                                    <i class="fas fa-microphone-alt me-2"></i>Ses Analizi Yap
                                </button>
                            </div>
                            
                            <!-- Hidden input for recorded audio -->
                            <input type="file" class="audio-file-input" id="recorded-audio-file" name="sound_file">
                        </form>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="section-header">
                    <h3>Nasıl Çalışır?</h3>
                </div>
                <div class="card info-card">
                    <div class="info-card-header">
                        <h5 class="mb-0">Adımlar</h5>
                    </div>
                    <div class="card-body">
                        <div class="info-item">
                            <div class="d-flex">
                                <div class="me-3">
                                    <span class="badge bg-primary rounded-pill">1</span>
                                </div>
                                <div>
                                    <strong>Evcil hayvanınızı seçin</strong>
                                    <p class="mb-0 text-muted small">Analiz için doğru hayvanı seçin</p>
                                </div>
                            </div>
                        </div>
                        <div class="info-item">
                            <div class="d-flex">
                                <div class="me-3">
                                    <span class="badge bg-primary rounded-pill">2</span>
                                </div>
                                <div>
                                    <strong>Durumu belirtin</strong>
                                    <p class="mb-0 text-muted small">Hayvanın sesini çıkardığı durumu açıklayın</p>
                                </div>
                            </div>
                        </div>
                        <div class="info-item">
                            <div class="d-flex">
                                <div class="me-3">
                                    <span class="badge bg-primary rounded-pill">3</span>
                                </div>
                                <div>
                                    <strong>Ses kaydedin veya dosya yükleyin</strong>
                                    <p class="mb-0 text-muted small">Canlı kayıt yapın veya mevcut dosya yükleyin</p>
                                </div>
                            </div>
                        </div>
                        <div class="info-item">
                            <div class="d-flex">
                                <div class="me-3">
                                    <span class="badge bg-primary rounded-pill">4</span>
                                </div>
                                <div>
                                    <strong>Analiz işlemini başlatın</strong>
                                    <p class="mb-0 text-muted small">AI analizini başlatmak için butona tıklayın</p>
                                </div>
                            </div>
                        </div>
                        <div class="info-item">
                            <div class="d-flex">
                                <div class="me-3">
                                    <span class="badge bg-primary rounded-pill">5</span>
                                </div>
                                <div>
                                    <strong>Sonuçları inceleyin</strong>
                                    <p class="mb-0 text-muted small">Detaylı analiz raporunu görüntüleyin</p>
                                </div>
                            </div>
                        </div>
                        <div class="alert alert-info mt-3 mb-0">
                            <i class="fas fa-info-circle me-2"></i>
                            <strong>Önemli:</strong> Durumu belirtmeniz, AI'nın daha doğru analiz yapmasını sağlar.
                        </div>
                    </div>
                </div>
                
                <div class="card info-card">
                    <div class="info-card-header">
                        <h5 class="mb-0">İpuçları</h5>
                    </div>
                    <div class="card-body">
                        <div class="info-item">
                            <i class="fas fa-volume-up text-primary me-2"></i>
                            <strong>Sessiz bir ortamda kayıt yapın</strong>
                        </div>
                        <div class="info-item">
                            <i class="fas fa-heart text-danger me-2"></i>
                            <strong>Hayvanınızı rahatsız etmeden kaydedin</strong>
                        </div>
                        <div class="info-item">
                            <i class="fas fa-clock text-warning me-2"></i>
                            <strong>Mümkünse sabırlı olun</strong>
                        </div>
                        <div class="info-item">
                            <i class="fas fa-bolt text-success me-2"></i>
                            <strong>Kısa ve net ses örnekleri tercih edin</strong>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Debug info panel (hidden by default) -->
    <div class="debug-info" id="debug-info"></div>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Debug logging function
        function debugLog(message) {
            const debugInfo = document.getElementById('debug-info');
            if (debugInfo) {
                const timestamp = new Date().toLocaleTimeString();
                debugInfo.innerHTML += `<div>[${timestamp}] ${message}</div>`;
                debugInfo.scrollTop = debugInfo.scrollHeight; // Auto-scroll to bottom
                console.log(`[UPLOAD_DEBUG] ${message}`);
            }
        }
        
        document.addEventListener('DOMContentLoaded', function() {
            debugLog('DOM loaded, initializing event listeners');
            
            // Element selections
            const browseFilesBtn = document.getElementById('browse-files-btn');
            const soundFileInput = document.getElementById('sound_file');
            const fileDropArea = document.getElementById('file-drop-area');
            const fileInfo = document.getElementById('file-info');
            const recordBtn = document.getElementById('record-btn');
            const recordingStatus = document.getElementById('recording-status');
            const recordingIndicator = document.getElementById('recording-indicator');
            const statusText = document.getElementById('status-text');
            const recordingTimer = document.getElementById('recording-timer');
            const recordingProgress = document.getElementById('recording-progress');
            const recordedAudioFile = document.getElementById('recorded-audio-file');
            const recordingArea = document.getElementById('recording-area');
            const analysisForm = document.getElementById('analysis-form');
            const submitBtn = document.getElementById('submit-btn');
            
            debugLog(`Elements found - browseFilesBtn: ${!!browseFilesBtn}, soundFileInput: ${!!soundFileInput}, recordBtn: ${!!recordBtn}`);
            
            // Recording variables
            let mediaRecorder;
            let audioChunks = [];
            let recordingInterval;
            let recordingStartTime;
            let isRecording = false;
            let recordingDuration = 0;
            
            // Remove any existing event listeners to prevent conflicts
            if (soundFileInput) {
                const cloneSoundFileInput = soundFileInput.cloneNode(true);
                soundFileInput.parentNode.replaceChild(cloneSoundFileInput, soundFileInput);
                soundFileInput = document.getElementById('sound_file'); // Get the new element
            }
            
            if (recordedAudioFile) {
                const cloneRecordedAudioFile = recordedAudioFile.cloneNode(true);
                recordedAudioFile.parentNode.replaceChild(cloneRecordedAudioFile, recordedAudioFile);
                recordedAudioFile = document.getElementById('recorded-audio-file'); // Get the new element
            }
            
            // Prevent global script.js validation from interfering with audio inputs
            if (soundFileInput) {
                soundFileInput.classList.add('audio-input');
                soundFileInput.setAttribute('data-audio-input', 'true');
            }
            if (recordedAudioFile) {
                recordedAudioFile.classList.add('audio-input');
                recordedAudioFile.setAttribute('data-audio-input', 'true');
            }
            
            // File selection button event
            if (browseFilesBtn && soundFileInput) {
                browseFilesBtn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    e.preventDefault();
                    debugLog('Browse files button clicked');
                    soundFileInput.click();
                });
            } else {
                debugLog('Browse files button or sound file input not found');
            }
            
            // File input change event for uploaded files
            if (soundFileInput && fileInfo) {
                soundFileInput.addEventListener('change', function(e) {
                    debugLog('File selection changed for uploaded file');
                    handleFileSelection(e.target, 'upload');
                });
            } else {
                debugLog('Sound file input or file info not found for upload');
            }
            
            // File input change event for recorded files
            if (recordedAudioFile && fileInfo) {
                recordedAudioFile.addEventListener('change', function(e) {
                    debugLog('File selection changed for recorded file');
                    handleFileSelection(e.target, 'record');
                });
            } else {
                debugLog('Recorded audio file input or file info not found for recording');
            }
            
            // File drop area click event
            if (fileDropArea) {
                fileDropArea.addEventListener('click', function(e) {
                    // If browse button is clicked, let its own handler work
                    if (e.target.closest('#browse-files-btn') || e.target.id === 'browse-files-btn') {
                        debugLog('Browse button clicked in drop area, skipping');
                        return;
                    }
                    
                    debugLog('File drop area clicked');
                    if (soundFileInput) {
                        soundFileInput.click();
                    }
                });
            } else {
                debugLog('File drop area not found');
            }
            
            // Drag and drop events
            if (fileDropArea && soundFileInput) {
                fileDropArea.addEventListener('dragover', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    fileDropArea.classList.add('active');
                    debugLog('Drag over event');
                });
                
                fileDropArea.addEventListener('dragleave', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    fileDropArea.classList.remove('active');
                    debugLog('Drag leave event');
                });
                
                fileDropArea.addEventListener('drop', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    fileDropArea.classList.remove('active');
                    debugLog('Drop event');
                    
                    const files = e.dataTransfer.files;
                    if (files.length > 0) {
                        const file = files[0];
                        debugLog(`Dropped file: ${file.name}`);
                        
                        // File type check
                        if (!file.type.startsWith('audio/')) {
                            debugLog('Invalid file type dropped');
                            alert('Lütfen sadece ses dosyası yükleyin.');
                            return;
                        }
                        
                        // File size check
                        if (file.size > 16 * 1024 * 1024) {
                            debugLog('File too large');
                            alert('Dosya boyutu 16MB\'dan büyük olamaz.');
                            return;
                        }
                        
                        // Assign to file input
                        soundFileInput.files = files;
                        debugLog('File assigned to input');
                        
                        // Handle file selection
                        handleFileSelection(soundFileInput, 'upload');
                    }
                });
            } else {
                debugLog('File drop area or sound file input not found for drag/drop');
            }
            
            // Recording button event
            if (recordBtn) {
                recordBtn.addEventListener('click', async function() {
                    debugLog(`Record button clicked, isRecording: ${isRecording}`);
                    
                    if (!isRecording) {
                        // Start recording
                        try {
                            debugLog('Requesting microphone access');
                            const stream = await navigator.mediaDevices.getUserMedia({ 
                                audio: {
                                    echoCancellation: true,
                                    noiseSuppression: true,
                                    sampleRate: 44100
                                } 
                            });
                            
                            debugLog('Microphone access granted');
                            mediaRecorder = new MediaRecorder(stream);
                            audioChunks = [];
                            
                            mediaRecorder.ondataavailable = function(event) {
                                if (event.data.size > 0) {
                                    audioChunks.push(event.data);
                                    debugLog(`Data available: ${event.data.size} bytes`);
                                }
                            };
                            
                            mediaRecorder.onstop = function() {
                                debugLog('Recording stopped');
                                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                                
                                // Assign recorded file to input
                                const file = new File([audioBlob], 'recording.wav', { type: 'audio/wav' });
                                const dataTransfer = new DataTransfer();
                                dataTransfer.items.add(file);
                                
                                if (recordedAudioFile) {
                                    recordedAudioFile.files = dataTransfer.files;
                                    debugLog('Recorded file assigned to input');
                                    
                                    // Handle file selection
                                    handleFileSelection(recordedAudioFile, 'record');
                                }
                                
                                // Clear uploaded file input
                                if (soundFileInput) {
                                    soundFileInput.value = '';
                                }
                                
                                // Stop stream
                                stream.getTracks().forEach(track => track.stop());
                                debugLog('Media stream tracks stopped');
                            };
                            
                            mediaRecorder.start();
                            startRecording();
                            
                        } catch (error) {
                            debugLog(`Microphone access error: ${error.message}`);
                            alert('Mikrofon erişimi sağlanamadı. Lütfen mikrofon izinlerini kontrol edin.');
                        }
                    } else {
                        // Stop recording
                        debugLog('Stopping recording');
                        if (mediaRecorder && mediaRecorder.state === 'recording') {
                            mediaRecorder.stop();
                        }
                        stopRecording();
                    }
                });
            } else {
                debugLog('Record button not found');
            }
            
            // Handle file selection for both upload and recording
            function handleFileSelection(fileInput, source) {
                if (fileInput.files && fileInput.files.length > 0) {
                    const file = fileInput.files[0];
                    const fileName = file.name;
                    const fileSize = (file.size / (1024 * 1024)).toFixed(2); // MB
                    
                    debugLog(`File selected: ${fileName}, Size: ${fileSize} MB, Source: ${source}`);
                    
                    // File size check (16MB limit)
                    if (file.size > 16 * 1024 * 1024) {
                        debugLog('File size exceeds limit');
                        alert('Dosya boyutu 16MB\'dan büyük olamaz.');
                        fileInput.value = '';
                        fileInfo.classList.remove('visible');
                        return;
                    }
                    
                    // File type check
                    if (!file.type.startsWith('audio/')) {
                        debugLog('Invalid file type selected');
                        alert('Lütfen sadece ses dosyası yükleyin.');
                        fileInput.value = '';
                        fileInfo.classList.remove('visible');
                        return;
                    }
                    
                    // Display file info
                    let iconClass = 'fas fa-file-audio text-primary';
                    let fileLabel = 'Seçilen dosya:';
                    
                    if (source === 'record') {
                        iconClass = 'fas fa-microphone text-danger';
                        fileLabel = 'Kaydedilen ses:';
                    }
                    
                    fileInfo.innerHTML = `
                        <div class="d-flex align-items-center">
                            <i class="${iconClass} me-2"></i>
                            <div>
                                <strong>${fileLabel}</strong> ${fileName}<br>
                                <small class="text-muted">Boyut: ${fileSize} MB</small>
                            </div>
                        </div>
                    `;
                    fileInfo.classList.add('visible');
                } else {
                    // Hide file info when selection is cancelled
                    fileInfo.classList.remove('visible');
                    debugLog('File selection cancelled or cleared');
                }
            }
            
            // Start recording function
            function startRecording() {
                isRecording = true;
                recordingStartTime = Date.now();
                debugLog('Starting recording');
                
                // UI updates
                if (recordBtn) {
                    recordBtn.classList.add('recording');
                    recordBtn.innerHTML = '<i class="fas fa-stop me-2 fa-lg"></i>Kaydı Durdur';
                }
                
                if (recordingIndicator) {
                    recordingIndicator.classList.add('active');
                }
                
                if (statusText) {
                    statusText.textContent = 'Kayıt yapılıyor...';
                    statusText.parentElement.classList.add('recording');
                }
                
                // Start timer
                recordingInterval = setInterval(updateRecordingTimer, 100);
                debugLog('Recording interval started');
            }
            
            // Stop recording function
            function stopRecording() {
                isRecording = false;
                recordingDuration = (Date.now() - recordingStartTime) / 1000; // in seconds
                debugLog('Stopping recording');
                
                // Stop timer
                if (recordingInterval) {
                    clearInterval(recordingInterval);
                    debugLog('Recording interval cleared');
                }
                
                // UI updates
                if (recordBtn) {
                    recordBtn.classList.remove('recording');
                    recordBtn.innerHTML = '<i class="fas fa-microphone me-2 fa-lg"></i>Kaydı Başlat';
                }
                
                if (recordingIndicator) {
                    recordingIndicator.classList.remove('active');
                }
                
                if (statusText) {
                    statusText.textContent = 'Kayıt tamamlandı';
                    statusText.parentElement.classList.remove('recording');
                }
                
                // Reset progress bar
                if (recordingProgress) {
                    recordingProgress.style.width = '0%';
                }
                
                if (recordingTimer) {
                    recordingTimer.textContent = '0:00';
                }
            }
            
            // Update recording timer function
            function updateRecordingTimer() {
                if (!isRecording) return;
                
                const elapsed = (Date.now() - recordingStartTime) / 1000; // seconds
                const maxDuration = 60; // 1 minute maximum
                
                // Update timer
                if (recordingTimer) {
                    recordingTimer.textContent = formatTime(elapsed);
                }
                
                // Update progress bar
                if (recordingProgress) {
                    const progress = Math.min((elapsed / maxDuration) * 100, 100);
                    recordingProgress.style.width = progress + '%';
                }
                
                // Stop if maximum duration reached
                if (elapsed >= maxDuration) {
                    debugLog('Maximum recording duration reached');
                    if (mediaRecorder && mediaRecorder.state === 'recording') {
                        mediaRecorder.stop();
                    }
                    stopRecording();
                }
            }
            
            // Format time function
            function formatTime(seconds) {
                const mins = Math.floor(seconds / 60);
                const secs = Math.floor(seconds % 60);
                return `${mins}:${secs.toString().padStart(2, '0')}`;
            }
            
            // Form submission check
            if (analysisForm) {
                analysisForm.addEventListener('submit', function(e) {
                    debugLog('Form submission attempted');
                    const petId = document.getElementById('pet_id');
                    const uploadedSoundFile = document.getElementById('sound_file');
                    const recordedSoundFile = document.getElementById('recorded-audio-file');
                    
                    // Pet selection check
                    if (!petId || !petId.value) {
                        e.preventDefault();
                        debugLog('Pet not selected');
                        alert('Lütfen evcil hayvanınızı seçin.');
                        petId.focus();
                        return false;
                    }
                    
                    // Sound file check
                    const hasUploadedFile = uploadedSoundFile && uploadedSoundFile.files && uploadedSoundFile.files.length > 0;
                    const hasRecordedAudio = recordedSoundFile && recordedSoundFile.files && recordedSoundFile.files.length > 0;
                    
                    debugLog(`Has uploaded file: ${hasUploadedFile}, Has recorded audio: ${hasRecordedAudio}`);
                    
                    if (!hasUploadedFile && !hasRecordedAudio) {
                        e.preventDefault();
                        debugLog('No audio file provided');
                        alert('Lütfen ses dosyası yükleyin veya ses kaydı yapın.');
                        return false;
                    }
                    
                    // Show loading state
                    if (submitBtn) {
                        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>İşleniyor...';
                        submitBtn.disabled = true;
                    }
                    
                    debugLog('Form submitted successfully');
                    return true;
                });
            } else {
                debugLog('Analysis form not found');
            }
            
            debugLog('All event listeners initialized successfully');
        });
        
        // Override global validation for audio inputs to prevent conflicts
        document.addEventListener('DOMContentLoaded', function() {
            // Add a small delay to ensure our event listeners are registered after global ones
            setTimeout(function() {
                const audioInputs = document.querySelectorAll('input[type="file"][data-audio-input="true"]');
                audioInputs.forEach(input => {
                    // Remove any existing validation listeners that might conflict
                    const clone = input.cloneNode(true);
                    input.parentNode.replaceChild(clone, input);
                    
                    // Add our own validation that won't conflict with global script
                    clone.addEventListener('change', function() {
                        // Our validation is handled in the handleFileSelection function
                        // This just prevents the global validation from running
                        console.log('Audio input change handled by upload page');
                    });
                });
            }, 100);
        });
    </script>
</body>
</html>
    '''
    return render_template_string(template)

if __name__ == '__main__':
    app.run(debug=True, port=5002)