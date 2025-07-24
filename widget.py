# This Python file uses the following encoding: utf-8
import sys
import port
import content

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Slot


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

        # Initialize program objects
        self.port = port.Port()
        self.content = content.Content()

        # Add options to connect
        self.ui.portsList.addItems(self.port.get_port_list())
        self.ui.portsList.currentTextChanged.connect(self.on_portsList_changed)

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
        """Ten slot jest wywoływany automatycznie po zmianie portsList."""
        print(f"Wybrano: {new_com}")
        self.port.connect(new_com)


    @Slot(str)
    def on_upper_changed(self, new_data):
        if new_data == "Date":
            print("new date upper")
            self.content.add_date(0)
        elif new_data == "Time":
            print("new time upper")
            self.content.add_time(0)
        elif new_data == "Not Selected":
            print("Clear row upper")
            self.content.clear_row(0)


    @Slot(str)
    def on_lower_changed(self, new_data):
        if new_data == "Date":
            print("new date lower")
            self.content.add_date(1)
        elif new_data == "Time":
            print("new time lower")
            self.content.add_time(1)
        elif new_data == "Not Selected":
            print("Clear row lower")
            self.content.clear_row(1)


    @Slot(list)
    def update_display_labels(self, new_data):
        self.ui.row_0.setText(new_data[0])
        self.ui.row_1.setText(new_data[1])


    def on_display_clicked(self):
        self.port.display("".join(self.content.get_content()))
        print(self.content.get_content())
        self.content.content_to_update.emit(self.content.get_content())




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
