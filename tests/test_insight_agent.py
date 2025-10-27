import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pytest
from src.agents.insight_agent import InsightAgent
from src.utils.config_loader import load_config


@pytest.mark.unit
def test_insight_agent_generates_hypotheses():
    config = load_config()
    agent = InsightAgent(config)
    result = agent.run()

    assert "hypotheses" in result
    assert isinstance(result["hypotheses"], list)