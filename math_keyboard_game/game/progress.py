"""Read/write local child progress data."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from .constants import PROGRESS_FILE, TOTAL_LEVELS


@dataclass
class ProgressState:
    unlocked_level: int = 1
    stars: Dict[str, int] = field(default_factory=dict)

    def star_for(self, level: int) -> int:
        return int(self.stars.get(str(level), 0))


def _default_data() -> Dict[str, object]:
    return {"unlocked_level": 1, "stars": {}}


def load_progress(path: Path = PROGRESS_FILE) -> ProgressState:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        save_progress(ProgressState(), path)
        return ProgressState()

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        state = ProgressState()
        save_progress(state, path)
        return state

    unlocked = int(raw.get("unlocked_level", 1))
    unlocked = max(1, min(TOTAL_LEVELS, unlocked))
    stars = raw.get("stars", {})
    if not isinstance(stars, dict):
        stars = {}
    clean_stars = {
        str(k): max(0, min(3, int(v)))
        for k, v in stars.items()
        if str(k).isdigit() and 1 <= int(k) <= TOTAL_LEVELS
    }
    return ProgressState(unlocked_level=unlocked, stars=clean_stars)


def save_progress(state: ProgressState, path: Path = PROGRESS_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "unlocked_level": state.unlocked_level,
        "stars": state.stars,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def reset_progress(path: Path = PROGRESS_FILE) -> ProgressState:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_default_data(), indent=2), encoding="utf-8")
    return ProgressState()


def complete_level(state: ProgressState, level: int, stars: int) -> ProgressState:
    stars = max(1, min(3, stars))
    current = state.star_for(level)
    state.stars[str(level)] = max(current, stars)

    next_level = min(TOTAL_LEVELS, level + 1)
    if state.unlocked_level < next_level:
        state.unlocked_level = next_level
    return state


def stars_row(stars: int) -> List[bool]:
    clamped = max(0, min(3, stars))
    return [i < clamped for i in range(3)]
