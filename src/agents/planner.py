import json
import google.generativeai as genai
from pathlib import Path


class PlannerAgent:
    """
    PlannerAgent
    -------------
    Generates a structured execution plan for the system 
    based on a user query using a Gemini model.
    """

    def __init__(self, config):
        self.config = config
        self.model_name = config["llm"]["model"]
        genai.configure(api_key=config["env"]["GOOGLE_API_KEY"])

    def run(self, query: str) -> dict:
        """Generate a structured task plan based on the given user query."""
        prompt_path = Path("prompts/planner_prompt.md")

        # Load the planner base prompt
        try:
            base_prompt = prompt_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"[PlannerAgent] Prompt file not found: {prompt_path}")
            return {"objective": query, "subtasks": []}

        # Construct the full LLM input prompt
        full_prompt = f"{base_prompt}\n\nUser Query: {query}\n"

        # Call the Gemini model
        try:
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(full_prompt)
            text_output = response.text.strip()
        except Exception as e:
            print(f"[PlannerAgent] Model call failed: {e}")
            return {"objective": query, "subtasks": []}

        # Parse JSON structure from the model output
        try:
            start_idx = text_output.find("{")
            end_idx = text_output.rfind("}") + 1
            parsed_json = text_output[start_idx:end_idx]
            plan = json.loads(parsed_json)

            print("[PlannerAgent] Task breakdown generated successfully:")
            for i, sub in enumerate(plan.get("subtasks", []), 1):
                print(f"   {i}. {sub.get('agent', 'Unknown Agent')} → {sub.get('action', 'No action specified')}")
            return plan

        except Exception as e:
            print(f"[PlannerAgent] Failed to parse plan: {e}")
            print("[PlannerAgent] Raw model output:")
            print(text_output)
            return {"objective": query, "subtasks": []}
