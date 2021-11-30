''' A Window Manager'''
import time
import sys
import subprocess
import logging
from Xlib import X, XK
from Xlib.display import Display


class wm():
    '''Main Window Manager class'''

    def __init__(self):
        self.windows = []
        self.active = None
        self.display = Display()
        self.root_window = self.display.screen().root
        self.height = self.root_window.get_geometry().height
        self.width = self.root_window.get_geometry().width
        self.focus = None
        self.key_t = 28  # self.display.keysym_to_keycodes(XK.XK_T)
        self.key_f = 41
        self.key_q = 24
        self.root_window.change_attributes(
               event_mask=X.SubstructureRedirectMask)
        for i in [24, 28, 41]:
            self.root_window.grab_key(
                i, X.Mod4Mask, 1, X.GrabModeAsync, X.GrabModeAsync
            )

    def run_application(self, command):
        subprocess.Popen(command)


    def handle_events(self):
        logging.debug(self.display.pending_events())
        time.sleep(0.001)
        if self.display.pending_events():
            event = self.display.next_event()
        else:
            return
        logging.debug(event)
        if event.type == X.MapRequest:
            self.windows.append(event.window)
            self.active = event.window
            event.window.configure(width=844, height=844)
            self.display.sync()
            event.window.map()
        elif event.type == X.KeyPress and event.detail == self.key_t:
            self.run_application(['/usr/bin/dmenu_run'])
        elif event.type == X.KeyPress and event.detail == self.key_q:
            if self.active:
                self.active.destroy()
                self.windows.remove(self.active)
                self.active = None
        elif event.type == X.KeyPress and event.detail == self.key_f:
            self.active.configure(width=self.width, height=self.height)
            self.display.sync()


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.info('Window manager started.')
    subprocess.Popen(["/usr/bin/feh", "--bg-fill", "bg.jpg"])
    while True:
        WindowManager.handle_events()


WindowManager = wm()

if __name__ == "__main__":
    main()
