"""Main Tkinter app for the gentle keyboard maths game."""

from __future__ import annotations

import random
import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional

from .constants import (
    ALLOWED_KEYS,
    APP_TITLE,
    COLORS,
    LOGO_PATH,
    PRAISE_TEXTS,
    QUESTIONS_PER_LEVEL,
    ROBOT_DIR,
    TOTAL_LEVELS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from .levels import Question, generate_level_questions
from .progress import ProgressState, complete_level, load_progress, reset_progress, save_progress, stars_row
from .widgets import FocusButton, draw_objects, draw_robot_placeholder, load_robot_images


class BaseScreen:
    """Shared screen API."""

    def __init__(self, app: "MathGameApp"):
        self.app = app
        self.frame = tk.Frame(app.root, bg=COLORS["bg"])

    def show(self) -> None:
        self.frame.pack(fill="both", expand=True)

    def hide(self) -> None:
        self.frame.pack_forget()

    def on_key(self, key: str) -> None:
        return


class StartScreen(BaseScreen):
    def __init__(self, app: "MathGameApp"):
        super().__init__(app)

        title = tk.Label(
            self.frame,
            text=APP_TITLE,
            bg=COLORS["bg"],
            fg=COLORS["title"],
            font=("Helvetica", 54, "bold"),
        )
        title.pack(pady=34)

        robot_area = tk.Canvas(self.frame, width=260, height=200, bg=COLORS["bg"], highlightthickness=0)
        robot_area.pack()
        app.draw_random_robot(robot_area, x=50, y=20)

        self.play_button = FocusButton(self.frame, "PLAY", width=300, height=130)
        self.play_button.pack(pady=30)
        self.play_button.set_focused(True)

        hint = tk.Label(
            self.frame,
            text="Arrows  Enter  Space",
            bg=COLORS["bg"],
            fg=COLORS["subtle"],
            font=("Helvetica", 22, "bold"),
        )
        hint.pack(pady=8)

    def on_key(self, key: str) -> None:
        if key in {"Return", "space"}:
            self.app.show_level_select()
        elif key == "Escape":
            self.app.show_parent_settings(back_target="start")


class LevelSelectScreen(BaseScreen):
    def __init__(self, app: "MathGameApp"):
        super().__init__(app)
        self.focus_index = 0
        self.level_buttons: List[FocusButton] = []
        self.star_labels: List[tk.Label] = []
        self.message_var = tk.StringVar(value="")

        top = tk.Label(
            self.frame,
            text="LEVELS",
            bg=COLORS["bg"],
            fg=COLORS["title"],
            font=("Helvetica", 46, "bold"),
        )
        top.pack(pady=20)

        self.grid = tk.Frame(self.frame, bg=COLORS["bg"])
        self.grid.pack()

        for idx in range(TOTAL_LEVELS):
            cell = tk.Frame(self.grid, bg=COLORS["bg"])
            row = idx // 5
            col = idx % 5
            cell.grid(row=row * 2, column=col, padx=14, pady=8)
            button = FocusButton(cell, str(idx + 1), width=160, height=100)
            button.pack()
            self.level_buttons.append(button)
            stars = tk.Label(cell, text="", bg=COLORS["bg"], fg=COLORS["star_on"], font=("Helvetica", 18, "bold"))
            stars.pack(pady=2)
            self.star_labels.append(stars)

        note = tk.Label(self.frame, textvariable=self.message_var, bg=COLORS["bg"], fg=COLORS["subtle"], font=("Helvetica", 20, "bold"))
        note.pack(pady=14)

    def refresh(self) -> None:
        state = self.app.progress
        self.message_var.set("")
        for idx, button in enumerate(self.level_buttons, start=1):
            locked = idx > state.unlocked_level
            button.set_locked(locked)
            stars = state.star_for(idx)
            self.star_labels[idx - 1].config(text=("*" * stars))
        self.focus_index = min(self.focus_index, TOTAL_LEVELS - 1)
        self._update_focus()

    def _update_focus(self) -> None:
        for idx, button in enumerate(self.level_buttons):
            button.set_focused(idx == self.focus_index)

    def on_key(self, key: str) -> None:
        row = self.focus_index // 5
        col = self.focus_index % 5

        if key == "Left":
            col = max(0, col - 1)
        elif key == "Right":
            col = min(4, col + 1)
        elif key == "Up":
            row = max(0, row - 1)
        elif key == "Down":
            row = min(1, row + 1)
        elif key in {"Return", "space"}:
            level = self.focus_index + 1
            if level <= self.app.progress.unlocked_level:
                self.app.start_level(level)
            else:
                self.message_var.set("Locked")
                self.app.play_soft_sound()
            return
        elif key == "Escape":
            self.app.show_parent_settings(back_target="levels")
            return
        else:
            return

        self.focus_index = row * 5 + col
        self._update_focus()


class QuizScreen(BaseScreen):
    def __init__(self, app: "MathGameApp", level: int):
        super().__init__(app)
        self.level = level
        self.questions = generate_level_questions(level, random.Random())
        self.current_index = 0
        self.choice_index = 0
        self.first_try_correct = 0
        self.first_try = True
        self.lock_input = False
        self.current_question: Optional[Question] = None

        self.header_var = tk.StringVar(value="")
        self.feedback_var = tk.StringVar(value="")

        header = tk.Label(
            self.frame,
            textvariable=self.header_var,
            bg=COLORS["bg"],
            fg=COLORS["title"],
            font=("Helvetica", 34, "bold"),
        )
        header.pack(pady=12)

        self.canvas = tk.Canvas(self.frame, width=980, height=340, bg=COLORS["panel"], highlightthickness=0)
        self.canvas.pack(pady=4)

        self.expression_var = tk.StringVar(value="")
        expression = tk.Label(
            self.frame,
            textvariable=self.expression_var,
            bg=COLORS["bg"],
            fg=COLORS["title"],
            font=("Helvetica", 48, "bold"),
        )
        expression.pack(pady=12)

        choices_wrap = tk.Frame(self.frame, bg=COLORS["bg"])
        choices_wrap.pack(pady=8)
        self.choice_buttons: List[FocusButton] = []
        for _ in range(3):
            btn = FocusButton(choices_wrap, "0", width=230, height=110)
            btn.pack(side="left", padx=16)
            self.choice_buttons.append(btn)

        self.feedback_label = tk.Label(
            self.frame,
            textvariable=self.feedback_var,
            bg=COLORS["bg"],
            fg=COLORS["subtle"],
            font=("Helvetica", 28, "bold"),
        )
        self.feedback_label.pack(pady=10)

        self.robot_canvas = tk.Canvas(self.frame, width=160, height=160, bg=COLORS["bg"], highlightthickness=0)
        self.robot_canvas.pack(pady=4)

        self.load_question()

    def load_question(self) -> None:
        self.lock_input = False
        self.current_question = self.questions[self.current_index]
        q = self.current_question
        self.first_try = True
        self.choice_index = 0
        self.feedback_var.set("")
        self.header_var.set(f"L{self.level}   {self.current_index + 1}/{QUESTIONS_PER_LEVEL}")

        for idx, value in enumerate(q.choices):
            self.choice_buttons[idx].set_text(str(value))
            self.choice_buttons[idx].set_focused(idx == self.choice_index)

        self._draw_question(q)

    def _draw_question(self, question: Question) -> None:
        self.canvas.delete("all")
        self.robot_canvas.delete("all")
        self.app.draw_random_robot(self.robot_canvas, 20, 20)

        if question.show_pictures:
            if question.operator in {"+", "-"}:
                draw_objects(self.canvas, question.object_type, question.left, 90, 70, width=300)
                draw_objects(self.canvas, question.object_type, question.right, 560, 70, width=300)
                self.canvas.create_text(490, 130, text=question.operator, font=("Helvetica", 64, "bold"), fill=COLORS["title"])
            else:
                draw_objects(self.canvas, question.object_type, question.left, 310, 70, width=360)

        if question.operator in {"+", "-"}:
            self.expression_var.set(f"{question.left} {question.operator} {question.right} = ?")
        elif question.prompt == "=":
            self.expression_var.set(f"{question.left} = ?")
        elif question.prompt == "?":
            self.expression_var.set("?")
        else:
            self.expression_var.set(question.prompt)

    def _set_choice_focus(self) -> None:
        for idx, button in enumerate(self.choice_buttons):
            button.set_focused(idx == self.choice_index)

    def _next_question(self) -> None:
        self.current_index += 1
        if self.current_index >= QUESTIONS_PER_LEVEL:
            if self.first_try_correct >= 5:
                stars = 3
            elif self.first_try_correct >= 3:
                stars = 2
            else:
                stars = 1
            self.app.finish_level(self.level, stars)
            return
        self.load_question()

    def on_key(self, key: str) -> None:
        if self.lock_input:
            return

        if key in {"Left", "Up"}:
            self.choice_index = (self.choice_index - 1) % len(self.choice_buttons)
            self._set_choice_focus()
            return
        if key in {"Right", "Down"}:
            self.choice_index = (self.choice_index + 1) % len(self.choice_buttons)
            self._set_choice_focus()
            return
        if key == "Escape":
            self.app.show_level_select()
            return
        if key not in {"Return", "space"}:
            return

        question = self.current_question
        if question is None:
            return

        selected = question.choices[self.choice_index]
        if selected == question.correct:
            if self.first_try:
                self.first_try_correct += 1
            self.feedback_var.set(random.choice(PRAISE_TEXTS))
            self.feedback_label.config(fg=COLORS["ok"])
            self.app.play_happy_sound()
            self.lock_input = True
            self.app.root.after(700, self._next_question)
        else:
            self.feedback_var.set("Try again")
            self.feedback_label.config(fg=COLORS["subtle"])
            self.app.play_soft_sound()
            self.first_try = False


class LevelCompleteScreen(BaseScreen):
    def __init__(self, app: "MathGameApp", level: int, stars: int):
        super().__init__(app)
        self.level = level
        self.stars = stars
        self.focus_index = 0
        self.options: List[FocusButton] = []

        title = tk.Label(
            self.frame,
            text=random.choice(PRAISE_TEXTS),
            bg=COLORS["bg"],
            fg=COLORS["title"],
            font=("Helvetica", 52, "bold"),
        )
        title.pack(pady=28)

        stars_str = "".join("*" if on else "-" for on in stars_row(stars))
        star_label = tk.Label(self.frame, text=stars_str, bg=COLORS["bg"], fg=COLORS["star_on"], font=("Helvetica", 56, "bold"))
        star_label.pack()

        robot = tk.Canvas(self.frame, width=220, height=180, bg=COLORS["bg"], highlightthickness=0)
        robot.pack(pady=12)
        app.draw_random_robot(robot, 30, 20)

        wrap = tk.Frame(self.frame, bg=COLORS["bg"])
        wrap.pack(pady=12)

        for text in ["Next", "Again", "Levels"]:
            btn = FocusButton(wrap, text, width=220, height=100)
            btn.pack(side="left", padx=12)
            self.options.append(btn)
        self._update_focus()

    def _update_focus(self) -> None:
        for idx, button in enumerate(self.options):
            button.set_focused(idx == self.focus_index)

    def on_key(self, key: str) -> None:
        if key in {"Left", "Up"}:
            self.focus_index = (self.focus_index - 1) % len(self.options)
            self._update_focus()
        elif key in {"Right", "Down"}:
            self.focus_index = (self.focus_index + 1) % len(self.options)
            self._update_focus()
        elif key == "Escape":
            self.app.show_level_select()
        elif key in {"Return", "space"}:
            if self.focus_index == 0:
                if self.level < TOTAL_LEVELS:
                    self.app.start_level(self.level + 1)
                else:
                    self.app.show_level_select()
            elif self.focus_index == 1:
                self.app.start_level(self.level)
            else:
                self.app.show_level_select()


class ParentSettingsScreen(BaseScreen):
    """Small hidden screen for parent reset only."""

    def __init__(self, app: "MathGameApp", back_target: str):
        super().__init__(app)
        self.back_target = back_target
        self.focus_index = 1
        self.options: List[FocusButton] = []
        self.message_var = tk.StringVar(value="")

        title = tk.Label(
            self.frame,
            text="Parent",
            bg=COLORS["bg"],
            fg=COLORS["title"],
            font=("Helvetica", 38, "bold"),
        )
        title.pack(pady=32)

        note = tk.Label(
            self.frame,
            text="Reset child progress?",
            bg=COLORS["bg"],
            fg=COLORS["subtle"],
            font=("Helvetica", 24, "bold"),
        )
        note.pack(pady=8)

        row = tk.Frame(self.frame, bg=COLORS["bg"])
        row.pack(pady=18)
        for text in ["Reset", "Back"]:
            btn = FocusButton(row, text, width=240, height=110)
            btn.pack(side="left", padx=18)
            self.options.append(btn)
        self._update_focus()

        msg = tk.Label(
            self.frame,
            textvariable=self.message_var,
            bg=COLORS["bg"],
            fg=COLORS["subtle"],
            font=("Helvetica", 20, "bold"),
        )
        msg.pack(pady=10)

    def _update_focus(self) -> None:
        for idx, button in enumerate(self.options):
            button.set_focused(idx == self.focus_index)

    def _go_back(self) -> None:
        if self.back_target == "start":
            self.app.show_start()
        else:
            self.app.show_level_select()

    def on_key(self, key: str) -> None:
        if key in {"Left", "Up"}:
            self.focus_index = (self.focus_index - 1) % len(self.options)
            self._update_focus()
        elif key in {"Right", "Down"}:
            self.focus_index = (self.focus_index + 1) % len(self.options)
            self._update_focus()
        elif key == "Escape":
            self._go_back()
        elif key in {"Return", "space"}:
            if self.focus_index == 0:
                self.app.progress = reset_progress()
                save_progress(self.app.progress)
                self.message_var.set("Progress reset")
                self.app.play_soft_sound()
                self.app.root.after(600, self._go_back)
            else:
                self._go_back()


class MathGameApp:
    """App shell that swaps keyboard-only screens."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self._app_logo: Optional[tk.PhotoImage] = None
        self._set_app_logo()
        self.root.configure(bg=COLORS["bg"])
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(900, 600)
        self.root.bind("<Key>", self._on_key)
        self.root.option_add("*Font", "Helvetica 20")

        style = ttk.Style()
        style.theme_use("clam")

        self.progress: ProgressState = load_progress()
        self.robot_images = load_robot_images(ROBOT_DIR)

        self.screen: Optional[BaseScreen] = None
        self.show_start()

    def _set_app_logo(self) -> None:
        """Set the window icon from local logo file when available."""
        if not LOGO_PATH.exists():
            return
        try:
            self._app_logo = tk.PhotoImage(file=str(LOGO_PATH))
            self.root.iconphoto(True, self._app_logo)
        except tk.TclError:
            # Keep running with default icon if format is unsupported.
            self._app_logo = None

    def _set_screen(self, screen: BaseScreen) -> None:
        if self.screen is not None:
            self.screen.hide()
        self.screen = screen
        self.screen.show()

    def _on_key(self, event: tk.Event) -> None:
        key = event.keysym
        if key not in ALLOWED_KEYS:
            return
        if self.screen:
            self.screen.on_key(key)

    def show_start(self) -> None:
        self._set_screen(StartScreen(self))

    def show_level_select(self) -> None:
        screen = LevelSelectScreen(self)
        screen.refresh()
        self._set_screen(screen)

    def show_parent_settings(self, back_target: str) -> None:
        self._set_screen(ParentSettingsScreen(self, back_target=back_target))

    def start_level(self, level: int) -> None:
        self._set_screen(QuizScreen(self, level))

    def finish_level(self, level: int, stars: int) -> None:
        self.progress = complete_level(self.progress, level, stars)
        save_progress(self.progress)
        self._set_screen(LevelCompleteScreen(self, level=level, stars=stars))

    def draw_random_robot(self, canvas: tk.Canvas, x: int, y: int) -> None:
        if self.robot_images:
            image = random.choice(self.robot_images)
            canvas.image = image
            canvas.create_image(x, y, image=image, anchor="nw")
            return
        draw_robot_placeholder(canvas, x, y)

    def play_happy_sound(self) -> None:
        # Simple local cue that works offline in Tkinter.
        self.root.bell()
        self.root.after(80, self.root.bell)

    def play_soft_sound(self) -> None:
        self.root.bell()

    def run(self) -> None:
        self.root.mainloop()
