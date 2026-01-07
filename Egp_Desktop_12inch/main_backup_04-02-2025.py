import os
from PyQt5.QtCore import pyqtSlot, QUrl, QTimer
import csv
import os.path
import plotly.graph_objs as go
from datetime import datetime, timedelta
from scipy.signal import lfilter
from sklearn.preprocessing import MinMaxScaler
import plotly.io as pio
import query_generator
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Rectangle
import math
# import more_itertools as mit
from matplotlib.widgets import RectangleSelector
import random
from multiprocessing import Process, freeze_support
import pymysql
from google.cloud import storage
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import *

# from PyQt5.QtCore import pyqtSlot

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Slider, LabelSet
from bokeh.plotting import Figure, output_file, show
from bokeh.embed import file_html
from bokeh.resources import CDN

from PyQt5.QtGui import QMovie
import sys
# import WeldAndPipeLength
import weld_update
import numpy as np
import seaborn as sns
import WeldToPipe
from google.cloud import bigquery
import pandas as pd
# from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import defects_and_points
import Components.update_form as formComponent

import Components.graph as graph
import Components.style as Style
import Components.logger as logger
import Components.config as Config
import Components.CreateProject as CreateProject
import Components.AddWeld as AddWeld
import Components.report_generator as Report

a = os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./utils/GCS_Auth.json"

Update_form_component = formComponent.UpdateForm()
connection = Config.connection
websearch = Config.xyz
company_list = []  # list of companies
credentials = Config.credentials
project_id = Config.project_id
client = bigquery.Client(credentials=credentials, project=project_id)
temp_defect = []
print(websearch)


class Ui_MainWindow(QtWidgets.QWidget):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1700, 820)
        MainWindow.showMaximized()

        self.count = 0
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.label_animation = QLabel(self)

        self.project_name = ''
        ##################### Left Main gridLayout #####################
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 190, 1200))
        self.gridLayoutWidget.adjustSize()

        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setStyleSheet(Style.list_grid_style)
        self.main_left = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.main_left.setContentsMargins(0, 0, 0, 0)
        self.main_left.setObjectName("main_left")

        ################### Left Main gridLayout add button Load data #########
        self.load_list_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.load_list_pushButton.setObjectName("load_list_pushButton")
        self.load_list_pushButton.clicked.connect(self.load_list)
        self.main_left.addWidget(self.load_list_pushButton, 0, 0, 1, 1)

        #################### Left Main gridlayout add listItems ##############
        self.left_listWidget = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.left_listWidget.setObjectName("left_listWidget")
        ########## Call the list_clicked  function ############
        self.left_listWidget.itemDoubleClicked.connect(self.list_clicked)
        self.left_listWidget.itemClicked.connect(self.get_project_name)
        self.main_left.addWidget(self.left_listWidget, 2, 0, 1, 1)
        self.add_to_list()

        ###################### Right Main gridLayout ############
        self.init_gridLayoutWidget_2()

        MainWindow.setCentralWidget(self.centralwidget)

        #################### MENUBAR BUTTONS #####################
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("File")
        # self.menubar.setStyleSheet(Style.menubar)
        self.menuFile = QtWidgets.QMenu(self.menubar)
        MainWindow.setMenuBar(self.menubar)
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuSearch = QtWidgets.QMenu(self.menubar)
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuhelp = QtWidgets.QMenu(self.menubar)

        ################### Add create_project in file menubar######
        self.actionCreate_Project = QtWidgets.QAction(MainWindow)
        self.actionCreate_Project.setObjectName("actionCreate_Project")
        # self.actionCreate_Project.setStyleSheet(Style.list_grid_style)
        self.menuFile.addAction(self.actionCreate_Project)

        ############# Type of defect Add in view menubar ###################
        self.actiontypeofdefect = QtWidgets.QAction(MainWindow)
        self.actiontypeofdefect.setObjectName("typeofdefect")
        self.menuView.addAction(self.actiontypeofdefect)

        ############## Add weld Manually ############
        self.addweld = QtWidgets.QAction(MainWindow)
        self.addweld.setObjectName("Add Weld")
        self.menuView.addAction(self.addweld)

        ############## Create Pipe ############
        self.create_pipe = QtWidgets.QAction(MainWindow)
        self.create_pipe.setObjectName("Create Pipe")
        self.menuView.addAction(self.create_pipe)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSearch.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuhelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def get_project_name(self, item):
        self.project_name = item

    def init_gridLayoutWidget_2(self):
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(100, 0, 1920, 800))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.main_right = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.main_right.setContentsMargins(0, 0, 0, 0)
        self.main_right.setObjectName("main_right")

    def _init_back_button(self):
        self.go_back_button = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        # self.go_back_button.styleSheet(Style.btn_type_primary)
        self.go_back_button.setText("Go Back")
        self.main_right.addWidget(self.go_back_button, 2, 0)
        self.go_back_button.clicked.connect(self.reset_default_screen)

    def init_gridLayoutWidget_4(self):
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.tab_visualize)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(0, 45, 1900, 1200))

        # self.gridLayoutWidget_5 = QtWidgets.QWidget(self.tab_visualize)
        # self.gridLayoutWidget_5.setGeometry(QtCore.QRect(0, 500, 1900, 1200))

        ############## Plot the visualization graph && NavigationToolbar inside the third tab #################
        self.figure = plt.figure(figsize=(18, 6))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.gridLayoutWidget_4)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.gridLayoutWidget_3)

        # self.figure1 = plt.figure(figsize=(18, 6))
        # self.canvas1 = FigureCanvas(self.figure)
        # self.canvas1.setParent(self.gridLayoutWidget_5)

    """
    Initialize the rigth_tabWidget inside the Right Main GridLayout
    """

    def init_tab(self):
        self.right_tabWidget = QtWidgets.QTabWidget(self.gridLayoutWidget_2)
        # self.right_tabWidget.styleSheet(Style.right_tabWidget)
        self.right_tabWidget.setObjectName("right_tabWidget")

        """
        Right tabwidget add tab,tab_2,tab_3,tab_4,tab_5,tab_6

        """
        self.tab_update = QtWidgets.QWidget()
        self.tab_update.setObjectName("tab")

        ############# Call the function init_update_form ###################
        self.tab_update.layout = QtWidgets.QVBoxLayout(self.tab_update)
        # self.tab_update.styleSheet(Style.tab_update)
        Update_form_component._init_form_layout(self.tab_update, self.tab_update.layout)

        self.right_tabWidget.addTab(self.tab_update, "")

        self.tab_visualize = QtWidgets.QWidget()
        self.tab_visualize.setObjectName("tab_2")

        self.tab_showData = QtWidgets.QWidget()
        self.tab_showData.setObjectName("tab_3")

        self.tab_line = QtWidgets.QWidget()             ########### Line_Chart #########
        self.tab_line.setObjectName("tab_4")

        self.tab_line1 = QtWidgets.QWidget()            ########### Weld_Selection #########
        self.tab_line1.setObjectName("tab_5")

        self.tab_line2 = QtWidgets.QWidget()
        self.tab_line2.setObjectName("tab_6")

        self.tab_heatmap = QtWidgets.QWidget()
        self.tab_heatmap.setObjectName("tab_7")

        self.clock_heatmap = QtWidgets.QWidget()
        self.clock_heatmap.setObjectName("tab_8")

        """
        Start From here third tab content
        """
        self.hbox = QtWidgets.QHBoxLayout(self.tab_visualize)
        self.vbox = QtWidgets.QVBoxLayout()

        # self.figure = plt.figure(figsize=(28, 7))
        self.figure1 = plt.figure(figsize=(20, 6))

        # self.canvas = FigureCanvas(self.figure)
        self.canvas1 = FigureCanvas(self.figure1)

        # self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar1 = NavigationToolbar(self.canvas1, self)

        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.setObjectName("Pipe_id")
        self.combo_box.setCurrentText("pipe_id")

        self.lower_Sensitivity_combo_box = QtWidgets.QLineEdit()
        self.lower_Sensitivity_combo_box.setFixedWidth(150)
        #self.lower_Sensitivity_combo_box.hide()

        self.upper_Sensitivity_combo_box = QtWidgets.QLineEdit()
        self.upper_Sensitivity_combo_box.setFixedWidth(150)
        #self.upper_Sensitivity_combo_box.hide()

        self.button = QtWidgets.QPushButton('Plot')
        self.button.resize(50, 50)

        self.reset_auto_hm_btn = QtWidgets.QPushButton('Reset')
        self.reset_auto_hm_btn.resize(50, 50)

        self.myTableWidget_hm = QtWidgets.QTableWidget()
        self.myTableWidget_hm.setGeometry(QtCore.QRect(30, 600, 1300, 235))
        self.myTableWidget_hm.setRowCount(30)
        self.myTableWidget_hm.setColumnCount(11)
        self.myTableWidget_hm.setColumnWidth(0, 160)
        self.myTableWidget_hm.setColumnWidth(1, 160)
        self.myTableWidget_hm.setColumnWidth(2, 160)
        self.myTableWidget_hm.setColumnWidth(3, 160)
        self.myTableWidget_hm.setColumnWidth(4, 160)
        self.myTableWidget_hm.setColumnWidth(5, 160)
        self.myTableWidget_hm.setColumnWidth(6, 160)
        self.myTableWidget_hm.setColumnWidth(7, 160)
        self.myTableWidget_hm.setColumnWidth(8, 160)
        self.myTableWidget_hm.setColumnWidth(9, 160)
        self.myTableWidget_hm.setColumnWidth(10, 160)
        self.myTableWidget_hm.horizontalHeader().setStretchLastSection(True)

        self.myTableWidget_hm.setHorizontalHeaderLabels(
            ['id', 'Pipe No.', 'Absolute Distance', 'Upstream', 'Pipe Length', 'Feature Type', 'Feature Identification',
             'Orientation', 'Length', 'Width', 'Dent %']
        )


        self.hbox.addLayout(self.vbox, 75)

        self.hbox1 = QtWidgets.QHBoxLayout()
        self.hbox2 = QtWidgets.QHBoxLayout()
        self.hbox3 = QtWidgets.QHBoxLayout()

        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)

        # self.hbox1.addWidget(self.toolbar)
        self.hbox1.addWidget(self.toolbar1)
        self.hbox1.addWidget(self.combo_box)
        self.hbox1.addWidget(self.lower_Sensitivity_combo_box)
        self.hbox1.addWidget(self.upper_Sensitivity_combo_box)
        self.reset_auto_hm_btn.clicked.connect(self.reset_auto_hm)
        self.button.clicked.connect(self.plot_heatmap_auto)
        self.hbox1.addWidget(self.button)
        self.hbox1.addWidget(self.reset_auto_hm_btn)
        self.hbox2.addWidget(self.canvas1)
        self.hbox3.addWidget(self.myTableWidget_hm)

        self.setLayout(self.hbox1)

        """
        End From here Third tab content
        """

        """
        Start From here fourth tab content
        """
        self.hb = QtWidgets.QHBoxLayout(self.tab_line)
        self.vb = QtWidgets.QVBoxLayout()

        self.figure_x = plt.figure(figsize=(25, 8))

        self.canvas_x = FigureCanvas(self.figure_x)

        self.toolbar_x = NavigationToolbar(self.canvas_x, self)

        self.combo = QtWidgets.QComboBox()
        self.combo.setObjectName("Pipe_id")
        self.combo.setCurrentText("pipe_id")
        self.reset_btn = QtWidgets.QPushButton('Reset')
        self.reset_btn.clicked.connect(self.reset_btn_fun)

        self.selection_mark_defect = QtWidgets.QPushButton()
        self.selection_mark_defect.setText("Mark Defect")
        self.selection_mark_defect.clicked.connect(self.mark_mdefect)

        self.selection_mark_base_value = QtWidgets.QPushButton()
        self.selection_mark_base_value.setText("Mark Base Value")
        self.selection_mark_base_value.clicked.connect(self.basevalue)

        self.rect_start_1 = None  # Store the starting point of the rectangle
        self.rect_end_1 = None

        self.button_x = QtWidgets.QPushButton('Line Chart')
        self.button_x.resize(50, 50)

        self.next_btn_lc = QtWidgets.QPushButton('Next')
        self.next_btn_lc.setStyleSheet("background-color: #4CAF50; color: white;")
        self.next_btn_lc.clicked.connect(self.Line_chart_next)

        self.prev_btn_lc = QtWidgets.QPushButton('Previous')
        self.prev_btn_lc.setStyleSheet("background-color: #4CAF50; color: white;")
        self.prev_btn_lc.clicked.connect(self.Line_chart_previous)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.prev_btn_lc)
        button_layout.addStretch(1)  # Adds a stretchable space between buttons
        button_layout.addWidget(self.next_btn_lc)

        self.myTableWidget_lc = QtWidgets.QTableWidget()
        self.myTableWidget_lc.setGeometry(QtCore.QRect(30, 600, 1300, 235))
        self.myTableWidget_lc.setRowCount(10)
        self.myTableWidget_lc.setColumnCount(11)
        self.myTableWidget_lc.setColumnWidth(0, 160)
        self.myTableWidget_lc.setColumnWidth(1, 160)
        self.myTableWidget_lc.setColumnWidth(2, 160)
        self.myTableWidget_lc.setColumnWidth(3, 160)
        self.myTableWidget_lc.setColumnWidth(4, 160)
        self.myTableWidget_lc.setColumnWidth(5, 160)
        self.myTableWidget_lc.setColumnWidth(6, 160)
        self.myTableWidget_lc.setColumnWidth(7, 160)
        self.myTableWidget_lc.setColumnWidth(8, 160)
        self.myTableWidget_lc.setColumnWidth(9, 160)
        self.myTableWidget_lc.setColumnWidth(10, 160)
        self.myTableWidget_lc.horizontalHeader().setStretchLastSection(True)

        self.myTableWidget_lc.setHorizontalHeaderLabels(
            ['id', 'Pipe No.', 'Absolute Distance', 'Upstream', 'Pipe Length', 'Feature Type', 'Feature Identification',
             'Orientation', 'Length', 'Width', 'Dent Difference']
        )

        self.hb.addLayout(self.vb, 75)

        self.hbox_1 = QtWidgets.QHBoxLayout()
        self.hbox_2 = QtWidgets.QHBoxLayout()
        self.hbox_table = QtWidgets.QHBoxLayout()

        self.vb.addLayout(self.hbox_1)
        self.vb.addLayout(self.hbox_2)
        self.vb.addLayout(self.hbox_table)

        button_layout_widget = QtWidgets.QWidget()
        button_layout_widget.setStyleSheet("background-color: white;")
        button_layout_widget.setLayout(button_layout)
        # Add the button layout widget to the canvas layout
        self.vb.addWidget(button_layout_widget)

        self.hbox_1.addWidget(self.toolbar_x)
        self.hbox_1.addWidget(self.combo)
        self.hbox_1.addWidget(self.button_x)
        self.button_x.clicked.connect(self.Line_chart)
        self.hbox_1.addWidget(self.selection_mark_base_value)
        self.hbox_1.addWidget(self.selection_mark_defect)
        self.hbox_1.addWidget(self.reset_btn)

        self.hbox_2.addWidget(self.canvas_x)
        # self.hbox_table.addWidget(self.myTableWidget_lc)

        self.setLayout(self.hbox_1)

        """
        End From here fourth tab content
        """

        """
        Start From here fifth tab content
        """

        self.hb5 = QtWidgets.QHBoxLayout(self.tab_line1)
        self.vb5 = QtWidgets.QVBoxLayout()

        self.figure_x5 = plt.figure(figsize=(25, 8))

        self.canvas_x5 = FigureCanvas(self.figure_x5)

        self.toolbar_x5 = NavigationToolbar(self.canvas_x5, self)

        self.start = QtWidgets.QLineEdit()
        self.end = QtWidgets.QLineEdit()

        self.button_x5 = QtWidgets.QPushButton('Line Chart 1')
        self.button_x5.resize(50, 50)
        self.hb5.addLayout(self.vb5, 75)

        self.hbox_5 = QtWidgets.QHBoxLayout()
        self.hbox_6 = QtWidgets.QHBoxLayout()

        self.vb5.addLayout(self.hbox_5)
        self.vb5.addLayout(self.hbox_6)

        self.hbox_5.addWidget(self.toolbar_x5)
        self.hbox_5.addWidget(self.start)
        self.hbox_5.addWidget(self.end)
        self.button_x5.clicked.connect(self.Line_chart1)
        # self.button_x5.styleSheet(Style.btn_type_primary)
        self.hbox_5.addWidget(self.button_x5)

        self.hbox_6.addWidget(self.canvas_x5)
        self.setLayout(self.hbox_5)
        """
        End From here fifth tab content

        """

        """
        Start from here six tab content

        """

        self.tab6_horizontal = QtWidgets.QHBoxLayout(self.tab_line2)
        self.tab6_horizontal1 = QtWidgets.QHBoxLayout()

        self.figure_tab6 = plt.figure(figsize=(25, 8))

        self.canvas_tab6 = FigureCanvas(self.figure_tab6)

        self.toolbar_tab6 = NavigationToolbar(self.canvas_tab6, self)
        self.combo1 = QtWidgets.QComboBox()
        self.combo1.setFixedSize(75, 25)
        self.combo1.setObjectName("Pipe_id")
        self.combo1.setCurrentText("pipe_id")

        self.button_tab6 = QtWidgets.QPushButton('Line Chart ')
        self.button_tab6.setFixedSize(75, 25)
        # self.button_tab6.resize(50, 50)

        self.button1_tab6 = QtWidgets.QPushButton('Circle')
        # self.button1_tab6.setFixedSize(75,25)
        self.button1_tab6.resize(50, 50)
        self.button1_tab6.hide()

        # self.layout2=QtWidgets.QVBoxLayout()
        self.tab6_horizontal.addLayout(self.tab6_horizontal1)
        self.hbox_5tab6 = QtWidgets.QVBoxLayout()

        self.hbox_6tab6 = QtWidgets.QVBoxLayout()

        self.tab6_horizontal1.addLayout(self.hbox_5tab6, 60)

        self.tab6_horizontal1.addLayout(self.hbox_6tab6, 40)

        ################## left layout ###############
        self.hbox_5tab6.addWidget(self.toolbar_tab6)
        self.hbox_5tab6.addWidget(self.combo1)
        self.hbox_5tab6.addWidget(self.button_tab6)

        self.button_tab6.clicked.connect(self.deformation_line)
        self.hbox_5tab6.addWidget(self.canvas_tab6)
        ################### Right Layout ##############

        self.button1_tab6.clicked.connect(self.on_click)
        self.hbox_6tab6.addWidget(self.button1_tab6)
        # self.hbox_6tab6.addWidget(self.graph_x)
        # self.hbox_6tab6.addWidget(self.canvas_tab6)
        self.setLayout(self.hbox_5tab6)

        """
        End from here six tab content

        """

        """
        Start from here seven tab content
        """
        self.hbox_20 = QtWidgets.QHBoxLayout(self.tab_heatmap)
        self.vbox_20 = QtWidgets.QVBoxLayout()
        self.figure_20 = plt.figure(figsize=(20, 6))
        self.canvas_20 = FigureCanvas(self.figure_20)
        self.toolbar_20 = NavigationToolbar(self.canvas_20, self)
        self.combo_box_tab8 = QtWidgets.QComboBox()
        self.show_btn_tab8 = QtWidgets.QPushButton('Show Pipe')
        self.show_btn_tab8.clicked.connect(self.show_heatmap_tab8)
        self.reset_btn_hm = QtWidgets.QPushButton('Reset Box')
        self.reset_btn_hm.clicked.connect(self.reset_btn_fun_heatmap)

        # Add these lines inside __init__ method or where you define your GUI components
        self.next_btn_tab8 = QtWidgets.QPushButton('Next')
        self.next_btn_tab8.setStyleSheet("background-color: #4CAF50; color: white;")
        self.next_btn_tab8.clicked.connect(self.show_next_heatmap_tab8)

        self.prev_btn_tab8 = QtWidgets.QPushButton('Previous')
        self.prev_btn_tab8.setStyleSheet("background-color: #4CAF50; color: white;")
        self.prev_btn_tab8.clicked.connect(self.show_previous_heatmap_tab8)

        # Create a QHBoxLayout for the buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.prev_btn_tab8)
        button_layout.addStretch(1)  # Adds a stretchable space between buttons
        button_layout.addWidget(self.next_btn_tab8)

        self.myTableWidget5 = QtWidgets.QTableWidget()
        self.myTableWidget5.setGeometry(QtCore.QRect(30, 600, 1300, 235))
        self.myTableWidget5.setRowCount(30)
        self.myTableWidget5.setColumnCount(11)
        self.myTableWidget5.setColumnWidth(0, 140)
        self.myTableWidget5.setColumnWidth(1, 140)
        self.myTableWidget5.setColumnWidth(2, 140)
        self.myTableWidget5.setColumnWidth(3, 140)
        self.myTableWidget5.setColumnWidth(4, 140)
        self.myTableWidget5.setColumnWidth(5, 140)
        self.myTableWidget5.setColumnWidth(6, 140)
        self.myTableWidget5.setColumnWidth(7, 140)
        self.myTableWidget5.setColumnWidth(8, 140)
        self.myTableWidget5.setColumnWidth(9, 140)
        self.myTableWidget5.setColumnWidth(10, 140)
        # self.myTableWidget5.setColumnWidth(12, 140)
        # self.myTableWidget5.setColumnWidth(13, 140)
        # self.myTableWidget5.setColumnWidth(14, 140)
        self.myTableWidget5.horizontalHeader().setStretchLastSection(True)

        self.myTableWidget5.setHorizontalHeaderLabels(
            ['id', 'Pipe_number', 'Absolute_distance', 'Upstream', 'Pipe_length', 'Feature_type',
             'Feature_identification',
             'Orientation_clock', 'Length', 'Width', 'Dent %']
        )

        self.hbox_20.addLayout(self.vbox_20)

        self.hbox_21 = QtWidgets.QHBoxLayout()
        self.hbox_22 = QtWidgets.QHBoxLayout()
        self.hbox_23 = QtWidgets.QHBoxLayout()
        self.vbox_20.addLayout(self.hbox_21)
        self.vbox_20.addLayout(self.hbox_22)

        # Set background color for the QHBoxLayout
        button_layout_widget = QtWidgets.QWidget()
        button_layout_widget.setStyleSheet("background-color: white;")
        button_layout_widget.setLayout(button_layout)
        # Add the button layout widget to the canvas layout
        self.vbox_20.addWidget(button_layout_widget)

        self.vbox_20.addLayout(self.hbox_23)

        self.hbox_21.addWidget(self.toolbar_20)
        self.hbox_21.addWidget(self.combo_box_tab8)
        self.hbox_21.addWidget(self.show_btn_tab8)
        self.hbox_21.addWidget(self.reset_btn_hm)

        self.hbox_22.addWidget(self.canvas_20)
        self.hbox_23.addWidget(self.myTableWidget5)

        self.setLayout(self.hbox_21)

        """
        Start from here second tab content for create_weld

        """

        ############## Table Widget(in the second tab) for create_weld information #############
        self.tab_showData.layout = QtWidgets.QVBoxLayout(self.tab_showData)
        self.myTableWidget = QtWidgets.QTableWidget()

        self.myTableWidget.setGeometry(QtCore.QRect(30, 30, 1000, 170))

        self.myTableWidget.setRowCount(7)
        self.myTableWidget.setColumnCount(11)
        self.myTableWidget.setColumnWidth(0, 140)
        self.myTableWidget.setColumnWidth(1, 140)
        self.myTableWidget.setColumnWidth(2, 140)
        self.myTableWidget.setColumnWidth(3, 140)
        self.myTableWidget.setColumnWidth(4, 140)
        self.myTableWidget.setColumnWidth(5, 140)
        self.myTableWidget.setColumnWidth(6, 140)
        self.myTableWidget.setColumnWidth(7, 140)
        self.myTableWidget.setColumnWidth(8, 140)
        self.myTableWidget.setColumnWidth(9, 140)
        self.myTableWidget.setColumnWidth(10, 140)
        self.myTableWidget.horizontalHeader().setStretchLastSection(True)

        self.myTableWidget.setHorizontalHeaderLabels(
            ['weld_number', 'runid', 'analytic_id', 'sensitivity', 'length',
             'start_index', 'end_index', 'start_oddo1', 'end_oddo1', 'start_oddo2', 'end_oddo2'])
        self.myTableWidget.doubleClicked.connect(self.viewClicked)
        self.myTableWidget.setSelectionBehavior(QTableView.SelectRows)
        ############# ShowWeld button(Inside the Second tab) #################
        self.ShowWeld = QtWidgets.QPushButton()
        self.ShowWeld.setGeometry(QtCore.QRect(690, 265, 160, 43))
        self.ShowWeld.setObjectName("Fetch Data")
        self.ShowWeld.setText("Fetch WeldDetail")
        ### Call the function Show_Weld #####
        self.ShowWeld.clicked.connect(self.Show_Weld)
        self.ShowWeld.setStyleSheet(Style.btn_type_primary)
        ### CreateWeld button(Inside the second tab) ###
        self.create_weld = QtWidgets.QPushButton()
        self.create_weld.setGeometry(QtCore.QRect(480, 265, 180, 43))
        self.create_weld.setObjectName("CreateWeld Data")
        self.create_weld.setText("Create_Weld")
        ############## Call the function CreateWeld #########
        self.create_weld.clicked.connect(self.CreateWeld)
        self.create_weld.setStyleSheet(Style.btn_type_primary)
        ################### End from here second tab content for create_weld #######################

        ############### start from here second content for weld_to_pipe record ####################

        ###############Table Widget(Inside the second tab) for weld_to_pipe information#############
        self.myTableWidget1 = QtWidgets.QTableWidget()

        self.myTableWidget1.setGeometry(QtCore.QRect(30, 310, 1300, 235))

        self.myTableWidget1.setRowCount(7)
        self.myTableWidget1.setColumnCount(8)
        self.myTableWidget1.setColumnWidth(0, 160)
        self.myTableWidget1.setColumnWidth(1, 160)
        self.myTableWidget1.setColumnWidth(2, 160)
        self.myTableWidget1.setColumnWidth(3, 160)
        self.myTableWidget1.setColumnWidth(4, 160)
        self.myTableWidget1.setColumnWidth(5, 160)
        self.myTableWidget1.setColumnWidth(6, 160)
        self.myTableWidget1.setColumnWidth(7, 160)
        self.myTableWidget1.horizontalHeader().setStretchLastSection(True)

        self.myTableWidget1.setHorizontalHeaderLabels(
            ['pipe_id', 'runid', 'analytic_id', 'lower_sensitivity', 'upper_sensitivity', 'length', 'start_index',
             'end_index'])
        ######################## Show_Weld_to_Pipe button(Inside the third tab) #################
        self.Show_Weld_to_Pipe = QtWidgets.QPushButton()
        self.Show_Weld_to_Pipe.setGeometry(QtCore.QRect(600, 550, 160, 43))
        self.Show_Weld_to_Pipe.setObjectName("Fetch Data")
        self.Show_Weld_to_Pipe.setText("Fetch WeldToPipe")
        ######## Call the function ShowWeldToPipe ##########
        self.Show_Weld_to_Pipe.clicked.connect(self.ShowWeldToPipe)
        self.Show_Weld_to_Pipe.setStyleSheet(Style.btn_type_primary)

        ###############Table Widget(Inside the Second tab) for defect_list information#############
        self.myTableWidget2 = QtWidgets.QTableWidget()
        self.myTableWidget2.setGeometry(QtCore.QRect(30, 600, 1300, 235))
        self.myTableWidget2.setRowCount(7)
        self.myTableWidget2.setColumnCount(11)
        self.myTableWidget2.setColumnWidth(0, 160)
        self.myTableWidget2.setColumnWidth(1, 160)
        self.myTableWidget2.setColumnWidth(2, 160)
        self.myTableWidget2.setColumnWidth(3, 160)
        self.myTableWidget2.setColumnWidth(4, 160)
        self.myTableWidget2.setColumnWidth(5, 160)
        self.myTableWidget2.setColumnWidth(6, 160)
        self.myTableWidget2.setColumnWidth(7, 160)
        self.myTableWidget2.setColumnWidth(8, 160)
        self.myTableWidget2.setColumnWidth(9, 160)
        self.myTableWidget2.setColumnWidth(10, 160)
        self.myTableWidget2.horizontalHeader().setStretchLastSection(True)

        self.myTableWidget2.setHorizontalHeaderLabels(
            ['defect_id', 'runid', 'start_observation', 'end_observation', 'start_sensor', 'end_sensor', 'angle',
             'length', 'breadth', 'depth', 'type'])

        ######################## Show_Weld_to_Pipe button(Inside the second tab) #################
        self.Show_Defect_list = QtWidgets.QPushButton()
        self.Show_Defect_list.setGeometry(QtCore.QRect(800, 840, 160, 43))
        self.Show_Defect_list.setObjectName("Fetch Data")
        self.Show_Defect_list.setText("Fetch DefectList")
        ######## Call the function ShowDefectList ##########
        self.Show_Defect_list.clicked.connect(self.DefectList)
        self.Show_Defect_list.setStyleSheet(Style.btn_type_primary)

        """
        End from here second tab content

        """


        ##################### Clock Heatmap Tab Start ##################

        self.hbox_24 = QtWidgets.QHBoxLayout(self.clock_heatmap)
        self.vbox_24 = QtWidgets.QVBoxLayout()

        self.m_output = QtWebEngineWidgets.QWebEngineView(self)

        self.figure_tab9 = plt.figure(figsize=(25, 8))
        self.canvas_tab9 = FigureCanvas(self.figure_tab9)
        self.toolbar_tab9 = NavigationToolbar(self.canvas_tab9, self)
        self.combo_box_tab9 = QtWidgets.QComboBox()
        self.show_btn_tab9 = QtWidgets.QPushButton('Show Pipe')
        self.show_btn_tab9.clicked.connect(self.tab9_clock_heatmap)

        # self.reset_btn_tab9 = QtWidgets.QPushButton('Reset Box')
        # self.reset_btn_tab9.clicked.connect(self.reset_btn_heatmap)

        # Add these lines inside __init__ method or where you define your GUI components
        # self.next_btn_tab9 = QtWidgets.QPushButton('Next')
        # self.next_btn_tab9.setStyleSheet("background-color: #4CAF50; color: white;")
        # self.next_btn_tab9.clicked.connect(self.show_next_clock_tab9)
        #
        # self.prev_btn_tab9 = QtWidgets.QPushButton('Previous')
        # self.prev_btn_tab9.setStyleSheet("background-color: #4CAF50; color: white;")
        # self.prev_btn_tab9.clicked.connect(self.show_previous_clock_tab9)
        #
        # # Create a QHBoxLayout for the buttons
        # button_layout = QtWidgets.QHBoxLayout()
        # button_layout.addWidget(self.prev_btn_tab9)
        # button_layout.addStretch(1)  # Adds a stretchable space between buttons
        # button_layout.addWidget(self.next_btn_tab9)

        self.myTableWidget_tab9 = QtWidgets.QTableWidget()
        self.myTableWidget_tab9.setGeometry(QtCore.QRect(30, 600, 1300, 235))
        self.myTableWidget_tab9.setRowCount(30)
        self.myTableWidget_tab9.setColumnCount(11)
        self.myTableWidget_tab9.setColumnWidth(0, 140)
        self.myTableWidget_tab9.setColumnWidth(1, 140)
        self.myTableWidget_tab9.setColumnWidth(2, 140)
        self.myTableWidget_tab9.setColumnWidth(3, 140)
        self.myTableWidget_tab9.setColumnWidth(4, 140)
        self.myTableWidget_tab9.setColumnWidth(5, 140)
        self.myTableWidget_tab9.setColumnWidth(6, 140)
        self.myTableWidget_tab9.setColumnWidth(7, 140)
        self.myTableWidget_tab9.setColumnWidth(8, 140)
        self.myTableWidget_tab9.setColumnWidth(9, 140)
        self.myTableWidget_tab9.setColumnWidth(10, 140)
        self.myTableWidget_tab9.horizontalHeader().setStretchLastSection(True)

        self.myTableWidget_tab9.setHorizontalHeaderLabels(
            ['id', 'Pipe_number', 'Absolute_distance', 'Upstream', 'Pipe_length', 'Feature_type',
             'Feature_identification',
             'Orientation_clock', 'Length', 'Width', 'Dent %']
        )

        self.hbox_24.addLayout(self.vbox_24)

        self.hbox_25 = QtWidgets.QHBoxLayout()
        self.hbox_26 = QtWidgets.QVBoxLayout()
        self.hbox_27 = QtWidgets.QHBoxLayout()
        self.vbox_24.addLayout(self.hbox_25)
        self.vbox_24.addLayout(self.hbox_26)

        # # Set background color for the QHBoxLayout
        # button_layout_widget = QtWidgets.QWidget()
        # button_layout_widget.setStyleSheet("background-color: white;")
        # button_layout_widget.setLayout(button_layout)
        # # Add the button layout widget to the canvas layout
        # self.vbox_24.addWidget(button_layout_widget)

        self.vbox_24.addLayout(self.hbox_27)

        self.hbox_25.addWidget(self.toolbar_tab9)
        self.hbox_25.addWidget(self.combo_box_tab9)
        self.hbox_25.addWidget(self.show_btn_tab9)
        # self.hbox_25.addWidget(self.reset_btn_tab9)

        # self.hbox_26.addWidget(self.canvas_24)

        self.hbox_26.addWidget(self.m_output)

        # self.hbox_26.setStretchFactor(self.m_output, 3)
        # self.hbox_26.addWidget(self.myTableWidget_tab9)

        self.setLayout(self.hbox_25)

        ##################### Clock Heatmap Tab End ##################



        self.tab_showData.layout.addWidget(self.myTableWidget)
        self.tab_showData.layout.addWidget(self.ShowWeld)
        self.tab_showData.layout.addWidget(self.create_weld)
        self.tab_showData.layout.addWidget(self.myTableWidget1)
        self.tab_showData.layout.addWidget(self.Show_Weld_to_Pipe)
        self.tab_showData.layout.addWidget(self.myTableWidget2)
        self.tab_showData.layout.addWidget(self.Show_Defect_list)
        self.tab_showData.setLayout(self.tab_showData.layout)

        self.right_tabWidget.addTab(self.tab_showData, "")
        self.right_tabWidget.addTab(self.tab_visualize, "")
        self.right_tabWidget.addTab(self.tab_line, "")
        self.right_tabWidget.addTab(self.tab_line1, "")
        self.right_tabWidget.addTab(self.tab_line2, "")
        self.right_tabWidget.addTab(self.tab_heatmap, "")
        self.right_tabWidget.addTab(self.clock_heatmap, "")

        self.main_right.addWidget(self.right_tabWidget, 1, 0, 1, 1)

    ################# When click the load List items ################
    def list_clicked(self, a):
        self.full_screen()
        self.project_name = a.text()

        self.init_tab()
        self.runid = Update_form_component.set_previous_form_data(a.text())

        ################Right tabWidget set Tab text#######################
        self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_update), "Pipe Details Update")
        self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_showData), "Weld And Pipe Show")
        self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_visualize), "Pipe Analysis With Heatmap")
        self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_line), "Pipe Analysis With Line")
        self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_line1), "Weld Selection")
        self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_line2), "Deformation selection")
        self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_heatmap), "Data Analysis")
        self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.clock_heatmap), "Heatmap")


    def show_next_heatmap_tab8(self):
        current_index = self.combo_box_tab8.currentIndex()
        if current_index < self.combo_box_tab8.count() - 1:
            self.combo_box_tab8.setCurrentIndex(current_index + 1)
            self.show_heatmap_tab8()

    def show_previous_heatmap_tab8(self):
        current_index = self.combo_box_tab8.currentIndex()
        if current_index > 0:
            self.combo_box_tab8.setCurrentIndex(current_index - 1)
            self.show_heatmap_tab8()

    def show_heatmap_tab8(self):
        weld_id = self.combo_box_tab8.currentText()
        self.weld_id = int(weld_id)
        runid = self.runid
        print(self.project_name)
        print("weld_id", weld_id)
        with connection.cursor() as cursor:
            Fetch_weld_detail = "SELECT start_index, end_index,start_oddo1,end_oddo1,start_oddo2,end_oddo2 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"
            # Execute query.
            cursor.execute(Fetch_weld_detail, (self.runid, self.weld_id, self.runid, self.weld_id))
            result = cursor.fetchall()
            print("result.....", result)
            start_oddo1 = result[0][2]
            end_oddo1 = result[1][3]
            start_oddo2 = result[0][4]
            end_oddo2 = result[1][5]
            print("start_oddo1", start_oddo1)
            print("end_oddo1", end_oddo1)
            print("start_oddo2", start_oddo2)
            print("end_oddo2", end_oddo2)
            self.weld_Pipe_length_oddo1 = end_oddo1 - start_oddo1
            self.weld_Pipe_length_oddo2 = end_oddo2 - start_oddo2
            if result:
                print("hi1")
                path = Config.weld_pipe_pkl + self.project_name + '/' + str(weld_id) + '.pkl'
                if os.path.isfile(path):
                    Config.print_with_time("File exist")
                    df_pipe = pd.read_pickle(path)
                    # df_pipe.to_csv("C:Users/Shradha Agarwal/Desktop/2.csv")
                    self.df_pipe_DA = df_pipe
                    print(path)
                    self.index_tab8 = df_pipe['index']
                    self.oddo1_heatmap1_mm = df_pipe['ODDO1'] - Config.oddo1
                    self.oddo1_heatmap_m = ((df_pipe['ODDO1'] - Config.oddo1) / 1000).round(3)
                    self.oddo2_heatmap1_mm = df_pipe['ODDO2'] - Config.oddo2
                    self.oddo2_heatmap_m = ((df_pipe['ODDO2'] - Config.oddo2) / 1000).round(3)
                    self.plot_heatmap(df_pipe, self.oddo1_heatmap_m, self.oddo1_heatmap1_mm, self.oddo2_heatmap_m,
                                      self.oddo2_heatmap1_mm, self.index_tab8)
                else:
                    print("result....", result)
                    folder_weld_path = Config.weld_pipe_pkl + self.project_name
                    print(folder_weld_path)
                    Config.print_with_time("File not exist")
                    try:
                        os.makedirs(folder_weld_path)
                    except:
                        Config.print_with_time("Folder already exists")

                    for i in range(len(result) - 1):
                        start_index, end_index = result[0][0], result[1][1]
                    print(start_index, end_index)
                    Config.print_with_time("Start fetching at : ")
                    query_for_start = 'SELECT * FROM ' + Config.table_name + ' WHERE index>={} AND  index<={} order by index'
                    query_job = client.query(query_for_start.format(start_index, end_index))
                    df_pipe = query_job.result().to_dataframe()
                    # print("dataframe", df_pipe)
                    df_pipe.to_pickle(folder_weld_path + '/' + str(weld_id) + '.pkl')
                    Config.print_with_time("Succesfully saved to pickle file")
                    self.df_pipe_DA = df_pipe
                    self.index_tab8 = df_pipe['index']
                    self.oddo1_heatmap1_mm = df_pipe['ODDO1'] - Config.oddo1
                    self.oddo1_heatmap_m = ((df_pipe['ODDO1'] - Config.oddo1) / 1000).round(3)
                    self.oddo2_heatmap1_mm = df_pipe['ODDO2'] - Config.oddo2
                    self.oddo2_heatmap_m = ((df_pipe['ODDO2'] - Config.oddo2) / 1000).round(3)
                    self.plot_heatmap(df_pipe, self.oddo1_heatmap_m, self.oddo1_heatmap1_mm, self.oddo2_heatmap_m,
                                      self.oddo2_heatmap1_mm, self.index_tab8)

            else:
                Config.print_with_time("No data found for this weld ID : ")

    def plot_heatmap(self, df_pipe, oddo1_heatmap_m, oddo1_heatmap1_mm, oddo2_heatmap_m, oddo2_heatmap1_mm, index_tab8):
        # print("oddo1_heatmap_m",oddo1_heatmap_m)
        # print("oddo1_heatmap_mm", oddo1_heatmap1_mm),
        # print("index_tab8",index_tab8)
        self.oddo1_heatmap1_mm_latest = list(oddo1_heatmap1_mm)
        self.oddo2_heatmap1_mm_latest = list(oddo2_heatmap1_mm)
        self.figure_20.clear()
        ax20 = self.figure_20.add_subplot(111)
        ax20.figure.subplots_adjust(bottom=0.213, left=0.077, top=0.855, right=1.000)

        df = df_pipe[['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5',
                      'proximity6', 'proximity7', 'proximity8', 'proximity9', 'proximity10',
                      'proximity11', 'proximity12',
                      'proximity13', 'proximity14', 'proximity15', 'proximity16',
                      'proximity17',
                      'proximity18','proximity19', 'proximity20', 'proximity21',
                                             'proximity22',
                                             'proximity23', 'proximity24']]

        sensor_column_fill = df.ffill(axis=0)
        Mean1 = sensor_column_fill.mean()

        # Multiply the value at proximity17 by 2
        Mean1['proximity17'] *= 1.00105

        # Mean1['proximity18'] *= 1.00112

        Mean1.tolist()
        # print("mean...", Mean1)

        df3 = ((sensor_column_fill - Mean1) / Mean1) * 10000

        df3[df3 < 0] = 0

        d1 = (df3.set_index(index_tab8).T).astype(float)
        print("dataframe", d1)

        # color_ranges = [
        #     (0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 90),
        #     (90, 100)]
        #
        # color_values = [
        #     '#82ffff', '#00CD00', '#008000', '#fd8f00', '#D98719', '#CD661D', '#EE4000',
        #     '#FF0000', '#820202', '#000000']

        color_ranges = [
            (-100, -90), (-90, -80), (-80, -70), (-70, -60), (-60, -50), (-50, -40), (-40, -30), (-30, -20),
            (-20, -10), (-10, 0),
            (0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 90),
            (90, 100)]

        color_values = ['#3d045a', '#4f355c', '#CD1076', '#8E236B', '#0530ad', '#6205db', '#8f39ff',
                        '#016fff', '#74b0ff', '#82ffff',
                        '#82ffff', '#00CD00', '#008000', '#fd8f00', '#D98719', '#CD661D', '#EE4000',
                        '#FF0000', '#820202', '#000000']

        custom_palette = sns.color_palette(color_values)

        bounds = [r[0] for r in color_ranges] + [color_ranges[-1][1]]

        cmap = ListedColormap(color_values)

        norm = BoundaryNorm(bounds, cmap.N)

        heat_map_obj = sns.heatmap(d1, cmap=cmap, ax=ax20, norm=norm)

        # heat_map_obj = sns.heatmap(d1, cmap='jet', ax=ax20, vmin=-50, vmax=50)
        heat_map_obj.set(xlabel="Index", ylabel="Sensors")
        ax20.set_xticklabels(ax20.get_xticklabels(), size=9)
        ax20.set_yticklabels(ax20.get_yticklabels(), size=9)

        # oddo1_li = list(oddo1_heatmap_m)
        oddo1_li = list(oddo2_heatmap_m)
        ax2 = ax20.twiny()
        num_ticks1 = len(ax20.get_xticks())  # Adjust the number of ticks based on your preference
        tick_positions1 = [int(i) for i in np.linspace(0, len(oddo1_li) - 1, num_ticks1)]
        ax2.set_xticks(tick_positions1)
        ax2.set_xticklabels([f'{oddo1_li[i]:.3f}' for i in tick_positions1], rotation=90)
        ax2.set_xlabel("Absolute Distance (m)")

        def on_hover(event):
            if event.xdata is not None and event.ydata is not None:
                x = int(event.xdata)
                y = int(event.ydata)
                self.index_hm_set = index_tab8.to_list()
                index_value = self.index_hm_set[x]
                value = d1.iloc[y, x]
                z = oddo1_li[x]
                self.toolbar_20.set_message(
                    f'Counter={index_value:.0f},Abs.distance(m)={z},Sensor_no={y:.0f},Value={value:.3f}')

        self.figure_20.canvas.mpl_connect('motion_notify_event', on_hover)

        plt.tight_layout()
        self.canvas_20.draw()
        rs = RectangleSelector(self.figure_20.gca(), self.line_select_callback,
                               useblit=False)
        plt.connect('key_press_event', rs)
        with connection.cursor() as cursor:
            Fetch_weld_detail = "select id,Pipe_No,Absolute_distance,Upstream,Pipe_length,Feature_type,Feature_identification,Orientation,length,Width,Depth_percentage from dent_update where runid='%s' and Pipe_No='%s'"
            # Execute query.
            cursor.execute(Fetch_weld_detail, (int(self.runid), int(self.weld_id)))
            self.myTableWidget5.setRowCount(0)
            allSQLRows = cursor.fetchall()
            if allSQLRows:
                for row_number, row_data in enumerate(allSQLRows):
                    self.myTableWidget5.insertRow(row_number)
                    for column_num, data in enumerate(row_data):
                        self.myTableWidget5.setItem(row_number, column_num,
                                                    QtWidgets.QTableWidgetItem(str(data)))
                self.myTableWidget5.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.myTableWidget5.doubleClicked.connect(self.handle_table_double_click)
            else:
                # self.myTableWidget5.doubleClicked.disconnect(self.handle_table_double_click)
                Config.warning_msg("No record found", "")

    def line_select_callback(self, eclick, erelease):
        self.rect_start_hm = eclick.xdata, eclick.ydata
        self.rect_end_hm = erelease.xdata, erelease.ydata
        self.draw_rectangle_2()

    def draw_rectangle_2(self):
        # Function to draw a rectangle on the Matplotlib plot
        if self.rect_start_hm is not None and self.rect_end_hm is not None:
            for patch in self.figure_20.gca().patches:
                patch.remove()
            x_start, y_start = self.rect_start_hm
            x_end, y_end = self.rect_end_hm
            if x_start is not None and y_start is not None and x_end is not None and y_end is not None:
                rect = plt.Rectangle(
                    (min(x_start, x_end), min(y_start, y_end)),
                    abs(x_end - x_start),
                    abs(y_end - y_start),
                    edgecolor='black',
                    linewidth=1,
                    fill=False
                )
                self.figure_20.gca().add_patch(rect)
                self.canvas_20.draw()
                self.show_name_dialog2()

    def show_name_dialog2(self):
        while True:
            name, ok = QInputDialog.getText(self, 'Enter Name', 'Enter the name of the drawn box:')
            if ok:
                if name.strip():  # Check if the entered name is not empty or just whitespace
                    x_start, y_start = self.rect_start_hm
                    x_end, y_end = self.rect_end_hm
                    runid = self.runid
                    pipe = self.weld_id
                    self.index_hm_set = self.index_tab8.to_list()
                    y_start15 = round(y_start)
                    y_end15 = round(y_end)
                    start_index15 = self.index_hm_set[round(x_start)]
                    end_index15 = self.index_hm_set[round(x_end)]
                    print("start_index", start_index15)
                    print("end_index", end_index15)
                    print("start_sensor", y_start15)
                    print("end_sensor", y_end15)
                    finial_defect_list = []
                    Config.print_with_time("Start fetching at : ")
                    query_for_start = 'SELECT * FROM ' + Config.table_name + ' WHERE index>={} AND  index<={} order by index'
                    query_job = client.query(query_for_start.format(start_index15, end_index15))
                    df_pipe = query_job.result().to_dataframe()
                    oddo1 = list(df_pipe['ODDO1'] - Config.oddo1)
                    oddo2 = list(df_pipe['ODDO2'] - Config.oddo2)
                    roll = list(df_pipe['ROLL'] - Config.roll_value)
                    print("oddo1", oddo1)
                    print("oddo2", oddo2)
                    print("roll", roll)

                    self.df_new = pd.DataFrame(self.df_pipe_DA, columns=['proximity1', 'proximity2', 'proximity3', 'proximity4',
                                                            'proximity5', 'proximity6', 'proximity7', 'proximity8',
                                                            'proximity9', 'proximity10', 'proximity11', 'proximity12',
                                                            'proximity13', 'proximity14', 'proximity15',
                                                            'proximity16', 'proximity17', 'proximity18', 'proximity19', 'proximity20', 'proximity21',
                                             'proximity22',
                                             'proximity23', 'proximity24'])

                    """
                    Calculate Upstream Distance oddo1 and oddo2
                    """
                    upstream_oddo1 = oddo1[0] - self.oddo1_heatmap1_mm_latest[0]
                    upstream_oddo2 = oddo2[0] - self.oddo2_heatmap1_mm_latest[0]
                    print("upstream_oddo1=>", upstream_oddo1)
                    print("upstream_oddo2=>", upstream_oddo2)

                    """
                    Calculate length of the defect
                    """
                    length_of_defect_oddo1 = round(oddo1[-1] - oddo1[0])
                    length_of_defect_oddo2 = round(oddo2[-1] - oddo2[0])
                    print("length_of_defect_oddo1=>", length_of_defect_oddo1)
                    print("length_of_defect_oddo2=>", length_of_defect_oddo2)

                    """
                    Calculate Abs.Distance of the defect
                    """
                    Abs_Distance_oddo1 = oddo1[0]
                    print("Abs.distance_oddo1=>", Abs_Distance_oddo1)

                    Abs_Distance_oddo2 = oddo2[0]
                    print("Abs.distance_oddo1=>", Abs_Distance_oddo2)

                    """
                    Calculate Width of the Defect
                    """
                    Width = Width_calculation(y_start15, y_end15)
                    Width = round(Width)
                    print("Width of Defect=>", Width)

                    type = 'External'

                    sensor_no = int((y_start15 + y_end15)/2)

                    angle = self.defect_marking_clock(roll, sensor_no, Abs_Distance_oddo2, oddo2)
                    print("angle", angle)

                    finial_defect_list.append({"start_index": start_index15, "end_index": end_index15,
                                               "start_sensor": y_start15, "end_sensor": y_end15,
                                               "Absolute_distance": int(Abs_Distance_oddo2),
                                               "Upstream": int(upstream_oddo2),
                                               "Pipe_length": self.weld_Pipe_length_oddo2,
                                               "Feature_type": type, "Feature_identification": name,
                                               "Orientation": angle, "WT": None,
                                               "length": length_of_defect_oddo2, "Width": Width,
                                               "Depth_percentage": None})
                    for i in finial_defect_list:
                        start_index = i['start_index']
                        end_index = i['end_index']
                        start_sensor = i['start_sensor']
                        end_sensor = i['end_sensor']
                        Absolute_distance = i['Absolute_distance']
                        Upstream = i['Upstream']
                        Pipe_length = i['Pipe_length']
                        Feature_type = i['Feature_type']
                        Feature_identification = i['Feature_identification']
                        Orientation = i['Orientation']
                        WT = i['WT']
                        length = i['length']
                        Width = i['Width']

                        Depth_percentage = i['Depth_percentage']

                        """
                        Insert data into database
                        """
                        with connection.cursor() as cursor:
                            query_defect_insert = "INSERT INTO dent_update (runid,Pipe_No,start_index,end_index,start_sensor,end_sensor,Absolute_distance,Upstream,Pipe_length,Feature_type,Feature_identification,Orientation,WT,length,Width,Depth_percentage) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

                            cursor.execute(query_defect_insert, (
                                int(runid), pipe, start_index, end_index, start_sensor, end_sensor,
                                Absolute_distance, Upstream, Pipe_length, Feature_type, Feature_identification,
                                Orientation, WT, length, Width, Depth_percentage))

                            connection.commit()
                        with connection.cursor() as cursor:
                            Fetch_weld_detail = "select id,Pipe_No,Absolute_distance,Upstream,Pipe_length,Feature_type,Feature_identification,Orientation,length,Width,Depth_percentage from dent_update where runid='%s' and Pipe_No='%s'"
                            # Execute query.
                            cursor.execute(Fetch_weld_detail, (int(self.runid), int(self.weld_id)))
                            self.myTableWidget5.setRowCount(0)
                            allSQLRows = cursor.fetchall()
                            if allSQLRows:
                                for row_number, row_data in enumerate(allSQLRows):
                                    self.myTableWidget5.insertRow(row_number)
                                    for column_num, data in enumerate(row_data):
                                        self.myTableWidget5.setItem(row_number, column_num,
                                                                    QtWidgets.QTableWidgetItem(str(data)))
                                self.myTableWidget5.setEditTriggers(QAbstractItemView.NoEditTriggers)
                                self.myTableWidget5.doubleClicked.connect(self.handle_table_double_click)
                            else:
                                # self.myTableWidget5.doubleClicked.disconnect(self.handle_table_double_click)
                                Config.warning_msg("No record found", "")
                    break
                else:
                    QMessageBox.warning(self, 'Invalid Input', 'Please enter a name.')
            else:
                print('Operation canceled.')
                break

    def defect_marking_clock(self, roll, sensor_no, abs_distance, oddo2_list):
        oddo2_list = [int(j) for j in oddo2_list]
        first_key_values = roll
        roll_dictionary = {'1': first_key_values}
        angle =[0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340]

        for i in range(2, 19):
            current_values = [round((value + angle[i-1]), 2) for value in first_key_values]
            roll_dictionary['{}'.format(i)] = current_values

        clock_dictionary = {}
        for key in roll_dictionary:
            clock_dictionary[key] = [self.degrees_to_hours_minutes(value) for value in roll_dictionary[key]]
        Roll_hr = pd.DataFrame(clock_dictionary)
        Roll_hr['ODDO2'] = oddo2_list
        # print("Roll_hr...", Roll_hr)

        index = oddo2_list.index(int(abs_distance))
        abs_distance_c = Roll_hr.iloc[index]
        value_clock = abs_distance_c[sensor_no]

        return value_clock


    def handle_table_double_click(self, item):
        # Get the row data including the unique ID
        row = item.row()
        unique_id = self.myTableWidget5.item(row, 0).text()  # Assuming the ID is in the first column

        # Query the database for the coordinates corresponding to the unique ID
        with Config.connection.cursor() as cursor:
            query_for_coordinates = "SELECT start_index, end_index, start_sensor, end_sensor, length,Feature_identification FROM dent_update WHERE id = %s"
            b = cursor.execute(query_for_coordinates, (unique_id))
            result = cursor.fetchone()  # Assuming the query returns only one row
            if result:
                start_index, end_index, y_start_hm, y_end_hm, length, Feature_identification = result
                print("Table Widget Query...", start_index, end_index, y_start_hm, y_end_hm)
                self.annotate_heatmap(start_index, end_index, y_start_hm, y_end_hm, unique_id, Feature_identification)
            else:
                QMessageBox.warning(self, 'Warning', 'No Record Found')

    def annotate_heatmap(self, start_index, end_index, y_start_hm, y_end_hm, unique_id, Feature_identification):
        self.index_hm_set = self.index_tab8.to_list()
        start_x_pos = self.index_hm_set.index(start_index)
        end_x_pos = self.index_hm_set.index(end_index)
        # Draw a rectangle on the heatmap image using matplotlib patches
        rect_width = end_x_pos - start_x_pos
        rect_height = y_end_hm - y_start_hm

        # Add unique ID annotation
        text_x_pos = (start_x_pos + end_x_pos) / 2  # Calculate the center position for the text
        text_y_pos = y_start_hm - 0.1 * rect_height  # Position the text slightly above the rectangle
        self.figure_20.gca().text(text_x_pos, text_y_pos, Feature_identification + '-' + unique_id, ha='center',
                                  va='bottom')

        # Create a Rectangle patch
        rect = Rectangle((start_x_pos, y_start_hm), rect_width, rect_height, edgecolor='black', linewidth=1, fill=False)
        self.figure_20.gca().add_patch(rect)
        self.canvas_20.draw()  # Redraw the canvas to display the rectangle

    def reset_btn_fun_heatmap(self):
        if self.figure_20.gca().patches:
            for patch in self.figure_20.gca().patches:
                patch.remove()
            for text in self.figure_20.gca().texts:
                text.remove()
            self.canvas_20.draw()
            self.rect_start_hm = None  # Store the starting point of the rectangle
            self.rect_end_hm = None


    # def show_next_clock_tab9(self):
    #     current_index = self.combo_box_tab9.currentIndex()
    #     if current_index < self.combo_box_tab9.count() - 1:
    #         self.combo_box_tab9.setCurrentIndex(current_index + 1)
    #         self.tab9_clock_heatmap()
    #
    # def show_previous_clock_tab9(self):
    #     current_index = self.combo_box_tab9.currentIndex()
    #     if current_index > 0:
    #         self.combo_box_tab9.setCurrentIndex(current_index - 1)
    #         self.tab9_clock_heatmap()


    def tab9_clock_heatmap(self):
        Config.print_with_time("Clock Heatmap called")
        runid = self.runid
        Weld_id_tab9 = self.combo_box_tab9.currentText()
        self.Weld_id_tab9 = int(Weld_id_tab9)
        # self.lower_sensitivity_tab9 = self.lower_Sensitivity_combo_box_tab9.currentText()
        # self.upper_sensitivity_tab9 = self.upper_Sensitivity_combo_box_tab9.currentText()

        with connection.cursor() as cursor:
            # query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
            query = "SELECT start_index, end_index,start_oddo1,end_oddo1 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"
            cursor.execute(query, (self.runid, self.Weld_id_tab9, self.runid, self.Weld_id_tab9))
            result = cursor.fetchall()
            start_oddo1=result[0][2]
            end_oddo1=result[1][3]

            self.weld_pipe_tab9=end_oddo1-start_oddo1
            print("Weld_pipe_Length",self.weld_pipe_tab9)
            if not result:
                Config.print_with_time("No data found for this pipe ID : ")
            else:
                """
                pkl file is found in local path 
                """
                path = Config.clock_pkl + self.project_name + '/' + str(self.Weld_id_tab9) + '.pkl'
                # print(path)
                if os.path.isfile(path):
                    Config.print_with_time("File exist")

                    df_clock_holl = pd.read_pickle(path)
                    # print(df_clock_holl.columns)
                    df_new_1 = df_clock_holl[['0:00:00', '0:40:00', '1:20:00', '2:00:00',
                                               '2:40:00', '3:20:00', '4:00:00', '4:40:00', '5:20:00', '6:00:00',
                                               '6:40:00', '7:20:00', '8:00:00', '8:40:00', '9:20:00', '10:00:00',
                                               '10:40:00', '11:20:00']]

                    df_clock_index = df_clock_holl['index']
                    df_clock_holl_oddo = ((df_clock_holl['ODDO2'])/1000).round(3)
                    df_new_1[df_new_1 < 0] = 0
                    d1 = (df_new_1).T
                    self.df_clock_index = df_clock_index

                    color_ranges = [
                        (-100, -90), (-90, -80), (-80, -70), (-70, -60), (-60, -50), (-50, -40), (-40, -30), (-30, -20),
                        (-20, -10), (-10, 0),
                        (0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 90),
                        (90, 100)
                    ]

                    color_values = [
                        '#3d045a', '#4f355c', '#CD1076', '#8E236B', '#0530ad', '#6205db', '#8f39ff',
                        '#016fff', '#74b0ff', '#82ffff',
                        '#82ffff', '#00CD00', '#008000', '#fd8f00', '#D98719', '#CD661D', '#EE4000',
                        '#FF0000', '#820202', '#000000'
                    ]

                    # Normalize the bounds to [0, 1]
                    bounds = [(r[0] + 100) / 200 for r in color_ranges] + [(color_ranges[-1][1] + 100) / 200]

                    # Create the colorscale
                    colorscale = []
                    for i in range(len(color_values)):
                        colorscale.append([bounds[i], color_values[i]])
                        colorscale.append([bounds[i + 1], color_values[i]])

                    heatmap_trace=go.Heatmap(x=[df_clock_index, df_clock_holl_oddo],
                                             y=[df_new_1.index, df_new_1.columns],
                                             z=d1,
                                             zmin=-100,
                                             zmax=100,
                                             colorscale=colorscale)


                    # heatmap_trace=go.Heatmap(x=[df_clock_index, df_clock_holl_oddo],
                    #          z=d1,
                    #          y=[df_new_1.index, df_new_1.columns],
                    #          zmin=-50,
                    #          zmax=50,
                    #          colorscale='jet')

                    fig = go.Figure(data=heatmap_trace)
                    self.fig = fig
                    fig.update_xaxes(title_text='Absolute Distance(m)',
                                     tickfont=dict(size=11),
                                     dtick=1500,
                                     tickangle=0, showticklabels=True, ticklen=0)
                    fig.update_yaxes(title_text='Orientation')

                    # plotly.offline.plot(fig, filename='heatmap.html', auto_open=False)
                    pio.write_html(fig, file='heatmap.html', auto_open=False)
                    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "heatmap.html"))
                    self.m_output.load(QUrl.fromLocalFile(file_path))

                else:
                    """
                    pkl file is not found than data fetch from GCP and save pkl file in local path
                    """
                    folder_path = Config.clock_pkl + self.project_name
                    # print(folder_path)
                    Config.print_with_time("File not exist")
                    try:
                        os.makedirs(folder_path)
                    except:
                        Config.print_with_time("Folder already exists")

                    start_index, end_index = result[0][0], result[1][1]
                    print(start_index, end_index)
                    Config.print_with_time("Start fetching at : ")

                    query_for_start = 'SELECT index, ODDO1, ODDO2, ROLL,[proximity1, proximity2, proximity3, proximity4,' \
                                      ' proximity5, proximity6, proximity7, proximity8, proximity9, proximity10, proximity11, ' \
                                      'proximity12, proximity13, proximity14, proximity15, proximity16, proximity17, ' \
                                      'proximity18, proximity19, proximity20, proximity21,proximity22, proximity23, proximity24] FROM ' + Config.table_name + ' WHERE index>={} AND index<={} AND runid={} order by index'
                    query_job = client.query(query_for_start.format(start_index, end_index, runid))
                    results = query_job.result()


                    # query, config = query_generator.get_pipe(self.lower_sensitivity_tab9, self.upper_sensitivity_tab9, runid,
                    #                                          start_index, end_index, self.Weld_id_tab9)
                    # query_job = client.query(query)
                    # results = query_job.result()

                    Config.print_with_time("End fetching  at : ")

                    data = []
                    self.index_tab9 = []
                    oddo_1 = []
                    oddo_2 = []
                    indexes = []
                    roll1 = []

                    Config.print_with_time("Start of conversion at : ")
                    for row in results:
                        self.index_tab9.append(row[0])
                        oddo_1.append(row[1])
                        oddo_2.append(row[2])
                        roll1.append(row[3])
                        data.append(row[4])


                    oddo1_tab9 = []
                    oddo2_tab9 = []
                    roll = []

                    """
                    Reference value will be consider 
                    """
                    for odometer1 in oddo_1:
                        od1 = odometer1 - Config.oddo1  ###16984.2 change According to run
                        oddo1_tab9.append(od1)
                    for odometer2 in oddo_2:
                        od2 = odometer2 - Config.oddo2  ###17690.36 change According to run
                        oddo2_tab9.append(od2)

                    """
                    Reference value will be consider
                    """
                    for roll2 in roll1:
                        roll3 = roll2 - Config.roll_value
                        roll.append(roll3)

                    df_new_tab9 = pd.DataFrame(data, columns=['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5',
                                                              'proximity6', 'proximity7', 'proximity8', 'proximity9', 'proximity10',
                                                              'proximity11', 'proximity12',
                                                              'proximity13', 'proximity14', 'proximity15', 'proximity16',
                                                              'proximity17',
                                                              'proximity18', 'proximity19', 'proximity20', 'proximity21', 'proximity22', 'proximity23', 'proximity24'])

                    df_clock_tranpose, df_clock = self.Roll_Calculation(df_new_tab9, roll)
                    Config.print_with_time("End of conversion at : ")

                    # index = df['index']
                    # oddo1 = df['ODDO1']
                    # oddo2 = df['ODDO2']
                    # index.reset_index(inplace=True, drop=True)
                    # oddo1.reset_index(inplace=True, drop=True)
                    # oddo2.reset_index(inplace=True, drop=True)

                    df_elem = pd.DataFrame({"index":self.index_tab9, "ODDO1":oddo1_tab9, "ODDO2":oddo2_tab9})
                    frames = [df_elem, df_clock]
                    df_new = pd.concat(frames, axis=1, join='inner')
                    df_new.to_pickle(folder_path + '/' + str(self.Weld_id_tab9) + '.pkl')
                    Config.print_with_time("Succesfully saved to pickle file")
                    df_clock_holl_oddo1 = (df_new['ODDO2']/1000).round(3)
                    df_clock_index = df_new['index']

                    self.df_clock_index = df_clock_index

                    color_ranges = [
                        (-100, -90), (-90, -80), (-80, -70), (-70, -60), (-60, -50), (-50, -40), (-40, -30), (-30, -20),
                        (-20, -10), (-10, 0),
                        (0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 90),
                        (90, 100)
                    ]

                    color_values = [
                        '#3d045a', '#4f355c', '#CD1076', '#8E236B', '#0530ad', '#6205db', '#8f39ff',
                        '#016fff', '#74b0ff', '#82ffff',
                        '#82ffff', '#00CD00', '#008000', '#fd8f00', '#D98719', '#CD661D', '#EE4000',
                        '#FF0000', '#820202', '#000000'
                    ]

                    # Normalize the bounds to [0, 1]
                    bounds = [(r[0] + 100) / 200 for r in color_ranges] + [(color_ranges[-1][1] + 100) / 200]

                    # Create the colorscale
                    colorscale = []
                    for i in range(len(color_values)):
                        colorscale.append([bounds[i], color_values[i]])
                        colorscale.append([bounds[i + 1], color_values[i]])

                    heatmap_trace=go.Heatmap(x=[df_clock_index, df_clock_holl_oddo1],
                                             y=[df_clock.index, df_clock.columns],
                                             z=df_clock_tranpose,
                                             zmin=-100,
                                             zmax=100,
                                             colorscale=colorscale)

                    # heatmap_trace=go.Heatmap(x=[df_clock_index, df_clock_holl_oddo1],
                    #                          y=[df_clock.index, df_clock.columns],
                    #                          z=df_clock_tranpose,
                    #                          zmin=-50,
                    #                          zmax=50,
                    #                          colorscale='jet')
                    fig = go.Figure(data=heatmap_trace)
                    self.fig = fig
                    fig.update_xaxes(title_text='Absolute Distance(m)',
                                     tickfont=dict(size=11),
                                     dtick=1500,
                                     tickangle=0, showticklabels=True, ticklen=0)
                    fig.update_yaxes(title_text='Orientation')

                    # plotly.offline.plot(fig, filename='heatmap.html', auto_open=False)
                    pio.write_html(fig, file='heatmap.html', auto_open=False)
                    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "heatmap.html"))
                    self.m_output.load(QUrl.fromLocalFile(file_path))

    #             timer = QTimer()
    #     #             timer.singleShot(2000, lambda: self.execute_table_query(int(runid), int(Weld_id_tab9)))  # Delay of 5 seconds
    #     #
    #     # def execute_table_query(self, runid, Weld_id_tab9):
    #     #     # Your code for the table query
    #     #     with connection.cursor() as cursor:
    #     #         Fetch_weld_detail = "select id,Pipe_No,Absolute_distance,Upstream,Pipe_length,Feature_type,Feature_identification,Orientation,length,Width,Depth_percentage from dent_update where runid='%s' and Pipe_No='%s'"
    #     #         cursor.execute(Fetch_weld_detail, (runid, Weld_id_tab9))
    #     #         self.myTableWidget_tab9.setRowCount(0)
    #     #         allSQLRows = cursor.fetchall()
    #     #         if allSQLRows:
    #     #             for row_number, row_data in enumerate(allSQLRows):
    #     #                 self.myTableWidget_tab9.insertRow(row_number)
    #     #                 for column_num, data in enumerate(row_data):
    #     #                     self.myTableWidget_tab9.setItem(row_number, column_num, QtWidgets.QTableWidgetItem(str(data)))
    #     #             self.myTableWidget_tab9.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #     #             self.myTableWidget_tab9.doubleClicked.connect(self.handle_table_double_click_tab9)
    #     #         else:
    #     #             Config.warning_msg("No record found", "")

    def degrees_to_hours_minutes(self, degrees):
        if (degrees < 0):
            degrees = degrees % 360
        elif degrees >= 360:
            degrees %= 360
        degrees_per_second = 360 / (12 * 60 * 60)
        total_seconds = degrees / degrees_per_second
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def Roll_Calculation(self, df_hall, roll):
        # df_x1=pd.DataFrame({"index":index,"Roll":roll,"ODDO1":oddo1,"ODDO2":oddo2})
        # # print(df_x)
        # frames = [df_x1, df_hall]
        # df1 = pd.concat(frames, axis=1, join='inner')
        # # print(df1)
        # # df1.to_csv("C:/Users/Shradha Agarwal/Desktop/test_new.csv")
        #
        # angle =[0, 3.75, 7.5, 11.25, 15.0, 18.75, 22.5, 26.25, 30.0, 33.75, 37.5, 41.25, 45.0, 48.75, 52.5, 56.25, 60.0, 63.75,
        #  67.5, 71.25, 75.0, 78.75, 82.5, 86.25, 90.0, 93.75, 97.5, 101.25, 105.0, 108.75, 112.5, 116.25, 120.0, 123.75,
        #  127.5, 131.25, 135.0, 138.75, 142.5, 146.25, 150.0, 153.75, 157.5, 161.25, 165.0, 168.75, 172.5, 176.25, 180.0,
        #  183.75, 187.5, 191.25, 195.0, 198.75, 202.5, 206.25, 210.0, 213.75, 217.5, 221.25, 225.0, 228.75, 232.5, 236.25,
        #  240.0, 243.75, 247.5, 251.25, 255.0, 258.75, 262.5, 266.25, 270.0, 273.75, 277.5, 281.25, 285.0, 288.75, 292.5,
        #  296.25, 300.0, 303.75, 307.5, 311.25, 315.0, 318.75, 322.5, 326.25, 330.0, 333.75, 337.5, 341.25, 345.0, 348.75,
        #  352.5, 356.25]
        #
        # for i in range(len(angle)):
        #     df1['Roll'+str(i+1)] = df1['Roll'] + angle[i]
        #
        # roll_res=[f'Roll{i}' for i in range(1, 97)]
        #
        # roll_df2=df1[[f'Roll{i}' for i in range(1, 97)]]
        #
        # df_hall=df1[[f'F{i}H{j}' for i in range(1, 25) for j in range(1, 5)]]
        #
        # k=roll_df2.values.tolist()
        #
        # s=[]
        # for i in k:
        #     g=[]
        #     for j in i:
        #         k=self.degrees_to_hours_minutes(j)
        #         g.append(k)
        #     s.append(g)
        # Roll_hr=pd.DataFrame(s)
        # Roll_hr_min=Roll_hr.transpose()
        #

        mean1=df_hall.mean()
        # mean1['proximity18'] *= 1.00112
        # mean1['proximity17'] *= 1.00105
        mean1.tolist()
        df_hall = ((df_hall - mean1) / mean1) * 10000

        # for i,data in enumerate(df_hall.columns):
        #     df_hall[data]=(df_hall[data]-mean1[i])/df_hall[data]*10000

        df_hall[df_hall < 0] = 0

        first_key_values = roll
        roll_dictionary = {'1': first_key_values}
        angle = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300, 315, 330, 345]

        for i in range(2, 25):
            current_values = [round((value + angle[i-1]), 2) for value in first_key_values]
            roll_dictionary['{}'.format(i)] = current_values

        clock_dictionary = {}
        for key in roll_dictionary:
            clock_dictionary[key] = [self.degrees_to_hours_minutes(value) for value in roll_dictionary[key]]

        Roll_hr = pd.DataFrame(clock_dictionary)

        df_hall.reset_index(inplace=True, drop=True)
        k=(df_hall.transpose()).astype(float)
        k.reset_index(inplace=True, drop=True)

        time_list = [timedelta(minutes=i*30) for i in range(24)]

        clock_list = [(time_list[i], time_list[i+1]) for i in range(len(time_list)-1)]
        clock_list.append((time_list[-1], timedelta(days=1)))

        clock_df = Roll_hr.applymap(lambda x: timedelta(hours=int(x.split(':')[0]), minutes=int(x.split(':')[1]), seconds=int(x.split(':')[2])) if isinstance(x, str) else x)
        df_clock = pd.DataFrame(0, index=range(clock_df.shape[0]), columns=[str(t) for t in time_list])

        # Iterate over each row
        for i in range(clock_df.shape[0]):
            # Iterate over each column
            for j in range(clock_df.shape[1]):
                # Get the value
                value = clock_df.iloc[i, j]
                # Check if the value is in any range
                for k, r in enumerate(clock_list):
                    if r[0] <= value < r[1]:
                        # If the value is in the current range, fill the corresponding value from hall_sensor into df_clock
                        df_clock[str(r[0])].iloc[i] = df_hall.iloc[i, j]
                        break

        print(df_clock)
        df_clock_tranpose = (df_clock).T

        # return Roll_hr_min, k, df_hall, df_clock_tranpose, oddo1_value, oddo2_value
        return df_clock_tranpose, df_clock

    # def handle_table_double_click_tab9(self, item):
    #     print("hi")
    #     # Get the row data including the unique ID
    #     row = item.row()
    #     unique_id = self.myTableWidget_tab9.item(row, 0).text()  # Assuming the ID is in the first column
    #
    #     # Query the database for the coordinates corresponding to the unique ID
    #     with connection.cursor() as cursor:
    #         query_for_coordinates = "SELECT start_index, end_index, start_sensor, end_sensor, length, Feature_identification FROM dent_update WHERE id = %s"
    #         cursor.execute(query_for_coordinates, (unique_id,))
    #         result = cursor.fetchone()  # Assuming the query returns only one row
    #         if result:
    #             start_index, end_index, y_start_hm, y_end_hm, length, Feature_identification = result
    #             print("Table Widget Query...", start_index, end_index, y_start_hm, y_end_hm)
    #             self.annotate_heatmap_tab9(start_index, end_index, y_start_hm, y_end_hm, length, Feature_identification)
    #         else:
    #             QMessageBox.warning(self, 'Warning', 'No Record Found')
    #
    # def annotate_heatmap_tab9(self, start_index, end_index, y_start_hm, y_end_hm, unique_id,Feature_identification):
    #     df_clock_index = self.df_clock_index.to_list()
    #     start_x_pos = start_index
    #     end_x_pos = end_index
    #     # start_x_pos = df_clock_index.index(start_index)
    #     # end_x_pos = df_clock_index.index(end_index)
    #     print("start_x_pos",start_x_pos, end_x_pos)
    #     # Draw a rectangle on the heatmap image using matplotlib patches
    #     rect_width = end_x_pos - start_x_pos
    #     rect_height = y_end_hm - y_start_hm
    #
    #     # Create annotation for the defect area
    #     self.fig.add_annotation(
    #         xref='x',
    #         yref='y',
    #         x=(start_x_pos + end_x_pos) / 2,  # Center position for the annotation
    #         y=y_start_hm,  # Position of the annotation
    #         text=Feature_identification,  # Text for the annotation
    #         showarrow=False,
    #         font=dict(
    #             color="black",
    #             size=12
    #         ),
    #     )
    #
    #     # Update layout to ensure annotations are displayed
    #     self.fig.update_layout(
    #         annotations=[],
    #         shapes=[
    #             dict(
    #                 type='rect',
    #                 xref='x',
    #                 yref='y',
    #                 x0=start_x_pos,
    #                 y0=y_start_hm,
    #                 x1=end_x_pos,
    #                 y1=y_end_hm,
    #                 line=dict(
    #                     color="black",
    #                     width=1
    #                 ),
    #                 fillcolor="rgba(255, 0, 0, 0.2)"  # Transparent red fill color
    #             )
    #         ]
    #     )
    #     print("hello clock")


    def line_select_callback_tab9(self, eclick, erelease):
        self.rect_start_tab9 = eclick.xdata, eclick.ydata
        self.rect_end_tab9 = erelease.xdata, erelease.ydata
        print("hi")
        # self.draw_rectangle_3()


    def reset_btn_fun_tab9(self):
        if self.figure_tab9.gca().patches:
            for patch in self.figure_tab9.gca().patches:
                patch.remove()
            for text in self.figure_tab9.gca().texts:
                text.remove()
            self.canvas_tab9.draw()
            self.rect_start__tab9 = None  # Store the starting point of the rectangle
            self.rect_end__tab9 = None


    """
    Selection of marking inside the weld selection(tab5)
    """

    def line_selection5(self, eclick, erelease):
        runid = self.runid
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        start_index = round(x1)
        end_index = round(x2)
        query_for_start = 'SELECT ODDO1,ODDO2 FROM ' + Config.table_name + ' WHERE index>{} AND index<{} AND runid={}'
        query_job = client.query(query_for_start.format(int(start_index), int(end_index), runid))
        results = query_job.result()
        oddo1 = []
        oddo2 = []
        for row in results:
            oddo1.append(row[0])
            oddo2.append(row[1])
        print(oddo1)
        print(oddo2)
        start_oddo1 = oddo1[0]
        end_oddo1 = oddo1[-1]
        start_oddo2 = oddo2[0]
        end_oddo2 = oddo2[-1]
        weld_length = end_oddo1 - start_oddo1 if end_oddo1 >= end_oddo2 else end_oddo2 - start_oddo2
        with connection.cursor() as cursor:
            # fetch_last_row = "select * from temp_welds where runid='%s' order by temp_weld_id DESC LIMIT 1"
            # # Execute query.
            # cursor.execute(fetch_last_row, (int(runid)))
            # allSQLRows = cursor.fetchall()
            # print(allSQLRows)
            type = 'manual'
            # weld_number = 1
            analytic_id = 1
            sensitivity = 1
            query_weld_insert = "INSERT INTO temp_welds (runid,analytic_id,sensitivity,start_index,end_index,type,start_oddo1,end_oddo1,start_oddo2,end_oddo2,length) VALUES('{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}')".format(
                runid, analytic_id, sensitivity, start_index, end_index, type, start_oddo1, end_oddo1,
                start_oddo2, end_oddo2, weld_length)

            # Execute query.
            b = cursor.execute(query_weld_insert)
            connection.commit()
            if b:
                QMessageBox.about(self, 'Insert', 'Data Inserted Successfully')
                self.hide()
            else:
                print("data is not inserted successfully")

    """
    End of weld selection and inserted data into database
    """

    """
    Plot Circle and calculate deformation in specific location in pipe 
    """

    def on_click(self):
        finial_defect_list = []
        for i in self.dent_list_d2:
            start_observation_x_value = i[0]
            end_observation_x1_value = i[2]
            start_observation_y_value = i[1]
            start_observation_y1_value = i[3]
            # print(start_observation_x_value, end_observation_x1_value,start_observation_y1_value,start_observation_y_value)
            query_for_start = 'SELECT index,ODDO1,ODDO2,[proximity1,proximity2,proximity3,proximity4,proximity5,proximity6,proximity7,proximity8,proximity9,proximity10,proximity11,proximity12,proximity13,proximity14,proximity15,proximity16,proximity17,proximity18,proximity19,proximity20,proximity21,proximity22,proximity23,proximity24] FROM ' + Config.table_name + ' WHERE index>{} AND index<{} order by index'
            query_job = client.query(query_for_start.format(start_observation_x_value, end_observation_x1_value))
            results = query_job.result()
            index_1 = []
            oddo_1 = []
            oddo_2 = []
            proximity = []
            for k in results:
                index_1.append(k[0])
                oddo_1.append(k[1])
                oddo_2.append(k[2])
                proximity.append(k[3])
            mean1 = proximity[0]

            ############################calculate dent length###############################
            oddo1_length = oddo_1[-1] - oddo_1[0]
            oddo2_length = oddo_2[-1] - oddo_2[0]

            ######################### end of length ##################################
            ################# calculate absolute distance ##################
            absolute_distance_oddo1 = oddo_1[0] + (oddo1_length / 2)
            absolute_distance_oddo2 = oddo_2[0] + (oddo2_length / 2)
            print("absolute_distance_oddo1", absolute_distance_oddo1)
            print("absolut_distance_oddo2", absolute_distance_oddo2)
            ################### end of absolute distance #############

            ##################### upstream calculation in dent #############
            up_oddo1 = absolute_distance_oddo1 - self.upstream_oddo1
            up_oddo2 = absolute_distance_oddo2 - self.upstream_oddo2
            print("Upstream_oddo1", up_oddo1)
            print("Upstream_oddo2", up_oddo2)
            ################## end of upstream #######################

            max_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ### Find the maximum value of each proximity sensor ########
            for l, data in enumerate(proximity):
                for m, data1 in enumerate(data):
                    if data1 > max_value[m]:
                        max_value[m] = data1

            min_value = []
            t = len(proximity[0])
            for i1 in range(t):
                e = []
                for k, data2 in enumerate(proximity):
                    e.append(data2[i1])
                min_value.append(min(e))

            print("mean1........", mean1)
            print("minimum", min_value)
            print("maximum", max_value)

            # dent_yes_or_not={}
            dent_metal_loss = {}
            for n, data3 in enumerate(max_value):
                b = data3 - mean1[n]
                if b >= 1000:
                    dent_metal_loss[n] = b
                else:
                    pass
            print("dent_metal_loss", dent_metal_loss)
            if len(dent_metal_loss) == 0:
                pass
            else:
                inverse_value = [(value, key) for key, value in dent_metal_loss.items()]
                print("inverse value", inverse_value)
                a = max(inverse_value)
                # max_value_difference = a[0]
                max_value_key = a[1]
                max_depth_value = max_value[max_value_key]
                print("max_value depth", max_depth_value)

            dent_metal_gain = {}
            for n1, data4 in enumerate(min_value):
                b1 = mean1[n1] - data4
                if b1 >= 1000:
                    dent_metal_gain[n1] = b1
            print("dent_metal_gain", dent_metal_gain)
            if len(dent_metal_gain) == 0:
                pass
            else:
                inverse_value1 = [(value1, key1) for key1, value1 in dent_metal_gain.items()]
                print("inverse value>>>>>>>>>>>", inverse_value1)
                a1 = max(inverse_value1)
                # max_value_difference = a1[0]
                min_value_key = a1[1]
                min_depth_value = min_value[min_value_key]
                mean_value_key = mean1[min_value_key]
                print("max_value depth>>>>>", min_depth_value)
                actual_depth_percentage = (mean_value_key - min_depth_value) / mean_value_key * 100
                print("% depth metal Gain", actual_depth_percentage)

            self.m_output = websearch()
            self.hbox_6tab6.addWidget(self.m_output)
            num_vars = 18
            centre = 0.5
            theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)
            x0, y0, r = [centre] * 3
            verts = [(r * np.cos(t) + x0, r * np.sin(t) + y0) for t in theta]
            x = [v[0] for v in verts]
            y = [v[1] for v in verts]
            difference_max = []
            difference_min = []
            for i1, data in enumerate(max_value):
                difference_max.append(max_value[i1] + ((data - mean1[i1]) * 100))
                difference_min.append(min_value[i1] - ((mean1[i1] - min_value[i1]) * 100))
            print("difference max", difference_max)
            print("difference min", difference_min)
            p = Figure(width=500, height=400)

            flist = [mean1, difference_min, difference_max]
            colors = ['blue', 'red', 'pink']
            for i in range(len(flist)):
                xt, yt = radar_patch(flist[i], theta, centre)

                p.patch(x=xt, y=yt, fill_alpha=0.15, line_color=colors[i])

            text = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P13', 'P14', 'P15',
                    'P16',
                    'P17', 'P18', '']
            source = ColumnDataSource({'x': xt, 'y': yt, 'text': text})
            # print("source",source)
            p.line(x="x", y="y", source=source)
            labels = LabelSet(x="x", y="y", text="text", source=source)
            p.add_layout(labels)
            layout = column(p)
            html = file_html(layout, CDN, "my plot")

            # html_file = self.bokeh_function1()
            self.m_output.setHtml(html)
            self.m_output.show()
            finial_defect_list.append({"angle": 0, "absolute_distance_oddo1": absolute_distance_oddo1,
                                       "absolute_distance_oddo2": absolute_distance_oddo2, "upstream_oddo1": up_oddo1,
                                       "upstream_oddo2": up_oddo2, "oddo1_length": oddo1_length,
                                       "oddo2_length": oddo2_length})
        print("final_defect_list", finial_defect_list)

    """
    Draw the rectangle selection of marking

    """

    def deformation_draw(self, dent_list1, ax8):
        for x in dent_list1:
            rect_obj = Rectangle((x[0], x[1]), x[2], x[3], fill=False, edgecolor='black')
            ax8.add_patch(rect_obj)
        self.button1_tab6.show()

    def deformation_selection(self, eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        self.dent_list_d1 = []
        self.dent_list_d2 = []
        self.dent_list_d2.append([x1, y2, x2, y1])
        self.dent_list_d1.append([x1, y1, x2 - x1, y2 - y1])
        # print("dent list1", self.dent_list_d1)
        # print("dent_list2", self.dent_list_d2)
        self.deformation_draw(self.dent_list_d1, self.ax8)

    """
    End the rectangle selection
    """

    """
    Six tab inside line chart with circular plot

    """

    def deformation_line(self):
        # self.m_output.hide()
        Config.print_with_time("Pre graph analysis called")
        runid = self.runid
        pipe_id = self.combo1.currentText()
        self.pipe_id = int(pipe_id)

        with connection.cursor() as cursor:
            query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
            cursor.execute(query)
            result = cursor.fetchone()
            # print(result)
            if not result:
                Config.print_with_time("No data found for this pipe ID : ")
            else:
                start_index, end_index = result[0], result[1]
                print("start index and end index", start_index, end_index)
                Config.print_with_time("Start fetching at : ")
                # query = query_generator.get_pipe(lower_sensitivity, upper_sensitivity, runid, start_index, end_index)
                # query_job = client.query(query)
                # results = query_job.result()

                to_execute = 'SELECT index,oddo1,oddo2,[proximity1, proximity2, proximity3, proximity4, proximity5, proximity6, proximity7, proximity8,proximity9, proximity10, proximity11, proximity12, proximity13, proximity14, proximity15,proximity16, proximity17, proximity18, proximity19, proximity20, proximity21, proximity22, proximity23, proximity24] FROM ' + Config.table_name + ' where index>{} and index<{} order by index'

                query_to_run = client.query(to_execute.format(start_index, end_index))
                results = query_to_run.result()
                # print(results)

                Config.print_with_time("End fetching  at:")
                data = []
                oddo1 = []
                oddo2 = []
                indexes = []
                index = []

                Config.print_with_time("Start of conversion at : ")
                for row in results:
                    data.append(row[3])
                    # data.append(row['frames'])
                    oddo1.append(row['oddo1'])
                    oddo2.append(row['oddo2'])
                    index.append(row['index'])
                    # indexes.append(ranges(index_of_occurrences(row['frames'], 1)))
                    indexes.append(ranges(index_of_occurrences(row[3], 1)))
                self.upstream_oddo1 = oddo1[0]
                self.upstream_oddo2 = oddo2[0]
                self.df_new_1 = pd.DataFrame(data,
                                             columns=['proximity1', 'proximity2', 'proximity3', 'proximity4',
                                                      'proximity5', 'proximity6', 'proximity7', 'proximity8',
                                                      'proximity9', 'proximity10', 'proximity11', 'proximity12',
                                                      'proximity13', 'proximity14', 'proximity15',
                                                      'proximity16', 'proximity17', 'proximity18', 'proximity19',
                                                      'proximity20', 'proximity21', 'proximity22', 'proximity23', 'proximity24'])
                # self.df_new = self.df_new.transpose()
                df_new = self.df_new_1
                df_mean = df_new.mean().tolist()
                ls = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1100000, 1200000,
                      1300000,
                      1400000, 1500000, 1600000, 1700000, 1800000]
                # df_new.to_csv('E:/Egp_desktop_web/Egp_Desktop/d.csv')
                df_new['new_index'] = np.arange(len(df_new))
                self.final_df_1 = df_new
                print(self.final_df_1)

                Config.print_with_time("Ending of conversion at : ")
                # print(df_new['new_index'])
                self.figure_tab6.clear()
                self.ax8 = self.figure_tab6.add_subplot(111)

                # discards the old graph
                self.ax8.clear()
                res = ['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5', 'proximity6', 'proximity7',
                       'proximity8',
                       'proximity9', 'proximity10', 'proximity11', 'proximity12', 'proximity13', 'proximity14',
                       'proximity15',
                       'proximity16', 'proximity17', 'proximity18', 'proximity19', 'proximity20',
                       'proximity21', 'proximity22', 'proximity23', 'proximity24']
                res1 = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7',
                        'P8', 'P9', 'P10', 'P11', 'P12', 'P13', 'P14',
                        'P15', 'P16', 'P17', 'P18','P19', 'P20', 'P21',
                        'P22', 'P23', 'P24']
                self.a1 = []
                for i, data in enumerate(res):
                    print(i, data)
                    df_y = (df_new[data] - df_mean[i]) + ls[i]
                    self.ax8.plot(index, df_y, label=res1[i])
                    self.a1.append(df_new[data])

                self.ax8.set_ylabel('Proximity Sensor')
                self.ax8.legend(loc='center left', bbox_to_anchor=(1, 0.4))
                self.canvas_tab6.draw()
                rs = RectangleSelector(self.ax8, self.deformation_selection,
                                       useblit=False)
                plt.connect('key_press_event', rs)

    """
    End of six tab all plot
    """

    """
    fifth tab inside weld selection
    """

    def Line_chart1(self):
        runid = self.runid
        start = int(self.start.text())
        end = int(self.end.text())
        print(start, end)
        query_for_start = 'SELECT * FROM ' + Config.table_name + ' WHERE index>{} AND index<{} order by index'
        query_job = client.query(query_for_start.format(start, end))
        df_plot_data = query_job.result().to_dataframe()
        df_x = df_plot_data[
            ['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5', 'proximity6', 'proximity7',
             'proximity8',
             'proximity9', 'proximity10', 'proximity11', 'proximity12', 'proximity13', 'proximity14', 'proximity15',
             'proximity16', 'proximity17', 'proximity18', 'proximity19', 'proximity20', 'proximity21', 'proximity22', 'proximity23', 'proximity24']]
        # df_plot_data.to_csv("C:/Users/Shradha Agarwal/Desktop/DataLog.csv")
        # print(df_plot_data)
        """
        Maximum and Minimum value of each proximity sensor
        """
        Maximum1 = df_x.max()
        k1 = list(Maximum1)
        # print("Maximum_value",k1)
        Minimum_value_each_proximity = df_x.min()
        k2 = list(Minimum_value_each_proximity)

        """
        Difference b/w maximum value and minimum value
        """
        t1 = []
        for j, data in enumerate(k1):
            t1.append(data - k2[j])

        res1 = ['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5',
                'proximity6', 'proximity7', 'proximity8', 'proximity9', 'proximity10',
                'proximity11', 'proximity12',
                'proximity13', 'proximity14', 'proximity15', 'proximity16',
                'proximity17',
                'proximity18', 'proximity19', 'proximity20', 'proximity21', 'proximity22', 'proximity23', 'proximity24']

        t2 = []
        # l = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000,
        #      17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000]
        l = 20
        for i, column in enumerate(res1):
            df_x[column] = ((((df_x[column] - k2[i]) / t1[i]) * 100) + (l * i))
            # yy = lfilter(b, a, df1_x)
            # t2.append(df1_x)
        """
        New DataFrame Created..............After Processing
        """

        # k3 = pd.DataFrame(t2).transpose()
        # print("DataFrame.....",k3)

        index = df_plot_data['index']

        self.figure_x5.clear()
        self.ax5 = self.figure_x5.add_subplot(111)

        # discards the old graph
        self.ax5.clear()
        # self.a1 = []
        for i in res1:
            self.ax5.plot(index.to_numpy(), df_x[i].to_numpy(), label=i)
            # self.a1.append(df_plot_data[i])
        self.ax5.set_ylabel('Proximity Sensor')
        self.canvas_x5.draw()
        rs1 = RectangleSelector(self.ax5, self.line_selection5, useblit=False)
        plt.connect('key_press_event', rs1)

    """
    End of the weld selection

    """
        # self.merge_pipe(self.runid)

    # dent_list=[]
    # def onpick(self,event):
    #     thisline = event.artist
    #     xdata = thisline.get_xdata()
    #     ydata = thisline.get_ydata()
    #     ind = event.ind
    #     points = tuple(zip(xdata[ind], ydata[ind]))
    #     print('onpick points:', points)

    # def line_select(self, event1, event2):
    #     x0, x1 = sorted([event1.xdata, event2.xdata])
    #     y0, y1 = sorted([event1.ydata, event2.ydata])
    #     #print(self.x)
    #     # start_index=x0
    #     # end_index=x1
    #
    #     #print("index start and end",start_index,end_index)
    #     query_for_start = 'SELECT index,[proximity1,proximity2,proximity3,proximity4,proximity5,proximity6,proximity7,proximity8,proximity9,proximity10,proximity11,proximity12,proximity13,proximity14,proximity15,proximity16,proximity17,proximity18, proximity19, proximity20, proximity21, proximity22, proximity23, proximity24] FROM ' + Config.table_name + ' WHERE index>{} AND index<{} order by index'
    #     query_job = client.query(query_for_start.format(x0, x1))
    #     results = query_job.result()
    #     #print(results)
    #     index1=[]
    #     proximity=[]
    #     for i in results:
    #         index1.append(i[0])
    #         proximity.append(i[1])
    #     #print(proximity)
    #     self.df = pd.DataFrame(proximity,
    #                                columns=['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5',
    #                                         'proximity6', 'proximity7', 'proximity8',
    #                                         'proximity9', 'proximity10', 'proximity11', 'proximity12', 'proximity13',
    #                                         'proximity14', 'proximity15',
    #                                         'proximity16', 'proximity17', 'proximity18'])
    #     # self.df_new = self.df_new.transpose()
    #     df = self.df
    #     print(df)
    #     b = []
    #     for i, data in enumerate(df):
    #         b.append(list(df[data]))
    #     d = []
    #     length = x1 - x0
    #     for i, data in enumerate(b):
    #         sum = 0
    #         for j, data1 in enumerate(data):
    #             #print(j,data1)
    #             sum = sum + data1
    #         d.append(sum / length)
    #     #print("hi")
    #     print(d)
    # for k,data in enumerate(proximity):
    #     print(data)
    # self.defect_list.append([x0, y0, x1, y1])
    # print(self.defect_list)

    # dent_list1 = []
    # dent_list2=[]
    # def line(self, eclick, erelease):
    #     x1, y1 = eclick.xdata, eclick.ydata
    #     x2, y2 = erelease.xdata, erelease.ydata
    #     self.dent_list2.append([x1, y2,  x2, y1])
    #     self.dent_list1.append([x1, y1,  x2 - x1, y2 - y1])
    #     #print(self.dent_list1)
    #     self.draw_rectangle(self.dent_list1, self.ax)

    # self.generate_graph()
    # print(self.dent_list1)
    # print(self.dent_list1)
    # ax.add_patch(self.dent_list1)
    # print(self.dent_list)
    # self.generate_graph()

    # def add_dent1(self):
    #     print(self.runid)
    #     print(self.pipe_id)
    #     dent_type = self.dent_list_combo_box.currentText()
    #     print(self.dent_list2)
    #     print("dent_type",dent_type)
    #     finial_dent_list = []
    #     for i in self.dent_list2:
    #         start_observation_x_value = i[0]
    #         end_observation_x1_value = i[2]
    #         start_observation_y_value=i[1]
    #         start_observation_y1_value=i[3]
    #
    #         print(start_observation_x_value, end_observation_x1_value,start_observation_y1_value,start_observation_y_value)
    #         query_for_start = 'SELECT index,ODDO1,ODDO2,[proximity1,proximity2,proximity3,proximity4,proximity5,proximity6,proximity7,proximity8,proximity9,proximity10,proximity11,proximity12,proximity13,proximity14,proximity15,proximity16,proximity17,proximity18, proximity19, proximity20, proximity21, proximity22, proximity23, proximity24] FROM ' + Config.table_name + ' WHERE index>{} AND index<{} order by index'
    #         query_job = client.query(query_for_start.format(start_observation_x_value, end_observation_x1_value))
    #         results = query_job.result()
    #         index1 = []
    #         oddo1=[]
    #         oddo2=[]
    #         proximity = []
    #         for k in results:
    #             index1.append(k[0])
    #             oddo1.append(k[1])
    #             oddo2.append(k[2])
    #             proximity.append(k[3])
    #         ####################### 10 inch Egp #############
    #
    #         ############################ calculate the length of the dent ##############
    #         # print(index1)
    #         # print(oddo1)
    #         oddo1_index = {}
    #         for p, data5 in enumerate(index1):
    #             if data5 == int(start_observation_x_value)+1:
    #                 oddo1_index['start_observation_index'] = p
    #             elif data5 == int(end_observation_x1_value)-1:
    #                 oddo1_index['end_observation_index'] = p
    #             else:
    #                 pass
    #         print(oddo1_index)
    #         oddo1_value_dent_start = oddo1[oddo1_index['start_observation_index']]
    #         oddo1_value_dent_end = oddo1[oddo1_index['end_observation_index']]
    #         dent_length=oddo1_value_dent_end-oddo1_value_dent_start
    #         print("dent_length",dent_length)
    #         ################################ end of the dent length caculation ###############
    #
    #         ################################ calculate the absolute distance ##########
    #         absolute_length = oddo1_value_dent_start + dent_length / 2
    #         print("absolute_length",absolute_length)
    #         ################################ end of the absolute distance #############
    #
    #         ########################## caculate the depth of the dent ##############
    #         maximum = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #         ### Find the maximum value of each proximity sensor ########
    #         for l, data in enumerate(proximity):
    #             for m, data1 in enumerate(data):
    #                 if data1 > maximum[m]:
    #                     maximum[m] = data1
    #
    #
    #         ######### Maximum value of each proximity sesore list #####
    #         print("max value each proximity",maximum)
    #         ############ get rows of start_observation at the 0Th position of element in proximity 2d list ###
    #         initial_observation=proximity[0]
    #         print("initial_observation of each proximity",initial_observation)
    #
    #         zip_object = zip(maximum, initial_observation)
    #         for list1_i, list2_i in zip_object:
    #             difference=(list1_i - list2_i)
    #             print("difference_of_two _list",difference)
    #
    #
    #         dent_yes_or_not={}
    #         dent_yes={}
    #         for n, data3 in enumerate(maximum):
    #                 #print(n, data3)
    #                 b=data3-initial_observation[n]
    #                 if b<=20000:
    #                     pass
    #                 elif 20001<b<35000:
    #                     dent_yes_or_not[n]=b
    #                 elif b>=35000:
    #                     dent_yes[n]=b
    #         print("dent_yes_or_not",dent_yes_or_not)
    #         print("dent_yes",dent_yes)
    #         if dent_yes:
    #             inverse_value = [(value, key) for key, value in dent_yes.items()]
    #             print("inverse value",inverse_value)
    #             a = max(inverse_value)
    #             max_value_difference=a[0]
    #             max_value_key=a[1]
    #             print("max_value_difference",max_value_difference)
    #             print("max_value_key",max_value_key)
    #
    #             max_depth_value=maximum[max_value_key]
    #             print("max_value depth",max_depth_value)
    #
    #
    #             ################################# start the breadth calculation ###########
    #             c=breadth(dent_yes)
    #             for x,data6 in enumerate(c):
    #                 start_sensor,end_sensor=data6['start'],data6['end']
    #                 print(start_sensor,end_sensor)
    #                 outer_diameter = 273
    #                 thickness = 6.35  ################# each pipe thickness can be change ############
    #                 inner_diameter = outer_diameter - 2 * (thickness)
    #                 radius = inner_diameter / 2
    #                 print("radius", radius)
    #
    #                 theta = 20  ####sensor to sensor b/w adjacent sensor
    #                 sensor_no = end_sensor - start_sensor
    #                 total_angle_sensor_to_sensor = (theta * sensor_no) + int(10)
    #                 print("total_angle_start_to_end", total_angle_sensor_to_sensor)
    #                 ######## angle convert to radian #######
    #                 b = math.radians(total_angle_sensor_to_sensor)
    #                 print("b calculated in radian", b)
    #                 arc_calculation_in_breadth = radius * b
    #                 print(arc_calculation_in_breadth)
    #
    #
    #             ################################# end of the breadth calculation #########
    #
    #             finial_dent_list.append(
    #                 {"angle": 0, "depth": max_depth_value, "length": dent_length, "breadth": arc_calculation_in_breadth,
    #                  "absolute_distance": absolute_length, "sensor_no": 0})
    #         else:
    #             print("no found dent")
    #
    #
    #
    #     print(finial_dent_list)

    # self.dent_list2=[]
    # def draw_rectangle(self,dent_list1,ax):
    #     for x in dent_list1:
    #         rect_obj = Rectangle((x[0], x[1]), x[2], x[3], fill=False, edgecolor='red')
    #         ax.add_patch(rect_obj)
    #     self.dent_list1=[]
    #     self.dent_list_combo_box.show()
    #     self.dent_list_combo_box.activated.connect(self.add_dent1)

    def plot_heatmap_visual(self):
        Config.print_with_time("Pre graph analysis called")
        runid = self.runid
        pipe_id = self.combo_box.currentText()
        self.pipe_id = int(pipe_id)
        with connection.cursor() as cursor:
            query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
            cursor.execute(query)
            result = cursor.fetchone()
            print(result)
            if result:
                start_index, end_index = result[0], result[1]
                print("start index and end index", start_index, end_index)
                path = Config.weld_pipe_pkl + self.project_name + '/' + str(pipe_id) + '.pkl'
                if os.path.isfile(path):
                    Config.print_with_time("File exist")
                    df_pipe = pd.read_pickle(path)
                    print("........", df_pipe)
                    self.index_tab3 = df_pipe['index']
                    self.oddo1_heatmap1_mm = df_pipe['ODDO2'] - Config.oddo1
                    self.oddo1_heatmap_m = ((df_pipe['ODDO2'] - Config.oddo1) / 1000).round(3)

                    self.figure1.clear()
                    self.ax1 = self.figure1.add_subplot(111)
                    self.ax1.figure.subplots_adjust(bottom=0.085, left=0.055, top=0.930, right=0.920)
                    self.ax1.clear()

                    res = ['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5', 'proximity6',
                           'proximity7',
                           'proximity8',
                           'proximity9', 'proximity10', 'proximity11', 'proximity12', 'proximity13', 'proximity14',
                           'proximity15',
                           'proximity16', 'proximity17', 'proximity18', 'proximity19', 'proximity20', 'proximity21', 'proximity22', 'proximity23', 'proximity24']

                    sensor_column = pd.DataFrame(df_pipe,
                                                 columns=['proximity1', 'proximity2', 'proximity3', 'proximity4',
                                                          'proximity5', 'proximity6',
                                                          'proximity7',
                                                          'proximity8',
                                                          'proximity9', 'proximity10', 'proximity11', 'proximity12',
                                                          'proximity13', 'proximity14',
                                                          'proximity15',
                                                          'proximity16', 'proximity17', 'proximity18', 'proximity19', 'proximity20',
                                                          'proximity21', 'proximity22', 'proximity23', 'proximity24'])

                    sensor_column_fill = sensor_column.ffill(axis=0)

                    scaler = MinMaxScaler()
                    scaled_values = scaler.fit_transform(df_pipe[res])
                    gap_size = 0
                    for i, col in enumerate(res):
                        df_pipe[col] = scaled_values[:, i] + i * gap_size

                    # print("DataFrame......",df1)
                    n = 30  # the larger n is, the smoother curve will be
                    b = [1.0 / n] * n
                    a = 1
                    ls = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0]

                    for j1, column2 in enumerate(res):
                        df_pipe[column2] = df_pipe[column2] + ls[j1]

                    df1 = df_pipe[['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5', 'proximity6',
                                   'proximity7',
                                   'proximity8',
                                   'proximity9', 'proximity10', 'proximity11', 'proximity12', 'proximity13',
                                   'proximity14',
                                   'proximity15',
                                   'proximity16', 'proximity17', 'proximity18', 'proximity19', 'proximity20', 'proximity21',
                                   'proximity22', 'proximity23', 'proximity24']]

                    # df1.to_csv("D:/VDT/EGP_8inch/test.csv")

                    Mean1 = df1.mean()
                    Mean1.tolist()
                    # print(Mean1)
                    df3 = ((df1 - Mean1) / Mean1) * 100
                    # print(df3)
                    d1 = (df3.set_index(self.index_tab3).T).astype(float)

                    # color_ranges = [
                    #     (-100, -90), (-90, -80), (-80, -70), (-70, -60), (-60, -50), (-50, -40), (-40, -30), (-30, -20),
                    #     (-20, -10), (-10, 0),
                    #     (0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 90),
                    #     (90, 100)]

                    # color_values = ['#3d045a', '#4f355c', '#CD1076', '#8E236B', '#0530ad', '#6205db', '#8f39ff',
                    #                 '#016fff', '#74b0ff', '#82ffff',
                    #                 '#82ffff', '#00CD00', '#008000', '#fd8f00', '#D98719', '#CD661D', '#EE4000',
                    #                 '#FF0000', '#820202', '#000000']

                    color_ranges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9),
                                    (9, 10)]

                    color_values = ['#82ffff', '#00CD00', '#008000', '#fd8f00', '#D98719', '#CD661D', '#EE4000',
                                    '#FF0000', '#820202', '#000000']

                    custom_palette = sns.color_palette(color_values)

                    bounds = [r[0] for r in color_ranges] + [color_ranges[-1][1]]

                    cmap = ListedColormap(color_values)

                    norm = BoundaryNorm(bounds, cmap.N)

                    # heat_map_obj = sns.heatmap(d1, cmap=cmap, ax=self.ax1, norm=norm)

                    heat_map_obj = sns.heatmap(d1, cmap=cmap, ax=self.ax1, norm=norm)

                    heat_map_obj.set(xlabel="Number of Observation", ylabel="Sensors")
                    self.ax1.set_xticklabels(self.ax1.get_xticklabels(), size=9)
                    self.ax1.set_yticklabels(self.ax1.get_yticklabels(), size=9)

                    oddo1_li = list(self.oddo1_heatmap_m)
                    ax2 = self.ax1.twiny()
                    num_ticks1 = len(self.ax1.get_xticks())  # Adjust the number of ticks based on your preference
                    tick_positions1 = [int(i) for i in np.linspace(0, len(oddo1_li) - 1, num_ticks1)]
                    ax2.set_xticks(tick_positions1)
                    ax2.set_xticklabels([f'{oddo1_li[i]:.3f}' for i in tick_positions1], rotation=90)
                    ax2.set_xlabel("Absolute Distance (m)")

                    # def on_hover(event):
                    #     if event.xdata is not None and event.ydata is not None:
                    #         x = int(event.xdata)
                    #         y = int(event.ydata)
                    #         self.index_hm_set = self.index_tab3.to_list()
                    #         index_value = self.index_hm_set[x]
                    #         value = df_pipe.iloc[y, x]
                    #         z = oddo1_li[x]
                    #         self.toolbar_20.set_message(
                    #             f'Counter={index_value:.0f},Abs.distance(m)={z},Sensor_no={y:.0f},Value={value:.3f}')
                    #
                    # self.figure1.canvas.mpl_connect('motion_notify_event', on_hover)

                    def on_hover(event):
                        if event.inaxes:
                            x, y = event.xdata, event.ydata
                            if x is not None:
                                x = int(event.xdata)
                                y = int(event.ydata)
                                z = (df_pipe.loc[df_pipe.index == x, 'ODDO2']) - Config.oddo2
                                Abs_distance = int(z.values[0])
                                index_value = df_pipe.loc[df_pipe.index == x, 'index']
                                index_value_1 = int(index_value.values[0])
                                print("index_value", index_value_1)
                                print("Abs.distance", Abs_distance)
                                self.toolbar_x.set_message(
                                    f"Index_Value={index_value_1}, Abs.Distance(mm)={Abs_distance},\nSensor_offset_Values={y}")
                            else:
                                self.toolbar_x.set_message(f" ")

                    self.canvas_x.mpl_connect('motion_notify_event', on_hover)
                    plt.tight_layout()
                    self.canvas1.draw()

            else:
                Config.print_with_time("No data found for this pipe ID : ")

    def plot_heatmap_auto(self):
        Config.print_with_time("Pre graph analysis called")
        runid = self.runid
        pipe_id = self.combo_box.currentText()
        self.pipe_id = int(pipe_id)
        lower_sensitivity = self.lower_Sensitivity_combo_box.text()
        upper_sensitivity = self.upper_Sensitivity_combo_box.text()
        # print(type(lower_sensitivity),type(upper_sensitivity))
        with connection.cursor() as cursor:
            query = "SELECT start_index,end_index,length FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
            cursor.execute(query)
            result = cursor.fetchone()
            print(result)
            if not result:
                Config.print_with_time("No data found for this pipe ID : ")

            else:
                start_index, end_index, Pipe_length = result[0], result[1], result[2]
                print("start index and end index", start_index, end_index)
                Config.print_with_time("Start fetching at : ")
                query = query_generator.get_pipe(lower_sensitivity, upper_sensitivity, runid, start_index, end_index,
                                                 self.pipe_id)
                query_job = client.query(query)
                results = query_job.result()


                data = []
                oddo_1 = []
                oddo_2 = []
                indexes = []
                roll1=[]
                index = []
                Config.print_with_time("Start of conversion at : ")
                for row in results:
                    data.append(row['frames'])
                    # data.append(row['frames'])
                    oddo_1.append(row['oddo1'])
                    oddo_2.append(row['oddo2'])
                    index.append(row['index'])
                    roll1.append(row['ROLL'])
                    indexes.append(ranges(index_of_occurrences(row['frames'], 1)))
                    #indexes.append(ranges(index_of_occurrences(row[3], 1)))
                oddo1 = []
                oddo2 = []
                roll = []

                """
                Reference value will be consider 
                """
                for odometer1 in oddo_1:
                    od1 = odometer1 - Config.oddo1  ###16984.2 change According to run
                    oddo1.append(od1)
                for odometer2 in oddo_2:
                    od2 = odometer2 - Config.oddo2  ###17690.36 change According to run
                    oddo2.append(od2)

                """
                Reference value will be consider
                """
                for roll2 in roll1:
                    roll3 = roll2 - Config.roll_value
                    roll.append(roll3)
                self.df_new = pd.DataFrame(data,
                                           columns=['proximity1', 'proximity2', 'proximity3', 'proximity4',
                                                    'proximity5', 'proximity6', 'proximity7', 'proximity8',
                                                    'proximity9', 'proximity10', 'proximity11', 'proximity12',
                                                    'proximity13', 'proximity14', 'proximity15',
                                                    'proximity16', 'proximity17', 'proximity18', 'proximity19',
                                                    'proximity20', 'proximity21', 'proximity22', 'proximity23', 'proximity24'])

                self.index_hm_auto = pd.Series(index)
                self.df_new = self.df_new.set_index(self.index_hm_auto).T

                # self.df_new = self.df_new.transpose()
                self.df_new[self.df_new<0]=0

                # self.df_new.to_csv("C:/Users/Shradha Agarwal/Desktop/8.csv")


                print("dataframe---percentage", self.df_new)

                query_for_start = 'SELECT proximity1, proximity2, proximity3, proximity4, proximity5, proximity6, proximity7, proximity8,proximity9, proximity10, proximity11, proximity12, proximity13, proximity14, proximity15,proximity16, proximity17, proximity18, proximity19, proximity20, proximity21, proximity22, proximity23, proximity24 FROM ' + Config.table_name + ' WHERE index>{} AND index<{} order by index'
                query_job = client.query(query_for_start.format(start_index, end_index))
                df = query_job.result().to_dataframe()

                print("dataframe--actual_value",df)
                # df.to_csv("C:/Users/Shradha Agarwal/Desktop/test.csv")


                raw_defects = extract_raw_defects(indexes)
                defects = []
                for row in raw_defects:
                    defects = defects + calculate_defect(row, data)
                finial_defects = defect_length_calculator(data, defects, oddo1, oddo2, roll, df, Pipe_length)
                print("final defect list", finial_defects)
                insert_defect_into_db(finial_defects, runid, pipe_id)
                Config.print_with_time("End of defect calculation at : ")
        self.defect_list = get_defect_list_from_db(runid, pipe_id)

        self.figure1.clear()
        self.ax1 = self.figure1.add_subplot(111)

        # color_ranges = [(0, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.4), (0.4, 0.5),
        #                 (0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1)]

        color_ranges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9),
                                    (9, 10)]

        color_values = ['#82ffff', '#00CD00', '#008000', '#fd8f00', '#D98719',
                        '#CD661D', '#EE4000', '#FF0000', '#820202', '#000000']

        # custom_palette = sns.color_palette(color_values)


        bounds = [r[0] for r in color_ranges] + [color_ranges[-1][1]]

        cmap = ListedColormap(color_values)

        norm = BoundaryNorm(bounds, cmap.N)

        heat_map_obj = sns.heatmap(self.df_new, cmap=cmap, ax=self.ax1, norm=norm)

        # heat_map_obj = sns.heatmap(self.df_new, cmap='jet', ax=self.ax1, vmin=-10, vmax=10)

        heat_map_obj.set(xlabel="Number of Observation", ylabel="Sensors")
        self.canvas1.draw()

        def on_hover(event):
            if event.xdata is not None and event.ydata is not None:
                x = int(event.xdata)
                y = int(event.ydata)
                self.index_hm = index
                index_value = self.index_hm[x]
                value = self.df_new.iloc[y, x]
                z = oddo2[x]
                self.toolbar1.set_message(
                    # f'Counter={index_value:.0f},Abs.distance(m)={z},Sensor_no={y:.0f},Value={value:.3f}')
                    f'Counter={index_value:.0f},Abs.distance(m)={z},Sensor_no={y:.0f}')

        self.figure1.canvas.mpl_connect('motion_notify_event', on_hover)

        with connection.cursor() as cursor:
            Fetch_weld_detail = "select id,pipe_id,absolute_distance,upstream,pipe_length,feature_type,feature_identification,orientation,length,width,depth_diff from dent where runid='%s' and pipe_id='%s'"
            # Execute query.
            cursor.execute(Fetch_weld_detail, (int(self.runid), int(self.pipe_id)))
            self.myTableWidget_hm.setRowCount(0)
            allSQLRows = cursor.fetchall()
            if allSQLRows:
                for row_number, row_data in enumerate(allSQLRows):
                    self.myTableWidget_hm.insertRow(row_number)
                    for column_num, data in enumerate(row_data):
                        self.myTableWidget_hm.setItem(row_number, column_num, QtWidgets.QTableWidgetItem(str(data)))
                self.myTableWidget_hm.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.myTableWidget_hm.doubleClicked.connect(self.handle_table_double_click_hm)
            else:
                # self.myTableWidget5.doubleClicked.disconnect(self.handle_table_double_click)
                Config.warning_msg("No record found", "")

    def handle_table_double_click_hm(self, item):
        # Get the row data including the unique ID
        row = item.row()
        unique_id = self.myTableWidget_hm.item(row, 0).text()  # Assuming the ID is in the first column

        # Query the database for the coordinates corresponding to the unique ID
        with Config.connection.cursor() as cursor:
            query_for_coordinates = "SELECT start_index, end_index, start_sensor, end_sensor, length,Feature_identification FROM dent WHERE id = %s"
            b = cursor.execute(query_for_coordinates, (unique_id))
            result = cursor.fetchone()  # Assuming the query returns only one row
            if result:
                start_index, end_index, y_start_hm, y_end_hm, length,Feature_identification = result
                print("Table Widget Query...", start_index, end_index, y_start_hm, y_end_hm)
                self.annotate_heatmap_hm(start_index, end_index, y_start_hm, y_end_hm, unique_id,Feature_identification)
            else:
                QMessageBox.warning(self, 'Warning', 'No Record Found')

    def annotate_heatmap_hm(self, start_index, end_index, y_start_hm, y_end_hm, unique_id,Feature_identification):
        # start_x_pos = self.index_hm_auto.index(start_index)
        # end_x_pos = self.index_hm_auto.index(end_index)

        start_x_pos = start_index
        end_x_pos = end_index

        # Draw a rectangle on the heatmap image using matplotlib patches
        rect_width = end_x_pos - start_x_pos
        rect_height = y_end_hm - y_start_hm

        # Add unique ID annotation
        text_x_pos = (start_x_pos + end_x_pos) / 2  # Calculate the center position for the text
        text_y_pos = y_start_hm - 0.3 * rect_height  # Position the text slightly above the rectangle
        self.figure1.gca().text(text_x_pos, text_y_pos, Feature_identification+'-'+unique_id, ha='center', va='bottom')

        # Create a Rectangle patch
        rect = Rectangle((start_x_pos, y_start_hm), rect_width, rect_height, edgecolor='black', linewidth=1, fill=False)
        self.figure1.gca().add_patch(rect)
        self.canvas1.draw()  # Redraw the canvas to display the rectangle

    def reset_auto_hm(self):
        if self.figure1.gca().patches:
            for patch in self.figure1.gca().patches:
                patch.remove()
            for text in self.figure1.gca().texts:
                text.remove()
            self.canvas1.draw()


        # def on_hover(event):
        #     if event.xdata is not None and event.ydata is not None:
        #         x = int(event.xdata)
        #         y = int(event.ydata)
        #         self.index_hm_set = index_tab8.to_list()
        #         index_value = self.index_hm_set[x]
        #         value = d1.iloc[y, x]
        #         z = oddo1_li[x]
        #         self.toolbar1.set_message(
        #             f'Counter={index_value:.0f},Abs.distance(m)={z},Sensor_no={y:.0f},Value={value:.3f}')
        #
        # self.figure1.canvas.mpl_connect('motion_notify_event', on_hover)

        # self.figure1.clear()
        # ax1 = self.figure1.add_subplot(111)
        # ax1.clear()
        # ax1.plot(index,oddo1)
        # ax1.set_ylabel('Odometer')
        # self.canvas1.draw()

    # def line_selection(self, eclick, erelease):
    #
    #     x1, y1 = eclick.xdata, eclick.ydata
    #     x2, y2 = erelease.xdata, erelease.ydata
    #     self.dent_list1 = []
    #     self.dent_list2 = []
    #     self.dent_list2.append([x1, y2, x2, y1])
    #     self.dent_list1.append([x1, y1, x2 - x1, y2 - y1])
    #     print("dent list1", self.dent_list1)
    #     print("dent_list2",self.dent_list2)
    #     self.draw_rectangle(self.dent_list1, self.ax)

    # def draw_rectangle(self,dent_list1,ax):
    #     for x in dent_list1:
    #         rect_obj = Rectangle((x[0], x[1]), x[2], x[3], fill=False, edgecolor='black')
    #         ax.add_patch(rect_obj)
    #     self.latitude.show()
    #     self.logitude.show()
    #     self.selection_mark_lat_long.show()
    #     self.selection_mark_base_value.show()
    #     self.selection_mark_lat_long.toggled.connect(self.submit)
    #     self.selection_mark_base_value.toggled.connect(self.basevalue)

    def reset_btn_fun(self):
        if self.figure_x.gca().patches:
            for patch in self.figure_x.gca().patches:
                patch.remove()
            for text in self.figure_x.gca().texts:
                text.remove()
            self.canvas_x.draw()
            self.rect_start_1 = None  # Store the starting point of the rectangle
            self.rect_end_1 = None

    def rect_selection_line_chart(self, eclick, erelease):
        if abs(eclick.x - erelease.x) >= 3 and abs(eclick.y - erelease.y) >= 3:
            self.rect_start_1 = eclick.xdata, eclick.ydata
            self.rect_end_1 = erelease.xdata, erelease.ydata

            if self.rect_start_1 is not None and self.rect_end_1 is not None:
                for patch in self.figure_x.gca().patches:
                    patch.remove()

                rect = plt.Rectangle(
                    (min(self.rect_start_1[0], self.rect_end_1[0]),
                     min(self.rect_start_1[1], self.rect_end_1[1])),
                    abs(self.rect_end_1[0] - self.rect_start_1[0]),
                    abs(self.rect_end_1[1] - self.rect_start_1[1]),
                    edgecolor='black',
                    linewidth=1,
                    fill=False
                )
                self.figure_x.gca().add_patch(rect)
                self.canvas_x.draw()

    def mark_mdefect(self):
        if self.rect_start_1 is not None and self.rect_end_1 is not None:
            x1, y1 = min(self.rect_start_1[0], self.rect_end_1[0]), \
                     min(self.rect_start_1[1], self.rect_end_1[1])
            x2, y2 = x1 + abs(self.rect_end_1[0] - self.rect_start_1[0]), \
                     y1 + abs(self.rect_end_1[1] - self.rect_start_1[1])
            # print(x1, y1, x2, y2)
            print("hello")
            while True:
                name, ok = QInputDialog.getText(self, 'Enter Name', 'Enter the name of the drawn box:')
                if ok:
                    if name.strip():  # Check if the entered name is not empty or just whitespace
                        x_start, y_start = self.rect_start_1
                        x_end, y_end = self.rect_end_1
                        runid = self.runid
                        pipe = self.pipe_id
                        index_chart = self.index_lc
                        start_index15 = index_chart[round(x_start)]
                        end_index15 = index_chart[round(x_end)]
                        y_start15 = round(y_start)
                        y_end15 = round(y_end)
                        print(start_index15, end_index15)
                        print("start_sensor", y_start15)
                        print("end_sensor", y_end15)

                        query_for_start = 'SELECT [proximity1 ,proximity2 ,proximity3 ,proximity4 ,proximity5 ,proximity6 ,proximity7 ,proximity8 ,proximity9 ,proximity10 ,proximity11 ,proximity12 ,proximity13 ,proximity14 ,proximity15 ,' \
                                'proximity16 ,proximity17 ,proximity18, proximity19, proximity20, proximity21, proximity22, proximity23, proximity24] as frames FROM ' + Config.table_name + ' WHERE index>{} AND index<{} order by index'
                        query_job = client.query(query_for_start.format(self.start_index_lc, self.end_index_lc))
                        results = query_job.result()
                        df_actual = query_job.result().to_dataframe()
                        # print("dataframe--actual_value",df_actual)
                        data_actual = []
                        Config.print_with_time("Start of conversion at : ")
                        for row in results:
                            data_actual.append(row['frames'])


                        finial_defect_list = []

                        Config.print_with_time("Start fetching at : ")
                        query_for_start = 'SELECT index,ODDO1,ODDO2,[proximity1,proximity2,proximity3,proximity4,proximity5,' \
                                          'proximity6,proximity7,proximity8,proximity9,proximity10,proximity11,proximity12,' \
                                          'proximity13,proximity14,proximity15,proximity16,proximity17,proximity18, proximity19, proximity20, proximity21, proximity22, proximity23, proximity24],ROLL FROM ' + Config.table_name + ' WHERE index>={} AND  index<={} order by index'
                        query_job = client.query(query_for_start.format(start_index15, end_index15))

                        results = query_job.result()

                        df = query_job.result().to_dataframe()

                        """
                        End fetching data from Google Bigquery
                        """
                        index1 = []
                        oddo_1 = []
                        oddo_2 = []
                        proxi_sensor = []
                        roll = []
                        indexes = []
                        for row in results:
                            index1.append(row[0])
                            oddo_1.append(row[1])
                            oddo_2.append(row[2])
                            proxi_sensor.append(row[3])
                            roll.append(row['ROLL'])
                            # indexes.append(ranges(index_of_occurrences(row['frames'], 1)))
                            # indexes.append(ranges(index_of_occurrences(row[3], 1)))

                        # print("holl sensor....", holl_sensor)

                        oddo1 = []
                        oddo2 = []
                        roll4 = []
                        for odometer1 in oddo_1:
                            od1 = odometer1 - Config.oddo1  ### change According to run
                            oddo1.append(od1)
                        for odometer2 in oddo_2:
                            od2 = odometer2 - Config.oddo2  ### change According to run
                            oddo2.append(od2)
                        """
                        Reference value will be consider
                        """
                        for roll2 in roll:
                            roll3 = roll2 - Config.roll_value
                            roll4.append(roll3)

                        # print("oddo1", oddo1)
                        # print("oddo2", oddo2)
                        # print("roll", roll)
                        # print("proxy...", proxi_sensor)

                        # df_pipe = proxi_sensor.to_dataframe()
                        # print(df_pipe)

                        """
                        Calculate Upstream Distance oddo1 and oddo2
                        """
                        upstream_oddo1 = oddo1[0] - self.oddo1[0]
                        upstream_oddo2 = oddo2[0] - self.oddo1[0]
                        print("upstream_oddo1=>", upstream_oddo1)
                        print("upstream_oddo2=>", upstream_oddo2)

                        """
                        Calculate length of the defect
                        """
                        length_of_defect_oddo1 = round(oddo1[-1] - oddo1[0])
                        length_of_defect_oddo2 = round(oddo2[-1] - oddo2[0])
                        print("length_of_defect_oddo1=>", length_of_defect_oddo1)
                        print("length_of_defect_oddo2=>", length_of_defect_oddo2)

                        """
                        Calculate Abs.Distance of the defect
                        """
                        Abs_Distance_oddo1 = oddo1[0]
                        print("Abs.distance_oddo1=>", Abs_Distance_oddo1)

                        Abs_Distance_oddo2 = oddo2[0]
                        print("Abs.distance_oddo1=>", Abs_Distance_oddo2)

                        """
                        Calculate Width of the Defect
                        """
                        Width = Width_calculation(y_start15, y_end15)
                        Width = round(Width)
                        print("Width of Defect=>", Width)

                        # each_proxy_sensor_max_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                        # for l, data in enumerate(proxi_sensor):
                        #     for m, data1 in enumerate(data):
                        #         if m >= y_start15 - 1 and m < y_end15:
                        #             if data1 > each_proxy_sensor_max_value[m]:
                        #                 each_proxy_sensor_max_value[m] = data1

                        """
                        Get rows of start_observation at the 0th Position of element in holl sensor 2d list
                        """
                        initial_observation = proxi_sensor[0]
                        # print("initial_observation", initial_observation)
                        # print("max_value_get",proxi_sensor)
                        dent_dataframe=pd.DataFrame(proxi_sensor, columns=['proximity1','proximity2','proximity3','proximity4','proximity5','proximity6','proximity7','proximity8','proximity9','proximity10','proximity11','proximity12','proximity13','proximity14','proximity15','proximity16','proximity17','proximity18', 'proximity19', 'proximity20', 'proximity21', 'proximity22', 'proximity23', 'proximity24'])
                        k=dent_dataframe.max()
                        each_proxy_sensor_max_value=k.to_list()
                        # print("maximum_value_list",each_proxy_sensor_max_value)


                        """
                        Difference between max_value_list and initial_observation
                        """
                        zip_object = zip(each_proxy_sensor_max_value, initial_observation)
                        difference_list = []
                        for list1_i, list2_i in zip_object:
                            difference_list.append(list1_i - list2_i)
                        print("difference list",difference_list)
                        """
                        Get max_value_difference_value
                        """
                        max_value_difference_value = max(difference_list)

                        """
                        Get index max_value_difference_value
                        """
                        max_value_difference_index = difference_list.index(max_value_difference_value)
                        print("sensor_no", max_value_difference_index)


                        """
                        Check max_value_list inside the index and get max_value
                        """
                        #max_value = each_proxy_sensor_max_value[max_value_difference_index]
                        #print("max_value", max_value)

                        """
                        Check initial_observation inside the index and get base value
                        """
                        #base_value=initial_observation[max_value_difference_index]
                        #print("base_value",base_value)

                        #depth=(max_value-base_value)
                        # depth=round(depth)
                        #print("depth...",depth)
                        depth=max_value_difference_value

                        """
                        .................Orientation Calculation..........................
                        """
                        angle = defect_angle_x(roll4, max_value_difference_index)
                        print("angle", angle)

                        # angle = '0:04'
                        type = 'External'

                        finial_defect_list.append({"start_index": start_index15, "end_index": end_index15,
                                                   "start_sensor": y_start15, "end_sensor": y_end15,
                                                   "sensor_no":max_value_difference_index,
                                                   "Absolute_distance": int(Abs_Distance_oddo2),
                                                   "Upstream": int(upstream_oddo2),
                                                   "Pipe_length": self.weld_pipe_length_oddo2_lc,
                                                   "Feature_type": type, "Feature_identification": name,
                                                   "Orientation": angle, "WT": None,
                                                   "length": int(length_of_defect_oddo2), "Width": Width,
                                                   "Depth_percentage": depth})

                        print(finial_defect_list)

                        for i in finial_defect_list:
                            start_index = i['start_index']
                            end_index = i['end_index']
                            start_sensor = i['start_sensor']
                            end_sensor = i['end_sensor']
                            sensor_no = i['sensor_no']
                            Absolute_distance = i['Absolute_distance']
                            Upstream = i['Upstream']
                            Pipe_length = i['Pipe_length']
                            Feature_type = i['Feature_type']
                            Feature_identification = i['Feature_identification']
                            Orientation = i['Orientation']
                            WT = i['WT']
                            length = i['length']
                            Width = i['Width']
                            Depth_percentage = i['Depth_percentage']

                            """
                            Insert data into database
                            """
                            with connection.cursor() as cursor:
                                query_defect_insert = "INSERT INTO dent_table (runid,Pipe_No,start_index,end_index,start_sensor,end_sensor,sensor_no,Absolute_distance,Upstream,Pipe_length,Feature_type,Feature_identification,Orientation,WT,length,Width,Depth_percentage) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                                cursor.execute(query_defect_insert, (
                                    int(runid), pipe, start_index, end_index, start_sensor, end_sensor,sensor_no,
                                    Absolute_distance, Upstream, Pipe_length, Feature_type,Feature_identification,
                                    Orientation, WT, length, Width, Depth_percentage))

                                connection.commit()
                                QMessageBox.information(self, 'Success', 'Data saved')

                            with connection.cursor() as cursor:
                                Fetch_weld_detail = "select id,Pipe_No,Absolute_distance,Upstream,Pipe_length,Feature_type,Feature_identification,Orientation,length,Width,Depth_percentage from dent_table where runid='%s' and Pipe_No='%s'"
                                # Execute query.
                                cursor.execute(Fetch_weld_detail, (int(self.runid), int(self.pipe_id)))
                                self.myTableWidget_lc.setRowCount(0)
                                allSQLRows = cursor.fetchall()
                                if allSQLRows:
                                    for row_number, row_data in enumerate(allSQLRows):
                                        self.myTableWidget_lc.insertRow(row_number)
                                        for column_num, data in enumerate(row_data):
                                            self.myTableWidget_lc.setItem(row_number, column_num,
                                                                        QtWidgets.QTableWidgetItem(str(data)))
                                    self.myTableWidget_lc.setEditTriggers(QAbstractItemView.NoEditTriggers)
                                    self.myTableWidget_lc.doubleClicked.connect(self.handle_table_double_click_lc)
                                else:
                                    # self.myTableWidget5.doubleClicked.disconnect(self.handle_table_double_click)
                                    Config.warning_msg("No record found", "")
                        break
                    else:
                        QMessageBox.warning(self, 'Invalid Input', 'Please enter a name.')
                else:
                    print('Operation canceled.')
                    break
        else:
            QMessageBox.warning(self, 'Invalid Input',
                                'Select RectangleSelection of Marking, then press the button for Lat And Long')


    def handle_table_double_click_lc(self, item):
        # Get the row data including the unique ID
        row = item.row()
        unique_id = self.myTableWidget_lc.item(row, 0).text()  # Assuming the ID is in the first column

        # Query the database for the coordinates corresponding to the unique ID
        with Config.connection.cursor() as cursor:
            query_for_coordinates = "SELECT start_index, end_index, start_sensor, end_sensor, length,Feature_identification FROM dent_table WHERE id = %s"
            b = cursor.execute(query_for_coordinates, (unique_id))
            result = cursor.fetchone()  # Assuming the query returns only one row
            if result:
                start_index, end_index, y_start_hm, y_end_hm, length,Feature_identification = result
                print("Table Widget Query...", start_index, end_index, y_start_hm, y_end_hm)
                self.annotate_heatmap_lc(start_index, end_index, y_start_hm, y_end_hm, unique_id,Feature_identification)
            else:
                QMessageBox.warning(self, 'Warning', 'No Record Found')

    def annotate_heatmap_lc(self, start_index, end_index, y_start_hm, y_end_hm, unique_id,Feature_identification):
        start_x_pos = self.index_lc.index(start_index)
        end_x_pos = self.index_lc.index(end_index)
        # Draw a rectangle on the heatmap image using matplotlib patches
        rect_width = end_x_pos - start_x_pos
        rect_height = y_end_hm - y_start_hm

        # Add unique ID annotation
        text_x_pos = (start_x_pos + end_x_pos) / 2  # Calculate the center position for the text
        text_y_pos = y_start_hm - 0.5 * rect_height  # Position the text slightly above the rectangle
        self.figure_x.gca().text(text_x_pos, text_y_pos, Feature_identification+'-'+unique_id, ha='center', va='bottom')

        # Create a Rectangle patch
        rect = Rectangle((start_x_pos, y_start_hm), rect_width, rect_height, edgecolor='black', linewidth=1, fill=False)
        self.figure_x.gca().add_patch(rect)
        self.canvas_x.draw()  # Redraw the canvas to display the rectangle


    def basevalue(self):
        print("hi base val func")
        if self.rect_start_1 is not None and self.rect_end_1 is not None:
            print("hi rect start1 func")
            index_chart = self.index_lc
            start_counter = index_chart[int(self.rect_start_1[0])]
            end_counter = index_chart[int(self.rect_end_1[0])]
            runid = self.runid
            pipe_id = self.pipe_id
            # print(start_counter, end_counter)
            query_for_start = 'SELECT proximity1, proximity2, proximity3, proximity4, proximity5, proximity6, proximity7, proximity8,proximity9, proximity10, proximity11, proximity12, proximity13, proximity14, proximity15,proximity16, proximity17, proximity18, proximity19, proximity20, proximity21, proximity22, proximity23, proximity24 FROM ' + Config.table_name + ' WHERE index>{} AND index<{} order by index'
            query_job = client.query(query_for_start.format(start_counter, end_counter))
            results = query_job.result().to_dataframe().mean()
            base_value_each_pipe = results.to_list()
            proximity1 = base_value_each_pipe[0]
            proximity2 = base_value_each_pipe[1]
            proximity3 = base_value_each_pipe[2]
            proximity4 = base_value_each_pipe[3]
            proximity5 = base_value_each_pipe[4]
            proximity6 = base_value_each_pipe[5]
            proximity7 = base_value_each_pipe[6]
            proximity8 = base_value_each_pipe[7]
            proximity9 = base_value_each_pipe[8]
            proximity10 = base_value_each_pipe[9]
            proximity11 = base_value_each_pipe[10]
            proximity12 = base_value_each_pipe[11]
            proximity13 = base_value_each_pipe[12]
            proximity14 = base_value_each_pipe[13]
            proximity15 = base_value_each_pipe[14]
            proximity16 = base_value_each_pipe[15]
            proximity17 = base_value_each_pipe[16]
            proximity18 = base_value_each_pipe[17]
            proximity19 = base_value_each_pipe[18]
            proximity20 = base_value_each_pipe[19]
            proximity21 = base_value_each_pipe[20]
            proximity22 = base_value_each_pipe[21]
            proximity23 = base_value_each_pipe[22]
            proximity24 = base_value_each_pipe[23]
            with connection.cursor() as cursor:
                query_pipe_insert = "INSERT INTO base_value (runid,pipe_id,proximity1, proximity2, proximity3, proximity4, proximity5, proximity6, proximity7, proximity8,proximity9, proximity10, proximity11, proximity12, proximity13, proximity14, proximity15,proximity16, proximity17, proximity18, proximity19, proximity20, proximity21, proximity22, proximity23, proximity24) VALUE({},'{}','{}','{}','{}','{}','{}',{},'{}','{}',{},'{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}',{},'{}','{}')".format(
                    runid, pipe_id, proximity1, proximity2, proximity3, proximity4, proximity5, proximity6, proximity7,
                    proximity8, proximity9, proximity10,
                    proximity11, proximity12, proximity13, proximity14, proximity15, proximity16, proximity17,
                    proximity18, proximity19, proximity20, proximity21, proximity22, proximity23, proximity24)
                cursor.execute(query_pipe_insert)
                connection.commit()
                QMessageBox.information(self, 'Success', 'Data saved')
        else:
            QMessageBox.warning(self, 'Invalid Input',
                                'Select RectangleSelection of Marking, then press the button for base value')
        # self.selection_mark_base_value.setCheckable(False)


    def Line_chart_next(self):
        current_index = self.combo.currentIndex()
        if current_index < self.combo.count() - 1:
            self.combo.setCurrentIndex(current_index + 1)
            self.Line_chart()

    def Line_chart_previous(self):
        current_index = self.combo.currentIndex()
        if current_index > 0:
            self.combo.setCurrentIndex(current_index - 1)
            self.Line_chart()


    def Line_chart(self):
        # print("hii")
        Config.print_with_time("Pre graph analysis called")
        runid = self.runid
        pipe_id = self.combo.currentText()
        self.pipe_id = int(pipe_id)
        with connection.cursor() as cursor:
            query = "SELECT start_index,end_index,length FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
            cursor.execute(query)
            result = cursor.fetchone()
            self.start_index_lc, self.end_index_lc, self.weld_pipe_length_oddo2_lc = result[0], result[1], result[2]

            if not result:
                Config.print_with_time("No data found for this pipe ID : ")
            else:
                """
                pkl file is found in local path 
                """
                path = Config.pkl_path + self.project_name + '/' + str(pipe_id) + '.pkl'
                # print("Path....", path)
                if os.path.isfile(path):
                    Config.print_with_time("File exist")
                    df_pipe = pd.read_pickle(path)
                    df_pipe = df_pipe.fillna(method='ffill')
                    self.index_lc = list(df_pipe['index'])
                    self.oddo1 = (df_pipe['ODDO2'] - Config.oddo2) / 1000

                    # start_oddo1 = self.oddo1[self.index_lc.index(start_index)]
                    # end_oddo1 = self.oddo1[self.index_lc.index(end_index)]
                    # self.weld_pipe_length_oddo2_lc = end_oddo1 - start_oddo1

                    self.figure_x.clear()
                    self.ax = self.figure_x.add_subplot(111)
                    self.ax.figure.subplots_adjust(bottom=0.085, left=0.055, top=0.930, right=0.920)
                    self.ax.clear()
                    self.df_new = df_pipe[
                        ['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5', 'proximity6',
                         'proximity7', 'proximity8',
                         'proximity9', 'proximity10', 'proximity11', 'proximity12', 'proximity13', 'proximity14',
                         'proximity15',
                         'proximity16', 'proximity17', 'proximity18', 'proximity19', 'proximity20', 'proximity21',
                         'proximity22', 'proximity23', 'proximity24']]
                    #print("Plotted data", self.df_new)
                    res = ['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5', 'proximity6',
                           'proximity7',
                           'proximity8',
                           'proximity9', 'proximity10', 'proximity11', 'proximity12', 'proximity13', 'proximity14',
                           'proximity15',
                           'proximity16', 'proximity17', 'proximity18', 'proximity19', 'proximity20', 'proximity21',
                           'proximity22', 'proximity23', 'proximity24']

                    # Maximum1 = self.df_new.max()
                    # k1 = list(Maximum1)
                    #
                    # Minimum_value_each_holl_sensor = self.df_new.min()
                    # k2 = list(Minimum_value_each_holl_sensor)
                    #
                    # """
                    # Difference b/w maximum value and minimum value
                    # """
                    # t1 = []
                    # for j, data in enumerate(k1):
                    #     t1.append(data - k2[j])
                    #
                    # l = 70
                    # for i, column in enumerate(res):
                    #     self.df_new[column] = ((((self.df_new[column] - k2[i]) / t1[i]) * 100) + (l * i))

                    scaler = MinMaxScaler()
                    scaled_values = scaler.fit_transform(df_pipe[res])
                    gap_size = 0
                    for i, col in enumerate(res):
                        df_pipe[col] = scaled_values[:, i] + i * gap_size

                    # print("DataFrame......",df1)
                    n = 30  # the larger n is, the smoother curve will be
                    b = [1.0 / n] * n
                    a = 1
                    ls = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0]

                    for j1, column2 in enumerate(res):
                        df_pipe[column2] = df_pipe[column2] + ls[j1]

                    for i, data in enumerate(res):
                        yy = lfilter(b, a, df_pipe[data])
                        self.ax.plot(self.index_lc, yy, label=data)

                    self.ax.margins(x=0, y=0)
                    oddo_val = list(self.oddo1)
                    num_ticks1 = len(self.ax.get_xticks())  # Adjust the number of ticks based on your preference
                    print(num_ticks1)
                    tick_positions1 = [int(i) for i in np.linspace(0, len(oddo_val) - 1, num_ticks1)]
                    print(tick_positions1)

                    ax4 = self.ax.twiny()
                    ax4.set_xticks(tick_positions1)
                    ax4.set_xticklabels([f'{oddo_val[i]:.3f}' for i in tick_positions1], size=8)
                    ax4.set_xlabel("Absolute Distance (m)", size=8)

                    def on_hover(event):
                        if event.inaxes:
                            x, y = event.xdata, event.ydata
                            if x is not None:
                                x = int(event.xdata)
                                y = int(event.ydata)
                                z = (df_pipe.loc[df_pipe.index == x, 'ODDO2']) - Config.oddo2
                                Abs_distance = int(z.values[0])
                                index_value = df_pipe.loc[df_pipe.index == x, 'index']
                                index_value_1 = int(index_value.values[0])
                                # print("index_value", index_value_1)
                                # print("Abs.distance", Abs_distance)
                                self.toolbar_x.set_message(
                                    f"Index_Value={index_value_1}, Abs.Distance(mm)={Abs_distance},\nSensor_offset_Values={y}")
                            else:
                                self.toolbar_x.set_message(f" ")

                    self.canvas_x.mpl_connect('motion_notify_event', on_hover)

                    self.ax.set_ylabel('Proximity Sensor')
                    self.ax.set_xlabel('Index')
                    self.ax.legend(loc='center left', bbox_to_anchor=(1, 0.4))
                    self.canvas_x.draw()
                    rs1 = RectangleSelector(self.figure_x.gca(), self.rect_selection_line_chart, useblit=False)
                    plt.connect('key_press_event', rs1)

                    # with connection.cursor() as cursor:
                    #     Fetch_weld_detail = "select id,Pipe_No,Absolute_distance,Upstream,Pipe_length,Feature_type,Feature_identification,Orientation,length,Width,Depth_percentage from dent_table where runid='%s' and Pipe_No='%s'"
                    #     # Execute query.
                    #     cursor.execute(Fetch_weld_detail, (int(self.runid), int(self.pipe_id)))
                    #     self.myTableWidget_lc.setRowCount(0)
                    #     allSQLRows = cursor.fetchall()
                    #     if allSQLRows:
                    #         for row_number, row_data in enumerate(allSQLRows):
                    #             self.myTableWidget_lc.insertRow(row_number)
                    #             for column_num, data in enumerate(row_data):
                    #                 self.myTableWidget_lc.setItem(row_number, column_num,
                    #                                             QtWidgets.QTableWidgetItem(str(data)))
                    #         self.myTableWidget_lc.setEditTriggers(QAbstractItemView.NoEditTriggers)
                    #         self.myTableWidget_lc.doubleClicked.connect(self.handle_table_double_click_lc)
                    #     else:
                    #         # self.myTableWidget5.doubleClicked.disconnect(self.handle_table_double_click)
                    #         Config.warning_msg("No record found", "")

                else:
                    """
                    pkl file is not found than data fetch from GCP and save pkl file in local path
                    """
                    folder_path = Config.pkl_path + self.project_name
                    print(folder_path)
                    Config.print_with_time("File not exist")
                    try:
                        os.makedirs(folder_path)
                    except:
                        Config.print_with_time("Folder already exists")
                    self.start_index_lc, self.end_index_lc = result[0], result[1]
                    print("start index and end index", self.start_index_lc, self.end_index_lc)
                    Config.print_with_time("Start fetching at : ")

                    query_for_start = 'SELECT * FROM ' + Config.table_name + ' WHERE index>={} AND  index<={} order by index'
                    query_job = client.query(query_for_start.format(self.start_index_lc, self.end_index_lc))
                    df_pipe = query_job.result().to_dataframe()
                    print("dataframe", df_pipe)
                    df_pipe.to_pickle(folder_path + '/' + str(pipe_id) + '.pkl')
                    Config.print_with_time("Succesfully saved to pickle file")
                    self.oddo1 = (df_pipe['ODDO2'] - Config.oddo2) / 1000
                    self.index_lc = list(df_pipe['index'])
                    self.figure_x.clear()
                    self.ax = self.figure_x.add_subplot(111)
                    self.ax.figure.subplots_adjust(bottom=0.085, left=0.055, top=0.930, right=0.920)
                    self.ax.clear()
                    self.df_new = df_pipe[
                        ['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5', 'proximity6',
                         'proximity7', 'proximity8',
                         'proximity9', 'proximity10', 'proximity11', 'proximity12', 'proximity13', 'proximity14',
                         'proximity15',
                         'proximity16', 'proximity17', 'proximity18', 'proximity19', 'proximity20', 'proximity21',
                         'proximity22', 'proximity23', 'proximity24']]
                    print("Plotted data", self.df_new)
                    res = ['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5', 'proximity6',
                           'proximity7',
                           'proximity8',
                           'proximity9', 'proximity10', 'proximity11', 'proximity12', 'proximity13', 'proximity14',
                           'proximity15',
                           'proximity16', 'proximity17', 'proximity18', 'proximity19', 'proximity20', 'proximity21',
                           'proximity22', 'proximity23', 'proximity24']
                    # Maximum1 = self.df_new.max()
                    # k1 = list(Maximum1)
                    #
                    # Minimum_value_each_holl_sensor = self.df_new.min()
                    # k2 = list(Minimum_value_each_holl_sensor)
                    #
                    # """
                    # Difference b/w maximum value and minimum value
                    # """
                    # t1 = []
                    # for j, data in enumerate(k1):
                    #     t1.append(data - k2[j])
                    #
                    # l = 70
                    # for i, column in enumerate(res):
                    #     self.df_new[column] = ((((self.df_new[column] - k2[i]) / t1[i]) * 100) + (l * i))
                    #
                    # for i,data in enumerate(res):
                    #     self.ax.plot(index,self.df_new[data].to_numpy(),label=data)

                    scaler = MinMaxScaler()
                    scaled_values = scaler.fit_transform(df_pipe[res])
                    gap_size = 0
                    for i, col in enumerate(res):
                        df_pipe[col] = scaled_values[:, i] + i * gap_size

                    # print("DataFrame......",df1)
                    n = 30  # the larger n is, the smoother curve will be
                    b = [1.0 / n] * n
                    a = 1
                    ls = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0]
                    ls = [round(i * 0.5, 1) for i in range(1, 25)]

                    for j1, column2 in enumerate(res):
                        df_pipe[column2] = df_pipe[column2] + ls[j1]

                    for i, data in enumerate(res):
                        yy = lfilter(b, a, df_pipe[data])
                        self.ax.plot(self.index_lc, yy, label=data)

                    self.ax.margins(x=0, y=0)
                    oddo_val = list(self.oddo1)
                    num_ticks1 = len(self.ax.get_xticks())  # Adjust the number of ticks based on your preference
                    print(num_ticks1)
                    tick_positions1 = [int(i) for i in np.linspace(0, len(oddo_val) - 1, num_ticks1)]
                    print(tick_positions1)

                    ax4 = self.ax.twiny()
                    ax4.set_xticks(tick_positions1)
                    ax4.set_xticklabels([f'{oddo_val[i]:.3f}' for i in tick_positions1], size=8)
                    ax4.set_xlabel("Absolute Distance (m)", size=8)

                    # def on_hover(event):
                    #     if event.inaxes:
                    #         x, y = event.xdata, event.ydata
                    #         if x is not None:
                    #             x = int(event.xdata)
                    #             y = int(event.ydata)
                    #             z = (df_pipe.loc[df_pipe.self.index_lc == x, 'ODDO2']) - Config.oddo2
                    #             Abs_distance = int(z.values[0])
                    #             index_value = df_pipe.loc[df_pipe.self.index_lc == x, 'index']
                    #             index_value_1=int(index_value.values[0])
                    #             print("index_value",index_value_1)
                    #             print("Abs.distance",Abs_distance)
                    #             self.toolbar_x.set_message(
                    #                 f"Index_Value={index_value_1}, Abs.Distance(mm)={Abs_distance},\nSensor_offset_Values={y}")
                    #         else:
                    #             self.toolbar_x.set_message(f" ")
                    #
                    # self.canvas_x.mpl_connect('motion_notify_event', on_hover)

                    self.ax.set_ylabel('Proximity Sensor')
                    self.ax.set_xlabel('Index')
                    self.ax.legend(loc='center left', bbox_to_anchor=(1, 0.4))
                    self.canvas_x.draw()
                    rs1 = RectangleSelector(self.figure_x.gca(), self.rect_selection_line_chart, useblit=False)
                    plt.connect('key_press_event', rs1)




                    # query = query_generator.get_pipe(lower_sensitivity, upper_sensitivity, runid, start_index, end_index)
                    # query_job = client.query(query)
                    # results = query_job.result()

                    # to_execute = 'SELECT index,oddo1,oddo2,[proximity1, proximity2, proximity3, proximity4, proximity5, proximity6, proximity7, proximity8,proximity9, proximity10, proximity11, proximity12, proximity13, proximity14, proximity15,proximity16, proximity17, proximity18, proximity19, proximity20, proximity21, proximity22, proximity23, proximity24] FROM ' + Config.table_name + ' where index>{} and index<{} order by index'
                    #
                    # query_to_run = client.query(to_execute.format(start_index, end_index))
                    # results = query_to_run.result()
                    # #print(results)
                    #
                    # Config.print_with_time("End fetching  at : ")
                    # data = []
                    # oddo1 = []
                    # oddo2 = []
                    # indexes = []
                    # index = []
                    #
                    # Config.print_with_time("Start of conversion at : ")
                    # for row in results:
                    #     data.append(row[3])
                    #     # data.append(row['frames'])
                    #     oddo1.append(row['oddo1'])
                    #     oddo2.append(row['oddo2'])
                    #     index.append(row['index'])
                    #     # indexes.append(ranges(index_of_occurrences(row['frames'], 1)))
                    #     indexes.append(ranges(index_of_occurrences(row[3], 1)))
                    # self.df_new = pd.DataFrame(data,
                    #                            columns=['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5', 'proximity6', 'proximity7', 'proximity8',
                    #                                     'proximity9', 'proximity10', 'proximity11', 'proximity12', 'proximity13', 'proximity14', 'proximity15',
                    #                                     'proximity16', 'proximity17', 'proximity18', 'proximity19', 'proximity20', 'proximity21', 'proximity22', 'proximity23', 'proximity24'])
                    # res = ['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5', 'proximity6', 'proximity7',
                    #        'proximity8',
                    #        'proximity9', 'proximity10', 'proximity11', 'proximity12', 'proximity13', 'proximity14',
                    #        'proximity15',
                    #        'proximity16', 'proximity17', 'proximity18', 'proximity19', 'proximity20', 'proximity21', 'proximity22', 'proximity23', 'proximity24']
                    # print("index...",index)
                    # Maximum1 = self.df_new.max()
                    # k1 = list(Maximum1)
                    #
                    # Minimum_value_each_holl_sensor = self.df_new.min()
                    # k2 = list(Minimum_value_each_holl_sensor)
                    #
                    # """
                    # Difference b/w maximum value and minimum value
                    # """
                    # t1 = []
                    # for j, data in enumerate(k1):
                    #     t1.append(data - k2[j])
                    #
                    # l = 100
                    # for i, column in enumerate(res):
                    #     self.df_new[column] = ((((self.df_new[column] - k2[i]) / t1[i]) * 100) + (l * i))
                    #
                    #
                    # Config.print_with_time("Ending of conversion at : ")
                    # self.figure_x.clear()
                    # self.ax = self.figure_x.add_subplot(111)
                    #
                    # # discards the old graph
                    # self.ax.clear()
                    # res = ['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5', 'proximity6', 'proximity7', 'proximity8',
                    #                                     'proximity9', 'proximity10', 'proximity11', 'proximity12', 'proximity13', 'proximity14', 'proximity15',
                    #                                     'proximity16', 'proximity17', 'proximity18', 'proximity19', 'proximity20', 'proximity21', 'proximity22', 'proximity23', 'proximity24']
                    # #self.a = []
                    # for i,data in enumerate(res):
                    #     self.ax.plot(index,self.df_new[data].to_numpy(),label=data)
                    #
                    #
                    # self.ax.set_ylabel('Proximity Sensor')
                    # self.ax.legend(loc='center left', bbox_to_anchor=(1, 0.4))
                    # self.canvas_x.draw()
                    # rs = RectangleSelector(self.ax, self.line_selection,
                    #                         useblit=False)
                    # plt.connect('key_press_event', rs)

        # self.GenerateGraph()

    # def GenerateGraph(self):
    #     graph.generate_heat_map(self.hbox2, self.full_screen, self.defect_list, self.df_new,
    #                              self.project_name, self.pipe_id, self.figure)

    #################### Hard Coded #########################################
    ###########################################################################
    # self.a = pd.read_csv('C:/Users/Monika Sharma/Dropbox/PC/Desktop/d.csv', index_col=0)
    # print(a)
    # self.a['index'] = np.arange(len(self.a))
    # self.final_df = self.a
    # self.ax = self.figure.add_subplot(111)
    # print(final_df)
    # self.generate_graph()

    # def plot(self):
    #     Config.print_with_time("Pre graph analysis called")
    #     runid = self.runid
    #     pipe_id = self.combo_box.currentText()
    #     self.pipe_id = int(pipe_id)
    #     # lower_sensitivity = self.lower_Sensitivity_combo_box.currentText()
    #     # upper_sensitivity = self.upper_Sensitivity_combo_box.currentText()
    #     # print(pipe_id)
    #     with connection.cursor() as cursor:
    #         query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
    #         cursor.execute(query)
    #         result = cursor.fetchone()
    #         print(result)
    #         if not result:
    #             Config.print_with_time("No data found for this pipe ID : ")
    #
    #         else:
    #             #################### Hard Coded #########################################
    #             ###########################################################################
    #             start_index, end_index = result[0], result[1]
    #             print("start index and end index", start_index, end_index)
    #             Config.print_with_time("Start fetching at : ")
    #             # query = query_generator.get_pipe(lower_sensitivity, upper_sensitivity, runid, start_index, end_index)
    #             # query_job = client.query(query)
    #             # results = query_job.result()
    #
    #             to_execute = 'SELECT index,oddo1,oddo2,[proximity1 ,proximity2 ,proximity3 ,proximity4 ,proximity5 ,proximity6 ,proximity7 ,proximity8 ,proximity9 ,proximity10 ,proximity11 ,proximity12 ,proximity13 ,proximity14 ,proximity15 ,' \
    #                          'proximity16 ,proximity17 ,proximity18, 'proximity19', 'proximity20', 'proximity21', 'proximity22', 'proximity23', 'proximity24'] FROM ' + Config.table_name + ' where index>{} and index<{} order by index'
    #
    #             query_to_run =client.query(to_execute.format(start_index, end_index))
    #             results = query_to_run.result()
    #             print(results)
    #
    #             Config.print_with_time("End fetching  at : ")
    #             data = []
    #             oddo1 = []
    #             oddo2 = []
    #             indexes = []
    #             index=[]
    #
    #             Config.print_with_time("Start of conversion at : ")
    #             for row in results:
    #                 data.append(row[3])
    #                 #data.append(row['frames'])
    #                 oddo1.append(row['oddo1'])
    #                 oddo2.append(row['oddo2'])
    #                 index.append(row['index'])
    #                 #indexes.append(ranges(index_of_occurrences(row['frames'], 1)))
    #                 indexes.append(ranges(index_of_occurrences(row[3], 1)))
    #             self.df_new = pd.DataFrame(data,
    #                                        columns=['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5', 'proximity6', 'proximity7', 'proximity8',
    #                                                 'proximity9', 'proximity10', 'proximity11', 'proximity12', 'proximity13', 'proximity14', 'proximity15',
    #                                                 'proximity16', 'proximity17', 'proximity18', 'proximity19', 'proximity20', 'proximity21', 'proximity22', 'proximity23', 'proximity24'])
    #             #self.df_new = self.df_new.transpose()
    #             df_new=self.df_new
    #             #df_new.to_csv('E:/Egp_desktop_web/Egp_Desktop/d.csv')
    #             df_new['new_index'] = np.arange(len(df_new))
    #             self.final_df=df_new
    #             print(self.final_df)
    #
    #             Config.print_with_time("Ending of conversion at : ")
    #             #print(df_new['new_index'])
    #             self.figure.clear()
    #             self.ax = self.figure.add_subplot(111)
    #
    #             # discards the old graph
    #             self.ax.clear()
    #             res=['proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5', 'proximity6', 'proximity7', 'proximity8',
    #                                                 'proximity9', 'proximity10', 'proximity11', 'proximity12', 'proximity13', 'proximity14', 'proximity15',
    #                                                 'proximity16', 'proximity17', 'proximity18', 'proximity19', 'proximity20', 'proximity21', 'proximity22', 'proximity23', 'proximity24']
    #             # plot data
    #             self.a=[]
    #             for i in res:
    #                 self.ax.plot(index,df_new[i],label=i)
    #                 self.a.append(df_new[i])
    #             self.ax.set_ylabel('Proximity')
    #             self.x=index
    #             # self.y=df_new[i]
    #             # self.a.append(self.y)
    #             # print("x value",self.x)
    #             # print("y value",self.y)
    #             self.canvas.draw()
    #
    #             self.figure1.clear()
    #             ax1 = self.figure1.add_subplot(111)
    #             ax1.clear()
    #             ax1.plot(index,oddo1)
    #             ax1.set_ylabel('Odometer')
    #             self.canvas1.draw()
    #             #self.generate_graph()
    #             #self.figure.canvas.mpl_connect('pick_event', self.onpick)
    #             rs = RectangleSelector(self.ax, self.line,
    #                                    useblit=False)
    #             plt.connect('key_press_event', rs)

    # self.draw_rectangle(self.dent_list, ax)

    # self.figure.clear()
    # ax = self.figure.add_subplot(111)
    # ax.clear()
    # res = ['index', 'proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5', 'proximity6',
    #        'proximity7', 'proximity8',
    #        'proximity9', 'proximity10', 'proximity11', 'proximity12', 'proximity13', 'proximity14',
    #        'proximity15',
    #        'proximity16', 'proximity17', 'proximity18', 'proximity19', 'proximity20', 'proximity21', 'proximity22', 'proximity23', 'proximity24']
    # self.a = []
    # rs = RectangleSelector(ax, self.line, useblit=False)
    # plt.connect('key_press_event', rs)
    # for i in res:
    #     ax.plot(self.final_df['index'], self.final_df[i], label=i)
    #     self.a.append(self.final_df[i])
    # ax.set_ylabel('Proximity')
    # self.canvas.draw()
    #################   Hard Coded#########################################
    ################################################################
    ###################################################################

    # def generate_graph(self):
    #     graph1.generate_heat_map(self.final_df, self.figure, self.line, self.canvas, self.dent_list1)

    # data = [random.random() for i in range(10)]
    #
    # # instead of ax.hold(False)
    # self.figure.clear()
    #
    # # create an axis
    # ax = self.figure.add_subplot(111)
    #
    # # plot data
    # ax.plot(data, '*-')

    # refresh canvas
    # self.canvas.draw()
    ######## GenerateGraph function #########
    # def pre_graph_analysis(self):
    #     Config.print_with_time("Pre graph analysis called")
    #     runid = self.runid
    #     pipe_id = self.combo_box.currentText()
    #     self.pipe_id = int(pipe_id)
    #     # lower_sensitivity = self.lower_Sensitivity_combo_box.currentText()
    #     # upper_sensitivity = self.upper_Sensitivity_combo_box.currentText()
    #     print(pipe_id)
    #     # return
    #     # self.defect_list = []
    #     # with connection.cursor() as cursor:
    #     #     query_pipe_end_update = "UPDATE pipes set lower_sensitivity='%s',upper_sensitivity='%s' where id='%s' "
    #     #     cursor.execute(query_pipe_end_update,
    #     #                    (float(lower_sensitivity), float(upper_sensitivity), int(pipe_id)))
    #     #     connection.commit()
    #
    #     with connection.cursor() as cursor:
    #         query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
    #         cursor.execute(query)
    #         result = cursor.fetchone()
    #         print(result)
    #         if not result:
    #             Config.print_with_time("No data found for this pipe ID : ")
    #
    #         else:
    #             start_index, end_index = result[0], result[1]
    #             Config.print_with_time("Start fetching at : ")
    #             query = query_generator.get_pipe(runid, start_index, end_index)
    #             query_job = client.query(query)
    #             results = query_job.result()
    #
    #             Config.print_with_time("End fetching  at : ")
    #             data = []
    #             oddo1 = []
    #             oddo2 = []
    #             indexes = []
    #             #index=[]
    #
    #             Config.print_with_time("Start of conversion at : ")
    #             for row in results:
    #                 data.append(row['frames'])
    #                 oddo1.append(row['oddo1'])
    #                 oddo2.append(row['oddo2'])
    #                 #index.append(row['index'])
    #                 indexes.append(ranges(index_of_occurrences(row['frames'], 1)))
    #             print("indexes",indexes)
    #             self.df_new = pd.DataFrame(data,
    #                                        columns=['F1H1', 'F1H2', 'F1H3', 'F1H4', 'F2H1', 'F2H2', 'F2H3', 'F2H4',
    #                                                 'F3H1', 'F3H2', 'F3H3', 'F3H4', 'F4H1', 'F4H2', 'F4H3',
    #                                                 'F4H4', 'F5H1', 'F5H2', 'F5H3', 'F5H4', 'F6H1', 'F6H2', 'F6H3',
    #                                                 'F6H4',
    #                                                 'F7H1', 'F7H2', 'F7H3', 'F7H4', 'F8H1', 'F8H2', 'F8H3', 'F8H4',
    #                                                 'F9H1', 'F9H2', 'F9H3', 'F9H4', 'F10H1', 'F10H2', 'F10H3', 'F10H4',
    #                                                 'F11H1', 'F11H2', 'F11H3', 'F11H4', 'F12H1', 'F12H2', 'F12H3',
    #                                                 'F12H4', 'F13H1', 'F13H2', 'F13H3', 'F13H4', 'F14H1', 'F14H2',
    #                                                 'F14H3', 'F14H4',
    #                                                 'F15H1', 'F15H2', 'F15H3', 'F15H4', 'F16H1', 'F16H2', 'F16H3',
    #                                                 'F16H4', 'F17H1', 'F17H2', 'F17H3', 'F17H4', 'F18H1', 'F18H2',
    #                                                 'F18H3', 'F18H4',
    #                                                 'F19H1', 'F19H2', 'F19H3', 'F19H4', 'F20H1', 'F20H2', 'F20H3',
    #                                                 'F20H4', 'F21H1', 'F21H2', 'F21H3', 'F21H4', 'F22H1', 'F22H2',
    #                                                 'F22H3', 'F22H4',
    #                                                 'F23H1', 'F23H2', 'F23H3', 'F23H4', 'F24H1', 'F24H2', 'F24H3',
    #                                                 'F24H4'])
    #             self.df_new = self.df_new.transpose()
    #
    #             print(oddo1)
    #             print(oddo2)
    #             print(indexes)
    #             # self.df_new['oddo1']=row['oddo1']
    #             # self.df_new['oddo2']=row['oddo2']
    #             # print(self.df_new)
    #             Config.print_with_time("Ending of conversion at : ")
    #             Config.print_with_time("Start of defect calculation at : ")
    #             raw_defects = extract_raw_defects(indexes)
    #             defects = []
    #             for row in raw_defects:
    #                 defects = defects + calculate_defect(row, data)
    #             finial_defects = defect_length_calculator(data, defects, oddo1, oddo2)
    #             print("final defect list", finial_defects)
    #             insert_defect_into_db(finial_defects, runid, pipe_id)
    #             Config.print_with_time("End of defect calculation at : ")
    #             # self.df = results.to_dataframe()
    #             # print(self.df)
    #     self.defect_list = get_defect_list_from_db(runid, pipe_id)
    #     self.GenerateGraph()

    # def GenerateGraph(self):
    #     graph.generate_heat_map(self.gridLayoutWidget_4, self.full_screen, self.defect_list, self.df_new,
    #                             self.line_select_callback, self.project_name, self.pipe_id, self.figure)

    # def line_select_callback(self, eclick, erelease):
    #     x1, y1 = eclick.xdata, eclick.ydata
    #     x2, y2 = erelease.xdata, erelease.ydata
    #     self.defect_list.append([x1, y1, x2 - x1, y2 - y1])
    #     print(self.defect_list)
    #     self.GenerateGraph()

    def reset_defect(self):
        runid = self.runid
        # self.reset_defect_pushButton.hide()

        # with connection.cursor() as cursor:
        #     a = cursor.execute("DELETE FROM defectdetail WHERE  runid=" + str(runid) + " and type='manual'")
        #     cursor.close()
        self.defect_list = []
        self.GenerateGraph()

    def add_defect(self):
        print("defect_list", self.defect_list)
        # self.add_defect_pushButton.hide()
        # temp_defect[0].append('unknown')
        # temp_defect[0].append(0.0)
        # temp_defect[0].append(0.0)
        # self.defect_list.append(temp_defect[0])
        # self.GenerateGraph()
        # # self.insert_and_update_defect_to_db(temp_defect, self.runid, self.pipe_id)
        # temp_defect.clear()
        # self.reset_defect_pushButton.show()

    def insert_and_update_defect_to_db(self, d_list, runid, pipe_id):
        for defect in d_list:
            print(defect)
            with Config.connection.cursor() as cursor:
                query_weld_insert = "INSERT INTO defectdetail (runid, pipe_id, defect_length, defect_breadth, defect_angle,defect_depth,type,x,y,category,min,max) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

                # Execute query.
                b = cursor.execute(query_weld_insert, (
                    int(runid), int(pipe_id), int(defect[2]), int(defect[3]), 0, 0, 'manual', int(defect[0]),
                    int(defect[1]), 'unknown', 0.0, 0.0))
                if b:
                    print("data is inserted successfully")
                else:
                    print("data is not inserted successfully")
                Config.connection.commit()
        return

    def pip_info(self):
        try:
            Config.print_with_time("pipe info method called")
            runid = str(self.runid)
            self.pipe_id = self.pipeLineNumberLineEdit.text()
            # # get the pipe_id from user and save that pipe_id for global use to be use by other functions and there value should be updated accordingly
            with connection.cursor() as cursor:
                # SQL
                Fetch_pipe_record = "select runid,analytic_id,pipe_id,pipe_start_filename,pipe_start_serialno," \
                                    "pipe_end_filename,pipe_end_serialno from pipedetail where runid='%s' and " \
                                    "pipe_id='%s' "
                # Execute query.
                cursor.execute(Fetch_pipe_record, (int(runid), int(self.pipe_id)))
                fetched_data = cursor.fetchall()
                print(fetched_data)
                connection.commit()
                if fetched_data:
                    path = './Data Frames/' + self.project_name.text() + '/' + self.pipe_id + '.pkl'
                    print(path)
                    if os.path.isfile(path):
                        Config.print_with_time("File exist")
                        self.df_pipe = pd.read_pickle(path)
                    else:
                        Config.print_with_time("File not exist")
                        try:
                            os.mkdir('./Data Frames/' + self.project_name.text())
                        except:
                            Config.print_with_time("Folder already exists")

                        pipe_start_file = fetched_data[0][3]
                        pipe_start_serial = fetched_data[0][4]
                        pipe_end_file = fetched_data[0][5]
                        pipe_end_serial = fetched_data[0][6]
                        query = 'select * from ' + Config.table_name + ' where filename>={} and Serialno>={} and filename<={} and Serialno<={} and runid={} ORDER BY filename, Serialno'
                        query_job = client.query(
                            query.format(pipe_start_file, pipe_start_serial, pipe_end_file, pipe_end_serial, runid))
                        print(query.format(pipe_start_file, pipe_start_serial, pipe_end_file, pipe_end_serial, runid))
                        self.df_pipe = query_job.to_dataframe()
                        Config.print_with_time("conversion to data frame is done")
                        self.df_pipe.to_pickle(path)
                        Config.print_with_time("successfully  saved to pickle")
                    # self.df_pipe.to_csv('recods.csv)
                    Config.info_msg("Data Successfully Loaded", "")
                    # self.pre_graph_analysis()
                else:
                    Config.warning_msg("Data not Found", "")
        except OSError as error:
            Config.warning_msg(OSError or "Network speed is very slow or invalid Pipe id", "")
            logger.log_error(error or "Set_msg_body method failed with unknown Error")

    def NextPipe(self):
        self.pipeLineNumberLineEdit.setText(str(int(self.pipe_id) + 1))
        self.pip_info()

    def prev_pipe(self):
        self.pipeLineNumberLineEdit.setText(str(int(self.pipe_id) - 1))
        self.pip_info()

    def ShowWeldToPipe(self):
        with connection.cursor() as cursor:
            runid = self.runid
            try:
                Fetch_pipe_detail = "select id,runid,analytic_id,lower_sensitivity,upper_sensitivity, length, start_index,end_index from pipes where runid = '%s'"
                # Execute query.
                cursor.execute(Fetch_pipe_detail, (int(runid)))
                self.myTableWidget1.setRowCount(0)
                allSQLRows = cursor.fetchall()

                # print(allSQLRows)
                # self.id = self.allSQLRows[0][0]
                # print("id>>>>>>>>>>>>>>>", self.id)
                if allSQLRows:
                    for row_number, row_data in enumerate(allSQLRows):
                        self.myTableWidget1.insertRow(row_number)
                        for column_num, data in enumerate(row_data):
                            self.myTableWidget1.setItem(row_number, column_num, QtWidgets.QTableWidgetItem(str(data)))
                    self.myTableWidget1.setEditTriggers(QAbstractItemView.NoEditTriggers)
                else:
                    Config.warning_msg("No record found", "")
                pipe_id_list = []
                pipe_id_list.clear()
                for i in allSQLRows:
                    pipe_id_list.append(str(i[0]))
                print("pipe_id_list", pipe_id_list)
                self.combo_box.addItems(pipe_id_list)
                self.combo.addItems(pipe_id_list)
                self.combo1.addItems(pipe_id_list)
            except:
                logger.log_warning("error in show weld to pipe")

    def viewClicked(self):
        list = []
        list.clear()
        for i in range(0, 8):
            list.append(self.myTableWidget.item(self.myTableWidget.currentRow(), i).text())
        self.analytic_id = list[1]

    # def get_defect_list_from_db(self):
    #     runid = self.runid
    #     pipe_id = self.pipe_id
    #     defects = []
    #     with connection.cursor() as cursor:
    #         try:
    #             Fetch_weld_detail = "select * from defectdetail where runid='%s' and pipe_id='%s'"
    #             # Execute query.
    #             cursor.execute(Fetch_weld_detail, (int(runid), int(pipe_id)))
    #             allSQLRows = cursor.fetchall()
    #             for row in allSQLRows:
    #                 defects.append([row[8], row[9], row[3], row[4], row[10], row[11], row[12]])
    #                 if row[7] == 'manual':
    #                     self.reset_defect_pushButton.show()
    #             return defects
    #         except:
    #             logger.log_error("Error during fetching defects from db for runid = " + self.runid)
    #             return []

    def Show_Weld(self):
        # print("hi")
        runid = self.runid
        with connection.cursor() as cursor:
            try:
                # Fetch_weld_detail = "select weld_number,runid,analytic_id,sensitivity,length,start_index,end_index,start_oddo1,end_oddo1,start_oddo2,end_oddo2 from welds where runid='%s'"
                Fetch_weld_detail = f"select weld_number,runid,analytic_id,sensitivity,length,start_index,end_index,start_oddo1,end_oddo1,start_oddo2,end_oddo2 from welds where runid='%s' and id>{1}"
                # Execute query.
                cursor.execute(Fetch_weld_detail, (int(runid)))
                self.myTableWidget.setRowCount(0)
                allSQLRows = cursor.fetchall()
                if allSQLRows:
                    for row_number, row_data in enumerate(allSQLRows):
                        self.myTableWidget.insertRow(row_number)
                        for column_num, data in enumerate(row_data):
                            self.myTableWidget.setItem(row_number, column_num, QtWidgets.QTableWidgetItem(str(data)))
                    self.myTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
                else:
                    Config.warning_msg("No record found", "")
                weld_id_list = []
                weld_id_list.clear()
                for i in allSQLRows:
                    weld_id_list.append(str(i[0]))
                print("pipe_id_list", weld_id_list)
                # self.combobox1.addItems(weld_id_list)
                self.combo_box_tab9.addItems(weld_id_list)
                self.combo_box_tab8.addItems(weld_id_list)
            except:
                logger.log_error("Fetch WeldDetail has some error")

    # def WeldToPipe(self):
    #     if Config.no_weld_indicator:
    #         self.weldtoPipe = WeldToPipe.Query(self.runid, 1)
    #     else:
    #         self.weldtoPipe = WeldToPipe.Query(self.runid, self.analytic_id)
    def DefectList(self):
        runid = self.runid
        with connection.cursor() as cursor:
            try:
                Fetch_weld_detail = "select id,runid,start_observation,end_observation,start_sensor,end_sensor,angle,length,breadth,depth,type from defect where runid='%s'"
                # Execute query.
                cursor.execute(Fetch_weld_detail, (int(runid)))
                self.myTableWidget2.setRowCount(0)
                allSQLRows = cursor.fetchall()
                if allSQLRows:
                    for row_number, row_data in enumerate(allSQLRows):
                        self.myTableWidget2.insertRow(row_number)
                        for column_num, data in enumerate(row_data):
                            self.myTableWidget2.setItem(row_number, column_num, QtWidgets.QTableWidgetItem(str(data)))
                    self.myTableWidget2.setEditTriggers(QAbstractItemView.NoEditTriggers)
                else:
                    Config.warning_msg("No record found", "")
            except:
                logger.log_error("Fetch DefectList has some error")

    def CreateWeld(self):
        try:
            self.sensitivity, okPressed = QInputDialog.getText(self, "Get integer", "sensitivity")
            if okPressed:
                pass
                # self.sensitivifty = self.sensitivity
            self.weldupdate = weld_update.Query_flow(self.runid, self.sensitivity)
        except:
            logger.log_error("sensitivity is not found")

    def merge_pipe(self, runid):
        with connection.cursor() as cursor:
            Fetch_pipe_record = "select pipe_length,pipe_id,pipe_start_filename," \
                                "pipe_end_filename from pipes where runid='%s'"
            cursor.execute(Fetch_pipe_record, (int(runid)))
            fetched_data = cursor.fetchall()
            for i, elem in enumerate(fetched_data):
                pass

    def load_list(self):
        try:
            with connection.cursor() as cursor:
                # with connection:
                # print("hi there")
                cursor.execute("SELECT `runid`,`ProjectName` FROM projectdetail ORDER BY  runid desc")
                allSQLRows = cursor.fetchall()
                print(allSQLRows)

                self.left_listWidget.clear()
                company_list.clear()
                for i in allSQLRows:
                    self.a = i[0]
                    self.b = i[1]
                    company_list.append(self.b)
                self.add_to_list()
        except:
            Config.warning_msg("DB Connection failed", "")

    def Typeofdefect(self):
        try:
            runid = self.runid
            # print(runid)
            try:
                self.thickness_pipe, okPressed = QInputDialog.getText(self, "Get integer", "thickness_pipe")
                if okPressed:
                    pass
                    thickness_pipe = float(self.thickness_pipe)
                    # print(thickness_pipe)
                    if thickness_pipe < 10.0:
                        geometrical_parameter = 10
                    else:
                        geometrical_parameter = thickness_pipe
                        # print(geometrical_parameter)
                    get_type_defect(geometrical_parameter, runid)

            except:
                logger.log_error("thickness_pipe is not found")

        except:
            QMessageBox.about(self, 'Info', 'Please select the runid')

    def full_screen(self):
        self.gridLayoutWidget.hide()
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 1900, 950))
        self.gridLayoutWidget_2.showMaximized()
        self._init_back_button()

    def reset_default_screen(self):
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(100, 0, 1700, 1200))
        self.gridLayoutWidget_2.showMaximized()
        self.gridLayoutWidget.show()
        self.gridLayoutWidget_2.deleteLater()
        self.init_gridLayoutWidget_2()
        self.gridLayoutWidget_2.show()

    def generate_report(self):
        Report.generate(self.project_name, self.runid)

    def add_to_list(self):
        for i in company_list:
            self.left_listWidget.addItem(i)

    def create_project(self):
        self.uploadData = CreateProject.AddProject()

    def AddWeld(self):
        try:
            runid = self.runid
            self.AddData = AddWeld.AddWeldDetail(self.runid)
        except:
            QMessageBox.about(self, 'Info', 'Please select the runid')

    def Create_pipe(self):
        try:
            runid = self.runid
            print(runid)
            with connection.cursor() as cursor:
                fetch_last_row = "select runid,start_index,end_index,type,analytic_id,sensitivity,length,start_oddo1,end_oddo1,start_oddo2,end_oddo2 from temp_welds where runid='%s' order by start_index"
                # Execute query.
                f_data = []
                cursor.execute(fetch_last_row, (int(runid)))
                allSQLRows = cursor.fetchall()
                for i, row in enumerate(allSQLRows):
                    temp = {"start_index": row[1], "end_index": row[2], "weld_number": i + 1,
                            "type": row[3], "analytic_id": row[4], "sensitivity": row[5], "length": row[6],
                            "start_oddo1": row[7], "end_oddo1": row[8], "start_oddo2": row[9], "end_oddo2": row[10],
                            "runid": runid}
                    # print(temp)
                    f_data.append(temp)
                    insert_weld_to_db(temp)
                last_index = 0
                last_oddo = 0
                pipes = []
                Config.print_with_time("Generating Pipe")
                last_weld = f_data[-1]
                # print(f_data)
                for row in f_data:
                    # print(row)
                    oddo = row["start_oddo1"] if row["start_oddo1"] > row["start_oddo2"] else row["start_oddo2"]
                    length = oddo - last_oddo
                    obj = {"start_index": last_index, "end_index": row["start_index"], "length": length,
                           "analytic_id": row["analytic_id"], "runid": runid}
                    pipes.append(obj)
                    last_index = row["end_index"]
                    last_oddo = row["end_oddo1"] if row["end_oddo1"] > row["end_oddo2"] else row["end_oddo2"]
                    insert_pipe_to_db(obj)
                # print(pipes)
                last_pipe = get_last_pipe(runid, last_weld, last_weld['analytic_id'])
                insert_pipe_to_db(last_pipe)
                Config.print_with_time("Pipe Generation completed")
                Config.print_with_time("process end at : ")

            return

        except:
            QMessageBox.about(self, 'Info', 'Please select the runid')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EGP TOOL"))

        self.load_list_pushButton.setText(_translate("MainWindow", "Load Data"))
        self.load_list_pushButton.setStyleSheet(Style.btn_type_primary)
        __sortingEnabled = self.left_listWidget.isSortingEnabled()
        self.left_listWidget.setSortingEnabled(False)
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuSearch.setTitle(_translate("MainWindow", "Search"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuhelp.setTitle(_translate("MainWindow", "Help"))

        self.actionCreate_Project.setText(_translate("MainWindow", "Create Project"))
        self.actionCreate_Project.triggered.connect(self.create_project)
        # self.actionCreate_Project.setStyleSheet(Style.btn_type_primary)
        ########################## Call the type of defect ########################
        self.actiontypeofdefect.setText(_translate("MainWindow", "Typeofdefect"))
        self.actiontypeofdefect.triggered.connect(self.Typeofdefect)
        ##################### call the Add weld ###############
        self.addweld.setText(_translate("MainWindow", "AddWeld"))
        self.addweld.triggered.connect(self.AddWeld)

        ##################### Create Pipe ###############
        self.create_pipe.setText(_translate("MainWindow", "Create_Pipe"))
        self.create_pipe.triggered.connect(self.Create_pipe)


def breadth(dent_yes):
    inverse_value = [key for key, value in dent_yes.items()]
    # print(inverse_value)

    ############  groups of continuous numbers in a array ##############
    sequences = np.split(inverse_value, np.array(np.where(np.diff(inverse_value) > 1)[0]) + 1)

    ########## min and max value find in group of list of tuple ###########
    l = []
    for s in sequences:
        if len(s) > 1:
            l.append((np.min(s), np.max(s)))
        else:
            l.append(s[0])
    # print(l)
    b = []
    for i in l:
        if type(i) == tuple:  ################# check i is tuple or element ############
            b.append({'start': i[0], 'end': i[1]})
        else:
            pass
    return b


def insert_weld_to_db(temp):
    print("weld_obj", temp)
    """
        This will insert weld object to mysql database
        :param weld_obj : Object with value of  runid,analytic_id,sensitivity,start_index,end_index,start_oddo1,end_oddo1,start_oddo2,end_oddo2,length and weld_number
    """
    try:

        query_weld_insert = "INSERT INTO welds (weld_number,runid,start_index,end_index,type,analytic_id,sensitivity,length,start_oddo1,end_oddo1,start_oddo2,end_oddo2) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # print(runid, analytic_id, Sensitivity, start_file, end_file, start_sno, end_sno)
        with connection.cursor() as cursor:
            cursor.execute(query_weld_insert, (
            temp["weld_number"], temp["runid"], temp["start_index"], temp["end_index"], temp["type"],
            temp["analytic_id"], temp["sensitivity"], temp["length"], temp["start_oddo1"], temp["end_oddo1"],
            temp["start_oddo2"], temp["end_oddo2"]))
            connection.commit()
        return
    except:
        print("Error While Inserting weld for runid ")


def insert_pipe_to_db(pipe_obj):
    """
        This will insert pipe_obj to mysql database
        :param pipe_obj : object will value of runid,analytic_id,length,start_index and end_index
    """
    try:
        query = "INSERT INTO pipes (runid,analytic_id,length,start_index,end_index) VALUE(%s,%s," \
                "%s,%s,%s) "
        with connection.cursor() as cursor:
            cursor.execute(query,
                           (pipe_obj["runid"], pipe_obj["analytic_id"], pipe_obj["length"], pipe_obj["start_index"],
                            pipe_obj["end_index"]))
            connection.commit()
        return
    except:
        print("Error While Inserting weld for runid ")


def Width_calculation(start_sensor1, end_sensor1):
    if start_sensor1 > end_sensor1:
        bredth = 0
        return bredth

    else:
        if start_sensor1 == end_sensor1:
            bredth = 16
            return bredth
        else:
            sensor = end_sensor1 - start_sensor1
            breadth = sensor * 32
            return breadth


def get_last_pipe(runid, weld_obj, analytic_id):
    """
        This will return the last pipe object to insert into mysql db
        :param runid: Id of the Project
    """
    query = "SELECT index,oddo1,oddo2 FROM `" + Config.table_name + "` order by index desc LIMIT 1 "
    query_job = client.query(query)
    results = query_job.result()
    for row in results:
        length = row['oddo1'] - weld_obj['end_oddo1']
        end_index = row['index']
        start_index = weld_obj['end_index']
        end_index = row['index']
        obj = {"start_index": start_index, "end_index": end_index, "length": length, "analytic_id": analytic_id,
               "runid": runid}
        return obj


def ranges(nums):
    #print("nums.....",nums)
    """"
    This will merge the continues indexes and return a list that will contain list of start_index and end_index
        :param arr : List of indexes to merge
    """
    try:
        gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s + 1 < e]
        # print("gaps",gaps)
        edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
        #print("edges",edges)
        return list(zip(edges, edges))
    except:
        print("Error while Grouping Index Range for defect")


def index_of_occurrences(arr, value):
    #print("arr....",arr)
    return [i for i, x in enumerate(arr) if x != 0 and x>0]
    #print("hdhhchfh",k)


def update_defect(type_of_defect, runid, defect_id):
    # print("hii")
    print(type_of_defect, runid)
    query = f'UPDATE defect SET  defect_type="{type_of_defect}" WHERE runid="{runid}" and id={defect_id}'
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()


def get_type_defect(geometrical_parameter, runid):
    print(geometrical_parameter, runid)
    with connection.cursor() as cursor:
        try:
            Fetch_defect_detail = "select length, breadth, id from defect where runid='%s'"
            # Execute query.
            cursor.execute(Fetch_defect_detail, (int(runid)))
            allSQLRows = cursor.fetchall()
            # print(allSQLRows)
            for i in allSQLRows:
                length_defect = i[0]
                width_defect = i[1]
                defect_id = i[2]
                # print("length of defect", length_defect)
                # print("width of defect", width_defect)
                L_ratio_W = length_defect / width_defect
                if width_defect > 3 * geometrical_parameter and length_defect > 3 * geometrical_parameter:
                    type_of_defect = 'GENERAL'
                elif (
                        6 * geometrical_parameter >= width_defect >= 1 * geometrical_parameter and 6 * geometrical_parameter >= length_defect >= 1 * geometrical_parameter) and (
                        0.5 < (L_ratio_W) < 2) and not (
                        width_defect >= 3 * geometrical_parameter and length_defect >= 3 * geometrical_parameter):
                    type_of_defect = 'PITTING'
                elif (1 * geometrical_parameter <= width_defect < 3 * geometrical_parameter) and (L_ratio_W >= 2):
                    type_of_defect = 'AXIAL GROOVING'
                elif L_ratio_W <= 0.5 and 3 * geometrical_parameter > length_defect >= 1 * geometrical_parameter:
                    type_of_defect = 'CIRCUMFERENTIAL GROOVING'
                elif 0 < width_defect < 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
                    type_of_defect = 'PINHOLE'
                elif 0 < width_defect < 1 * geometrical_parameter and length_defect >= 1 * geometrical_parameter:
                    type_of_defect = 'AXIAL SLOTTING'
                elif width_defect >= 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
                    type_of_defect = 'CIRCUMFERENTIAL SLOTTING'
                update_defect(type_of_defect, runid, defect_id)
        except:
            logger.log_error("type of defect is not permissiable value")


def extract_raw_defects(arr):
    print("array",arr)
    list_of_raw_defect = []
    temp_list = []
    for i, row in enumerate(arr):
        if len(row) > 0:
            temp_list.append(i)
        elif len(temp_list) > 0:
            list_of_raw_defect.append({"start": temp_list[0], "end": temp_list[-1]})
            temp_list = []
    # print("temp_list",temp_list)
    if len(temp_list) > 0:
        list_of_raw_defect.append({"start": temp_list[0], "end": temp_list[-1]})
        temp_list = []
    return list_of_raw_defect


def calculate_defect(raw_defects, pipe_data, number_of_sensor=18):  # TODO pass number of sensor
    start = raw_defects["start"]
    end = raw_defects["end"]
    sensor_index = []
    for i in range(number_of_sensor):
        flag = False
        for row in pipe_data[start:end + 1]:
            if (row[i] != 0 and row[i]>0):
                flag = True
                break
        if flag:
            sensor_index.append(i)
    defects = []
    print("sensor_index", sensor_index)
    index_list = ranges(sensor_index)
    for row in index_list:
        defects.append(
            {"start_observation": start, "end_observation": end, "start_sensor": row[0], "end_sensor": row[1]})
    return defects


def defect_length_calculator(data, defects, oddo1, oddo2, roll, df, Pipe_length):
    finial_defect_list = []
    for i, defect in enumerate(defects):
        start, end, start_sensor, end_sensor = defect["start_observation"], defect["end_observation"], defect[
            "start_sensor"], defect["end_sensor"]

        print(start,end,start_sensor,end_sensor)
        if start_sensor>end_sensor:
            pass
        else:
        ##################### choose ODD1  and ODD2 sensor #####################
            """Absolute Distance Calculation....."""
            absolute_length = oddo2[start]
            print("absolute_length", absolute_length)

            """Dent Length Calculation......."""
            length = oddo2[end] - oddo2[start]
            print("dent_length",length)

            """Upstream Calculation"""
            upstream=oddo2[end]-oddo2[0]
            print("upstreamn calculate...",upstream)

            """Width Calculation"""
            Width = Width_calculation(start_sensor, end_sensor)
            Width = round(Width)
            print("Width of Defect=>", Width)

            """ Dent Calculation......."""
            max_value_list, data_observation, data1, a, b = defect_max(data, start, end, start_sensor, end_sensor)
            #print("max_value_list",max_value_list)
            """
            First row get start observation to end observation
            """
            initial_observation_1 = [0 if k1 < 0 else k1 for k1 in data_observation[0]]
            #print("initial_observation...",initial_observation_1)

            """
            difference between max_value_list and initial_observation
            """
            zip_object = zip(max_value_list, initial_observation_1)
            difference_list = []
            for list1_i, list2_i in zip_object:
             difference_list.append(list1_i - list2_i)

            max_value_difference_value = max(difference_list)

            max_value_difference_index = difference_list.index(max_value_difference_value)
            print("max_value_index",max_value_difference_index)

            column_name=df.columns[max_value_difference_index]
            #print("column_name...",column_name)

            values_within_range = df.loc[start:end, column_name]
            #print("filtered_df....",values_within_range)

            min_value = values_within_range.min()
            max_value = values_within_range.max()
            #print("min_value.....",min_value)
            #print("max_value.....",max_value)
            max_value_get_row_index=values_within_range.index.max()
            #print("max_value_get_row_index.....", max_value_get_row_index)
            difference_value=max_value-min_value
            print("difference_value_max_value_and_base_value_each_sensor",difference_value)

            roll_position=roll[max_value_get_row_index]
            print("roll_position_index_value",roll_position)

            sensor_number=max_value_difference_index+1
            initial_calculation_of_each_sensor=(sensor_number-1)*20

            if roll_position > 0:
                roll_position = roll_position + initial_calculation_of_each_sensor
                if roll_position > 360:
                    roll_position = roll_position % 360
            else:
                roll_position = 360 + roll_position
                roll_position = roll_position + initial_calculation_of_each_sensor
                if roll_position > 360:
                    roll_position = roll_position % 360

            print('roll_position.....',roll_position)
            hr,min=degree_to_time(roll_position)
            g=':'
            angle_hr_min=str(hr)+g+str(min)
            print("Orientation....",angle_hr_min)

            finial_defect_list.append({**defect,"start_index":start,"end_index":end,"start_sensor":start_sensor,"end_sensor":end_sensor,"sensor_no":max_value_difference_index,
                                        "absolute_distance": absolute_length,"orientation": angle_hr_min,"WT":6.5,"length": int(length),"width":Width ,"depth_diff": difference_value,
                                       "upstream":upstream,"pipe_length":Pipe_length,"feature_identification":'Dent',"feature_type":'External'
                                       })  # TODO calculate breadth(same flapper or not)
    return (finial_defect_list)


def defect_angle_x(roll_x, sensor):
    roll_angle=list(roll_x)
    roll_position=roll_angle[0]
    print("roll_postion and sensor", roll_position, sensor)
    x = 2.52
    y = 2.4
    z = 3.41
    a = 11.75
    b = int(sensor / 16)
    c = b * a

    d = int(sensor / 8)
    e = d - b
    f = e * z

    g = int(sensor / 4)
    h = g - (b + e)
    i = h * y

    j = sensor * x
    # roll_position = 0.15
    initial_calculation_of_each_sensor = c + f + i + j
    print("a", initial_calculation_of_each_sensor)
    if roll_position > 0:
        # print(roll_position)
        roll_position = roll_position + initial_calculation_of_each_sensor
        if roll_position > 360:
            print(roll_position)
            roll_position = roll_position % 360
    else:
        roll_position = 360 + roll_position
        roll_position = roll_position + initial_calculation_of_each_sensor
        if roll_position > 360:
            roll_position = roll_position % 360
            angle = initial_calculation_of_each_sensor + roll_position
            print("angle rotation", angle)
            print("angle", roll_position)
    adsmd = roll_position / 30
    k = int(adsmd)
    m = int(roll_position % 30)
    g = ':'
    angle_hr_min = str(k) + g + str(m)
    return angle_hr_min


def Width_calculation(start_sensor1, end_sensor1):
    if start_sensor1 > end_sensor1:
        bredth = 0
        return bredth

    else:
        if start_sensor1 == end_sensor1:
            bredth = 16
            return bredth
        else:
            sensor=end_sensor1-start_sensor1
            breadth=sensor*32
            return breadth


def degree_to_time(degrees):
    # Convert degrees to hours
    hours = degrees // 30  # Each hour represents 30 degrees

    # Convert remaining degrees to minutes
    remaining_degrees = degrees % 30
    minutes = remaining_degrees / 0.5  # Each minute represents 0.5 degrees

    return int(hours), int(minutes)

def insert_defect_into_db(finial_defects, runid, pipe_id):
    # with connection.cursor() as cursor:
    #     a = cursor.execute("DELETE FROM dent WHERE  pipe_id=" + pipe_id + "")
    #     print(a)
    #     cursor.close()
    for i in finial_defects:
        start_index = i['start_index']
        end_index = i['end_index']
        start_sensor = i['start_sensor']
        end_sensor = i['end_sensor']
        sensor_no=i['sensor_no']
        absolute_distance = i['absolute_distance']
        orientation=i['orientation']
        WT=i['WT']
        length = i['length']
        width=i['width']
        depth_diff=i['depth_diff']
        upstream=i['upstream']
        pipe_length=i['pipe_length']
        feature_identification=i['feature_identification']
        feature_type=i['feature_type']
        with connection.cursor() as cursor:
            query_defect_insert = "INSERT INTO dent (runid,pipe_id,start_index,end_index,start_sensor,end_sensor,sensor_no,absolute_distance,orientation,WT,length,width,depth_diff,upstream,pipe_length,feature_identification,feature_type) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
            # print(runid, analytic_id, Sensitivity, start_file, end_file, start_sno, end_sno)

            cursor.execute(query_defect_insert, (
                int(runid), pipe_id, start_index, end_index, start_sensor, end_sensor,sensor_no,absolute_distance,orientation,WT, length,
                width, depth_diff, upstream, pipe_length,feature_identification,feature_type))

            connection.commit()


def defect_max(data, start, end, a, b):
    data_observation = []
    maximum_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    data1 = data[start:end]
    # df=pd.DataFrame(data1)

    # print(b)
    for row in data1:
        data_observation.append(row)
        for y, data2 in enumerate(row):
            ############# check data the range b/w start_sensor=a and end_sensor=b ############
            if y > a - 1 and y < b + 1:
                if abs(data2) >= maximum_value[y]:
                    maximum_value[y] = abs(data2)
    return (maximum_value, data_observation, data1,a,b)


def radar_patch(r, theta, centre):
    offset = 0.01
    yt = r * np.sin(theta)
    xt = r * np.cos(theta)
    print("x value", xt)
    print("y value", yt)
    return xt, yt


def get_defect_list_from_db(runid, pipe_id):
    # runid = self.runid
    # pipe_id = self.pipe_id
    defects = []
    with connection.cursor() as cursor:
        try:
            Fetch_weld_detail = "select * from dent where runid='%s' and pipe_id='%s'"
            # Execute query.
            cursor.execute(Fetch_weld_detail, (int(runid), int(pipe_id)))
            allSQLRows = cursor.fetchall()
            for row in allSQLRows:
                # print(row[3])
                defects.append([row[3], row[4], row[5], row[6]])
                # if row[11] == 'manual':
                #     self.reset_defect_pushButton.show()

            return defects
        except:
            logger.log_error("Error during fetching defects from db for runid = " + runid)
            return []


if __name__ == "__main__":
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # u1=QWebEngineView()
    sys.exit(app.exec_())
