# This Python file uses the following encoding: utf-8
from datetime import datetime
from PySide6.QtCore import QTimer, QObject, Signal


class Content(QObject):
    content_to_update = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.content = ["",""]
        self.options = ["Not Selected", "Time", "Date"]
        self.selected = ["Not Selected", "Not Selected"]

        self.minute_monitor = QTimer(self)
        self.minute_monitor.setInterval(1000)
        self.minute_monitor.timeout.connect(self._check_minute_change)
        self._last_minute = datetime.now().minute
        self.minute_monitor.start()

    def _check_minute_change(self):
        """Metoda wywoływana przez QTimer co sekundę, sprawdza zmianę minuty."""
        current_minute = datetime.now().minute
        if current_minute != self._last_minute:
            self._last_minute = current_minute
            print(f"Minuta się zmieniła! Czas: {datetime.now().strftime('%H:%M')}")

            self._update_content()
            self.content_to_update.emit(self.get_content())


    def _update_content(self):
        """Automatycznie aktualizuje zawartość content na podstawie jego zawartości"""
        for row in range(len(self.selected)):
            if self.selected[row] == "Time":
                self.add_time(row)
            elif self.selected[row] == "Date":
                self.add_date(row)


    def add_time(self, row: int):
        time = datetime.now()
        time = time.strftime("%H:%M")
        self.content[row] = time
        self.selected[row] = "Time"


    def add_date(self, row: int):
        date = datetime.now()
        date = date.strftime("%d.%m.%Y")
        self.content[row] = date
        self.selected[row] = "Date"


    def clear_row(self, row: int):
        self.content[row] = ""
        self.selected[row] = "Not Selected"


    def get_content(self):
        print([item.center(16) for item in self.content])
        return [item.center(16) for item in self.content]

