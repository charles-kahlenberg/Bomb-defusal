import pygame

from character_overlay import draw_character
from display_utils import create_fullscreen_display

try:
    from bomb_configs import RPi, component_button_state
except ImportError:
    RPi = False
    component_button_state = None


TEXTBOX_X = 277
TEXTBOX_Y = 42
TEXTBOX_WIDTH = 471
TEXTBOX_HEIGHT = 132
TEXTBOX_ALPHA = 180
TEXT_PADDING_X = 18
TEXT_PADDING_Y = 16
PROMPT_OFFSET_Y = 45

VENT_PANEL_X = 300
VENT_PANEL_Y = 232
VENT_PANEL_WIDTH = 425
VENT_PANEL_HEIGHT = 299


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

    bg = pygame.image.load("img_keys/base.png").convert()
    bg = pygame.transform.scale(bg, screen.get_size())

    screen_width, screen_height = screen.get_size()

    vent_panel = pygame.image.load("img_keys/vent.png").convert_alpha()
    vent_panel = pygame.transform.smoothscale(
        vent_panel,
        (VENT_PANEL_WIDTH, VENT_PANEL_HEIGHT)
    )

    rect_pos = pygame.image.load('img_keys/DoorM.png').convert_alpha()
    rect_pos = pygame.transform.scale(rect_pos, screen.get_size())
    rect_surf = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    rect_surf.fill((0, 0, 0, 255))

    messages = [
        "You have put our name to question for too long.....",
        "For this you shall die!",
        "There's a bomb strapped to your chair!",
        "MWAJAHAHAHAHAHAHA!",
        "Good luck getting out of this!",
    ]

    activem = 0
    message = messages[activem]

    font = pygame.font.Font("img_keys/Baskic8.otf", 16)
    counter = 0
    done = False
    final_message_done_time = None
    pygame.mixer.music.load("intro.mp3")
    pygame.mixer.music.set_volume(10.00)
    talking = pygame.mixer.Channel
    started = False
    notplayed = True

    dpos = rect_pos.get_rect()
    dpos.center = (510, 280)
    rect_color = (0, 0, 0)
    count = 0
    speed = 1
    tcounter = 0
    
    doorup = False
    pon = False
    prev_btn = False
    sswa = False

    running = True

    while running:
        now = pygame.time.get_ticks()

        def advance_message():
            nonlocal activem, done, final_message_done_time, message, counter, running

            if done:
                if activem < len(messages) - 1:
                    activem += 1
                    done = False
                    final_message_done_time = None
                    message = messages[activem]
                    counter = 0
                else:
                    running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not RPi:
                    advance_message()

        if RPi and component_button_state is not None and doorup:
            btn = component_button_state.value

            if btn and not prev_btn:
                advance_message()

            prev_btn = btn

        screen.fill((255, 255, 255))

        screen.blit(bg, (0, 0))
        draw_character(screen)
        screen.blit(vent_panel, (VENT_PANEL_X, VENT_PANEL_Y))
        screen.blit(rect_surf, (0, 0))
        screen.blit(rect_pos, dpos)

        if dpos.y > -600:
            dpos.y -= 3
            started = True
        else:
            doorup = True

        if doorup:
            count += 1
            if sswa != True:
                sswitch = pygame.mixer.Sound("img_keys/Switch.mp3")
                pygame.mixer.Sound.set_volume(sswitch, 1.0)
                sswitch.play()
                sswa = True
            if count > 55:
                rect_surf.fill((0, 0, 0, 0))
            if count > 125:
                pon = True

        if started and notplayed:
            notplayed = False
            pygame.mixer.music.play()
        c1t = pygame.mixer.Sound("img_keys/C1Talking.mp3")
        pygame.mixer.Sound.set_volume(c1t, 1.0)

        if pon:
            if counter < speed * len(message):
                counter += 1
                if tcounter == 0:
                    c1t.play()
                tcounter += 1
                if tcounter > 20:
                    tcounter = 0
            else:
                done = True
                tcounter = 0
                pygame.mixer.stop()

                if activem == len(messages) - 1:
                    if final_message_done_time is None:
                        final_message_done_time = now
                    elif now - final_message_done_time >= 3000:
                        running = False

            text_box = pygame.Surface((TEXTBOX_WIDTH, TEXTBOX_HEIGHT), pygame.SRCALPHA)
            text_box.fill((0, 0, 0, TEXTBOX_ALPHA))
            screen.blit(text_box, (TEXTBOX_X, TEXTBOX_Y))

            border_rect = pygame.Rect(TEXTBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
            pygame.draw.rect(screen, (255, 255, 255), border_rect, 2)

            snip = font.render(message[0:counter // speed], True, "white")
            screen.blit(snip, (TEXTBOX_X + TEXT_PADDING_X, TEXTBOX_Y + TEXT_PADDING_Y))

            if done and activem < len(messages) - 1:
                prompt_text = "Press Button" if RPi else "Press Enter"
                prompt = font.render(prompt_text, True, (180, 180, 180))
                screen.blit(prompt, (TEXTBOX_X + TEXT_PADDING_X, TEXTBOX_Y + PROMPT_OFFSET_Y))

        pygame.display.flip()
        clock.tick(24)

    if created_display:
        pygame.quit()

    return True

if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)