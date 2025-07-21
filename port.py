# This Python file uses the following encoding: utf-8
import serial.tools.list_ports
from time import sleep


class Port:
    def __init__(self):
        self.ports = serial.tools.list_ports.comports()
        self.serialInst = serial.Serial()
        self.portsList = []

    def get_port_list(self) -> list:
        self.portsList = []
        for port in self.ports:
            self.portsList.append(str(port.device))
        return self.portsList


    def connect(self, com) -> None:
        for i in range(len(self.portsList)):
            if self.portsList[i].startswith(com):
                use = str(com)
        self.serialInst.baudrate = 9600
        self.serialInst.port = use
        self.serialInst.open()
        # Time needed to establish connection
        sleep(1.5)
        self.display("Connected".center(16))


    def display(self, text: str):
        self.serialInst.write(text.encode('utf-8'))
