import re
from typing import List, Dict


class ComplianceChecker:
    """Check contracts against Indian laws and standard compliance rules."""

    INDIAN_LAW_KEYWORDS = {
        "indian contract act": ["Indian Contract Act", "ICA", "1872"],
        "sale of goods act": ["Sale of Goods Act", "1930", "goods"],
        "labour law": ["Labour", "Employment", "Minimum Wage", "Working Hours", "ESI", "EPF"],
        "gst act": ["GST", "Goods and Services Tax", "IGST", "CGST"],
        "data protection": ["Data Protection", "Personal Data", "DISHA", "Privacy"],
        "companies act": ["Companies Act", "2013", "board", "directors"],
    }

    COMPLIANCE_RULES = [
        {
            "name": "Force Majeure Clause",
            "keywords": ["force majeure", "act of god", "unforeseen circumstances"],
            "severity": "Medium",
            "description": "Missing force majeure clause may expose parties to liability.",
            "india_specific": "Indian courts recognize force majeure under ICA 1872 Section 32",
        },
        {
            "name": "Dispute Resolution Mechanism",
            "keywords": ["arbitration", "mediation", "jurisdiction", "courts"],
            "severity": "High",
            "description": "Jurisdiction and arbitration should be clearly defined.",
            "india_specific": "Should specify Indian courts or arbitration under Arbitration & Conciliation Act 1996",
        },
        {
            "name": "Severability Clause",
            "keywords": ["severability", "invalid provision", "remainder"],
            "severity": "Medium",
            "description": "Severability clause ensures partial invalidity doesn't void the contract.",
            "india_specific": "Protects contract if parts found void under Indian law",
        },
        {
            "name": "Amendment Procedure",
            "keywords": ["amendment", "modification", "written consent"],
            "severity": "Low",
            "description": "Should specify how contract can be modified.",
            "india_specific": "Written amendments required for legal validity under ICA 1872",
        },
        {
            "name": "Limitation of Liability",
            "keywords": ["limitation of liability", "cap on liability", "damages"],
            "severity": "High",
            "description": "Liability caps protect both parties from excessive damages.",
            "india_specific": "Caps must be reasonable; ICA 1872 allows/disallows certain clauses",
        },
    ]

    INDIA_SPECIFIC_RULES = [
        {
            "name": "GST Compliance Clause",
            "keywords": ["GST", "tax", "Goods and Services Tax"],
            "severity": "High",
            "description": "GST compliance clause should clarify tax responsibilities in India",
            "requirement": "If contract involves goods/services in India, must address GST treatment"
        },
        {
            "name": "Labour Law Compliance",
            "keywords": ["employee", "worker", "labour", "wage"],
            "severity": "High",
            "description": "Employment contracts must comply with Indian labour laws",
            "requirement": "Must reference minimum wage, working hours, gratuity as per state law"
        },
        {
            "name": "Applicable Law Reference",
            "keywords": ["applicable law", "governing law", "indian law"],
            "severity": "High",
            "description": "Contract should specify Indian jurisdiction",
            "requirement": "Clear statement: 'This contract shall be governed by laws of India'"
        },
        {
            "name": "Arbitration Clause (India)",
            "keywords": ["arbitration", "arbitrator"],
            "severity": "Medium",
            "description": "Should reference Indian Arbitration & Conciliation Act 1996",
            "requirement": "Arbitration seat should be in India; venue specified"
        },
        {
            "name": "Notice Period (Employment)",
            "keywords": ["notice period", "termination notice", "notice"],
            "severity": "Medium",
            "description": "Employment termination should have adequate notice period",
            "requirement": "Minimum 30 days notice complies with most Indian state labour codes"
        },
        {
            "name": "Data Protection Clause",
            "keywords": ["data", "personal", "privacy", "protection"],
            "severity": "Medium",
            "description": "If personal data involved, must address DISHA and privacy",
            "requirement": "Compliance with Indian privacy and data protection standards"
        },
    ]

    @classmethod
    def check_compliance(cls, text: str) -> List[Dict]:
        """Check contract for generic compliance issues."""
        issues = []
        text_lower = text.lower()

        for rule in cls.COMPLIANCE_RULES:
            found = any(kw.lower() in text_lower for kw in rule["keywords"])
            if not found:
                issues.append({
                    "rule": rule["name"],
                    "status": "Missing",
                    "severity": rule["severity"],
                    "description": rule["description"],
                    "india_specific": rule.get("india_specific", ""),
                })
            else:
                issues.append({
                    "rule": rule["name"],
                    "status": "Present",
                    "severity": rule["severity"],
                    "description": f"{rule['name']} is present in the contract.",
                    "india_specific": rule.get("india_specific", ""),
                })

        return issues

    @classmethod
    def check_india_specific_compliance(cls, text: str) -> List[Dict]:
        """Check India-specific legal compliance."""
        issues = []
        text_lower = text.lower()

        for rule in cls.INDIA_SPECIFIC_RULES:
            found = any(kw.lower() in text_lower for kw in rule["keywords"])
            
            issues.append({
                "rule": rule["name"],
                "status": "Present" if found else "Missing",
                "severity": rule["severity"],
                "description": rule["description"],
                "requirement": rule["requirement"],
                "india_specific": True
            })

        return issues

    @classmethod
    def check_indian_law_references(cls, text: str) -> List[str]:
        """Check for references to Indian laws."""
        references = []
        text_lower = text.lower()

        for law, keywords in cls.INDIAN_LAW_KEYWORDS.items():
            if any(kw.lower() in text_lower for kw in keywords):
                references.append(law.title())

        return references

    @classmethod
    def generate_compliance_report(cls, text: str) -> Dict:
        """Generate comprehensive compliance report."""
        generic_issues = cls.check_compliance(text)
        india_issues = cls.check_india_specific_compliance(text)
        law_references = cls.check_indian_law_references(text)
        
        missing_generic = sum(1 for i in generic_issues if i["status"] == "Missing")
        missing_india = sum(1 for i in india_issues if i["status"] == "Missing")
        
        overall_status = "High Risk" if (missing_generic > 2 or missing_india > 3) else \
                        "Medium Risk" if (missing_generic > 0 or missing_india > 0) else \
                        "Compliant"
        
        return {
            "overall_compliance_status": overall_status,
            "generic_issues": generic_issues,
            "india_specific_issues": india_issues,
            "law_references": law_references,
            "missing_clauses": missing_generic + missing_india,
            "total_checks": len(generic_issues) + len(india_issues),
            "issues": generic_issues + india_issues,
        }

