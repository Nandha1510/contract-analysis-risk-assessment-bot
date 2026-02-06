# 📖 API Reference Guide

## Contract Analysis Bot - Complete API Documentation

---

## 🎯 Quick Navigation

- [Parsers API](#parsers-api)
- [NLP API](#nlp-api)
- [Advanced NLP API](#advanced-nlp-api)
- [Risk Assessment API](#risk-assessment-api)
- [Compliance API](#compliance-api)
- [Templates API](#templates-api)
- [Audit API](#audit-api)
- [Report Generation API](#report-generation-api)

---

## Parsers API

### `parse_file(uploaded_file) -> str`
**Purpose**: Universal file parser for PDF, DOCX, TXT  
**Module**: `contract_parser.parsers`

**Parameters**:
- `uploaded_file`: Streamlit UploadedFile object or file-like object

**Returns**: Extracted text as string

**Example**:
```python
from contract_parser.parsers import parse_file

with open("contract.pdf", "rb") as f:
    text = parse_file(f)
    print(text)
```

### `parse_pdf(file_stream) -> str`
**Purpose**: Extract text from PDF files  
**Module**: `contract_parser.parsers`

**Returns**: PDF text content

### `parse_docx(file_stream) -> str`
**Purpose**: Extract text from DOCX files  
**Module**: `contract_parser.parsers`

**Returns**: Document text content

### `parse_txt(file_stream) -> str`
**Purpose**: Read and decode text files  
**Module**: `contract_parser.parsers`

**Returns**: File text (auto-detects UTF-8/Latin-1 encoding)

---

## NLP API

### `class ContractNLP`
**Module**: `contract_parser.nlp`

#### `__init__(model_name: str = "en_core_web_sm")`
Initialize spaCy NLP pipeline

#### `process_text(text: str) -> Doc`
Process text through spaCy

**Returns**: spaCy Doc object

**Example**:
```python
from contract_parser.nlp import ContractNLP

nlp = ContractNLP()
doc = nlp.process_text("This is a contract.")
```

#### `extract_clauses(doc: Doc) -> List[str]`
Extract clauses from processed document

**Returns**: List of clause strings (max 200)

#### `extract_entities(doc: Doc) -> List[Dict]`
Extract entities (PERSON, ORG, MONEY, etc.)

**Returns**: List of dicts with `text` and `label`

---

## Advanced NLP API

### `class HindiNormalizer`
**Module**: `contract_parser.advanced_nlp`

#### `normalize(text: str) -> str`
Convert Hindi terms to English equivalents

**Example**:
```python
from contract_parser.advanced_nlp import HindiNormalizer

text = "यह अग्रीमेंट है"
normalized = HindiNormalizer.normalize(text)
# Output: "यह Agreement है"
```

**Supported Hindi Terms**: Agreement, Party, Date, Payment, Term, etc.

---

### `class ContractClassifier`
**Module**: `contract_parser.advanced_nlp`

#### `classify(text: str) -> Dict`
Classify contract type

**Returns**:
```python
{
    "type": "service",  # or employment, vendor, lease, partnership, nda
    "confidence": 0.85
}
```

**Supported Types**:
- employment
- vendor
- lease
- partnership
- service
- nda

**Example**:
```python
from contract_parser.advanced_nlp import ContractClassifier

result = ContractClassifier.classify("Service agreement for development work...")
print(result["type"])  # service
```

---

### `class EntityExtractor`
**Module**: `contract_parser.advanced_nlp`

#### `extract_parties(text: str) -> List[str]`
Extract party names from contract

**Example**:
```python
parties = EntityExtractor.extract_parties(
    "BETWEEN ABC Corp AND XYZ Services"
)
# Returns: ["ABC Corp", "XYZ Services"]
```

#### `extract_dates(text: str) -> List[str]`
Extract dates in multiple formats

**Supported Formats**:
- "1st January 2025"
- "01/01/2025"
- "2025-01-01"

#### `extract_amounts(text: str) -> List[Dict]`
Extract monetary amounts

**Returns**:
```python
[
    {"amount": "500000", "currency": "INR"},
    {"amount": "1000", "currency": "USD"}
]
```

#### `extract_obligations(text: str) -> List[str]`
Extract "shall", "must" clauses (max 50)

#### `extract_rights(text: str) -> List[str]`
Extract "may", "entitled to" clauses (max 50)

#### `extract_prohibitions(text: str) -> List[str]`
Extract "shall not", "cannot" clauses (max 50)

---

### `class ClauseSimilarity`
**Module**: `contract_parser.advanced_nlp`

#### `__init__(threshold: float = 0.7)`
Initialize similarity matcher

#### `similarity_score(text1: str, text2: str) -> float`
Calculate similarity between two texts (0-1)

#### `find_similar_clauses(clause: str, template_clauses: List[str]) -> List[Dict]`
Find similar clauses from templates

**Returns**:
```python
[
    {
        "template_clause": "...",
        "similarity_score": 0.85
    }
]
```

**Example**:
```python
from contract_parser.advanced_nlp import ClauseSimilarity

sim = ClauseSimilarity(threshold=0.7)
results = sim.find_similar_clauses(
    "Party shall maintain confidentiality",
    ["Both parties agree to keep information confidential"]
)
```

---

## Risk Assessment API

### `class RiskAssessor`
**Module**: `contract_parser.risk_assessor`

#### `score_clause(clause: str) -> Tuple[str, List[str]]`
Score a single clause for risk

**Returns**:
```python
("High", ["Indemnity clause found", "IP transfer detected"])
```

#### `aggregate_scores(clause_scores: List[str]) -> str`
Calculate contract-level risk

**Returns**: "High", "Medium", or "Low"

---

### `class AdvancedRiskAssessor`
**Module**: `contract_parser.advanced_risk_assessor`

#### `score_clause_detailed(clause: str) -> Dict`
Detailed clause scoring with reasoning

**Returns**:
```python
{
    "overall_risk": "High",
    "issues_found": 3,
    "detailed_issues": [
        {
            "name": "Broad Indemnity",
            "risk_level": "High",
            "reason": "...",
            "recommendation": "..."
        }
    ]
}
```

**Example**:
```python
from contract_parser.advanced_risk_assessor import AdvancedRiskAssessor

assessor = AdvancedRiskAssessor()
result = assessor.score_clause_detailed(
    "Party A shall indemnify and hold harmless..."
)
```

#### `detect_ambiguities(clause: str) -> List[Dict]`
Find ambiguous language

**Returns**:
```python
[
    {
        "type": "Undefined Standard",
        "phrase": "best efforts",
        "problem": "Not defined; open to interpretation",
        "suggestion": "..."
    }
]
```

#### `aggregate_risk(clause_scores: List[str]) -> str`
Advanced risk aggregation

---

## Compliance API

### `class ComplianceChecker`
**Module**: `contract_parser.compliance_checker`

#### `check_compliance(text: str) -> List[Dict]`
Check for required compliance clauses

**Returns**:
```python
[
    {
        "rule": "Force Majeure Clause",
        "status": "Missing",
        "severity": "Medium",
        "description": "..."
    }
]
```

#### `check_indian_law_references(text: str) -> List[str]`
Check for Indian law references

**Returns**: List of references found

#### `generate_compliance_report(text: str) -> Dict`
Generate full compliance report

**Returns**:
```python
{
    "total_rules_checked": 5,
    "missing_clauses": 2,
    "high_severity_issues": 1,
    "issues": [...],
    "law_references": [...],
    "overall_compliance_status": "At Risk" or "Good"
}
```

**Example**:
```python
from contract_parser.compliance_checker import ComplianceChecker

report = ComplianceChecker.generate_compliance_report(contract_text)
print(report["overall_compliance_status"])
```

---

## Templates API

### `class TemplateGenerator`
**Module**: `contract_parser.template_generator`

#### `list_templates() -> List[str]`
Get all available templates

**Returns**: 
```python
["service_agreement", "employment_agreement", "vendor_agreement"]
```

#### `get_template(template_type: str) -> Dict`
Retrieve a specific template

**Returns**:
```python
{
    "title": "Service Agreement",
    "sections": [
        {
            "heading": "1. Scope of Services",
            "clauses": ["...", "..."]
        }
    ]
}
```

**Example**:
```python
from contract_parser.template_generator import TemplateGenerator

template = TemplateGenerator.get_template("service_agreement")
for section in template["sections"]:
    print(section["heading"])
```

#### `get_alternative_clause(clause_name: str) -> Dict`
Get improvement suggestions for a clause type

**Clause Types**: auto_renewal, ip_assignment, liability_cap, non_compete, confidentiality

**Returns**:
```python
{
    "clause_type": "auto_renewal",
    "avoid": "This agreement shall automatically renew...",
    "prefer": "This agreement expires on [DATE]...",
    "reason": "Avoids accidental lock-in..."
}
```

#### `generate_custom_template(contract_type: str, custom_values: Dict) -> str`
Generate template with custom values

**Example**:
```python
values = {
    "DESCRIBE SERVICES": "Web development",
    "AMOUNT": "500000",
    "DURATION": "12 months"
}
template = TemplateGenerator.generate_custom_template(
    "service_agreement", 
    values
)
```

---

## Audit API

### `class AuditLogger`
**Module**: `utils.audit`

#### `__init__(path: str = "audit_logs.json")`
Initialize audit logger

#### `log_event(event_type: str, payload: dict)`
Log an event

**Example**:
```python
from utils.audit import AuditLogger

audit = AuditLogger()
audit.log_event("contract_uploaded", {
    "filename": "agreement.pdf",
    "size": 15234
})
```

**Event Types**: contract_uploaded, risk_analysis, export_json, export_pdf, etc.

---

## Report Generation API

### `class ReportGenerator`
**Module**: `utils.report_generator`

#### `generate_summary_report(...) -> Dict`
Create structured analysis report

**Parameters**:
- contract_text: str
- entities: List[Dict]
- clauses: List[Dict]
- compliance_issues: List[Dict]
- contract_risk: str
- contract_type: str

**Returns**: Structured report dict

#### `generate_markdown_report(report: Dict) -> str`
Convert to Markdown format

#### `generate_html_report(report: Dict) -> str`
Convert to HTML format

**Example**:
```python
from utils.report_generator import ReportGenerator

report = ReportGenerator.generate_summary_report(...)
md = ReportGenerator.generate_markdown_report(report)
html = ReportGenerator.generate_html_report(report)
```

---

## LLM Client API

### `class LLMClient`
**Module**: `contract_parser.llm_client`

#### `summarize(prompt: str) -> str`
Generate summary (currently simulated)

**Note**: Replace with actual Claude/GPT-4 integration

**Example**:
```python
from contract_parser.llm_client import LLMClient

llm = LLMClient()
summary = llm.summarize("Summarize this contract...")
```

---

## Integration Example

```python
from contract_parser import (
    parse_file,
    ContractNLP,
    AdvancedRiskAssessor,
    ComplianceChecker,
)
from contract_parser.advanced_nlp import (
    ContractClassifier,
    EntityExtractor,
)

# Parse
text = parse_file(contract_file)

# Classify
classifier_result = ContractClassifier.classify(text)

# Extract entities
parties = EntityExtractor.extract_parties(text)
amounts = EntityExtractor.extract_amounts(text)

# Assess risks
nlp = ContractNLP()
doc = nlp.process_text(text)
clauses = nlp.extract_clauses(doc)

assessor = AdvancedRiskAssessor()
clause_risks = []
for clause in clauses:
    risk = assessor.score_clause_detailed(clause)
    clause_risks.append(risk)

# Check compliance
compliance = ComplianceChecker.generate_compliance_report(text)

# Generate report
from utils.report_generator import ReportGenerator
report = ReportGenerator.generate_summary_report(
    text, [], clause_risks, compliance["issues"],
    assessor.aggregate_risk([r["overall_risk"] for r in clause_risks]),
    classifier_result["type"]
)
```

---

## Error Handling

### Common Exceptions

```python
# File parsing
FileNotFoundError  # File doesn't exist
UnicodeDecodeError # Invalid encoding

# NLP
RuntimeError  # spaCy model not found

# Compliance
KeyError  # Invalid rule name

# Templates
KeyError  # Template type not found
```

### Best Practices

```python
try:
    text = parse_file(f)
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Error parsing: {e}")
```

---

## Performance Tips

1. **Batch Processing**: Process multiple contracts sequentially
2. **Caching**: Cache spaCy model between calls
3. **Memory**: Limit clauses extraction to 200 max
4. **Optimization**: Use `advanced_nlp` for better performance

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-02-06 | Initial release |

---

**API Version**: 1.0  
**Status**: Stable  
**Last Updated**: February 6, 2025
