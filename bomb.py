#################################
# CSC 102 Defuse the Bomb Project
# Main program
# Team: 
#################################

# import the configs
from bomb_configs import *
from bomb_phases import *
import pygame
import sys
from pathlib import Path
import importlib.util
import threading
import queue
import time
from display_utils import create_fullscreen_display, DESIGN_SIZE

# class Lcd:
#     def __init__(self, size=(1024, 576)):
#         pygame.init()
#         pygame.font.init()
#         self.width, self.height = size
#         self.screen = create_fullscreen_display("Defuse the Bomb")
#         self.clock = pygame.time.Clock()
#         self.font_small = pygame.font.SysFont("Courier New", 16)
#         self.font_med = pygame.font.SysFont("Courier New", 22)
#         self.bg = (0, 0, 0)


def import_game_module(module_name, file_name):
    project_dir = Path(__file__).resolve().parent
    game_path = project_dir / file_name

    spec = importlib.util.spec_from_file_location(module_name, game_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# import pygame intro module by file path
def import_pygame_intro():
    return import_game_module("pygame_intro", "pygameIntro.py")

# import the wires GUI module by file path
def import_wires_gui():
    return import_game_module("wires_gui", "Wires GUI.py")


# import the melody game module by file path
def import_melody_game():
    return import_game_module("melody_game", "Melody Game.py")


# import the safe/keypad game module by file path
def import_safe_game():
    return import_game_module("safe_game", "Safe Game.py")


# import the keypad intro module by file path
def import_keypad_intro():
    return import_game_module("keypad_intro", "keypad_intro.py")


# import the vent intro module by file path
def import_vent_intro():
    return import_game_module("vent_intro", "ventintro.py")


# import the vent minigame module by file path
def import_fling_test():
    return import_game_module("fling_test", "flingtest.py")


# import the wires intro module by file path
def import_wires_intro():
    return import_game_module("wires_intro", "wires_intro.py")


# import the switch intro module by file path
def import_switch_intro():
    return import_game_module("switch_intro", "switch_intro.py")


# import the switchG module by file path
def import_switch_g():
    return import_game_module("switch_g", "SwitchG.py")


# import the outro module by file path
def import_outro():
    return import_game_module("outro", "outro.py")


# import the game over screen module by file path
def import_gameover():
    return import_game_module("gameover", "gameover.py")


class BombTimerThread(threading.Thread):
    def __init__(self, seconds):
        super().__init__(daemon=True)
        self.seconds_left = seconds
        self.expired = False
        self.running = True
        self.paused = False
        self.lock = threading.Lock()

    def run(self):
        while True:
            time.sleep(1)

            with self.lock:
                if not self.running:
                    break

                if self.paused:
                    continue

                self.seconds_left -= 1

                if self.seconds_left <= 0:
                    self.seconds_left = 0
                    self.expired = True
                    self.running = False
                    break

    def stop(self):
        with self.lock:
            self.running = False

    def pause(self):
        with self.lock:
            self.paused = True

    def get_time_left(self):
        with self.lock:
            return self.seconds_left

    def is_expired(self):
        with self.lock:
            return self.expired


def run_program(name, module_loader, screen, clock, bomb_timer):
    if bomb_timer.is_expired():
        return False

    try:
        module = module_loader()
        result = module.main(screen, clock)
    except Exception as error:
        print(f"{name} crashed: {error}")
        return False

    if bomb_timer.is_expired():
        return False

    return result


def setup_phases():
    global timer, keypad, wires, button, toggles

    timer = Timer(component_7seg, COUNTDOWN)
    keypad = Keypad(component_keypad, keypad_target)
    wires = Wires(component_wires, wires_target)
    button = Button(component_button_state, component_button_RGB, button_target, button_color, timer)
    toggles = Toggles(component_toggles, toggles_target)

    timer.start()
    keypad.start()
    wires.start()
    button.start()
    toggles.start()


def stop_hardware_phases():
    if not RPi:
        return

    for phase_name in ("timer", "keypad", "wires", "button", "toggles"):
        phase = globals().get(phase_name)

        if phase is not None:
            phase._running = False

    if "component_7seg" in globals():
        component_7seg.blink_rate = 0
        component_7seg.fill(0)

    if "button" in globals():
        for pin in button._rgb:
            pin.value = True


def show_game_over(screen, clock):
    pygame.mixer.stop()
    pygame.mixer.music.stop()

    gameover = import_gameover()
    gameover.main(screen, clock)

    return False


def main():
    pygame.init()
    pygame.mixer.init()

    screen = create_fullscreen_display("Defuse the Bomb")
    clock = pygame.time.Clock()

    bomb_timer = BombTimerThread(COUNTDOWN)
    bomb_timer.start()

    if RPi:
        setup_phases()

    game_sequence = [
        ("Intro", import_pygame_intro, False),
        ("Vent Intro", import_vent_intro, False),
        ("Vent Minigame", import_fling_test, True),
        ("Wires Intro", import_wires_intro, False),
        ("Wires Game", import_wires_gui, True),
        ("Keypad Intro", import_keypad_intro, False),
        ("Safe Game", import_safe_game, True),
        ("Switch Intro", import_switch_intro, False),
        ("Switch Game", import_switch_g, True),
        ("Outro", import_outro, False),
    ]

    for program_name, module_loader, death_on_fail in game_sequence:
        if bomb_timer.is_expired():
            bomb_timer.stop()
            stop_hardware_phases()
            return show_game_over(screen, clock)

        if program_name == "Vent Intro":
            pygame.mixer.music.load("img_keys/10. Aphex Twin - Mt Saint Michel + Saint Michaels Mount.mp3")
            pygame.mixer.music.set_volume(10.00)
            pygame.mixer.music.play()

        program_result = run_program(
            program_name,
            module_loader,
            screen,
            clock,
            bomb_timer
        )

        if DEBUG and death_on_fail:
            print(f"DEBUG mode: forcing {program_name} to return True")
            program_result = True

        if program_result and program_name == "Switch Game":
            pygame.mixer.music.stop()
            bomb_timer.pause()

            if RPi and "timer" in globals() and not timer._paused:
                timer.pause()

        if bomb_timer.is_expired():
            bomb_timer.stop()
            stop_hardware_phases()
            return show_game_over(screen, clock)

        if not program_result:
            bomb_timer.stop()
            stop_hardware_phases()

            if death_on_fail:
                return show_game_over(screen, clock)

            pygame.quit()
            return False

    bomb_timer.stop()
    stop_hardware_phases()
    pygame.quit()
    return True

if __name__ == "__main__":
    raise SystemExit(main())
