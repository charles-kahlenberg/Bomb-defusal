import pygame
import sys


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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for sw in switches:
                    if sw.handle_click(event.pos):
                        break

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
