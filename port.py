import serial.tools.list_ports


class port:
    def __init__(self):
        self.ports = serial.tools.list_ports.comports()
        self.serialInst = serial.Serial()
        self.portsList = []

    def get_port_listv(self) -> list:
        self.portsList = []
        for port in self.ports:
            self.portList.append(str(port))
        return self.portList


    def connect(self, com: int):
        for i in range(len(self.portsList)):
            if self.portsList[i].startswith("COM" + str(com)):
                use = "COM" + str(com)
        self.serialInst.baudrate = 9600
        self.serialInst.port = use
        self.serialInst.open()


    def display(self, text: str):
        self.serialInst.write(text.encode('utf-8'))
