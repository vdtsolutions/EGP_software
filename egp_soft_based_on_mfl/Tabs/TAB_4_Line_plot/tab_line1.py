from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets, QtWebEngineWidgets
import os

import matplotlib.pyplot as plt
from pathlib import Path


'''
    Imports for Functions 
'''
from .widgets.Linechart_countervSensor_btn import Line_chart1
from .widgets.feature_btn import feature_selection_func
from .widgets.basevalue_btn import basevalue
from .widgets.Reset_btn import reset_btn_fun
from .widgets.mark_lat_long_btn import mark_lat_long
from .widgets.next_prev_btn import Line_chart1_next, Line_chart1_previous

# Dynamically locate the GMFL root (2 levels above this file)
GMFL_ROOT = Path(__file__).resolve().parents[2]


def gmfl_path(relative):
    """Return absolute path inside GMFL backend_data/temp folder."""
    temp_dir = GMFL_ROOT / "backend_data" / "data_generated" / "temp"
    os.makedirs(temp_dir, exist_ok=True)  # make sure folder exists
    return str(temp_dir / relative)




class LinePlotTab:
    """
    Line Plotting Tab (PyQt5 Version)
    ---------------------------------
    - Child UI class that delegates all event handlers to the parent main window.
    - Keeps logic identical to the procedural version.
    """

    def __init__(self, parent=None):
        self.parent = parent
        self.config = self.parent.config
        self._setup_tab()

    # =====================================================
    # ----------------- UI SETUP --------------------------
    # =====================================================
    def _setup_tab(self):
        """Sets up all widgets and layouts (logic unchanged)."""
        PROFESSIONAL_BUTTON_STYLE = """
        QPushButton {
            font-size: 13px;
            font-family: 'Segoe UI', Arial;
            font-weight: 600;
            padding: 4px 14px;
            color: white;
            background-color: #2F5EF9;
            border: 1px solid #1537B3;
            border-radius: 0px;  /* rectangular */
        }
        QPushButton:hover {
            background-color: #1E4BE0;
            border-color: #102F9A;
        }
        QPushButton:pressed {
            background-color: #153CC0;
            border-color: #0C267B;
        }
        """

        # ---- Create Tab Widget ----
        self.tab_line1 = QtWidgets.QWidget()
        self.tab_line1.setObjectName("tab_4")
        self.tab_line1.setStyleSheet("background-color: #EDF6FF;")

        # ---- Layouts ----
        self.hb5 = QtWidgets.QHBoxLayout(self.tab_line1)
        self.vb5 = QtWidgets.QVBoxLayout()

        # ---- Matplotlib Canvas ----
        self.figure_x5 = plt.figure(figsize=(25, 8))
        self.canvas_x5 = FigureCanvas(self.figure_x5)
        self.toolbar_x5 = NavigationToolbar(self.canvas_x5, self.tab_line1)

        # ---- Combo Box ----
        self.combo = QtWidgets.QComboBox()
        self.combo.setObjectName("Pipe_id")
        self.combo.setCurrentText("pipe_id")

        # ---- Reset Button ----
        self.reset_btn = QtWidgets.QPushButton("Reset")
        self.reset_btn.setStyleSheet(PROFESSIONAL_BUTTON_STYLE)
        self.reset_btn.clicked.connect(lambda: reset_btn_fun(self))

        # ---- Latitude / Longitude ----
        self.latitude = QtWidgets.QLineEdit()
        self.latitude.setFixedWidth(100)
        self.logitude = QtWidgets.QLineEdit()
        self.logitude.setFixedWidth(100)

        # ---- Marker Buttons ----
        self.selection_mark_lat_long = QtWidgets.QPushButton("Mark Lat Long")
        self.selection_mark_lat_long.setStyleSheet(PROFESSIONAL_BUTTON_STYLE)
        self.selection_mark_lat_long.clicked.connect(lambda: mark_lat_long(self))

        self.selection_mark_base_value = QtWidgets.QPushButton("Mark Base Value")
        self.selection_mark_base_value.setStyleSheet(PROFESSIONAL_BUTTON_STYLE)
        self.selection_mark_base_value.clicked.connect(lambda: basevalue(self))


        self.feature_selection = QtWidgets.QPushButton("Mark Feature")
        self.feature_selection.setStyleSheet(PROFESSIONAL_BUTTON_STYLE)
        self.feature_selection.clicked.connect(lambda: feature_selection_func(self))

        # ---- Internal State ----
        self.rect_start_1 = None
        self.rect_end_1 = None

        # ---- Line Chart + Navigation Buttons ----
        self.button_x5 = QtWidgets.QPushButton("Line Chart")
        self.button_x5.setStyleSheet(PROFESSIONAL_BUTTON_STYLE)
        self.button_x5.clicked.connect(lambda: Line_chart1(self))
        self.button_x5.resize(50, 50)

        self.next_btn_lc = QtWidgets.QPushButton("Next")
        self.next_btn_lc.setStyleSheet("background-color: white; color: black;")
        self.next_btn_lc.clicked.connect(lambda: Line_chart1_next(self))

        self.prev_btn_lc = QtWidgets.QPushButton("Previous")
        self.prev_btn_lc.setStyleSheet("background-color: white; color: black;")
        self.prev_btn_lc.clicked.connect(lambda: Line_chart1_previous(self))

        # ---- Navigation Layout ----
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.prev_btn_lc)
        button_layout.addStretch(1)
        button_layout.addWidget(self.next_btn_lc)
        button_layout_widget = QtWidgets.QWidget()
        button_layout_widget.setLayout(button_layout)

        # ---- Web Output View ----
        self.m_output_proxi = QtWebEngineWidgets.QWebEngineView(self.tab_line1)

        # ---- Main Layout Hierarchy ----
        self.hb5.addLayout(self.vb5, 75)

        self.hbox_5 = QtWidgets.QHBoxLayout()
        self.hbox_6 = QtWidgets.QHBoxLayout()
        self.hbox_7 = QtWidgets.QHBoxLayout()

        self.vb5.addLayout(self.hbox_5)
        self.vb5.addLayout(self.hbox_6, 60)
        self.vb5.addLayout(self.hbox_7, 40)
        self.vb5.addWidget(button_layout_widget)

        # ---- Top Toolbar Section ----
        self.hbox_5.addWidget(self.toolbar_x5)
        self.hbox_5.addWidget(self.combo)
        self.hbox_5.addWidget(self.button_x5)
        self.hbox_5.addWidget(self.latitude)
        self.hbox_5.addWidget(self.logitude)
        self.hbox_5.addWidget(self.selection_mark_lat_long)
        self.hbox_5.addWidget(self.selection_mark_base_value)
        self.hbox_5.addWidget(self.feature_selection)
        self.hbox_5.addWidget(self.reset_btn)

        # ---- Chart and Output ----
        self.hbox_6.addWidget(self.canvas_x5)
        self.hbox_7.addWidget(self.m_output_proxi)

        self.tab_line1.setLayout(self.hb5)

        """
        -------> End of fourth tab (Line Plotting)
        """








