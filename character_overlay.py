import pygame


BC1_IMAGE_PATH = "img_keys/BC1.png"
BC2_IMAGE_PATH = "img_keys/BC2.png"

BC1_TOP_FRAME_PATHS = [
    "img_keys/Top1C1.png",
]

BC2_TOP_FRAME_PATHS = [
    "img_keys/Top1C2.png",
    "img_keys/Top2C2.png",
    "img_keys/Top3C2.png",
]

BC1_TOP_FRAME_TIME_MS = 700
BC2_TOP_FRAME_TIME_MS = 700

# Adjust these to move/resize BC1 everywhere.
BC1_X = 40
BC1_Y = 73
BC1_WIDTH = 175
BC1_HEIGHT = 180

# Adjust these to move/resize the animated top layer for BC1.
BC1_TOP_X = 41
BC1_TOP_Y = 64
BC1_TOP_WIDTH = 170
BC1_TOP_HEIGHT = 180

# Adjust these to move/resize BC2 everywhere.
BC2_X = 840
BC2_Y = 73
BC2_WIDTH = 175
BC2_HEIGHT = 180

# Adjust these to move/resize the animated top layer for BC2.
BC2_TOP_X = 840
BC2_TOP_Y = 64
BC2_TOP_WIDTH = 170
BC2_TOP_HEIGHT = 180


_cached_bc1_image = None
_cached_bc2_image = None
_cached_bc1_top_frames = None
_cached_bc2_top_frames = None


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


def get_bc1_top_frames():
    global _cached_bc1_top_frames

    if _cached_bc1_top_frames is None:
        _cached_bc1_top_frames = []

        for frame_path in BC1_TOP_FRAME_PATHS:
            image = pygame.image.load(frame_path).convert_alpha()
            scaled_image = pygame.transform.scale(
                image,
                (BC1_TOP_WIDTH, BC1_TOP_HEIGHT)
            )
            _cached_bc1_top_frames.append(scaled_image)

    return _cached_bc1_top_frames


def get_bc2_top_frames():
    global _cached_bc2_top_frames

    if _cached_bc2_top_frames is None:
        _cached_bc2_top_frames = []

        for frame_path in BC2_TOP_FRAME_PATHS:
            image = pygame.image.load(frame_path).convert_alpha()
            scaled_image = pygame.transform.scale(
                image,
                (BC2_TOP_WIDTH, BC2_TOP_HEIGHT)
            )
            _cached_bc2_top_frames.append(scaled_image)

    return _cached_bc2_top_frames


def get_current_frame(frames, frame_time_ms):
    frame_index = (pygame.time.get_ticks() // frame_time_ms) % len(frames)
    return frames[frame_index]


def draw_character(surface):
    bc1_image = get_bc1_image()
    bc2_image = get_bc2_image()

    bc1_top_frame = get_current_frame(get_bc1_top_frames(), BC1_TOP_FRAME_TIME_MS)
    bc2_top_frame = get_current_frame(get_bc2_top_frames(), BC2_TOP_FRAME_TIME_MS)

    surface.blit(bc1_image, (BC1_X, BC1_Y))
    surface.blit(bc1_top_frame, (BC1_TOP_X, BC1_TOP_Y))

    surface.blit(bc2_image, (BC2_X, BC2_Y))
    surface.blit(bc2_top_frame, (BC2_TOP_X, BC2_TOP_Y))