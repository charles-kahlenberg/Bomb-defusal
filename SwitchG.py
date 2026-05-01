
import pygame
import sys
import random

KEY_W, KEY_H = 34, 144


class Switch(pygame.sprite.Sprite):
    def __init__(self, x, y, label, value, key):
        super().__init__()
        self.down = pygame.transform.scale(
            pygame.image.load("SwitchD.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.up = pygame.transform.scale(
            pygame.image.load("SwitchUp.png").convert_alpha(), (KEY_W, KEY_H)
        )
        
        self.fu1 = pygame.transform.scale(
            pygame.image.load("SwitchFUp1.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.fu2 = pygame.transform.scale(
            pygame.image.load("SwitchFUp2.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.fu3 = pygame.transform.scale(
            pygame.image.load("SwitchFUp3.png").convert_alpha(), (KEY_W, KEY_H)
        )
        
        self.fd1 = pygame.transform.scale(
            pygame.image.load("SwitchFD1.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.fd2 = pygame.transform.scale(
            pygame.image.load("SwitchFD2.png").convert_alpha(), (KEY_W, KEY_H)
        )
        self.fd3= pygame.transform.scale(
            pygame.image.load("SwitchFD3.png").convert_alpha(), (KEY_W, KEY_H)
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
            
    # vibe coded by claude
    def draw_labels(self, screen, font):
        label_surf = font.render(self.label, True, (255, 255, 255))
        screen.blit(label_surf, label_surf.get_rect(center=(self.rect.centerx, self.rect.top - 20)))

def randomval(first):
    
    baby = random.randint(0,3)
    valu1 = first[baby]
    first.remove(first[baby])
    baby2 = random.randint(0,2)
    valu2 = first[baby2]
    first.remove(first[baby2])
    baby3 = random.randint(0,1)
    valu3 = first[baby3]
    first.remove(first[baby3])
    valu4 = first[0]
    values = [valu1, valu2, valu3, valu4]
    return values
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((616, 342))
    pygame.display.set_caption("Switches")
    font  = pygame.font.Font("Baskic8.otf", 24)
    clock = pygame.time.Clock()
    Bg = pygame.image.load("SwitchesBg.png").convert()
    Door = pygame.image.load("Door.png").convert()
    
    spacing = 30
    start_x = (820 - (4 * KEY_W + 3 * (spacing - KEY_W))) // 2
    #creates switch objects
    rannum =  random.randint(0,3)
    
    first = [1, 2, 4, 8]
    randomvals = randomval(first)
    valu1 = randomvals[0]
    valu2 = randomvals[1]
    valu3 = randomvals[2]
    valu4 = randomvals[3]
    
    print(valu1)
    print(valu2)
    print(valu3)
    print(valu4)
    
    switches = [
        Switch(start_x + 0 * spacing, 110, "", valu1, pygame.K_SPACE),
        Switch(start_x + 2 * spacing, 110, "", valu2, pygame.K_SPACE),
        Switch(start_x + 4 * spacing, 110, "", valu3, pygame.K_SPACE),
        Switch(start_x + 6 * spacing, 110, "", valu4, pygame.K_SPACE),
    ]
    all_sprites = pygame.sprite.Group(*switches)
    
    # constants
    target = random.randint(1, 15)
    rounds = 0
    strikes = 0
    game_over = False
    won = False
    prev_btn = False
    flipping = False
    counter = 0
    tcounter = 0


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
                    tcounter = 0
                    i = 0
                    target = random.randint(1,15)
                    randomvals = randomval(first)
                    for sw in switches:
                        sw.value = randomvals[i]
                        i += 1
                if rounds == 2:
                    tcounter = 0
                    i = 0
                    randomvals = randomval(second)
                    target = 0
                    for sw in switches:
                        sw.value = randomvals[i]
                        i += 1
                    for r in randomvals:
                        if random.randint(0,1) == 1:
                            target += r
                if rounds == 3:
                    tcounter = 0
                    i = 0
                    randomvals = randomval(third)
                    target = 0
                    for sw in switches:
                        sw.value = randomvals[i]
                        i += 1
                    for r in randomvals:
                        if random.randint(0,1) == 1:
                            target += r
                if rounds == 4:
                    tcounter = 0
                    i = 0
                    randomvals = randomval(fourth)
                    target = 0
                    for sw in switches:
                        sw.value = randomvals[i]
                        i += 1
                    for r in randomvals:
                        if random.randint(0,1) == 1:
                            target += r
        else:
            tcounter = -100
            strikes += 1
            if strikes >= 3:
                won = False
                game_over = True

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if flipping == False:
                    for sw in switches:
                        worked = sw.handle_click(event.pos)
                        if worked == True:
                            flipswitch = sw
                            flipping = True
                    

            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_RETURN:
                    confirm()

        # pushbutton confirm (rising edge)
        # draw the screen

        if flipping:
            if flipswitch.flipup == True:
                if counter == 0:
                    counter += 1
                    flipswitch.image = flipswitch.fu1
                if counter <= 6:
                    counter += 1
                    flipswitch.image = flipswitch.fu2
                if counter <= 9:
                    counter += 1
                    flipswitch.image = flipswitch.fu3
                if counter > 9:
                    counter = 0
                    flipping = False
                    flipswitch.image = flipswitch.up
            else:
                if counter == 0:
                    counter += 1
                    flipswitch.image = flipswitch.fd1
                if counter <= 6:
                    counter += 1
                    flipswitch.image = flipswitch.fd2
                if counter <= 9:
                    counter += 1
                    flipswitch.image = flipswitch.fd3
                if counter > 9:
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
            if 0 <= tcounter and tcounter <= 100:
                hud = font.render(f"Round: {rounds+1}/5", True, (255,255,255))
                tcounter += 1
            if tcounter > 100:
                hud = font.render(f"Target: {target}", True, (255,255,255))
        else:
            hud = font.render(f"You win!", True, (255,255,255))
        
        screen.blit(hud, (380, 40))
        total = sum(sw.value for sw in switches if sw.on)
        tot = font.render(f"Total : {total}", True, (255,255,255))
        screen.blit(tot, (380, 290))
        total = sum(sw.value for sw in switches if sw.on)
        
        
        hint_text = "Flip switches | Press button to confirm" 
        hint = font.render(hint_text, True, (150, 150, 150))
        screen.blit(hint, hint.get_rect(center=(300, 400)))

        if won:
            screen.blit(font.render("You win!", True, (0, 255, 0)), (240, 370))
            pygame.display.flip()
            pygame.time.wait(1000)
            pygame.quit()
            return True

        elif game_over:
            screen.blit(font.render("Game Over!", True, (255, 60, 60)), (230, 370))
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

