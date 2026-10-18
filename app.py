"""Basvuru Rehberim: Streamlit demo for Samsung Innovation Campus SDG hackathon."""
from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from ai_service import GuideError, PROMPT_FILES, api_key_from_environment, generate_guide, detect_personal_data

load_dotenv()
st.set_page_config(page_title="Başvuru Rehberim", page_icon="📄", layout="centered")

st.title("📄 Başvuru Rehberim")
st.caption("SDG 10 • Karmaşık başvuru duyurularını anlaşılır adımlara dönüştürür")
st.info("Eğitim amaçlı AI prototipidir. Resmî başvuru şartlarını ilgili kurumun duyurusundan doğrulayın.")

SAMPLES = Path(__file__).resolve().parent / "tests" / "samples"
DEMO_FILES = sorted(SAMPLES.glob("*.txt"))

with st.sidebar:
    st.header("Model ve analiz")
    model = st.text_input("Gemini model", value=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
    technique = st.selectbox("Prompt tekniği", options=list(PROMPT_FILES), index=2,
                             help="Değişen promptlarla aynı duyuruyu karşılaştırabilirsiniz.")
    reading_level = st.radio("Açıklama düzeyi", options=("Kolay Türkçe", "Standart Türkçe"), index=0)
    st.caption("API anahtarı .env veya GEMINI_API_KEY ortam değişkeninden alınır; arayüzde gösterilmez.")

if "source_text" not in st.session_state:
    st.session_state["source_text"] = ""

col_a, col_b = st.columns([2, 1])
with col_a:
    selection = st.selectbox("Örnek duyuru", ["Kendim gireceğim"] + [p.stem.replace("_", " ").title() for p in DEMO_FILES])
with col_b:
    st.write(" ")
    if st.button("Örneği doldur", disabled=selection == "Kendim gireceğim"):
        index = [p.stem.replace("_", " ").title() for p in DEMO_FILES].index(selection)
        st.session_state["source_text"] = DEMO_FILES[index].read_text(encoding="utf-8")

source = st.text_area("Resmî duyuru metni", key="source_text", height=230,
                      placeholder="Kimlik numarası veya kişisel bilgiler içermeyen duyuru metnini buraya yapıştırın...")
st.caption(f"{len(source):,} / 12.000 karakter • Kişisel veriler içeren metinleri göndermeyin.")

if source and detect_personal_data(source):
    st.warning("Metin olası kişisel veri içeriyor. Analizden önce anonimleştirin.")

if st.button("🔎 Duyuruyu analiz et", type="primary", use_container_width=True):
    # Prevent a failed prompt attempt from leaving a previous technique's output on screen.
    st.session_state.pop("result", None)
    st.session_state.pop("analyzed_source", None)
    st.session_state.pop("technique", None)
    try:
        key = api_key_from_environment()
        # For Streamlit Community Cloud deployment, store GEMINI_API_KEY in app secrets.
        if not key:
            try:
                key = st.secrets.get("GEMINI_API_KEY", "")
            except Exception:
                key = ""
        with st.spinner("Model kaynağı inceliyor..."):
            result = generate_guide(source, reading_level, technique, key, model)
        st.session_state["result"] = result
        st.session_state["analyzed_source"] = source
        st.session_state["technique"] = technique
    except GuideError as exc:
        st.error(str(exc))
    except Exception:
        st.error("Beklenmeyen hata. Terminal çıktısını kontrol edin; API anahtarını paylaşmayın.")

if "result" in st.session_state:
    result = st.session_state["result"]
    st.divider()
    st.caption("Analiz yöntemi: " + st.session_state.get("technique", ""))
    st.subheader("Anlaşılır açıklama")
    st.write(result["summary"])

    st.subheader("Başvuru şartları")
    if not result["requirements"]:
        st.write("Metinde açık şart bulunamadı.")
    for item in result["requirements"]:
        st.markdown("- " + item["text"])
        st.caption(("✅ Birebir kaynak alıntısı: " if item["evidence_match"] else "⚠️ Doğrulanamayan alıntı: ") + (item["quote"] or "Alıntı yok"))

    st.subheader("Gerekli belgeler")
    if not result["documents"]:
        st.write("Metinde açık belge bulunamadı.")
    for item in result["documents"]:
        st.markdown("- " + item["text"])
        st.caption(("✅ Birebir kaynak alıntısı: " if item["evidence_match"] else "⚠️ Doğrulanamayan alıntı: ") + (item["quote"] or "Alıntı yok"))

    st.subheader("Son başvuru tarihi")
    st.write(result["deadline"]["text"])
    if result["deadline"]["quote"]:
        st.caption(("✅ " if result["deadline"]["evidence_match"] else "⚠️ Doğrulanamayan alıntı: ") + result["deadline"]["quote"])

    st.subheader("Kontrol listesi")
    for i, step in enumerate(result["steps"], 1):
        st.markdown(f"{i}. {step}")

    if result["missing_information"]:
        st.warning("**Eksik/belirsiz bilgiler:** " + " | ".join(result["missing_information"]))
    if result["validation_warnings"]:
        st.error("**Kaynak doğrulama uyarısı:** " + " | ".join(result["validation_warnings"]))
    if result["notes"]:
        st.caption("Notlar: " + " | ".join(result["notes"]))
    st.info("Bu sonuç yalnızca verilen metinden türetilmiştir; alıntıların eşleşmesi yorumun doğruluğunu tek başına garanti etmez. Resmî kaynağı kontrol edin.")
    st.download_button("JSON sonucu indir", data=__import__("json").dumps(result, ensure_ascii=False, indent=2),
                       file_name="basvuru_analizi.json", mime="application/json")
