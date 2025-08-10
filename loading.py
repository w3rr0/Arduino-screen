# This Python file uses the following encoding: utf-8
from PySide6.QtGui import QMovie
from PySide6.QtCore import Signal, QThread, Slot, QEventLoop


class TaskThread(QThread):
    task_done = Signal(object)

    def __init__(self, actual_task_function, parent=None):
        super().__init__(parent)
        self.task_function = actual_task_function
        self.result = None

    def run(self):
        try:
            self.result = self.task_function()
        except Exception:
            self.result = None
        finally:
            self.task_done.emit(self.result)

class Loading:
    def __init__(self, parent_widget, loading_label):
        self.parent_widget = parent_widget
        self.loading_label = loading_label
        self.gif_path = "loading_gear.gif"

        self.movie = QMovie(self.gif_path)
        self.loading_label.setMovie(self.movie)

        self._thread = None
        self._result = None

    def __enter__(self):
        """
        Triggers animations and event loops.
        """
        self.parent_widget.setEnabled(False)
        self.loading_label.show()
        self.movie.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Stops animations and cleans up after itself.
        """
        # Stop animation and unlock UI
        self.movie.stop()
        self.loading_label.hide()
        self.parent_widget.setEnabled(True)

        # Make sure the thread is finished
        if self._thread and self._thread.isRunning():
            self._thread.quit()
            self._thread.wait()

        # Safe delete thread object
        if self._thread:
            self._thread.deleteLater()

        # Show exceptions
        return False

    @Slot(object)
    def _on_task_done(self, result):
        """
        Stores the result from the thread.
        """
        self._result = result


    def run(self, task_function):
        """
        Wykonuje podaną funkcję w osobnym wątku, utrzymując responsywność UI.
        Czeka na zakończenie zadania i zwraca jego wynik.
        """
        self._thread = TaskThread(task_function)
        self._thread.task_done.connect(self._on_task_done)

        loop = QEventLoop()
        self._thread.finished.connect(loop.quit)

        self._thread.start()
        loop.exec()

        return self._result
