import pygame
import threading
import time

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


class IntroState:
    def __init__(self, screen_size, messages):
        self.lock = threading.Lock()
        self.running = True
        self.result = True

        self.screen_width, self.screen_height = screen_size
        self.messages = messages
        self.active_message = 0
        self.message = messages[0]
        self.counter = 0
        self.speed = 1
        self.done = False
        self.final_message_done_time = None

        self.door_y = 0
        self.door_center_x = 510
        self.door_center_y = 280
        self.door_started = False
        self.door_up = False
        self.door_count = 0
        self.overlay_alpha = 255
        self.panel_on = False
        self.switch_sound_played = False

        self.music_started = False
        self.music_played = False

        self.text_sound_counter = 0
        self.advance_requested = False


class DoorThread(threading.Thread):
    def __init__(self, state):
        super().__init__(daemon=True)
        self.state = state

    def run(self):
        while True:
            with self.state.lock:
                if not self.state.running:
                    break

                if self.state.door_y > -600:
                    self.state.door_y -= 3
                    self.state.door_started = True
                else:
                    self.state.door_up = True

                if self.state.door_up:
                    self.state.door_count += 1

                    if self.state.door_count > 55:
                        self.state.overlay_alpha = 0

                    if self.state.door_count > 125:
                        self.state.panel_on = True

            time.sleep(1 / 24)


class CharacterThread(threading.Thread):
    def __init__(self, state):
        super().__init__(daemon=True)
        self.state = state

    def run(self):
        while True:
            with self.state.lock:
                if not self.state.running:
                    break
                # Character animation itself is handled by character_overlay using pygame ticks.
                # This thread exists to keep character timing/state separate if more animation
                # state is added later.
            time.sleep(1 / 24)


class TextThread(threading.Thread):
    def __init__(self, state):
        super().__init__(daemon=True)
        self.state = state

    def run(self):
        while True:
            with self.state.lock:
                if not self.state.running:
                    break

                now = pygame.time.get_ticks()

                if self.state.advance_requested and self.state.done:
                    self.state.advance_requested = False

                    if self.state.active_message < len(self.state.messages) - 1:
                        self.state.active_message += 1
                        self.state.message = self.state.messages[self.state.active_message]
                        self.state.counter = 0
                        self.state.done = False
                        self.state.final_message_done_time = None
                    else:
                        self.state.running = False
                        break

                if self.state.panel_on:
                    if self.state.counter < self.state.speed * len(self.state.message):
                        self.state.counter += 1
                        self.state.text_sound_counter += 1

                        if self.state.text_sound_counter > 20:
                            self.state.text_sound_counter = 0
                    else:
                        self.state.done = True
                        self.state.text_sound_counter = 0

                        if self.state.active_message == len(self.state.messages) - 1:
                            if self.state.final_message_done_time is None:
                                self.state.final_message_done_time = now
                            elif now - self.state.final_message_done_time >= 3000:
                                self.state.running = False
                                break

            time.sleep(1 / 24)


class AudioThread(threading.Thread):
    def __init__(self, state):
        super().__init__(daemon=True)
        self.state = state
        self.switch_sound = pygame.mixer.Sound("img_keys/Switch.mp3")
        self.talking_sound = pygame.mixer.Sound("img_keys/C1Talking.mp3")
        pygame.mixer.Sound.set_volume(self.switch_sound, 1.0)
        pygame.mixer.Sound.set_volume(self.talking_sound, 1.0)

    def run(self):
        while True:
            play_switch = False
            play_talking = False
            stop_talking = False
            play_music = False

            with self.state.lock:
                if not self.state.running:
                    break

                if self.state.door_started and not self.state.music_played:
                    self.state.music_played = True
                    play_music = True

                if self.state.door_up and not self.state.switch_sound_played:
                    self.state.switch_sound_played = True
                    play_switch = True

                if self.state.panel_on and not self.state.done:
                    if self.state.text_sound_counter == 1:
                        play_talking = True

                if self.state.done:
                    stop_talking = True

            if play_music:
                pygame.mixer.music.play()

            if play_switch:
                self.switch_sound.play()

            if play_talking:
                self.talking_sound.play()

            if stop_talking:
                pygame.mixer.stop()

            time.sleep(1 / 24)


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

    door_image = pygame.image.load("img_keys/DoorM.png").convert_alpha()
    door_image = pygame.transform.scale(door_image, screen.get_size())

    font = pygame.font.Font("img_keys/Baskic8.otf", 16)

    pygame.mixer.music.load("intro.mp3")
    pygame.mixer.music.set_volume(10.00)

    messages = [
        "You have put our name to question for too long.....",
        "For this you shall die!",
        "There's a bomb strapped to your chair!",
        "MWAJAHAHAHAHAHAHA!",
        "Good luck getting out of this!",
    ]

    state = IntroState(screen.get_size(), messages)

    threads = [
        DoorThread(state),
        CharacterThread(state),
        TextThread(state),
        AudioThread(state),
    ]

    for thread in threads:
        thread.start()

    prev_btn = False

    while True:
        with state.lock:
            running = state.running
            door_up = state.door_up

        if not running:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with state.lock:
                    state.running = False
                    state.result = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not RPi:
                    with state.lock:
                        state.advance_requested = True

        if RPi and component_button_state is not None and door_up:
            btn = component_button_state.value

            if btn and not prev_btn:
                with state.lock:
                    state.advance_requested = True

            prev_btn = btn

        with state.lock:
            door_y = state.door_y
            overlay_alpha = state.overlay_alpha
            panel_on = state.panel_on
            typed_text = state.message[0:state.counter // state.speed]
            done = state.done
            active_message = state.active_message
            result = state.result

        screen.fill((255, 255, 255))
        screen.blit(bg, (0, 0))
        draw_character(screen, intro_mode=True)
        screen.blit(vent_panel, (VENT_PANEL_X, VENT_PANEL_Y))

        if overlay_alpha > 0:
            rect_surf = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            rect_surf.fill((0, 0, 0, overlay_alpha))
            screen.blit(rect_surf, (0, 0))

        door_rect = door_image.get_rect()
        door_rect.center = (510, 280)
        door_rect.y = door_y
        screen.blit(door_image, door_rect)

        if panel_on:
            text_box = pygame.Surface((TEXTBOX_WIDTH, TEXTBOX_HEIGHT), pygame.SRCALPHA)
            text_box.fill((0, 0, 0, TEXTBOX_ALPHA))
            screen.blit(text_box, (TEXTBOX_X, TEXTBOX_Y))

            border_rect = pygame.Rect(TEXTBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
            pygame.draw.rect(screen, (255, 255, 255), border_rect, 2)

            snip = font.render(typed_text, True, "white")
            screen.blit(snip, (TEXTBOX_X + TEXT_PADDING_X, TEXTBOX_Y + TEXT_PADDING_Y))

            if done and active_message < len(messages) - 1:
                prompt_text = "Press Button" if RPi else "Press Enter"
                prompt = font.render(prompt_text, True, (180, 180, 180))
                screen.blit(prompt, (TEXTBOX_X + TEXT_PADDING_X, TEXTBOX_Y + PROMPT_OFFSET_Y))

        pygame.display.flip()
        clock.tick(24)

    with state.lock:
        state.running = False

    for thread in threads:
        thread.join(timeout=0.5)

    if created_display:
        pygame.quit()

    return result


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)