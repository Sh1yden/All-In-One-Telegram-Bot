import json
import subprocess
from typing import Tuple

from src.core import get_logger

_lg = get_logger()


def start_tuna(port: int) -> Tuple[str, subprocess.Popen]:

    process = subprocess.Popen(
        ["tuna", "http", str(port), "--log-format", "json", "--log", "stdout"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if process:
        _lg.info("Process Created Successful.")

    public_url = None

    if process.stdout is not None:
        for line in process.stdout:
            try:
                data = json.loads(line.strip())
                if "url" in data:
                    public_url = data["url"]
                    break
            except json.JSONDecodeError:
                _lg.critical("JSONDecodeError.")
                continue

    if not public_url:
        process.terminate()
        raise RuntimeError("Не удалось получить публичный URL от tuna.")

    return public_url, process
