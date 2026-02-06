import spacy
from spacy.tokens import Doc
from typing import List, Dict
import re


class ContractNLP:
    def __init__(self, model_name: str = "en_core_web_sm"):
        try:
            self.nlp = spacy.load(model_name)
        except Exception:
            # fallback: blank English model
            self.nlp = spacy.blank("en")

    def process_text(self, text: str) -> Doc:
        # Basic cleaning and normalization
        text = text.replace("\r\n", "\n")
        return self.nlp(text)

    def extract_entities(self, doc: Doc) -> List[Dict]:
        entities = []
        for ent in doc.ents:
            entities.append({"text": ent.text, "label": ent.label_})
        # naive extractions for amounts and dates if spacy misses
        amounts = re.findall(r"\bRs\.?\s*[0-9,]+\b|\bINR\s*[0-9,]+\b|\b[0-9,]+\s*(?:rupees|Rs)\b", doc.text)
        for a in amounts:
            entities.append({"text": a, "label": "MONEY"})
        return entities

    def extract_clauses(self, doc: Doc) -> List[str]:
        # simple heuristic: split on line breaks and semicolons, keep length > 20
        raw = doc.text
        parts = re.split(r"\n{1,}|;|\.\s{2,}", raw)
        clauses = [p.strip() for p in parts if len(p.strip()) > 20]
        # limit to first 200 clauses for performance
        return clauses[:200]
