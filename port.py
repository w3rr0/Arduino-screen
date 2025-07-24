# This Python file uses the following encoding: utf-8
import serial.tools.list_ports
from time import sleep
from PySide6.QtCore import QObject, Slot


class Port(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ports = serial.tools.list_ports.comports()
        self.serialInst = serial.Serial()
        self.portsList = []
        self.connected_port = None

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
        self.connected_port = com
        # Time needed to establish connection
        sleep(1.5)
        self.display("Connected".center(16))


    def display(self, text: str):
        self.serialInst.write(text.encode('utf-8'))


    # Function for auto updates
    @Slot(list)
    def auto_update(self, new_content: list):
        self.display("".join(new_content))
