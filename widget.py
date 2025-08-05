# This Python file uses the following encoding: utf-8
import sys
import port
import content
import utils
from loading import Loading

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Slot
from PySide6.QtGui import QMovie, QIcon


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.setWindowTitle("Arduino Screen")
        self.setWindowIcon(QIcon("screen.png"))


        # Style text
        self.ui.row_0.setStyleSheet("letter-spacing: 2px;")
        self.ui.row_1.setStyleSheet("letter-spacing: 2px;")


        # Set loading animation
        self.loading_gif = QMovie("loading_gear.gif")
        self.ui.loading.setMovie(self.loading_gif)


        # Initialize program objects
        self.port = port.Port()
        self.content = content.Content()
        self.loader = Loading(self, self.ui.loading)


        # Add options to connect
        org_popup = self.ui.portsList.showPopup

        def update_ports_list():
            """
            Updates the list of available ports before expanding it
            """
            current_selection = self.ui.portsList.currentText()

            self.ui.portsList.clear()
            current_ports = ["Not Selected"] + self.port.get_port_list()
            self.ui.portsList.addItems(current_ports)

            if current_selection in current_ports:
                index = current_ports.index(current_selection)
                self.ui.portsList.setCurrentIndex(index)

            org_popup()

        self.ui.portsList.showPopup = update_ports_list
        self.ui.portsList.currentTextChanged.connect(self.on_portsList_changed)

        # Connect connection info
        self.port.arduino_ready.connect(self.display_connection)

        # Connect selecting default port
        self.port.failed_connection.connect(self.on_failed_connection)

        # Add options to display
        self.ui.upper.addItems(self.content.options)
        self.ui.lower.addItems(self.content.options)
        self.ui.upper.currentTextChanged.connect(self.on_upper_changed)
        self.ui.lower.currentTextChanged.connect(self.on_lower_changed)

        # Connect display button
        self.ui.display.clicked.connect(self.on_display_clicked)

        # Connect auto refresh func to slot
        self.content.content_to_update.connect(self.port.auto_update)
        self.content.display_new.connect(self.update_display_labels)

        # Display "Disconnected" after app close
        app = QApplication.instance()
        app.aboutToQuit.connect(lambda: self.port.display("Disconnected".center(16)))


    @Slot(str)
    def on_portsList_changed(self, new_com):
        """Automatically connects the port when selected"""
        with self.loader as load:
            load.run(lambda: self.port.connect(new_com))


    @Slot()
    def on_failed_connection(self):
        """set Not Selected"""
        self.ui.portsList.setCurrentIndex(0)


    @Slot(str)
    def on_upper_changed(self, new_data):
        """Changes the upper selected"""
        self.content.selected[0] = new_data


    @Slot(str)
    def on_lower_changed(self, new_data):
        """Changes the lower selected"""
        self.content.selected[1] = new_data


    @utils.if_connected
    @Slot(list)
    def update_display_labels(self, new_data):
        """Displays the current text from the arduino screen"""
        self.ui.row_0.setText(new_data[0])
        self.ui.row_1.setText(new_data[1])


    @utils.if_connected
    @Slot()
    def display_connection(self):
        """Display connection info in UI"""
        self.ui.row_0.setText("Connected".center(16))


    @utils.if_connected
    def on_display_clicked(self):
        """Displays the currently selected option on the arduino screen"""
        with self.loader as load:
            load.run(lambda: self.content.update_displayed())




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
