"""Shared constants for UI and gameplay."""

from pathlib import Path

APP_TITLE = "Happy Number Keys"
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700

ROOT_DIR = Path(__file__).resolve().parent.parent
LOGO_PATH = ROOT_DIR / "logo.png"
ASSETS_DIR = ROOT_DIR / "assets"
ROBOT_DIR = ASSETS_DIR / "images" / "robots"
DATA_DIR = ROOT_DIR / "data"
PROGRESS_FILE = DATA_DIR / "progress.json"

TOTAL_LEVELS = 10
QUESTIONS_PER_LEVEL = 5

ALLOWED_KEYS = {
    "Left",
    "Right",
    "Up",
    "Down",
    "Return",
    "space",
    "Escape",
}

COLORS = {
    "bg": "#F4FBFF",
    "panel": "#FFFFFF",
    "title": "#2C3E50",
    "subtle": "#52616B",
    "choice": "#CFE8FF",
    "focus": "#FFB347",
    "focus_text": "#1F2D3A",
    "ok": "#79D070",
    "retry": "#F7DCA1",
    "star_on": "#F9C74F",
    "star_off": "#E2E8F0",
}

OBJECT_TYPES = ["apples", "mangoes", "dots", "stars", "balls", "blocks"]
PRAISE_TEXTS = ["Good job!", "Well done!", "Keep it up!"]
