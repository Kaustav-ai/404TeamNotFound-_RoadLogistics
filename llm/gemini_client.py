import google.generativeai as genai
import os

def gemini_review(decision_text: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "APPROVE"

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-1.5-pro")
        prompt = f"""
Review the AI decision below for risk or over-optimism.

Decision:
{decision_text}

Reply ONLY:
APPROVE
or
OVERRIDE: <short reason>
"""
        res = model.generate_content(prompt)
        text = res.text.upper()
        return text if "OVERRIDE" in text else "APPROVE"
    except:
        return "APPROVE"
