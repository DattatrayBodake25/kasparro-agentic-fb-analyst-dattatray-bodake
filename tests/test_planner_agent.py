import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pytest
from src.agents.planner import PlannerAgent
from src.utils.config_loader import load_config


@pytest.mark.unit
def test_planner_generates_valid_plan():
    config = load_config()
    agent = PlannerAgent(config)
    query = "Analyze ROAS drop"
    plan = agent.run(query)

    assert isinstance(plan, dict)
    assert "subtasks" in plan
    assert len(plan["subtasks"]) > 0
    for task in plan["subtasks"]:
        assert "agent" in task
        assert "action" in task