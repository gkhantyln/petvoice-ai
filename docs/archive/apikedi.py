import gradio as gr
import google.generativeai as genai
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from datetime import datetime
import os
import shutil
import pandas as pd

# --- Konfigürasyon ---
GOOGLE_API_KEY = "AIzaSyAzsPNOm7f9fqS9gYV_PKsJUS0GuEKQSQ4" #os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Lütfen Google AI API anahtarınızı 'GOOGLE_API_KEY' adında bir ortam değişkeni olarak ayarlayın.")
genai.configure(api_key=GOOGLE_API_KEY)

DATA_DIR = "kayitlar"
SPECTROGRAM_DIR = "spektrogramlar"
CSV_FILE = "hayvan_ses_veritabani.csv"  # Changed from kedi_ses_veritabani.csv
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SPECTROGRAM_DIR, exist_ok=True)

# --- Fonksiyonlar ---

def plot_spectrogram_from_data(data, fs, output_path):
    plt.figure(figsize=(10, 4))
    plt.specgram(data, Fs=fs, NFFT=1024, noverlap=512, cmap='inferno')
    plt.title("Hayvan Sesi Spektrogramı")  # Changed from Kedi Sesi Spektrogramı
    plt.xlabel("Zaman (saniye)")
    plt.ylabel("Frekans (Hz)")
    plt.colorbar(label='Yoğunluk (dB)')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path

# YENİ PARAMETRELER EKLENDİ: hayvan_turu, durum_secimi, diger_durum_aciklama
def analyze_animal_sound(audio_filepath, hayvan_turu, durum_secimi, diger_durum_aciklama):
    """
    Ses dosyasını, hayvan türünü ve bağlamı alır, Gemini ile analiz eder, sonucu kaydeder
    ve arayüze döndürür.
    """
    if audio_filepath is None:
        return "Lütfen bir ses dosyası yükleyin veya kaydedin.", None

    try:
        # --- 1. Dosyayı ve Veriyi Hazırla ---
        benzersiz_id = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        yeni_dosya_adi = f"hayvan_sesi_{benzersiz_id}.wav"  # Changed from kedi_sesi_
        kayit_yolu = os.path.join(DATA_DIR, yeni_dosya_adi)
        shutil.copy(audio_filepath, kayit_yolu)
        fs, data = read(kayit_yolu)
        if data.ndim > 1: data = data[:, 0]

        # --- 2. Spektrogram Oluştur ---
        spektrogram_path = os.path.join(SPECTROGRAM_DIR, f"spektrogram_{benzersiz_id}.png")
        plot_spectrogram_from_data(data, fs, spektrogram_path)

        # --- 3. Gemini AI ile Analiz (DİNAMİK PROMPT İLE) ---
        print(f"'{kayit_yolu}' dosyası Gemini'ye analiz için gönderiliyor...")
        
        # Kullanıcının girdiği hayvan türünü belirle
        if hayvan_turu == "Diğer...":
            hayvan_turu_context = diger_durum_aciklama.strip()  # Using diger_durum_aciklama for animal type
            if not hayvan_turu_context:
                hayvan_turu_context = "Belirtilmemiş bir hayvan"
        else:
            hayvan_turu_context = hayvan_turu

        # Kullanıcının girdiği durumu belirle
        durum_context = ""
        if durum_secimi == "Diğer...":
            durum_context = diger_durum_aciklama.strip()
        else:
            durum_context = durum_secimi

        if not durum_context or durum_context == "Genel (Durum Belirtilmedi)":
            durum_context = "Kullanıcı özel bir durum belirtmedi. Lütfen genel bir analiz yap."
        
        print(f"Analiz için belirlenen hayvan türü: {hayvan_turu_context}")
        print(f"Analiz için belirlenen bağlam: {durum_context}")

        model = genai.GenerativeModel('models/gemini-2.0-flash') #gemini-1.5-flash-latest
        
        # Read the audio file content
        with open(kayit_yolu, 'rb') as audio_file:
            audio_data = audio_file.read()
        
        # Create a file part using FileData
        file_part = {
            'mime_type': 'audio/wav',
            'data': audio_data
        }

        # Yapay zekaya verilecek dinamik talimat (Prompt)
        prompt = f"""
        Sen bir hayvan davranışları ve sesleri konusunda uzman bir yapay zekasın.
        Görevin, sana verilen {hayvan_turu_context} sesini ve KULLANICININ SAĞLADIĞI AŞAĞIDAKİ BAĞLAMI dikkate alarak analiz etmektir.

        ---
        **Kullanıcı Tarafından Sağlanan Ek Bilgi (Bağlam):**
        Hayvan Türü: {hayvan_turu_context}
        Durum: {durum_context}
        ---

        Lütfen bu bağlamı öncelikli olarak kullanarak, aşağıdaki formatta detaylı bir analiz sun:

        **1. Sesin Genel Tanımı:**
        (Örn: "Kısa, tiz ve tekrarlayan bir ses.")

        **2. Olası Duygusal Durum (Belirtilen Duruma Göre):**
        (Örn: "Belirtilen 'oyun oynarken' durumuna bakıldığında, bu ses yüksek ihtimalle heyecan ve davet içeriyor.")

        **3. Olası Anlamı ve İsteği ("Tercümesi"):**
        (Örn: "Hadi oynamaya devam edelim!", "Acıktım, yemek kabım boş.", "Beni rahat bırak, korkuyorum!")

        **4. Sahibine Tavsiye (Belirtilen Duruma ve Hayvan Türüne Göre):**
        (Örn: "Evcil hayvanınızın oyun isteğine karşılık verin.", "Evcil hayvanınız 'hastayken' bu sesi çıkarıyorsa, bir veteriner hekim ile danışmanız önerilir.")
        """

        # Pass the file part and prompt to generate_content
        response = model.generate_content([prompt, file_part])
        ai_yorumu = response.text
        print("Gemini'den analiz alındı.")

        # --- 4. Veriyi CSV Dosyasına Kaydet ---
        yeni_veri = {
            'id': [benzersiz_id], 'dosya_adi': [yeni_dosya_adi],
            'hayvan_turu': [hayvan_turu_context], 'belirtilen_durum': [durum_context], 'ai_yorumu': [ai_yorumu],
            'tarih': [datetime.now()]
        }
        df = pd.DataFrame(yeni_veri)
        df.to_csv(CSV_FILE, mode='a', header=not os.path.exists(CSV_FILE), index=False, encoding='utf-8-sig')
        print(f"Analiz '{CSV_FILE}' dosyasına kaydedildi.")

        return ai_yorumu, spektrogram_path

    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return f"Analiz sırasında bir hata oluştu: {e}", None

# --- Gradio Arayüzü (YENİ ELEMANLARLA) ---

# "Diğer..." seçildiğinde metin kutusunun görünürlüğünü güncelleyen fonksiyon
def update_visibility(secim):
    if secim == "Diğer...":
        return gr.Textbox(visible=True)
    else:
        return gr.Textbox(visible=False, value="")

# Arayüzü gr.Blocks ile oluşturuyoruz
with gr.Blocks() as demo:
    gr.Markdown("# 🐾 Tüm Hayvanlar İçin Bağlam Destekli Akıllı Ses Analizörü")  # Updated title
    gr.Markdown("""
    Evcil hayvanınızın sesini, hayvan türünü ve sesin çıktığı **durumu** belirtin. Gemini yapay zekası, verdiğiniz bu **bağlama göre** çok daha isabetli bir analiz yapsın.
    """)  # Updated description

    with gr.Row():
        with gr.Column(scale=1):
            # Girdi Bileşenleri
            audio_input = gr.Audio(
                sources=["microphone", "upload"], type="filepath",
                label="Hayvanınızın Sesini Yükleyin veya Canlı Kaydedin"  # Updated label
            )

            # Hayvan türü seçimi
            hayvan_turu_secenekleri = [
                "Kedi", "Köpek", "Kuş", "At", "İnek", "Koyun", "Keçi", "Domuz", "Tavuk", "Balık", "Diğer..."
            ]
            hayvan_turu_dropdown = gr.Dropdown(
                choices=hayvan_turu_secenekleri,
                label="Hayvan Türü Nedir?",
                value="Kedi"
            )

            durum_secenekleri = [
                "Genel (Durum Belirtilmedi)", "Oyun Oynarken", "Yemek Beklerken / Açken",
                "Tuvaletteyken", "Korkmuş / Stresliyken", "Hastayken / Acı Çekerken",
                "Uykudan Önce / Uyanırken", "Diğer Hayvanlarla İletişim Kurarken", "Diğer..."
            ]
            durum_dropdown = gr.Dropdown(
                choices=durum_secenekleri,
                label="Sesin Çıkarıldığı Durum Nedir?",
                value="Genel (Durum Belirtilmedi)"
            )

            diger_durum_input = gr.Textbox(
                label="Lütfen 'Diğer' durumu veya hayvan türünü açıklayınız:",  # Updated label
                placeholder="Örn: Veterinere giderken arabada... veya Tavşan",  # Updated placeholder
                interactive=True,
                visible=False
            )
            
            submit_btn = gr.Button("Analizi Başlat", variant="primary")

        with gr.Column(scale=2):
            # Çıktı Bileşenleri
            markdown_output = gr.Markdown(label="Yapay Zeka Hayvan Sesi Yorumcusu")  # Updated label
            image_output = gr.Image(type="filepath", label="Ses Spektrogramı")

    # Olayları (Events) Tanımlama
    
    # 1. Dropdown değiştiğinde, metin kutusunun görünürlüğünü güncelle
    hayvan_turu_dropdown.change(fn=update_visibility, inputs=hayvan_turu_dropdown, outputs=diger_durum_input)
    durum_dropdown.change(fn=update_visibility, inputs=durum_dropdown, outputs=diger_durum_input)

    # 2. Butona tıklandığında, ana analiz fonksiyonunu çalıştır
    submit_btn.click(
        fn=analyze_animal_sound,
        inputs=[audio_input, hayvan_turu_dropdown, durum_dropdown, diger_durum_input],
        outputs=[markdown_output, image_output]
    )
    
    gr.Markdown("""
    ---
    **Nasıl Çalışır?**
    1.  Bir ses dosyası yükleyin veya kaydedin.
    2.  **En önemli adım:** Sesin hangi hayvandan (kedi, köpek, kuş, vs.) geldiğini ve hangi durumda (oyun, yemek, hastalık vb.) çıkarıldığını açılır menüden seçin. Eğer durum veya hayvan türü listede yoksa, "Diğer..." seçip kendiniz yazın.
    3.  "Analizi Başlat" butonuna tıklayın. Yapay zeka, sesi, hayvan türünü ve belirttiğiniz durumu birlikte analiz ederek size özel bir yorum sunar.
    """)  # Updated instructions

if __name__ == "__main__":
    demo.launch(share=True)