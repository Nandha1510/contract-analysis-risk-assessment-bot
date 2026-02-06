from typing import Dict, List
import json


class TemplateGenerator:
    """Generate SME-friendly contract templates and alternative clauses."""

    TEMPLATES = {
        "service_agreement": {
            "title": "Service Agreement",
            "sections": [
                {
                    "heading": "1. Scope of Services",
                    "clauses": [
                        "Service Provider agrees to provide the following services: [DESCRIBE SERVICES]",
                        "Deliverables shall be provided on the following timeline: [TIMELINE]",
                        "Acceptance criteria: [SPECIFY CRITERIA]",
                    ],
                },
                {
                    "heading": "2. Payment Terms",
                    "clauses": [
                        "Total fee: INR [AMOUNT]",
                        "Payment schedule: [NET 30 / MILESTONE-BASED / MONTHLY]",
                        "Invoices to be issued on [DATE]",
                        "Late payments attract 1.5% monthly interest (capped at 18% p.a.)",
                    ],
                },
                {
                    "heading": "3. Term & Termination",
                    "clauses": [
                        "Initial term: [DURATION] from the Effective Date",
                        "Either party may terminate with 30 days written notice",
                        "Termination for cause upon [SPECIFY CAUSE]",
                    ],
                },
                {
                    "heading": "4. Intellectual Property",
                    "clauses": [
                        "IP created by Service Provider shall remain their property",
                        "Client receives a non-exclusive license to use deliverables",
                        "Confidential information shall be returned upon termination",
                    ],
                },
                {
                    "heading": "5. Limitation of Liability",
                    "clauses": [
                        "Total liability capped at fees paid in the 12-month period",
                        "Neither party liable for indirect, consequential, or punitive damages",
                    ],
                },
            ],
        },
        "employment_agreement": {
            "title": "Employment Agreement",
            "sections": [
                {
                    "heading": "1. Position & Compensation",
                    "clauses": [
                        "Job title: [TITLE]",
                        "Monthly salary: INR [AMOUNT]",
                        "Benefits: [SPECIFY: Health Insurance, PF, etc.]",
                    ],
                },
                {
                    "heading": "2. Term & Termination",
                    "clauses": [
                        "Probation period: [3-6 MONTHS]",
                        "Either party may terminate with [30/60/90] days notice",
                        "Severance: [SPECIFY ENTITLEMENT]",
                    ],
                },
                {
                    "heading": "3. Confidentiality & Non-Compete",
                    "clauses": [
                        "Employee shall maintain confidentiality during and after employment",
                        "Non-compete period: [6/12 MONTHS] post-termination (limited to relevant industry)",
                    ],
                },
                {
                    "heading": "4. Intellectual Property",
                    "clauses": [
                        "IP created during employment belongs to the employer",
                        "Works created on personal time remain employee's property",
                    ],
                },
            ],
        },
        "vendor_agreement": {
            "title": "Vendor/Supplier Agreement",
            "sections": [
                {
                    "heading": "1. Goods/Services Description",
                    "clauses": [
                        "Vendor shall supply: [PRODUCT/SERVICE]",
                        "Quality standards: [SPECIFY]",
                        "Delivery schedule: [SPECIFY]",
                    ],
                },
                {
                    "heading": "2. Payment & Pricing",
                    "clauses": [
                        "Unit price: INR [AMOUNT]",
                        "Payment terms: NET [30/45/60]",
                        "Volume discounts: [IF APPLICABLE]",
                    ],
                },
                {
                    "heading": "3. Warranty & Liability",
                    "clauses": [
                        "Vendor warrants goods are free from defects",
                        "Warranty period: [12 MONTHS]",
                        "Vendor liable for non-conforming goods",
                    ],
                },
                {
                    "heading": "4. Termination",
                    "clauses": [
                        "Either party may terminate with [30/60] days notice",
                        "Immediate termination for material breach",
                    ],
                },
            ],
        },
    }

    ALTERNATIVE_CLAUSES = {
        "auto_renewal": [
            "AVOID: 'This Agreement shall automatically renew unless either party opts out.'",
            "PREFER: 'This Agreement expires on [DATE]. Renewal requires written consent from both parties.'",
            "REASON: Avoids accidental lock-in and ensures active consent.",
        ],
        "ip_assignment": [
            "AVOID: 'All IP created under this Agreement is assigned to the Company.'",
            "PREFER: 'IP created specifically for Client deliverables is assigned to Client. IP created by Vendor remains their property.'",
            "REASON: Balances ownership and prevents over-broad assignments.",
        ],
        "liability_cap": [
            "AVOID: 'No liability cap.'",
            "PREFER: 'Each party's total liability capped at fees paid in the preceding 12 months.'",
            "REASON: Protects both parties and is standard in contracts.",
        ],
        "non_compete": [
            "AVOID: 'Employee shall not work for competing firms indefinitely.'",
            "PREFER: 'Employee shall not work for direct competitors for 6 months post-termination within India.'",
            "REASON: Reasonable restriction is more enforceable under Indian law.",
        ],
        "confidentiality": [
            "GOOD: 'Confidential information excludes: (a) publicly known data, (b) independently developed, (c) legally required disclosure.'",
            "REASON: Standard carve-outs make NDA reasonable and enforceable.",
        ],
    }

    @classmethod
    def get_template(cls, template_type: str) -> Dict:
        """Retrieve a template by type."""
        if template_type in cls.TEMPLATES:
            return cls.TEMPLATES[template_type]
        return {"error": f"Template '{template_type}' not found."}

    @classmethod
    def list_templates(cls) -> List[str]:
        """List all available templates."""
        return list(cls.TEMPLATES.keys())

    @classmethod
    def get_alternative_clause(cls, clause_name: str) -> Dict:
        """Get alternative/improved clause suggestion."""
        if clause_name in cls.ALTERNATIVE_CLAUSES:
            alt = cls.ALTERNATIVE_CLAUSES[clause_name]
            return {
                "clause_type": clause_name,
                "avoid": alt[0],
                "prefer": alt[1],
                "reason": alt[2],
            }
        return {"error": f"Alternative clause '{clause_name}' not found."}

    @classmethod
    def generate_custom_template(cls, contract_type: str, custom_values: Dict) -> str:
        """Generate a custom template with filled values."""
        template = cls.get_template(contract_type)
        if "error" in template:
            return json.dumps(template)

        markdown = f"# {template['title']}\n\n"
        for section in template['sections']:
            markdown += f"## {section['heading']}\n\n"
            for clause in section['clauses']:
                # Replace placeholders
                for key, value in custom_values.items():
                    clause = clause.replace(f"[{key}]", str(value))
                markdown += f"- {clause}\n"
            markdown += "\n"
        return markdown
