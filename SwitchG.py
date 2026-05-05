"""
SwitchG.py

Switch/binary puzzle minigame for the Bomb Defusal game.

Responsibilities:
- Displays a switch panel inside the main game screen.
- Generates target values for each round.
- Allows the player to toggle switches to match the target total.
- Tracks strikes, rounds, and switch flip limits.
- Supports mouse input on PC and physical toggle/button input on RPi.

Gameplay:
- Each switch has a hidden numeric value.
- The player toggles switches until their total matches the target.
- Pressing Enter on PC, or the physical button on RPi, confirms the answer.
- Incorrect totals add strikes.
- Too many strikes causes failure.
- Completing all rounds causes success.

Thread usage:
- SwitchTextThread updates HUD text.
- SwitchesThread handles switch animation and RPi toggle polling.

Returns:
- True when all switch rounds are completed.
- False when the player loses or closes the window.
"""

import pygame
import random
import threading
import time

from bomb_configs import *
from character_overlay import draw_character
from display_utils import create_fullscreen_display

if RPi:
    from bomb_configs import component_toggles, component_button_state

GAME_W, GAME_H = 616, 342

MINIGAME_WINDOW_X = 300
MINIGAME_WINDOW_Y = 232
MINIGAME_WINDOW_W = 425
MINIGAME_WINDOW_H = 299

KEY_W, KEY_H = 34, 144

# Balance setting:
# This limits how many times switches can be flipped UP per round.
# Flipping a switch DOWN does not count.
MAX_UP_FLIPS_PER_ROUND = 10
FLIP_COUNTER_DISPLAY_MS = 1000


class Switch(pygame.sprite.Sprite):
    def __init__(self, x, y, label, value, key):
        super().__init__()
        self.down = pygame.transform.scale(
            pygame.image.load("img_keys/SwitchD.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.up = pygame.transform.scale(
            pygame.image.load("img_keys/SwitchUp.png").convert_alpha(), (KEY_W, KEY_H)
        )
        
        self.fu1 = pygame.transform.scale(
            pygame.image.load("img_keys/SwitchFUp1.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.fu2 = pygame.transform.scale(
            pygame.image.load("img_keys/SwitchFUp2.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.fu3 = pygame.transform.scale(
            pygame.image.load("img_keys/SwitchFUp3.png").convert_alpha(), (KEY_W, KEY_H)
        )
        
        self.fd1 = pygame.transform.scale(
            pygame.image.load("img_keys/SwitchFD1.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.fd2 = pygame.transform.scale(
            pygame.image.load("img_keys/SwitchFD2.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.fd3= pygame.transform.scale(
            pygame.image.load("img_keys/SwitchFD3.png").convert_alpha(), (KEY_W, KEY_H)
        )
        
        self.value = value
        self.key   = key
        self.on    = False
        self.image = self.down
        self.rect  = self.image.get_rect(topleft=(x, y))
        self.label = label
        self.framecount = 0
        self.flipup = False
        self.flipdown = True

    def toggle(self):
        self.on = not self.on
        if self.on:
            self.flipup = True
            self.flipdown = False
        else:
            self.flipdown = True
            self.flipup = False

    def set_state(self, new_state):
        if self.on != new_state:
            self.toggle()
            return True

        return False

    def handle_click(self, pos):
        worked = False
        if self.rect.collidepoint(pos):
            self.toggle()
            worked = True
            return worked

        return worked

    def draw_labels(self, screen, font):
        label_surf = font.render(self.label, True, (255, 255, 255))
        screen.blit(label_surf, label_surf.get_rect(center=(self.rect.centerx, self.rect.top - 20)))


def randomval(values):
    values = values[:]
    random.shuffle(values)
    return values[:4]


class SwitchGameState:
    def __init__(self):
        self.lock = threading.RLock()
        self.running = True

        self.rounds = 0
        self.strikes = 0
        self.target = random.randint(1, 15)

        self.up_flips_this_round = 0
        self.flip_counter_visible_until = 0

        self.game_over = False
        self.won = False

        self.prev_btn = False

        self.flipping = False
        self.flipswitch_index = None
        self.flip_counter = 0

        self.tcounter = 0
        self.hud_text = "Round: 1/5"
        self.hud_color = (255, 255, 255)
        self.total = 0


class SwitchTextThread(threading.Thread):
    def __init__(self, state):
        super().__init__(daemon=True)
        self.state = state

    def run(self):
        while True:
            with self.state.lock:
                if not self.state.running:
                    break

                if self.state.rounds < 5:
                    if self.state.tcounter <= 0:
                        self.state.hud_text = f"Strikes: {self.state.strikes}/3"
                        self.state.hud_color = (255, 255, 255)
                        self.state.tcounter += 1
                    elif self.state.tcounter <= 100:
                        self.state.hud_text = f"Round: {self.state.rounds + 1}/5"
                        self.state.hud_color = (255, 255, 255)
                        self.state.tcounter += 1
                    else:
                        self.state.hud_text = f"Target: {self.state.target}"
                        self.state.hud_color = (255, 255, 255)
                else:
                    self.state.hud_text = "You win!"
                    self.state.hud_color = (255, 255, 255)

            time.sleep(1 / 60)


class SwitchesThread(threading.Thread):
    def __init__(self, state, switches):
        super().__init__(daemon=True)
        self.state = state
        self.switches = switches

    def run(self):
        while True:
            with self.state.lock:
                if not self.state.running:
                    break

                if RPi and not self.state.game_over and not self.state.won:
                    for index, pin in enumerate(component_toggles):
                        sw = self.switches[index]
                        is_flipping_up = pin.value and not sw.on
                        out_of_up_flips = self.state.up_flips_this_round >= MAX_UP_FLIPS_PER_ROUND

                        if is_flipping_up and out_of_up_flips:
                            self.state.won = False
                            self.state.game_over = True
                            break

                        if not self.state.flipping and sw.set_state(pin.value):
                            if is_flipping_up:
                                self.state.up_flips_this_round += 1
                                self.state.flip_counter_visible_until = (
                                    pygame.time.get_ticks() + FLIP_COUNTER_DISPLAY_MS
                                )

                                if self.state.up_flips_this_round >= MAX_UP_FLIPS_PER_ROUND:
                                    self.state.won = False
                                    self.state.game_over = True

                            self.state.flipswitch_index = index
                            self.state.flipping = True
                            break

                if self.state.flipping and self.state.flipswitch_index is not None:
                    flipswitch = self.switches[self.state.flipswitch_index]

                    if flipswitch.flipup:
                        if self.state.flip_counter == 0:
                            self.state.flip_counter += 1
                            flipswitch.image = flipswitch.fu1
                        elif self.state.flip_counter <= 6:
                            self.state.flip_counter += 1
                            flipswitch.image = flipswitch.fu2
                        elif self.state.flip_counter <= 9:
                            self.state.flip_counter += 1
                            flipswitch.image = flipswitch.fu3
                        else:
                            self.state.flip_counter = 0
                            self.state.flipping = False
                            self.state.flipswitch_index = None
                            flipswitch.image = flipswitch.up
                    else:
                        if self.state.flip_counter == 0:
                            self.state.flip_counter += 1
                            flipswitch.image = flipswitch.fd1
                        elif self.state.flip_counter <= 6:
                            self.state.flip_counter += 1
                            flipswitch.image = flipswitch.fd2
                        elif self.state.flip_counter <= 9:
                            self.state.flip_counter += 1
                            flipswitch.image = flipswitch.fd3
                        else:
                            self.state.flip_counter = 0
                            self.state.flipping = False
                            self.state.flipswitch_index = None
                            flipswitch.image = flipswitch.down

                self.state.total = sum(sw.value for sw in self.switches if sw.on)

            time.sleep(1 / 60)


def main(screen=None, clock=None):
    if not pygame.get_init():
        pygame.init()

    created_display = screen is None

    if screen is None:
        screen = create_fullscreen_display("Switches")

    pygame.display.set_caption("Switches")

    main_screen = screen
    game_surface = pygame.Surface((GAME_W, GAME_H), pygame.SRCALPHA)
    screen = game_surface

    if clock is None:
        clock = pygame.time.Clock()

    intro_bg = pygame.image.load("img_keys/base.png").convert()
    intro_bg = pygame.transform.scale(intro_bg, main_screen.get_size())

    minigame_rect = pygame.Rect(
        MINIGAME_WINDOW_X,
        MINIGAME_WINDOW_Y,
        MINIGAME_WINDOW_W,
        MINIGAME_WINDOW_H
    )

    def show_frame():
        main_screen.blit(intro_bg, (0, 0))
        draw_character(main_screen)
        scaled_game = pygame.transform.smoothscale(game_surface, minigame_rect.size)
        main_screen.blit(scaled_game, minigame_rect)
        pygame.display.flip()

    def screen_pos_to_game_pos(pos):
        if not minigame_rect.collidepoint(pos):
            return None

        rel_x = pos[0] - minigame_rect.x
        rel_y = pos[1] - minigame_rect.y

        game_x = int(rel_x * GAME_W / minigame_rect.w)
        game_y = int(rel_y * GAME_H / minigame_rect.h)

        return game_x, game_y

    font = pygame.font.Font("img_keys/Baskic8.otf", 24)

    bg = pygame.image.load("img_keys/SwitchesBg.png").convert()
    bg = pygame.transform.scale(bg, (GAME_W, GAME_H))

    door = pygame.image.load("img_keys/Door.png").convert()

    spacing = 30
    start_x = (820 - (4 * KEY_W + 3 * (spacing - KEY_W))) // 2

    randomvals = randomval([1, 2, 4, 8])

    switches = [
        Switch(start_x + 0 * spacing, 110, "", randomvals[0], pygame.K_SPACE),
        Switch(start_x + 2 * spacing, 110, "", randomvals[1], pygame.K_SPACE),
        Switch(start_x + 4 * spacing, 110, "", randomvals[2], pygame.K_SPACE),
        Switch(start_x + 6 * spacing, 110, "", randomvals[3], pygame.K_SPACE),
    ]

    all_sprites = pygame.sprite.Group(*switches)

    state = SwitchGameState()

    text_thread = SwitchTextThread(state)
    switches_thread = SwitchesThread(state, switches)

    text_thread.start()
    switches_thread.start()

    def reset_switches_to_off():
        with state.lock:
            for sw in switches:
                if sw.on:
                    sw.on = False
                    sw.flipup = False
                    sw.flipdown = True
                    sw.image = sw.down

            state.flipping = False
            state.flipswitch_index = None
            state.flip_counter = 0
            state.total = 0

    def confirm():
        with state.lock:
            total = sum(sw.value for sw in switches if sw.on)

            if total == state.target:
                state.tcounter = 0
                state.rounds += 1
                state.up_flips_this_round = 0

                if state.rounds >= 5:
                    state.won = True
                    state.game_over = True
                    return

                first = [1, 2, 4, 8]
                second = [16, 4, 32, 8, 64]
                third = [128, 256, 64, 32, 16, 512]
                fourth = [413, 27, 31, 93]

                if state.rounds <= 1:
                    state.target = random.randint(1, 15)
                    randomvals = randomval(first)
                elif state.rounds == 2:
                    randomvals = randomval(second)
                    state.target = 0

                    for r in randomvals:
                        if random.randint(0, 1) == 1:
                            state.target += r
                elif state.rounds == 3:
                    randomvals = randomval(third)
                    state.target = 0

                    for r in randomvals:
                        if random.randint(0, 1) == 1:
                            state.target += r
                else:
                    randomvals = randomval(fourth)
                    state.target = 0

                    for r in randomvals:
                        if random.randint(0, 1) == 1:
                            state.target += r

                for i, sw in enumerate(switches):
                    sw.value = randomvals[i]
            else:
                state.tcounter = -100
                state.strikes += 1

                if state.strikes >= 3:
                    state.won = False
                    state.game_over = True

        with state.lock:
            should_reset = not state.game_over

        if should_reset:
            reset_switches_to_off()

    running = True

    while running:
        with state.lock:
            game_over = state.game_over
            won = state.won

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with state.lock:
                    state.running = False

                text_thread.join(timeout=0.5)
                switches_thread.join(timeout=0.5)

                if created_display:
                    pygame.quit()

                return False

            elif event.type == pygame.MOUSEBUTTONDOWN and not RPi and not game_over:
                game_pos = screen_pos_to_game_pos(event.pos)

                if game_pos is not None:
                    with state.lock:
                        if not state.flipping:
                            for index, sw in enumerate(switches):
                                is_flipping_up = sw.rect.collidepoint(game_pos) and not sw.on
                                out_of_up_flips = state.up_flips_this_round >= MAX_UP_FLIPS_PER_ROUND

                                if is_flipping_up and out_of_up_flips:
                                    state.won = False
                                    state.game_over = True
                                    break

                                worked = sw.handle_click(game_pos)

                                if worked:
                                    if is_flipping_up:
                                        state.up_flips_this_round += 1
                                        state.flip_counter_visible_until = (
                                            pygame.time.get_ticks() + FLIP_COUNTER_DISPLAY_MS
                                        )

                                        if state.up_flips_this_round >= MAX_UP_FLIPS_PER_ROUND:
                                            state.won = False
                                            state.game_over = True

                                    state.flipswitch_index = index
                                    state.flipping = True
                                    break

            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_RETURN and not RPi:
                    confirm()

        if RPi and not game_over and not won:
            btn = component_button_state.value
            should_confirm = False

            with state.lock:
                if btn and not state.prev_btn:
                    should_confirm = True

                state.prev_btn = btn

            if should_confirm:
                confirm()

        screen.blit(bg, (0, 0))
        screen.blit(door, (29, 16))
        all_sprites.draw(screen)

        with state.lock:
            hud_text = state.hud_text
            hud_color = state.hud_color
            total_value = state.total
            flips_left = MAX_UP_FLIPS_PER_ROUND - state.up_flips_this_round
            show_flip_counter = pygame.time.get_ticks() < state.flip_counter_visible_until
            won = state.won
            game_over = state.game_over

        hud = font.render(hud_text, True, hud_color)
        screen.blit(hud, (380, 40))

        if show_flip_counter:
            bottom_text = font.render(
                f"Flips: {flips_left}/{MAX_UP_FLIPS_PER_ROUND}",
                True,
                (255, 255, 255)
            )
        else:
            bottom_text = font.render(
                f"Total : {total_value}",
                True,
                (255, 255, 255)
            )

        screen.blit(bottom_text, (380, 290))

        if won:
            #screen.blit(font.render("You win!", True, (0, 255, 0)), (240, 270))
            show_frame()
            pygame.time.wait(1000)

            with state.lock:
                state.running = False

            text_thread.join(timeout=0.5)
            switches_thread.join(timeout=0.5)

            if created_display:
                pygame.quit()

            return True

        if game_over:
            #screen.blit(font.render("Game Over!", True, (255, 60, 60)), (230, 270))
            show_frame()
            pygame.time.wait(1000)

            with state.lock:
                state.running = False

            text_thread.join(timeout=0.5)
            switches_thread.join(timeout=0.5)

            if created_display:
                pygame.quit()

            return False

        show_frame()
        clock.tick(60)

    with state.lock:
        state.running = False

    text_thread.join(timeout=0.5)
    switches_thread.join(timeout=0.5)

    if created_display:
        pygame.quit()

    return False


if __name__ == "__main__":
    raise SystemExit(main())
