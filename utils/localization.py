"""Language localization and translations for UI."""

TRANSLATIONS = {
    "english": {
        # Headers and Navigation
        "title": "⚖️ Contract Analysis & Risk Assessment Bot",
        "subtitle": "Analyze contracts, identify risks, and receive actionable legal insights for SMEs",
        "nav_upload": "Upload & Analyze",
        "nav_templates": "Templates",
        "nav_kb": "Knowledge Base",
        "nav_batch": "Batch Processing",
        "nav_audit": "Audit Logs",
        "nav_help": "Help",
        
        # Upload Section
        "upload_header": "📤 Upload Contract",
        "upload_label": "Select a contract file",
        "parsing": "🔄 Parsing contract...",
        
        # Tabs
        "tab_overview": "📊 Overview",
        "tab_risk": "⚠️ Risk Analysis",
        "tab_compliance": "✓ Compliance",
        "tab_clauses": "📄 Clauses",
        "tab_classification": "🏷️ Classifications",
        "tab_templates": "💡 Templates",
        "tab_export": "📑 Export",
        
        # Overview Tab
        "overview_header": "Contract Overview",
        "contract_type": "Contract Type",
        "confidence": "Confidence",
        "doc_length": "Document Length",
        "extracting_entities": "🔍 Extracting entities...",
        "parties": "👥 Parties",
        "no_parties": "No parties detected.",
        "dates": "📅 Dates Found",
        "no_dates": "No dates detected.",
        "amounts": "💰 Financial Amounts",
        "no_amounts": "No amounts detected.",
        
        # Risk Tab
        "risk_assessment": "🚨 Risk Assessment",
        "analyzing_risks": "⏳ Analyzing clauses for risks...",
        "high_risk": "🔴 High Risk",
        "medium_risk": "🟠 Medium Risk",
        "low_risk": "🟢 Low Risk",
        "overall_risk": "Overall Contract Risk",
        "high_risk_clauses": "High-Risk Clauses",
        "full_text": "Full Text",
        "issues": "Issues",
        "ambiguities": "Ambiguities Detected",
        "recommendation": "Recommendation",
        
        # Compliance Tab
        "compliance_checklist": "📋 Compliance Checklist",
        "running_compliance_checks": "📊 Running compliance checks...",
        "compliance_status": "Overall Compliance Status",
        "missing_clauses": "Missing Clauses",
        "compliance_issues": "Compliance Issues",
        "india_compliance": "India-Specific Compliance",
        "law_references": "Indian Law References",
        
        # Clause Tab
        "clause_analysis": "📄 Clause-by-Clause Analysis",
        "filter_risk": "Filter by Risk Level",
        "all": "All",
        "showing": "Showing",
        "clauses": "clauses",
        "issues_found": "Issues Found",
        
        # Classification Tab
        "clause_classification": "🏷️ Automatic Clause Classification",
        "classifying": "Classifying clauses...",
        "total_classified": "Total Clauses Classified",
        "clause_distribution": "Clause Distribution by Category",
        "detailed_classifications": "Detailed Classifications",
        "confidence": "Confidence",
        
        # Templates
        "templates_header": "📋 SME Contract Templates",
        "templates_page_title": "📋 Contract Templates & Suggestions",
        "select_template_type": "Select Template Type",
        "view_template": "View Template",
        "suggested_improvements": "📌 Suggested Improvements",
        "select_clause_type": "Select a clause type to improve",
        "get_alternative": "Get Alternative Clause",
        "avoid": "Avoid",
        "prefer": "Prefer",
        "reason": "Reason",
        "select_template": "Select Template",
        "view_full_template": "View Full Template",
        "custom_template": "🔄 Generate Custom Template",
        "fill_placeholders": "Fill in placeholders:",
        "services_desc": "Description of Services",
        "amount_inr": "Amount (INR)",
        "duration": "Duration (e.g., 12 months)",
        "generate": "Generate Template",
        "download_template": "📥 Download Template",
        
        # Knowledge Base
        "kb_header": "📚 Common Contract Issues & Solutions",
        "kb_stats": "📊 Knowledge Base Statistics",
        "total_issues": "Total Known Issues",
        "high_impact": "High-Impact Issues",
        "sme_focused": "SME Focused",
        "high_impact_list": "🎯 High-Impact Issues",
        "browse_issues": "🔍 Browse All Known Issues",
        "select_issue": "Select an issue to view details",
        "title": "Title",
        "frequency": "Frequency",
        "impact": "Impact",
        "india_sme_context": "India SME Context",
        "description": "Description",
        "example": "Example",
        "risk": "Risk",
        "solution": "Solution",
        "sample_fix": "Sample Fix",
        
        # Batch Processing
        "batch_header": "📦 Batch Contract Analysis",
        "batch_info": "Analyze multiple contracts at once and generate comparative reports",
        "step1": "Step 1: Prepare Files",
        "step1_info": "Place all contract files (PDF/DOCX/TXT) in a folder",
        "step2": "Step 2: Enter Folder Path",
        "folder_path": "Enter folder path (or leave empty for demo)",
        "process_batch": "🚀 Process Batch",
        "processing": "Processing batch... This may take a few minutes",
        "processed_count": "✅ Processed",
        "contracts": "contracts",
        "batch_summary": "Batch Summary",
        "total_processed": "Total Processed",
        "failed": "Failed",
        "contract_details": "Contract Details",
        "download_batch": "📥 Download Batch Report (JSON)",
        "no_files": "No contract files found in folder",
        "enter_path": "Please enter a valid folder path or demo mode will be shown",
        "demo_mode": "Demo Mode: Sample Batch Analysis",
        "production_demo": "In production, this would show results from analyzing multiple contracts",
        
        # Export
        "export_header": "📊 Export Reports",
        "json_report_button": "📄 Generate JSON Report",
        "markdown_report_button": "📋 Generate Markdown Report",
        "html_report_button": "🌐 Generate HTML Report",
        "pdf_report_button": "📄 Generate PDF Report",
        "generating_pdf": "Generating PDF...",
        "report_summary": "Report Summary",
        "pdf_success": "✅ PDF generated successfully!",
        "download_json": "📥 Download JSON",
        "download_md": "📥 Download Markdown",
        "download_html": "📥 Download HTML",
        "download_pdf": "📥 Download PDF",
        
        # Audit Logs
        "audit_header": "📝 Audit Trail",
        "total_events": "Total events logged",
        "recent_logs": "Display recent logs",
        "download_logs": "Download Audit Logs",
        "no_logs": "No audit logs yet.",
        
        # Help
        "help_header": "❓ Help & Documentation",
        "how_to_use": "How to Use This Bot",
        "risk_levels": "Risk Levels",
        "supported_features": "Supported Features",
        "tips": "Tips for SMEs",
        "gemini_setup": "Gemini API Setup",
        
        # Footer
        "footer": "🛡️ Contract Analysis & Risk Assessment Bot | v1.0 | Confidential & Secure",
        
        # Settings
        "settings": "⚙️ Settings",
        "risk_threshold": "Risk Threshold",
        "language": "Contract Language",
    },
    
    "hindi": {
        # Headers and Navigation
        "title": "⚖️ अनुबंध विश्लेषण और जोखिम मूल्यांकन बॉट",
        "subtitle": "अनुबंधों का विश्लेषण करें, जोखिमों की पहचान करें, और SMEs के लिए कार्रवाई योग्य कानूनी अंतर्दृष्टि प्राप्त करें",
        "nav_upload": "अपलोड और विश्लेषण करें",
        "nav_templates": "टेम्पलेट",
        "nav_kb": "ज्ञान आधार",
        "nav_batch": "बैच प्रोसेसिंग",
        "nav_audit": "ऑडिट लॉग्स",
        "nav_help": "सहायता",
        
        # Upload Section
        "upload_header": "📤 अनुबंध अपलोड करें",
        "upload_label": "एक अनुबंध फाइल चुनें",
        "parsing": "🔄 अनुबंध को पार्स कर रहे हैं...",
        
        # Tabs
        "tab_overview": "📊 सारांश",
        "tab_risk": "⚠️ जोखिम विश्लेषण",
        "tab_compliance": "✓ अनुपालन",
        "tab_clauses": "📄 खंड",
        "tab_classification": "🏷️ वर्गीकरण",
        "tab_templates": "💡 टेम्पलेट",
        "tab_export": "📑 निर्यात",
        
        # Overview Tab
        "overview_header": "अनुबंध सारांश",
        "contract_type": "अनुबंध प्रकार",
        "confidence": "विश्वास",
        "doc_length": "दस्तावेज़ लंबाई",
        "extracting_entities": "🔍 संस्थाओं को निकाल रहे हैं...",
        "parties": "👥 पक्ष",
        "no_parties": "कोई पक्ष का पता नहीं चला।",
        "dates": "📅 मिलीं तारीखें",
        "no_dates": "कोई तारीख का पता नहीं चला।",
        "amounts": "💰 वित्तीय राशियाँ",
        "no_amounts": "कोई राशि का पता नहीं चला।",
        
        # Risk Tab
        "risk_assessment": "🚨 जोखिम मूल्यांकन",
        "analyzing_risks": "⏳ खंडों का विश्लेषण कर रहे हैं...",
        "high_risk": "🔴 उच्च जोखिम",
        "medium_risk": "🟠 मध्यम जोखिम",
        "low_risk": "🟢 कम जोखिम",
        "overall_risk": "समग्र अनुबंध जोखिम",
        "high_risk_clauses": "उच्च जोखिम खंड",
        "full_text": "पूरा पाठ",
        "issues": "समस्याएँ",
        "ambiguities": "पहचाना गया अस्पष्टता",
        "recommendation": "सिफारिश",
        
        # Compliance Tab
        "compliance_checklist": "📋 अनुपालन चेकलिस्ट",
        "running_compliance_checks": "📊 अनुपालन जांच चला रहे हैं...",
        "compliance_status": "समग्र अनुपालन स्थिति",
        "missing_clauses": "अनुपस्थित खंड",
        "compliance_issues": "अनुपालन समस्याएँ",
        "india_compliance": "भारत-विशिष्ट अनुपालन",
        "law_references": "भारतीय कानूनों के संदर्भ",
        
        # Clause Tab
        "clause_analysis": "📄 खंड-दर-खंड विश्लेषण",
        "filter_risk": "जोखिम स्तर से फ़िल्टर करें",
        "all": "सभी",
        "showing": "दिखा रहे हैं",
        "clauses": "खंड",
        "issues_found": "पहचाई गई समस्याएँ",
        
        # Classification Tab
        "clause_classification": "🏷️ स्वचालित खंड वर्गीकरण",
        "classifying": "खंडों को वर्गीकृत कर रहे हैं...",
        "total_classified": "कुल वर्गीकृत खंड",
        "clause_distribution": "श्रेणी द्वारा खंड वितरण",
        "detailed_classifications": "विस्तृत वर्गीकरण",
        "confidence": "आत्मविश्वास",
        
        # Templates
        "templates_header": "📋 SME अनुबंध टेम्पलेट",
        "templates_page_title": "📋 अनुबंध टेम्पलेट और सुझाव",
        "select_template_type": "टेम्पलेट प्रकार चुनें",
        "view_template": "टेम्पलेट देखें",
        "suggested_improvements": "📌 सुझाए गए सुधार",
        "select_clause_type": "सुधार के लिए खंड प्रकार चुनें",
        "get_alternative": "वैकल्पिक खंड प्राप्त करें",
        "avoid": "बचें",
        "prefer": "पसंद करें",
        "reason": "कारण",
        "select_template": "टेम्पलेट चुनें",
        "view_full_template": "पूर्ण टेम्पलेट देखें",
        "custom_template": "🔄 कस्टम टेम्पलेट बनाएँ",
        "fill_placeholders": "प्लेसहोल्डर भरें:",
        "services_desc": "सेवाओं का विवरण",
        "amount_inr": "राशि (INR)",
        "duration": "अवधि (उदा। 12 महीने)",
        "generate": "टेम्पलेट बनाएँ",
        "download_template": "📥 टेम्पलेट डाउनलोड करें",
        
        # Knowledge Base
        "kb_header": "📚 सामान्य अनुबंध समस्याएँ और समाधान",
        "kb_stats": "📊 ज्ञान आधार सांख्यिकी",
        "total_issues": "कुल ज्ञात समस्याएँ",
        "high_impact": "उच्च प्रभाव समस्याएँ",
        "sme_focused": "SME केंद्रित",
        "high_impact_list": "🎯 उच्च प्रभाव समस्याएँ",
        "browse_issues": "🔍 सभी ज्ञात समस्याएँ ब्राउज़ करें",
        "select_issue": "विवरण देखने के लिए समस्या चुनें",
        "title": "शीर्षक",
        "frequency": "आवृत्ति",
        "impact": "प्रभाव",
        "india_sme_context": "भारत SME संदर्भ",
        "description": "विवरण",
        "example": "उदाहरण",
        "risk": "जोखिम",
        "solution": "समाधान",
        "sample_fix": "नमूना सुधार",
        
        # Batch Processing
        "batch_header": "📦 बैच अनुबंध विश्लेषण",
        "batch_info": "एक साथ कई अनुबंधों का विश्लेषण करें और तुलनात्मक रिपोर्ट बनाएँ",
        "step1": "चरण 1: फ़ाइलें तैयार करें",
        "step1_info": "सभी अनुबंध फ़ाइलें (PDF/DOCX/TXT) एक फ़ोल्डर में रखें",
        "step2": "चरण 2: फ़ोल्डर पथ दर्ज करें",
        "folder_path": "फ़ोल्डर पथ दर्ज करें (या डेमो के लिए खाली छोड़ें)",
        "process_batch": "🚀 बैच प्रोसेस करें",
        "processing": "बैच को प्रोसेस कर रहे हैं... इसमें कुछ मिनट लग सकते हैं",
        "processed_count": "✅ प्रक्षित किए गए",
        "contracts": "अनुबंध",
        "batch_summary": "बैच सारांश",
        "total_processed": "कुल प्रक्षित",
        "failed": "विफल",
        "contract_details": "अनुबंध विवरण",
        "download_batch": "📥 बैच रिपोर्ट डाउनलोड करें (JSON)",
        "no_files": "फ़ोल्डर में कोई अनुबंध फ़ाइल नहीं मिली",
        "enter_path": "कृपया वैध फ़ोल्डर पथ दर्ज करें या डेमो मोड दिखाया जाएगा",
        "demo_mode": "डेमो मोड: नमूना बैच विश्लेषण",
        "production_demo": "उत्पादन में, यह कई अनुबंधों के विश्लेषण के परिणाम दिखाएगा",
        
        # Export
        "export_header": "📊 रिपोर्ट निर्यात करें",
        "json_report_button": "📄 JSON रिपोर्ट बनाएँ",
        "markdown_report_button": "📋 मार्कडाउन रिपोर्ट बनाएँ",
        "html_report_button": "🌐 HTML रिपोर्ट बनाएँ",
        "pdf_report_button": "📄 PDF रिपोर्ट बनाएँ",
        "generating_pdf": "PDF बना रहे हैं...",
        "report_summary": "रिपोर्ट सारांश",
        "pdf_success": "✅ PDF सफलतापूर्वक बनाया गया!",
        "download_json": "📥 JSON डाउनलोड करें",
        "download_md": "📥 मार्कडाउन डाउनलोड करें",
        "download_html": "📥 HTML डाउनलोड करें",
        "download_pdf": "📥 PDF डाउनलोड करें",
        
        # Audit Logs
        "audit_header": "📝 ऑडिट ट्रेल",
        "total_events": "कुल लॉग किए गए इवेंट",
        "recent_logs": "हाल के लॉग दिखाएँ",
        "download_logs": "ऑडिट लॉग्स डाउनलोड करें",
        "no_logs": "अभी कोई ऑडिट लॉग नहीं।",
        
        # Help
        "help_header": "❓ सहायता और दस्तावेज़ीकरण",
        "how_to_use": "इस बॉट का उपयोग कैसे करें",
        "risk_levels": "जोखिम स्तर",
        "supported_features": "समर्थित विशेषताएँ",
        "tips": "SMEs के लिए सुझाव",
        "gemini_setup": "Gemini API सेटअप",
        
        # Footer
        "footer": "🛡️ अनुबंध विश्लेषण और जोखिम मूल्यांकन बॉट | v1.0 | गोपनीय और सुरक्षित",
        
        # Settings
        "settings": "⚙️ सेटिंग्स",
        "risk_threshold": "जोखिम थ्रेसहोल्ड",
        "language": "अनुबंध भाषा",
    }
}

def get_text(language: str, key: str) -> str:
    """Get translated text for given language and key."""
    lang = "hindi" if language.lower() == "hindi" else "english"
    return TRANSLATIONS.get(lang, TRANSLATIONS["english"]).get(key, key)
