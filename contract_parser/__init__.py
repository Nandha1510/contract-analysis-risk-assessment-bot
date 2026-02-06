"""
Contract Parser Package
Comprehensive contract analysis using NLP, risk assessment, and compliance checking.
"""

from .parsers import parse_file
from .nlp import ContractNLP
from .risk_assessor import RiskAssessor
from .advanced_nlp import (
    HindiNormalizer,
    ClauseSimilarity,
    ContractClassifier,
    EntityExtractor,
)
from .advanced_risk_assessor import AdvancedRiskAssessor
from .compliance_checker import ComplianceChecker
from .template_generator import TemplateGenerator
from .llm_client import LLMClient

__version__ = "1.0"
__author__ = "Contract Analysis Bot Team"

__all__ = [
    "parse_file",
    "ContractNLP",
    "RiskAssessor",
    "HindiNormalizer",
    "ClauseSimilarity",
    "ContractClassifier",
    "EntityExtractor",
    "AdvancedRiskAssessor",
    "ComplianceChecker",
    "TemplateGenerator",
    "LLMClient",
]
