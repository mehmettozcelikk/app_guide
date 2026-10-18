# Başvuru Rehberim / Accessible AI Application Guide

**Samsung Innovation Campus – SDG GenAI Hackathon (prototype)**

## Problem and audience
Official application announcements often contain complex language, scattered eligibility conditions, and easily missed deadlines. This prototype helps Turkish-speaking people who find those announcements difficult to understand. It summarizes the supplied text, extracts conditions/documents/deadlines, and creates a checklist.

**SDG:** SDG 10 (Reduced Inequalities), with a potential contribution to Target 10.2 through more accessible information. It is a prototype, not a proof of SDG impact.

**Important:** The assistant does not make eligibility decisions, submit applications, browse official websites, or guarantee that a notice is authentic or current.

## Features
- Text paste → live LLM analysis → structured results.
- Source-excerpt traceability for conditions, documents, and deadlines.
- Missing-information and privacy warnings.
- Three prompt versions: zero-shot, few-shot, and step-by-step (using the role/goal/context/constraints/style/output-format structure).
- Three fictional test notices, one adversarial notice, and recorded sample outputs in `tests/results/`.

## Tech stack
Python 3.11+ / Streamlit / Google GenAI SDK / an eligible Gemini API model.

## Start locally (macOS/Linux)
1. Install Python 3.11+ and open a terminal in this directory.
2. `python3 -m venv .venv`
3. `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `cp .env.example .env`
6. Add your Gemini API key to `.env` (never share or commit it). Confirm your model and account have **Free Tier** access at https://ai.google.dev/gemini-api/docs/pricing .
7. `python -m unittest discover -s tests -v`
8. `python api_smoke_test.py` (real Gemini connectivity check; report any problem before continuing).
9. `python -m streamlit run app.py`
10. Open the local URL, select a fictional notice and click **Örneği doldur → Duyuruyu analiz et**.

Optional: set `GEMINI_MODEL` in `.env` to a free-tier model available on your account. Tested with: `gemini-3.5-flash-lite` (verify current Free Tier availability in your account).

### Windows PowerShell
Activate using `.venv\Scripts\Activate.ps1` instead of `source .venv/bin/activate`. Copy `.env.example` to `.env` manually or use `Copy-Item .env.example .env`.

## Deployment (optional)
A repository may be deployed on Streamlit Community Cloud. Add `GEMINI_API_KEY` and (if required) `GEMINI_MODEL` to the deployed app's **Secrets** settings, **not** the repository. Do not publish it open to high-volume real-world usage without quotas, abuse handling, and an appropriate privacy notice.

## Prompt experiments
Use the same model/temperature and the same sample document for every version. Record conditions, documents, false claims, quote mismatches and JSON validity in `tests/evaluation_template.csv`. Do not invent measured results. Quoted excerpt matching only verifies exact text presence, not the semantic correctness of interpretation.

## Ethical safeguards and limitations
- Fictional sample notices; do not submit private personal data.
- Basic email, phone and 11-digit-number checks are not complete PII prevention.
- Explicit instructions to treat source text as untrusted data; adversarial testing is recommended.
- Source excerpts and missing-information labels reduce, but **do not eliminate**, hallucinations.
- This prototype requires human verification against the official announcement.

## Submission checklist
- [ ] Live model responds to a **new** pasted notice.
- [ ] Compare prompt versions; save real measurements.
- [ ] Complete the 1–2-page report, export to PDF, add to `docs/`.
- [ ] Complete an English presentation and publish its file or link.
- [ ] Record an ~5-min English demo with screen sharing and publish an accessible video link.
- [ ] Check public/authorized GitHub repository accessibility and README.
- [ ] Submit all links **before 18 October 2026, 19:00 (Türkiye time)**.

Source: Samsung Innovation Campus – *Hackathon Kılavuzu: SDG'ler için Üretken Yapay Zekâ*.

## Actual hackathon observations (18 October 2026)
- Gemini API smoke test and end-to-end Streamlit test were observed successful by the participant.
- Three prompting styles generated valid JSON on the first fictional burs announcement after fixing the few-shot schema examples.
- Original few-shot failed schema validation on an item missing `text` and `quote`. The pre-fix prompt is preserved in `prompts/few_shot_before_fix.txt`; current prompt is `prompts/few_shot.txt`.
- Second scenario produced an unsupported certainty about income eligibility despite matching quote excerpts; see `docs/test_findings_tr.md`.
- Third scenario correctly flagged an unspecified deadline; adversarial scenario ignored a fake instruction on one trial.
- `docs/report.pdf` describes the evaluation and limitations. Do not claim field-validated impact or universal robustness.
