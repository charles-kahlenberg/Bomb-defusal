import pygame
import sys
from display_utils import create_fullscreen_display


try:
    from bomb_configs import RPi, component_button_state
except ImportError:
    RPi = False
    component_button_state = None


SCREEN_W = 1024
SCREEN_H = 576

DIED_TEXT = "YOU DIED"
QUIT_TEXT_RPI = "Press Button to Quit"
QUIT_TEXT_PC = "Press Enter to Quit"

DIED_COLOR = (180, 0, 0)
QUIT_COLOR = (150, 150, 150)

DIED_FONT_SIZE = 80
QUIT_FONT_SIZE = 24

DIED_FADE_MS = 2500
WAIT_BEFORE_QUIT_TEXT_MS = 5000
QUIT_TEXT_FADE_MS = 2000


def draw_centered_text(surface, font, text, color, alpha, center_pos):
    text_surface = font.render(text, True, color).convert_alpha()
    text_surface.set_alpha(alpha)
    text_rect = text_surface.get_rect(center=center_pos)
    surface.blit(text_surface, text_rect)


def main(screen=None, clock=None):
    if not pygame.get_init():
        pygame.init()

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    created_display = screen is None
    if screen is None:
        screen = create_fullscreen_display("Defuse the Bomb")

    if clock is None:
        clock = pygame.time.Clock()

    pygame.display.set_caption("Defuse the Bomb")

    died_font = pygame.font.SysFont("serif", DIED_FONT_SIZE, bold=True)
    quit_font = pygame.font.SysFont("serif", QUIT_FONT_SIZE)

    start_time = pygame.time.get_ticks()
    prev_btn = False
    running = True

    while running:
        now = pygame.time.get_ticks()
        elapsed = now - start_time

        quit_text_ready = elapsed >= WAIT_BEFORE_QUIT_TEXT_MS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if quit_text_ready and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not RPi:
                    pygame.quit()
                    sys.exit()

        if quit_text_ready and RPi and component_button_state is not None:
            btn = component_button_state.value

            if btn and not prev_btn:
                pygame.quit()
                sys.exit()

            prev_btn = btn

        died_alpha = min(255, int((elapsed / DIED_FADE_MS) * 255))

        if quit_text_ready:
            quit_elapsed = elapsed - WAIT_BEFORE_QUIT_TEXT_MS
            quit_alpha = min(255, int((quit_elapsed / QUIT_TEXT_FADE_MS) * 255))
        else:
            quit_alpha = 0

        screen.fill((0, 0, 0))

        draw_centered_text(
            screen,
            died_font,
            DIED_TEXT,
            DIED_COLOR,
            died_alpha,
            (screen.get_width() // 2, screen.get_height() // 2 - 40)
        )

        quit_text = QUIT_TEXT_RPI if RPi else QUIT_TEXT_PC
        draw_centered_text(
            screen,
            quit_font,
            quit_text,
            QUIT_COLOR,
            quit_alpha,
            (screen.get_width() // 2, screen.get_height() // 2 + 55)
        )

        pygame.display.flip()
        clock.tick(60)

    if created_display:
        pygame.quit()


if __name__ == "__main__":
    main()