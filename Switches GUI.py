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

KEY_W, KEY_H = 80, 180


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

    def draw_labels(self, screen, font):
        label_surf = font.render(self.label, True, (255, 255, 255))
        screen.blit(label_surf, label_surf.get_rect(center=(self.rect.centerx, self.rect.top - 20)))
        state_surf = font.render("ON" if self.on else "OFF", True, (255, 255, 255))
        screen.blit(state_surf, state_surf.get_rect(center=(self.rect.centerx, self.rect.bottom + 20)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 420))
    pygame.display.set_caption("Switches")
    font  = pygame.font.SysFont(None, 28)
    clock = pygame.time.Clock()

    spacing = 120
    start_x = (600 - (4 * KEY_W + 3 * (spacing - KEY_W))) // 2
    switches = [
        Switch(start_x + 0 * spacing, 80, "SW1", 8, pygame.K_1),
        Switch(start_x + 1 * spacing, 80, "SW2", 4, pygame.K_2),
        Switch(start_x + 2 * spacing, 80, "SW3", 2, pygame.K_3),
        Switch(start_x + 3 * spacing, 80, "SW4", 1, pygame.K_4),
    ]
    all_sprites = pygame.sprite.Group(*switches)

    # constants
    target = random.randint(1, 15)
    rounds = 0
    strikes = 0
    game_over = False
    won = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # toggles switches on or off (keyboard)
            elif event.type == pygame.KEYDOWN and not game_over and not won:
                for sw in switches:
                    if event.key == sw.key:
                        sw.toggle()

            # press Enter to confirm
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not game_over and not won:
                # add the values of the ON switches together
                total = sum(sw.value for sw in switches if sw.on)
                # check if correct
                if total == target:
                    rounds += 1
                   
                    if rounds >= 5:
                        won = True
                    else:
                        for sw in switches:
                            if sw.on:
                                sw.toggle()
                        # generate a new random number for next round
                        target = random.randint(1, 15)
                else:
                    strikes += 1
                    
                    if strikes >= 3:
                        game_over = True

        # draw the screen
        screen.fill((30, 30, 30))
        all_sprites.draw(screen)
        for sw in switches:
            sw.draw_labels(screen, font)

        hud = font.render(f"Target: {target}   Round: {rounds+1}/5   Strikes: {strikes}/3", True, (255, 255, 255))
        screen.blit(hud, (10, 10))

        hint = font.render("Click to toggle | Enter to confirm", True, (150, 150, 150))
        screen.blit(hint, hint.get_rect(center=(300, 400)))

        if won:
            screen.blit(font.render("You win!", True, (0, 255, 0)), (240, 370))
        elif game_over:
            screen.blit(font.render("Game Over!", True, (255, 60, 60)), (230, 370))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
