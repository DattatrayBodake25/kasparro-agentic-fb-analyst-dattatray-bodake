import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
import pytest

# --- Mock Google Generative AI (prevents live API calls) ---
import google.generativeai as genai

class MockGenerativeModel:
    """Mock Gemini model to bypass actual API calls."""
    def __init__(self, *args, **kwargs):
        pass

    def generate_content(self, prompt):
        # Return simple structured mock output to simulate Gemini response
        class Response:
            text = json.dumps({
                "objective": "Analyze ROAS drop",
                "subtasks": [
                    {"agent": "Data Agent", "action": "Analyze data trends"},
                    {"agent": "Insight Agent", "action": "Generate hypotheses"},
                    {"agent": "Evaluator Agent", "action": "Validate hypotheses"},
                    {"agent": "Creative Agent", "action": "Generate new creatives"}
                ]
            })
        return Response()

# Replace real class with mock globally
genai.GenerativeModel = MockGenerativeModel


# --- Imports after mocking ---
from src.utils.config_loader import load_config
from src.agents.planner import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent
from src.agents.report_generator import ReportGenerator


@pytest.fixture(scope="module")
def config():
    """Load configuration once for all tests."""
    return load_config()


@pytest.fixture(scope="module")
def reports_dir(tmp_path_factory):
    """Create a temporary reports directory for test outputs."""
    return tmp_path_factory.mktemp("reports")

@pytest.mark.integration
def test_full_agentic_pipeline(config, reports_dir):
    """
    End-to-end test of the full Agentic Facebook Analyst pipeline.

    This version uses a mock Gemini model to avoid external API calls.
    It verifies that each agent runs and produces expected output files.
    """

    try:
        # --- Step 1: Planner Agent ---
        planner = PlannerAgent(config)
        query = "Analyze ROAS drop"
        plan = planner.run(query)
        assert "subtasks" in plan and len(plan["subtasks"]) > 0, \
            "Planner should generate at least one subtask."

        # --- Step 2: Data Agent ---
        data_agent = DataAgent(config)
        data_summary = data_agent.run()
        assert "roas_trend" in data_summary, "Data summary must include 'roas_trend'."

        data_summary_path = reports_dir / "data_summary.json"
        data_summary_path.write_text(json.dumps(data_summary, indent=2), encoding="utf-8")

        # --- Step 3: Insight Agent ---
        insight_agent = InsightAgent(config)
        insights = insight_agent.run()
        assert "hypotheses" in insights, "Insight Agent should generate hypotheses."

        insights_path = reports_dir / "insights.json"
        insights_path.write_text(json.dumps(insights, indent=2), encoding="utf-8")

        # --- Step 4: Evaluator Agent ---
        evaluator_agent = EvaluatorAgent(config)
        evaluation = evaluator_agent.run()
        assert "validated_hypotheses" in evaluation, \
            "Evaluator should produce validated hypotheses."

        eval_path = reports_dir / "evaluation_results.json"
        eval_path.write_text(json.dumps(evaluation, indent=2), encoding="utf-8")

        # --- Step 5: Creative Agent ---
        creative_agent = CreativeAgent(
            config=config,
            data_path=config["paths"]["data"],
            insights_path=insights_path,
            creative_output_path=reports_dir / "creatives.json",
            prompt_path="prompts/creative_prompt.md"
        )
        creative_output = creative_agent.run()
        assert isinstance(creative_output, dict), "Creative Agent output must be a dict."
        assert "analysis" in creative_output, "Creative output must include an 'analysis' field."

        creative_output_path = reports_dir / "creatives.json"
        assert creative_output_path.exists(), "Creative output JSON must be saved."

        # --- Step 6: Report Generator ---
        report_output_path = reports_dir / "report.md"
        report_gen = ReportGenerator(reports_dir=reports_dir, output_file=report_output_path)
        report_gen.generate_markdown_report()
        assert report_output_path.exists(), "Markdown report should be generated successfully."

        print("\nFull pipeline test executed successfully.")
        print(f"Report generated at: {report_output_path}")

    except Exception as e:
        pytest.fail(f"Full pipeline test failed with error: {e}")
