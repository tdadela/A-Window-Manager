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


    def draw_windows(self):
        n = len(self.windows)
        for i, window in enumerate(self.windows):
            print(int(self.width/n), int(self.height), int(i*self.width/n), 0)
            '''
            event.window.change_attributes(
                    width=int(self.width/n),
                    height=int(self.height),
                    x=int(i*self.width/n),
                    y=0
                    )
            window.map()
            '''
            window.configure(
                width=int(self.width/n),
                height=int(self.height),
                x=int(i*self.width/n),
                y=0
            )
        self.display.flush()  # ??
        self.display.sync()  # ??


    def handle_events(self):
        for window in self.windows:
            if window not in self.root_window.query_tree().children:
                self.windows.remove(window)
                self.draw_windows()
        logging.debug(self.display.pending_events())
        time.sleep(.1)
        if self.display.pending_events():
            event = self.display.next_event()
        else:
            return
        logging.debug(event)
        if event.type == X.MapRequest:
            self.windows.append(event.window)
            self.active = event.window
            '''
            event.window.configure(
                    width=self.width//2,
                    height=self.height//2,
                    x=self.width//4,
                    y=self.height//4
                    )
            '''
            event.window.map()
            self.draw_windows()
        elif event.type == X.KeyPress and event.detail == self.key_t:
            self.run_application(['/usr/bin/dmenu_run'])
        elif event.type == X.KeyPress and event.detail == self.key_q:
            if self.active is not None:
                self.active.destroy()
                self.windows.remove(self.active)
                self.active = None
                self.draw_windows()
        elif event.type == X.DestroyNotify:
            window = event.window
            self.windows.remove(window)
            print(len(self.windows))

        elif event.type == X.KeyPress and event.detail == self.key_f and self.active is not None:
            self.active.configure(
                    width=self.width,
                    height=self.height,
                    y=0,
                    x=0
                    )
            self.display.sync()

    def set_active(self):
        if self.root_window.query_pointer().child != self.root_window:
            self.active = self.root_window.query_pointer().child
        else:
            self.active = None


def main():
    logging.basicConfig(filename='wm.log', filemode='a', level=logging.DEBUG)
    logging.critical('Window manager started.')
    subprocess.Popen(["/usr/bin/feh", "--bg-fill", "bg.jpg"])
    while True:
        WindowManager.handle_events()
        WindowManager.set_active()


WindowManager = wm()

if __name__ == "__main__":
    main()
