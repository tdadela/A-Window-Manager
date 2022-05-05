''' A Window Manager'''
import logging
import itertools
from Xlib import X
from Xlib.display import Display
from . import config
from . import setting
from . import utils
from .workspace_manager import WorkspaceManager
from .distribute_windows import distribute_windows
from .setting import shortcut, workspace_number, on_startup, MODKEY_MASK


class WindowManager:
    '''Main Window Manager class'''

    def __init__(self):
        self.active = None
        self.horizontal = True
        self.display = Display()
        self.root_window = self.display.screen().root
        self.height = self.root_window.get_geometry().height
        self.width = self.root_window.get_geometry().width
        self.wsm = WorkspaceManager(
            self.root_window.get_geometry(), setting.NO_WORKSPACES)

        self.root_window.change_attributes(
            event_mask=X.SubstructureRedirectMask)
        for i in itertools.chain(shortcut.values(), workspace_number.keys()):
            self.root_window.grab_key(
                i, MODKEY_MASK, 1, X.GrabModeAsync, X.GrabModeAsync
            )
        for i in itertools.chain(workspace_number.keys()):
            self.root_window.grab_key(
                i, setting.CHANGE_WINDOW_WORKSPACE, 1,
                X.GrabModeAsync, X.GrabModeAsync
            )

    def draw_windows(self):
        '''Draw windows in horizontal tiling mode'''
        windows_to_draw = self.wsm.get_current_workspace().get_all_windows()
        distribute_windows(
            windows_to_draw,
            width=self.width,
            height=self.height,
            horizontal=self.horizontal)
        self.display.flush()

    def handle_maprequest(self, event):
        '''Handle X11 MapRequest'''
        self.wsm.receive_window(event.window)
        self.active = event.window
        event.window.map()
        self.draw_windows()

    def handle_destroyrequest(self, event):
        '''Handle X11 DestroyRequest'''
        window = event.window
        # window.unmap()
        for worksp in self.wsm.workspaces:
            if window in worksp.windows:
                worksp.windows.remove(window)
                if self.wsm.get_current_workspace() == worksp:
                    self.draw_windows()
                break

    @staticmethod
    def run_launcher():
        '''Execute application launcher'''
        utils.run_application(
            utils.get_program_location(config.LAUNCHER).split()
        )

    def close_window(self):
        '''Close active window'''
        if self.active:
            # self.active.destroy()  # too brutal
            self.active.kill_client()
            self.wsm.remove_window(self.active)
            self.active = None
            self.draw_windows()

    def full_screen(self):
        '''Turn off/on full screen mode'''
        if not self.active:
            return

        if not self.wsm.is_fullscreen():
            windows = self.wsm.get_current_workspace().get_all_windows()
            for window in windows:
                if window != self.active:
                    window.unmap()
            self.active.configure(
                #  stack_mode=X.Above,
                width=self.width,
                height=self.height,
                y=0,
                x=0
            )
            self.display.flush()
        else:
            windows = self.wsm.get_current_workspace().get_all_windows()
            for window in windows:
                if window != self.active:
                    window.map()
            self.draw_windows()

        self.wsm.change_fullscreen_state()

    def handle_events(self):
        '''Handle X11 events'''
        current_windows = self.wsm.get_current_workspace().get_all_windows()
        for window in current_windows:
            if window not in self.root_window.query_tree().children:
                # current_windows.remove(window)
                self.wsm.remove_window(window)
                self.draw_windows()
        event = self.display.next_event()
        print(event)
        self.set_active()
        logging.debug(event)
        if event.type == X.MapRequest:
            self.handle_maprequest(event)
        elif event.type == X.DestroyNotify:
            self.handle_destroyrequest(event)
        elif event.type == X.KeyPress:
            if event.detail in workspace_number.keys():
                if event.state == MODKEY_MASK:
                    self.wsm.change_workspace(
                        workspace_number[event.detail]
                    )
                    self.draw_windows()
                elif event.state == setting.CHANGE_WINDOW_WORKSPACE:
                    if self.active:
                        self.wsm.move_between_workspaces(
                            self.active, workspace_number[event.detail])
                        self.draw_windows()

            if event.detail == shortcut['launcher_key']:
                self.run_launcher()
            elif event.detail == shortcut['close_window_key']:
                self.close_window()
            elif event.detail == shortcut['full_screen_key']:
                self.full_screen()
            elif event.detail == shortcut['move_left']:
                if self.active:
                    self.wsm.move_window_left(self.active)
                    self.draw_windows()
            elif event.detail == shortcut['move_right']:
                if self.active:
                    self.wsm.move_window_right(self.active)
                    self.draw_windows()
            elif event.detail == shortcut['rotate']:
                self.horizontal = not self.horizontal
                self.draw_windows()

    def set_active(self):
        '''Set focused windows'''
        #  print(self.display.get_input_focus())
        #  self.active = self.display.get_input_focus()  # ['Window']
        pointed = self.root_window.query_pointer().child
        if pointed != self.root_window or isinstance(pointed, int):
            self.active = pointed
        else:
            self.active = None


def main():
    '''Main loop for window manager events.'''
    window_manager = WindowManager()
    logging.basicConfig(filename=config.LOGFILE,
                        filemode='w', level=logging.DEBUG)
    logging.debug('Window manager started.')
    on_startup()
    while True:
        window_manager.handle_events()


if __name__ == "__main__":
    main()
