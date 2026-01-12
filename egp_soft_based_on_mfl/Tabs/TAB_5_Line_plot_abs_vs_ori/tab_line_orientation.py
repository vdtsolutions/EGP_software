# orientation_tab5.py
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from .widgets.LineChart_draw import Line_chart_orientation
from .widgets.next_prev_btn_helper import Line_chart_orientation_next, Line_chart_orientation_previous

class Tab5LineOrientation(QtWidgets.QWidget):
    """Self-contained Tab 5 with its own UI and button logic."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # keep reference if you need to call parent methods
        self.config = self.parent.config
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

        # Tab look
        self.setObjectName("tab_5")
        self.setStyleSheet("background-color: #EDF6FF;")

        # ---------------- layouts ----------------
        self.hb_orientation = QtWidgets.QHBoxLayout(self)
        self.vb_orientation = QtWidgets.QVBoxLayout()

        # ---------------- figure / canvas / toolbar ----------------
        self.figure_x_orientation = plt.figure(figsize=(25, 8))
        self.canvas_x_orientation = FigureCanvas(self.figure_x_orientation)
        self.toolbar_x_orientation = NavigationToolbar(self.canvas_x_orientation, self)

        # ---------------- controls ----------------
        self.m_output_orientation = QtWebEngineWidgets.QWebEngineView(self)

        self.combo_orientation = QtWidgets.QComboBox()
        self.combo_orientation.setObjectName("Pipe_id")
        self.combo_orientation.setCurrentText("Pipe_id")

        lowerSensitivity_list_orientation = ['-3.5', '0.99', '0.80', '0.79']
        self.lower_Sensitivity_combo_box_orientation = QComboBox()
        self.lower_Sensitivity_combo_box_orientation.addItems(lowerSensitivity_list_orientation)

        upperSensitivity_list_orientation = ['1.01', '1.08', '1.09']
        self.upper_Sensitivity_combo_box_orientation = QComboBox()
        self.upper_Sensitivity_combo_box_orientation.addItems(upperSensitivity_list_orientation)

        # ---------------- buttons ----------------
        self.button_x5_orienatation = QtWidgets.QPushButton('Line Chart 2')
        self.button_x5_orienatation.setStyleSheet(PROFESSIONAL_BUTTON_STYLE)
        self.button_x5_orienatation.resize(50, 50)
        self.button_x5_orienatation.clicked.connect(lambda: Line_chart_orientation(self))

        self.next_btn_lc_orienatation = QtWidgets.QPushButton('Next')
        self.next_btn_lc_orienatation.setStyleSheet("background-color: white; color: black;")
        self.next_btn_lc_orienatation.clicked.connect(lambda: Line_chart_orientation_next(self))

        self.prev_btn_lc_orienatation = QtWidgets.QPushButton('Previous')
        self.prev_btn_lc_orienatation.setStyleSheet("background-color: white; color: black;")
        self.prev_btn_lc_orienatation.clicked.connect(lambda: Line_chart_orientation_previous(self))

        # ---------------- button row ----------------
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.prev_btn_lc_orienatation)
        button_layout.addStretch(1)
        button_layout.addWidget(self.next_btn_lc_orienatation)
        button_layout_widget = QtWidgets.QWidget()
        button_layout_widget.setLayout(button_layout)
        button_layout_widget.setFixedHeight(50)

        # ---------------- sub-rows ----------------
        self.hbox_5_orientation = QtWidgets.QHBoxLayout()
        self.hbox_6_orientation = QtWidgets.QHBoxLayout()
        self.hbox_7_orientation = QtWidgets.QHBoxLayout()

        self.vb_orientation.addLayout(self.hbox_5_orientation)
        self.vb_orientation.addLayout(self.hbox_6_orientation)
        self.vb_orientation.addLayout(self.hbox_7_orientation)
        self.vb_orientation.addWidget(button_layout_widget)

        self.hb_orientation.addLayout(self.vb_orientation, 75)

        # ---------------- row contents ----------------
        self.hbox_5_orientation.addWidget(self.toolbar_x_orientation)
        self.hbox_5_orientation.addWidget(self.combo_orientation)
        self.hbox_5_orientation.addWidget(self.button_x5_orienatation)
        self.hbox_6_orientation.addWidget(self.m_output_orientation)

