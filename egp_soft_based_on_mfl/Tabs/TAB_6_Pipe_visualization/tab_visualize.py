from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


from .widgets.Analysis_btn import pre_graph_analysis
from .widgets.reset_next_prev_btn import reset_btn_fun_pipe, graph_analysis_next, graph_analysis_previous
from .widgets.helper_func import box_selection_all_defect, generate_report




class VisualizeTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.runid = None
        self.Weld_id = None
        # keep reference to parent so we can connect signals to parent's slots
        self.parent = parent
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

        # ---- BEGIN: original code verbatim style ----
        self.setObjectName("tab_6")
        self.setStyleSheet("background-color: #EDF6FF;")

        self.hbox = QtWidgets.QHBoxLayout(self)
        self.vbox = QtWidgets.QVBoxLayout()

        self.figure = plt.figure(figsize=(20, 6))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.reset_pushButton = QtWidgets.QPushButton("Reset")
        self.reset_pushButton.clicked.connect(lambda: reset_btn_fun_pipe(self))
        # self.reset_defect_pushButton.hide()

        self.All_box_selection = QtWidgets.QPushButton("Box_selection")
        self.All_box_selection.clicked.connect(lambda: box_selection_all_defect(self))

        """
        Pipe_id in combo_box  inside the fifth tab
        """
        self.combo_box = QComboBox()

        """
        Lower_Sensitivity in combo_box inside the fifth tab
        """
        lowerSensitivity_list = ['0', '0.99', '0.98', '0.97', '0.96', '0.95', '0.94', '0.93', '0.92', '0.91', '0.90',
                                 '0.89',
                                 '0.88', '0.87', '0.86', '0.85', '0.84', '0.83', '0.82', '0.81', '0.80', '0.79', '0.78',
                                 '0.77', '0.76', '0.75', '0.74', '0.71', '0.70', '0.68', '0.66', '0.64', '0.62', '0.60']

        self.lower_Sensitivity_combo_box = QComboBox()
        self.lower_Sensitivity_combo_box.addItems(lowerSensitivity_list)

        """
        upper_Sensitivity in combo_box inside the fifth tab
        """
        upperSensitivity_list = ['0', '1.01', '1.02', '1.03', '1.04',
                                 '1.05', '1.06', '1.07', '1.08', '1.09', '1.10', '1.11',
                                 '1.12', '1.13', '1.14', '1.15', '1.16',
                                 '1.17', '1.18', '1.19', '1.20', '1.22', '1.24', '1.26', '1.28', '1.30', '1.31', '1.32',
                                 '1.33', '1.34', '1.35', '1.36', '1.38', '1.40', '1.42', '1.44', '1.46']

        self.upper_Sensitivity_combo_box = QComboBox()
        self.upper_Sensitivity_combo_box.addItems(upperSensitivity_list)

        """
        Analysis button inside the fifth tab
        """
        self.Analaysis_pushButton = QtWidgets.QPushButton("Analysis")
        self.Analaysis_pushButton.setStyleSheet(PROFESSIONAL_BUTTON_STYLE)
        self.Analaysis_pushButton.clicked.connect(lambda: pre_graph_analysis(self))

        """
        Generate button inside the fifth tab
        """
        self.generatepushButton = QtWidgets.QPushButton("Generate Report")
        self.generatepushButton.clicked.connect(lambda: generate_report(self))

        self.next_btn_pre = QtWidgets.QPushButton('Next')
        self.next_btn_pre.setStyleSheet("background-color: white; color: black;")
        self.next_btn_pre.clicked.connect(lambda: graph_analysis_next(self))

        self.prev_btn_pre = QtWidgets.QPushButton('Previous')
        self.prev_btn_pre.setStyleSheet("background-color: white; color: black;")
        self.prev_btn_pre.clicked.connect(lambda: graph_analysis_previous(self))

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.prev_btn_pre)
        button_layout.addStretch(1)  # Adds a stretchable space between buttons
        button_layout.addWidget(self.next_btn_pre)

        self.myTableWidget3 = QtWidgets.QTableWidget()
        self.myTableWidget3.setGeometry(QtCore.QRect(30, 600, 1300, 235))
        self.myTableWidget3.setRowCount(30)
        self.myTableWidget3.setColumnCount(10)
        self.myTableWidget3.setColumnWidth(0, 150)
        self.myTableWidget3.setColumnWidth(1, 150)
        self.myTableWidget3.setColumnWidth(2, 150)
        self.myTableWidget3.setColumnWidth(3, 150)
        self.myTableWidget3.setColumnWidth(4, 150)
        self.myTableWidget3.setColumnWidth(5, 150)
        self.myTableWidget3.setColumnWidth(6, 150)
        self.myTableWidget3.setColumnWidth(7, 150)
        self.myTableWidget3.setColumnWidth(8, 150)
        self.myTableWidget3.setColumnWidth(9, 150)
        self.myTableWidget3.setHorizontalHeaderLabels(
            ['Defect_id', 'Pipe_id', 'Absolute_distance(m)', 'Distance_to_Upstream(m)', 'Feature_type',
             'Dimensions_classification', 'Orientation_clock(hr:min)', 'Length(mm)', 'Width(mm)', 'Depth(%)'])
        # self.myTableWidget3.resizeColumnsToContents()
        self.myTableWidget3.horizontalHeader().setStretchLastSection(True)

        self.hbox.addLayout(self.vbox)

        self.hbox_8 = QtWidgets.QHBoxLayout()
        self.hbox_9 = QtWidgets.QHBoxLayout()
        self.hbox_10 = QtWidgets.QHBoxLayout()
        self.vbox.addLayout(self.hbox_8)
        self.vbox.addLayout(self.hbox_9)
        self.vbox.addLayout(self.hbox_10)

        self.hbox_8.addWidget(self.toolbar)
        # self.hbox_8.addWidget(self.add_defect_pushButton)
        self.hbox_8.addWidget(self.combo_box)
        # self.hbox_8.addWidget(self.lower_Sensitivity_combo_box)
        # self.hbox_8.addWidget(self.upper_Sensitivity_combo_box)
        self.hbox_8.addWidget(self.Analaysis_pushButton)
        self.hbox_8.addWidget(self.All_box_selection)
        # self.hbox_8.addWidget(self.deleteButton)
        # self.hbox_8.addWidget(self.generatepushButton)
        self.hbox_8.addWidget(self.reset_pushButton)

        self.hbox_9.addWidget(self.canvas)

        button_layout_widget = QtWidgets.QWidget()
        # button_layout_widget.setStyleSheet("background-color: white;")
        button_layout_widget.setLayout(button_layout)
        # Add the button layout widget to the canvas layout
        self.vbox.addWidget(button_layout_widget)

        # self.hbox_8.addWidget(self.Showdefect)
        self.hbox_10.addWidget(self.myTableWidget3)

        # IMPORTANT:
        # your original code ends with:
        #     self.setLayout(self.hbox_8)
        # which technically overwrites layouts, but I'll keep it identical.
        self.setLayout(self.hbox_8)
        # ---- END: original code verbatim style ----

