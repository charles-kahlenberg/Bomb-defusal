# Switches GUI


#Binary Game

#Psuedocode
#1. Generate a random number 16-1
#2. 4 inputs, first button = 8, second button = 4, third button = 2, fourth button = 1
#3. Add the values of the buttons together
#4. If the sum of the buttons is equal to the random number, you win, if not, you lose



import pygame
import sys
import random


class Switch:
    def __init__(self, x, y, width=80, height=180, label=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.on = False

    def toggle(self):
        self.on = not self.on

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.toggle()
            return True
        return False

    def draw(self, screen, font):
        body_color = (60, 60, 60)
        frame_color = (200, 200, 200)
        knob_color = (0, 220, 0) if self.on else (200, 0, 0)

        pygame.draw.rect(screen, body_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, frame_color, self.rect, width=3, border_radius=10)

        knob_w = self.rect.width - 20
        knob_h = (self.rect.height - 30) // 2
        knob_x = self.rect.x + 10
        knob_y = self.rect.y + 10 if self.on else self.rect.bottom - 10 - knob_h
        pygame.draw.rect(screen, knob_color, (knob_x, knob_y, knob_w, knob_h), border_radius=8)

        state = "ON" if self.on else "OFF"
        state_surf = font.render(state, True, (255, 255, 255))
        screen.blit(state_surf, state_surf.get_rect(center=(self.rect.centerx, self.rect.bottom + 24)))

        label_surf = font.render(self.label, True, (255, 255, 255))
        screen.blit(label_surf, label_surf.get_rect(center=(self.rect.centerx, self.rect.top - 24)))




def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Switches")
    font = pygame.font.SysFont(None, 28)
    clock = pygame.time.Clock()

    spacing = 120
    start_x = (600 - (4 * 80 + 3 * (spacing - 80))) // 2
    y = 100
    switches = [
        Switch(start_x + i * spacing, y, label=f"SW{i + 1}")
        for i in range(4)
    ]
    random_number = random.randint(1, 16)

    rounds = 0
    strikes = 0
    max_strikes = 3
    game_over = False
    won = False

    melody = []
    player_melody = []
    state = "start_round"    # "start_round" -> "computer_playing" -> "player_input" -> "check" -> "between_rounds" (Planned by Claude)
    check_time = 0
    chord_gap_ms = 800        # time between computer-played chords
    between_rounds_ms = 1000  # pause after a round so the last highlight stays visible
    pre_result_ms = 250       # tiny beat between the last click and the win/lose sound
    timer = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and state in ("player_input"): # imported from Safe Game
                key_to_index = {pygame.K_1: 8, pygame.K_2: 4, pygame.K_3: 2, pygame.K_4: 1,}
        if not game_over and not won:
            if state == "start round":
                # Generate a random number for the round
                random_number = random.randint(1, 16)
                print(f"Round {rounds + 1}: Target number is {random_number}")
                state = "player_input"
            elif state == "player_input":
                if event.type == pygame.KEYDOWN and event.key in key_to_index:
                    for sw in switches:
                        if sw.handle_click(event.pos):
                            break
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # Check the player's input
                    total = sum(8 if sw.on else 0 for sw in switches) + sum(4 if sw.on else 0 for sw in switches) + sum(2 if sw.on else 0 for sw in switches) + sum(1 if sw.on else 0 for sw in switches)
                    if total == random_number:
                        print("Correct! You win this round.")
                        won = True
                    else:
                        print("Incorrect! You lose this round.")
                        strikes += 1
                        if strikes >= max_strikes:
                            print("Game Over! You've reached the maximum strikes.")
                            game_over = True
            

        screen.fill((0, 0, 0))
        for sw in switches:
            sw.draw(screen, font)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return [sw.on for sw in switches]


if __name__ == "__main__":
    main()
    sys.exit(0)

#Binary Game

#Psuedocode
#1. Generate a random number 16-1
#2. 4 inputs, first button = 8, second button = 4, third button = 2, fourth button = 1
#3. User puts in their input by toggling the switches on or off
#4. Press a button to confirm when they are finisihed
#5. Check state to see if the user was correct,  Add the values of the buttons together ff the sum of the buttons is equal to the random number, you win, if not, you lose
#6. If they are incorrect, then they get a strike, if they get 3 strikes, they lose. If they are correct, they win.
# Continue for 5 rounds


