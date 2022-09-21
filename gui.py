import ctypes
import os
import platform
from pathlib import Path

import pyduinocli
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QApplication,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# Ensure arduino:avr is installed
os.system("arduino-cli core install arduino:avr")

arduino_cli = pyduinocli.Arduino()
TEMPLATE_SKETCH_PATH = Path(__file__).parent / "template.ino"
OUTPUT_SKETCH_PATH = Path(__file__).parent / "out" / "out.ino"
OUTPUT_SKETCH_PATH_STR = OUTPUT_SKETCH_PATH.as_posix()
ARDUINO_BOARD_FULLY_QUALIFIED_NAME = "arduino:avr:nano:cpu=atmega328old"
PORT = "com3"


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wifi interface")
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        my_icon = QIcon("./icon.svg")

        self.setWindowIcon(my_icon)

        sub = QHBoxLayout()
        sub.addWidget(QLabel("SSID:-"))
        wifi_ssid_line_edit = QLineEdit()
        sub.addWidget(wifi_ssid_line_edit)
        layout.addLayout(sub)

        sub = QHBoxLayout()
        sub.addWidget(QLabel("Password:-"))
        wifi_password_line_edit = QLineEdit()
        sub.addWidget(wifi_password_line_edit)
        layout.addLayout(sub)

        sub = QHBoxLayout()
        checkbox = QCheckBox("Show Password", self)
        sub.setAlignment(Qt.AlignLeft)
        sub.addWidget(checkbox)
        layout.addLayout(sub)

        sub = QHBoxLayout()
        upload_btn = QPushButton("Upload")
        wifi_ssid_line_edit.returnPressed.connect(upload_btn.clicked)
        upload_btn.clicked.connect(
            lambda: self.modify_template_and_upload(
                wifi_ssid_line_edit.text(), wifi_password_line_edit.text()
            )
        )
        sub.addWidget(upload_btn)
        layout.addLayout(sub)

        sub = QHBoxLayout()
        sub.addWidget(QLabel("Output:-"))
        layout.addLayout(sub)

        self.show()

    def modify_template_and_upload(self, SSID, password):
        with open(TEMPLATE_SKETCH_PATH, "r") as file:
            code_str = file.read()
            new_code_str = code_str.replace("{{WIFI_SSID}}", SSID).replace(
                "{{WIFI_PASSWORD}}", password
            )
        os.makedirs(OUTPUT_SKETCH_PATH.parent, exist_ok=True)
        with open(OUTPUT_SKETCH_PATH, "w") as file:
            file.write(new_code_str)

        arduino_cli.compile(OUTPUT_SKETCH_PATH_STR, fqbn=ARDUINO_BOARD_FULLY_QUALIFIED_NAME)
        arduino_cli.upload(
            OUTPUT_SKETCH_PATH_STR, port=PORT, fqbn=ARDUINO_BOARD_FULLY_QUALIFIED_NAME
        )


app = QApplication()

# Fix icon not showing in Windows taskbar
if platform.system() == "Windows":
    # https://learn.microsoft.com/en-us/windows/win32/shell/appids#:~:text=to%20unexpected%20results.-,How%20to%20Form%20an%20Application%2DDefined%20AppUserModelID,-An%20application%20must
    app_id = "II.WifiSketchUploader"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)  # type: ignore

window = MainWindow()

app.exec_()
