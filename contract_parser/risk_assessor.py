from typing import Tuple, List
import re


class RiskAssessor:
    # Clause risk categories are Low / Medium / High
    def __init__(self):
        # basic keyword-driven rules
        self.rules = [
            (re.compile(r"indemnif", re.I), "High", "Indemnity clause found"),
            (re.compile(r"unilat|unilateral", re.I), "High", "Unilateral termination or action"),
            (re.compile(r"auto-?renew|auto renew|renewal", re.I), "Medium", "Auto-renewal detected"),
            (re.compile(r"liabilit|limitation of liabilit", re.I), "Medium", "Liability / limitation language"),
            (re.compile(r"non-?compete|non ?compete", re.I), "High", "Non-compete clause (restrictive)"),
            (re.compile(r"arbitrat|jurisdict", re.I), "Medium", "Arbitration / jurisdiction clause"),
            (re.compile(r"penalt|late fee|delay charge", re.I), "Medium", "Penalty or late fee clause"),
            (re.compile(r"intellectual property|ip transfer|assign of ip|assigns? rights", re.I), "High", "IP transfer or assignment clause"),
            (re.compile(r"confidenti|non ?disclos", re.I), "Low", "Confidentiality / NDA clause"),
        ]

    def score_clause(self, clause: str) -> Tuple[str, List[str]]:
        reasons = []
        weights = {"Low": 1, "Medium": 2, "High": 3}
        max_score = 0
        for pattern, level, reason in self.rules:
            if pattern.search(clause):
                reasons.append(reason)
                max_score = max(max_score, weights[level])

        # heuristics: long indemnities or monetary penalties increase score
        if re.search(r"\b(liquidated damages|damages|penalty)\b", clause, re.I):
            max_score = max(max_score, 3)

        if max_score == 3:
            return "High", reasons
        if max_score == 2:
            return "Medium", reasons
        return "Low", reasons

    def aggregate_scores(self, clause_scores: List[str]) -> str:
        # clause_scores: list of 'Low'/'Medium'/'High'
        mapping = {"Low": 1, "Medium": 2, "High": 3}
        if not clause_scores:
            return "Low"
        avg = sum(mapping.get(s, 1) for s in clause_scores) / len(clause_scores)
        if avg >= 2.5:
            return "High"
        if avg >= 1.5:
            return "Medium"
        return "Low"
