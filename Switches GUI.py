# Switches GUI - Binary Game
#
# Pseudocode:
# 1. Generate a random number 1-16
# 2. 4 switches: SW1=8, SW2=4, SW3=2, SW4=1
# 3. User toggles switches on or off
# 4. Press Enter to confirm
# 5. Add the values of the ON switches together
# 6. If sum == target -> correct; else -> strike
# 7. 3 strikes = lose | 5 correct rounds = win

import pygame
import sys
import random
from bomb_configs import *
if RPi:
    from bomb_configs import component_toggles, component_button_state

SCREEN_W, SCREEN_H = 1024, 576
KEY_W, KEY_H = 100, 230


class Switch(pygame.sprite.Sprite):
    def __init__(self, x, y, label, value, key):
        super().__init__()
        self.white_image = pygame.transform.scale(
            pygame.image.load("img_keys/white_key.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.red_image = pygame.transform.scale(
            pygame.image.load("img_keys/red_key.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.value = value
        self.key   = key
        self.on    = False
        self.image = self.white_image
        self.rect  = self.image.get_rect(topleft=(x, y))
        self.label = label

    def toggle(self):
        self.on = not self.on
        self.image = self.red_image if self.on else self.white_image

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.toggle()
            
    # vibe coded by claude
    def draw_labels(self, screen, font):
        label_surf = font.render(self.label, True, (255, 255, 255))
        screen.blit(label_surf, label_surf.get_rect(center=(self.rect.centerx, self.rect.top - 20)))
        state_surf = font.render("ON" if self.on else "OFF", True, (255, 255, 255))
        screen.blit(state_surf, state_surf.get_rect(center=(self.rect.centerx, self.rect.bottom + 20)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Switches")
    font = pygame.font.SysFont(None, 32)
    clock = pygame.time.Clock()

    spacing = 170
    start_x = (SCREEN_W - (4 * KEY_W + 3 * (spacing - KEY_W))) // 2
    #creates switch objects
    switches = [
        Switch(start_x + 0 * spacing, 80, "SW1", 8, board.D12),
        Switch(start_x + 1 * spacing, 80, "SW2", 4, board.D16),
        Switch(start_x + 2 * spacing, 80, "SW3", 2, board.D20),
        Switch(start_x + 3 * spacing, 80, "SW4", 1, board.D21),
    ]
    all_sprites = pygame.sprite.Group(*switches)

    # constants
    target = random.randint(1, 15)
    rounds = 0
    strikes = 0
    game_over = False
    won = False
    prev_btn = False

    def confirm():
        nonlocal rounds, strikes, game_over, won, target
        total = sum(sw.value for sw in switches if sw.on)
        if total == target:
            rounds += 1
            if rounds >= 5:
                won = True
                game_over = True
            else:
                for sw in switches:
                    if sw.on:
                        sw.toggle()
                target = random.randint(1, 15)
        else:
            strikes += 1
            if strikes >= 3:
                won = False
                game_over = True

    running = True
    while running:
        # mirror physical toggle switches onto the GUI
        if RPi and not game_over and not won:
            for sw, pin in zip(switches, component_toggles):
                if sw.on != pin.value:
                    sw.toggle()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not RPi and not game_over:
                for sw in switches:
                    sw.handle_click(event.pos)

            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_RETURN:
                    confirm()

        # pushbutton confirm (rising edge)
        if RPi and not game_over and not won:
            btn = component_button_state.value
            if btn and not prev_btn:
                confirm()
            prev_btn = btn

        # draw the screen
        screen.fill((30, 30, 30))
        all_sprites.draw(screen)
        for sw in switches:
            sw.draw_labels(screen, font)

        hud = font.render(f"Target: {target}   Round: {rounds+1}/5   Strikes: {strikes}/3", True, (255, 255, 255))
        screen.blit(hud, (20, 20))

        hint_text = "Flip switches | Press button to confirm" if RPi else "Click to toggle | Enter to confirm"
        hint = font.render(hint_text, True, (150, 150, 150))
        screen.blit(hint, hint.get_rect(center=(SCREEN_W // 2, SCREEN_H - 35)))

        if won:
            win_text = font.render("You win!", True, (0, 255, 0))
            screen.blit(win_text, win_text.get_rect(center=(SCREEN_W // 2, SCREEN_H - 80)))
            pygame.display.flip()
            pygame.time.wait(1000)
            pygame.quit()
            return True

        elif game_over:
            lose_text = font.render("Game Over!", True, (255, 60, 60))
            screen.blit(lose_text, lose_text.get_rect(center=(SCREEN_W // 2, SCREEN_H - 80)))
            pygame.display.flip()
            pygame.time.wait(1000)
            pygame.quit()
            return False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return False


if __name__ == "__main__":
    raise SystemExit(main())
