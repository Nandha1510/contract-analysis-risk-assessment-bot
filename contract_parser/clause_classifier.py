from typing import Dict, List
import re


class ClauseClassifier:
    """Classify extracted clauses into standard categories."""

    CLAUSE_CATEGORIES = {
        "payment_terms": {
            "keywords": ["payment", "invoice", "due date", "net", "advance", "installment", "interest"],
            "description": "Payment schedule and financial terms"
        },
        "liability_indemnity": {
            "keywords": ["indemnifi", "hold harmless", "liability", "damages", "compensation", "claim"],
            "description": "Liability limitations and indemnification"
        },
        "intellectual_property": {
            "keywords": ["intellectual property", "ip", "patent", "copyright", "trademark", "ownership", "assign"],
            "description": "IP rights and ownership"
        },
        "confidentiality_nda": {
            "keywords": ["confidential", "non-disclos", "proprietary", "secret", "nda"],
            "description": "Confidentiality and NDA obligations"
        },
        "termination": {
            "keywords": ["terminat", "expir", "end date", "dissolution", "cancellation"],
            "description": "Contract termination and end conditions"
        },
        "dispute_resolution": {
            "keywords": ["arbitrat", "jurisdict", "court", "governing law", "mediat", "dispute"],
            "description": "Dispute resolution and jurisdiction"
        },
        "warranties": {
            "keywords": ["warrant", "represent", "guarantee", "condition", "fitness"],
            "description": "Warranties and representations"
        },
        "obligations": {
            "keywords": ["shall", "must", "required", "obliged", "responsible"],
            "description": "Obligations and duties"
        },
        "rights": {
            "keywords": ["right to", "entitled", "may", "permitted", "allowed"],
            "description": "Rights and permissions"
        },
        "penalties": {
            "keywords": ["penalty", "fine", "breach", "violation", "non-compliance"],
            "description": "Penalties for breach or non-compliance"
        },
        "renewal_extension": {
            "keywords": ["renew", "extend", "renewal", "extension", "auto-renew"],
            "description": "Renewal and extension terms"
        },
        "limitation_of_liability": {
            "keywords": ["limitation of liability", "limit", "cap", "exclude", "not liable"],
            "description": "Liability limitation clauses"
        },
        "force_majeure": {
            "keywords": ["force majeure", "act of god", "unforeseen", "catastrophe"],
            "description": "Force majeure and unforeseeable events"
        },
        "severability": {
            "keywords": ["severability", "invalid", "void", "severable", "remainder"],
            "description": "Severability and validity"
        },
        "amendment": {
            "keywords": ["amend", "modif", "written consent", "change"],
            "description": "Amendment and modification procedures"
        }
    }

    @classmethod
    def classify_clause(cls, clause_text: str) -> Dict:
        """Classify a single clause into categories."""
        clause_lower = clause_text.lower()
        matches = {}
        
        for category, info in cls.CLAUSE_CATEGORIES.items():
            score = 0
            matched_keywords = []
            
            for keyword in info["keywords"]:
                if keyword.lower() in clause_lower:
                    score += 1
                    matched_keywords.append(keyword)
            
            if score > 0:
                matches[category] = {
                    "score": score,
                    "matched_keywords": matched_keywords,
                    "description": info["description"]
                }
        
        if not matches:
            return {
                "category": "general",
                "confidence": 0,
                "description": "General clause (no specific category matched)"
            }
        
        best_category = max(matches, key=lambda x: matches[x]["score"])
        best_score = matches[best_category]["score"]
        
        return {
            "category": best_category,
            "confidence": min(best_score / 4, 1.0),  # Normalize to 0-1
            "matched_keywords": matches[best_category]["matched_keywords"],
            "description": matches[best_category]["description"],
            "all_matches": matches
        }

    @classmethod
    def classify_clauses_batch(cls, clauses: List[str]) -> List[Dict]:
        """Classify multiple clauses."""
        results = []
        for i, clause in enumerate(clauses):
            classification = cls.classify_clause(clause)
            classification["clause_index"] = i
            classification["text"] = clause[:100] + "..." if len(clause) > 100 else clause
            results.append(classification)
        
        return results

    @classmethod
    def get_category_summary(cls, classified_clauses: List[Dict]) -> Dict:
        """Get summary of clause categories found."""
        category_counts = {}
        
        for clause in classified_clauses:
            category = clause.get("category", "general")
            if category not in category_counts:
                category_counts[category] = 0
            category_counts[category] += 1
        
        return {
            "total_clauses": len(classified_clauses),
            "categories_found": category_counts,
            "most_common": max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else None
        }
