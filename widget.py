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

        self.port = port.Port()
        self.content = content.Content()

        self.ui.portsList.addItems(self.port.get_port_list())
        self.ui.portsList.currentTextChanged.connect(self.on_portsList_changed)

        self.ui.upper.addItems(self.content.options)
        self.ui.lower.addItems(self.content.options)

        self.ui.display.clicked.connect(self.on_display_clicked)

    @Slot(str)
    def on_portsList_changed(self, new_com):
        """Ten slot jest wywoływany automatycznie po zmianie portsList."""
        print(f"Wybrano: {new_text}")
        self.port.connect(new_com)

    def on_display_clicked(self):
        print("clicked")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
