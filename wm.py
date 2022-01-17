''' A Window Manager'''
import logging
import itertools
from Xlib import X, XK
from Xlib.display import Display
import lib.utils
import config
from lib.workspace import Workspace
from lib.workspace_manager import WorkspaceManager
from shortcut import shortcut, workspace_number


class wm:
    '''Main Window Manager class'''

    def __init__(self):
        self.wsm = WorkspaceManager(config.NO_WORKSPACES)

        self.focus = None
        self.active = None
        self.fullscreen = False
        self.display = Display()
        self.root_window = self.display.screen().root
        self.height = self.root_window.get_geometry().height
        self.width = self.root_window.get_geometry().width
        self.root_window.change_attributes(
            event_mask=X.SubstructureRedirectMask)
        for i in itertools.chain(shortcut.values(), workspace_number.keys()):
            self.root_window.grab_key(
                i, X.Mod4Mask, 1, X.GrabModeAsync, X.GrabModeAsync
            )

    def draw_windows(self):
        '''Draw windows in horizontal tiling mode'''
        windows_to_draw = self.wsm.get_current_workspace().windows
        no_windows = len(windows_to_draw)
        prev_end = -1
        for i, window in enumerate(windows_to_draw):
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
        self.display.flush()

    def handle_maprequest(self, event):
        '''Handle X11 MapRequest'''
        self.wsm.receive_window(event.window)
        self.active = event.window
        event.window.map()
        self.draw_windows()

    def run_launcher(self):
        lib.utils.run_application(
            lib.utils.get_program_location(config.LAUNCHER).split()
        )

    def close_window(self):
        if self.active:
            self.active.destroy()  # too brutal
            current_windows = self.wsm.get_current_workspace().windows
            current_windows.remove(self.active)
            self.active = None
            self.draw_windows()

    def full_screen(self):
        if not self.active:
            return

        if not self.fullscreen:
            self.active.configure(
                stack_mode=X.Above,
                width=self.width,
                height=self.height,
                y=0,
                x=0
            )
            self.display.flush()
        else:
            self.draw_windows()

        self.fullscreen = not self.fullscreen

    def handle_events(self):
        '''Handle X11 events'''
        current_windows = self.wsm.get_current_workspace().windows
        for window in current_windows:
            if window not in self.root_window.query_tree().children:
                current_windows.remove(window)
                self.draw_windows()
        event = self.display.next_event()
        self.set_active()
        logging.debug(event)
        if event.type == X.MapRequest:
            self.handle_maprequest(event)
        elif event.type == X.DestroyNotify:
            window = event.window
            window.unmap()
            for worksp in self.wsm.workspaces:
                if window in worksp.windows:
                    worksp.windows.remove(window)
                    if self.wsm.get_current_workspace() == worksp:
                        self.draw_windows()
                    break
        elif event.type == X.KeyPress:
            if event.detail in workspace_number.keys():
                self.wsm.change_workspace(
                    workspace_number[event.detail]
                )

            if event.detail == shortcut['launcher_key']:
                self.run_launcher()
            elif event.detail == shortcut['close_window_key']:
                self.close_window()
            elif event.detail == shortcut['full_screen_key']:
                self.full_screen()

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
    logging.basicConfig(filename=config.LOGFILE,
                        filemode='w', level=logging.DEBUG)
    logging.debug('Window manager started.')
    config.on_startup()
    while True:
        WindowManager.handle_events()


WindowManager = wm()

if __name__ == "__main__":
    main()
