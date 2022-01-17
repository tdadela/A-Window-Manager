'''Config file'''
import lib.utils


def on_startup():
    '''User startup script.'''
    background_file = 'bg.jpg'
    lib.utils.run_application(
        f"{lib.utils.get_program_location('feh')} --bg-fill {background_file}"
        .split()
    )


shortcuts = {
    'full_screen_key': 'f',
    'close_window_key': 'q',
    'launcher_key': 't',
}

workspace_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
NO_WORKSPACES = len(workspace_keys)

LOGFILE = 'wm.log'
LAUNCHER = 'dmenu_run'
