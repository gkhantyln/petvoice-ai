// app/static/js/spectrogram.js
// Interaktif spektrogram görselleştirme

document.addEventListener('DOMContentLoaded', function() {
    const spectrogramContainer = document.getElementById('interactive-spectrogram');
    
    if (spectrogramContainer && spectrogramContainer.dataset.jsonPath) {
        loadSpectrogramData(spectrogramContainer.dataset.jsonPath);
    }
});

function loadSpectrogramData(jsonPath) {
    fetch(jsonPath)
        .then(response => response.json())
        .then(data => {
            renderInteractiveSpectrogram(data);
        })
        .catch(error => {
            console.error('Spektrogram verisi yüklenirken hata oluştu:', error);
        });
}

function renderInteractiveSpectrogram(data) {
    const container = document.getElementById('interactive-spectrogram');
    
    // Mevcut canvas'ı kullan veya yeni bir tane oluştur
    let canvas = container.querySelector('canvas');
    if (!canvas) {
        canvas = document.createElement('canvas');
        container.innerHTML = '';
        container.appendChild(canvas);
    }
    
    // Canvas'ı container'a göre boyutlandır
    const containerRect = container.getBoundingClientRect();
    canvas.width = containerRect.width;
    canvas.height = containerRect.height;
    
    // Canvas'ın CSS boyutlarını ayarla
    canvas.style.width = containerRect.width + 'px';
    canvas.style.height = containerRect.height + 'px';
    
    const ctx = canvas.getContext('2d');
    
    // Veriyi işle
    const times = new Float32Array(data.times);
    const frequencies = new Float32Array(data.frequencies);
    const Sxx = data.Sxx;
    
    // Renk skalası için min/max değerleri bul
    let minVal = Infinity;
    let maxVal = -Infinity;
    
    for (let i = 0; i < Sxx.length; i++) {
        for (let j = 0; j < Sxx[i].length; j++) {
            if (Sxx[i][j] < minVal) minVal = Sxx[i][j];
            if (Sxx[i][j] > maxVal) maxVal = Sxx[i][j];
        }
    }
    
    // Spektrogramı çiz
    const imgData = ctx.createImageData(canvas.width, canvas.height);
    const pixels = imgData.data;
    
    const timeStep = times.length / canvas.width;
    const freqStep = frequencies.length / canvas.height;
    
    for (let x = 0; x < canvas.width; x++) {
        const timeIndex = Math.floor(x * timeStep);
        if (timeIndex >= Sxx.length) continue;
        
        for (let y = 0; y < canvas.height; y++) {
            const freqIndex = Math.floor((canvas.height - y - 1) * freqStep);
            if (freqIndex >= Sxx[timeIndex].length) continue;
            
            const value = Sxx[timeIndex][freqIndex];
            const normalized = (value - minVal) / (maxVal - minVal);
            
            // Renk skalası (mor -> mavi -> cyan -> yeşil -> sarı -> kırmızı)
            const r = getColorComponent(normalized, [128, 0, 0, 255, 255, 255]);
            const g = getColorComponent(normalized, [0, 0, 128, 255, 255, 0]);
            const b = getColorComponent(normalized, [128, 255, 255, 255, 0, 0]);
            
            const pixelIndex = (y * canvas.width + x) * 4;
            pixels[pixelIndex] = r;     // R
            pixels[pixelIndex + 1] = g; // G
            pixels[pixelIndex + 2] = b; // B
            pixels[pixelIndex + 3] = 255; // Alpha
        }
    }
    
    ctx.putImageData(imgData, 0, 0);
    
    // Eksen etiketleri ekle
    addAxisLabels(ctx, canvas.width, canvas.height, times, frequencies);
}

function getColorComponent(t, colors) {
    const n = colors.length - 1;
    const i = Math.floor(t * n);
    const f = (t * n) - i;
    
    if (i >= n) return colors[n];
    return Math.round(colors[i] + f * (colors[i + 1] - colors[i]));
}

function addAxisLabels(ctx, width, height, times, frequencies) {
    ctx.fillStyle = 'white';
    ctx.font = '12px Arial';
    ctx.textBaseline = 'top';
    
    // X ekseni (zaman)
    ctx.fillText('0s', 10, height - 20);
    ctx.fillText(Math.round(times[times.length - 1]) + 's', width - 30, height - 20);
    
    // Y ekseni (frekans)
    ctx.fillText('0Hz', 10, 10);
    ctx.fillText(Math.round(frequencies[frequencies.length - 1]) + 'Hz', 10, height - 30);
}