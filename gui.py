from pathlib import Path
import pyduinocli
from pprint import pprint
import os

# os.system("./arduino-cli core install arduino:avr")

arduino = pyduinocli.Arduino()

with open(Path(__file__).parent / "template" / "template.ino", "r") as file:
    code_str = file.read()
    new_code_str = code_str.replace("{{LED_VALUE}}", "5")

with open(Path(__file__).parent / "out" / "out.ino", "w") as file:
    file.write(new_code_str)

arduino.compile("./out/out.ino", fqbn="arduino:avr:nano")
arduino.upload("./out/out.ino", port='com3', fqbn="arduino:avr:nano:cpu=atmega328old")
