from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout
# from modular_maker.main import MainWindow
from egp_soft_based_on_mfl.Tabs.TAB_9_dent_analysis.modular_maker.main2 import MainWindow


class CircularDentEmbedded(QWidget):
    """
    Embed-safe version of Circular Dent app.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create your existing app window
        self.window = MainWindow()

        # Make it behave like a widget (NOT a top-level window)
        self.window.setParent(self)
        self.window.setWindowFlags(self.window.windowFlags() & ~Qt.Window)

        layout.addWidget(self.window)
