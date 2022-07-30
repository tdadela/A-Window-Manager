'''Processing user's config'''
import logging
from Xlib import X
from Xlib.display import Display
from . import config
from . import utils


def on_startup():
    '''User startup script.'''
    background_file = config.BACKGROUND_FILE
    utils.run_application(['python', 'bar.py'])
    utils.run_application(
        [utils.get_program_location(config.BACKGROUND_SETTER),
            config.BACKGROUND_SETTER_ARGS, background_file]
    )


def key_to_keycodes(char):
    '''Convert key to its key code'''
    key_code = list(Display().keysym_to_keycodes(ord(char)))[0][0]
    return key_code


shortcut = {}
for name, keyname in config.shortcuts.items():
    shortcut[name] = key_to_keycodes(keyname)

# workspace_shortcut = {}
workspace_number = {}
for i, key in enumerate(config.workspace_keys):
    keycode = key_to_keycodes(key)
    # workspace_shortcut[f'workspace_{i+1}_key'] = keycode
    workspace_number[keycode] = i


NO_WORKSPACES = len(config.workspace_keys)
MODKEY_MASK = X.Mod1Mask if config.MODKEY == '1' else X.Mod4Mask
CHANGE_WINDOW_WORKSPACE = MODKEY_MASK | X.ShiftMask
LOG_LEVEL = logging.getLevelName(config.LOGGING_LEVEL)
