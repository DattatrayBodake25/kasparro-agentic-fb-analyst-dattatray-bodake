import os
import yaml
from dotenv import load_dotenv
from pathlib import Path

def load_config(config_path: str = "config/config.yaml") -> dict:
    """Load YAML config + environment variables"""
    # Load .env
    load_dotenv()

    # Load YAML
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Inject environment variables
    config["env"] = {
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "LANGFUSE_PUBLIC_KEY": os.getenv("LANGFUSE_PUBLIC_KEY"),
        "LANGFUSE_SECRET_KEY": os.getenv("LANGFUSE_SECRET_KEY"),
    }

    return config

if __name__ == "__main__":
    cfg = load_config()
    print("Config loaded successfully:")
    print(cfg)