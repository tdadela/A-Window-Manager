import utils

def onStartup():
    '''User startup script.'''
    background_file = "bg.jpg"
    utils.run_application(f"{utils.get_program_location('feh')} --bg-fill {background_file}".split())