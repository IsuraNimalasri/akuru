import tkinter as tk
from tkinter import font as tkfont
import platform

from akuru.mappings import KEY_MAP

COLORS = {
    "bg": "#FFF8E7",
    "display_bg": "#FFF8E7",
    "display_fg": "#0E5EAF",
}

SINHALA_FONTS = [
    "Noto Sans Sinhala",
    "Iskoola Pota",
    "UN-Abhaya",
    "Malithi Web",
    "Sinhala Sangam MN",
]


def _find_sinhala_font(root):
    available = set(tkfont.families(root))
    for name in SINHALA_FONTS:
        if name in available:
            return name
    return None


class AkuruApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("අකුරු - Akuru")
        self.root.configure(bg=COLORS["bg"])

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_w}x{screen_h}+0+0")

        try:
            self.root.attributes("-fullscreen", True)
        except tk.TclError:
            pass

        sinhala_font = _find_sinhala_font(self.root)
        base = sinhala_font or "TkDefaultFont"
        self.font_display = (base, 48)

        self._build_ui()

        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.display = tk.Text(
            self.root,
            font=self.font_display,
            bg=COLORS["display_bg"],
            fg=COLORS["display_fg"],
            wrap="word",
            padx=32,
            pady=32,
            insertwidth=6,
            insertbackground="#E74C3C",
            insertontime=600,
            insertofftime=300,
            relief="flat",
            bd=0,
        )
        self.display.grid(row=0, column=0, sticky="nsew")

        self.display.bind("<Key>", self._on_key)
        self.display.focus_set()

    def _on_key(self, event):
        if event.keysym in ("BackSpace", "Delete"):
            pos = self.display.index("insert")
            if pos == "1.0":
                return "break"
            line, col = pos.split(".")
            line, col = int(line), int(col)
            if col > 0:
                line_text = self.display.get(f"{line}.0", pos)
                self.display.delete(f"{line}.{len(line_text) - 1}", pos)
            elif line > 1:
                self.display.delete(f"{line - 1}.end", pos)
            return "break"
        if event.keysym == "Return":
            self.display.insert("insert", "\n")
            return "break"
        if event.keysym == "space":
            self.display.insert("insert", " ")
            return "break"
        if event.keysym == "Escape":
            return

        char = event.char
        if char and char in KEY_MAP:
            self.display.insert("insert", KEY_MAP[char])
            return "break"

        if char and char.isprintable():
            return "break"

    def run(self):
        self.root.mainloop()
