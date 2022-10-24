import os
from pathlib import Path

IS_PROD = os.getenv("IS_PROD") is not None

PORT = int(os.getenv("PORT", "8081"))

JSON_DIR = (Path(__file__).parent / "../json").resolve()


def parsha_json(parsha: int):
    return JSON_DIR / f"{parsha}.json"
