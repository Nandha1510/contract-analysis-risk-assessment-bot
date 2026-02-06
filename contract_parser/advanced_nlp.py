import re
from typing import List, Dict, Tuple
from difflib import SequenceMatcher
import nltk
from nltk.tokenize import sent_tokenize

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)


class HindiNormalizer:
    """Handles Hindi to English transliteration and normalization for multilingual contracts."""

    HINDI_ENGLISH_MAP = {
        "अग्रीमेंट": "Agreement",
        "पार्टी": "Party",
        "तारीख": "Date",
        "भुगतान": "Payment",
        "अवधि": "Term",
        "समाप्ति": "Termination",
        "गोपनीयता": "Confidentiality",
        "दायित्व": "Liability",
        "क्षतिपूर्ति": "Indemnity",
        "बौद्धिक संपदा": "Intellectual Property",
        "लागू कानून": "Governing Law",
        "मध्यस्थता": "Arbitration",
    }

    @classmethod
    def normalize(cls, text: str) -> str:
        """Convert Hindi words to English equivalents."""
        normalized = text
        for hindi, english in cls.HINDI_ENGLISH_MAP.items():
            normalized = normalized.replace(hindi, english)
        return normalized


class ClauseSimilarity:
    """Finds similar clauses across contracts and templates using sequence matching."""

    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold

    def similarity_score(self, text1: str, text2: str) -> float:
        """Compute similarity between two clause texts (0-1)."""
        s = SequenceMatcher(None, text1.lower(), text2.lower())
        return s.ratio()

    def find_similar_clauses(self, clause: str, template_clauses: List[str]) -> List[Dict]:
        """Find similar clauses from a template."""
        results = []
        for tmpl_clause in template_clauses:
            score = self.similarity_score(clause, tmpl_clause)
            if score >= self.threshold:
                results.append({
                    "template_clause": tmpl_clause,
                    "similarity_score": score,
                })
        return sorted(results, key=lambda x: x["similarity_score"], reverse=True)


class ContractClassifier:
    """Classify contract type based on content."""

    TYPES = {
        "employment": ["employment", "employee", "salary", "benefits", "termination of employment"],
        "vendor": ["vendor", "supplier", "purchase", "delivery", "goods", "services"],
        "lease": ["lease", "tenant", "landlord", "rent", "property", "premises"],
        "partnership": ["partnership", "partner", "profit sharing", "equity", "dissolution"],
        "service": ["service", "client", "deliverables", "scope", "milestones"],
        "nda": ["confidential", "disclosure", "non-disclosure", "proprietary"],
    }

    @classmethod
    def classify(cls, text: str) -> Dict:
        """Classify the contract type."""
        text_lower = text.lower()
        scores = {}
        for ctype, keywords in cls.TYPES.items():
            count = sum(text_lower.count(kw) for kw in keywords)
            scores[ctype] = count
        if not any(scores.values()):
            return {"type": "unknown", "confidence": 0}
        best_type = max(scores, key=scores.get)
        confidence = scores[best_type] / sum(scores.values()) if sum(scores.values()) > 0 else 0
        return {"type": best_type, "confidence": min(confidence, 1.0)}


class EntityExtractor:
    """Advanced NER for legal contracts."""

    @staticmethod
    def extract_parties(text: str) -> List[str]:
        """Extract party names."""
        parties = []
        # Simple heuristic: look for "BETWEEN ... AND" or "Parties:" patterns
        between_match = re.search(r"BETWEEN\s+([^A-Z]+?)\s+AND\s+([^A-Z]+?)(?:\.|:|$)", text, re.IGNORECASE)
        if between_match:
            parties.append(between_match.group(1).strip())
            parties.append(between_match.group(2).strip())
        parties_match = re.findall(r"(?:Party|Parties?)[:\s]+([^\n]+)", text, re.IGNORECASE)
        parties.extend([p.strip() for p in parties_match])
        return list(set(p for p in parties if len(p) > 3))

    @staticmethod
    def extract_dates(text: str) -> List[str]:
        """Extract dates from text."""
        date_patterns = [
            r"\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}",
            r"\d{1,2}/\d{1,2}/\d{4}",
            r"\d{4}-\d{1,2}-\d{1,2}",
        ]
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, text))
        return list(set(dates))

    @staticmethod
    def extract_amounts(text: str) -> List[Dict]:
        """Extract monetary amounts."""
        amounts = []
        patterns = [
            (r"(?:Rs|INR|Rupees?)\s*[.\s]?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)", "INR"),
            (r"\$\s*(\d{1,3}(?:,,\d{3})*(?:\.\d{2})?)", "USD"),
            (r"(?:USD|US\$)\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)", "USD"),
        ]
        for pattern, currency in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                amounts.append({"amount": match, "currency": currency})
        return amounts

    @staticmethod
    def extract_jurisdiction(text: str) -> List[str]:
        """Extract jurisdiction/venue information."""
        jurisdictions = []
        patterns = [
            r"(?:jurisdiction|governed by|applicable law)[:\s]+([^.,\n]+)",
            r"(?:courts of|venue|seat of arbitration)[:\s]+([^.,\n]+)",
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            jurisdictions.extend(matches)
        return list(set(j.strip() for j in jurisdictions if j.strip()))

    @staticmethod
    def extract_key_dates(text: str) -> List[Dict]:
        """Extract important dates with context."""
        dates = []
        date_patterns = [
            (r"(?:Effective Date|Execution Date)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})", "effective_date"),
            (r"(?:Expiry|Termination|End Date)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})", "expiry_date"),
            (r"(?:Renewal|Anniversary)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})", "renewal_date"),
        ]
        for pattern, date_type in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                dates.append({"date": match, "type": date_type})
        return dates

    @staticmethod
    def extract_payment_terms(text: str) -> List[Dict]:
        """Extract payment-related information."""
        payments = []
        patterns = [
            (r"(?:Payment Term|Due|Net)[:\s]+([^.\n]+)", "payment_term"),
            (r"(?:Invoice|Billing)[:\s]+([^.\n]+)", "invoice_term"),
        ]
        for pattern, term_type in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                payments.append({"term": match.strip(), "type": term_type})
        return payments

    @staticmethod
    def extract_obligations(text: str) -> List[str]:
        """Extract obligation phrases."""
        obligations = []
        keywords = ["shall", "must", "required to", "obliged to", "responsible for"]
        sentences = sent_tokenize(text)
        for sent in sentences:
            if any(kw in sent.lower() for kw in keywords):
                obligations.append(sent.strip())
        return obligations[:50]  # limit to first 50

    @staticmethod
    def extract_rights(text: str) -> List[str]:
        """Extract rights phrases."""
        rights = []
        keywords = ["right to", "entitled to", "may", "permitted to", "may choose"]
        sentences = sent_tokenize(text)
        for sent in sentences:
            if any(kw in sent.lower() for kw in keywords):
                rights.append(sent.strip())
        return rights[:50]

    @staticmethod
    def extract_prohibitions(text: str) -> List[str]:
        """Extract prohibition phrases."""
        prohibitions = []
        keywords = ["shall not", "cannot", "prohibited", "no right to", "not permitted"]
        sentences = sent_tokenize(text)
        for sent in sentences:
            if any(kw in sent.lower() for kw in keywords):
                prohibitions.append(sent.strip())
        return prohibitions[:50]
