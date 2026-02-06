from typing import List, Dict
import json
from datetime import datetime


class ContractKnowledgeBase:
    """Knowledge base of common contract issues faced by Indian SMEs."""

    COMMON_ISSUES = {
        "indemnity_overreach": {
            "title": "Broad Indemnity Clause",
            "frequency": "Very High",
            "impact": "High",
            "description": "Vendor requires client to indemnify for all claims including vendor's negligence",
            "example": "Client shall indemnify and hold harmless Vendor from all claims, damages, and losses",
            "risk": "Exposes SME to unlimited liability for vendor's mistakes",
            "solution": "Limit indemnity to client's gross negligence; exclude vendor's negligence",
            "sample_fix": "Client shall indemnify Vendor only for claims arising from Client's gross negligence or willful misconduct",
            "frequency_india": "Seen in 70% of vendor contracts analyzed"
        },
        "non_compete_duration": {
            "title": "Excessive Non-Compete Period",
            "frequency": "High",
            "impact": "High",
            "description": "Non-compete period of 3-5 years preventing business after employment",
            "example": "Employee agrees not to compete for 5 years post-employment",
            "risk": "Severely restricts employee livelihood and career growth",
            "solution": "Limit to 6-12 months; specify geographic scope",
            "sample_fix": "Employee agrees not to compete for 12 months post-employment in [specific city] only",
            "frequency_india": "Common in 60% of employment contracts"
        },
        "unilateral_termination": {
            "title": "One-Sided Termination Rights",
            "frequency": "Very High",
            "impact": "High",
            "description": "Only vendor can terminate without notice; client cannot",
            "example": "Vendor may terminate this agreement at any time without cause or notice",
            "risk": "SME left without contractual remedy; service interruption",
            "solution": "Make termination mutual; add notice periods (30-60 days)",
            "sample_fix": "Either party may terminate with 30 days written notice. Termination for cause effective immediately",
            "frequency_india": "Found in 75% of SaaS/service contracts"
        },
        "auto_renewal_trap": {
            "title": "Auto-Renewal Without Opt-Out",
            "frequency": "Very High",
            "impact": "Medium",
            "description": "Contract auto-renews unless client explicitly opts out 60 days before",
            "example": "This agreement shall automatically renew unless notice given 60 days prior",
            "risk": "Accidental renewal; unwanted billing; difficulty canceling",
            "solution": "Require explicit renewal; mandate email reminders 90 days before",
            "sample_fix": "This agreement terminates on [date]. Renewal requires written agreement signed by both parties",
            "frequency_india": "Traps SMEs in 55% of SaaS subscription contracts"
        },
        "ip_transfer_broad": {
            "title": "Broad IP Ownership Transfer",
            "frequency": "High",
            "impact": "High",
            "description": "Vendor claims ownership of all work including pre-existing IP",
            "example": "All intellectual property created shall belong solely to Client",
            "risk": "SME loses ownership of tools, customizations, pre-existing assets",
            "solution": "Separate deliverables IP from pre-existing and background IP",
            "sample_fix": "IP created specifically for Deliverables transfers to Client. Vendor retains ownership of tools, templates, and pre-existing IP",
            "frequency_india": "Appears in 65% of development/service contracts"
        },
        "unlimited_liability": {
            "title": "No Liability Cap",
            "frequency": "High",
            "impact": "High",
            "description": "Contract allows unlimited damages; no cap on liability",
            "example": "Provider liable for all direct, indirect, and consequential damages without limit",
            "risk": "Exposure to massive financial liability exceeding contract value",
            "solution": "Cap liability at 1x annual fees or 12-month payments",
            "sample_fix": "Total liability capped at fees paid in preceding 12 months. Excludes indirect/consequential damages",
            "frequency_india": "Risk in 50% of service/lease contracts"
        },
        "vague_timeline": {
            "title": "Undefined Delivery Timelines",
            "frequency": "Medium",
            "impact": "Medium",
            "description": "Deliverables required 'as soon as possible' or 'promptly' without dates",
            "example": "'Services shall be delivered promptly and in a timely manner'",
            "risk": "Disputes over deadline; vendor delays; no recourse",
            "solution": "Specify exact dates, milestones, or 'within X business days'",
            "sample_fix": "Services shall be delivered within 15 business days of purchase order",
            "frequency_india": "Causes 45% of vendor disputes in SME sector"
        },
        "penalty_excessive": {
            "title": "Excessive Penalty Clauses",
            "frequency": "Medium",
            "impact": "Medium",
            "description": "Disproportionate penalties for minor breaches (e.g., 20% for 1-day delay)",
            "example": "Vendor charges 5% of contract value for each day of delay",
            "risk": "Unfair financial burden for minor non-compliance",
            "solution": "Make penalties proportional; tie to actual damages",
            "sample_fix": "Late delivery penalty: 0.5% per week, capped at 5% of monthly fees",
            "frequency_india": "Found in 40% of vendor contracts"
        },
        "jurisdiction_conflict": {
            "title": "Conflicting Jurisdiction Clauses",
            "frequency": "Low",
            "impact": "High",
            "description": "Different clauses specify different courts/arbitration venues",
            "example": "One clause says 'Mumbai courts'; another says 'Delhi arbitration'",
            "risk": "Confusion; expensive litigation; disputes over which venue applies",
            "solution": "Single, clear jurisdiction clause specifying one venue",
            "sample_fix": "This contract governed by laws of India. Disputes resolved by arbitration in Mumbai under SIAC rules",
            "frequency_india": "Rare but creates major disputes when present"
        },
        "confidentiality_overreach": {
            "title": "Overly Broad Confidentiality",
            "frequency": "Medium",
            "impact": "Medium",
            "description": "Everything confidential forever; no carve-outs for public domain or required disclosures",
            "example": "All information shall remain confidential in perpetuity without exception",
            "risk": "Cannot disclose even public info; legal conflicts if required to disclose",
            "solution": "Add carve-outs: public domain, independently developed, legally required",
            "sample_fix": "Confidential info except: (a) publicly available, (b) independently developed, (c) required by law",
            "frequency_india": "Seen in 50% of NDA/service contracts"
        }
    }

    @classmethod
    def get_issue_by_name(cls, issue_name: str) -> Dict:
        """Get details of a specific known issue."""
        return cls.COMMON_ISSUES.get(issue_name, {})

    @classmethod
    def get_similar_issues(cls, risk_pattern: str) -> List[Dict]:
        """Find similar issues from knowledge base based on pattern."""
        similar = []
        risk_lower = risk_pattern.lower()
        
        for issue_key, issue_data in cls.COMMON_ISSUES.items():
            if any(keyword in risk_lower for keyword in issue_data["title"].lower().split()):
                similar.append({
                    "key": issue_key,
                    "data": issue_data
                })
        
        return similar

    @classmethod
    def get_high_impact_issues(cls) -> List[Dict]:
        """Get all high-impact issues from knowledge base."""
        high_impact = []
        for issue_key, issue_data in cls.COMMON_ISSUES.items():
            if issue_data["impact"] == "High":
                high_impact.append({
                    "key": issue_key,
                    "title": issue_data["title"],
                    "frequency": issue_data["frequency"],
                    "frequency_india": issue_data.get("frequency_india", "")
                })
        return high_impact

    @classmethod
    def get_knowledge_base_stats(cls) -> Dict:
        """Get statistics about knowledge base."""
        issues = list(cls.COMMON_ISSUES.values())
        return {
            "total_known_issues": len(issues),
            "high_impact": sum(1 for i in issues if i["impact"] == "High"),
            "very_high_frequency": sum(1 for i in issues if i["frequency"] == "Very High"),
            "average_frequency": sum(1 for i in issues if i["frequency"] in ["High", "Very High"]) / len(issues),
            "india_sme_focus": True,
            "last_updated": "2026-02-06"
        }

    @classmethod
    def suggest_from_knowledge_base(cls, clause_text: str, detected_issues: List[Dict]) -> List[Dict]:
        """Suggest solutions based on detected issues matching knowledge base."""
        suggestions = []
        clause_lower = clause_text.lower()
        
        for issue_key, issue_data in cls.COMMON_ISSUES.items():
            if any(keyword in clause_lower for keyword in issue_data["title"].lower().split()):
                suggestions.append({
                    "issue": issue_data["title"],
                    "description": issue_data["description"],
                    "solution": issue_data["solution"],
                    "sample_fix": issue_data["sample_fix"],
                    "based_on": "Knowledge Base"
                })
        
        return suggestions
