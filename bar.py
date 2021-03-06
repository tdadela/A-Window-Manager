import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import threading
import socket
import time
from awm import config

update_workspace_label = None
update_date_label = None


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        global update_workspace_label
        global update_date_label

        self.setWindowTitle("AWM - bar")
        self.setStyleSheet("background-color: black;")
        self.setLayout(qtw.QHBoxLayout())

        self.workspace_label = self.create_label(qtc.Qt.AlignLeft)
        self.date_label = self.create_label(qtc.Qt.AlignRight)

        self.update_workspace_label(1)
        update_workspace_label = self.update_workspace_label
        update_date_label = self.update_date_label

        screen_width = qtw.QDesktopWidget().screenGeometry(-1).width()
        self.setFixedWidth(screen_width)
        self.setFixedHeight(config.BAR_HEIGHT)

        self.show()

    def create_label(self, alignment):
        label = qtw.QLabel("loading")
        label.setAttribute(qtc.Qt.WA_TranslucentBackground, True)
        label_gce = qtw.QGraphicsColorizeEffect()
        label_gce.setColor(qtc.Qt.white)
        label.setGraphicsEffect(label_gce)
        label.setAlignment(alignment | qtc.Qt.AlignVCenter)
        label.setFont(qtg.QFont('Ubuntu Mono', config.BAR_FONT_SIZE))

        self.layout().addWidget(label)

        return label

    def update_workspace_label(self, workspace_id):
        workspace_amt = len(config.workspace_keys)
        text = " ".join(map(lambda x: f"{x}" if x != workspace_id else f"[{x}]", range(
            1, workspace_amt + 1)))
        self.workspace_label.setText(text)

    def update_date_label(self):
        text = time.strftime("%H:%M")
        self.date_label.setText(text)


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
        try:
            new_workspace = int(data)
            update_workspace_label(new_workspace)
        except ValueError:
            print('Workspace ID received from wm was invalid.')
        c.close()


def date_updator():
    time.sleep(1)
    while True:
        update_date_label()
        time.sleep(60)


if __name__ == "__main__":
    vm_listener_thread = threading.Thread(target=wait_for_wm_data)
    vm_listener_thread.start()

    date_updator_thread = threading.Thread(target=date_updator)
    date_updator_thread.start()

    app = qtw.QApplication([])
    mw = MainWindow()

    app.exec_()
