import os
import json
import google.generativeai as genai
from src.utils.logger import log_step

# Configure Gemini (ensure GOOGLE_API_KEY is set in .env)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def call_gemini(prompt: str, model: str = "gemini-2.0-flash"):
    """Wrapper to call Google Gemini model for real LLM inference."""
    log_step("LLM", "call_gemini", f"Calling Gemini model: {model}")
    try:
        response = genai.GenerativeModel(model).generate_content(prompt)
        return response.text
    except Exception as e:
        log_step("LLM", "call_gemini", f" Gemini API call failed: {e}")
        raise


def call_llm_model(model: str, prompt: str, temperature: float = 0.7):
    """
    Simulated LLM interface used by InsightAgent or fallback mode.
    If Gemini API fails or simulation is preferred, returns a JSON-like response.
    """
    log_step("LLM", "call_llm_model", f"Simulating call for model: {model}")

    # Simulated responses for Insight Agent
    if "Insight Agent" in prompt or "hypotheses" in prompt.lower():
        simulated_output = {
            "hypotheses": [
                {
                    "id": "H1",
                    "title": "Ad Fatigue reducing CTR and conversions",
                    "evidence": "ROAS declining with consistent spend and impressions; CTR also low for multiple campaigns.",
                    "confidence": 0.82,
                },
                {
                    "id": "H2",
                    "title": "Increased competition in ad auctions",
                    "evidence": "ROAS decline despite steady CTR may suggest higher CPMs or auction pressure.",
                    "confidence": 0.67,
                },
                {
                    "id": "H3",
                    "title": "Audience targeting misalignment",
                    "evidence": "CTR low across multiple demographic segments; possible mismatch with creative messaging.",
                    "confidence": 0.74,
                },
            ]
        }
        return json.dumps(simulated_output, indent=2)

    # Simulated responses for Creative Agent
    elif "Creative Agent" in prompt or "creatives" in prompt.lower():
        simulated_output = {
            "recommendations": [
                {
                    "creative_id": "CR-101",
                    "issue": "Low engagement rate",
                    "recommendation": "Use more emotional storytelling and lifestyle imagery.",
                    "confidence": 0.88,
                },
                {
                    "creative_id": "CR-102",
                    "issue": "High CPM with low CTR",
                    "recommendation": "Simplify visuals, improve call-to-action placement.",
                    "confidence": 0.81,
                },
                {
                    "creative_id": "CR-103",
                    "issue": "Ad fatigue detected",
                    "recommendation": "Refresh visual layout and test new headline.",
                    "confidence": 0.79,
                },
            ],
        }
        return json.dumps(simulated_output, indent=2)

    # Generic fallback
    fallback = {"message": "Simulated generic LLM response", "prompt_excerpt": prompt[:150]}
    return json.dumps(fallback, indent=2)