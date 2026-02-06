"""
Integration Guide for Contract Analysis Bot
This module shows how to use the bot programmatically (not just via Streamlit UI)
"""

from contract_parser.parsers import parse_file
from contract_parser.nlp import ContractNLP
from contract_parser.advanced_nlp import (
    ContractClassifier,
    EntityExtractor,
    ClauseSimilarity,
    HindiNormalizer,
)
from contract_parser.advanced_risk_assessor import AdvancedRiskAssessor
from contract_parser.compliance_checker import ComplianceChecker
from contract_parser.template_generator import TemplateGenerator
from utils.audit import AuditLogger
import json


class ContractAnalysisAPI:
    """
    Programmatic API for contract analysis.
    Use this if you want to integrate the bot with other systems.
    """

    def __init__(self):
        self.nlp = ContractNLP()
        self.classifier = ContractClassifier()
        self.entity_extractor = EntityExtractor()
        self.risk_assessor = AdvancedRiskAssessor()
        self.compliance_checker = ComplianceChecker()
        self.audit = AuditLogger("audit_logs.json")

    def analyze_contract_text(self, text: str, language: str = "English") -> dict:
        """
        Analyze contract from raw text.
        
        Args:
            text: Contract content as string
            language: "English" or "Hindi"
        
        Returns:
            dict with analysis results
        """
        # Normalize if Hindi
        if language == "Hindi":
            text = HindiNormalizer.normalize(text)

        # Classify
        classification = self.classifier.classify(text)

        # Extract entities
        parties = self.entity_extractor.extract_parties(text)
        dates = self.entity_extractor.extract_dates(text)
        amounts = self.entity_extractor.extract_amounts(text)
        obligations = self.entity_extractor.extract_obligations(text)
        rights = self.entity_extractor.extract_rights(text)
        prohibitions = self.entity_extractor.extract_prohibitions(text)

        # Process NLP
        doc = self.nlp.process_text(text)
        clauses = self.nlp.extract_clauses(doc)

        # Score clauses
        clause_results = []
        for i, clause in enumerate(clauses):
            detailed_score = self.risk_assessor.score_clause_detailed(clause)
            ambiguities = self.risk_assessor.detect_ambiguities(clause)
            clause_results.append({
                "clause_index": i,
                "text": clause[:200],
                "risk_level": detailed_score["overall_risk"],
                "issues_count": detailed_score["issues_found"],
                "ambiguities_count": len(ambiguities),
            })

        # Contract-level risk
        contract_risk = self.risk_assessor.aggregate_risk(
            [c["risk_level"] for c in clause_results]
        )

        # Compliance
        compliance = self.compliance_checker.generate_compliance_report(text)

        # Log event
        self.audit.log_event("contract_analyzed", {
            "contract_type": classification["type"],
            "clause_count": len(clauses),
            "risk_level": contract_risk,
        })

        return {
            "metadata": {
                "contract_type": classification["type"],
                "confidence": classification["confidence"],
                "total_clauses": len(clauses),
                "total_chars": len(text),
            },
            "entities": {
                "parties": parties,
                "dates": dates,
                "amounts": amounts,
                "obligations_count": len(obligations),
                "rights_count": len(rights),
                "prohibitions_count": len(prohibitions),
            },
            "risk_assessment": {
                "overall_risk": contract_risk,
                "high_risk_clauses": sum(1 for c in clause_results if c["risk_level"] == "High"),
                "medium_risk_clauses": sum(1 for c in clause_results if c["risk_level"] == "Medium"),
                "total_issues": sum(c["issues_count"] for c in clause_results),
            },
            "compliance": {
                "status": compliance["overall_compliance_status"],
                "missing_clauses": compliance["missing_clauses"],
                "law_references": compliance["law_references"],
            },
            "clauses_analyzed": len(clause_results),
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def example_1_simple_analysis():
    """Example: Analyze a contract from file"""
    print("=" * 70)
    print("Example 1: Analyze Contract from File")
    print("=" * 70)

    with open("data/sample_contract_en.txt", "r", encoding="utf-8") as f:
        text = f.read()

    api = ContractAnalysisAPI()
    result = api.analyze_contract_text(text)

    print("\n✓ Analysis Complete:")
    print(f"  Contract Type: {result['metadata']['contract_type']}")
    print(f"  Risk Level: {result['risk_assessment']['overall_risk']}")
    print(f"  Parties: {len(result['entities']['parties'])}")
    print(f"  Clauses: {result['metadata']['total_clauses']}")
    print(f"\nFull Result:")
    print(json.dumps(result, indent=2))


def example_2_hindi_contract():
    """Example: Analyze Hindi contract"""
    print("\n" + "=" * 70)
    print("Example 2: Analyze Hindi Contract")
    print("=" * 70)

    with open("data/sample_contract_hi.txt", "r", encoding="utf-8") as f:
        text = f.read()

    api = ContractAnalysisAPI()
    result = api.analyze_contract_text(text, language="Hindi")

    print(f"\n✓ Hindi Contract Analysis:")
    print(f"  Type: {result['metadata']['contract_type']}")
    print(f"  Risk: {result['risk_assessment']['overall_risk']}")


def example_3_template_matching():
    """Example: Match clauses to template"""
    print("\n" + "=" * 70)
    print("Example 3: Template Matching")
    print("=" * 70)

    from contract_parser.advanced_nlp import ClauseSimilarity

    clause = "Party A shall maintain confidentiality of proprietary information."
    template = TemplateGenerator.get_template("service_agreement")

    similarity = ClauseSimilarity(threshold=0.6)
    all_template_clauses = []
    for section in template["sections"]:
        all_template_clauses.extend(section["clauses"])

    similar = similarity.find_similar_clauses(clause, all_template_clauses)
    print(f"\n✓ Similar Clauses Found: {len(similar)}")
    for match in similar:
        print(f"  Similarity: {match['similarity_score']:.2%}")
        print(f"  Template: {match['template_clause'][:80]}...")


def example_4_export_json():
    """Example: Export analysis as JSON for integration"""
    print("\n" + "=" * 70)
    print("Example 4: Export as JSON")
    print("=" * 70)

    with open("data/sample_contract_en.txt", "r", encoding="utf-8") as f:
        text = f.read()

    api = ContractAnalysisAPI()
    result = api.analyze_contract_text(text)

    # Save as JSON
    with open("contract_analysis_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("\n✓ Analysis exported to: contract_analysis_result.json")
    print(f"  Size: {json.dumps(result).__sizeof__()} bytes")


def example_5_batch_analysis():
    """Example: Analyze multiple contracts"""
    print("\n" + "=" * 70)
    print("Example 5: Batch Analysis")
    print("=" * 70)

    import os
    from pathlib import Path

    api = ContractAnalysisAPI()
    results = {}

    # Analyze all contracts in data/ folder
    data_folder = Path("data")
    for file in data_folder.glob("sample_contract_*.txt"):
        print(f"\nAnalyzing: {file.name}")
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
        
        result = api.analyze_contract_text(text)
        results[file.name] = {
            "type": result["metadata"]["contract_type"],
            "risk": result["risk_assessment"]["overall_risk"],
            "clauses": result["metadata"]["total_clauses"],
        }

    print("\n✓ Batch Analysis Complete:")
    for name, data in results.items():
        print(f"  {name}: {data['type']} | Risk: {data['risk']} | Clauses: {data['clauses']}")


def example_6_custom_analysis_workflow():
    """Example: Custom analysis workflow"""
    print("\n" + "=" * 70)
    print("Example 6: Custom Analysis Workflow")
    print("=" * 70)

    text = """
    SERVICE AGREEMENT
    
    Between: ABC Corporation AND XYZ Services
    
    1. Scope: Provide software development services worth INR 10,00,000
    2. Auto-renewal: Agreement auto-renews unless either party opts out.
    3. Non-compete: Developer shall not work for competitors for 12 months.
    4. IP Rights: All code is assigned to ABC Corporation.
    """

    api = ContractAnalysisAPI()
    result = api.analyze_contract_text(text)

    print(f"\n✓ Quick Analysis:")
    print(f"  Type: {result['metadata']['contract_type']}")
    print(f"  Risk: {result['risk_assessment']['overall_risk']}")

    # Get template suggestions
    print(f"\n✓ Template Suggestions:")
    templates = TemplateGenerator.list_templates()
    print(f"  Available: {', '.join(templates)}")

    # Get alternative clauses
    print(f"\n✓ Improvement Suggestions:")
    alts = [
        "auto_renewal",
        "ip_assignment",
        "non_compete",
    ]
    for alt_type in alts:
        alt = TemplateGenerator.get_alternative_clause(alt_type)
        print(f"\n  {alt_type.upper()}:")
        print(f"    Avoid: {alt['avoid'][:60]}...")
        print(f"    Prefer: {alt['prefer'][:60]}...")


# ============================================================================
# RUN EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("\n" + "█" * 70)
    print("Contract Analysis Bot - Integration Examples")
    print("█" * 70)

    try:
        example_1_simple_analysis()
        example_2_hindi_contract()
        example_3_template_matching()
        example_4_export_json()
        example_5_batch_analysis()
        example_6_custom_analysis_workflow()

        print("\n" + "█" * 70)
        print("✅ All examples completed successfully!")
        print("█" * 70)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
