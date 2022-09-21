import os
from pathlib import Path
import ctypes

import pyduinocli
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QCheckBox,

)
from PySide6.QtGui import QIcon

# Ensure arduino:avr is installed
os.system("arduino-cli core install arduino:avr")
TEMPLATE_SKETCH_PATH = Path(__file__).parent / "template.ino"
OUTPUT_SKETCH_PATH = Path(__file__).parent / "out" / "out.ino"


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wifi interface")
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        my_icon = QIcon()
        my_icon.addFile('Arduino_Logo.svg.png')

        self.setWindowIcon(my_icon)

        sub = QHBoxLayout()
        sub.addWidget(QLabel("SSID:-        "))
        line_edit = QLineEdit()
        sub.addWidget(line_edit)
        layout.addLayout(sub)

        sub = QHBoxLayout()
        sub.addWidget(QLabel("Password:-"))
        line_edit_two = QLineEdit()
        sub.addWidget(line_edit_two)
        layout.addLayout(sub)


        sub =QHBoxLayout()
        checkbox = QCheckBox("show", self)
        sub.addWidget(QLabel("                                                                  " ))
        sub.addWidget(checkbox)
        layout.addLayout(sub)


        sub = QHBoxLayout()
        upload_btn = QPushButton("Upload")
        line_edit.returnPressed.connect(upload_btn.clicked)
        upload_btn.clicked.connect(lambda: self.modify_template_and_upload(line_edit.text(),line_edit_two.text()))
        sub.addWidget(upload_btn)
        layout.addLayout(sub)

        sub = QHBoxLayout()
        sub.addWidget(QLabel("output:-"))
        layout.addLayout(sub)

        myappid = 'Arduino_Logo.svg.png' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.show()

    def modify_template_and_upload(self, SSID ,password):
        with open(TEMPLATE_SKETCH_PATH, "r") as file:
            code_str = file.read()
            new_code_str = code_str.replace("{{WIFI_SSID}}", SSID).replace("{{WIFI_PASSWORD}}", password)
        os.makedirs(OUTPUT_SKETCH_PATH.parent, exist_ok=True)
        with open(OUTPUT_SKETCH_PATH, "w") as file:
            file.write(new_code_str)

        arduino = pyduinocli.Arduino()
        arduino.compile(OUTPUT_SKETCH_PATH.as_posix(), fqbn="arduino:avr:nano:cpu=atmega328old")
        arduino.upload(OUTPUT_SKETCH_PATH.as_posix(), port="com3", fqbn="arduino:avr:nano:cpu=atmega328old")


app = QApplication()

window = MainWindow()

app.exec()
