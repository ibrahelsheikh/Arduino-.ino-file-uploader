import os
from pathlib import Path

import pyduinocli
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QPushButton,
)

# Ensure arduino:avr is installed
os.system("arduino-cli core install arduino:avr")

TEMPLATE_SKETCH_PATH = Path(__file__).parent / "template.ino"
OUTPUT_SKETCH_PATH = Path(__file__).parent / "out" / "out.ino"


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arduino CLI")
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        sub = QHBoxLayout()
        sub.addWidget(QLabel("WiFi Pin:"))
        line_edit = QLineEdit()
        sub.addWidget(line_edit)
        layout.addLayout(sub)

        sub = QHBoxLayout()
        upload_btn = QPushButton("Upload")
        line_edit.returnPressed.connect(upload_btn.clicked)
        upload_btn.clicked.connect(lambda: self.modify_template_and_upload(line_edit.text()))
        sub.addWidget(upload_btn)
        layout.addLayout(sub)

        self.show()

    def modify_template_and_upload(self, wifi_password):
        with open(TEMPLATE_SKETCH_PATH, "r") as file:
            code_str = file.read()
            new_code_str = code_str.replace("{{LED_VALUE}}", wifi_password)

        os.makedirs(OUTPUT_SKETCH_PATH.parent, exist_ok=True)
        with open(OUTPUT_SKETCH_PATH, "w") as file:
            file.write(new_code_str)

        arduino = pyduinocli.Arduino()
        arduino.compile(OUTPUT_SKETCH_PATH.as_posix(), fqbn="arduino:avr:nano:cpu=atmega328old")
        arduino.upload(OUTPUT_SKETCH_PATH.as_posix(), port="com3", fqbn="arduino:avr:nano:cpu=atmega328old")


app = QApplication()

window = MainWindow()

app.exec()
