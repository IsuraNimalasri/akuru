"""Download RoboHash robot images for offline use in this game.

Run once during setup (with internet), then the game uses local files only.
"""

from __future__ import annotations

from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.request import urlopen


TARGET_DIR = Path(__file__).resolve().parent / "assets" / "images" / "robots"
SEEDS = [
    "happy-number-keys-1",
    "happy-number-keys-2",
    "happy-number-keys-3",
    "happy-number-keys-4",
    "happy-number-keys-5",
    "happy-number-keys-6",
]


def robohash_url(seed: str) -> str:
    return f"https://robohash.org/{seed}.png?set=set3&size=220x220"


def download(seed: str, index: int) -> None:
    url = robohash_url(seed)
    target = TARGET_DIR / f"robot_robohash_{index}.png"
    with urlopen(url, timeout=20) as response:
        data = response.read()
    target.write_bytes(data)
    print(f"saved: {target.name}")


def main() -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    print(f"target: {TARGET_DIR}")
    for idx, seed in enumerate(SEEDS, start=1):
        try:
            download(seed, idx)
        except (URLError, HTTPError, TimeoutError) as exc:
            print(f"skip {seed}: {exc}")
    print("done")


if __name__ == "__main__":
    main()
