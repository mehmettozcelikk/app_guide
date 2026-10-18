import json
import unittest

from ai_service import GuideError, detect_personal_data, render_prompt, validate_guide

SOURCE = "Öğrenciler başvurabilir. Öğrenci belgesi zorunludur. Son gün 25 Ekim 2026."


def sample():
    return {
        "summary": "Öğrenciler başvurabilir.",
        "requirements": [{"text": "Öğrenciler", "quote": "Öğrenciler başvurabilir"}],
        "documents": [{"text": "Öğrenci belgesi", "quote": "Öğrenci belgesi zorunludur"}],
        "deadline": {"text": "25 Ekim 2026", "quote": "Son gün 25 Ekim 2026"},
        "steps": ["Öğrenci belgesini hazırlayın"],
        "missing_information": [],
        "notes": ["Resmî duyuruyu doğrulayın"],
    }


class AIServiceTests(unittest.TestCase):
    def test_render_all_three_prompts(self):
        for tech in ("Zero-shot", "Few-shot", "Step-by-step (final)"):
            prompt = render_prompt(SOURCE, "Kolay Türkçe", tech)
            self.assertIn(SOURCE, prompt)
            self.assertNotIn("{{SOURCE_TEXT}}", prompt)
            self.assertIn("Kolay Türkçe", prompt)

    def test_few_shot_example_schema_matches_validator(self):
        from pathlib import Path
        import re
        prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "few_shot.txt"
        body = prompt_path.read_text(encoding="utf-8")
        examples = re.findall(r"ÖRNEK JSON:\s*(\{.*?\})\s*(?=\n\[EXAMPLE|\n\[NEW TASK\])", body, re.DOTALL)
        self.assertEqual(len(examples), 2)
        for example in examples:
            parsed = json.loads(example)
            self.assertIsInstance(parsed["requirements"], list)
            self.assertIsInstance(parsed["documents"], list)
            for field in ("requirements", "documents"):
                for entry in parsed[field]:
                    self.assertIsInstance(entry["text"], str)
                    self.assertIsInstance(entry["quote"], str)
            self.assertIsInstance(parsed["deadline"]["text"], str)
            self.assertIsInstance(parsed["deadline"]["quote"], str)

    def test_valid_json_quote_match(self):
        guide = validate_guide(json.dumps(sample(), ensure_ascii=False), SOURCE)
        self.assertEqual(guide["validation_warnings"], [])
        self.assertTrue(guide["requirements"][0]["evidence_match"])

    def test_wrong_quote_detected(self):
        example = sample()
        example["documents"][0]["quote"] = "olmayan alıntı"
        guide = validate_guide(json.dumps(example, ensure_ascii=False), SOURCE)
        self.assertEqual(len(guide["validation_warnings"]), 1)

    def test_wrong_schema_rejected(self):
        with self.assertRaises(GuideError):
            validate_guide('{"summary":"only this"}', SOURCE)

    def test_pii_block(self):
        self.assertIn("e-posta adresi", detect_personal_data("example@sample.com"))
        self.assertIn("11 haneli numara", detect_personal_data("12345678901"))
        self.assertEqual(detect_personal_data(SOURCE), [])


if __name__ == "__main__":
    unittest.main()
