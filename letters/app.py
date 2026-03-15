import tkinter as tk

COLORS = {
    "bg": "#F7F6F3",
    "dot": "#C5C2BC",
    "display_fg": "#5645ED",
}


class LettersApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Letters - English Typing")
        self.root.configure(bg=COLORS["bg"])

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_w}x{screen_h}+0+0")

        try:
            self.root.state("zoomed")
        except tk.TclError:
            pass

        self.font_display = ("TkDefaultFont", 48)
        self.margin = 48
        self.content = ""
        self.cursor_on = True
        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.background = tk.Canvas(
            self.root,
            bg=COLORS["bg"],
            highlightthickness=0,
            bd=0,
        )
        self.background.grid(row=0, column=0, sticky="nsew")

        width = max(200, self.root.winfo_screenwidth() - (self.margin * 2))
        self.text_item = self.background.create_text(
            self.margin,
            self.margin,
            anchor="nw",
            text="",
            fill=COLORS["display_fg"],
            font=self.font_display,
            width=width,
        )

        # Hidden focus widget to receive keyboard events reliably.
        self.input_bridge = tk.Text(
            self.background,
            bg=COLORS["bg"],
            fg=COLORS["bg"],
            width=1,
            height=1,
            relief="flat",
            bd=0,
            highlightthickness=0,
        )
        self.input_bridge.place(x=0, y=0, width=1, height=1)
        self.input_bridge.bind("<Key>", self._on_key)

        self.background.bind("<Configure>", self._on_resize)
        self.background.bind("<Button-1>", self._focus_input)
        self._focus_input(None)
        self._refresh_view()
        self._blink_cursor()

    def _on_resize(self, event):
        self._draw_notebook_dots(event.width, event.height)
        width = max(200, event.width - (self.margin * 2))
        self.background.itemconfigure(self.text_item, width=width)
        self._refresh_view()

    def _draw_notebook_dots(self, width, height):
        self.background.delete("dot")
        spacing = 24
        radius = 1
        for y in range(spacing, height, spacing):
            for x in range(spacing, width, spacing):
                self.background.create_oval(
                    x - radius,
                    y - radius,
                    x + radius,
                    y + radius,
                    fill=COLORS["dot"],
                    outline="",
                    tags="dot",
                )

    def _focus_input(self, _event):
        self.input_bridge.focus_set()

    def _refresh_view(self):
        display_text = f"{self.content}|" if self.cursor_on else self.content
        self.background.itemconfigure(self.text_item, text=display_text)

    def _blink_cursor(self):
        self.cursor_on = not self.cursor_on
        self._refresh_view()
        self.root.after(500, self._blink_cursor)

    def _on_key(self, event):
        if event.keysym in ("BackSpace", "Delete"):
            if self.content:
                self.content = self.content[:-1]
                self._refresh_view()
            return "break"

        if event.keysym == "Return":
            self.content += "\n"
            self._refresh_view()
            return "break"

        if event.keysym == "space":
            self.content += " "
            self._refresh_view()
            return "break"

        if event.keysym == "Escape":
            return

        # Accept letters, numbers, punctuation, and symbols.
        char = event.char
        if char and char.isprintable():
            self.content += char
            self._refresh_view()
            return "break"

    def run(self):
        self.root.mainloop()
