from pathlib import Path

import yaml

config: dict = (
    yaml.safe_load(
        (Path(__file__).resolve().parent.parent / "config.yml").read_text(
            encoding="utf-8"
        )
    )
    or {}
)
