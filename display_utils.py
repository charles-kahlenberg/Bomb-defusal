"""
display_utils.py

Shared display helpers for the Bomb Defusal game.

Responsibilities:
- Defines the game's logical design resolution.
- Creates the fullscreen Pygame display.
- Uses pygame.SCALED so the game keeps 1024x576 coordinates on different screens.

Important constants:
- DESIGN_W / DESIGN_H: Logical game resolution.
- DESIGN_SIZE: Tuple used for display creation.
- FULLSCREEN_FLAGS: Pygame flags used for fullscreen scaling.

Notes:
- Other modules should use create_fullscreen_display() instead of creating their own
  display directly, so all screens share the same resolution behavior.
"""

# display_utils.py
import pygame

DESIGN_W = 1024
DESIGN_H = 576
DESIGN_SIZE = (DESIGN_W, DESIGN_H)

FULLSCREEN_FLAGS = pygame.FULLSCREEN | pygame.SCALED


def create_fullscreen_display(caption=None):
    """
    Creates a fullscreen Pygame display while preserving the game's
    1024x576 logical coordinate system.

    pygame.SCALED scales the 1024x576 game surface to the actual monitor
    resolution, so existing coordinates keep their positions.
    """
    screen = pygame.display.set_mode(DESIGN_SIZE, FULLSCREEN_FLAGS)

    if caption:
        pygame.display.set_caption(caption)

    return screen