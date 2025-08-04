# This Python file uses the following encoding: utf-8
import openmeteo_requests
import requests_cache
import requests
import unicodedata

from datetime import datetime
from PySide6.QtCore import QTimer, QObject, Signal
from retry_requests import retry


class Content(QObject):
    content_to_update = Signal(list)
    display_new = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize lists to control content
        self.content = ["",""]
        self.options = ["Not Selected", "Time", "Date", "Weather"]
        self.selected = ["Not Selected", "Not Selected"]
        self.displayed = ["Not Selected", "Not Selected"]

        # Setup minute_monitor to continuous refreshing data
        self.minute_monitor = QTimer(self)
        self.minute_monitor.setInterval(1000)
        self.minute_monitor.timeout.connect(self._check_minute_change)
        self._last_minute = datetime.now().minute
        self.minute_monitor.start()

        # Setup the Open-Meteo API client with cache and retry on error
        self.cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        self.retry_session = retry(self.cache_session, retries = 5, backoff_factor = 0.2)
        self.openmeteo = openmeteo_requests.Client(session = self.retry_session)
        self.url = "https://api.open-meteo.com/v1/forecast"
        self.ip_url = "https://ipinfo.io/json"


    def _check_minute_change(self):
        """
        Method called by QTimer every second.
        Checks the minute change, if any, updates the content using the _update_content method.
        """
        current_minute = datetime.now().minute
        if current_minute != self._last_minute and self.displayed != ["Not Selected", "Not Selected"]:
            self._last_minute = current_minute
            self._update_content()
            self.content_to_update.emit(self.get_content())
            self.display_new.emit(self.get_content())


    def _update_content(self):
        """
        Called by _check_minute_change.
        Updates "content" based on what is currently displayed.
        """
        for row in range(len(self.displayed)):
            if self.displayed[row] == "Time":
                self.add_time(row)
            elif self.displayed[row] == "Date":
                self.add_date(row)
            elif self.displayed[row] == "Weather":
                self.add_temperature(row)
            elif self.displayed[row] == "Not Selected":
                self.clear_row(row)


    def add_time(self, row: int):
        time = datetime.now()
        time = time.strftime("%H:%M")
        self.content[row] = time
        self.displayed[row] = "Time"


    def add_date(self, row: int):
        date = datetime.now()
        date = date.strftime("%d.%m.%Y")
        self.content[row] = date
        self.displayed[row] = "Date"


    def add_temperature(self, row: int):
        response = requests.get(self.ip_url)
        data = response.json()

        latitude = None
        longitude = None
        city = data.get("city")

        if 'loc' in data:
            loc_parts = data['loc'].split(',')
            if len(loc_parts) == 2:
                latitude = float(loc_parts[0])
                longitude = float(loc_parts[1])

        params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": True
        }
        responses = self.openmeteo.weather_api(self.url, params=params)
        response = responses[0]
        current_weather = response.Current()
        label = f"{city}: {round(current_weather.Variables(0).Value(), 1)}°C"
        if len(label) > 16:
            label = f"{round(current_weather.Variables(0).Value(), 1)}°C"
        self.content[row] = label
        self.displayed[row] = "Weather"


    def clear_row(self, row: int) -> None:
        self.content[row] = ""
        self.displayed[row] = "Not Selected"


    def update_displayed(self) -> None:
        self.displayed = list(self.selected)
        self._update_content()
        self.content_to_update.emit(self.get_content())
        self.display_new.emit(self.get_content())


    def get_content(self):
        def strip_accents(text: str) -> str:
            normalized_text = unicodedata.normalize('NFD', text)
            stripped_text = ''.join(
                char for char in normalized_text if not unicodedata.combining(char)
            )
            return stripped_text

        return [strip_accents(item.center(16)) for item in self.content]


