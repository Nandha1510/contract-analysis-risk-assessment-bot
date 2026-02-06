import streamlit as st
import pandas as pd
from contract_parser.parsers import parse_file
from contract_parser.nlp import ContractNLP
from contract_parser.risk_assessor import RiskAssessor
from contract_parser.llm_client import LLMClient
from contract_parser.advanced_nlp import (
    HindiNormalizer,
    ClauseSimilarity,
    ContractClassifier,
    EntityExtractor,
)
from contract_parser.advanced_risk_assessor import AdvancedRiskAssessor
from contract_parser.compliance_checker import ComplianceChecker
from contract_parser.template_generator import TemplateGenerator
from contract_parser.clause_classifier import ClauseClassifier
from contract_parser.knowledge_base import ContractKnowledgeBase
from contract_parser.batch_processor import BatchProcessor
from utils.audit import AuditLogger
from utils.report_generator import ReportGenerator
from utils.localization import get_text
import json
import io
import os
from datetime import datetime


st.set_page_config(
    page_title="Contract Analysis & Risk Assessment Bot",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    .main-header { font-size: 2.5em; color: #1f77b4; font-weight: bold; }
    .risk-high { color: #d62728; font-weight: bold; }
    .risk-medium { color: #ff7f0e; font-weight: bold; }
    .risk-low { color: #2ca02c; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='main-header'>⚖️ Contract Analysis & Risk Assessment Bot</h1>", unsafe_allow_html=True)
st.markdown("**Analyze contracts, identify risks, and receive actionable legal insights for SMEs**")

# Initialize session state
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "contract_text" not in st.session_state:
    st.session_state.contract_text = ""
if "custom_template" not in st.session_state:
    st.session_state.custom_template = None
if "custom_template_type" not in st.session_state:
    st.session_state.custom_template_type = ""
if "language" not in st.session_state:
    st.session_state.language = "English"

# Initialize modules
nlp = ContractNLP()
assessor = RiskAssessor()
advanced_assessor = AdvancedRiskAssessor()
llm = LLMClient()
compliance_checker = ComplianceChecker()
template_gen = TemplateGenerator()
entity_extractor = EntityExtractor()
clause_similarity = ClauseSimilarity()
audit = AuditLogger("audit_logs.json")
report_gen = ReportGenerator()

# Sidebar
with st.sidebar:
    st.header("📋 Navigation")
    
    # Language selector at top
    lang_choice = st.selectbox("Language / भाषा", ["English", "Hindi"])
    st.session_state.language = lang_choice
    
    # Get translated text
    t = lambda key: get_text(lang_choice, key)
    
    page = st.radio(
        "Select View:",
        [
            t("nav_upload"),
            t("nav_templates"),
            t("nav_kb"),
            t("nav_batch"),
            t("nav_audit"),
            t("nav_help"),
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.subheader(t("settings"))
    risk_threshold = st.slider(t("risk_threshold"), 0.0, 1.0, 0.7)
    
    # Include language selector
    st.caption("Language already selected above ⬆")


    

# Main Content
t = lambda key: get_text(st.session_state.language, key)

if page == t("nav_upload"):
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(t("upload_header"))
        uploaded = st.file_uploader(
            t("upload_label"),
            type=["pdf", "docx", "txt"],
            label_visibility="collapsed"
        )

    if uploaded:
        with st.spinner(t("parsing")):
            raw_text = parse_file(uploaded)
            st.session_state.contract_text = raw_text
            st.session_state.uploaded_file = uploaded.name
            audit.log_contract_upload(uploaded.name, len(raw_text), "")

        # Normalize if Hindi
        if st.session_state.language == "Hindi":
            raw_text = HindiNormalizer.normalize(raw_text)

        # Tab Interface
        tab1, tab2, tab3, tab4, tab4b, tab5, tab6 = st.tabs(
            [
                t("tab_overview"),
                t("tab_risk"),
                t("tab_compliance"),
                t("tab_clauses"),
                t("tab_classification"),
                t("tab_templates"),
                t("tab_export"),
            ]
        )

        with tab1:
            st.subheader(t("overview_header"))
            
            # Contract Classification
            classifier_result = ContractClassifier.classify(raw_text)
            col1, col2, col3 = st.columns(3)
            col1.metric(t("contract_type"), classifier_result.get("type", "Unknown"))
            col2.metric(t("confidence"), f"{classifier_result.get('confidence', 0):.1%}")
            col3.metric(t("doc_length"), f"{len(raw_text)} chars")

            # Extract Entities
            with st.spinner(t("extracting_entities")):
                parties = entity_extractor.extract_parties(raw_text)
                dates = entity_extractor.extract_dates(raw_text)
                amounts = entity_extractor.extract_amounts(raw_text)

            st.markdown(f"### {t('parties')}")
            if parties:
                for party in parties[:5]:
                    st.write(f"- {party}")
            else:
                st.write(t("no_parties"))

            st.markdown(f"### {t('dates')}")
            if dates:
                for date in dates[:5]:
                    st.write(f"- {date}")
            else:
                st.write(t("no_dates"))

            st.markdown(f"### {t('amounts')}")
            if amounts:
                df_amounts = pd.DataFrame(amounts[:10])
                st.dataframe(df_amounts, use_container_width=True)
            else:
                st.write(t("no_amounts"))

        with tab2:
            st.subheader(t("risk_assessment"))
            
            with st.spinner(t("analyzing_risks")):
                doc = nlp.process_text(raw_text)
                clauses = nlp.extract_clauses(doc)

            clause_results = []
            for i, clause in enumerate(clauses):
                detailed_score = advanced_assessor.score_clause_detailed(clause)
                ambiguities = advanced_assessor.detect_ambiguities(clause)
                clause_results.append({
                    "id": i,
                    "text": clause[:100] + "...",
                    "full_text": clause,
                    "risk": detailed_score["overall_risk"],
                    "issues": detailed_score["detailed_issues"],
                    "ambiguities": ambiguities,
                })

            # Risk Summary
            high_risk_count = sum(1 for c in clause_results if c["risk"] == "High")
            medium_risk_count = sum(1 for c in clause_results if c["risk"] == "Medium")
            low_risk_count = sum(1 for c in clause_results if c["risk"] == "Low")

            col1, col2, col3 = st.columns(3)
            col1.metric(t("high_risk"), high_risk_count, delta=-1 if high_risk_count == 0 else None)
            col2.metric(t("medium_risk"), medium_risk_count)
            col3.metric(t("low_risk"), low_risk_count)

            contract_risk = advanced_assessor.aggregate_risk([c["risk"] for c in clause_results])
            st.markdown(f"### {t('overall_risk')}: <span class='risk-{contract_risk.lower()}'>{contract_risk}</span>", unsafe_allow_html=True)

            # High Risk Clauses
            st.markdown(f"### {t('high_risk_clauses')}")
            high_risk_clauses = [c for c in clause_results if c["risk"] == "High"]
            for clause_data in high_risk_clauses[:10]:
                with st.expander(f"🔴 {clause_data['text']}", expanded=False):
                    st.write(f"**{t('full_text')}:** {clause_data['full_text']}")
                    st.write(f"**{t('issues')}:**")
                    for issue in clause_data["issues"]:
                        st.write(f"- **{issue['name']}** - {issue['reason']}")
                        st.write(f"  **{t('recommendation')}:** {issue['recommendation']}")
                    
                    if clause_data["ambiguities"]:
                        st.write(f"**{t('ambiguities')}:**")
                        for amb in clause_data["ambiguities"]:
                            st.write(f"- {amb['type']}: {amb['problem']}")
                            st.write(f"  **{t('recommendation')}:** {amb['suggestion']}")

            audit.log_event("risk_analysis", {"high_risk": high_risk_count, "medium_risk": medium_risk_count, "contract_type": classifier_result.get("type")})

        with tab3:
            st.subheader(t("compliance_checklist"))
            
            with st.spinner(t("running_compliance_checks")):
                compliance_report = compliance_checker.generate_compliance_report(raw_text)

            st.metric(t("compliance_status"), compliance_report["overall_compliance_status"])
            st.metric(t("missing_clauses"), compliance_report["missing_clauses"])

            st.markdown(f"### {t('compliance_issues')}")
            df_compliance = pd.DataFrame(compliance_report["issues"])
            st.dataframe(df_compliance, use_container_width=True)

            st.markdown(f"### {t('india_compliance')}")
            india_issues = compliance_report.get("india_specific_issues", [])
            if india_issues:
                df_india = pd.DataFrame(india_issues)
                st.dataframe(df_india, use_container_width=True)

            st.markdown(f"### {t('law_references')}")
            for ref in compliance_report.get("law_references", []):
                st.write(f"- {ref}")

            audit.log_event("compliance_check", {
                "overall_status": compliance_report["overall_compliance_status"],
                "missing_clauses": compliance_report["missing_clauses"]
            })

        with tab4:
            st.subheader(t("clause_analysis"))
            
            clause_filter = st.selectbox(t("filter_risk"), [t("all"), "High", "Medium", "Low"])
            filtered_clauses = clause_results if clause_filter == t("all") else [c for c in clause_results if c["risk"] == clause_filter]

            st.write(f"{t('showing')} {len(filtered_clauses)} {t('clauses')}")
            for clause_data in filtered_clauses[:30]:
                risk_color = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}.get(clause_data["risk"], "")
                with st.expander(f"{risk_color} Clause {clause_data['id']}: {clause_data['text']}"):
                    st.write(clause_data["full_text"])
                    if clause_data["issues"]:
                        st.write(f"**{t('issues_found')}:**")
                        for issue in clause_data["issues"]:
                            st.write(f"- {issue['name']}: {issue['reason']}")

        with tab4b:
            st.subheader(t("clause_classification"))
            
            with st.spinner(t("classifying")):
                classified = ClauseClassifier.classify_clauses_batch(
                    [c["full_text"] for c in clause_results[:50]]
                )
            
            # Summary
            category_summary = ClauseClassifier.get_category_summary(classified)
            st.metric(t("total_classified"), category_summary["total_clauses"])
            
            st.write(f"### {t('clause_distribution')}")
            if category_summary.get("categories_found"):
                df_categories = pd.DataFrame([
                    {"Category": k, "Count": v} 
                    for k, v in category_summary["categories_found"].items()
                ])
                st.bar_chart(df_categories.set_index("Category"))
            
            st.write(f"### {t('detailed_classifications')}")
            for clause_class in classified[:20]:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{clause_class['category'].title()}**")
                    st.caption(clause_class.get('description', 'General clause'))
                with col2:
                    st.metric(t("confidence"), f"{clause_class.get('confidence', 0):.0%}")


        with tab5:
            st.subheader(t("templates_page_title"))
            
            template_type = st.selectbox(t("select_template_type"), template_gen.list_templates())
            
            if st.button(t("view_template")):
                template = template_gen.get_template(template_type)
                st.markdown(f"### {template['title']}")
                for section in template['sections']:
                    st.markdown(f"#### {section['heading']}")
                    for clause in section['clauses']:
                        st.write(f"- {clause}")

            st.markdown("---")
            st.subheader(t("suggested_improvements"))
            
            suggestions = [
                "auto_renewal",
                "ip_assignment",
                "liability_cap",
                "non_compete",
                "confidentiality",
            ]
            
            selected_suggestion = st.selectbox(t("select_clause_type"), suggestions)
            if st.button(t("get_alternative")):
                alt = template_gen.get_alternative_clause(selected_suggestion)
                if "error" not in alt:
                    st.write(f"**{t('avoid')}:** {alt['avoid']}")
                    st.write(f"**{t('prefer')}:** {alt['prefer']}")
                    st.write(f"**{t('reason')}:** {alt['reason']}")

        with tab6:
            st.subheader(t("export_header"))
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button(t("json_report_button")):
                    report = report_gen.generate_summary_report(
                        raw_text,
                        [],
                        clause_results,
                        compliance_report["issues"],
                        contract_risk,
                        classifier_result.get("type", "Unknown"),
                    )
                    
                    st.write(f"### {t('report_summary')}")
                    st.json(report["summary"])
                    
                    audit.log_event("report_generated", {"format": "JSON"})
                    
                    # Download
                    json_str = json.dumps(report, indent=2)
                    st.download_button(
                        t("download_json"),
                        json_str,
                        file_name=f"contract_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                    )

            with col2:
                if st.button(t("markdown_report_button")):
                    report = report_gen.generate_summary_report(
                        raw_text,
                        [],
                        clause_results,
                        compliance_report["issues"],
                        contract_risk,
                        classifier_result.get("type", "Unknown"),
                    )
                    md_report = report_gen.generate_markdown_report(report)
                    audit.log_event("report_generated", {"format": "Markdown"})
                    st.download_button(
                        t("download_md"),
                        md_report,
                        file_name=f"contract_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown",
                    )

            with col3:
                if st.button(t("html_report_button")):
                    report = report_gen.generate_summary_report(
                        raw_text,
                        [],
                        clause_results,
                        compliance_report["issues"],
                        contract_risk,
                        classifier_result.get("type", "Unknown"),
                    )
                    html_report = report_gen.generate_html_report(report)
                    audit.log_event("report_generated", {"format": "HTML"})
                    st.download_button(
                        t("download_html"),
                        html_report,
                        file_name=f"contract_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html",
                    )

            with col4:
                if st.button(t("pdf_report_button")):
                    with st.spinner(t("generating_pdf")):
                        report = report_gen.generate_summary_report(
                            raw_text,
                            [],
                            clause_results,
                            compliance_report["issues"],
                            contract_risk,
                            classifier_result.get("type", "Unknown"),
                        )
                        pdf_bytes = report_gen.generate_pdf_report(report)
                        audit.log_event("report_generated", {"format": "PDF"})
                        st.download_button(
                            "📥 Download PDF",
                            pdf_bytes,
                            file_name=f"contract_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                        )
                        st.success("✅ PDF generated successfully!")

elif page == t("nav_templates"):
    st.subheader(t("templates_header"))
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        template_type = st.selectbox(t("select_template"), template_gen.list_templates())
        
        if st.button(t("view_full_template")):
            template = template_gen.get_template(template_type)
            with col2:
                st.markdown(f"### {template['title']}")
                for section in template['sections']:
                    st.markdown(f"#### {section['heading']}")
                    for clause in section['clauses']:
                        st.write(f"- {clause}")

    st.markdown("---")
    st.subheader(t("custom_template"))
    
    with st.form("custom_template_form"):
        ctype = st.selectbox(t("select_template_type"), template_gen.list_templates(), key="form_template")
        custom_values = {}
        
        st.write(t("fill_placeholders"))
        custom_values["DESCRIBE SERVICES"] = st.text_input(t("services_desc"))
        custom_values["AMOUNT"] = st.number_input(t("amount_inr"), min_value=0)
        custom_values["DURATION"] = st.text_input(t("duration"))
        
        if st.form_submit_button(t("generate")):
            st.session_state.custom_template = template_gen.generate_custom_template(ctype, custom_values)
            st.session_state.custom_template_type = ctype
    
    # Display generated template and download button outside form
    if hasattr(st.session_state, 'custom_template'):
        st.text_area("Generated Template", st.session_state.custom_template, height=400)
        st.download_button(
            t("download_template"),
            st.session_state.custom_template,
            file_name=f"{st.session_state.custom_template_type}_template.md",
            mime="text/markdown",
        )

elif page == t("nav_audit"):
    st.subheader(t("audit_header"))
    
    try:
        with open("audit_logs.json", "r", encoding="utf-8") as f:
            logs = json.load(f)
        
        st.write(f"{t('total_events')}: {len(logs)}")
        
        # Display recent logs
        if logs:
            df_logs = pd.DataFrame(logs)
            st.dataframe(df_logs.tail(20), use_container_width=True)
            
            if st.button(t("download_logs")):
                st.download_button(
                    t("download_logs"),
                    json.dumps(logs, indent=2),
                    file_name="audit_logs.json",
                    mime="application/json",
                )
    except FileNotFoundError:
        st.write(t("no_logs"))

elif page == t("nav_kb"):
    st.subheader(t("kb_header"))
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.info(t("kb_stats"))
        kb_stats = ContractKnowledgeBase.get_knowledge_base_stats()
        st.metric(t("total_issues"), kb_stats["total_known_issues"])
        st.metric(t("high_impact"), kb_stats["high_impact"])
        st.metric(t("sme_focused"), "✓ India")
    
    with col2:
        st.info(t("high_impact_list"))
        high_impact = ContractKnowledgeBase.get_high_impact_issues()
        for issue in high_impact:
            st.write(f"**{issue['title']}** - {issue['frequency']}")
            st.caption(f"India: {issue['frequency_india']}")
    
    st.markdown("---")
    
    st.subheader(t("browse_issues"))
    selected_issue = st.selectbox(
        t("select_issue"),
        [f"{k}: {v['title']}" for k, v in ContractKnowledgeBase.COMMON_ISSUES.items()]
    )
    
    if selected_issue:
        issue_key = selected_issue.split(":")[0]
        issue_data = ContractKnowledgeBase.get_issue_by_name(issue_key)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.write(f"**{t('title')}**: {issue_data['title']}")
            st.write(f"**{t('frequency')}**: {issue_data['frequency']}")
            st.write(f"**{t('impact')}**: {issue_data['impact']}")
            
        with col2:
            st.write(f"**{t('india_sme_context')}**: {issue_data['frequency_india']}")
        
        st.write(f"**{t('description')}**: {issue_data['description']}")
        st.write(f"**{t('example')}**: {issue_data['example']}")
        st.write(f"**{t('risk')}**: {issue_data['risk']}")
        st.write(f"**{t('solution')}**: {issue_data['solution']}")
        st.write(f"**{t('sample_fix')}**: `{issue_data['sample_fix']}`")

elif page == t("nav_batch"):
    st.subheader(t("batch_header"))
    
    st.info(t("batch_info"))
    
    st.write(f"### {t('step1')}")
    st.write(t("step1_info"))
    
    st.write(f"### {t('step2')}")
    folder_path = st.text_input(t("folder_path"), "")
    
    if st.button(t("process_batch")):
        if folder_path and os.path.exists(folder_path):
            with st.spinner(t("processing")):
                import os
                files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) 
                        if f.endswith(('.pdf', '.docx', '.txt'))]
                
                if files:
                    processor = BatchProcessor()
                    batch_results = processor.process_batch(files)
                    
                    st.success(f"{t('processed_count')} {batch_results['processed_count']} {t('contracts')}")
                    
                    # Display summary
                    st.write(f"### {t('batch_summary')}")
                    col1, col2, col3 = st.columns(3)
                    col1.metric(t("total_processed"), batch_results['processed_count'])
                    col2.metric(t("failed"), batch_results['failed_count'])
                    col3.metric(t("high_risk"), batch_results['summary'].get('high_risk_contracts', 0))
                    
                    # Detailed results
                    st.write(f"### {t('contract_details')}")
                    df_results = pd.DataFrame(batch_results['contracts'])
                    st.dataframe(df_results, use_container_width=True)
                    
                    # Download results
                    st.download_button(
                        t("download_batch"),
                        json.dumps(batch_results, indent=2),
                        file_name=f"batch_report_{batch_results['batch_id']}.json",
                        mime="application/json"
                    )
                else:
                    st.error(t("no_files"))
        else:
            st.warning(t("enter_path"))
            
            st.write(f"### {t('demo_mode')}")
            st.info(t("production_demo"))

elif page == t("nav_help"):
    st.subheader(t("help_header"))
    
    st.markdown(f"""
    ### {t("how_to_use")}
    
    1. **Upload a Contract**: Click "{t('nav_upload')}" and select a PDF, DOCX, or TXT file.
    2. **Review Overview**: See contract type, parties, dates, and amounts.
    3. **Analyze Risks**: Check high-risk clauses and their implications.
    4. **Check Compliance**: Verify if required clauses are present.
    5. **Review Clauses**: Go clause-by-clause for detailed analysis.
    6. **Get Templates**: Use SME templates for creating new contracts.
    7. **Export Reports**: Download analysis in JSON, Markdown, HTML, or PDF.
    8. **Knowledge Base**: Browse 10+ common contract issues faced by Indian SMEs.
    9. **Batch Processing**: Analyze multiple contracts at once.
    
    ### {t("supported_features")}
    - ✓ PDF, DOCX, TXT parsing
    - ✓ Hindi/English contracts
    - ✓ Clause extraction & automatic classification
    - ✓ Compliance checking (Indian laws + 8 India-specific checks)
    - ✓ Entity extraction (6 types: parties, dates, amounts, jurisdiction, payment terms, key dates)
    - ✓ Template generation
    - ✓ Multi-format export (JSON, MD, HTML, PDF)
    - ✓ Batch processing (multiple contracts)
    - ✓ Knowledge base (10 SME issues)
    - ✓ Audit logging with compliance summary
    - ✓ AI-powered (Gemini API) explanations and suggestions
    - ✓ Bilingual UI (English & Hindi)
    
    ### {t("risk_levels")}
    - 🔴 **High**: Requires immediate review; likely unfavorable or risky.
    - 🟠 **Medium**: Review needed; clarify or modify if needed.
    - 🟢 **Low**: Generally acceptable; standard terms.
    
    ### {t("tips")}
    - Always review High-risk clauses before signing.
    - Use templates to standardize your own contracts.
    - Check Knowledge Base for common issues in your contract type.
    - Keep records of all contract analyses for compliance.
    - Consult a lawyer for complex or high-value contracts.
    
    ### {t("gemini_setup")}
    To enable AI-powered features:
    1. Get free API key from: https://aistudio.google.com/app/apikey
    2. Create `.env` file in project root
    3. Add: `GEMINI_API_KEY=your_key_here`
    4. Restart the app
    """)



st.markdown("---")
st.caption(t("footer"))
