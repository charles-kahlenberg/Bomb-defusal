
import pygame
import sys
import random
from bomb_configs import *

if RPi:
    from bomb_configs import component_toggles, component_button_state

KEY_W, KEY_H = 34, 144


class Switch(pygame.sprite.Sprite):
    def __init__(self, x, y, label, value, key):
        super().__init__()
        self.down = pygame.transform.scale(
            pygame.image.load("img_keys\SwitchD.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.up = pygame.transform.scale(
            pygame.image.load("img_keys\SwitchUp.png").convert_alpha(), (KEY_W, KEY_H)
        )
        
        self.fu1 = pygame.transform.scale(
            pygame.image.load("img_keys\SwitchFUp1.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.fu2 = pygame.transform.scale(
            pygame.image.load("img_keys\SwitchFUp2.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.fu3 = pygame.transform.scale(
            pygame.image.load("img_keys\SwitchFUp3.png").convert_alpha(), (KEY_W, KEY_H)
        )
        
        self.fd1 = pygame.transform.scale(
            pygame.image.load("img_keys\SwitchFD1.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.fd2 = pygame.transform.scale(
            pygame.image.load("img_keys\SwitchFD2.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.fd3= pygame.transform.scale(
            pygame.image.load("img_keys\SwitchFD3.png").convert_alpha(), (KEY_W, KEY_H)
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


def randomval(first):
    baby = random.randint(0, 3)
    valu1 = first[baby]
    first.remove(first[baby])

    baby2 = random.randint(0, 2)
    valu2 = first[baby2]
    first.remove(first[baby2])

    baby3 = random.randint(0, 1)
    valu3 = first[baby3]
    first.remove(first[baby3])
    valu4 = first[0]
    values = [valu1, valu2, valu3, valu4]
    return values


def main(screen=None, clock=None):
    if not pygame.get_init():
        pygame.init()

    created_display = screen is None

    if screen is None:
        screen = pygame.display.set_mode((616, 342))

    pygame.display.set_caption("Switches")

    if clock is None:
        clock = pygame.time.Clock()

    font = pygame.font.Font("img_keys\Baskic8.otf", 24)
    Bg = pygame.image.load("img_keys\SwitchesBg.png").convert()
    Door = pygame.image.load("img_keys\Door.png").convert()

    spacing = 30
    start_x = (820 - (4 * KEY_W + 3 * (spacing - KEY_W))) // 2

    first = [1, 2, 4, 8]
    randomvals = randomval(first)

    switches = [
        Switch(start_x + 0 * spacing, 110, "", randomvals[0], pygame.K_SPACE),
        Switch(start_x + 2 * spacing, 110, "", randomvals[1], pygame.K_SPACE),
        Switch(start_x + 4 * spacing, 110, "", randomvals[2], pygame.K_SPACE),
        Switch(start_x + 6 * spacing, 110, "", randomvals[3], pygame.K_SPACE),
    ]

    all_sprites = pygame.sprite.Group(*switches)

    target = random.randint(1, 15)
    rounds = 0
    strikes = 0
    game_over = False
    won = False
    prev_btn = False
    flipping = False
    flipswitch = None
    counter = 0
    tcounter = 0

    def reset_switches_to_off():
        nonlocal flipping, flipswitch, counter

        for sw in switches:
            if sw.on:
                sw.on = False
                sw.flipup = False
                sw.flipdown = True
                sw.image = sw.down

        flipping = False
        flipswitch = None
        counter = 0

    def confirm():
        nonlocal rounds, strikes, game_over, won, target, tcounter

        total = sum(sw.value for sw in switches if sw.on)

        if total == target:
            tcounter = 0
            rounds += 1

            if rounds >= 5:
                won = True
                game_over = True
            else:
                first = [1, 2, 4, 8]
                second = [16, 4, 32, 8, 64]
                third = [128, 256, 64, 32, 16, 512]
                fourth = [413, 27, 31, 93]

                if rounds <= 1:
                    target = random.randint(1, 15)
                    randomvals = randomval(first)

                elif rounds == 2:
                    randomvals = randomval(second)
                    target = 0
                    for r in randomvals:
                        if random.randint(0, 1) == 1:
                            target += r

                elif rounds == 3:
                    randomvals = randomval(third)
                    target = 0
                    for r in randomvals:
                        if random.randint(0, 1) == 1:
                            target += r

                else:
                    randomvals = randomval(fourth)
                    target = 0
                    for r in randomvals:
                        if random.randint(0, 1) == 1:
                            target += r

                for i, sw in enumerate(switches):
                    sw.value = randomvals[i]

                reset_switches_to_off()
        else:
            tcounter = -100
            strikes += 1

            if strikes >= 3:
                won = False
                game_over = True

    running = True

    while running:
        if RPi and not game_over and not won:
            for sw, pin in zip(switches, component_toggles):
                if not flipping and sw.set_state(pin.value):
                    flipswitch = sw
                    flipping = True
                    break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if created_display:
                    pygame.quit()

                return False

            elif event.type == pygame.MOUSEBUTTONDOWN and not RPi and not game_over:
                if not flipping:
                    for sw in switches:
                        worked = sw.handle_click(event.pos)

                        if worked:
                            flipswitch = sw
                            flipping = True
                            break

            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_RETURN and not RPi:
                    confirm()

        if RPi and not game_over and not won:
            btn = component_button_state.value

            if btn and not prev_btn:
                confirm()

            prev_btn = btn

        if flipping and flipswitch is not None:
            if flipswitch.flipup:
                if counter == 0:
                    counter += 1
                    flipswitch.image = flipswitch.fu1
                elif counter <= 6:
                    counter += 1
                    flipswitch.image = flipswitch.fu2
                elif counter <= 9:
                    counter += 1
                    flipswitch.image = flipswitch.fu3
                else:
                    counter = 0
                    flipping = False
                    flipswitch.image = flipswitch.up
            else:
                if counter == 0:
                    counter += 1
                    flipswitch.image = flipswitch.fd1
                elif counter <= 6:
                    counter += 1
                    flipswitch.image = flipswitch.fd2
                elif counter <= 9:
                    counter += 1
                    flipswitch.image = flipswitch.fd3
                else:
                    counter = 0
                    flipping = False
                    flipswitch.image = flipswitch.down

        screen.blit(Bg, (0, 0))
        screen.blit(Door, (29, 16))
        all_sprites.draw(screen)

        if rounds < 5:
            if tcounter <= 0:
                hud = font.render(f"Strikes: {strikes}/3", True, (255, 255, 255))
                tcounter += 1
            elif 0 <= tcounter <= 100:
                hud = font.render(f"Round: {rounds + 1}/5", True, (255, 255, 255))
                tcounter += 1
            else:
                hud = font.render(f"Target: {target}", True, (255, 255, 255))
        else:
            hud = font.render("You win!", True, (255, 255, 255))

        screen.blit(hud, (380, 40))

        total = sum(sw.value for sw in switches if sw.on)
        tot = font.render(f"Total : {total}", True, (255, 255, 255))
        screen.blit(tot, (380, 290))

        hint_text = "Flip switches | Press button to confirm" if RPi else "Click switches | Press Enter to confirm"
        hint = font.render(hint_text, True, (150, 150, 150))
        screen.blit(hint, hint.get_rect(center=(300, 325)))

        if won:
            screen.blit(font.render("You win!", True, (0, 255, 0)), (240, 270))
            pygame.display.flip()
            pygame.time.wait(1000)

            if created_display:
                pygame.quit()

            return True

        elif game_over:
            screen.blit(font.render("Game Over!", True, (255, 60, 60)), (230, 270))
            pygame.display.flip()
            pygame.time.wait(1000)

            if created_display:
                pygame.quit()

            return False

        pygame.display.flip()
        clock.tick(60)

    if created_display:
        pygame.quit()

    return False


if __name__ == "__main__":
    raise SystemExit(main())
