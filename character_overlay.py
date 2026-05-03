import pygame


BC1_IMAGE_PATH = "img_keys/BC1.png"
BC2_IMAGE_PATH = "img_keys/BC2.png"

# Adjust these to move/resize BC1 everywhere.
BC1_X = 40
BC1_Y = 73
BC1_WIDTH = 175
BC1_HEIGHT = 180

# Adjust these to move/resize BC2 everywhere.
BC2_X = 840
BC2_Y = 73
BC2_WIDTH = 175
BC2_HEIGHT = 180


_cached_bc1_image = None
_cached_bc2_image = None


def get_bc1_image():
    global _cached_bc1_image

    if _cached_bc1_image is None:
        image = pygame.image.load(BC1_IMAGE_PATH).convert_alpha()
        _cached_bc1_image = pygame.transform.scale(
            image,
            (BC1_WIDTH, BC1_HEIGHT)
        )

    return _cached_bc1_image


def get_bc2_image():
    global _cached_bc2_image

    if _cached_bc2_image is None:
        image = pygame.image.load(BC2_IMAGE_PATH).convert_alpha()
        _cached_bc2_image = pygame.transform.scale(
            image,
            (BC2_WIDTH, BC2_HEIGHT)
        )

    return _cached_bc2_image


def draw_character(surface):
    bc1_image = get_bc1_image()
    bc2_image = get_bc2_image()

    surface.blit(bc1_image, (BC1_X, BC1_Y))
    surface.blit(bc2_image, (BC2_X, BC2_Y))