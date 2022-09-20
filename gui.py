import os
from pathlib import Path

import pyduinocli

# Ensure arduino:avr is installed
os.system("arduino-cli core install arduino:avr")

TEMPLATE_SKETCH_PATH = (Path(__file__).parent / "template" / "template.ino").as_posix()
OUTPUT_SKETCH_PATH = (Path(__file__).parent / "out" / "out.ino").as_posix()

arduino = pyduinocli.Arduino()

with open(TEMPLATE_SKETCH_PATH, "r") as file:
    code_str = file.read()
    new_code_str = code_str.replace("{{LED_VALUE}}", "5")

with open(OUTPUT_SKETCH_PATH, "w") as file:
    file.write(new_code_str)

arduino.compile(OUTPUT_SKETCH_PATH, fqbn="arduino:avr:nano")
arduino.upload(
    OUTPUT_SKETCH_PATH, port="com3", fqbn="arduino:avr:nano:cpu=atmega328old"
)
