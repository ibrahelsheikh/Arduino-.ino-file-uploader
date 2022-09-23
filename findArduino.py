import serial.tools.list_ports
global port_case

def get_ports():
    ports = serial.tools.list_ports.comports()

    return ports


def findArduino(portsFound):
    commPort = 'None'
    numConnection = len(portsFound)

    for i in range(0, numConnection):
        port = foundPorts[i]
        strPort = str(port)

        if 'Arduino' in strPort:
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])

    return commPort


foundPorts = get_ports()
connectPort = findArduino(foundPorts)


def get_port_name():
    return connectPort


def check_connection_case():
    pass


if connectPort != 'None':
    ser = serial.Serial(connectPort, baudrate=9600, timeout=1)
    port_case =str('Connected to '+ connectPort)
    print(port_case)
    get_port_name()

else:
    port_case = 'Connection Issue!'
    print(port_case)

print('DONE')
