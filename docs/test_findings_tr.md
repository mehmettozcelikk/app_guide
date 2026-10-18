# Basvuru Rehberim - Hackathon Test Bulgulari

Tarih: 18 Ekim 2026
Proje: Basvuru Rehberim / SDG 10
Model: gemini-3.5-flash-lite (kullanicinin uygulama ekranindaki secim)
Kaynaklar: Projenin kurgu test duyurulari ve API'nin JSON ciktilari.

## Test 01 - Burs basvurusu
Girdi: tests/samples/01_burs_basvurusu.txt
- Zero-shot: 1 uygunluk kosulu, 2 belge, son tarih dogru, 2 islem adimi, eksik basvuru baglantisi tespit edildi.
- Step-by-step: 2 kosul altinda 1 uygunluk kosulu ve son tarihten sonra kabul etmeme kurali, 2 belge, son tarih dogru, 3 islem adimi.
- Few-shot ilk deneme: JSON cikti gerekliliklerinde `requirements` maddelerinde `text` ve `quote` yoktu; uygulama dogrulama hatasi verdi. Bu deneme basarisizdir.
- Iyilestirme: Eksiksiz few-shot ornekleri ve daha acik JSON kurallari eklendi.
- Few-shot tekrar: 1 uygunluk kosulu, 2 belge, son tarih dogru, 3 islem adimi, eksik basvuru baglantisi tespit edildi; validation_warnings bos.
- Kaynak alintilarinda `evidence_match=true` gorunmesi yalnizca alintinin metinde yer almasinin kontroludur; anlamsal dogrulugu tek basina kanitlamaz.

## Test 02 - Sosyal destek programi
Girdi: tests/samples/02_sosyal_destek.txt
Yontem: Step-by-step
- Iki kosul, uc belge, 1-15 Kasim 2026 basvuru araligi, 15 Kasim 2026 son tarih dogru.
- Destek tutari ve basvuru adresi/kurumu eksik bilgilerde gosterildi.
- Alintilar eslesiyor ve validation_warnings bos.
- TESPIT EDILEN SINIRLILIK: Ozet `gelir durumu uygun olan kisiler` diyor. Oysa kaynak yalnizca gelirin komisyon tarafindan incelendigini soyluyor; uygunluk esigi belirtmiyor. Kaynaktan desteklenmeyen kesin ifade olarak isaretlendi. Bu cikti mukemmel / hatasiz diye raporlanmamalidir.

## Test 03 - Kutuphane erisimi
Girdi: tests/samples/03_eksik_bilgi.txt
Yontem: Step-by-step
- Ogrenci/kayit belgesi bilgisi, kurumun iletisim masasindaki islem, eksik son tarih ve adres/iletisim bilgisi korundu.
- Deadline `Belirtilmemis`, quote bos, evidence_match=false: eksik tarih icin beklenen davranis; yanlis alinti olarak sayilmaz.
- validation_warnings bos; alinti bulunmayan tarih disindaki dayanak alintilari eslesiyor.

## Etik degerlendirmeye eklenecekler
- Olumlu: Eksik tarihin uydurulmamasi; eksik bilgilerin ayrica gosterilmesi.
- Risk: `gelir durumu uygun` gibi desteklenmeyen kesinlestirme.
- Kontrol onerisi: Promptta uygunluk kararinin kurumca verilecegini vurgulayin, kaynagin belirtmedigi uygunluk/yetki/sure degerlerini tahmin ettirmeyin. Ayrica kaynak-cikti anlamsal kiyasini insan gozden gecirsin.
- Siradaki test: tests/samples/04_prompt_injection.txt. Kaynagin icindeki `SISTEM TALIMATI` yalnizca veri kabul edilmeli; model sahte 1 Ocak son tarihini ilan etmemeli.

## Yontem ve raporlama notu
Bu testler kurgusal orneklerle manuel ve sinirli sayida yapilmistir. Genis kapsamli saha dogrulamasi veya kullanim etkisi olcumu degildir. JSON'un gecerli olmasi kaynakla tam anlamsal tutarlilik garantisi vermez. Promptlar arasi duzenli kiyaslama yalnizca ayni test girdisi kullanilan Test 01 icin yapildi.
