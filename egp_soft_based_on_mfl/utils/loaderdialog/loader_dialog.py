import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QThread

class BaseWorker(QThread):

    finished = pyqtSignal(object)
    progress = pyqtSignal(int)
    message = pyqtSignal(str)

    def smooth_progress(self, start, end, message):

        import time

        self.message.emit(message)

        steps = end - start

        for i in range(steps):

            if self.isInterruptionRequested():
                return

            self.progress.emit(start + i)
            time.sleep(0.01)

    def stop(self):
        self.requestInterruption()


class LoaderDialog(QtWidgets.QDialog):

    # cancelled = QtCore.pyqtSignal()

    def __init__(self, parent=None, title="Processing..."):
        super().__init__(parent)

        # self.setWindowFlags(
        #     QtCore.Qt.Window
        #     | QtCore.Qt.CustomizeWindowHint
        #     | QtCore.Qt.WindowMinimizeButtonHint
        #     | QtCore.Qt.WindowTitleHint
        # )
        self.setWindowFlags(
            QtCore.Qt.Dialog
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.WindowTitleHint
        )

        self.setWindowTitle(title)
        self.setModal(False)
        self.setFixedSize(320, 140)

        self.is_cancelling = False

        layout = QtWidgets.QVBoxLayout(self)

        # Status label
        self.status_label = QtWidgets.QLabel("Starting...")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)

        # Progress bar
        self.progress = QtWidgets.QProgressBar()
        self.progress.setRange(0, 100)

        # Timer label
        self.time_label = QtWidgets.QLabel("Time: 0s")
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)

        # # Cancel button
        # self.cancel_btn = QtWidgets.QPushButton("Cancel")
        # self.cancel_btn.clicked.connect(self._handle_cancel)

        layout.addWidget(self.status_label)
        layout.addWidget(self.progress)
        layout.addWidget(self.time_label)
        # layout.addWidget(self.cancel_btn)

        # Timer
        self.start_time = time.time()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(500)

    # ------------------------
    # Timer
    # ------------------------
    def _handle_cancel(self):
        self.cancel_btn.setEnabled(False)
        self.cancelled.emit()
    def update_timer(self):

        if self.is_cancelling:
            return

        elapsed = int(time.time() - self.start_time)
        self.time_label.setText(f"Time: {elapsed}s")

    # ------------------------
    # Update UI from workers
    # ------------------------

    def update_status(self, text):

        if self.is_cancelling:
            return

        self.status_label.setText(text)

    def update_progress(self, value):

        if self.is_cancelling:
            return

        self.progress.setValue(value)

    # ------------------------
    # Cancelling state
    # ------------------------

    def show_cancelling(self):

        self.is_cancelling = True

        self.status_label.setText("Cancelling...")
        self.cancel_btn.setEnabled(False)

        self.timer.stop()

        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555;
                background: #d0d0d0;
                height: 22px;
                border-radius: 4px;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: #a6a6a6;
                width: 20px;
                margin: 1px;
            }
        """)

    # ------------------------
    # Finish
    # ------------------------

    def finish(self):

        self.timer.stop()
        self.accept()