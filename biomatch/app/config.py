import os
from typing import Any, Dict

from dotenv import load_dotenv
import yaml


def load_config(config_path: str = None) -> Dict[str, Any]:
    """Load configuration from YAML and environment variables.

    Environment variables can override database URL or other runtime settings.
    """
    load_dotenv()
    path = config_path or os.environ.get("BIOMATCH_CONFIG", os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml"))

    config: Dict[str, Any] = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    # Database URL (env overrides)
    db_url = os.environ.get("DATABASE_URL") or config.get("database", {}).get("url")
    if db_url is None:
        # default to local sqlite in project root
        db_url = "sqlite:///./biomatch.db"
    config.setdefault("database", {})
    config["database"]["url"] = db_url

    # Defaults if missing
    config.setdefault("matching", {"min_confidence": 0.35, "face_weight": 0.6, "voice_weight": 0.4, "topk": 5})
    config.setdefault("video", {"sample_fps": 1, "max_frames": 20})
    config.setdefault("face", {"detection_threshold": 0.95, "image_enhance": True})
    config.setdefault("voice", {"min_duration_seconds": 2})

    return config