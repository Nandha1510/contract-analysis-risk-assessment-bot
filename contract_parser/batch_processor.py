from typing import List, Dict
import os
import json
from datetime import datetime
from contract_parser.parsers import parse_file
from contract_parser.advanced_nlp import ContractClassifier, EntityExtractor
from contract_parser.advanced_risk_assessor import AdvancedRiskAssessor
from contract_parser.compliance_checker import ComplianceChecker


class BatchProcessor:
    """Process multiple contracts in batch mode."""

    def __init__(self):
        self.classifier = ContractClassifier()
        self.entity_extractor = EntityExtractor()
        self.risk_assessor = AdvancedRiskAssessor()
        self.compliance_checker = ComplianceChecker()
        self.batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = []

    def process_batch(self, file_paths: List[str], output_dir: str = "batch_results") -> Dict:
        """Process multiple contract files and generate batch report."""
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        batch_results = {
            "batch_id": self.batch_id,
            "timestamp": datetime.now().isoformat(),
            "total_files": len(file_paths),
            "processed_count": 0,
            "failed_count": 0,
            "contracts": [],
            "summary": {}
        }

        for file_path in file_paths:
            try:
                contract_result = self._process_single_contract(file_path)
                batch_results["contracts"].append(contract_result)
                batch_results["processed_count"] += 1
            except Exception as e:
                batch_results["failed_count"] += 1
                batch_results["contracts"].append({
                    "file": os.path.basename(file_path),
                    "status": "Failed",
                    "error": str(e)
                })

        # Generate batch summary
        batch_results["summary"] = self._generate_batch_summary(batch_results["contracts"])

        # Save batch results
        output_file = os.path.join(output_dir, f"batch_analysis_{self.batch_id}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(batch_results, f, indent=2, ensure_ascii=False)

        return batch_results

    def _process_single_contract(self, file_path: str) -> Dict:
        """Process a single contract file."""
        
        # Parse file
        with open(file_path, "rb") as f:
            raw_text = parse_file(f)
        
        if not raw_text or len(raw_text) < 100:
            return {
                "file": os.path.basename(file_path),
                "status": "Failed",
                "reason": "File too small or empty"
            }

        # Classify contract
        classification = ContractClassifier.classify(raw_text)

        # Extract entities
        parties = EntityExtractor.extract_parties(raw_text)
        dates = EntityExtractor.extract_dates(raw_text)
        amounts = EntityExtractor.extract_amounts(raw_text)
        obligations = EntityExtractor.extract_obligations(raw_text)

        # Risk assessment (sample - first 100 clauses)
        clauses = raw_text.split("\n\n")[:100]
        clause_risks = []
        high_count = 0

        for clause in clauses:
            if len(clause.strip()) > 20:
                score = self.risk_assessor.score_clause_detailed(clause)
                if score["overall_risk"] == "High":
                    high_count += 1
                clause_risks.append(score["overall_risk"])

        contract_risk = self.risk_assessor.aggregate_risk(clause_risks)

        # Compliance check
        compliance = self.compliance_checker.check_compliance(raw_text)
        compliance_issues = sum(1 for c in compliance if c["status"] == "Missing")

        return {
            "file": os.path.basename(file_path),
            "status": "Processed",
            "contract_type": classification.get("type", "unknown"),
            "confidence": classification.get("confidence", 0),
            "parties_count": len(parties),
            "parties": parties[:3],  # First 3
            "dates_found": len(dates),
            "amounts_found": len(amounts),
            "total_obligations": len(obligations),
            "total_clauses_analyzed": len(clause_risks),
            "high_risk_clauses": high_count,
            "overall_risk": contract_risk,
            "compliance_issues": compliance_issues,
            "file_size_chars": len(raw_text)
        }

    def _generate_batch_summary(self, contracts: List[Dict]) -> Dict:
        """Generate summary statistics for batch."""
        processed = [c for c in contracts if c.get("status") == "Processed"]
        
        if not processed:
            return {"status": "No contracts processed"}

        high_risk_count = sum(1 for c in processed if c.get("overall_risk") == "High")
        medium_risk_count = sum(1 for c in processed if c.get("overall_risk") == "Medium")
        
        contract_types = {}
        for c in processed:
            ctype = c.get("contract_type", "unknown")
            contract_types[ctype] = contract_types.get(ctype, 0) + 1

        avg_compliance_issues = sum(c.get("compliance_issues", 0) for c in processed) / len(processed) if processed else 0
        avg_parties = sum(c.get("parties_count", 0) for c in processed) / len(processed) if processed else 0

        return {
            "total_analyzed": len(processed),
            "high_risk_contracts": high_risk_count,
            "medium_risk_contracts": medium_risk_count,
            "low_risk_contracts": len(processed) - high_risk_count - medium_risk_count,
            "contract_type_distribution": contract_types,
            "average_compliance_issues": round(avg_compliance_issues, 2),
            "average_parties_per_contract": round(avg_parties, 1),
            "total_high_risk_clauses": sum(c.get("high_risk_clauses", 0) for c in processed),
        }

    def compare_contracts(self, contracts_data: List[Dict]) -> Dict:
        """Compare multiple contracts for similarities and differences."""
        
        comparison = {
            "total_contracts": len(contracts_data),
            "comparison_date": datetime.now().isoformat(),
            "risk_distribution": {},
            "contract_type_distribution": {},
            "party_analysis": {},
            "high_risk_patterns": []
        }

        # Analyze risk distribution
        for contract in contracts_data:
            risk = contract.get("overall_risk", "Unknown")
            comparison["risk_distribution"][risk] = comparison["risk_distribution"].get(risk, 0) + 1

            # Contract type distribution
            ctype = contract.get("contract_type", "unknown")
            comparison["contract_type_distribution"][ctype] = comparison["contract_type_distribution"].get(ctype, 0) + 1

        return comparison
