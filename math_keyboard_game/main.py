"""Entry point for the keyboard-only maths game."""

from game.app import MathGameApp


def main() -> None:
    app = MathGameApp()
    app.run()


if __name__ == "__main__":
    main()
