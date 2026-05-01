#################################
# CSC 102 Defuse the Bomb Project
# GUI and Phase class definitions
# Team: 
#################################

# import the configs
from bomb_configs import *
# other imports
import pygame
from threading import Thread
from time import sleep
import os
import sys
pygame.init()

SCREEN_W, SCREEN_H = 1024, 576
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Rectangle Test")

bg = pygame.image.load("base.png").convert()
bg = pygame.transform.scale(bg, (SCREEN_W, SCREEN_H))

rect_pos = pygame.Rect(0, 0, SCREEN_W, SCREEN_H)
rect_pos2 = pygame.Rect(0, 240, SCREEN_W, 240)
rect_surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
rect_surf.fill((0, 0, 0, 160))
messages = ["You have put our name to question for too long.....",]
import time as _time

#########
# classes
#########
# the LCD display GUI (pygame-based)
class LabelLike:
    def __init__(self, text=""):
        self._text = text
        self._destroyed = False
    def __setitem__(self, key, value):
        if key == "text":
            self._text = value
    def __getitem__(self, key):
        if key == "text":
            return self._text
    def destroy(self):
        self._text = ""
        self._destroyed = True
    def __str__(self):
        return self._text

class ButtonLike:
    def __init__(self, text, rect, callback):
        self.text = text
        self.rect = rect
        self.callback = callback
        self._destroyed = False
    def destroy(self):
        self._destroyed = True

class Lcd:
    def __init__(self, size=(1024, 576)):
        pygame.init()
        pygame.font.init()
        self.width, self.height = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Defuse the Bomb")
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont("Courier New", 16)
        self.font_med = pygame.font.SysFont("Courier New", 22)
        self.bg = (0, 0, 0)
        self.fg = (0, 255, 0)
        self.white = (255, 255, 255)
        self.red = (200, 0, 0)

        # timers and button refs
        self._timer = None
        self._button = None

        # scheduled callbacks (due_ms, func, args)
        self._scheduled = []

        # UI elements
        self._lscroll = LabelLike("")
        self._ltimer = LabelLike("")
        self._lkeypad = LabelLike("")
        self._lwires = LabelLike("")
        self._lbutton = LabelLike("")
        self._ltoggles = LabelLike("")
        self._lstrikes = LabelLike("")

        self._ui_buttons = []
        self._bpause = None
        self._bquit = None
        self._bretry = None

        # initial boot layout
        self.setupBoot()

    def setupBoot(self):
        self._lscroll = LabelLike("")

    def setup(self):
        self._ltimer = LabelLike("Time left: ")
        self._lkeypad = LabelLike("Keypad phase: ")
        self._lwires = LabelLike("Wires phase: ")
        self._lbutton = LabelLike("Button phase: ")
        self._ltoggles = LabelLike("Toggles phase: ")
        self._lstrikes = LabelLike("Strikes left: ")

        if (SHOW_BUTTONS):
            pause_rect = pygame.Rect(30, self.height - 70, 140, 45)
            quit_rect = pygame.Rect(self.width - 170, self.height - 70, 140, 45)
            self._bpause = ButtonLike("Pause", pause_rect, self.pause)
            self._bquit = ButtonLike("Quit", quit_rect, self.quit)
            self._ui_buttons.extend([self._bpause, self._bquit])

    # scheduling like tkinter's after
    def after(self, delay_ms, func, *args):
        due = pygame.time.get_ticks() + int(delay_ms)
        self._scheduled.append((due, func, args))

    def _process_scheduled(self):
        now = pygame.time.get_ticks()
        ready = [s for s in self._scheduled if s[0] <= now]
        for due, func, args in ready:
            try:
                func(*args)
            except Exception as e:
                print("Scheduled call error:", e)
            try:
                self._scheduled.remove((due, func, args))
            except ValueError:
                pass

    # lets us pause/unpause the timer (7-segment display)
    def setTimer(self, timer):
        self._timer = timer

    # lets us turn off the pushbutton's RGB LED
    def setButton(self, button):
        self._button = button

    def pause(self):
        if (self._timer):
            try:
                self._timer.pause()
            except Exception:
                pass

    # setup the conclusion GUI (explosion/defusion)
    def conclusion(self, success=False):
        self._lscroll["text"] = ""
        self._ltimer.destroy()
        self._lkeypad.destroy()
        self._lwires.destroy()
        self._lbutton.destroy()
        self._ltoggles.destroy()
        self._lstrikes.destroy()
        for b in list(self._ui_buttons):
            b.destroy()
        self._ui_buttons = []

        # retry and quit buttons (centered)
        retry_rect = pygame.Rect(self.width // 2 - 140, self.height // 2 - 20, 120, 40)
        quit_rect = pygame.Rect(self.width // 2 + 20, self.height // 2 - 20, 120, 40)
        self._bretry = ButtonLike("Retry", retry_rect, self.retry)
        self._bquit = ButtonLike("Quit", quit_rect, self.quit)
        self._ui_buttons.extend([self._bretry, self._bquit])

    # re-attempts the bomb (after an explosion or a successful defusion)
    def retry(self):
        os.execv(sys.executable, [sys.executable] + sys.argv)

    # quits the GUI, resetting some components
    def quit(self):
        if (RPi and self._timer):
            try:
                self._timer._running = False
                self._timer._component.blink_rate = 0
                self._timer._component.fill(0)
                for pin in self._button._rgb:
                    pin.value = True
            except Exception:
                pass
        pygame.quit()
        sys.exit(0)

    # event handling from the main loop
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for b in self._ui_buttons:
                if not getattr(b, '_destroyed', False) and b.rect.collidepoint(pos):
                    try:
                        b.callback()
                    except Exception as e:
                        print('Button callback error', e)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.pause()
            elif event.key == pygame.K_q:
                self.quit()

    # render the GUI (call each frame)
    def render(self):
        self.screen.fill(self.bg)
        # scroll/boot text at top
        try:
            lines = self._lscroll["text"].splitlines()
        except Exception:
            lines = [str(self._lscroll)]
        y = 8
        for line in lines:
            surf = self.font_small.render(line, True, self.white)
            self.screen.blit(surf, (10, y))
            y += self.font_small.get_linesize()

        # main labels
        labels = [
            (self._ltimer, 90),
            (self._lkeypad, 130),
            (self._lwires, 170),
            (self._lbutton, 210),
            (self._ltoggles, 250),
            (self._lstrikes, 290),
        ]
        for lbl, y in labels:
            try:
                text = lbl["text"]
            except Exception:
                text = str(lbl)
            surf = self.font_med.render(text, True, self.fg)
            self.screen.blit(surf, (16, y))

        # draw buttons
        for b in self._ui_buttons:
            if getattr(b, '_destroyed', False):
                continue
            pygame.draw.rect(self.screen, self.red, b.rect)
            txt = self.font_med.render(b.text, True, self.white)
            txt_rect = txt.get_rect(center=b.rect.center)
            self.screen.blit(txt, txt_rect)

        pygame.display.flip()


# template (superclass) for various bomb components/phases
class PhaseThread(Thread):
    def __init__(self, name, component=None, target=None):
        super().__init__(name=name, daemon=True)
        # phases have an electronic component (which usually represents the GPIO pins)
        self._component = component
        # phases have a target value (e.g., a specific combination on the keypad, the proper jumper wires to "cut", etc)
        self._target = target
        # phases can be successfully defused
        self._defused = False
        # phases can be failed (which result in a strike)
        self._failed = False
        # phases have a value (e.g., a pushbutton can be True/Pressed or False/Released, several jumper wires can be "cut"/False, etc)
        self._value = None
        # phase threads are either running or not
        self._running = False

# the timer phase
class Timer(PhaseThread):
    def __init__(self, component, initial_value, name="Timer"):
        super().__init__(name, component)
        # the default value is the specified initial value
        self._value = initial_value
        # is the timer paused?
        self._paused = False
        # initialize the timer's minutes/seconds representation
        self._min = ""
        self._sec = ""
        # by default, each tick is 1 second
        self._interval = 1

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            if (not self._paused):
                # update the timer and display its value on the 7-segment display
                self._update()
                self._component.print(str(self))
                # wait 1s (default) and continue
                sleep(self._interval)
                # the timer has expired -> phase failed (explode)
                if (self._value == 0):
                    self._running = False
                self._value -= 1
            else:
                sleep(0.1)

    # updates the timer (only internally called)
    def _update(self):
        self._min = f"{self._value // 60}".zfill(2)
        self._sec = f"{self._value % 60}".zfill(2)

    # pauses and unpauses the timer
    def pause(self):
        # toggle the paused state
        self._paused = not self._paused
        # blink the 7-segment display when paused
        self._component.blink_rate = (2 if self._paused else 0)

    # returns the timer as a string (mm:ss)
    def __str__(self):
        return f"{self._min}:{self._sec}"

# the keypad phase
class Keypad(PhaseThread):
    def __init__(self, component, target, name="Keypad"):
        super().__init__(name, component, target)
        # the default value is an empty string
        self._value = ""

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            # process keys when keypad key(s) are pressed
            if (self._component.pressed_keys):
                # debounce
                while (self._component.pressed_keys):
                    try:
                        # just grab the first key pressed if more than one were pressed
                        key = self._component.pressed_keys[0]
                    except:
                        key = ""
                    sleep(0.1)
                # log the key
                self._value += str(key)
                # the combination is correct -> phase defused
                if (self._value == self._target):
                    self._defused = True
                # the combination is incorrect -> phase failed (strike)
                elif (self._value != self._target[0:len(self._value)]):
                    self._failed = True
            sleep(0.1)

    # returns the keypad combination as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return self._value

# the jumper wires phase
class Wires(PhaseThread):
    def __init__(self, component, target, name="Wires"):
        super().__init__(name, component, target)

    # runs the thread
    def run(self):
        # TODO
        pass

    # returns the jumper wires state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            # TODO
            pass

# the pushbutton phase
class Button(PhaseThread):
    def __init__(self, component_state, component_rgb, target, color, timer, name="Button"):
        super().__init__(name, component_state, target)
        # the default value is False/Released
        self._value = False
        # has the pushbutton been pressed?
        self._pressed = False
        # we need the pushbutton's RGB pins to set its color
        self._rgb = component_rgb
        # the pushbutton's randomly selected LED color
        self._color = color
        # we need to know about the timer (7-segment display) to be able to determine correct pushbutton releases in some cases
        self._timer = timer

    # runs the thread
    def run(self):
        self._running = True
        # set the RGB LED color
        self._rgb[0].value = False if self._color == "R" else True
        self._rgb[1].value = False if self._color == "G" else True
        self._rgb[2].value = False if self._color == "B" else True
        while (self._running):
            # get the pushbutton's state
            self._value = self._component.value
            # it is pressed
            if (self._value):
                # note it
                self._pressed = True
            # it is released
            else:
                # was it previously pressed?
                if (self._pressed):
                    # check the release parameters
                    # for R, nothing else is needed
                    # for G or B, a specific digit must be in the timer (sec) when released
                    if (not self._target or self._target in self._timer._sec):
                        self._defused = True
                    else:
                        self._failed = True
                    # note that the pushbutton was released
                    self._pressed = False
            sleep(0.1)

    # returns the pushbutton's state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return str("Pressed" if self._value else "Released")

# the toggle switches phase
class Toggles(PhaseThread):
    def __init__(self, component, target, name="Toggles"):
        super().__init__(name, component, target)

    # runs the thread
    def run(self):
        # TODO
        pass

    # returns the toggle switches state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            # TODO
            pass
