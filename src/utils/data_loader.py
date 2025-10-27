import json

def safe_load_json(path):
    """Safely loads a JSON file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Could not load JSON from {path}: {e}")
        return {}
