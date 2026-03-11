import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.utils.format_utils import format_json_as_markdown

# Test the JSON formatting function with the data you provided
test_json_data = {
    "analiz_basligi": "Kedi Vocalizasyon Analizi - Oyun Oynarken",
    "hayvan_bilgileri": {
        "tur": "Kedi",
        "yas": "4",
        "cinsiyet": "Erkek",
        "saglik_durumu": "Sağlıklı"
    },
    "ses_verileri": {
        "sure": "2.95 saniye",
        "frekans_araligi": "(0, 22050.0) Hz",
        "yogunluk": "51.08 dB",
        "dominant_frekans": "3056.16 Hz"
    },
    "baglam": "Oyun Oynarken",
    "profesyonel_analiz": {
        "aciliyet_seviyesi": 1,
        "tespit_edilen_duygu_durumu": "Bu ses, kedilerin avlanma içgüdüsü tetiklendiğinde veya oyuncak/av hedefine odaklandığında çıkardığı 'chattering' veya 'trilling' (çatırdayan veya titrek ses) olarak bilinen tipik bir vokalizasyondur. Dominant frekansın 3000 Hz'nin üzerinde olması, bu tür yüksek perdeli ve kısa süreli seslerle tutarlıdır. Kedinizin bu sesle birlikte ağız hareketleri (dişlerini birbirine vurur gibi) gözlemlenmesi muhtemeldir. Bu, genellikle yoğun odaklanma, heyecan, avlanma dürtüsü ve bazen de avı yakalayamama veya ulaşamama durumunda ortaya çıkan hafif bir frustrasyon veya gerginlik ile ilişkilidir. Kısacası, kediniz 'Avımı yakalamak istiyorum!' veya 'Çok heyecanlıyım!' demektedir.",
        "olasi_ihtiyac_veya_sorun": {
            "ihtiyac": "Kedinin avlanma içgüdüsünü tatmin etme, zihinsel ve fiziksel uyarım. Kedinizin doğal avlanma döngüsünü (kovalama, yakalama, 'öldürme') tamamlamasına olanak tanıyan daha tatmin edici ve etkileşimli oyunlar oynamaya devam etmek.",
            "sorun": "Bu vokalizasyonun kendisi bir sorun değildir; aksine sağlıklı bir kedinin doğal ve içgüdüsel bir davranışıdır. Ancak, eğer kedi sürekli olarak ulaşamadığı bir hedefe (örn. pencere dışındaki kuşlar, ulaşılmaz bir oyuncak) bu şekilde tepki veriyor ve bu durum aşırıya kaçıyorsa, bu durum kedide zamanla frustrasyon birikimine yol açabilir. Oyun seanslarının sonunda avı yakalayamaması, bu frustrasyonu artırabilir."
        },
        "sahibe_tavsiyeler": [
            "**Davranışı Anlayın:** Kedinizin bu sesi çıkarması tamamen doğal ve sağlıklı bir avlanma davranışıdır. Endişe etmenize gerek yoktur.",
            "**Etkileşimli Oyunları Sürdürün:** Kedinizin avlanma içgüdülerini tatmin edecek, 'kovalama-yakalama-öldürme' döngüsünü tamamlamasına olanak tanıyan interaktif oyunlar oynamaya devam edin. Oltalı oyuncaklar, yakalayabileceği ve ağzına alıp taşıyabileceği oyuncaklar (örneğin tüylü fareler) tercih edin.",
            "**Oyunları Doğru Bitirin:** Oyun seanslarını, kedinizin 'avı yakalayıp öldürmesine' (yani oyuncağı ele geçirmesine, birkaç kez ısırmasına veya patilemesine) ve sonunda küçük bir ödül (mama veya ödül maması) almasına izin vererek bitirin. Bu, avlanma dürtüsünün tatmin edilmesine yardımcı olur ve frustrasyonu azaltır.",
            "**Çevresel Zenginleştirme:** Kedinizin çevresini zenginleştirerek (tırmanma ağaçları, tüneller, pencere kenarı gözlem noktaları) zihinsel uyarım sağlamaya devam edin."
        ],
        "veteriner_kontrolu_gerekli_mi": "Hayır. Mevcut bilgiler ve bağlam (sağlıklı bir kedi, oyun sırasında çıkarılan ses) göz önüne alındığında, bu ses tamamen normal bir davranıştır ve veteriner kontrolü gerektirmez. Ancak, eğer kedi bu sesleri aşırı sık ve stres belirtileriyle birlikte (iştahsızlık, saklanma, aşırı yalanma, agresyon vb.) gösteriyorsa, genel sağlık kontrolü için veteriner hekime danışılması uygun olabilir. Bu sesin sadece oyun esnasında olması, endişe edilecek bir durum olmadığını göstermektedir.",
        "guven_skoru": 98
    }
}

print("Testing JSON to Markdown formatting...")
formatted = format_json_as_markdown(test_json_data)
print(formatted)