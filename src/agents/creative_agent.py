import json
from pathlib import Path
from datetime import datetime
import pandas as pd

from src.utils.logger import log_step
from src.utils.data_loader import safe_load_json
from src.utils.llm import call_gemini


class CreativeAgent:
    """
    CreativeAgent
    --------------
    Analyzes underperforming Facebook Ads creatives and
    generates improvement ideas using an LLM (e.g., Gemini).

    Workflow:
      1. Load and filter creatives below CTR/ROAS thresholds
      2. Identify performance issues
      3. Generate creative improvement ideas via LLM
    """

    def __init__(
        self,
        config,
        data_path: str = "data/synthetic_fb_ads_undergarments.csv",
        insights_path: str = "reports/insights.json",
        creative_output_path: str = "reports/creatives.json",
        prompt_path: str = "prompts/creative_prompt.md"
    ):
        self.config = config
        self.data_path = Path(data_path)
        self.insights_path = Path(insights_path)
        self.creative_output_path = Path(creative_output_path)
        self.prompt_path = Path(prompt_path)
        self.data = None
        self.analysis_results = []

    def load_data(self):
        """Load ad performance data safely and normalize column names."""
        log_step("CreativeAgent", "Loading ad performance data.")
        try:
            df = pd.read_csv(self.data_path)
            df.columns = [c.lower() for c in df.columns]
            self.data = df
            log_step("CreativeAgent", f"Data loaded successfully ({len(df)} rows).")
        except FileNotFoundError:
            log_step("CreativeAgent", f"Data file not found: {self.data_path}")
            raise
        except Exception as e:
            log_step("CreativeAgent", f"Error loading data: {e}")
            raise

    def analyze_creatives(self):
        """Identify creatives performing below CTR/ROAS thresholds."""
        log_step("CreativeAgent", "Analyzing underperforming creatives.")

        ctr_threshold = self.config["thresholds"].get("low_ctr", 0.7)
        roas_threshold = self.config["thresholds"].get("low_roas", 1.5)

        for idx, row in self.data.iterrows():
            ctr = row.get("ctr", 0)
            roas = row.get("roas", 0)

            if ctr < ctr_threshold or roas < roas_threshold:
                issue = self.identify_issue(ctr, roas)
                self.analysis_results.append({
                    "creative_id": row.get("ad_id", f"CR-{idx}"),
                    "campaign_name": row.get("campaign_name", "Unknown"),
                    "ctr": ctr,
                    "roas": roas,
                    "spend": row.get("spend", 0),
                    "identified_issue": issue,
                })

        log_step(
            "CreativeAgent",
            f"Detected {len(self.analysis_results)} underperforming creatives."
        )

    def identify_issue(self, ctr, roas):
        """Basic rules to identify common performance issues."""
        if ctr < 0.5:
            return "Low engagement — possible ad fatigue or weak copy."
        if roas < 1.2:
            return "Low conversion — possible targeting or offer mismatch."
        return "Moderate performance — requires further testing."

    def generate_improvements(self):
        """
        Generate improvement ideas using the LLM.
        Combines creative analysis and prior insights for context.
        """
        log_step("CreativeAgent", "Generating creative improvement suggestions.")

        insights = safe_load_json(self.insights_path)
        prompt_template = self._load_prompt_template()

        # Combine analysis + insights into a structured context
        context = (
            "You are a senior Facebook Ads creative strategist.\n\n"
            "Underperforming creatives:\n"
            f"{json.dumps(self.analysis_results, indent=2)}\n\n"
            "Context (insights from earlier analysis):\n"
            f"{json.dumps(insights, indent=2)}\n\n"
            "Now, based on this information, propose 3 new creative ideas for each weak area.\n"
            "Use the following format:\n"
            f"{prompt_template}"
        )

        try:
            llm_output = call_gemini(context)
            parsed_output = self._parse_llm_output(llm_output)

            final_output = {
                "timestamp": datetime.now().isoformat(),
                "analysis": self.analysis_results,
                "creative_recommendations": parsed_output.get("creative_recommendations", []),
                "raw_output": parsed_output.get("raw_output", ""),
            }

            self._save_json(self.creative_output_path, final_output)
            log_step("CreativeAgent", "Creative recommendations saved successfully.")
            return final_output

        except Exception as e:
            log_step("CreativeAgent", f"Error generating creative recommendations: {e}")
            raise

    def _load_prompt_template(self):
        """Read the creative prompt file."""
        try:
            return self.prompt_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {self.prompt_path}")
        except Exception as e:
            log_step("CreativeAgent", f"Error reading prompt file: {e}")
            raise

    def _parse_llm_output(self, text: str):
        """Parse JSON-like LLM output safely and robustly."""
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            json_str = text[start:end].strip()
            if not json_str:
                raise ValueError("Empty JSON segment in LLM output.")
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Attempt partial recovery if malformed JSON
            log_step("CreativeAgent", "Partial JSON detected, attempting fallback parsing.")
            try:
                fixed_text = text.replace("\n", " ").replace("'", '"')
                start = fixed_text.find("{")
                end = fixed_text.rfind("}") + 1
                return json.loads(fixed_text[start:end])
            except Exception:
                log_step("CreativeAgent", "Fallback parsing failed; returning raw output.")
                return {"creative_recommendations": [], "raw_output": text}
        except Exception as e:
            log_step("CreativeAgent", f"Parsing error: {e}")
            return {"creative_recommendations": [], "raw_output": text}

    def _save_json(self, path: Path, data: dict):
        """Save structured data to JSON file."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            log_step("CreativeAgent", f"Output saved to: {path}")
        except Exception as e:
            log_step("CreativeAgent", f"Error saving JSON file: {e}")
            raise

    def run(self):
        """Main entry point for the CreativeAgent."""
        self.load_data()
        self.analyze_creatives()
        return self.generate_improvements()