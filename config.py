'''Config file'''
import lib.utils


def on_startup():
    '''User startup script.'''
    background_file = "bg.jpg"
    lib.utils.run_application(
        f"{lib.utils.get_program_location('feh')} --bg-fill {background_file}"
        .split()
    )
