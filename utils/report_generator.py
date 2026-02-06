from typing import Dict, List
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime


class ReportGenerator:
    """Generate comprehensive reports in multiple formats."""

    @staticmethod
    def generate_summary_report(
        contract_text: str,
        entities: List[Dict],
        clauses: List[Dict],
        compliance_issues: List[Dict],
        contract_risk: str,
        contract_type: str,
    ) -> Dict:
        """Generate a comprehensive summary report."""
        return {
            "summary": {
                "contract_type": contract_type,
                "total_length_chars": len(contract_text),
                "total_clauses": len(clauses),
                "parties_count": len([e for e in entities if e.get("label") == "PERSON"]),
                "overall_risk_level": contract_risk,
                "compliance_issues_count": sum(1 for issue in compliance_issues if issue["status"] == "Missing"),
            },
            "entities": entities,
            "risk_analysis": {
                "high_risk_clauses": [c for c in clauses if c.get("risk") == "High"],
                "medium_risk_clauses": [c for c in clauses if c.get("risk") == "Medium"],
                "total_issues": sum(len(c.get("issues", [])) for c in clauses),
            },
            "compliance": compliance_issues,
            "recommendations": [
                "Review all High-risk clauses before execution.",
                "Ensure auto-renewal and termination clauses are mutual.",
                "Verify IP assignment scope does not cover unintended assets.",
                "Confirm liability caps are reasonable and fair.",
            ],
        }

    @staticmethod
    def generate_markdown_report(report: Dict) -> str:
        """Convert report to Markdown format."""
        md = "# Contract Analysis Report\n\n"

        summary = report.get("summary", {})
        md += "## Executive Summary\n\n"
        md += f"- **Contract Type**: {summary.get('contract_type', 'Unknown')}\n"
        md += f"- **Overall Risk Level**: **{summary.get('overall_risk_level', 'Low')}**\n"
        md += f"- **Total Clauses Analyzed**: {summary.get('total_clauses', 0)}\n"
        md += f"- **Compliance Issues**: {summary.get('compliance_issues_count', 0)}\n\n"

        risk_analysis = report.get("risk_analysis", {})
        md += "## Risk Analysis\n\n"
        md += f"- **High-Risk Clauses**: {len(risk_analysis.get('high_risk_clauses', []))}\n"
        md += f"- **Medium-Risk Clauses**: {len(risk_analysis.get('medium_risk_clauses', []))}\n"
        md += f"- **Total Issues Found**: {risk_analysis.get('total_issues', 0)}\n\n"

        compliance = report.get("compliance", [])
        md += "## Compliance Checklist\n\n"
        for issue in compliance:
            status_icon = "✓" if issue.get("status") == "Present" else "✗"
            md += f"{status_icon} **{issue.get('rule', 'Unknown')}** ({issue.get('severity', 'Medium')})\n"
            md += f"  - {issue.get('description', '')}\n\n"

        recommendations = report.get("recommendations", [])
        md += "## Recommendations\n\n"
        for i, rec in enumerate(recommendations, 1):
            md += f"{i}. {rec}\n"

        return md

    @staticmethod
    def generate_html_report(report: Dict) -> str:
        """Convert report to HTML format."""
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Contract Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
        h1, h2 { color: #2c3e50; }
        .high-risk { color: #e74c3c; font-weight: bold; }
        .medium-risk { color: #f39c12; font-weight: bold; }
        .low-risk { color: #27ae60; font-weight: bold; }
        table { border-collapse: collapse; width: 100%; margin-top: 10px; }
        th, td { border: 1px solid #bdc3c7; padding: 10px; text-align: left; }
        th { background-color: #ecf0f1; }
        .section { margin-top: 30px; padding: 15px; border-left: 4px solid #3498db; }
    </style>
</head>
<body>
    <h1>Contract Analysis Report</h1>
"""

        summary = report.get("summary", {})
        html += "<div class='section'><h2>Executive Summary</h2>"
        html += f"<p><strong>Contract Type</strong>: {summary.get('contract_type', 'Unknown')}</p>"
        html += f"<p><strong>Overall Risk Level</strong>: <span class='{summary.get('overall_risk_level', 'Low').lower()}-risk'>{summary.get('overall_risk_level', 'Low')}</span></p>"
        html += f"<p><strong>Total Clauses</strong>: {summary.get('total_clauses', 0)}</p>"
        html += f"<p><strong>Compliance Issues</strong>: {summary.get('compliance_issues_count', 0)}</p>"
        html += "</div>"

        compliance = report.get("compliance", [])
        html += "<div class='section'><h2>Compliance Checklist</h2><table>"
        html += "<tr><th>Rule</th><th>Status</th><th>Severity</th><th>Description</th></tr>"
        for issue in compliance:
            status = "✓ Present" if issue.get("status") == "Present" else "✗ Missing"
            html += f"<tr><td>{issue.get('rule', '')}</td><td>{status}</td><td>{issue.get('severity', '')}</td><td>{issue.get('description', '')}</td></tr>"
        html += "</table></div>"

        html += """
    </body>
</html>
"""
        return html

    @staticmethod
    def generate_pdf_report(report: Dict, filename: str = None) -> bytes:
        """Generate PDF report using ReportLab."""
        
        if filename is None:
            filename = f"contract_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2ca02c'),
            spaceAfter=12,
            spaceBefore=12
        )

        # Title
        story.append(Paragraph("Contract Analysis Report", title_style))
        story.append(Spacer(1, 0.2*inch))

        # Summary
        summary = report.get("summary", {})
        story.append(Paragraph("Executive Summary", heading_style))
        
        summary_data = [
            ["Metric", "Value"],
            ["Contract Type", str(summary.get('contract_type', 'Unknown'))],
            ["Overall Risk Level", str(summary.get('overall_risk_level', 'Low'))],
            ["Total Clauses", str(summary.get('total_clauses', 0))],
            ["Compliance Issues", str(summary.get('compliance_issues_count', 0))],
        ]
        
        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.2*inch))

        # Compliance section
        compliance = report.get("compliance", [])
        story.append(Paragraph("Compliance Checklist", heading_style))
        
        comp_data = [["Rule", "Status", "Severity"]]
        for issue in compliance[:10]:  # Limit to 10 to fit on page
            status = "Present" if issue.get("status") == "Present" else "Missing"
            comp_data.append([
                str(issue.get('rule', '')),
                status,
                str(issue.get('severity', ''))
            ])
        
        comp_table = Table(comp_data)
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(comp_table)
        story.append(Spacer(1, 0.2*inch))

        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

