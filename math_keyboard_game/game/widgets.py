"""Reusable UI widgets and drawing helpers."""

from pathlib import Path
import tkinter as tk
from typing import List

from .constants import COLORS


class FocusButton(tk.Frame):
    """Large keyboard-focused button."""

    def __init__(self, parent: tk.Widget, text: str, width: int = 240, height: int = 120):
        super().__init__(parent, bg=COLORS["choice"], highlightthickness=6)
        self.configure(highlightbackground=COLORS["choice"], highlightcolor=COLORS["focus"])
        self._text = tk.Label(
            self,
            text=text,
            bg=COLORS["choice"],
            fg=COLORS["focus_text"],
            font=("Helvetica", 34, "bold"),
            width=max(1, width // 35),
            height=max(1, height // 45),
        )
        self._text.pack(expand=True, fill="both", padx=8, pady=8)
        self.locked = False

    def set_text(self, text: str) -> None:
        self._text.config(text=text)

    def set_focused(self, focused: bool) -> None:
        color = COLORS["focus"] if focused else COLORS["choice"]
        self.configure(highlightbackground=color)

    def set_locked(self, locked: bool) -> None:
        self.locked = locked
        if locked:
            self._text.config(fg="#95A5A6")
            self.configure(bg="#EAF2F8")
            self._text.configure(bg="#EAF2F8")
        else:
            self._text.config(fg=COLORS["focus_text"])
            self.configure(bg=COLORS["choice"])
            self._text.configure(bg=COLORS["choice"])


def draw_objects(canvas: tk.Canvas, object_type: str, count: int, x0: int, y0: int, width: int = 360) -> None:
    """Draws simple local objects for counting."""
    if count <= 0:
        return

    cols = min(5, count)
    gap_x = width / max(1, cols)
    size = 28
    for idx in range(count):
        row = idx // cols
        col = idx % cols
        cx = x0 + int(col * gap_x + gap_x / 2)
        cy = y0 + row * 70

        if object_type == "apples":
            canvas.create_oval(cx - size, cy - size, cx + size, cy + size, fill="#F94144", outline="")
            canvas.create_rectangle(cx - 4, cy - size - 10, cx + 4, cy - size + 2, fill="#6D4C41", outline="")
            canvas.create_oval(cx + 4, cy - size - 8, cx + 18, cy - size + 4, fill="#90BE6D", outline="")
        elif object_type == "mangoes":
            canvas.create_oval(cx - size + 4, cy - size, cx + size, cy + size - 6, fill="#F9C74F", outline="")
        elif object_type == "dots":
            canvas.create_oval(cx - 12, cy - 12, cx + 12, cy + 12, fill="#577590", outline="")
        elif object_type == "stars":
            points = [
                cx,
                cy - 26,
                cx + 10,
                cy - 8,
                cx + 26,
                cy - 6,
                cx + 14,
                cy + 8,
                cx + 18,
                cy + 24,
                cx,
                cy + 14,
                cx - 18,
                cy + 24,
                cx - 14,
                cy + 8,
                cx - 26,
                cy - 6,
                cx - 10,
                cy - 8,
            ]
            canvas.create_polygon(points, fill="#F9C74F", outline="")
        elif object_type == "blocks":
            canvas.create_rectangle(cx - 24, cy - 24, cx + 24, cy + 24, fill="#43AA8B", outline="")
        else:
            canvas.create_oval(cx - 24, cy - 24, cx + 24, cy + 24, fill="#90BE6D", outline="")


def draw_robot_placeholder(canvas: tk.Canvas, x: int, y: int, scale: int = 1) -> None:
    """Draws a friendly robot when image files are missing."""
    s = max(1, scale)
    canvas.create_rectangle(x, y, x + 120 * s, y + 120 * s, fill="#D9EDFF", outline="#6CA6CD", width=4)
    canvas.create_rectangle(x + 20 * s, y + 20 * s, x + 100 * s, y + 70 * s, fill="#FFFFFF", outline="#6CA6CD", width=3)
    canvas.create_oval(x + 32 * s, y + 34 * s, x + 48 * s, y + 50 * s, fill="#4A90E2", outline="")
    canvas.create_oval(x + 72 * s, y + 34 * s, x + 88 * s, y + 50 * s, fill="#4A90E2", outline="")
    canvas.create_arc(
        x + 40 * s,
        y + 44 * s,
        x + 80 * s,
        y + 66 * s,
        start=200,
        extent=140,
        style=tk.ARC,
        width=3,
        outline="#6CA6CD",
    )
    canvas.create_line(x + 60 * s, y - 10 * s, x + 60 * s, y + 6 * s, fill="#6CA6CD", width=3)
    canvas.create_oval(x + 54 * s, y - 18 * s, x + 66 * s, y - 6 * s, fill="#F9C74F", outline="")


def load_robot_images(folder: Path) -> List[tk.PhotoImage]:
    images: List[tk.PhotoImage] = []
    patterns = ("*.png", "*.gif", "*.ppm", "*.pgm")
    for pattern in patterns:
        for path in sorted(folder.glob(pattern)):
            try:
                images.append(tk.PhotoImage(file=str(path)))
            except tk.TclError:
                continue
    return images
