import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pytest
from src.agents.evaluator_agent import EvaluatorAgent
from src.utils.config_loader import load_config


@pytest.mark.unit
def test_evaluator_agent_validates_hypotheses():
    config = load_config()
    agent = EvaluatorAgent(config)
    result = agent.run()

    assert "validated_hypotheses" in result
    assert isinstance(result["validated_hypotheses"], list)
