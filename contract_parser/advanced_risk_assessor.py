from typing import List, Dict, Tuple
import re


class AdvancedRiskAssessor:
    """Enhanced risk assessor with detailed scoring, ambiguity detection, and recommendations."""

    def __init__(self):
        self.detailed_rules = [
            # High Risk Rules
            {
                "name": "Broad Indemnity",
                "pattern": r"indemnif|hold harmless",
                "risk_level": "High",
                "reason": "Indemnity clauses can expose parties to significant liability",
                "recommendation": "Specify scope, carve out exceptions, limit to direct damages",
            },
            {
                "name": "Non-Compete Clause",
                "pattern": r"non-?compete|non ?compete",
                "risk_level": "High",
                "reason": "Overly broad non-compete is often unenforceable and restrictive",
                "recommendation": "Limit to 6-12 months, specific industries, defined geography",
            },
            {
                "name": "Unilateral Termination",
                "pattern": r"unilateral|can terminate|may terminate at will",
                "risk_level": "High",
                "reason": "One-sided termination rights imbalance the contract",
                "recommendation": "Make termination mutual with notice periods (30-60 days)",
            },
            {
                "name": "IP Assignment",
                "pattern": r"intellectual property|assign.*rights|ip transfer|assigns? all rights",
                "risk_level": "High",
                "reason": "Broad IP assignment may transfer unintended ownership",
                "recommendation": "Limit to deliverables only; retain ownership of pre-existing IP",
            },
            {
                "name": "No Liability Cap",
                "pattern": r"unlimited liability|no limit|no cap|all damages",
                "risk_level": "High",
                "reason": "Uncapped liability exposes parties to unlimited risk",
                "recommendation": "Cap at 1x annual fees or 12-month average payments",
            },
            # Medium Risk Rules
            {
                "name": "Auto-Renewal",
                "pattern": r"auto-?renew|auto renew|automatically renew|renewal unless",
                "risk_level": "Medium",
                "reason": "Auto-renewal can lock parties in without active consent",
                "recommendation": "Require explicit written renewal; mandate 60-day opt-out notice",
            },
            {
                "name": "Penalty Clauses",
                "pattern": r"penalty|late fee|liquidated damages|delay charge",
                "risk_level": "Medium",
                "reason": "Excessive penalties may be unenforceable as penalties (vs. liquidated damages)",
                "recommendation": "Ensure penalties are reasonable, pre-estimate actual loss",
            },
            {
                "name": "Jurisdiction/Arbitration Ambiguity",
                "pattern": r"jurisdict|arbitrat|venue|legal action",
                "risk_level": "Medium",
                "reason": "Unclear dispute resolution procedures lead to litigation costs",
                "recommendation": "Specify jurisdiction, arbitration seat, applicable law clearly",
            },
            {
                "name": "Lock-in Period",
                "pattern": r"lock-?in|locked in|minimum term|lock in period",
                "risk_level": "Medium",
                "reason": "Long lock-in periods limit flexibility",
                "recommendation": "Limit to 12 months; allow break clauses with notice",
            },
            {
                "name": "Broad Confidentiality",
                "pattern": r"confidential|proprietary|trade secret|non.disclos",
                "risk_level": "Low",
                "reason": "Overly broad confidentiality obligations may be impractical",
                "recommendation": "Include carve-outs: public domain, independently developed, required by law",
            },
            # Low Risk Rules
            {
                "name": "Ambiguous Language",
                "pattern": r"may|might|could|possibly|where applicable|as appropriate",
                "risk_level": "Low",
                "reason": "Vague language creates interpretation disputes",
                "recommendation": "Use precise terms: 'shall', 'must'; define 'best efforts'",
            },
        ]

    def score_clause_detailed(self, clause: str) -> Dict:
        """Score a clause with detailed analysis."""
        issues = []
        max_risk = "Low"

        for rule in self.detailed_rules:
            if re.search(rule["pattern"], clause, re.IGNORECASE):
                issues.append({
                    "name": rule["name"],
                    "risk_level": rule["risk_level"],
                    "reason": rule["reason"],
                    "recommendation": rule["recommendation"],
                })
                # Update max risk
                if rule["risk_level"] == "High":
                    max_risk = "High"
                elif rule["risk_level"] == "Medium" and max_risk != "High":
                    max_risk = "Medium"

        # Additional checks for very long clauses (often sign of poor drafting)
        if len(clause) > 1000:
            issues.insert(0, {
                "name": "Overly Long Clause",
                "risk_level": "Low",
                "reason": "Clause is unusually long; may contain multiple obligations",
                "recommendation": "Break into sub-clauses for clarity",
            })

        # Check for ambiguous/undefined terms
        undefined_terms = re.findall(r'"([^"]+)"|\'([^\']+)\'', clause)
        if undefined_terms and len(undefined_terms) > 3:
            issues.insert(0, {
                "name": "Many Quoted Terms",
                "risk_level": "Low",
                "reason": "Multiple quoted terms suggest special definitions needed",
                "recommendation": "Add a definitions section or use defined terms consistently",
            })

        return {
            "overall_risk": max_risk,
            "issues_found": len(issues),
            "detailed_issues": issues,
        }

    def detect_ambiguities(self, clause: str) -> List[Dict]:
        """Detect ambiguous phrasing in a clause."""
        ambiguities = []

        # Undefined "best efforts"
        if re.search(r"best efforts|commercially reasonable", clause, re.IGNORECASE):
            ambiguities.append({
                "type": "Undefined Standard",
                "phrase": "best efforts / commercially reasonable",
                "problem": "Not defined; open to interpretation",
                "suggestion": "Define explicitly: 'using reasonable efforts consistent with industry standards'",
            })

        # Time references without specificity
        if re.search(r"\bsoon\b|\basap\b|promptly|immediately", clause, re.IGNORECASE):
            ambiguities.append({
                "type": "Vague Timeline",
                "phrase": "soon / ASAP / promptly",
                "problem": "No specific timeframe given",
                "suggestion": "Specify: 'within [X] days' or 'within [X] business days'",
            })

        # Conditional obligations without clarity
        if re.search(r"if.*then|subject to|depending on|as applicable", clause, re.IGNORECASE):
            ambiguities.append({
                "type": "Conditional Obligation",
                "phrase": "if-then / subject to",
                "problem": "Conditions may be ambiguous or too flexible",
                "suggestion": "Clearly specify all conditions and consequences",
            })

        return ambiguities

    def aggregate_risk(self, clause_scores: List[str]) -> str:
        """Aggregate clause-level scores to contract risk."""
        if not clause_scores:
            return "Low"

        high_count = clause_scores.count("High")
        medium_count = clause_scores.count("Medium")

        if high_count > 0:
            return "High"
        if medium_count > 2:
            return "High"
        if medium_count > 0:
            return "Medium"
        return "Low"
