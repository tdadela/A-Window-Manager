import config
from Xlib.display import Display

shortcut = {}
for short in config.shortcuts.keys():
    shortcut[short] = list(Display().keysym_to_keycodes(
        ord(config.shortcuts[short])))[0][0]
