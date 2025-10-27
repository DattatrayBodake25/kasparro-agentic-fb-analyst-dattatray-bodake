import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
import pytest
from src.agents.creative_agent import CreativeAgent
from src.utils.config_loader import load_config


@pytest.mark.unit
def test_creative_agent_creates_output(tmp_path):
    config = load_config()
    insights_path = tmp_path / "insights.json"
    insights_path.write_text(json.dumps({"dummy": "insight"}))

    creative_agent = CreativeAgent(
        config=config,
        data_path=config["paths"]["data"],
        insights_path=insights_path,
        creative_output_path=tmp_path / "creatives.json",
        prompt_path="prompts/creative_prompt.md"
    )

    result = creative_agent.run()
    assert "analysis" in result
    assert (tmp_path / "creatives.json").exists()
