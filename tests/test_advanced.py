"""
Comprehensive test suite for Contract Analysis & Risk Assessment Bot
"""
import pytest
from contract_parser.advanced_nlp import (
    HindiNormalizer,
    ClauseSimilarity,
    ContractClassifier,
    EntityExtractor,
)
from contract_parser.advanced_risk_assessor import AdvancedRiskAssessor
from contract_parser.compliance_checker import ComplianceChecker
from contract_parser.template_generator import TemplateGenerator


class TestHindiNormalizer:
    """Test Hindi text normalization."""

    def test_normalize_hindi_to_english(self):
        hindi_text = "यह अग्रीमेंट पार्टी A और पार्टी B के बीच है।"
        normalized = HindiNormalizer.normalize(hindi_text)
        assert "Agreement" in normalized
        assert "Party" in normalized


class TestContractClassifier:
    """Test contract type classification."""

    def test_classify_service_agreement(self):
        text = "This service agreement provides deliverables and milestones for client services."
        result = ContractClassifier.classify(text)
        assert result["type"] == "service"
        assert result["confidence"] > 0

    def test_classify_employment(self):
        text = "Employment agreement with salary, benefits, and termination of employment conditions."
        result = ContractClassifier.classify(text)
        assert result["type"] == "employment"


class TestEntityExtractor:
    """Test entity extraction."""

    def test_extract_parties(self):
        text = "BETWEEN ABC Corporation AND XYZ Services Ltd."
        parties = EntityExtractor.extract_parties(text)
        assert len(parties) >= 2
        assert any("ABC" in p for p in parties)

    def test_extract_dates(self):
        text = "This Agreement is dated 1st January 2025."
        dates = EntityExtractor.extract_dates(text)
        assert len(dates) > 0
        assert "2025" in dates[0]

    def test_extract_amounts(self):
        text = "The contract value is INR 5,00,000."
        amounts = EntityExtractor.extract_amounts(text)
        assert len(amounts) > 0
        assert amounts[0]["currency"] == "INR"

    def test_extract_obligations(self):
        text = "Party A shall deliver goods on time. Party B must pay within 30 days."
        obligations = EntityExtractor.extract_obligations(text)
        assert len(obligations) > 0

    def test_extract_rights(self):
        text = "Party A has the right to terminate. Party B may choose the payment method."
        rights = EntityExtractor.extract_rights(text)
        assert len(rights) > 0

    def test_extract_prohibitions(self):
        text = "Party A shall not disclose information. Competitors are not permitted to bid."
        prohibitions = EntityExtractor.extract_prohibitions(text)
        assert len(prohibitions) > 0


class TestClauseSimilarity:
    """Test clause similarity matching."""

    def test_similarity_exact_match(self):
        sim = ClauseSimilarity(threshold=0.9)
        score = sim.similarity_score("Confidential information", "Confidential information")
        assert score == 1.0

    def test_similarity_partial_match(self):
        sim = ClauseSimilarity(threshold=0.5)
        score = sim.similarity_score("Confidential information clause", "Confidential information")
        assert score > 0.7

    def test_find_similar_clauses(self):
        sim = ClauseSimilarity(threshold=0.6)
        clause = "We shall maintain confidentiality of proprietary data."
        templates = [
            "Both parties agree to maintain confidentiality of proprietary information.",
            "The agreement covers sales terms and conditions.",
        ]
        results = sim.find_similar_clauses(clause, templates)
        assert len(results) > 0


class TestAdvancedRiskAssessor:
    """Test advanced risk assessment."""

    def test_score_indemnity_clause_high(self):
        assessor = AdvancedRiskAssessor()
        clause = "Party A shall indemnify and hold harmless Party B from all claims."
        result = assessor.score_clause_detailed(clause)
        assert result["overall_risk"] == "High"

    def test_score_auto_renewal_medium(self):
        assessor = AdvancedRiskAssessor()
        clause = "This agreement shall automatically renew unless either party opts out."
        result = assessor.score_clause_detailed(clause)
        assert result["overall_risk"] in ["Medium", "High"]

    def test_detect_ambiguities(self):
        assessor = AdvancedRiskAssessor()
        clause = "Party A shall use best efforts and provide service as soon as possible."
        ambiguities = assessor.detect_ambiguities(clause)
        assert len(ambiguities) > 0
        assert any("best efforts" in a["phrase"] for a in ambiguities)

    def test_aggregate_risk_high(self):
        assessor = AdvancedRiskAssessor()
        scores = ["High", "High", "Medium", "Low"]
        result = assessor.aggregate_risk(scores)
        assert result == "High"

    def test_aggregate_risk_medium(self):
        assessor = AdvancedRiskAssessor()
        scores = ["Medium", "Medium", "Low"]
        result = assessor.aggregate_risk(scores)
        assert result == "High"


class TestComplianceChecker:
    """Test compliance checking."""

    def test_check_compliance_missing(self):
        text = "Simple agreement without detailed clauses."
        issues = ComplianceChecker.check_compliance(text)
        missing = [i for i in issues if i["status"] == "Missing"]
        assert len(missing) > 0

    def test_check_compliance_present(self):
        text = "This agreement includes arbitration and mediation procedures."
        issues = ComplianceChecker.check_compliance(text)
        present = [i for i in issues if i["status"] == "Present"]
        assert len(present) > 0

    def test_check_indian_law_references(self):
        text = "This agreement complies with the Indian Contract Act."
        refs = ComplianceChecker.check_indian_law_references(text)
        assert "indian contract act" in refs or len(refs) > 0


class TestTemplateGenerator:
    """Test template generation."""

    def test_list_templates(self):
        templates = TemplateGenerator.list_templates()
        assert len(templates) > 0
        assert "service_agreement" in templates

    def test_get_template_service_agreement(self):
        template = TemplateGenerator.get_template("service_agreement")
        assert "sections" in template
        assert "Service Agreement" in template["title"]

    def test_get_alternative_clause_auto_renewal(self):
        alt = TemplateGenerator.get_alternative_clause("auto_renewal")
        assert "avoid" in alt
        assert "prefer" in alt
        assert "reason" in alt

    def test_generate_custom_template(self):
        values = {
            "DESCRIBE SERVICES": "Web development services",
            "AMOUNT": "500000",
            "DURATION": "12 months",
        }
        template = TemplateGenerator.generate_custom_template("service_agreement", values)
        assert "Web development services" in template
        assert "500000" in template
        assert "12 months" in template


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
