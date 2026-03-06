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


def _create_cat_image(bg_color):
    T = bg_color
    E = "#FF8C00"
    F = "#FFB347"
    B = "#2C3E50"
    P = "#FF69B4"

    cat = [
        [T, E, T, T, T, T, E, T],
        [E, E, T, T, T, T, E, E],
        [E, F, F, F, F, F, F, E],
        [F, F, B, F, F, B, F, F],
        [F, F, F, F, F, F, F, F],
        [F, F, F, P, P, F, F, F],
        [T, F, F, F, F, F, F, T],
        [T, T, F, F, F, F, T, T],
    ]

    base = tk.PhotoImage(width=8, height=8)
    rows = []
    for row in cat:
        rows.append("{" + " ".join(row) + "}")
    base.put(" ".join(rows))
    return base.zoom(3, 3)


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

        self._bob_index = 0
        self._bob_offset = 0

        self._build_ui()
        self._create_cursor()
        self._update_cursor_pos()
        self._animate_bob()

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
            insertwidth=0,
            relief="flat",
            bd=0,
        )
        self.display.grid(row=0, column=0, sticky="nsew")

        self.display.bind("<Key>", self._on_key)
        self.display.focus_set()

    def _create_cursor(self):
        self._cursor_img = _create_cat_image(COLORS["display_bg"])
        self._cursor_label = tk.Label(
            self.display,
            image=self._cursor_img,
            bg=COLORS["display_bg"],
            bd=0,
        )
        self._cursor_label.bind(
            "<Button-1>", lambda e: self.display.focus_set()
        )

    def _update_cursor_pos(self):
        try:
            bbox = self.display.bbox("insert")
            if bbox:
                x, y, w, h = bbox
                cat_h = self._cursor_img.height()
                self._cursor_label.place(
                    x=x + w,
                    y=y + h - cat_h + self._bob_offset,
                )
            else:
                self._cursor_label.place_forget()
        except tk.TclError:
            pass
        self.root.after(30, self._update_cursor_pos)

    def _animate_bob(self):
        seq = [0, -1, -2, -3, -2, -1, 0, 1, 2, 3, 2, 1]
        self._bob_index = (self._bob_index + 1) % len(seq)
        self._bob_offset = seq[self._bob_index]
        self.root.after(120, self._animate_bob)

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
