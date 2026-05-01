#################################
# CSC 102 Defuse the Bomb Project
# Main program
# Team: 
#################################

# import the configs
from bomb_configs import *
# import the phases
from bomb_phases import *
import pygame
import sys
from pathlib import Path
import importlib.util


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


# import the switches GUI module by file path
def import_switches_gui():
    return import_game_module("switches_gui", "Switches GUI.py")

###########
# functions
###########
# generates the bootup sequence on the LCD
def bootup(n=0):
    gui._lscroll["text"] = boot_text.replace("\x00", "")
    # configure the remaining GUI widgets
    gui.setup()
    # setup the phase threads, execute them, and check their statuses
    if (RPi):
        setup_phases()
        check_phases()
    # if we're animating
   
# sets up the phase threads
def setup_phases():
    global timer, keypad, wires, button, toggles
    
    # setup the timer thread
    timer = Timer(component_7seg, COUNTDOWN)
    # bind the 7-segment display to the LCD GUI so that it can be paused/unpaused from the GUI
    # gui.setTimer(timer)
    # setup the keypad thread
    keypad = Keypad(component_keypad, keypad_target)
    # setup the jumper wires thread
    wires = Wires(component_wires, wires_target)
    # setup the pushbutton thread
    button = Button(component_button_state, component_button_RGB, button_target, button_color, timer)
    # bind the pushbutton to the LCD GUI so that its LED can be turned off when we quit
    # gui.setButton(button)
    # setup the toggle switches thread
    toggles = Toggles(component_toggles, toggles_target)

    # start the phase threads
    timer.start()
    keypad.start()
    wires.start()
    button.start()
    toggles.start()

# checks the phase threads
def check_phases():
    global active_phases
    
    # check the timer
    if (timer._running):
        # update the GUI
        gui._ltimer["text"] = f"Time left: {timer}"
    else:
        # the countdown has expired -> explode!
        # turn off the bomb and render the conclusion GUI
        turn_off()
        gui.after(100, gui.conclusion, False)
        # don't check any more phases
        return
    # check the keypad
    if (keypad._running):
        # update the GUI
        gui._lkeypad["text"] = f"Combination: {keypad}"
        # the phase is defused -> stop the thread
        if (keypad._defused):
            keypad._running = False
            active_phases -= 1
        # the phase has failed -> strike
        elif (keypad._failed):
            strike()
            # reset the keypad
            keypad._failed = False
            keypad._value = ""
    # check the wires
    if (wires._running):
        # update the GUI
        gui._lwires["text"] = f"Wires: {wires}"
        # the phase is defused -> stop the thread
        if (wires._defused):
            wires._running = False
            active_phases -= 1
        # the phase has failed -> strike
        elif (wires._failed):
            strike()
            # reset the wires
            wires._failed = False
    # check the button
    if (button._running):
        # update the GUI
        gui._lbutton["text"] = f"Button: {button}"
        # the phase is defused -> stop the thread
        if (button._defused):
            button._running = False
            active_phases -= 1
        # the phase has failed -> strike
        elif (button._failed):
            strike()
            # reset the button
            button._failed = False
    # check the toggles
    if (toggles._running):
        # update the GUI
        gui._ltoggles["text"] = f"Toggles: {toggles}"
        # the phase is defused -> stop the thread
        if (toggles._defused):
            toggles._running = False
            active_phases -= 1
        # the phase has failed -> strike
        elif (toggles._failed):
            strike()
            # reset the toggles
            toggles._failed = False

    # note the strikes on the GUI
    gui._lstrikes["text"] = f"Strikes left: {strikes_left}"
    # too many strikes -> explode!
    if (strikes_left == 0):
        # turn off the bomb and render the conclusion GUI
        turn_off()
        gui.after(1000, gui.conclusion, False)
        # stop checking phases
        return

    # the bomb has been successfully defused!
    if (active_phases == 0):
        # turn off the bomb and render the conclusion GUI
        turn_off()
        gui.after(100, gui.conclusion, True)
        # stop checking phases
        return

    # check the phases again after a slight delay
    gui.after(100, check_phases)

# handles a strike
def strike():
    global strikes_left
    
    # note the strike
    strikes_left -= 1

# turns off the bomb
def turn_off():
    # stop all threads
    timer._running = False
    keypad._running = False
    wires._running = False
    button._running = False
    toggles._running = False

    # turn off the 7-segment display
    component_7seg.blink_rate = 0
    component_7seg.fill(0)
    # turn off the pushbutton's LED
    for pin in button._rgb:
        pin.value = True

def main():
    #setup_phases()

    pygame.init()
    pygame.mixer.init()

=======
>>>>>>> 71efed5e27033d32e6e9a58e77a0adcc3a76879d
    screen = pygame.display.set_mode((1024, 576))
    pygame.display.set_caption("Defuse the Bomb")
    clock = pygame.time.Clock()

    # launch the pygame intro first
    pygame_intro = import_pygame_intro()
    intro_done = pygame_intro.main(screen, clock)

    if not intro_done:
        pygame.quit()
        return False

    # move on to wires GUI
    wires_gui = import_wires_gui()
    wires_won = wires_gui.main(screen, clock)
<<<<<<< HEAD
>>>>>>> 71efed5e27033d32e6e9a58e77a0adcc3a76879d
=======
>>>>>>> 71efed5e27033d32e6e9a58e77a0adcc3a76879d
=======
=======
=======
>>>>>>> 71efed5e27033d32e6e9a58e77a0adcc3a76879d
    screen = pygame.display.set_mode((1024, 576))
    pygame.display.set_caption("Defuse the Bomb")
    clock = pygame.time.Clock()

    # launch the pygame intro first
    pygame_intro = import_pygame_intro()
    intro_done = pygame_intro.main(screen, clock)

    if not intro_done:
        pygame.quit()
        return False

    # move on to wires GUI
    wires_gui = import_wires_gui()
    wires_won = wires_gui.main(screen, clock)
<<<<<<< HEAD
>>>>>>> 71efed5e27033d32e6e9a58e77a0adcc3a76879d
=======
>>>>>>> 71efed5e27033d32e6e9a58e77a0adcc3a76879d

    # if wires fail, quit immediately
    if not wires_won:
        pygame.quit()
        return False

    # safe game
    safe_game = import_safe_game()
    safe_won = safe_game.main(screen, clock)

    if not safe_won:
        pygame.quit()
        return False

    # switches game
    switches_gui = import_switches_gui()
    switches_won = switches_gui.main(screen, clock)

    if not switches_won:
        pygame.quit()
        return False

    pygame.quit()
    return True


######
# MAIN
######

if __name__ == "__main__":
    raise SystemExit(main())
gui = Lcd()

# initialize the bomb strikes and active phases (i.e., not yet defused)
strikes_left = NUM_STRIKES
active_phases = NUM_PHASES

# "boot" the bomb (schedule the bootup)
gui = Lcd()

# initialize the bomb strikes and active phases (i.e., not yet defused)
strikes_left = NUM_STRIKES
active_phases = NUM_PHASES

# "boot" the bomb (schedule the bootup)
gui.after(100, bootup)

# main pygame loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gui.quit()
        else:
            gui.handle_event(event)

    # run any scheduled callbacks
    gui._process_scheduled()

    # render the GUI
    gui.render()

    # cap the frame rate
    clock.tick(30)
