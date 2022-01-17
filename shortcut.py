import config
from Xlib.display import Display


def key_to_keycodes(key):
    '''Convert key to its key code'''
    key_code = list(Display().keysym_to_keycodes(ord(key)))[0][0]
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
