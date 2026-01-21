import os
from pathlib import Path

from PyQt5 import QtWidgets, QtGui

from egp_soft_based_on_mfl.Tabs.TAB_9_dent_analysis.modular_maker.embedded_app import CircularDentEmbedded
from .widgets.screen_1 import build_screen1 as build_screen1_layout
from .widgets.screen_2 import build_screen2 as build_screen2_layout
from .widgets.tabs_builder import init_tab as tab_builder_screen2
from .widgets.setup_ui import setupUi as setupUi_layout

import warnings


warnings.filterwarnings('ignore')


# Dynamically locate the GMFL root (2 levels above this file)
GMFL_ROOT = Path(__file__).resolve().parents[1]


def gmfl_path(relative):
    """Return absolute path inside GMFL backend_data/temp folder."""
    temp_dir = GMFL_ROOT / "backend_data" / "data_generated" / "temp"
    os.makedirs(temp_dir, exist_ok=True)  # make sure folder exists
    return str(temp_dir / relative)




class WatermarkWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #f2f2f2;")  # grey background
        self.watermark = QtGui.QPixmap(r"D:\Anubhav\vdt_backend\GMFL_12_Inch_Desktop\utils\Picture1.png")
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.08)  # transparency (adjust karo)

        # Center me watermark draw karo
        x = (self.width() - self.watermark.width()) / 2
        y = (self.height() - self.watermark.height()) / 2
        painter.drawPixmap(int(x), int(y), self.watermark)



class Ui_MainWindow(QtWidgets.QWidget):

    # ------------------------------------------------------------------
    # Main window initializer:
    # - Creates background + menubar
    # - Builds stacked screens (Landing + Main App/ screen_1 + screen_2)
    # - Sets up overall layout system
    # ------------------------------------------------------------------
    def setupUi(self, MainWindow):
        setupUi_layout(self, MainWindow)



    # ------------------------------------------------------------------
    # Screen 1: Landing page (Select Inch + Load Project)
    # ------------------------------------------------------------------
    def build_screen1(self):
        build_screen1_layout(self)

    # ------------------------------------------------------------------
    # Screen 2: Main application (Tabs + Footer Info + Home Button)
    # ------------------------------------------------------------------
    def build_screen2(self):
        build_screen2_layout(self)

    # ------------------------------------------------------------------
    # Tab initialization for Screen 2 (creates all tab pages)
    # ------------------------------------------------------------------
    def init_tab(self):
        print(f" pipetally inside init: {self.pipetally}")
        tab_builder_screen2(self)

    def try_enable_advanced_tabs(self):
        print("DEBUG → weld_loaded:", self.weld_loaded,
              "pipe_loaded:", self.pipe_loaded)

        if self.weld_loaded and self.pipe_loaded:
            for idx in self.tabs_to_unlock:
                self.right_tabWidget.setTabEnabled(idx, True)
            print("✅ Tabs 4–7 ENABLED")
        else:
            print("⏳ Not enabling yet…")

    def launch_new_app_inside_tab(self):
        if getattr(self, "_dent_loaded", False):
            return

        print("🌀 Loading Circular Dent app inside tab")

        self.dent_widget = CircularDentEmbedded(self)
        self.new_app_layout.addWidget(self.dent_widget)

        self._dent_loaded = True










