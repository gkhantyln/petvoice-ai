// 
// PetVoice AI Custom JavaScript
// Bu dosya, uygulamanın özel JavaScript işlevlerini içerir
//

// Document ready function
document.addEventListener('DOMContentLoaded', function() {
    // Console log for debugging
    console.log('PetVoice AI loaded');
    
    // Form submission handling
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            // Show loading spinner on submit
            const submitButtons = form.querySelectorAll('button[type="submit"]');
            submitButtons.forEach(button => {
                button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> İşleniyor...';
                button.disabled = true;
            });
        });
    });
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Toggle password visibility
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const passwordInput = document.getElementById(targetId);
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    });
});

// Function to refresh task status
function checkTaskStatus(taskId, elementId) {
    // This function would be used to check background task status
    // Implementation would depend on your specific needs
    console.log('Checking task status for: ' + taskId);
}

// Function to update progress bar
function updateProgressBar(elementId, percentage) {
    const progressBar = document.getElementById(elementId);
    if (progressBar) {
        progressBar.style.width = percentage + '%';
        progressBar.setAttribute('aria-valuenow', percentage);
    }
}

// Function to show/hide elements
function toggleElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        if (element.style.display === 'none') {
            element.style.display = 'block';
        } else {
            element.style.display = 'none';
        }
    }
}

// File upload validation
function validateFileUpload(input) {
    // Skip validation for audio inputs to avoid conflicts with upload page
    if (input.hasAttribute('data-audio-input') || (input.name && input.name.includes('sound'))) {
        return true;
    }
    
    const fileSize = input.files[0].size / 1024 / 1024; // in MB
    const fileExtension = input.files[0].name.split('.').pop().toLowerCase();
    const allowedExtensions = ['wav', 'mp3', 'ogg', 'flac'];
    
    if (fileSize > 16) {
        alert('Dosya boyutu 16MB\'dan büyük olamaz.');
        input.value = '';
        return false;
    }
    
    if (!allowedExtensions.includes(fileExtension)) {
        alert('Lütfen geçerli bir ses dosyası seçin (wav, mp3, ogg, flac).');
        input.value = '';
        return false;
    }
    
    return true;
}

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
    
    // Wait for DOM to be fully loaded
    window.addEventListener('load', function() {
        debugLog('Window loaded, initializing event listeners');
        
        // Element selections
        // *** DEĞİŞİKLİK: Klonlama sonrası yeniden atanacak değişkenler 'let' olarak değiştirildi. ***
        let browseFilesBtn = document.getElementById('browse-files-btn');
        let soundFileInput = document.getElementById('sound_file');
        let recordBtn = document.getElementById('record-btn');
        let recordedAudioFile = document.getElementById('recorded-audio-file');
        
        // Diğer elementler const kalabilir
        const fileDropArea = document.getElementById('file-drop-area');
        const fileInfo = document.getElementById('file-info');
        const recordingStatus = document.getElementById('recording-status');
        const recordingIndicator = document.getElementById('recording-indicator');
        const statusText = document.getElementById('status-text');
        const recordingTimer = document.getElementById('recording-timer');
        const recordingProgress = document.getElementById('recording-progress');
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
        
        // *** DEĞİŞİKLİK: Klonlama ve yeniden atama mantığı düzeltildi ***
        // Bu blok, diğer script'lerden gelen event listener'ları temizler.
        // Düzgün çalışması için değişkenlerin 'let' olması gerekir.
        function cloneAndReplace(element) {
            if (element) {
                const newElement = element.cloneNode(true);
                element.parentNode.replaceChild(newElement, element);
                return newElement;
            }
            return null;
        }
        
        soundFileInput = cloneAndReplace(soundFileInput);
        recordedAudioFile = cloneAndReplace(recordedAudioFile);
        browseFilesBtn = cloneAndReplace(browseFilesBtn);
        recordBtn = cloneAndReplace(recordBtn);
        
        // File selection button event
        if (browseFilesBtn && soundFileInput) {
            browseFilesBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
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
            ['dragover', 'dragleave', 'drop'].forEach(eventName => {
                fileDropArea.addEventListener(eventName, e => {
                    e.preventDefault();
                    e.stopPropagation();
                });
            });
            fileDropArea.addEventListener('dragover', () => fileDropArea.classList.add('active'));
            fileDropArea.addEventListener('dragleave', () => fileDropArea.classList.remove('active'));
            fileDropArea.addEventListener('drop', e => {
                fileDropArea.classList.remove('active');
                debugLog('Drop event');
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    const file = files[0];
                    if (!file.type.startsWith('audio/')) {
                        alert('Lütfen sadece ses dosyası yükleyin.');
                        return;
                    }
                    if (file.size > 16 * 1024 * 1024) {
                        alert('Dosya boyutu 16MB\'dan büyük olamaz.');
                        return;
                    }
                    soundFileInput.files = files;
                    handleFileSelection(soundFileInput, 'upload');
                }
            });
        } else {
            debugLog('File drop area or sound file input not found for drag/drop');
        }
        
        // Recording button event
        if (recordBtn) {
            recordBtn.addEventListener('click', async function(e) {
                e.preventDefault();
                e.stopPropagation();
                debugLog(`Record button clicked, isRecording: ${isRecording}`);
                
                if (!isRecording) {
                    try {
                        const stream = await navigator.mediaDevices.getUserMedia({ 
                            audio: {
                                echoCancellation: true,
                                noiseSuppression: true,
                                sampleRate: 44100
                            } 
                        });
                        
                        mediaRecorder = new MediaRecorder(stream);
                        audioChunks = [];
                        
                        mediaRecorder.ondataavailable = event => {
                            if (event.data.size > 0) audioChunks.push(event.data);
                        };
                        
                        mediaRecorder.onstop = () => {
                            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                            const file = new File([audioBlob], 'recording.wav', { type: 'audio/wav' });
                            const dataTransfer = new DataTransfer();
                            dataTransfer.items.add(file);
                            
                            if (recordedAudioFile) {
                                recordedAudioFile.files = dataTransfer.files;
                                handleFileSelection(recordedAudioFile, 'record');
                            }
                            if (soundFileInput) soundFileInput.value = '';
                            
                            stream.getTracks().forEach(track => track.stop());
                        };
                        
                        mediaRecorder.start();
                        startRecording();
                        
                    } catch (error) {
                        debugLog(`Microphone access error: ${error.message}`);
                        alert('Mikrofon erişimi sağlanamadı. Lütfen mikrofon izinlerini kontrol edin.');
                    }
                } else {
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
                const fileSize = (file.size / (1024 * 1024)).toFixed(2);
                
                if (file.size > 16 * 1024 * 1024) {
                    alert('Dosya boyutu 16MB\'dan büyük olamaz.');
                    fileInput.value = '';
                    fileInfo.classList.remove('visible');
                    return;
                }
                
                if (!file.type.startsWith('audio/')) {
                    alert('Lütfen sadece ses dosyası yükleyin.');
                    fileInput.value = '';
                    fileInfo.classList.remove('visible');
                    return;
                }
                
                let iconClass = source === 'record' ? 'fas fa-microphone text-danger' : 'fas fa-file-audio text-primary';
                let fileLabel = source === 'record' ? 'Kaydedilen ses:' : 'Seçilen dosya:';
                
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
                fileInfo.classList.remove('visible');
            }
        }
        
        function startRecording() {
            isRecording = true;
            recordingStartTime = Date.now();
            if (recordBtn) {
                recordBtn.classList.add('recording');
                recordBtn.innerHTML = '<i class="fas fa-stop me-2 fa-lg"></i>Kaydı Durdur';
            }
            if (recordingIndicator) recordingIndicator.classList.add('active');
            if (statusText) {
                statusText.textContent = 'Kayıt yapılıyor...';
                statusText.parentElement.classList.add('recording');
            }
            recordingInterval = setInterval(updateRecordingTimer, 100);
        }
        
        function stopRecording() {
            isRecording = false;
            if (recordingInterval) clearInterval(recordingInterval);
            if (recordBtn) {
                recordBtn.classList.remove('recording');
                recordBtn.innerHTML = '<i class="fas fa-microphone me-2 fa-lg"></i>Kaydı Başlat';
            }
            if (recordingIndicator) recordingIndicator.classList.remove('active');
            if (statusText) {
                statusText.textContent = 'Kayıt tamamlandı';
                statusText.parentElement.classList.remove('recording');
            }
            if (recordingProgress) recordingProgress.style.width = '0%';
            if (recordingTimer) recordingTimer.textContent = '0:00';
        }
        
        function updateRecordingTimer() {
            if (!isRecording) return;
            const elapsed = (Date.now() - recordingStartTime) / 1000;
            const maxDuration = 60;
            if (recordingTimer) recordingTimer.textContent = formatTime(elapsed);
            if (recordingProgress) {
                const progress = Math.min((elapsed / maxDuration) * 100, 100);
                recordingProgress.style.width = progress + '%';
            }
            if (elapsed >= maxDuration) {
                if (mediaRecorder && mediaRecorder.state === 'recording') {
                    mediaRecorder.stop();
                }
                stopRecording();
            }
        }
        
        function formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${mins}:${secs.toString().padStart(2, '0')}`;
        }
        
        if (analysisForm) {
            analysisForm.addEventListener('submit', function(e) {
                const petId = document.getElementById('pet_id');
                const hasUploadedFile = soundFileInput && soundFileInput.files.length > 0;
                const hasRecordedAudio = recordedAudioFile && recordedAudioFile.files.length > 0;
                
                if (!petId || !petId.value) {
                    e.preventDefault();
                    alert('Lütfen evcil hayvanınızı seçin.');
                    petId.focus();
                    return;
                }
                
                if (!hasUploadedFile && !hasRecordedAudio) {
                    e.preventDefault();
                    alert('Lütfen ses dosyası yükleyin veya ses kaydı yapın.');
                    return;
                }
                
                if (submitBtn) {
                    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>İşleniyor...';
                    submitBtn.disabled = true;
                }
            });
        }
        
        debugLog('All event listeners initialized successfully');
    });

// Add event listener to file inputs
document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        // Only apply validation to non-audio inputs to avoid conflicts
        if (!input.hasAttribute('data-audio-input') && !input.name.includes('sound')) {
            input.addEventListener('change', function() {
                validateFileUpload(this);
            });
        }
    });
});