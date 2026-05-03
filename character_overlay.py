import pygame


BC1_FRAME_PATHS = [
    "img_keys/1C1.png",
    "img_keys/1C2.png",
]

BC1_FRAME_TIME_MS = 700

# Adjust these to move/resize the character everywhere.
BC1_X = 36
BC1_Y = 55
BC1_WIDTH = 175
BC1_HEIGHT = 200


_cached_bc1_frames = None


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


def get_current_frame(frames, frame_time_ms):
    frame_index = (pygame.time.get_ticks() // frame_time_ms) % len(frames)
    return frames[frame_index]


def draw_character(surface):
    bc1_frame = get_current_frame(get_bc1_frames(), BC1_FRAME_TIME_MS)
    surface.blit(bc1_frame, (BC1_X, BC1_Y))