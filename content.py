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

                self.add_time(0) # Zamienić na metodę która automatycznie decyduje co i gdzie zmieniać
                self.content_to_update.emit(self.get_content())


    def add_time(self, row: int):
        time = datetime.now()
        time = time.strftime("%H:%M")
        self.content[row] = time


    def add_date(self, row: int):
        date = datetime.now()
        date = date.strftime("%d.%m.%Y")
        self.content[row] = date


    def clear_row(self, row: int):
        self.content[row] = ""


    def get_content(self):
        print([item.center(16) for item in self.content])
        return [item.center(16) for item in self.content]












        # %Y - Rok z czterema cyframi (np. 2025)

        # %m - Miesiąc jako liczba (od 01 do 12)

        # %d - Dzień miesiąca (od 01 do 31)

        # %H - Godzina w formacie 24-godzinnym (od 00 do 23)

        # %M - Minuty (od 00 do 59)

        # %S - Sekundy (od 00 do 59)



        # # Formatowanie do popularnego formatu
        # format_daty = "%Y-%m-%d %H:%M:%S"
        # sformatowana_data = teraz.strftime(format_daty)

        # print(f"Aktualna data i godzina to: {sformatowana_data}")
        # # Wynik: Aktualna data i godzina to: 2025-07-20 20:28:59

        # print(f"Obecna godzina to: {teraz.hour}:{teraz.minute}")
        # # Możesz też odwołać się bezpośrednio do atrybutów: .year, .month, .day, .hour, .minute, .second
