import os
from pathlib import Path
from typing import Dict


def load_dotenv(dotenv_path: str = ".env") -> Dict[str, str]:
    path = Path(dotenv_path)
    if not path.exists():
        return {}

    env_vars: Dict[str, str] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            if "=" not in stripped:
                continue

            key, value = stripped.split("=", 1)
            env_vars[key.strip()] = value.strip().strip('"').strip("'")

    os.environ.update(env_vars)
    return env_vars


def getenv(key: str, default: str | None = None) -> str | None:
    return os.environ.get(key, default)
