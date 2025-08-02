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
    def __init__(self, parent_widget, loading_label, task_function):
        """
        Initialize context manager.
        """
        self.parent_widget = parent_widget
        self.loading_label = loading_label
        self.task_function = task_function
        self.gif_path = "loading_gear.gif"

        self.movie = QMovie(self.gif_path)
        self.result = None
        self.thread = None
        self.loop = None

    def __enter__(self):
        """
        Triggers animations and event loops.
        """

        # Show animation and block UI
        self.parent_widget.setEnabled(False)
        self.loading_label.setMovie(self.movie)
        self.movie.start()
        self.loading_label.show()

        # Config and start main thread
        self.thread = TaskThread(self.task_function)
        self.thread.task_done.connect(self._on_task_done)

        # Create local loop to ensure that the UI works
        self.loop = QEventLoop()
        self.thread.finished.connect(self.loop.quit)

        self.thread.start()
        self.loop.exec()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Stops animations and cleans up after itself.
        """

        # Stop animation and unlock UI
        self.movie.stop()
        self.loading_label.hide()
        self.parent_widget.setEnabled(True)

        # Clean
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()

        # Show exceptions
        return False

    @Slot(object)
    def _on_task_done(self, result):
        """
        Stores the result from the thread.
        """
        self.result = result
