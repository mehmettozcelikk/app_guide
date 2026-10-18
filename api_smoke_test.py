"""Run this first, before launching the web UI, to verify a REAL Gemini API call."""
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY", "")
model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
if not key or key.startswith("BURAYA_"):
    raise SystemExit("GEMINI_API_KEY eksik: .env dosyasina gercek API anahtarinizi ekleyin.")

try:
    from google import genai
    with genai.Client(api_key=key) as client:
        answer = client.models.generate_content(
            model=model,
            contents="Lutfen yalnizca 'BAGLANTI BASARILI' yaz."
        )
    print("Model yaniti:", answer.text)
    print("TEST SONUCU: Gemini API ile gercek baglanti kuruldu.")
except Exception as exc:
    print("TEST SONUCU: API baglantisi kurulamadi.")
    print("API anahtarini, model adini, bolgesel erisimi ve ucretsiz kotani kontrol edin.")
    print("Hata tipi:", type(exc).__name__)
    raise SystemExit(1)
