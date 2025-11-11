import json
from typing import Any
from pathlib import Path

from bot.src.core import get_logger

_lg = get_logger()


def init_dir_and_files() -> None:
    try:
        _lg.info("DEVELOPING")
    except Exception as e:
        _lg.critical(f"Internal error: {e}.")


def load_from_file(self, file_path: Path | str, mode: str = "r") -> Any | None:
    """Load data from JSON file and return its contents"""
    try:
        with open(file_path, mode, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        _lg.critical(f"Internal error: {e}.")
        return None


def save_to_file(
    self,
    file_path: Path | str,
    var: dict[str, Any],
    jsonl: bool = False,
    mode: str = "w",
) -> None:
    """Save value to JSON or JSONL file"""
    try:
        if jsonl:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(var, ensure_ascii=False) + "\n")
        else:
            with open(file_path, mode, encoding="utf-8") as f:
                json.dump(var, f, indent=2, ensure_ascii=False)
    except Exception as e:
        _lg.critical(f"Internal error: {e}.")
