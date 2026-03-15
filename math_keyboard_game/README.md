# Happy Number Keys (Raspberry Pi)

Gentle keyboard-only maths game for a Year 3 child.

## Features

- 10 soft levels from counting to easy `+` and `-`
- Keyboard-only play (`Left` `Right` `Up` `Down` `Enter` `Space`)
- No mouse required
- Big buttons, big numbers, one question per screen
- Friendly feedback and robot praise images
- Local progress save in `data/progress.json`
- Hidden parent reset area with `Escape`
- Offline play (no internet at runtime)

## Folder structure

```text
math_keyboard_game/
├── main.py
├── download_robohash_images.py
├── requirements.txt
├── README.md
├── assets/
│   ├── images/
│   │   └── robots/
│   │       ├── robot_1.ppm
│   │       ├── robot_2.ppm
│   │       ├── robot_3.ppm
│   │       └── robot_robohash_*.png (optional, generated)
│   └── sounds/
│       └── README.md
├── data/
│   └── progress.json
└── game/
    ├── __init__.py
    ├── app.py
    ├── constants.py
    ├── levels.py
    ├── progress.py
    └── widgets.py
```

## Run on Raspberry Pi

1. Open terminal in `math_keyboard_game`
2. Run:

```bash
python3 main.py
```

## Quick scripts

```bash
./install.sh
./build.sh
```

Optional RoboHash download during build:

```bash
./build.sh --with-robohash
```

## Raspberry Pi desktop app scripts

Build and install as a desktop game app:

```bash
./build_pi.sh
./install_pi.sh
```

Optional RoboHash download during Pi build:

```bash
./build_pi.sh --with-robohash
```

What `install_pi.sh` does:
- creates/uses `.venv`
- installs requirements
- creates desktop launcher files:
  - `~/.local/share/applications/happy-number-keys.desktop`
  - `~/Desktop/happy-number-keys.desktop`
- uses `logo.png` as app icon

If you use a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Keyboard controls

- `Left/Right/Up/Down` move focus
- `Enter` or `Space` choose
- `Escape` opens parent reset area (from Start/Levels) or backs out (in game)

## Replace praise robot images later

- Put local robot images in `assets/images/robots/`
- Supported now: `.png`, `.gif`, `.ppm`, `.pgm`
- The game uses local files only at runtime (offline)

### Use RoboHash images (one-time setup with internet)

```bash
python3 download_robohash_images.py
```

This creates files like `robot_robohash_1.png` in `assets/images/robots/`.
After this step, game runtime is still fully offline.

## Progress data

- Saved automatically to `data/progress.json`
- Parent can reset from hidden parent screen (`Escape` -> `Reset`)
