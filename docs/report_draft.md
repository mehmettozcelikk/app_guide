# Accessible AI Application Guide — Hackathon Report (DRAFT)

## Problem & SDG
Complex official announcements are difficult for many applicants to interpret. Our prototype supports clearer access to application information for Turkish-speaking applicants. UN SDG 10 (Reduced Inequalities), potentially Target 10.2 (social inclusion). Intended impact: decrease the effort required to understand source documents. This potential must be tested with users before claiming an actual impact.

## Target users and workflow
Users paste public announcement text and select a reading level. The app generates a plain-language summary, conditions, documents, deadline, checklist and missing-information notes. It quotes relevant text for traceability. The app does not determine eligibility or submit applications.

## Model & prompt engineering
Model: [fill exact Gemini model/version used]. Platform: Google AI Studio / Gemini API Free Tier [verify]. We built zero-shot, few-shot and step-by-step prompt versions. The final prompt uses role, goal, context, constraints, style and structured JSON output. Why: improve extractive accuracy, reduce unsupported claims, and make the response machine-readable.

## Evaluation
Data: three fictional sample notices and one adversarial notice; actual source announcements may be used after removing personal data. Compare prompt versions under the same model and settings. Complete measured outcomes from `tests/evaluation_template.csv`: [real accuracy], [missing facts], [unsupported claims], [JSON validity]. Do not fabricate numbers.

## Ethics, limitations and mitigation
Risks: hallucinated deadlines, misleading eligibility advice, harmful bias, prompt injection and private data exposure. Safeguards: only supplied source text, direct source quotes, explicit missing-info labels, input PII screening, untrusted-document boundaries, and an instruction to verify original official sources. Quote matching does not guarantee factual interpretation; human review remains necessary. Free-tier provider data policies require caution with confidential data.

## Challenges & next steps
[Write actual technical difficulties and repairs after testing.] Next steps: improve anonymization and source verification, accessibility checks with real users, and controlled evaluation on genuine public notices.
