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
        self.ui.portsList.addItems(self.port.get_port_list())
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
        self.content.content_to_update.connect(self.update_display_labels)

        # Display "Disconnected" after app close
        app = QApplication.instance()
        app.aboutToQuit.connect(lambda: self.port.display("Disconnected".center(16)))


    @Slot(str)
    def on_portsList_changed(self, new_com):
        """Automatically connects the port when selected"""
        print(f"Wybrano: {new_com}")
        with self.loader as load:
            load.run(lambda: self.port.connect(new_com))


    @Slot()
    def on_failed_connection(self):
        self.ui.portsList.setCurrentIndex(0)


    @Slot(str)
    def on_upper_changed(self, new_data):
        """Automatically changes the upper content when selected"""
        if new_data == "Date":
            print("new date upper")
            self.content.add_date(0)
        elif new_data == "Time":
            print("new time upper")
            self.content.add_time(0)
        elif new_data == "Weather":
            print("new weather upper")
            self.content.add_temperature(0)
        elif new_data == "Not Selected":
            print("Clear row upper")
            self.content.clear_row(0)


    @Slot(str)
    def on_lower_changed(self, new_data):
        """Automatically changes the lower content when selected"""
        if new_data == "Date":
            print("new date lower")
            self.content.add_date(1)
        elif new_data == "Time":
            print("new time lower")
            self.content.add_time(1)
        elif new_data == "Weather":
            print("new weather lower")
            self.content.add_temperature(1)
        elif new_data == "Not Selected":
            print("Clear row lower")
            self.content.clear_row(1)


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
        print(self.content.get_content())
        self.content.content_to_update.emit(self.content.get_content())




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
