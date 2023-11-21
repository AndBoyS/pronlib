import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> Any:
    with open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def dump_json(obj: Any, path: str | Path) -> None:
    with open(path, "wt", encoding="utf") as f:
        json.dump(obj, f, ensure_ascii=False)
