# This Python file uses the following encoding: utf-8
import sys
import port

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
        self.ui.portsList.addItems(self.port.get_port_list())

        self.ui.portsList.currentTextChanged.connect(self.on_portsList_changed)

    @Slot(str)
    def on_portsList_changed(self, new_text):
        """Ten slot jest wywoływany automatycznie po zmianie portsList."""
        print(f"Wybrano: {new_text}")
        self.port.connect(new_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
