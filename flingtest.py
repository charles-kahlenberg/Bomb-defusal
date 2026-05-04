import pygame
from character_overlay import draw_character

try:
    from bomb_configs import RPi, component_keypad
except ImportError:
    RPi = False
    component_keypad = None


GAME_W = 1024
GAME_H = 576

WIRE_WINDOW_X = 300
WIRE_WINDOW_Y = 232
WIRE_WINDOW_W = 425
WIRE_WINDOW_H = 299

VENT_WINDOW_X = 300
VENT_WINDOW_Y = 232
VENT_WINDOW_W = 425
VENT_WINDOW_H = 299

TEXTBOX_X = 277
TEXTBOX_Y = 42
TEXTBOX_WIDTH = 471
TEXTBOX_HEIGHT = 132
TEXTBOX_ALPHA = 180


def main(screen=None, clock=None):
    if not pygame.get_init():
        pygame.init()

    created_display = screen is None
    if screen is None:
        screen = pygame.display.set_mode((1024, 576))

    if clock is None:
        clock = pygame.time.Clock()

    pygame.display.set_caption("Vent Minigame")

    main_screen = screen
    wire_surface = pygame.Surface((GAME_W, GAME_H), pygame.SRCALPHA)

    intro_bg = pygame.image.load("img_keys/base.png").convert()
    intro_bg = pygame.transform.scale(intro_bg, main_screen.get_size())

    wire_rect = pygame.Rect(
        WIRE_WINDOW_X,
        WIRE_WINDOW_Y,
        WIRE_WINDOW_W,
        WIRE_WINDOW_H
    )

    vent_rect = pygame.Rect(
        VENT_WINDOW_X,
        VENT_WINDOW_Y,
        VENT_WINDOW_W,
        VENT_WINDOW_H
    )

    def show_frame():
        main_screen.blit(intro_bg, (0, 0))
        draw_character(main_screen)

        text_box = pygame.Surface((TEXTBOX_WIDTH, TEXTBOX_HEIGHT), pygame.SRCALPHA)
        text_box.fill((0, 0, 0, TEXTBOX_ALPHA))
        main_screen.blit(text_box, (TEXTBOX_X, TEXTBOX_Y))

        border_rect = pygame.Rect(TEXTBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
        pygame.draw.rect(main_screen, (255, 255, 255), border_rect, 2)

        scaled_wires = pygame.transform.smoothscale(wire_surface, wire_rect.size)
        main_screen.blit(scaled_wires, wire_rect)

    vent = pygame.image.load("img_keys/vent.png").convert_alpha()
    vent = pygame.transform.smoothscale(vent, vent_rect.size)
    ven1 = pygame.mixer.Sound("img_keys/LongVent.mp3")

    wire_bg = pygame.image.load("img_keys/WireBG.png").convert()
    wire_bg = pygame.transform.scale(wire_bg, wire_surface.get_size())

    def load_wire_endpoint(path, scale):
        image = pygame.image.load(path).convert_alpha()
        new_size = (
            int(image.get_width() * scale),
            int(image.get_height() * scale)
        )
        return pygame.transform.smoothscale(image, new_size)

    def draw_image_centered(surface, image, center):
        surface.blit(image, image.get_rect(center=center))

    wire_endpoint_images = {
        "circle1": load_wire_endpoint("img_keys/W1T.png", 2.25),
        "circle2": load_wire_endpoint("img_keys/W2T.png", 2.25),
        "circle3": load_wire_endpoint("img_keys/W3T.png", 2.25),
        "circle4": load_wire_endpoint("img_keys/W4T.png", 2.25),
        "circle5": load_wire_endpoint("img_keys/W5T.png", 2.25),
        "circle6": load_wire_endpoint("img_keys/W1B.png", 2.25),
        "circle7": load_wire_endpoint("img_keys/W2B.png", 2.25),
        "circle8": load_wire_endpoint("img_keys/W3B.png", 2.25),
        "circle9": load_wire_endpoint("img_keys/W4B.png", 2.25),
        "circle10": load_wire_endpoint("img_keys/W5B.png", 2.25),
    }

    wire_endpoint_positions = {
        "circle1": (112, 184),
        "circle2": (312, 143),
        "circle3": (512, 152),
        "circle4": (712, 168),
        "circle5": (912, 114),
        "circle6": (112, 450),
        "circle7": (312, 416),
        "circle8": (512, 430),
        "circle9": (712, 428),
        "circle10": (912, 418),
    }

    angle = 0
    pressed = []
    target_sequence = [1, 2, 3, 4]

    rx = VENT_WINDOW_X
    ry = VENT_WINDOW_Y
    count = 0

    fling = False
    notflung = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if created_display:
                    pygame.quit()
                return False

            if event.type == pygame.KEYDOWN and not RPi:
                if event.key == pygame.K_1:
                    pressed.append(1)
                elif event.key == pygame.K_2:
                    pressed.append(2)
                elif event.key == pygame.K_3:
                    pressed.append(3)
                elif event.key == pygame.K_4:
                    pressed.append(4)

        if RPi and component_keypad is not None:
            keys = component_keypad.pressed_keys

            if keys:
                current_key = keys[0]

                if current_key != last_rpi_key:
                    if current_key in (1, 2, 3, 4):
                        pressed.append(current_key)

                    last_rpi_key = current_key
            else:
                last_rpi_key = None

        wire_surface.fill((0, 0, 0, 0))

        wire_surface.blit(wire_bg, (0, 0))

        for endpoint_name, position in wire_endpoint_positions.items():
            draw_image_centered(wire_surface, wire_endpoint_images[endpoint_name], position)

        if pressed == target_sequence:
            fling = True
        elif len(pressed) >= len(target_sequence):
            pressed = []

        if fling:
            count += 1
            angle += 20
            rx -= 40
            ry -= 40
            if notflung == False:
                ven1.play()
                notflung = True

            if count >= 35:
                return True

        show_frame()

        fvent = pygame.transform.rotate(vent, angle)
        main_screen.blit(fvent, (rx, ry))
        pygame.display.flip()

        clock.tick(60)

    if created_display:
        pygame.quit()

    return False


if __name__ == "__main__":
    raise SystemExit(main())
