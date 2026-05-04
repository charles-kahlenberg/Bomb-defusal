# Bomb Defusal Game

A multi-phase bomb defusal game built with Python and Pygame. The project supports both a graphical user interface (GUI) and physical hardware integration via Raspberry Pi (RPi).

## Overview

The game challenges players to defuse a bomb by completing a series of minigames (phases). It includes:
- **Intro/Story sequences**: Narrative elements between games.
- **Vent/Fling Minigame**: A physics-based or navigation challenge.
- **Wires GUI**: A wire-connection puzzle.
- **Safe Game/Keypad**: Numeric code entry.
- **Switch Game**: Toggle switch puzzles.

The project is designed to be extensible, allowing for new phases to be added through `bomb_phases.py` and configured in `bomb_configs.py`.

## Tech Stack

- **Language**: Python 3
- **Graphics/Audio**: [Pygame](https://www.pygame.org/)
- **Math/Logic**: NumPy
- **Hardware Integration**: Adafruit CircuitPython libraries (for Raspberry Pi mode)

## Requirements

### Software
- Python 3.x
- Pygame
- NumPy
- (Optional) Adafruit libraries for RPi: `adafruit-circuitpython-ht16k33`, `adafruit-circuitpython-matrixkeypad`

### Hardware (Optional)
If running in RPi mode (`RPi = True` in `bomb_configs.py`):
- Raspberry Pi
- 7-segment display (HT16K33)
- Matrix Keypad
- Jumper wires
- Pushbuttons and RGB LEDs
- Toggle switches

## Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/charl/Bomb-defusal.git
   cd Bomb-defusal
   ```

2. **Install dependencies**:
   ```bash
   pip install pygame numpy
   # If using RPi components:
   # pip install adafruit-circuitpython-ht16k33 adafruit-circuitpython-matrixkeypad
   ```

3. **Configuration**:
   Open `bomb_configs.py` to adjust settings:
   - Set `RPi = True` if using physical hardware, or `RPi = False` for GUI-only mode.
   - Adjust `NUM_STRIKES`, `COUNTDOWN`, and `DEBUG` mode.

## Running the Game

The main entry point is `bomb.py`:

```bash
python bomb.py
```

### Other Scripts
You can also run individual minigames for testing:
- `python "Wires GUI.py"`
- `python "Safe Game.py"`
- `python SwitchG.py`

## Project Structure

- `bomb.py`: The main game controller and orchestrator.
- `bomb_configs.py`: Configuration constants and hardware pin mappings.
- `bomb_phases.py`: Logic for the various bomb phases and hardware threads.
- `character_overlay.py`: Handles drawing character animations on the screen.
- `images/` & `img_keys/`: Asset directories containing sprites, backgrounds, and sound effects.
- `og code/`: Backup or original versions of core scripts.

## Environment Variables

No specific environment variables are required, as most configuration is handled in `bomb_configs.py`.

## Tests

- TODO: Implement formal unit tests or integration tests.
- Manual testing can be performed by running individual minigame scripts.

## License

- TODO: Specify license (e.g., MIT, GPL). No license file found in repository.
