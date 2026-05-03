import pygame


BC1_FRAME_PATHS = [
    "img_keys/1C1.png",
    "img_keys/1C2.png",
]

BC2_FRAME_PATHS = [
    "img_keys/2C1.png",
    "img_keys/2C2.png",
    "img_keys/2C3.png",
]

BC1_FRAME_TIME_MS = 700
BC2_FRAME_TIME_MS = 700

# Adjust these to move/resize BC1 everywhere.
BC1_X = 36
BC1_Y = 68
BC1_WIDTH = 175
BC1_HEIGHT = 185

# Adjust these to move/resize BC2 everywhere.
BC2_X = 805
BC2_Y = 68
BC2_WIDTH = 175
BC2_HEIGHT = 185


_cached_bc1_frames = None
_cached_bc2_frames = None


def get_bc1_frames():
    global _cached_bc1_frames

    if _cached_bc1_frames is None:
        _cached_bc1_frames = []

        for frame_path in BC1_FRAME_PATHS:
            image = pygame.image.load(frame_path).convert_alpha()
            scaled_image = pygame.transform.scale(
                image,
                (BC1_WIDTH, BC1_HEIGHT)
            )
            _cached_bc1_frames.append(scaled_image)

    return _cached_bc1_frames


def get_bc2_frames():
    global _cached_bc2_frames

    if _cached_bc2_frames is None:
        _cached_bc2_frames = []

        for frame_path in BC2_FRAME_PATHS:
            image = pygame.image.load(frame_path).convert_alpha()
            scaled_image = pygame.transform.scale(
                image,
                (BC2_WIDTH, BC2_HEIGHT)
            )
            _cached_bc2_frames.append(scaled_image)

    return _cached_bc2_frames


def get_current_frame(frames, frame_time_ms):
    frame_index = (pygame.time.get_ticks() // frame_time_ms) % len(frames)
    return frames[frame_index]

def draw_character(surface):
    bc1_frame = get_current_frame(get_bc1_frames(), BC1_FRAME_TIME_MS)
    bc2_frame = get_current_frame(get_bc2_frames(), BC2_FRAME_TIME_MS)

    surface.blit(bc1_frame, (BC1_X, BC1_Y))
    surface.blit(bc2_frame, (BC2_X, BC2_Y))