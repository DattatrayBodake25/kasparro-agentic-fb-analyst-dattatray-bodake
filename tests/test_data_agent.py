import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pytest
from src.agents.data_agent import DataAgent
from src.utils.config_loader import load_config


@pytest.mark.unit
def test_data_agent_generates_summary():
    config = load_config()
    agent = DataAgent(config)
    summary = agent.run()

    assert "roas_trend" in summary
    assert "low_ctr_summary" in summary
    assert isinstance(summary["roas_trend"], dict)
