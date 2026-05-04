import pygame
import random


BC1_FRAME_PATHS = [
    "img_keys/1C1.png",
    "img_keys/1C2.png",
    "img_keys/1C3.png",
]

BC2_FRAME_PATHS = [
    "img_keys/2C1.png",
    "img_keys/2C2.png",
    "img_keys/2C3.png",
]

BC1_SPECIAL_FRAME_PATHS = [
    "img_keys/1CLaugh.png",
    "img_keys/1CSpeak.png",
]

BC1_FRAME_TIME_MS = 700
BC2_FRAME_TIME_MS = 700
BC1_SPECIAL_CHANCE = 0.20

# Adjust these to move/resize BC1 everywhere.
BC1_X = 36
BC1_Y = 53
BC1_WIDTH = 180
BC1_HEIGHT = 200

# Adjust these to move/resize BC2 everywhere.
BC2_X = 803
BC2_Y = 50
BC2_WIDTH = 182
BC2_HEIGHT = 200


_cached_bc1_frames = None
_cached_bc2_frames = None

_bc1_last_rotation_index = None
_bc1_current_frame = None


def load_scaled_frames(frame_paths, width, height):
    frames = []

    for frame_path in frame_paths:
        image = pygame.image.load(frame_path).convert_alpha()
        scaled_image = pygame.transform.scale(
            image,
            (width, height)
        )
        frames.append(scaled_image)

    return frames


def get_bc1_frames():
    global _cached_bc1_frames

    if _cached_bc1_frames is None:
        _cached_bc1_frames = load_scaled_frames(
            BC1_FRAME_PATHS,
            BC1_WIDTH,
            BC1_HEIGHT
        )

    return _cached_bc1_frames


def get_bc1_special_frames():
    global _cached_bc1_special_frames

    if _cached_bc1_special_frames is None:
        _cached_bc1_special_frames = load_scaled_frames(
            BC1_SPECIAL_FRAME_PATHS,
            BC1_WIDTH,
            BC1_HEIGHT
        )

    return _cached_bc1_special_frames


def get_bc2_frames():
    global _cached_bc2_frames

    if _cached_bc2_frames is None:
        _cached_bc2_frames = load_scaled_frames(
            BC2_FRAME_PATHS,
            BC2_WIDTH,
            BC2_HEIGHT
        )

    return _cached_bc2_frames


def get_current_frame(frames, frame_time_ms):
    frame_index = (pygame.time.get_ticks() // frame_time_ms) % len(frames)
    return frames[frame_index]


def get_current_bc1_frame():
    global _bc1_last_rotation_index
    global _bc1_current_frame

    bc1_frames = get_bc1_frames()
    bc1_special_frames = get_bc1_special_frames()

    rotation_index = pygame.time.get_ticks() // BC1_FRAME_TIME_MS

    if rotation_index != _bc1_last_rotation_index:
        normal_frame_index = rotation_index % len(bc1_frames)

        if random.random() < BC1_SPECIAL_CHANCE:
            _bc1_current_frame = random.choice(bc1_special_frames)
        else:
            _bc1_current_frame = bc1_frames[normal_frame_index]

        _bc1_last_rotation_index = rotation_index

    return _bc1_current_frame


def draw_character(surface):
    bc1_frame = get_current_bc1_frame()
    bc2_frame = get_current_frame(get_bc2_frames(), BC2_FRAME_TIME_MS)

    surface.blit(bc1_frame, (BC1_X, BC1_Y))
    surface.blit(bc2_frame, (BC2_X, BC2_Y))