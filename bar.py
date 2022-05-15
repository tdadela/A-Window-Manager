import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import threading
import socket

update_workspace_label = None


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        global update_workspace_label
        self.setWindowTitle("AWM - bar")
        self.setStyleSheet("background-color: black;")
        self.setLayout(qtw.QVBoxLayout())
        self.labelka = qtw.QLabel("AWM bar is initializing.")
        labelka_gce = qtw.QGraphicsColorizeEffect()
        self.labelka.setAttribute(qtc.Qt.WA_TranslucentBackground, True)
        labelka_gce.setColor(qtc.Qt.white)
        self.labelka.setGraphicsEffect(labelka_gce)
        self.labelka.setFont(qtg.QFont('Ubuntu Mono', 18))
        self.layout().addWidget(self.labelka)
        self.update_workspace_label(1)
        update_workspace_label = self.update_workspace_label

        self.setFixedWidth(800)
        self.setFixedHeight(50)

        self.show()

    def update_workspace_label(self, workspace_id):
        text = " ".join(map(lambda x: str(x) if x
                            != workspace_id else f"[{x}]", range(1, 10)))
        self.labelka.setText(text)


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


if __name__ == "__main__":
    x = threading.Thread(target=wait_for_wm_data)
    x.start()

    app = qtw.QApplication([])
    mw = MainWindow()

    app.exec_()
