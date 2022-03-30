import socket

import threading

from kivy.app import App
from kivy.config import Config

from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '200')

update_workspace_label = None


class TestApp(App):
    def build(self):
        global update_workspace_label
        self.layout = FloatLayout()
        self.workspace_label = Label(text="workspace_label",
                                     font_size=30)

        self.layout.add_widget(self.workspace_label)
        update_workspace_label = self.update_workspace_label
        return self.layout

    def update_workspace_label(self, workspace_id):
        text = " ".join(map(lambda x: str(x) if str(
            x) != workspace_id else f"[{x}]", range(1, 10)))
        self.workspace_label.text = text


def wait_for_wm_data():
    host = socket.gethostname()
    port = 8080

    s = socket.socket()
    s.bind((host, port))

    while True:
        s.listen(1)
        c, addr = s.accept()
        print("Connection from: " + str(addr))
        data = c.recv(1024).decode('utf-8')
        if not data:
            break
        print('From wm: ' + data)
        update_workspace_label(data)
        c.close()


if __name__ == "__main__":
    x = threading.Thread(target=wait_for_wm_data)
    x.start()
    TestApp().run()
