''' A Window Manager'''
import logging
from Xlib import X, XK
from Xlib.display import Display
import utils
import config


class wm():
    '''Main Window Manager class'''

    def __init__(self):
        self.windows = []
        self.active = None
        self.fullscreen = False
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

    def draw_windows(self):
        '''Draw windows in horizontal tiling mode'''
        no_windows = len(self.windows)
        prev_end = -1
        for i, window in enumerate(self.windows):
            if i == no_windows - 1:
                fill_till = self.width
            else:
                fill_till = self.width // no_windows * (i + 1)
            window.configure(
                width=fill_till - prev_end,
                height=self.height,
                x=prev_end + 1,
                y=0
            )
            prev_end = fill_till
        self.display.sync()

    def handle_events(self):
        '''Handle X11 events'''
        for window in self.windows:
            if window not in self.root_window.query_tree().children:
                self.windows.remove(window)
                self.draw_windows()
        event = self.display.next_event()
        self.set_active()
        logging.debug(event)
        if event.type == X.MapRequest:
            self.windows.append(event.window)
            self.active = event.window
            event.window.map()
            self.draw_windows()
        elif event.type == X.DestroyNotify:
            window = event.window
            window.unmap()
            self.windows.remove(window)
        elif event.type == X.KeyPress:
            if event.detail == self.key_t:
                utils.run_application(
                    utils.get_program_location("dmenu_run").split()
                )

            elif event.detail == self.key_q:
                if self.active is not None:
                    self.active.destroy()
                    self.windows.remove(self.active)
                    self.active = None
                    self.draw_windows()

            elif event.detail == self.key_f and self.active is not None:
                if not self.fullscreen:
                    self.active.configure(
                        stack_mode=X.Above,
                        width=self.width,
                        height=self.height,
                        y=0,
                        x=0
                    )
                    self.display.sync()
                else:
                    self.draw_windows()

                self.fullscreen = not self.fullscreen

    def set_active(self):
        '''Set focused windows'''
        if self.root_window.query_pointer().child != self.root_window:
            self.active = self.root_window.query_pointer().child
            if isinstance(self.active, int):
                self.active = None
        else:
            self.active = None


def main():
    '''Main loop for window manager events.'''
    logging.basicConfig(filename='wm.log', filemode='w', level=logging.DEBUG)
    logging.debug('Window manager started.')
    config.on_startup()
    while True:
        WindowManager.handle_events()


WindowManager = wm()

if __name__ == "__main__":
    main()
