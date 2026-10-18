"""Gemini integration and validation for Basvuru Rehberim."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

PROJECT_DIR = Path(__file__).resolve().parent
PROMPT_FILES = {
    "Zero-shot": "zero_shot.txt",
    "Few-shot": "few_shot.txt",
    "Step-by-step (final)": "final_prompt.txt",
}
LIST_FIELDS = ("requirements", "documents")
REQUIRED_FIELDS = ("summary", "requirements", "documents", "deadline", "steps", "missing_information", "notes")


class GuideError(Exception):
    """An application-friendly error."""


def detect_personal_data(text: str) -> list[str]:
    """Basic demonstration safeguards; deliberately not a full PII detector."""
    found: list[str] = []
    if re.search(r"(?<!\d)\d{11}(?!\d)", text):
        found.append("11 haneli numara")
    if re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text):
        found.append("e-posta adresi")
    # Common Turkish phone prefixes, including +90 or 0; minimize false positives.
    if re.search(r"(?<!\d)(?:\+90\s*|0\s*)?5\d{2}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}(?!\d)", text):
        found.append("telefon numarasi")
    return found


def render_prompt(source_text: str, reading_level: str, technique: str = "Step-by-step (final)") -> str:
    if technique not in PROMPT_FILES:
        raise GuideError("Bilinmeyen prompt teknigi.")
    template = (PROJECT_DIR / "prompts" / PROMPT_FILES[technique]).read_text(encoding="utf-8")
    return template.replace("{{READING_LEVEL}}", reading_level).replace("{{SOURCE_TEXT}}", source_text)


def _normalize_item_list(value: Any, label: str) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise GuideError(f"'{label}' alani bir liste olmali.")
    items: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict) or not isinstance(item.get("text"), str) or not isinstance(item.get("quote"), str):
            raise GuideError(f"'{label}' icindeki her oge 'text' ve 'quote' metinlerini icermeli.")
        if item["text"].strip():
            items.append({"text": item["text"].strip(), "quote": item["quote"].strip()})
    return items


def validate_guide(raw_json: str, original: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise GuideError("Model gecerli JSON dondurmedi; lutfen tekrar deneyin.") from exc
    if not isinstance(parsed, dict):
        raise GuideError("Modelin yaniti bir JSON nesnesi olmali.")
    missing = [f for f in REQUIRED_FIELDS if f not in parsed]
    if missing:
        raise GuideError("Modelin yanitinda alan eksik: " + ", ".join(missing))
    if not isinstance(parsed["summary"], str):
        raise GuideError("Ozet metin olmali.")
    for field in LIST_FIELDS:
        parsed[field] = _normalize_item_list(parsed[field], field)
    if not isinstance(parsed["deadline"], dict):
        raise GuideError("Son tarih alani nesne olmali.")
    for field in ("text", "quote"):
        if not isinstance(parsed["deadline"].get(field), str):
            raise GuideError(f"Son tarih alaninda '{field}' metni eksik.")
    for field in ("steps", "missing_information", "notes"):
        if not isinstance(parsed[field], list) or not all(isinstance(x, str) for x in parsed[field]):
            raise GuideError(f"'{field}' metin listesi olmali.")

    evidence_warnings: list[str] = []
    for field in LIST_FIELDS:
        for n, item in enumerate(parsed[field], start=1):
            item["evidence_match"] = bool(item["quote"] and item["quote"] in original)
            if not item["evidence_match"]:
                evidence_warnings.append(f"{field} #{n}: kaynak alinti eslesmedi.")

    deadline = parsed["deadline"]
    deadline["evidence_match"] = bool(deadline["quote"] and deadline["quote"] in original)
    if not deadline["evidence_match"] and deadline["text"].strip().casefold() not in ("belirtilmemiş", "belirtilmemis", "not stated", "not provided"):
        evidence_warnings.append("Son tarih: kaynak alinti eslesmedi.")

    # Matching an exact quote supports traceability; it does not prove the model's interpretation is correct.
    parsed["validation_warnings"] = evidence_warnings
    return parsed


def generate_guide(source_text: str, reading_level: str, technique: str, api_key: str, model: str) -> dict[str, Any]:
    if len(source_text.strip()) < 50:
        raise GuideError("Lutfen en az 50 karakterlik basvuru duyurusu girin.")
    if len(source_text) > 12000:
        raise GuideError("Prototip en fazla 12.000 karakter destekler.")
    pii = detect_personal_data(source_text)
    if pii:
        raise GuideError("Metinde olasi kisisel veri var (" + ", ".join(pii) + "). Lutfen anonimlestirin.")
    if not api_key.strip():
        raise GuideError("GEMINI_API_KEY tanimli degil. README'deki adimlari izleyin.")

    from google import genai
    from google.genai import types

    prompt = render_prompt(source_text, reading_level, technique)
    try:
        with genai.Client(api_key=api_key) as client:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )
    except Exception as exc:
        # Do not expose API keys or entire request payloads from provider error traces to end users.
        raise GuideError("Model istegi basarisiz. API anahtari, ucretsiz kota ve model adini kontrol edin. Ayrinti icin terminal kaydina bakin.") from exc
    if not getattr(response, "text", None):
        raise GuideError("Model bos yanit dondurdu; tekrar deneyin.")
    return validate_guide(response.text, source_text)


def api_key_from_environment() -> str:
    return os.environ.get("GEMINI_API_KEY", "")
