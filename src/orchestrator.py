import argparse
import json
from pathlib import Path

from src.utils.config_loader import load_config
from src.utils.logger import log_event

from src.agents.planner import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent
from src.agents.report_generator import ReportGenerator


def main(query: str | None = None):
    """Main orchestrator for the Kasparro Agentic FB Analyst project."""
    
    # Allow both CLI and programmatic use
    if query is None:
        parser = argparse.ArgumentParser(description="Kasparro Agentic FB Analyst")
        parser.add_argument("query", type=str, help="Example: 'Analyze ROAS drop'")
        args = parser.parse_args()
        query = args.query

    # --- Initialize configuration and environment ---
    try:
        config = load_config()
        Path("logs").mkdir(exist_ok=True)
        Path("reports").mkdir(exist_ok=True)
    except Exception as e:
        print(f"Error initializing environment: {e}")
        return

    print("Starting Agentic System")
    print(f"Query: {query}")
    print(f"Mode: {config['project']['mode']}")
    print(f"Using data: {config['paths']['data']}")
    print("Configuration and environment loaded successfully.\n")

    log_event("System", "initialized", {"query": query, "mode": config["project"]["mode"]})

    # --- Step 1: Planner Agent ---
    print("[Planner Agent] Decomposing query into subtasks...")
    try:
        planner = PlannerAgent(config)
        plan = planner.run(query)
        log_event("PlannerAgent", "completed", plan)

        print("Planner stage completed.\n")
        print("Structured Plan Output:")
        print(json.dumps(plan, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Planner Agent failed: {e}")
        return

    # --- Step 2: Data Agent ---
    print("\n[Data Agent] Summarizing dataset...")
    try:
        data_agent = DataAgent(config)
        data_summary = data_agent.run()
        log_event("DataAgent", "completed", data_summary)

        data_summary_path = Path("reports/data_summary.json")
        with open(data_summary_path, "w", encoding="utf-8") as f:
            json.dump(data_summary, f, indent=2, ensure_ascii=False)

        print(f"Data summary saved to {data_summary_path}")
        print("Next: Insight Agent will generate hypotheses (Step 3).")
    except Exception as e:
        print(f"Data Agent failed: {e}")
        return

    # --- Step 3: Insight Agent ---
    print("\n[Insight Agent] Generating hypotheses...")
    try:
        insight_agent = InsightAgent(config)
        insights = insight_agent.run()
        log_event("InsightAgent", "completed", insights)

        insights_path = Path("reports/insights.json")
        with open(insights_path, "w", encoding="utf-8") as f:
            json.dump(insights, f, indent=2, ensure_ascii=False)

        print("Insights saved to reports/insights.json")
    except Exception as e:
        print(f"Insight Agent failed: {e}")
        return

    # --- Step 4: Evaluator Agent ---
    print("\n[Evaluator Agent] Validating hypotheses...")
    try:
        evaluator_agent = EvaluatorAgent(config)
        evaluation = evaluator_agent.run()
        log_event("EvaluatorAgent", "completed", evaluation)

        eval_path = Path("reports/evaluation_results.json")
        with open(eval_path, "w", encoding="utf-8") as f:
            json.dump(evaluation, f, indent=2, ensure_ascii=False)

        print("Evaluation results saved to reports/evaluation_results.json")
        print("Next: Creative Agent will analyze underperforming creatives (Step 5).")
    except Exception as e:
        print(f"Evaluator Agent failed: {e}")
        return

    # --- Step 5: Creative Agent ---
    print("\n[Creative Agent] Analyzing and generating creative recommendations...")
    try:
        creative_agent = CreativeAgent(
            config=config,
            data_path=config["paths"]["data"],
            insights_path="reports/insights.json",
            creative_output_path="reports/creatives.json",
            prompt_path="prompts/creative_prompt.md"
        )

        creative_output = creative_agent.run()
        log_event("CreativeAgent", "completed", creative_output)

        creative_output_path = Path("reports/creatives.json")
        with open(creative_output_path, "w", encoding="utf-8") as f:
            json.dump(creative_output, f, indent=2, ensure_ascii=False)

        print("Creative output saved to reports/creatives.json")
    except Exception as e:
        print(f"Creative Agent failed: {e}")
        return

    # --- Step 6: Report Generator ---
    print("\n[Report Generator] Compiling final report...")
    try:
        report_gen = ReportGenerator(reports_dir="reports", output_file="reports/report.md")
        report_gen.generate_markdown_report()
        log_event("ReportGenerator", "completed", {"output": "reports/report.md"})
        print("Report successfully generated at: reports/report.md")
    except Exception as e:
        print(f"Report Generator failed: {e}")
        return

    # --- Completion ---
    print("\nAgentic System Run Complete.")
    print("Outputs generated:")
    print(" - reports/data_summary.json")
    print(" - reports/insights.json")
    print(" - reports/evaluation_results.json")
    print(" - reports/creatives.json")
    print(" - reports/report.md")
    print("End-to-end analysis completed successfully.")
    log_event("System", "completed", {"outputs_dir": "reports"})


if __name__ == "__main__":
    main()
