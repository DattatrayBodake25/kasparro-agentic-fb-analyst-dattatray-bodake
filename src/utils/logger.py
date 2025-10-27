import json
from datetime import datetime
from pathlib import Path

# === Setup ===
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "system.log"


def _write_log(entry: dict):
    """Internal helper to append JSON log entries."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def log_event(agent_name: str, event: str, details: dict = None):
    """
    Generic event logger for all agents.
    Example:
        log_event("PlannerAgent", "completed", {"steps": 4})
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "event": event,
        "details": details or {}
    }
    _write_log(entry)


def log_step(agent_name: str, message: str, step: str = None):
    """
    Step-level logger (used heavily in agents).
    Compatible with existing calls like:
        log_step("CreativeAgent", "Loading data...")
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "step": step or "default",
        "message": message
    }
    _write_log(entry)
    print(f"[{agent_name}] {message}")
