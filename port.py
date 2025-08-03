# This Python file uses the following encoding: utf-8
import utils

import serial.tools.list_ports
from PySide6.QtCore import QObject, Slot, QTimer, Signal


class Port(QObject):
    arduino_ready = Signal()
    failed_connection = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ports = serial.tools.list_ports.comports()
        self.serialInst = serial.Serial()
        self.serialInst.timeout = 0.1
        self.portsList = []
        self.connected_port = None


    # Get available port list
    def get_port_list(self) -> list:
        self.portsList = []
        for port in self.ports:
            self.portsList.append(str(port.device))
        return self.portsList


    # Connect to port
    def connect(self, com: str) -> None:
        # Close the port if it was open
        if self.serialInst.is_open:
                self.serialInst.close()
                utils.CONNECTED = False

        # If "Not Selected" selected, do not connect and return
        if com == "Not Selected":
            return

        for i in range(len(self.portsList)):
            if self.portsList[i].startswith(com):
                use = str(com)
        self.serialInst.baudrate = 9600
        self.serialInst.port = use
        self.serialInst.open()
        self.connected_port = com
        for _ in range(50): # 50 times * (100ms[QTimer] + 100ms[timeout]) = 10 seconds
            line = self.serialInst.readline().decode('utf-8').strip()
            if line == "READY":
                self.arduino_ready.emit()
                self.display("Connected".center(16))
                utils.CONNECTED = True
                return
            QTimer.singleShot(100, lambda: None)
        # Failed to connect to the selected port
        self.failed_connection.emit()


    # Display text on arduino screen
    @utils.if_connected
    def display(self, text: str):
        self.serialInst.write(text.encode('utf-8'))


    # Function for auto updates
    @utils.if_connected
    @Slot(list)
    def auto_update(self, new_content: list):
        self.display("".join(new_content))
