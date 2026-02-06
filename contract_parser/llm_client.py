import os
from typing import Optional


class LLMClient:
    """Gemini API client for legal contract analysis with fallback to rule-based analysis."""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = "gemini-1.5-flash"  # or gemini-pro for stronger reasoning
        self.client = None
        
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel(self.model_name)
                self.available = True
            except ImportError:
                print("⚠️ google-generativeai not installed. Install with: pip install google-generativeai")
                self.available = False
        else:
            self.available = False

    def summarize(self, prompt: str, max_length: int = 500) -> str:
        """Summarize contract or clause in plain English."""
        if not self.available:
            return self._fallback_summarize(prompt[:1200])
        
        try:
            response = self.client.generate_content(
                f"Summarize this legal text in simple business English (max {max_length} words):\n\n{prompt[:3000]}"
            )
            return response.text
        except Exception as e:
            return self._fallback_summarize(prompt[:1200])

    def explain_clause(self, clause: str) -> dict:
        """Explain a clause in simple language with key points."""
        if not self.available:
            return self._fallback_explain(clause)
        
        try:
            prompt = f"""Analyze this legal clause and provide:
1. Simple explanation (2-3 sentences)
2. Key obligations (if any)
3. Key rights (if any) 
4. Potential risks (if any)
5. Recommendation for SME

Clause: {clause}"""
            
            response = self.client.generate_content(prompt)
            text = response.text
            
            return {
                "explanation": text,
                "source": "Gemini API",
                "available": True
            }
        except Exception as e:
            return self._fallback_explain(clause)

    def suggest_alternative(self, clause: str, risk_level: str) -> dict:
        """Suggest alternative wording for a problematic clause."""
        if not self.available:
            return self._fallback_alternative(clause, risk_level)
        
        try:
            prompt = f"""For this {risk_level}-risk legal clause, suggest a more balanced alternative wording 
that protects both parties fairly and is SME-friendly:

Original: {clause}

Provide:
1. Problem with original
2. Suggested alternative
3. Why it's better"""
            
            response = self.client.generate_content(prompt)
            return {
                "suggestion": response.text,
                "source": "Gemini API",
                "available": True
            }
        except Exception as e:
            return self._fallback_alternative(clause, risk_level)

    def risk_reasoning(self, clause: str) -> str:
        """Generate detailed risk reasoning using LLM."""
        if not self.available:
            return "Risk assessment based on keyword matching (LLM unavailable)"
        
        try:
            prompt = f"""Why is this legal clause risky? Provide brief risk reasoning:

{clause}

Format: [Risk Category]: [Specific Concern]"""
            
            response = self.client.generate_content(prompt)
            return response.text
        except Exception as e:
            return "Risk assessment based on keyword matching (LLM error)"

    def _fallback_summarize(self, text: str) -> str:
        """Fallback when Gemini API unavailable."""
        return f"""📝 Summary (Rule-based, Gemini API unavailable):
        
Key excerpt: {text[:300]}...

To enable AI-powered summaries:
1. Get free Gemini API key from: https://aistudio.google.com/app/apikey
2. Add to .env file: GEMINI_API_KEY=your_key_here
3. Install: pip install google-generativeai
4. Restart the app"""

    def _fallback_explain(self, clause: str) -> dict:
        return {
            "explanation": f"Clause excerpt: {clause[:200]}...\n\nNote: Enable Gemini API for AI explanations.",
            "source": "Rule-based",
            "available": False
        }

    def _fallback_alternative(self, clause: str, risk_level: str) -> dict:
        return {
            "suggestion": f"To get AI-powered alternatives for {risk_level}-risk clauses, enable Gemini API.",
            "source": "Rule-based",
            "available": False
        }
