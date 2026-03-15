try:
    # Works when running from repo root: python -m letters.main
    from letters.app import LettersApp
except ModuleNotFoundError:
    # Works when running inside letters/: python main.py
    from app import LettersApp


def main():
    app = LettersApp()
    app.run()


if __name__ == "__main__":
    main()
