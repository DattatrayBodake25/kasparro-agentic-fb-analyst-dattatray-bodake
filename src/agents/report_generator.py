import json
from datetime import datetime
from pathlib import Path


class ReportGenerator:
    """
    ReportGenerator
    ----------------
    Aggregates and compiles outputs from all agents into a unified Markdown report.
    """

    def __init__(self, reports_dir: str = "reports", output_file: str = "reports/report.md"):
        self.reports_dir = Path(reports_dir)
        self.output_file = Path(output_file)
        self.output_file.parent.mkdir(exist_ok=True)

    def _load_json(self, filename: str):
        """Safely load a JSON file from the reports directory."""
        path = self.reports_dir / filename
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"[ReportGenerator] Warning: Failed to parse JSON from {filename}.")
        return None

    def generate_markdown_report(self):
        """Combine agent outputs into a structured Markdown report."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # === Load all agent outputs ===
        data_summary = self._load_json("data_summary.json")
        insights = self._load_json("insights.json")
        evaluation = self._load_json("evaluation_results.json")
        creative_analysis = self._load_json("creative_analysis.json")
        creative_recommendations = (
            self._load_json("creative_recommendations.json")
            or self._load_json("creatives.json")
        )

        md = [
            "# Facebook ROAS Diagnostic Report",
            f"**Generated on:** {now}",
            "\n---\n"
        ]

        # === Section 1: Data Summary ===
        md.append("## 1. Data Summary\n")
        if data_summary:
            md.append(f"- Dataset Rows: {data_summary.get('dataset_rows', 'N/A')}")
            md.append(f"- ROAS Trend: {data_summary.get('roas_trend', 'N/A')}")
            md.append(f"- Low CTR Summary: {data_summary.get('low_ctr_summary', 'N/A')}")
            md.append(f"- Timestamp: {data_summary.get('timestamp', 'N/A')}")
        else:
            md.append("_No data summary available._")

        md.append("\n---\n")

        # === Section 2: Generated Hypotheses ===
        md.append("## 2. Generated Hypotheses\n")
        if insights and "hypotheses" in insights:
            for i, h in enumerate(insights["hypotheses"], 1):
                md.append(f"### {i}. {h.get('title', 'Untitled Hypothesis')}")
                md.append(f"- Evidence: {h.get('evidence', 'N/A')}")
                md.append(f"- Confidence: {h.get('confidence', 'N/A')}\n")
        else:
            md.append("_No hypotheses available._")

        md.append("\n---\n")

        # === Section 3: Hypothesis Evaluation ===
        md.append("## 3. Hypothesis Evaluation Results\n")
        if evaluation and "validated_hypotheses" in evaluation:
            for i, h in enumerate(evaluation["validated_hypotheses"], 1):
                md.append(f"### {i}. {h.get('title', 'Unnamed Hypothesis')}")
                md.append(f"- Reasoning: {h.get('reasoning', 'N/A')}")
                md.append(f"- Validated Confidence: {h.get('validated_confidence', 'N/A')}\n")
        else:
            md.append("_No evaluation results available._")

        md.append("\n---\n")

        # === Section 4: Creative Performance Analysis ===
        md.append("## 4. Creative Performance Analysis\n")
        if creative_analysis and "analysis" in creative_analysis:
            count = len(creative_analysis.get("analysis", []))
            md.append(f"- Underperforming Creatives Found: {count}\n")
            for c in creative_analysis.get("analysis", [])[:5]:
                md.append(
                    f"  - Creative ID: {c.get('creative_id', 'N/A')}, "
                    f"CTR: {c.get('ctr', 'N/A')}, "
                    f"ROAS: {c.get('roas', 'N/A')}"
                )
        else:
            md.append("_No creative analysis results found._")

        md.append("\n---\n")

        # === Section 5: Creative Recommendations ===
        md.append("## 5. Creative Recommendations\n")
        if creative_recommendations and "creative_recommendations" in creative_recommendations:
            for rec in creative_recommendations["creative_recommendations"][:3]:
                md.append(
                    f"### Creative ID: {rec.get('creative_id', 'N/A')} "
                    f"({rec.get('campaign_name', 'Unknown Campaign')})"
                )
                md.append(f"- Identified Issue: {rec.get('identified_issue', 'N/A')}")

                for r in rec.get("recommendations", []):
                    rec_type = r.get("type", "General")
                    md.append(f"  - Type: {rec_type}")
                    if rec_type == "Ad Copy":
                        md.append(f"    - Headline: {r.get('headline', 'N/A')}")
                        md.append(f"    - Primary Text: {r.get('primary_text', 'N/A')}")
                        md.append(f"    - CTA: {r.get('cta', 'N/A')}")
                    elif rec_type == "Visual Concept":
                        md.append(f"    - Theme: {r.get('theme', 'N/A')}")
                        md.append(f"    - Description: {r.get('description', 'N/A')}")
                    elif rec_type == "Targeting":
                        md.append(f"    - Suggestion: {r.get('suggestion', 'N/A')}")
                    md.append(f"    - Rationale: {r.get('rationale', 'N/A')}\n")
        else:
            md.append("_No creative recommendations available._")

        md.append("\n---\n")
        md.append("**End of Report**")

        # === Write to Markdown file ===
        self.output_file.write_text("\n".join(md), encoding="utf-8")
        print(f"[ReportGenerator] Report successfully generated at: {self.output_file}")