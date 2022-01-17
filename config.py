'''Config file'''
import lib.utils


def on_startup():
    '''User startup script.'''
    background_file = "bg.jpg"
    lib.utils.run_application(
        f"{lib.utils.get_program_location('feh')} --bg-fill {background_file}"
        .split()
    )


shortcuts = {
    "fullscreen_key": 'f',
    "close_window_key": 'q',
    "launcher_key": 't',
    "workspace_1_key": '1',
    "workspace_2_key": '2'
}

LOGFILE = 'wm.log'
LAUNCHER = 'dmenu_run'
