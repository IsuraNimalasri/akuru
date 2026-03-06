import tkinter as tk
from tkinter import font as tkfont
import platform

from akuru.mappings import VOWELS, CONSONANTS, VOWEL_SIGNS, KEY_MAP

COLORS = {
    "bg": "#FFF8E7",
    "display_bg": "#FFFFFF",
    "display_fg": "#2C3E50",
    "vowel": "#5DADE2",
    "vowel_hover": "#3498DB",
    "consonant": "#58D68D",
    "consonant_hover": "#2ECC71",
    "sign": "#F0AD4E",
    "sign_hover": "#E89B2D",
    "action": "#E74C3C",
    "action_hover": "#C0392B",
    "space": "#AEB6BF",
    "space_hover": "#95A5A6",
    "section_label": "#6C3483",
    "key_fg": "#FFFFFF",
    "tooltip_fg": "#7F8C8D",
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
        self.root.minsize(600, 500)

        sinhala_font = _find_sinhala_font(self.root)
        base = sinhala_font or "TkDefaultFont"

        self.font_display = (base, 28)
        self.font_button = (base, 18)
        self.font_tooltip = ("TkDefaultFont", 9)
        self.font_section = ("TkDefaultFont", 12, "bold")
        self.font_action = ("TkDefaultFont", 12)

        self._build_ui()
        self.root.bind("<Key>", self._on_key)

    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        wrapper = tk.Canvas(self.root, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=wrapper.yview)
        self.scroll_frame = tk.Frame(wrapper, bg=COLORS["bg"])

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: wrapper.configure(scrollregion=wrapper.bbox("all")),
        )
        wrapper.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        wrapper.configure(yscrollcommand=scrollbar.set)

        wrapper.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.scroll_frame.columnconfigure(0, weight=1)

        self._bind_mousewheel(wrapper)

        self._build_display(self.scroll_frame)
        self._build_toolbar(self.scroll_frame)
        self._build_section(
            self.scroll_frame, "ස්වර  (Vowels)", VOWELS, COLORS["vowel"], COLORS["vowel_hover"]
        )
        self._build_consonants(self.scroll_frame)
        self._build_section(
            self.scroll_frame, "පිලි  (Vowel Signs)", VOWEL_SIGNS, COLORS["sign"], COLORS["sign_hover"]
        )

    def _bind_mousewheel(self, canvas):
        def _on_mousewheel(event):
            if platform.system() == "Darwin":
                canvas.yview_scroll(int(-1 * event.delta), "units")
            else:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_linux_scroll_up(event):
            canvas.yview_scroll(-1, "units")

        def _on_linux_scroll_down(event):
            canvas.yview_scroll(1, "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", _on_linux_scroll_up)
        canvas.bind_all("<Button-5>", _on_linux_scroll_down)

    def _build_display(self, parent):
        frame = tk.Frame(parent, bg=COLORS["bg"])
        frame.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        frame.columnconfigure(0, weight=1)

        self.display = tk.Text(
            frame,
            height=4,
            font=self.font_display,
            bg=COLORS["display_bg"],
            fg=COLORS["display_fg"],
            relief="groove",
            bd=2,
            wrap="word",
            padx=12,
            pady=12,
            insertwidth=3,
        )
        self.display.grid(row=0, column=0, sticky="ew")

    def _build_toolbar(self, parent):
        frame = tk.Frame(parent, bg=COLORS["bg"])
        frame.grid(row=1, column=0, sticky="ew", padx=16, pady=4)

        actions = [
            ("⌫  Backspace", self._backspace, COLORS["action"], COLORS["action_hover"]),
            ("Clear All", self._clear, COLORS["action"], COLORS["action_hover"]),
            ("Space", self._space, COLORS["space"], COLORS["space_hover"]),
        ]
        for text, cmd, bg, hover_bg in actions:
            btn = tk.Button(
                frame,
                text=text,
                font=self.font_action,
                bg=bg,
                fg=COLORS["key_fg"],
                activebackground=hover_bg,
                activeforeground=COLORS["key_fg"],
                relief="flat",
                bd=0,
                padx=14,
                pady=6,
                cursor="hand2",
                command=cmd,
            )
            btn.pack(side="left", padx=4)
            self._add_hover(btn, bg, hover_bg)

    def _build_section(self, parent, title, chars, bg, hover_bg):
        row_idx = parent.grid_size()[1]
        section = tk.Frame(parent, bg=COLORS["bg"])
        section.grid(row=row_idx, column=0, sticky="ew", padx=16, pady=(12, 4))
        section.columnconfigure(0, weight=1)

        label = tk.Label(
            section,
            text=title,
            font=self.font_section,
            bg=COLORS["bg"],
            fg=COLORS["section_label"],
            anchor="w",
        )
        label.pack(anchor="w", pady=(0, 6))

        btn_frame = tk.Frame(section, bg=COLORS["bg"])
        btn_frame.pack(fill="x")

        for char, hint in chars:
            self._make_char_button(btn_frame, char, hint, bg, hover_bg)

    def _build_consonants(self, parent):
        row_idx = parent.grid_size()[1]
        section = tk.Frame(parent, bg=COLORS["bg"])
        section.grid(row=row_idx, column=0, sticky="ew", padx=16, pady=(12, 4))
        section.columnconfigure(0, weight=1)

        label = tk.Label(
            section,
            text="ව්‍යඤ්ජන  (Consonants)",
            font=self.font_section,
            bg=COLORS["bg"],
            fg=COLORS["section_label"],
            anchor="w",
        )
        label.pack(anchor="w", pady=(0, 6))

        for group in CONSONANTS:
            row_frame = tk.Frame(section, bg=COLORS["bg"])
            row_frame.pack(fill="x", pady=1)
            for char, hint in group:
                self._make_char_button(
                    row_frame, char, hint, COLORS["consonant"], COLORS["consonant_hover"]
                )

    def _make_char_button(self, parent, char, hint, bg, hover_bg):
        wrapper = tk.Frame(parent, bg=COLORS["bg"])
        wrapper.pack(side="left", padx=3, pady=3)

        btn = tk.Button(
            wrapper,
            text=char,
            font=self.font_button,
            bg=bg,
            fg=COLORS["key_fg"],
            activebackground=hover_bg,
            activeforeground=COLORS["key_fg"],
            width=3,
            height=1,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda c=char: self._insert(c),
        )
        btn.pack()

        tip = tk.Label(
            wrapper,
            text=hint,
            font=self.font_tooltip,
            bg=COLORS["bg"],
            fg=COLORS["tooltip_fg"],
        )
        tip.pack()

        self._add_hover(btn, bg, hover_bg)

    def _add_hover(self, btn, normal_bg, hover_bg):
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.configure(bg=normal_bg))

    def _insert(self, char):
        self.display.insert("insert", char)
        self.display.see("insert")
        self.display.focus_set()

    def _backspace(self):
        try:
            self.display.delete("insert-1c", "insert")
        except tk.TclError:
            pass
        self.display.focus_set()

    def _clear(self):
        self.display.delete("1.0", "end")
        self.display.focus_set()

    def _space(self):
        self._insert(" ")

    def _on_key(self, event):
        if event.keysym == "BackSpace" or event.keysym == "Delete":
            return
        if event.keysym == "Return":
            self._insert("\n")
            return "break"
        char = event.char
        if char in KEY_MAP:
            self._insert(KEY_MAP[char])
            return "break"

    def run(self):
        self.root.mainloop()
