# This Python file uses the following encoding: utf-8
import openmeteo_requests
import requests_cache
import requests

from datetime import datetime
from PySide6.QtCore import QTimer, QObject, Signal
from retry_requests import retry


class Content(QObject):
    content_to_update = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize lists to control content
        self.content = ["",""]
        self.options = ["Not Selected", "Time", "Date", "Weather"]
        self.selected = ["Not Selected", "Not Selected"]

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
        if current_minute != self._last_minute and self.selected != ["Not Selected", "Not Selected"]:
            self._last_minute = current_minute
            self._update_content()
            self.content_to_update.emit(self.get_content())


    def _update_content(self):
        """
        Called by _check_minute_change.
        Updates "content" based on what is currently selected.
        """
        for row in range(len(self.selected)):
            if self.selected[row] == "Time":
                self.add_time(row)
            elif self.selected[row] == "Date":
                self.add_date(row)
            elif self.selected[row] == "Weather":
                self.add_temperature(row)


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
        self.content[row] = f"{city}: {round(current_weather.Variables(0).Value(), 1)}°C"
        self.selected[row] = "Weather"


    def clear_row(self, row: int):
        self.content[row] = ""
        self.selected[row] = "Not Selected"


    def get_content(self):
        print([item.center(16) for item in self.content])
        return [item.center(16) for item in self.content]

