import atexit; atexit.register(lambda: print('>>> Exiting main.py normally'))

import os
import re
import math
import json
from pywt import cwt
import shutil
import joblib
from scipy.interpolate import interp1d
import plotly.io as pio
import plotly.graph_objs as go
from kaleido.scopes import plotly

import plotly.offline
import seaborn as sns
from statistics import mean
from datetime import datetime, timedelta
from matplotlib.transforms import Bbox
from matplotlib.widgets import RectangleSelector
import numpy as np
import os.path
import matplotlib.patheffects as path_effects
from scipy.signal import savgol_filter, lfilter
from sklearn.preprocessing import MinMaxScaler
import pymysql
from PyQt5.QtCore import Qt, QUrl
import sys
#import WeldAndPipeLength
from extras import weld_update
from google.cloud import bigquery
import pandas as pd
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import GMFL_12_Inch_Desktop.Tabs.TAB_1_update_form.widgets.update_form as formComponent
import Components.graph as graph
import Components.style as Style
import Components.style1 as Style1
# import Components.logger as logger
import Components.CreateProject as CreateProject
import Components.endcounter_to_startcounter_distance as endcounter_to_startcounter_distance
import Components.AddWeld as AddWeld
# import Components.report_generator as Report
import warnings
warnings.filterwarnings('ignore')
websearch = config.xyz


from concurrent.futures import ProcessPoolExecutor
a = os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./utils/GCS_Auth.json"
Update_form_component = formComponent.UpdateForm()
connection = config.connection
company_list = []  # list of companies
credentials = config.credentials
project_id = config.project_id
client = bigquery.Client(credentials=credentials, project=project_id)
config = json.loads(open('./utils/proximity_base_value.json').read())
temp_defect = []

def func(a):
    print(a)
    query_for_start = 'SELECT * FROM ' + config.table_name + ' WHERE index>={} AND  index<={} order by index'
    query_job = client.query(query_for_start.format(a[0], a[1]))
    l1 = query_job.result().to_dataframe()
    return l1

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

        """
        Left Main GridLayout
        """
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 190, 1200))
        self.gridLayoutWidget.adjustSize()

        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setStyleSheet(Style1.list_grid_style)
        self.main_left = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.main_left.setContentsMargins(0, 0, 0, 0)
        self.main_left.setObjectName("main_left")

        """
        Left Main GridLayout add button Load data
        """
        self.load_list_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.load_list_pushButton.setObjectName("load_list_pushButton")
        self.load_list_pushButton.clicked.connect(self.load_list)
        self.main_left.addWidget(self.load_list_pushButton, 0, 0, 1, 1)

        """
        Left Main GridLayout add ListItems
        """
        self.left_listWidget = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.left_listWidget.setObjectName("left_listWidget")

        """
        Call the list_clicked function
        """
        self.left_listWidget.itemDoubleClicked.connect(self.list_clicked)
        self.left_listWidget.itemClicked.connect(self.get_project_name)
        self.main_left.addWidget(self.left_listWidget, 2, 0, 1, 1)
        self.add_to_list()

        """
        Right Main GridLayout
        """
        self.init_gridLayoutWidget_2()
        MainWindow.setCentralWidget(self.centralwidget)

        """
        Menubar Buttons
        """
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("File")
        self.menubar.setStyleSheet(Style.menubar)
        self.menuFile = QtWidgets.QMenu(self.menubar)
        MainWindow.setMenuBar(self.menubar)
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuSearch = QtWidgets.QMenu(self.menubar)
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuhelp = QtWidgets.QMenu(self.menubar)

        """
        Add Create Project in the file menubar
        """
        self.actionCreate_Project = QtWidgets.QAction(MainWindow)
        self.actionCreate_Project.setObjectName("actionCreate_Project")
        self.menuFile.addAction(self.actionCreate_Project)

        """
        Length Calculation b/w startcounter to endcounter 
        """
        self.distance = QtWidgets.QAction(MainWindow)
        self.distance.setObjectName("Distance")
        self.menuFile.addAction(self.distance)

        """
        Type of defect add in view menubar
        """
        self.actiontypeofdefect = QtWidgets.QAction(MainWindow)
        self.actiontypeofdefect.setObjectName("Defect Type")
        self.menuView.addAction(self.actiontypeofdefect)

        """
        Add weld Manually
        """
        self.addweld = QtWidgets.QAction(MainWindow)
        self.addweld.setObjectName("Add Manual Weld")
        self.menuView.addAction(self.addweld)

        """
        Create Pipe
        """
        self.create_pipe = QtWidgets.QAction(MainWindow)
        self.create_pipe.setObjectName("Pipe Create")
        self.menuView.addAction(self.create_pipe)

        """
        Update Defect
        """
        self.Update_defect = QtWidgets.QAction(MainWindow)
        self.Update_defect.setObjectName("Update Defect")
        self.menuView.addAction(self.Update_defect)

        """
        Erf Calculation
        """
        self.erf = QtWidgets.QAction(MainWindow)
        self.erf.setObjectName("Erf Calculation")
        self.menuView.addAction(self.erf)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSearch.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuhelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def get_project_name(self, item):
        """
        This function takes one parameter
        param item:Get the project name
        """
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
        self.go_back_button.setStyleSheet(Style.btn_type_primary)
        self.go_back_button.setText("Go Back")
        self.main_right.addWidget(self.go_back_button, 2, 0)
        self.go_back_button.clicked.connect(self.reset_default_screen)

    """
    Initialize the right tabwidget inside the Right Main GridLayout
    """
    def init_tab(self):
        self.right_tabWidget = QtWidgets.QTabWidget(self.gridLayoutWidget_2)
        self.right_tabWidget.setObjectName("right_tabWidget")

        self.tab_update = QtWidgets.QWidget()
        self.tab_update.setObjectName("tab")

        """
        Call the function init_update_form
        """
        self.tab_update.layout = QtWidgets.QVBoxLayout(self.tab_update)
        self.tab_update.setStyleSheet(Style.tab_update)
        Update_form_component._init_form_layout(self.tab_update, self.tab_update.layout)

        """
        Right tabwidget add tab,tab_2,tab_3,tab_4,tab_5
        """
        self.right_tabWidget.addTab(self.tab_update, "")
        self.right_tabWidget.setStyleSheet(Style.right_tabWidget)

        self.tab_weld_selection = QtWidgets.QWidget()
        self.tab_weld_selection.setObjectName("tab_2")

        self.tab_showData = QtWidgets.QWidget()
        self.tab_showData.setObjectName("tab_3")

        self.tab_line1 = QtWidgets.QWidget()
        self.tab_line1.setObjectName("tab_4")

        self.tab_line_orientation = QtWidgets.QWidget()
        self.tab_line_orientation.setObjectName("tab_5")

        self.tab_visualize = QtWidgets.QWidget()
        self.tab_visualize.setObjectName("tab_6")

        self.continue_heatmap_tab = QtWidgets.QWidget()
        self.continue_heatmap_tab.setObjectName("tab_7")

        self.Graph1 = QtWidgets.QWidget()
        self.Graph1.setObjectName("tab_8")

        self.tab_Pipe = QtWidgets.QWidget()
        self.tab_Pipe.setObjectName("tab_9")

        # self.tab_Pipe=QtWidgets.QWidget()
        # self.tab_Pipe.setObjectName("tab_8")
        #
        # self.tab_Analysis = QtWidgets.QWidget()
        # self.tab_Analysis.setObjectName("tab_9")

        """
        Here tab 2 weld selection
        """

        self.hb15 = QtWidgets.QHBoxLayout(self.tab_weld_selection)
        self.vb15 = QtWidgets.QVBoxLayout()
        self.figure_x15 = plt.figure(figsize=(25, 8))
        self.canvas_x15 = FigureCanvas(self.figure_x15)
        self.toolbar_x15 = NavigationToolbar(self.canvas_x15, self)
        self.start15 = QtWidgets.QLineEdit()
        self.end15 = QtWidgets.QLineEdit()
        self.button_x15 = QtWidgets.QPushButton('Weld Selection')
        self.button_x15.resize(50, 50)
        self.hb15.addLayout(self.vb15, 75)
        self.hbox_15 = QtWidgets.QHBoxLayout()
        self.hbox_16 = QtWidgets.QHBoxLayout()
        self.vb15.addLayout(self.hbox_15)
        self.vb15.addLayout(self.hbox_16)
        self.hbox_15.addWidget(self.toolbar_x15)
        self.hbox_15.addWidget(self.start15)
        self.hbox_15.addWidget(self.end15)
        self.button_x15.clicked.connect(self.weld_selection)
        self.button_x15.setStyleSheet(Style.btn_type_primary)
        self.hbox_15.addWidget(self.button_x15)
        self.hbox_16.addWidget(self.canvas_x15)
        self.setLayout(self.hbox_15)
        """
        End of the tab 2
        """

        """
        Start from here third tab content for create_weld
        Table Widget within the third tab for create_weld information
        """
        self.tab_showData.layout = QtWidgets.QVBoxLayout()
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

        """
        Weld button located inside the third tab
        """
        self.ShowWeld = QtWidgets.QPushButton()
        self.ShowWeld.setGeometry(QtCore.QRect(690, 265, 160, 43))
        self.ShowWeld.setObjectName("Fetch Data")
        self.ShowWeld.setText("Fetch Weld Details")
        """
        Call the function show_weld
        """
        self.ShowWeld.clicked.connect(self.Show_Weld)
        self.ShowWeld.setStyleSheet(Style.btn_type_primary)

        """
        Create Weld button located inside the third tab
        """

        self.create_weld = QtWidgets.QPushButton()
        self.create_weld.setGeometry(QtCore.QRect(480, 265, 180, 43))
        self.create_weld.setObjectName("Create Weld Data")
        self.create_weld.setText("Create Weld and Pipe")

        """
        Call the function CreateWeld
        """
        self.create_weld.clicked.connect(self.CreateWeld)
        self.create_weld.setStyleSheet(Style.btn_type_primary)

        """
        Third tab end here
        """


        """
        Here the Third content for the Weld_to_Pipe
        """
        """
        Table widget located within the third tab for weld_to_pipe information
        """

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

        """
        Show weld to pipe button within the third tab
        """
        self.Show_Weld_to_Pipe = QtWidgets.QPushButton()
        self.Show_Weld_to_Pipe.setGeometry(QtCore.QRect(600, 550, 160, 43))
        self.Show_Weld_to_Pipe.setObjectName("Fetch Data")
        self.Show_Weld_to_Pipe.setText("Fetch Weld To Pipe")

        """
        Call the function Show Weld to Pipe
        """
        self.Show_Weld_to_Pipe.clicked.connect(self.ShowWeldToPipe)
        self.Show_Weld_to_Pipe.setStyleSheet(Style.btn_type_primary)

        """
        Table widget within the third tab for defect list information
        """
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
            ['defect_id', 'runid', 'start_observation', 'end_observation', 'start_sensor', 'end_sensor', 'angle', 'length', 'breadth', 'depth', 'type'])

        """
        Show Weld to Pipe button within the  third tab
        """
        self.Show_Defect_list = QtWidgets.QPushButton()
        self.Show_Defect_list.setGeometry(QtCore.QRect(800, 840, 160, 43))
        self.Show_Defect_list.setObjectName("Fetch Data")
        self.Show_Defect_list.setText("Fetch Defect List")

        """
        Call the function Show DefectList
        """
        self.Show_Defect_list.clicked.connect(self.DefectList)
        self.Show_Defect_list.setStyleSheet(Style.btn_type_primary)
        self.tab_showData.layout.addWidget(self.myTableWidget)
        self.tab_showData.layout.addWidget(self.ShowWeld)
        self.tab_showData.layout.addWidget(self.create_weld)
        self.tab_showData.layout.addWidget(self.myTableWidget1)
        self.tab_showData.layout.addWidget(self.Show_Weld_to_Pipe)
        self.tab_showData.layout.addWidget(self.myTableWidget2)
        self.tab_showData.layout.addWidget(self.Show_Defect_list)
        self.tab_showData.setLayout(self.tab_showData.layout)

        """
        Line Plotting Within the fourth tab
        """
        self.hb5 = QtWidgets.QHBoxLayout(self.tab_line1)
        self.vb5 = QtWidgets.QVBoxLayout()
        self.figure_x5 = plt.figure(figsize=(25, 8))
        self.canvas_x5 = FigureCanvas(self.figure_x5)
        self.toolbar_x5 = NavigationToolbar(self.canvas_x5, self)
        # self.start = QtWidgets.QLineEdit()
        # self.end = QtWidgets.QLineEdit()
        self.combo = QtWidgets.QComboBox()
        # self.combo.setStyleSheet(Style.btn_type_primary)
        self.combo.setObjectName("Pipe_id")
        self.combo.setCurrentText("pipe_id")
        self.reset_btn = QtWidgets.QPushButton('Reset')
        self.reset_btn.clicked.connect(self.reset_btn_fun)

        self.latitude = QtWidgets.QLineEdit()
        self.latitude.setFixedWidth(100)
        self.logitude = QtWidgets.QLineEdit()
        self.logitude.setFixedWidth(100)

        self.selection_mark_lat_long = QtWidgets.QPushButton()
        self.selection_mark_lat_long.setText("Mark Lat Long")
        self.selection_mark_lat_long.clicked.connect(self.mark_lat_long)

        self.selection_mark_base_value = QtWidgets.QPushButton()
        self.selection_mark_base_value.setText("Mark Base Value")
        self.selection_mark_base_value.clicked.connect(self.basevalue)

        self.feature_selection = QtWidgets.QPushButton()
        self.feature_selection.setText("Mark Feature")
        self.feature_selection.clicked.connect(self.feature_selection_func)

        self.rect_start_1 = None  # Store the starting point of the rectangle
        self.rect_end_1 = None

        self.button_x5 = QtWidgets.QPushButton('Line Chart')
        self.button_x5.clicked.connect(self.Line_chart1)
        # self.button_x5.setStyleSheet(Style.btn_type_primary)
        self.button_x5.resize(50, 50)

        self.next_btn_lc = QtWidgets.QPushButton('Next')
        self.next_btn_lc.setStyleSheet("background-color: white; color: black;")
        self.next_btn_lc.clicked.connect(self.Line_chart1_next)

        self.prev_btn_lc = QtWidgets.QPushButton('Previous')
        self.prev_btn_lc.setStyleSheet("background-color: white; color: black;")
        self.prev_btn_lc.clicked.connect(self.Line_chart1_previous)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.prev_btn_lc)
        button_layout.addStretch(1)  # Adds a stretchable space between buttons
        button_layout.addWidget(self.next_btn_lc)

        self.m_output_proxi = QtWebEngineWidgets.QWebEngineView(self)

        self.hb5.addLayout(self.vb5, 75)

        self.hbox_5 = QtWidgets.QHBoxLayout()
        self.hbox_6 = QtWidgets.QHBoxLayout()
        self.hbox_7 = QtWidgets.QHBoxLayout()

        self.vb5.addLayout(self.hbox_5)
        self.vb5.addLayout(self.hbox_6, 60)
        self.vb5.addLayout(self.hbox_7, 40)
        self.hbox_7.addWidget(self.m_output_proxi)

        button_layout_widget = QtWidgets.QWidget()
        # button_layout_widget.setStyleSheet("background-color: white;")
        button_layout_widget.setLayout(button_layout)
        self.vb5.addWidget(button_layout_widget)

        self.hbox_5.addWidget(self.toolbar_x5)
        self.hbox_5.addWidget(self.combo)
        self.hbox_5.addWidget(self.button_x5)

        self.hbox_5.addWidget(self.latitude)
        self.hbox_5.addWidget(self.logitude)
        self.hbox_5.addWidget(self.selection_mark_lat_long)
        self.hbox_5.addWidget(self.selection_mark_base_value)
        self.hbox_5.addWidget(self.feature_selection)
        self.hbox_5.addWidget(self.reset_btn)

        self.hbox_6.addWidget(self.canvas_x5)

        self.setLayout(self.hbox_5)

        """
------->Here end of fourth tab
        """


        """
 ------->Start from here fifth Tab Line Plot (Absolute Distance vs Orienatation)
        """
        self.hb_orientation = QtWidgets.QHBoxLayout(self.tab_line_orientation)
        self.vb_orientation = QtWidgets.QVBoxLayout()

        self.figure_x_orientation = plt.figure(figsize=(25, 8))

        self.canvas_x_orientation = FigureCanvas(self.figure_x_orientation)

        self.toolbar_x_orientation = NavigationToolbar(self.canvas_x_orientation, self)

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

        self.button_x5_orienatation = QtWidgets.QPushButton('Line Chart 2')
        self.button_x5_orienatation.resize(50, 50)
        self.button_x5_orienatation.clicked.connect(self.Line_chart_orientation)

        self.next_btn_lc_orienatation = QtWidgets.QPushButton('Next')
        self.next_btn_lc_orienatation.setStyleSheet("background-color: white; color: black;")
        self.next_btn_lc_orienatation.clicked.connect(self.Line_chart_orientation_next)

        self.prev_btn_lc_orienatation = QtWidgets.QPushButton('Previous')
        self.prev_btn_lc_orienatation.setStyleSheet("background-color: white; color: black;")
        self.prev_btn_lc_orienatation.clicked.connect(self.Line_chart_orientation_previous)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.prev_btn_lc_orienatation)
        button_layout.addStretch(1)  # Adds a stretchable space between buttons
        button_layout.addWidget(self.next_btn_lc_orienatation)

        self.hb_orientation.addLayout(self.vb_orientation, 75)

        self.hbox_5_orientation = QtWidgets.QHBoxLayout()
        self.hbox_6_orientation = QtWidgets.QHBoxLayout()
        self.hbox_7_orientation = QtWidgets.QHBoxLayout()

        self.vb_orientation.addLayout(self.hbox_5_orientation)
        self.vb_orientation.addLayout(self.hbox_6_orientation)
        self.vb_orientation.addLayout(self.hbox_7_orientation)

        button_layout_widget = QtWidgets.QWidget()
        # button_layout_widget.setStyleSheet("background-color: white;")
        button_layout_widget.setLayout(button_layout)
        button_layout_widget.setFixedHeight(50)  # Adjust this value as required
        self.vb_orientation.addWidget(button_layout_widget)

        self.hbox_5_orientation.addWidget(self.toolbar_x_orientation)
        self.hbox_5_orientation.addWidget(self.combo_orientation)
        # self.hbox_5_orientation.addWidget(self.lower_Sensitivity_combo_box_orientation)
        # self.hbox_5_orientation.addWidget(self.upper_Sensitivity_combo_box_orientation)
        self.hbox_5_orientation.addWidget(self.button_x5_orienatation)

        self.hbox_6_orientation.addWidget(self.m_output_orientation)
        self.setLayout(self.hbox_5_orientation)

        """
        End from here Fifth Tab
        """


        """
 ------->Start From here six tab (Pipe Visualization..)
        """
        self.hbox = QtWidgets.QHBoxLayout(self.tab_visualize)
        self.vbox = QtWidgets.QVBoxLayout()

        self.figure = plt.figure(figsize=(20, 6))

        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)

        self.reset_pushButton = QtWidgets.QPushButton("Reset")
        self.reset_pushButton.clicked.connect(self.reset_btn_fun_pipe)
        # self.reset_defect_pushButton.hide()

        self.All_box_selection = QtWidgets.QPushButton("Box_selection")
        self.All_box_selection.clicked.connect(self.box_selection_all_defect)

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
        self.Analaysis_pushButton.clicked.connect(self.pre_graph_analysis)

        """
        Generate button inside the fifth tab
        """
        self.generatepushButton = QtWidgets.QPushButton("Generate Report")
        self.generatepushButton.clicked.connect(self.generate_report)

        self.next_btn_pre = QtWidgets.QPushButton('Next')
        self.next_btn_pre.setStyleSheet("background-color: white; color: black;")
        self.next_btn_pre.clicked.connect(self.graph_analysis_next)

        self.prev_btn_pre = QtWidgets.QPushButton('Previous')
        self.prev_btn_pre.setStyleSheet("background-color: white; color: black;")
        self.prev_btn_pre.clicked.connect(self.graph_analysis_previous)

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

        self.setLayout(self.hbox_8)

        """
 ------->End from here six tab .........................
        """


        """
 ------->Start from here seven tab (Orientation Heatmap)......................
        """
        self.hbox_con_hm = QtWidgets.QHBoxLayout(self.continue_heatmap_tab)
        self.vbox_con_hm = QtWidgets.QVBoxLayout()

        self.m_output = QtWebEngineWidgets.QWebEngineView(self)

        # self.figure_tab9 = plt.figure()

        self.figure_tab9 = plt.figure(figsize=(20, 6))
        self.canvas_tab9 = FigureCanvas(self.figure_tab9)
        self.toolbar_tab9 = NavigationToolbar(self.canvas_tab9, self)

        self.reset_btn_tab9 = QtWidgets.QPushButton("Reset")
        self.reset_btn_tab9.clicked.connect(self.reset_btn_fun_chm)
        self.reset_btn_tab9.setVisible(False)  # Initially hidden

        self.all_box_selection1 = QtWidgets.QPushButton("Defect Selection")
        self.all_box_selection1.clicked.connect(self.all_box_selection_ori_heatmap)
        self.all_box_selection1.setVisible(False)  # Initially hidden

        self.combo_tab9 = QComboBox()

        # """
        # Lower_Sensitivity in combo_box inside the fifth tab
        # """
        # lowerSensitivity_list_tab9 = ['0', '0.70', '0.99', '-1', '-1.5', '-2', '-2.5', '-3.5', '-4', '0.98', '0.95']
        # # lowerSensitivity_list_tab9 = ['0', '0.71']
        # self.lower_Sensitivity_combo_box_tab9 = QComboBox()
        # self.lower_Sensitivity_combo_box_tab9.addItems(lowerSensitivity_list_tab9)
        #
        # """
        # upper_Sensitivity in combo_box inside the fifth tab
        # """
        # upperSensitivity_list_tab9 = ['0.42', '1.01', '1.02', '1.03', '1.04', '1.05', '1.06', '1.07', '1.08', '1.09',
        #                               '1.10',
        #                               '1.11', '1.14', '1.16', '1.18', '1.20', '1.25', '1.30', '1.35', '1.40', '1.45',
        #                               '1.50']

        # upperSensitivity_list_tab9 = ['0', '1.02','1.05', '1.08', '1.12', '1.15']
        # self.upper_Sensitivity_combo_box_tab9 = QComboBox()
        # # self.upper_Sensitivity_combo_box.setFixedSize(120, 35)
        # self.upper_Sensitivity_combo_box_tab9.addItems(upperSensitivity_list_tab9)

        self.Analaysis_btn_tab9 = QtWidgets.QPushButton("Analysis")
        self.Analaysis_btn_tab9.clicked.connect(self.tab9_heatmap)

        self.next_btn_hm = QtWidgets.QPushButton('Next')
        self.next_btn_hm.setStyleSheet("background-color: white; color: black;")
        self.next_btn_hm.clicked.connect(self.tab9_heatmap_next)

        self.prev_btn_hm = QtWidgets.QPushButton('Previous')
        self.prev_btn_hm.setStyleSheet("background-color: white; color: black;")
        self.prev_btn_hm.clicked.connect(self.tab9_heatmap_previous)

        self.export_btn_hm = QtWidgets.QPushButton('Export Sheet')
        self.export_btn_hm.setStyleSheet("background-color: white; color: black;")
        self.export_btn_hm.clicked.connect(self.export_to_excel)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.prev_btn_hm)  # Left button
        button_layout.addStretch(1)  # Stretch to push buttons apart
        button_layout.addWidget(self.export_btn_hm)  # Center button
        button_layout.addStretch(1)  # Stretch to push buttons apart
        button_layout.addWidget(self.next_btn_hm)  # Right button

        self.myTableWidget_tab9 = QtWidgets.QTableWidget()
        self.myTableWidget_tab9.setGeometry(QtCore.QRect(30, 600, 1300, 235))
        self.myTableWidget_tab9.setRowCount(30)
        self.myTableWidget_tab9.setColumnCount(11)
        self.myTableWidget_tab9.setColumnWidth(0, 160)
        self.myTableWidget_tab9.setColumnWidth(1, 160)
        self.myTableWidget_tab9.setColumnWidth(2, 160)
        self.myTableWidget_tab9.setColumnWidth(3, 160)
        self.myTableWidget_tab9.setColumnWidth(4, 160)
        self.myTableWidget_tab9.setColumnWidth(5, 160)
        self.myTableWidget_tab9.setColumnWidth(6, 160)
        self.myTableWidget_tab9.setColumnWidth(7, 160)
        self.myTableWidget_tab9.setColumnWidth(8, 160)
        self.myTableWidget_tab9.setColumnWidth(9, 160)
        self.myTableWidget_tab9.setColumnWidth(10, 160)
        self.myTableWidget_tab9.horizontalHeader().setStretchLastSection(True)
        self.myTableWidget_tab9.setHorizontalHeaderLabels(
            ['Defect_id', 'Pipe_id', 'WT(mm)', 'Absolute_distance(m)', 'Distance_to_Upstream(m)', 'Feature_type',
             'Dimensions_classification', 'Orientation_clock(hr:min)', 'Length(mm)', 'Width(mm)', 'Depth(%)'])
        # **Make the table read-only**
        self.myTableWidget_tab9.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.hbox_con_hm.addLayout(self.vbox_con_hm)

        self.hbox_con_hm_1 = QtWidgets.QHBoxLayout()
        self.hbox_con_hm_2 = QtWidgets.QHBoxLayout()
        self.hbox_con_hm_3 = QtWidgets.QHBoxLayout()
        self.vbox_con_hm.addLayout(self.hbox_con_hm_1, 10)
        self.vbox_con_hm.addLayout(self.hbox_con_hm_2, 70)
        self.vbox_con_hm.addLayout(self.hbox_con_hm_3, 20)

        button_layout_widget = QtWidgets.QWidget()
        # button_layout_widget.setStyleSheet("background-color: white;")
        button_layout_widget.setLayout(button_layout)
        # Add the button layout widget to the canvas layout
        self.vbox_con_hm.addWidget(button_layout_widget)

        self.hbox_con_hm_1.addWidget(self.toolbar_tab9)
        self.hbox_con_hm_1.addWidget(self.combo_tab9)
        # self.hbox_con_hm_1.addWidget(self.lower_Sensitivity_combo_box_tab9)
        # self.hbox_con_hm_1.addWidget(self.upper_Sensitivity_combo_box_tab9)
        self.hbox_con_hm_1.addWidget(self.Analaysis_btn_tab9)
        self.hbox_con_hm_1.addWidget(self.all_box_selection1)
        self.hbox_con_hm_1.addWidget(self.reset_btn_tab9)
        self.hbox_con_hm_2.addWidget(self.canvas_tab9)

        self.hbox_con_hm_2.addWidget(self.m_output)
        self.hbox_con_hm_3.addWidget(self.myTableWidget_tab9)
        self.setLayout(self.hbox_con_hm_1)

        # Initially set both widgets to be hidden
        self.canvas_tab9.setVisible(False)
        self.m_output.setVisible(False)

        """
 ------->End from here tab seven Orienatation Heatmap
        """

        """
------->Start from here Eight Tab Line Plot (Magnetization Plot and Velocity Plot)
        """
        self.hb_graph = QtWidgets.QHBoxLayout(self.Graph1)
        self.vb_graph = QtWidgets.QVBoxLayout()

        self.figure_x_graph = plt.figure(figsize=(25, 8))

        self.canvas_x_graph = FigureCanvas(self.figure_x_graph)

        self.toolbar_x_graph = NavigationToolbar(self.canvas_x_graph, self)

        self.m_output_graph = QtWebEngineWidgets.QWebEngineView(self)  # Single WebEngineView

        self.combo_graph = QtWidgets.QComboBox()

        self.combo_graph.setObjectName("Pipe_id")
        self.combo_graph.setCurrentText("Pipe_id")

        self.button_x5_mgraph = QtWidgets.QPushButton('Magnetization')
        self.button_x5_mgraph.resize(50, 50)
        self.button_x5_mgraph.clicked.connect(self.Magnetization)

        self.button_x5_vgraph = QtWidgets.QPushButton('Velocity')
        self.button_x5_vgraph.resize(50, 50)
        self.button_x5_vgraph.clicked.connect(self.Velocity)

        self.button_x5_tgraph = QtWidgets.QPushButton('Temperature')
        self.button_x5_tgraph.resize(50, 50)
        self.button_x5_tgraph.clicked.connect(self.Temperature_profile)

        self.button_x5_slgraph = QtWidgets.QPushButton('Sensor Loss')
        self.button_x5_slgraph.resize(50, 50)
        self.button_x5_slgraph.clicked.connect(self.Sensor_loss)

        self.hb_graph.addLayout(self.vb_graph, 75)

        self.hbox_5_graph = QtWidgets.QHBoxLayout()
        self.hbox_6_graph = QtWidgets.QHBoxLayout()
        # self.hbox_7_graph = QtWidgets.QHBoxLayout()

        self.vb_graph.addLayout(self.hbox_5_graph, 20)
        self.vb_graph.addLayout(self.hbox_6_graph, 40)
        # self.vb_graph.addLayout(self.hbox_7_graph, 40)

        self.hbox_5_graph.addWidget(self.toolbar_x_graph)
        self.hbox_5_graph.addWidget(self.combo_graph)
        self.hbox_5_graph.addWidget(self.button_x5_mgraph)
        self.hbox_5_graph.addWidget(self.button_x5_vgraph)
        self.hbox_5_graph.addWidget(self.button_x5_slgraph)
        # self.hbox_5_graph.addWidget(self.button_x5_tgraph)

        self.hbox_6_graph.addWidget(self.m_output_graph)

        # self.hbox_6_graph.addWidget(self.m_output_m)
        # self.hbox_7_graph.addWidget(self.m_output_v)
        self.setLayout(self.hbox_5_graph)

        """
 ------->End from here eight Tab
        """

        """
 ------->Start from here Nine tab for Feature Selection (Line Chart)
        """
        self.horizonatal = QtWidgets.QHBoxLayout(self.tab_Pipe)
        self.vertical = QtWidgets.QVBoxLayout()
        # self.web_view = websearch()
        # print("Websearch....", self.web_view)
        self.figure_image = plt.figure(figsize=(25, 8))
        self.canvas_image = FigureCanvas(self.figure_image)
        self.toolbar_menu = NavigationToolbar(self.canvas_image, self)

        self.button_line = QtWidgets.QPushButton('Line Chart 2')
        # self.button_line.clicked.connect(self.Line_chart2)
        # self.button_line.resize(50, 50)

        self.reset_btn_feature = QtWidgets.QPushButton('Reset')
        # self.reset_btn_feature.clicked.connect(self.reset_btn_feature_fun)

        self.combo_box1 = QtWidgets.QComboBox()

        self.horizonatal.addLayout(self.vertical, 75)
        self.hbox_up1 = QtWidgets.QHBoxLayout()
        self.hbox_up2 = QtWidgets.QHBoxLayout()

        self.vertical.addLayout(self.hbox_up1)
        self.vertical.addLayout(self.hbox_up2)

        self.hbox_up1.addWidget(self.toolbar_menu)
        self.hbox_up1.addWidget(self.combo_box1)

        self.hbox_up1.addWidget(self.button_line)
        self.hbox_up1.addWidget(self.reset_btn_feature)

        self.hbox_up2.addWidget(self.canvas_image)
        self.setLayout(self.hbox_up2)

        self.is_drawing_rect = False
        self.rect_start = None  # Store the starting point of the rectangle
        self.rect_end = None  # Store the ending point of the rectangle

        """
 ------->End from here Nine tab ()
        """

        self.right_tabWidget.addTab(self.tab_weld_selection, "")
        self.right_tabWidget.addTab(self.tab_showData, "")
        self.right_tabWidget.addTab(self.tab_line1, "")
        self.right_tabWidget.addTab(self.tab_line_orientation, "")
        self.right_tabWidget.addTab(self.tab_visualize, "")
        self.right_tabWidget.addTab(self.continue_heatmap_tab, "")
        self.right_tabWidget.addTab(self.Graph1, "")
        # self.right_tabWidget.addTab(self.tab_Pipe, "")
        self.main_right.addWidget(self.right_tabWidget, 1, 0, 1, 1)


    def list_clicked(self, a):
        """
        When the load button is clicked ,the list items are loaded
        """
        self.full_screen()
        self.project_name = a.text()
        print(self.project_name)

        self.init_tab()
        self.runid = Update_form_component.set_previous_form_data(a.text())

        """
        Right Tab Widget set tab text
        """
        self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_update), "Update")
        self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_weld_selection), "Weld Selection")
        self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_showData), "Table Data Show")
        self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_line1), "Line Plot (Counter v/s Sensor)")
        self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_line_orientation), "Line Plot(Absolute v/s Orienatation)")
        self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_visualize), "Pipe Visualization (Heatmap)")
        self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.continue_heatmap_tab), "Heatmap(Absolute v/s Orienatation)")
        self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.Graph1), "Graph")
        # self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_Pipe), "Feature Selection")
        # self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_Analysis), "Data Analysis")


    """
----->Weld Selection tab(2) all functions starts from here
    """

    def select_weld(self, eclick, erelease):
        runid = self.runid
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        start_index15 = round(x1)
        end_index15 = round(x2)
        print(start_index15, end_index15)
        query_for_start = 'SELECT ODDO1,ODDO2 FROM ' + config.table_name + ' WHERE index>{} AND index<{} AND runid={} order by index'
        query_job = client.query(query_for_start.format(int(start_index15), int(end_index15), runid))
        results = query_job.result()
        print(results)
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

        # if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
        #     print("start_index15: ", start_index15)
        #     print("end_index15: ", end_index15)
        #     QMessageBox.about(self, 'Sucess', 'Data Saved Successfully')
        #     self.hide()
        # else:
        #     print("data is not inserted successfully")
        #     QMessageBox.warning(self, 'Invalid', 'Please select again')

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
                runid, analytic_id, sensitivity, start_index15, end_index15, type, start_oddo1, end_oddo1,
                start_oddo2, end_oddo2, weld_length)

            # Execute query.
            b = cursor.execute(query_weld_insert)
            connection.commit()
            if b:
                QMessageBox.about(self, 'Insert', 'Data Inserted Successfully')
                self.hide()
            else:
                print("data is not inserted successfully")

        # print(start_index15)
        # print(end_index15)

    """
    The line plot includes the selection of the weld.
    """
    def weld_selection(self):
        runid = self.runid
        start15 = int(self.start15.text())
        end15 = int(self.end15.text())
        print(start15, end15)
        """
        Old Code
        """
        # query_for_start = 'SELECT * FROM ' + Config.table_name + ' WHERE index>{} AND index<{} AND runid={} order by index'
        # query_job = client.query(query_for_start.format(start15, end15, runid))
        # df_plot_data1 = query_job.result().to_dataframe()
        # print(df_plot_data1)
        """
        New Code
        """
        future = []
        config.print_with_time("Start_time")
        executor = ProcessPoolExecutor(10)
        x = 20000
        while start15 < end15:
            future.append(executor.submit(func, [start15 + 1, start15 + x]))
            # print(start_index + 1, " ", start_index + x)
            start15 = start15 + x

        d1 = []
        for x in future:
            df = x.result()
            d1.append(df)

        df_plot_data1 = pd.concat(d1)

        index = df_plot_data1['index']
        self.figure_x15.clear()
        self.ax15 = self.figure_x15.add_subplot(111)

        # discards the old graph
        self.ax15.clear()
        res = ['F1H1', 'F1H2', 'F1H3', 'F1H4', 'F2H1', 'F2H2', 'F2H3', 'F2H4',
               'F3H1', 'F3H2', 'F3H3', 'F3H4', 'F4H1', 'F4H2', 'F4H3',
               'F4H4', 'F5H1', 'F5H2', 'F5H3', 'F5H4', 'F6H1', 'F6H2', 'F6H3', 'F6H4',
               'F7H1', 'F7H2', 'F7H3', 'F7H4', 'F8H1', 'F8H2', 'F8H3', 'F8H4', 'F9H1', 'F9H2', 'F9H3', 'F9H4', 'F10H1',
               'F10H2', 'F10H3', 'F10H4',
               'F11H1', 'F11H2', 'F11H3', 'F11H4', 'F12H1', 'F12H2', 'F12H3', 'F12H4', 'F13H1', 'F13H2', 'F13H3',
               'F13H4', 'F14H1', 'F14H2', 'F14H3', 'F14H4',
               'F15H1', 'F15H2', 'F15H3', 'F15H4', 'F16H1', 'F16H2', 'F16H3', 'F16H4', 'F17H1', 'F17H2', 'F17H3',
               'F17H4', 'F18H1', 'F18H2', 'F18H3', 'F18H4',
               'F19H1', 'F19H2', 'F19H3', 'F19H4', 'F20H1', 'F20H2', 'F20H3', 'F20H4', 'F21H1', 'F21H2', 'F21H3',
               'F21H4', 'F22H1', 'F22H2', 'F22H3', 'F22H4',
               'F23H1', 'F23H2', 'F23H3', 'F23H4', 'F24H1', 'F24H2', 'F24H3', 'F24H4',
               "F25H1", "F25H2", "F25H3", "F25H4", "F26H1", "F26H2", "F26H3",
               "F26H4", "F27H1", "F27H2", "F27H3", "F27H4", "F28H1", "F28H2", "F28H3",
               "F28H4", "F29H1", "F29H2", "F29H3", "F29H4", "F30H1", "F30H2", "F30H3",
               "F30H4",  "F31H1", "F31H2", "F31H3", "F31H4", "F32H1", "F32H2", "F32H3",
               "F32H4", "F33H1", "F33H2", "F33H3", "F33H4", "F34H1", "F34H2", "F34H3",
               "F34H4", "F35H1", "F35H2", "F35H3", "F35H4", "F36H1", "F36H2", "F36H3", "F36H4"]
        self.a2 = []
        for i, data in enumerate(res):
            self.ax15.plot(index, (df_plot_data1[data] + i * 1400).to_numpy(), label=i)
            self.a2.append(df_plot_data1[data] + i * 1400)
        self.ax15.set_ylabel('Hall Sensor')
        self.canvas_x15.draw()
        config.print_with_time("End_time")
        rs2 = RectangleSelector(self.ax15, self.select_weld, useblit=True)
        plt.connect('key_press_event', rs2)

    """
----->Weld Selection tab(2) all functions ends here
    """

    """
----->Line chart tab(4) all functions starts from here
    """
    def reset_btn_fun(self):
        if self.figure_x5.gca().patches:
            for patch in self.figure_x5.gca().patches:
                patch.remove()
            self.canvas_x5.draw()
            self.latitude.clear()
            self.logitude.clear()
            self.rect_start_1 = None  # Store the starting point of the rectangle
            self.rect_end_1 = None

    def line_selection5(self, eclick, erelease):
        if abs(eclick.x - erelease.x) >= 3 and abs(eclick.y - erelease.y) >= 3:
            self.rect_start_1 = eclick.xdata, eclick.ydata
            self.rect_end_1 = erelease.xdata, erelease.ydata

            if self.rect_start_1 is not None and self.rect_end_1 is not None:
                for patch in self.figure_x5.gca().patches:
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
                self.figure_x5.gca().add_patch(rect)
                self.canvas_x5.draw()

    def Line_chart1_next(self):
        current_index = self.combo.currentIndex()
        if current_index < self.combo.count() - 1:
            self.combo.setCurrentIndex(current_index + 1)
            self.Line_chart1()

    def Line_chart1_previous(self):
        current_index = self.combo.currentIndex()
        if current_index > 0:
            self.combo.setCurrentIndex(current_index - 1)
            self.Line_chart1()

    def Line_chart1(self):
        runid = self.runid
        weld_id = self.combo.currentText()
        self.weld_id = int(weld_id)
        p = self.project_name
        print(p)
        with connection.cursor() as cursor:
            # query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
            query = "SELECT start_index, end_index,start_oddo1,end_oddo1 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"

            cursor.execute(query, (self.runid, self.weld_id, self.runid, self.weld_id))
            result = cursor.fetchall()
            if result:
                path = config.weld_pipe_pkl + self.project_name + '/' + str(weld_id) + '.pkl'
                print(path)
                if os.path.isfile(path):
                    config.print_with_time("File exist")
                    df_pipe = pd.read_pickle(path)
                    #print(self.df_pipe)

                    self.plot_linechart_sensor(df_pipe)

                else:
                    folder_path = config.weld_pipe_pkl + self.project_name
                    print(folder_path)
                    config.print_with_time("File not exist")
                    try:
                        os.makedirs(folder_path)

                    except:
                        config.print_with_time("Folder already exists")
                    start_index, end_index = result[0][0], result[1][1]
                    print("start index and end index", start_index, end_index)
                    config.print_with_time("Start fetching at : ")

                    # query_for_start = 'SELECT * FROM ' + Config.table_name + ' WHERE index>{} AND index<{} order by index'
                    # query_job = client.query(query_for_start.format(start_index, end_index))
                    # self.df_pipe = query_job.result().to_dataframe()
                    # Config.print_with_time("conversion to data frame is done")
                    # self.df_pipe.to_pickle(path)
                    # Config.print_with_time("successfully  saved to pickle")
                    # # index = self.df_pipe['index']
                    # self.index = self.df_pipe['index']
                    # oddo1 = (self.df_pipe['ODDO1'] - Config.oddo1) / 1000
                    # # print("index....", index)
                    # self.figure_x5.clear()
                    # self.ax5 = self.figure_x5.add_subplot(111)

                    """
                    New Code
                    """
                    # start = time.time()
                    # print("start", start)
                    # executor = ThreadPoolExecutor(16)
                    #
                    # # start_index = 234637
                    # # end_index = 275019
                    # k = []
                    # while start_index < end_index:
                    #     k.append([start_index + 1, start_index + 2000])
                    #     start_index = start_index + 2000
                    # k1 = k[-1]
                    # del k[-1]
                    # k.append([k1[0], end_index])
                    # future = []
                    # for t in range(len(k)):
                    #     a = k[t]
                    #     future.append(executor.submit(func, [a[0], a[1]]))
                    # d1 = []
                    # for x in future:
                    #     df = x.result()
                    #     d1.append(df)
                    #
                    # df_pipe = pd.concat(d1)
                    # df_pipe.reset_index(inplace=True)
                    # # print("Plotted data", df_pipe)
                    # df_pipe.to_pickle(folder_path + '/' + str(weld_id) + '.pkl')
                    # Config.print_with_time("Succesfully saved to pickle file")

                    query_for_start = 'SELECT index,ROLL,ODDO1,ODDO2,[F1H1, F1H2, F1H3, F1H4, F2H1, F2H2, F2H3, F2H4,F3H1, F3H2, F3H3, F3H4, F4H1, F4H2, F4H3,F4H4, F5H1, F5H2, F5H3, F5H4, F6H1, F6H2, F6H3, F6H4,F7H1, F7H2, F7H3, F7H4, F8H1, F8H2, F8H3, F8H4, F9H1, F9H2, F9H3, F9H4, F10H1,F10H2, F10H3, F10H4,F11H1, F11H2, F11H3, F11H4, F12H1, F12H2, F12H3, F12H4, F13H1, F13H2, F13H3,F13H4, F14H1, F14H2, F14H3, F14H4,F15H1, F15H2, F15H3, F15H4, F16H1, F16H2, F16H3, F16H4, F17H1, F17H2, F17H3,F17H4, F18H1, F18H2, F18H3, F18H4,F19H1, F19H2, F19H3, F19H4, F20H1, F20H2, F20H3, F20H4, F21H1, F21H2, F21H3,F21H4, F22H1, F22H2, F22H3, F22H4,F23H1, F23H2, F23H3, F23H4, F24H1, F24H2, F24H3, F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4,F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1,F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4],PITCH,YAW FROM ' + config.table_name + ' WHERE index>{} AND index<{} order by index'
                    query_job = client.query(query_for_start.format(start_index, end_index))
                    results = query_job.result()

                    data = []
                    index_t4 = []
                    oddo_1 = []
                    oddo_2 = []
                    # indexes = []
                    roll1 = []
                    pitch1 = []
                    yaw1 = []

                    for row in results:
                        index_t4.append(row[0])
                        roll1.append(row[1])
                        oddo_1.append(row[2])
                        oddo_2.append(row[3])
                        data.append(row[4])
                        pitch1.append(row[5])
                        yaw1.append(row[6])
                        """
                        Swapping the Pitch data to Roll data
                        """

                    oddo1_t4 = []
                    oddo2_t4 = []
                    roll_t4 = []
                    pitch_t4 = []
                    yaw_t4 = []

                    """
                    Reference value will be consider
                    """
                    for odometer1 in oddo_1:
                        od1 = odometer1 - config.oddo1  ###16984.2 change According to run
                        oddo1_t4.append(od1)
                    for odometer2 in oddo_2:
                        od2 = odometer2 - config.oddo2  ###17690.36 change According to run
                        oddo2_t4.append(od2)

                    """
                    Reference value will be consider
                    """
                    for roll2 in roll1:
                        roll3 = roll2 - config.roll_value
                        roll_t4.append(roll3)

                    for pitch2 in pitch1:
                        pitch3 = pitch2 - config.pitch_value
                        pitch_t4.append(pitch3)

                    for yaw2 in yaw1:
                        yaw3 = yaw2 - config.yaw_value
                        yaw_t4.append(yaw3)

                    query_for_start = 'SELECT index,[F1P1, F2P2, F3P3, F4P4, F5P1, F6P2, F7P3, F8P4, F9P1, F10P2, F11P3, F12P4, F13P1, F14P2, F15P3, F16P4, F17P1, F18P2, F19P3, F20P4, F21P1, F22P2, F23P3, F24P4, F25P1, F26P2, F27P3, F28P4, F29P1, F30P2, F31P3, F32P4, F33P1, F34P2, F35P3, F36P4] FROM ' + config.table_name + ' WHERE index>{} AND index<{} order by index'
                    query_job = client.query(query_for_start.format(start_index, end_index))
                    results_1 = query_job.result()
                    data1 = []
                    index_lc = []
                    for row1 in results_1:
                        index_lc.append(row1[0])
                        data1.append(row1[1])

                    df_new_proximity_lc = pd.DataFrame(data1, columns=['F1P1', 'F2P2', 'F3P3', 'F4P4', 'F5P1', 'F6P2', 'F7P3', 'F8P4',
                                                                        'F9P1', 'F10P2', 'F11P3', 'F12P4', 'F13P1', 'F14P2', 'F15P3',
                                                                         'F16P4', 'F17P1', 'F18P2', 'F19P3', 'F20P4', 'F21P1', 'F22P2',
                                                                         'F23P3', 'F24P4', 'F25P1', 'F26P2', 'F27P3', 'F28P4', 'F29P1',
                                                                         'F30P2', 'F31P3', 'F32P4', 'F33P1', 'F34P2', 'F35P3', 'F36P4'])

                    df_new_t4 = pd.DataFrame(data, columns=[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)])

                    df_elem = pd.DataFrame({"index": index_t4, "ODDO1": oddo_1, "ROLL": roll_t4, "PITCH": pitch_t4, "YAW": yaw_t4})
                    frames = [df_elem, df_new_t4]
                    df_pipe = pd.concat(frames, axis=1, join='inner')

                    for col in df_new_proximity_lc.columns:
                        df_pipe[col] = df_new_proximity_lc[col]

                    # df_new.reset_index(inplace=True)
                    # print("Plotted data", df_pipe)
                    df_pipe.to_pickle(folder_path + '/' + str(weld_id) + '.pkl')
                    config.print_with_time("Succesfully saved to pickle file")
                    config.print_with_time("End fetching  at : ")

                    self.plot_linechart_sensor(df_pipe)
            else:
                config.print_with_time("No data found for this pipe ID : ")

    def plot_linechart_sensor(self, df_pipe):
        print("hi sensor linechart")
        self.index = df_pipe['index']
        oddo1 = (df_pipe['ODDO1'] - config.oddo1) / 1000

        self.figure_x5.clear()
        self.ax5 = self.figure_x5.add_subplot(111)
        self.ax5.figure.subplots_adjust(bottom=0.085, left=0.055, top=0.930, right=0.920)

        self.ax5.clear()
        # print("Plotted data", df_plot_data)
        res = [f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)]

        df1 = df_pipe[[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)]]
        df1 = df1.apply(pd.to_numeric, errors='coerce')

        window_length = 15
        polyorder = 2
        for col in res:
            data = df1[col].values
            time_index = np.arange(len(df1))
            coefficients = np.polyfit(time_index, data, polyorder)
            trend = np.polyval(coefficients, time_index)
            data_dettrended = data - trend
            data_denoised = savgol_filter(data_dettrended, window_length, polyorder)
            df1.loc[:len(df1), col] = data_denoised

        for i, data in enumerate(res):
            df1[data] = df1[data] + i * 1400

        n = 15  # the larger n is, the smoother curve will be
        b = [1.0 / n] * n
        a = 1

        for i, data in enumerate(res):
            filtered_data = lfilter(b, a, df1[data])
            self.ax5.plot(self.index, filtered_data, label=i)

        self.ax5.margins(x=0, y=0)
        oddo_val = list(oddo1)
        num_ticks1 = len(self.ax5.get_xticks())  # Adjust the number of ticks based on your preference
        # print(num_ticks1)
        tick_positions1 = [int(i) for i in np.linspace(0, len(oddo_val) - 1, num_ticks1)]
        # print(tick_positions1)

        ax4 = self.ax5.twiny()
        ax4.set_xticks(tick_positions1)
        ax4.set_xticklabels([f'{oddo_val[i]:.2f}' for i in tick_positions1], size=8)
        ax4.set_xlabel("Absolute Distance (m)", size=8)

        def on_hover(event):
            if event.inaxes:
                try:
                    x, y = event.xdata, event.ydata
                    if x is not None:
                        x = int(event.xdata)
                        y = int(event.ydata)
                        z = (df_pipe.loc[df_pipe.index == x, 'ODDO1']) - config.oddo1
                        Abs_distance = int(z.values[0])
                        index_value = df_pipe.loc[df_pipe.index == x, 'index']
                        index_value_1 = int(index_value.values[0])
                        # print("index_value",index_value_1)
                        # print("Abs.distance",Abs_distance)
                        self.toolbar_x5.set_message(
                            f"Index_Value={index_value_1}, Abs.Distance(mm)={Abs_distance/1000:.2f},\nSensor_offset_Values={y}")

                except (IndexError, ValueError):
                    # Print a user-friendly message instead of showing an error
                    print("Hovering outside valid data range. No data available.")

        self.canvas_x5.mpl_connect('motion_notify_event', on_hover)

        legend = self.ax5.legend(res, loc="upper left", bbox_to_anchor=(1.02, 0, 0.07, 1))

        d = {"down": 30, "up": -30}

        def func_scroll(evt):
            if legend.contains(evt):
                bbox = legend.get_bbox_to_anchor()
                bbox = Bbox.from_bounds(bbox.x0, bbox.y0 + d[evt.button], bbox.width, bbox.height)
                tr = legend.axes.transAxes.inverted()
                legend.set_bbox_to_anchor(bbox.transformed(tr))
                self.canvas_x5.draw_idle()

        self.canvas_x5.mpl_connect("scroll_event", func_scroll)

        # Integrate the pick event code here
        lines = [line for line in self.ax5.get_lines()]
        map_legend_to_ax = {}  # Will map legend lines to original lines.

        pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

        for legend_line, ax_line in zip(legend.get_lines(), lines):
            legend_line.set_picker(pickradius)  # Enable picking on the legend line.
            map_legend_to_ax[legend_line] = ax_line

        def on_pick(event):
            # On the pick event, find the original line corresponding to the legend
            # proxy line, and toggle its visibility.
            legend_line = event.artist

            # Do nothing if the source of the event is not a legend line.
            if legend_line not in map_legend_to_ax:
                return

            ax_line = map_legend_to_ax[legend_line]
            visible = not ax_line.get_visible()
            ax_line.set_visible(visible)
            # Change the alpha on the line in the legend, so we can see what lines
            # have been toggled.
            legend_line.set_alpha(1.0 if visible else 0.2)
            self.canvas_x5.draw()

        self.canvas_x5.mpl_connect('pick_event', on_pick)
        self.ax5.set_ylabel('Hall Sensor')

        df_proxi_data = ['F1P1', 'F2P2', 'F3P3', 'F4P4', 'F5P1', 'F6P2', 'F7P3',
                           'F8P4', 'F9P1', 'F10P2', 'F11P3', 'F12P4', 'F13P1',
                           'F14P2', 'F15P3', 'F16P4', 'F17P1', 'F18P2', 'F19P3',
                           'F20P4', 'F21P1', 'F22P2', 'F23P3', 'F24P4', 'F25P1', 'F26P2', 'F27P3', 'F28P4', 'F29P1',
                           'F30P2', 'F31P3', 'F32P4', 'F33P1', 'F34P2', 'F35P3', 'F36P4']

        # df_proximity = df_pipe[['F1P1', 'F2P2', 'F3P3', 'F4P4', 'F5P1', 'F6P2', 'F7P3',
        #                    'F8P4', 'F9P1', 'F10P2', 'F11P3', 'F12P4', 'F13P1',
        #                    'F14P2', 'F15P3', 'F16P4', 'F17P1', 'F18P2', 'F19P3',
        #                    'F20P4', 'F21P1', 'F22P2', 'F23P3', 'F24P4', 'F25P1', 'F26P2', 'F27P3', 'F28P4', 'F29P1',
        #                     'F30P2', 'F31P3', 'F32P4', 'F33P1', 'F34P2', 'F35P3', 'F36P4']]

        scaler = MinMaxScaler()
        scaled_values = scaler.fit_transform(df_pipe[df_proxi_data])
        gap_size = 0
        for i, col in enumerate(df_proxi_data):
            df_pipe[col] = scaled_values[:, i] + i * gap_size

        n = 15  # the larger n is, the smoother curve will be
        b = [1.0 / n] * n
        a = 1
        ls = [round(i * 0.3, 1) for i in range(1, 37)]

        for j1, column2 in enumerate(df_proxi_data):
            df_pipe[column2] = df_pipe[column2] + ls[j1]

        fig = go.Figure()
        for i1, column1 in enumerate(df_proxi_data):
            yy = lfilter(b, a, df_pipe[column1])
            fig.add_trace(go.Scatter(x=[df_pipe.index, round(oddo1, 3)], y=yy, name=column1))

        # Mean1 = df_proximity.mean()
        # Mean1.tolist()
        #
        # ls = [36000 * i for i in range(1, 25)]
        #
        # fig = go.Figure()
        # for i, column in enumerate(df_proxi_data):
        #     df3 = (df_pipe[column] - Mean1[column]) + ls[i]
        #     fig.add_trace(go.Scatter(x=[df_pipe.index, oddo1], y=df3, name=column))

        fig.update_layout(
            width=1800,
            height=400,
            # margin=dict(l=140),
            # paper_bgcolor='#e99595',
            # plot_bgcolor='rgb(255, 255, 255)',
            title={'x': 0.5},
            font={"family": "courier"},
        )
        fig.update_xaxes(
            title_text="ODDO1(Absolute Distance(m))",
            # title_font_family="Arial",
            tickfont=dict(size=11),
            dtick=1000,  # Show the x-axis line
            tickangle=0, showticklabels=True, ticklen=0,
        )
        fig.add_annotation(
            xref="x domain",
            yref="y domain",
            # The arrow head will be 25% along the x axis, starting from the left
            x=-0.084,
            # The arrow head will be 40% along the y axis, starting from the bottom
            y=-0.034,
            showarrow=False,
        )

        pio.write_html(fig, file='h_line_chart_proxi.html', auto_open=False)
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "h_line_chart_proxi.html"))
        self.m_output_proxi.load(QUrl.fromLocalFile(file_path))

        self.canvas_x5.draw()
        config.print_with_time("End plotting  at : ")

        rs1 = RectangleSelector(self.figure_x5.gca(), self.line_selection5, useblit=True)
        plt.connect('key_press_event', rs1)

    def mark_lat_long(self):
        if self.rect_start_1 is not None and self.rect_end_1 is not None:
            x1, y1 = min(self.rect_start_1[0], self.rect_end_1[0]), \
                     min(self.rect_start_1[1], self.rect_end_1[1])
            x2, y2 = x1 + abs(self.rect_end_1[0] - self.rect_start_1[0]), \
                     y1 + abs(self.rect_end_1[1] - self.rect_start_1[1])
            lat_mark = self.latitude.text().strip()
            long_mark = self.logitude.text().strip()

            if lat_mark and long_mark:
                index = self.index
                start_index = index.iloc[int(self.rect_start_1[0])]
                end_index = index.iloc[int(self.rect_end_1[0])]
                runid = self.runid
                weld_id = self.weld_id
                print(runid, weld_id)
                print(start_index, end_index)
                query_for_start = 'SELECT * FROM ' + config.table_name + ' WHERE index={}'
                query_job = client.query(query_for_start.format(start_index))
                results_1 = query_job.result()
                oddo1 = []
                oddo2 = []
                for row1 in results_1:
                    oddo1.append(row1['ODDO1'])
                    oddo2.append(row1['ODDO2'])
                """
                    Change oddo1 and oddo2 distance according to reference
                """
                oddo1 = oddo1[0] - config.oddo1
                oddo2 = oddo2[0] - config.oddo2
                print(oddo1, oddo2)
                with connection.cursor() as cursor:
                    same_lw_up_check = cursor.execute(
                        'SELECT absolute_distance_oddo1,absolute_distance_oddo2 FROM dgps_segment where absolute_distance_oddo1="' + str(
                            oddo1) + '" and absolute_distance_oddo2="' + str(oddo2) + '"')
                    if same_lw_up_check:
                        return 'HII'
                    else:
                        query_pipe_insert = "INSERT INTO dgps_segment (runid, pipe_id, start_index, absolute_distance_oddo2,absolute_distance_oddo1,Latitude,Logitude) VALUE(%s,%s,%s,%s,%s,%s,%s) "

                        # Execute query.
                        cursor.execute(query_pipe_insert,
                                       (int(runid), int(weld_id), int(start_index), oddo2, oddo1, lat_mark, long_mark))
                        connection.commit()
                QMessageBox.information(self, 'Success', 'Data saved')
            else:
                QMessageBox.warning(self, 'Invalid Input', 'Enter any value')
        else:
            QMessageBox.warning(self, 'Invalid Input',
                                'Select RectangleSelection of Marking, then press the button for Lat And Long')

    """
    This function we are using to mean of each sensor its depends on Pipe
    """
    def basevalue(self):
        print("hi base val func")
        if self.rect_start_1 is not None and self.rect_end_1 is not None:
            print("hi rect start1 func")
            index_chart = self.index.tolist()
            # print(index)
            start_counter = index_chart[int(self.rect_start_1[0])]
            end_counter = index_chart[int(self.rect_end_1[0])]
            # print("counters", start_counter, end_counter)
            runid = self.runid
            weld_id = self.weld_id
            print(runid, weld_id)
            print(start_counter, end_counter)
            query_for_start = 'SELECT F1H1, F1H2, F1H3, F1H4, F2H1, F2H2, F2H3, F2H4,F3H1, F3H2, F3H3, F3H4, F4H1, F4H2, F4H3, F4H4, F5H1, F5H2, F5H3, F5H4, F6H1, F6H2, F6H3, F6H4, F7H1, F7H2, F7H3, F7H4, F8H1, F8H2, F8H3, F8H4, F9H1, F9H2, F9H3, F9H4, F10H1, F10H2, F10H3, F10H4, F11H1, F11H2, F11H3, F11H4, F12H1, F12H2, F12H3, F12H4, F13H1, F13H2, F13H3, F13H4, F14H1, F14H2, F14H3, F14H4, F15H1, F15H2, F15H3, F15H4, F16H1, F16H2, F16H3, F16H4, F17H1, F17H2, F17H3, F17H4, F18H1, F18H2, F18H3, F18H4, F19H1, F19H2, F19H3, F19H4, F20H1, F20H2, F20H3, F20H4, F21H1, F21H2, F21H3, F21H4, F22H1, F22H2, F22H3, F22H4, F23H1, F23H2, F23H3, F23H4, F24H1, F24H2, F24H3, F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4, F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1, F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4 FROM ' + config.table_name + ' WHERE index>{} AND index<{} order by index'
            query_job = client.query(query_for_start.format(start_counter, end_counter))
            results = query_job.result().to_dataframe().mean()
            base_value_each_pipe = results.to_list()
            print("base_value_each_pipe.....", base_value_each_pipe)
            F1H1 = base_value_each_pipe[0]
            F1H2 = base_value_each_pipe[1]
            F1H3 = base_value_each_pipe[2]
            F1H4 = base_value_each_pipe[3]
            F2H1 = base_value_each_pipe[4]
            F2H2 = base_value_each_pipe[5]
            F2H3 = base_value_each_pipe[6]
            F2H4 = base_value_each_pipe[7]
            F3H1 = base_value_each_pipe[8]
            F3H2 = base_value_each_pipe[9]
            F3H3 = base_value_each_pipe[10]
            F3H4 = base_value_each_pipe[11]
            F4H1 = base_value_each_pipe[12]
            F4H2 = base_value_each_pipe[13]
            F4H3 = base_value_each_pipe[14]
            F4H4 = base_value_each_pipe[15]
            F5H1 = base_value_each_pipe[16]
            F5H2 = base_value_each_pipe[17]
            F5H3 = base_value_each_pipe[18]
            F5H4 = base_value_each_pipe[29]
            F6H1 = base_value_each_pipe[20]
            F6H2 = base_value_each_pipe[21]
            F6H3 = base_value_each_pipe[22]
            F6H4 = base_value_each_pipe[23]
            F7H1 = base_value_each_pipe[24]
            F7H2 = base_value_each_pipe[25]
            F7H3 = base_value_each_pipe[26]
            F7H4 = base_value_each_pipe[27]
            F8H1 = base_value_each_pipe[28]
            F8H2 = base_value_each_pipe[29]
            F8H3 = base_value_each_pipe[30]
            F8H4 = base_value_each_pipe[31]
            F9H1 = base_value_each_pipe[32]
            F9H2 = base_value_each_pipe[33]
            F9H3 = base_value_each_pipe[34]
            F9H4 = base_value_each_pipe[35]
            F10H1 = base_value_each_pipe[36]
            F10H2 = base_value_each_pipe[37]
            F10H3 = base_value_each_pipe[38]
            F10H4 = base_value_each_pipe[39]
            F11H1 = base_value_each_pipe[40]
            F11H2 = base_value_each_pipe[41]
            F11H3 = base_value_each_pipe[42]
            F11H4 = base_value_each_pipe[43]
            F12H1 = base_value_each_pipe[44]
            F12H2 = base_value_each_pipe[45]
            F12H3 = base_value_each_pipe[46]
            F12H4 = base_value_each_pipe[47]
            F13H1 = base_value_each_pipe[48]
            F13H2 = base_value_each_pipe[49]
            F13H3 = base_value_each_pipe[50]
            F13H4 = base_value_each_pipe[51]
            F14H1 = base_value_each_pipe[52]
            F14H2 = base_value_each_pipe[53]
            F14H3 = base_value_each_pipe[54]
            F14H4 = base_value_each_pipe[55]
            F15H1 = base_value_each_pipe[56]
            F15H2 = base_value_each_pipe[57]
            F15H3 = base_value_each_pipe[58]
            F15H4 = base_value_each_pipe[59]
            F16H1 = base_value_each_pipe[60]
            F16H2 = base_value_each_pipe[61]
            F16H3 = base_value_each_pipe[62]
            F16H4 = base_value_each_pipe[63]
            F17H1 = base_value_each_pipe[64]
            F17H2 = base_value_each_pipe[65]
            F17H3 = base_value_each_pipe[66]
            F17H4 = base_value_each_pipe[67]
            F18H1 = base_value_each_pipe[68]
            F18H2 = base_value_each_pipe[69]
            F18H3 = base_value_each_pipe[70]
            F18H4 = base_value_each_pipe[71]
            F19H1 = base_value_each_pipe[72]
            F19H2 = base_value_each_pipe[73]
            F19H3 = base_value_each_pipe[74]
            F19H4 = base_value_each_pipe[75]
            F20H1 = base_value_each_pipe[76]
            F20H2 = base_value_each_pipe[77]
            F20H3 = base_value_each_pipe[78]
            F20H4 = base_value_each_pipe[79]
            F21H1 = base_value_each_pipe[80]
            F21H2 = base_value_each_pipe[81]
            F21H3 = base_value_each_pipe[82]
            F21H4 = base_value_each_pipe[83]
            F22H1 = base_value_each_pipe[84]
            F22H2 = base_value_each_pipe[85]
            F22H3 = base_value_each_pipe[86]
            F22H4 = base_value_each_pipe[87]
            F23H1 = base_value_each_pipe[88]
            F23H2 = base_value_each_pipe[89]
            F23H3 = base_value_each_pipe[90]
            F23H4 = base_value_each_pipe[91]
            F24H1 = base_value_each_pipe[92]
            F24H2 = base_value_each_pipe[93]
            F24H3 = base_value_each_pipe[94]
            F24H4 = base_value_each_pipe[95]
            F25H1 = base_value_each_pipe[96]
            F25H2 = base_value_each_pipe[97]
            F25H3 = base_value_each_pipe[98]
            F25H4 = base_value_each_pipe[99]
            F26H1 = base_value_each_pipe[100]
            F26H2 = base_value_each_pipe[101]
            F26H3 = base_value_each_pipe[102]
            F26H4 = base_value_each_pipe[103]
            F27H1 = base_value_each_pipe[104]
            F27H2 = base_value_each_pipe[105]
            F27H3 = base_value_each_pipe[106]
            F27H4 = base_value_each_pipe[107]
            F28H1 = base_value_each_pipe[108]
            F28H2 = base_value_each_pipe[109]
            F28H3 = base_value_each_pipe[110]
            F28H4 = base_value_each_pipe[111]
            F29H1 = base_value_each_pipe[112]
            F29H2 = base_value_each_pipe[113]
            F29H3 = base_value_each_pipe[114]
            F29H4 = base_value_each_pipe[115]
            F30H1 = base_value_each_pipe[116]
            F30H2 = base_value_each_pipe[117]
            F30H3 = base_value_each_pipe[118]
            F30H4 = base_value_each_pipe[119]
            F31H1 = base_value_each_pipe[120]
            F31H2 = base_value_each_pipe[121]
            F31H3 = base_value_each_pipe[122]
            F31H4 = base_value_each_pipe[123]
            F32H1 = base_value_each_pipe[124]
            F32H2 = base_value_each_pipe[125]
            F32H3 = base_value_each_pipe[126]
            F32H4 = base_value_each_pipe[127]
            F33H1 = base_value_each_pipe[128]
            F33H2 = base_value_each_pipe[129]
            F33H3 = base_value_each_pipe[130]
            F33H4 = base_value_each_pipe[131]
            F34H1 = base_value_each_pipe[132]
            F34H2 = base_value_each_pipe[133]
            F34H3 = base_value_each_pipe[134]
            F34H4 = base_value_each_pipe[135]
            F35H1 = base_value_each_pipe[136]
            F35H2 = base_value_each_pipe[137]
            F35H3 = base_value_each_pipe[138]
            F35H4 = base_value_each_pipe[139]
            F36H1 = base_value_each_pipe[140]
            F36H2 = base_value_each_pipe[141]
            F36H3 = base_value_each_pipe[142]
            F36H4 = base_value_each_pipe[143]
            print("F36H4", F36H4)

            # print(F32H4)
            with connection.cursor() as cursor:
                query_pipe_insert = "INSERT INTO base_value (runid,pipe_id, F1H1, F1H2, F1H3, F1H4, F2H1, F2H2, F2H3, F2H4, F3H1, F3H2, F3H3, F3H4, F4H1, F4H2, F4H3, F4H4, F5H1, F5H2, F5H3, F5H4, F6H1, F6H2, F6H3, F6H4, F7H1, F7H2, F7H3, F7H4, F8H1, F8H2, F8H3, F8H4,F9H1, F9H2, F9H3, F9H4, F10H1, F10H2, F10H3, F10H4, F11H1, F11H2, F11H3, F11H4, F12H1, F12H2, F12H3, F12H4, F13H1, F13H2, F13H3, F13H4, F14H1, F14H2, F14H3, F14H4, F15H1, F15H2, F15H3, F15H4, F16H1, F16H2, F16H3, F16H4, F17H1, F17H2, F17H3, F17H4, F18H1, F18H2, F18H3, F18H4, F19H1, F19H2, F19H3, F19H4, F20H1, F20H2, F20H3, F20H4, F21H1, F21H2, F21H3, F21H4, F22H1, F22H2, F22H3, F22H4, F23H1, F23H2, F23H3, F23H4, F24H1, F24H2, F24H3, F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4, F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1, F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4) VALUE('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    runid, weld_id, F1H1, F1H2, F1H3, F1H4, F2H1, F2H2, F2H3, F2H4, F3H1, F3H2, F3H3, F3H4, F4H1, F4H2,
                    F4H3, F4H4, F5H1, F5H2, F5H3, F5H4, F6H1, F6H2, F6H3, F6H4, F7H1, F7H2, F7H3, F7H4, F8H1, F8H2,
                    F8H3, F8H4, F9H1, F9H2, F9H3, F9H4, F10H1, F10H2, F10H3, F10H4, F11H1, F11H2, F11H3, F11H4, F12H1,
                    F12H2, F12H3, F12H4, F13H1, F13H2, F13H3, F13H4, F14H1, F14H2, F14H3, F14H4, F15H1, F15H2, F15H3,
                    F15H4, F16H1, F16H2, F16H3, F16H4, F17H1, F17H2, F17H3, F17H4, F18H1, F18H2, F18H3, F18H4, F19H1,
                    F19H2, F19H3, F19H4, F20H1, F20H2, F20H3, F20H4, F21H1, F21H2, F21H3, F21H4, F22H1, F22H2, F22H3,
                    F22H4, F23H1, F23H2, F23H3, F23H4, F24H1, F24H2, F24H3, F24H4, F25H1, F25H2, F25H3, F25H4, F26H1,
                    F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4, F29H1, F29H2, F29H3,
                    F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1,
                    F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3,
                    F36H4)
                cursor.execute(query_pipe_insert)
                connection.commit()
                QMessageBox.information(self, 'Success', 'Data saved')
        else:
            QMessageBox.warning(self, 'Invalid Input',
                                'Select RectangleSelection of Marking, then press the button for base value')

    def feature_selection_func(self):
        if self.rect_start_1 is not None and self.rect_end_1 is not None:
            print("hi rect start1 func")
            while True:
                name, ok = QInputDialog.getText(self, 'Enter Name', 'Enter the name of the drawn box:')
                if ok:
                    if name.strip():  # Check if the entered name is not empty or just whitespace
                        x_start, y_start = self.rect_start_1
                        x_end, y_end = self.rect_end_1
                        runid = self.runid
                        pipe = self.weld_id
                        index_k = self.index.tolist()
                        start_index15 = index_k[round(x_start)]
                        end_index15 = index_k[round(x_end)]
                        # start_index15 = round(x_start)
                        # end_index15 = round(x_end)
                        print(start_index15, end_index15, name)
                        query_for_start = 'SELECT ODDO1,ODDO2 FROM ' + config.table_name + ' WHERE index>={} AND index<={} AND runid={} order by index'
                        query_job = client.query(
                            query_for_start.format(int(start_index15), int(end_index15), runid))
                        results = query_job.result()
                        oddo1 = []
                        oddo2 = []
                        for row in results:
                            oddo1.append(row[0])
                            oddo2.append(row[1])
                        # print(oddo1)
                        # print(oddo2)
                        start_oddo1 = oddo1[0] - config.oddo1
                        end_oddo1 = oddo1[-1] - config.oddo1
                        start_oddo2 = oddo2[0] - config.oddo2
                        end_oddo2 = oddo2[-1] - config.oddo2
                        length_oddo1 = end_oddo1 - start_oddo1
                        length_oddo2 = end_oddo2 - start_oddo2
                        with connection.cursor() as cursor:
                            type = 'manual'
                            query_weld_insert = "INSERT INTO anomalies (runid, start_index, end_index,type,start_oddo1,end_oddo1,start_oddo2,end_oddo2,length_oddo1,length_oddo2,feature_name,Pipe_No) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                                runid, start_index15, end_index15, type, start_oddo1, end_oddo1,
                                start_oddo2, end_oddo2, length_oddo1, length_oddo2, name, pipe)

                            # Execute query.
                            b = cursor.execute(query_weld_insert)
                            connection.commit()
                            QMessageBox.information(self, 'Success', 'Data saved')
                        break  # Exit the loop if a valid name is provided
                    else:
                        QMessageBox.warning(self, 'Invalid Input', 'Please enter a name.')
                else:
                    print('Operation canceled.')
                    break
        else:
            QMessageBox.warning(self, 'Invalid Input',
                                'Select RectangleSelection of Marking, then press the button for base value')
    """
------>Line chart tab(4) all functions ends here
    """

    """
------>Line chart orientation tab(5) all functions starts from here
    """
    def Line_chart_orientation_next(self):
        current_index = self.combo_orientation.currentIndex()
        if current_index < self.combo_orientation.count() - 1:
            self.combo_orientation.setCurrentIndex(current_index + 1)
            self.Line_chart_orientation()

    def Line_chart_orientation_previous(self):
        current_index = self.combo_orientation.currentIndex()
        if current_index > 0:
            self.combo_orientation.setCurrentIndex(current_index - 1)
            self.Line_chart_orientation()

    def Line_chart_orientation(self):
        runid = self.runid
        weld_num = self.combo_orientation.currentText()
        self.weld_num = int(weld_num)
        # self.lower_sensitivity_orien = self.lower_Sensitivity_combo_box_orientation.currentText()
        # self.upper_sensitivity_orien = self.upper_Sensitivity_combo_box_orientation.currentText()

        with connection.cursor() as cursor:
            query = "SELECT start_index, end_index,start_oddo1,end_oddo1 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"
            cursor.execute(query, (self.runid, self.weld_num, self.runid, self.weld_num))
            result = cursor.fetchall()
            start_oddo1 = result[0][2]
            end_oddo1 = result[1][3]

            if not result:
                config.print_with_time("No data found for this pipe ID : ")
            else:
                """
                pkl file is found in local path
                """
                path = config.roll_pkl_lc + self.project_name + '/' + str(weld_num) + '.pkl'
                print(path)
                if os.path.isfile(path):
                    config.print_with_time("File exist")
                    df_clock_holl = pd.read_pickle(path)
                    val_ori_sensVal = df_clock_holl[[f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]]

                    df_clock_index = df_clock_holl['index']
                    oddo1_tab9 = round(df_clock_holl['ODDO1']/1000, 2)

                    config.print_with_time("Start fetching at : ")
                    # start_index, end_index = result[0][0], result[1][1]
                    # query_for_start = 'SELECT index,[F1H1, F1H2, F1H3, F1H4, F2H1, F2H2, F2H3, F2H4,F3H1, F3H2, F3H3, F3H4, F4H1, F4H2, F4H3,F4H4, F5H1, F5H2, F5H3, F5H4, F6H1, F6H2, F6H3, F6H4,F7H1, F7H2, F7H3, F7H4, F8H1, F8H2, F8H3, F8H4, F9H1, F9H2, F9H3, F9H4, F10H1,F10H2, F10H3, F10H4,F11H1, F11H2, F11H3, F11H4, F12H1, F12H2, F12H3, F12H4, F13H1, F13H2, F13H3,F13H4, F14H1, F14H2, F14H3, F14H4,F15H1, F15H2, F15H3, F15H4, F16H1, F16H2, F16H3, F16H4, F17H1, F17H2, F17H3,F17H4, F18H1, F18H2, F18H3, F18H4,F19H1, F19H2, F19H3, F19H4, F20H1, F20H2, F20H3, F20H4, F21H1, F21H2, F21H3,F21H4, F22H1, F22H2, F22H3, F22H4,F23H1, F23H2, F23H3, F23H4, F24H1, F24H2, F24H3, F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4,F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1,F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4] FROM ' + Config.table_name + ' WHERE index>{} AND index<{} order by index'
                    # query_job = client.query(query_for_start.format(start_index, end_index))
                    # results_1 = query_job.result()
                    # data1 = []
                    # index_hm_ori_lc = []
                    # for row1 in results_1:
                    #     index_hm_ori_lc.append(row1[0])
                    #     data1.append(row1[1])
                    #
                    # df_new_tab9 = pd.DataFrame(data1, columns=[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)])
                    # df_new_tab9.columns = val_ori_sensVal.columns
                    # df1_aligned = val_ori_sensVal.reindex(df_new_tab9.index)
                    # result_new = df1_aligned.where(df1_aligned != 0, df_new_tab9)
                    # result_new = result_new.dropna()
                    # # print("result",result)
                    # result_new.reset_index(drop=True, inplace=True)

                    # df_new_tab9 = df_new_tab9.apply(pd.to_numeric, errors='coerce')
                    #
                    # window_length = 15
                    # polyorder = 2
                    # for col in df_new_tab9.columns:
                    #     data = df_new_tab9[col].values
                    #     time_index = np.arange(len(df_new_tab9))
                    #     coefficients = np.polyfit(time_index, data, polyorder)
                    #     trend = np.polyval(coefficients, time_index)
                    #     data_dettrended = data - trend
                    #     data_denoised = savgol_filter(data_dettrended, window_length, polyorder)
                    #     df_new_tab9[col] = data_denoised
                    #     # df_new_tab9.loc[:len(result_new), col] = data_denoised
                    # Config.print_with_time("End fetching at : ")

                    # res = [f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]
                    #
                    # scaler = MinMaxScaler()
                    # scaled_values = scaler.fit_transform(df_clock_holl[res])
                    # gap_size = 0
                    # for i, col in enumerate(res):
                    #     df_clock_holl[col] = scaled_values[:, i] + i * gap_size
                    #
                    # n = 15  # the larger n is, the smoother curve will be
                    # b = [1.0 / n] * n
                    # a = 1
                    # ls = [round(i * 0.3, 1) for i in range(1, 145)]
                    #
                    # for j1, column2 in enumerate(res):
                    #     df_clock_holl[column2] = df_clock_holl[column2] + ls[j1]

                    # for i, data in enumerate(res):
                    #     yy = lfilter(b, a, df_clock_holl[data])
                    #     self.ax5.plot((df_clock_holl['index']).to_numpy(), yy, label=i)

                    fig = go.Figure()
                    for i1, column1 in enumerate(val_ori_sensVal):
                        fig.add_trace(
                            go.Scatter(x=[df_clock_index, oddo1_tab9], y=df_clock_holl[column1], name=column1))
                        # fig.update_layout()
                    fig.update_xaxes(
                        # tickfont=dict(size=11),
                        dtick=1000,
                        title_text="Absolute Distance(m))",
                        # tickangle=0, showticklabels=True, ticklen=0
                    )
                    config.print_with_time("End fetching at : ")
                    pio.write_html(fig, file='h_line_chart_ori.html', auto_open=False)
                    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "h_line_chart_ori.html"))
                    self.m_output_orientation.load(QUrl.fromLocalFile(file_path))
                    config.print_with_time("Plotted...")

                else:
                    """
                    pkl file is not found than data fetch from GCP and save pkl file in local path
                    """

                    folder_path = config.roll_pkl_lc + self.project_name
                    print(folder_path)
                    config.print_with_time("File not exist")
                    try:
                        os.makedirs(folder_path)
                    except:
                        config.print_with_time("Folder already exists")

                    start_index, end_index = result[0][0], result[1][1]
                    print(start_index, end_index)
                    config.print_with_time("Start fetching at : ")

                    query_for_start = 'SELECT index,ROLL,ODDO1,ODDO2,[F1H1, F1H2, F1H3, F1H4, F2H1, F2H2, F2H3, F2H4,F3H1, F3H2, F3H3, F3H4, F4H1, F4H2, F4H3,F4H4, F5H1, F5H2, F5H3, F5H4, F6H1, F6H2, F6H3, F6H4,F7H1, F7H2, F7H3, F7H4, F8H1, F8H2, F8H3, F8H4, F9H1, F9H2, F9H3, F9H4, F10H1,F10H2, F10H3, F10H4,F11H1, F11H2, F11H3, F11H4, F12H1, F12H2, F12H3, F12H4, F13H1, F13H2, F13H3,F13H4, F14H1, F14H2, F14H3, F14H4,F15H1, F15H2, F15H3, F15H4, F16H1, F16H2, F16H3, F16H4, F17H1, F17H2, F17H3,F17H4, F18H1, F18H2, F18H3, F18H4,F19H1, F19H2, F19H3, F19H4, F20H1, F20H2, F20H3, F20H4, F21H1, F21H2, F21H3,F21H4, F22H1, F22H2, F22H3, F22H4,F23H1, F23H2, F23H3, F23H4, F24H1, F24H2, F24H3, F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4,F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1,F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4] FROM ' + config.table_name + ' WHERE index>{} AND index<{} order by index'
                    query_job = client.query(query_for_start.format(start_index, end_index))
                    results = query_job.result()

                    data = []
                    index_orientation = []
                    oddo_1 = []
                    oddo_2 = []
                    indexes = []
                    roll1 = []

                    for row in results:
                        index_orientation.append(row[0])
                        roll1.append(row[1])
                        oddo_1.append(row[2])
                        oddo_2.append(row[3])
                        data.append(row[4])
                        """
                        Swapping the Pitch data to Roll data
                        """

                        # indexes.append(ranges(index_of_occurrences(row['frames'], 1)))

                    oddo1_tab_orientation = []
                    oddo2_tab_orientation = []
                    roll_t_orientation = []

                    """
                    Reference value will be consider
                    """
                    for odometer1 in oddo_1:
                        od1 = odometer1 - config.oddo1  ###16984.2 change According to run
                        oddo1_tab_orientation.append(od1)
                    for odometer2 in oddo_2:
                        od2 = odometer2 - config.oddo2  ###17690.36 change According to run
                        oddo2_tab_orientation.append(od2)

                    """
                    Reference value will be consider
                    """
                    for roll2 in roll1:
                        roll3 = roll2 - config.roll_value
                        roll_t_orientation.append(roll3)

                    query_for_start = 'SELECT index,[F1P1, F2P2, F3P3, F4P4, F5P1, F6P2, F7P3, F8P4, F9P1, F10P2, F11P3, F12P4, F13P1, F14P2, F15P3, F16P4, F17P1, F18P2, F19P3, F20P4, F21P1, F22P2, F23P3, F24P4, F25P1, F26P2, F27P3, F28P4, F29P1, F30P2, F31P3, F32P4, F33P1, F34P2, F35P3, F36P4] FROM ' + config.table_name + ' WHERE index>{} AND index<{} order by index'
                    query_job = client.query(query_for_start.format(start_index, end_index))
                    results_1 = query_job.result()
                    data1 = []
                    index_hm_ori_lc = []
                    for row1 in results_1:
                        index_hm_ori_lc.append(row1[0])
                        data1.append(row1[1])
                    # print("start_index.....", start_index)

                    df_new_proximity_ori_lc = pd.DataFrame(data1,
                                                                  columns=['F1P1', 'F2P2', 'F3P3', 'F4P4', 'F5P1',
                                                                       'F6P2', 'F7P3',
                                                                       'F8P4',
                                                                       'F9P1', 'F10P2', 'F11P3', 'F12P4', 'F13P1',
                                                                       'F14P2',
                                                                       'F15P3', 'F16P4', 'F17P1', 'F18P2', 'F19P3',
                                                                       'F20P4', 'F21P1', 'F22P2', 'F23P3', 'F24P4', 'F25P1',
                                                                       'F26P2', 'F27P3', 'F28P4', 'F29P1', 'F30P2', 'F31P3',
                                                                       'F32P4', 'F33P1', 'F34P2', 'F35P3', 'F36P4'])


                    df_new_t5 = pd.DataFrame(data, columns=[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)])

                    # mean_row_wise_dataframe = df_new_tab9.mean(axis=1)
                    # multiply_by_factor_magnetization = mean_row_wise_dataframe * 0.0004854

                    sensor_columns = [f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)]
                    # df1 = df_new_t5[[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)]]
                    # df_new_t5 = df_new_t5.apply(pd.to_numeric, errors='coerce')
                    # window_length = 15
                    # polyorder = 2
                    # for col in sensor_columns:
                    #     data = df1[col].values
                    #     time_index = np.arange(len(df1))
                    #     coefficients = np.polyfit(time_index, data, polyorder)
                    #     trend = np.polyval(coefficients, time_index)
                    #     data_dettrended = data - trend
                    #     data_denoised = savgol_filter(data_dettrended, window_length, polyorder)
                    #     df_new_t5.loc[:len(df1), col] = data_denoised

                    # self.figure_x_orientation.clear()
                    # self.ax_ori = self.figure_x_orientation.add_subplot(111)
                    # self.ax_ori.figure.subplots_adjust(bottom=0.085, left=0.055, top=0.930, right=0.920)
                    # self.ax_ori.clear()
                    # print("Plotted data", df_plot_data)

                    df_new_t5.columns = [f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]
                    for i, data in enumerate(df_new_t5.columns):
                        df_new_t5[data] = df_new_t5[data] + i * 1400

                    n = 15  # the larger n is, the smoother curve will be
                    b = [1.0 / n] * n
                    a = 1

                    # for i, data in enumerate(df_new_t5.columns):
                    #     filtered_data = lfilter(b, a, df_new_t5[data])
                    #     self.ax_ori.plot(index_orientation, filtered_data, label=i)
                    #
                    # self.ax_ori.margins(x=0, y=0)
                    #
                    # oddo1 = [(x/1000) for x in oddo1_tab_orientation]
                    # oddo_val = list(oddo1)
                    # num_ticks1 = len(self.ax_ori.get_xticks())  # Adjust the number of ticks based on your preference
                    # # print(num_ticks1)
                    # tick_positions1 = [int(i) for i in np.linspace(0, len(oddo_val) - 1, num_ticks1)]
                    # # print(tick_positions1)
                    # #
                    # ax4 = self.ax_ori.twiny()
                    # ax4.set_xticks(tick_positions1)
                    # ax4.set_xticklabels([f'{oddo_val[i]:.2f}' for i in tick_positions1], size=8)
                    # ax4.set_xlabel("Absolute Distance (m)", size=8)
                    #
                    # def on_hover(event):
                    #     if event.inaxes:
                    #         try:
                    #             x, y = event.xdata, event.ydata
                    #             if x is not None:
                    #                 x = int(event.xdata)
                    #                 y = int(event.ydata)
                    #                 z = (df_pipe.loc[df_pipe.index == x, 'ODDO1']) - Config.oddo1
                    #                 Abs_distance = int(z.values[0])
                    #                 index_value = df_pipe.loc[df_pipe.index == x, 'index']
                    #                 index_value_1 = int(index_value.values[0])
                    #                 # print("index_value",index_value_1)
                    #                 # print("Abs.distance",Abs_distance)
                    #                 self.toolbar_x_orientation.set_message(
                    #                     f"Index_Value={index_value_1}, Abs.Distance(mm)={Abs_distance / 1000:.2f},\nSensor_offset_Values={y}")
                    #
                    #         except (IndexError, ValueError):
                    #             # Print a user-friendly message instead of showing an error
                    #             print("Hovering outside valid data range. No data available.")
                    #
                    # self.canvas_x_orientation.mpl_connect('motion_notify_event', on_hover)

                    # legend = self.ax_ori.legend(res, loc="upper left", bbox_to_anchor=(1.02, 0, 0.07, 1))
                    # d = {"down": 30, "up": -30}
                    # def func_scroll(evt):
                    #     if legend.contains(evt):
                    #         bbox = legend.get_bbox_to_anchor()
                    #         bbox = Bbox.from_bounds(bbox.x0, bbox.y0 + d[evt.button], bbox.width, bbox.height)
                    #         tr = legend.axes.transAxes.inverted()
                    #         legend.set_bbox_to_anchor(bbox.transformed(tr))
                    #         self.canvas_x5.draw_idle()
                    #
                    # self.canvas_x5.mpl_connect("scroll_event", func_scroll)
                    #
                    # # Integrate the pick event code here
                    # lines = [line for line in self.ax5.get_lines()]
                    # map_legend_to_ax = {}  # Will map legend lines to original lines.
                    #
                    # pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.
                    #
                    # for legend_line, ax_line in zip(legend.get_lines(), lines):
                    #     legend_line.set_picker(pickradius)  # Enable picking on the legend line.
                    #     map_legend_to_ax[legend_line] = ax_line
                    #
                    # def on_pick(event):
                    #     # On the pick event, find the original line corresponding to the legend
                    #     # proxy line, and toggle its visibility.
                    #     legend_line = event.artist
                    #
                    #     # Do nothing if the source of the event is not a legend line.
                    #     if legend_line not in map_legend_to_ax:
                    #         return
                    #
                    #     ax_line = map_legend_to_ax[legend_line]
                    #     visible = not ax_line.get_visible()
                    #     ax_line.set_visible(visible)
                    #     # Change the alpha on the line in the legend, so we can see what lines
                    #     # have been toggled.
                    #     legend_line.set_alpha(1.0 if visible else 0.2)
                    #     self.canvas_x5.draw()
                    #
                    # self.canvas_x5.mpl_connect('pick_event', on_pick)

                    # self.ax_ori.set_ylabel('Hall Sensor')
                    #
                    # self.canvas_x_orientation.draw()
                    # Config.print_with_time("End plotting  at : ")



                    # column_means = df_new_t5.abs().mean()
                    # sensor_mean = [int(i_x) for i_x in column_means]
                    #
                    # for col, data in enumerate(df_new_t5.columns):
                    #     df_new_t5[data] = df_new_t5[data].apply(
                    #         lambda x: x if (x > column_means[data]) or (x < column_means[data]) else 0)

                    # Config.print_with_time("Roll calculation starts at : ")
                    # map_ori_sens_ind, val_ori_sensVal = self.Roll_Calculation(df_new_t5, roll_t_orientation)
                    # Config.print_with_time("Roll calculation ends at : ")

                    # val_ori_sensVal = val_ori_sensVal.astype(int)

                    df_new_t5.columns = [f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]
                    df_elem = pd.DataFrame({"index": index_orientation, "ODDO1": oddo1_tab_orientation,
                                            "ODDO2": oddo2_tab_orientation})
                    frames = [df_elem, df_new_t5]
                    df_new = pd.concat(frames, axis=1, join='inner')

                    # for col in map_ori_sens_ind.columns:
                    #     df_new[col + '_x'] = map_ori_sens_ind[col]

                    # for col in df_new_proximity_ori_lc.columns:
                    #     df_new[col] = df_new_proximity_ori_lc[col]

                    config.print_with_time("End of conversion at : ")
                    # df_new.to_pickle(folder_path + '/' + str(self.weld_num) + '.pkl')
                    # Config.print_with_time("Succesfully saved to pickle file")

                    df_clock_holl_oddo1 = (df_new['ODDO1'] / 1000).round(3)
                    df_clock_index = df_new['index']
                    df_new_1 = df_new[[f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]]

                    fig = go.Figure()
                    for i1, column1 in enumerate(df_new_1):
                        filtered_data = lfilter(b, a, df_new_1[data])
                        fig.add_trace(
                        # for i, data in enumerate(df_new_t5.columns):
                            go.Scatter(x=[df_clock_index, df_clock_holl_oddo1], y=filtered_data, name=column1))
                        # fig.update_layout()
                    fig.update_xaxes(
                        tickfont=dict(size=11),
                        dtick=300,
                        title_text="Absolute Distance(m))",
                        tickangle=0, showticklabels=True, ticklen=0)
                    config.print_with_time("Plotting...")
                    pio.write_html(fig, file='heatmap2.html', auto_open=False)
                    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "heatmap2.html"))
                    self.m_output_orientation.load(QUrl.fromLocalFile(file_path))
                    config.print_with_time("Plotted...")

    """
----->Line chart orientation tab(5) functions ends here
    """


    """
----->Heatmap(sensor VS Oddo) tab(6) functions starts from here
    """
    def graph_analysis_next(self):
        current_index = self.combo_box.currentIndex()
        if current_index < self.combo_box.count() - 1:
            self.combo_box.setCurrentIndex(current_index + 1)
            self.pre_graph_analysis()

    def graph_analysis_previous(self):
        current_index = self.combo_box.currentIndex()
        if current_index > 0:
            self.combo_box.setCurrentIndex(current_index - 1)
            self.pre_graph_analysis()

    def pre_graph_analysis(self):
        config.print_with_time("Pre graph analysis called")
        runid = self.runid
        Weld_id = self.combo_box.currentText()
        self.Weld_id = int(Weld_id)
        self.lower_sensitivity = self.lower_Sensitivity_combo_box.currentText()
        self.upper_sensitivity = self.upper_Sensitivity_combo_box.currentText()

        with connection.cursor() as cursor:
            # query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
            query = "SELECT start_index, end_index,start_oddo1,end_oddo1 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"
            cursor.execute(query, (self.runid, self.Weld_id, self.runid, self.Weld_id))
            result = cursor.fetchall()
            start_oddo1=result[0][2]
            end_oddo1=result[1][3]
            self.pipe_len_8 = end_oddo1 - start_oddo1
            print("Weld_pipe_Length", self.pipe_len_8)

            if not result:
                config.print_with_time("No data found for this pipe ID : ")
            else:
                """
                pkl file is found in local path
                """
                path = config.weld_pipe_pkl + self.project_name + '/' + str(self.Weld_id) + '.pkl'
                if os.path.isfile(path):
                    config.print_with_time("File exist")
                    df_new_8 = pd.read_pickle(path)

                    self.index_tab8 = df_new_8['index']
                    self.oddo1_tab8 = (df_new_8['ODDO1'] - config.oddo1)
                    self.df_new_tab8 = pd.DataFrame(df_new_8, columns=[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)])

                else:
                    """
                    pkl file is not found than data fetch from GCP and save pkl file in local path
                    """
                    folder_path = config.weld_pipe_pkl + self.project_name
                    print(folder_path)
                    config.print_with_time("File not exist")
                    try:
                        os.makedirs(folder_path)
                    except:
                        config.print_with_time("Folder already exists")

                    start_index, end_index = result[0][0], result[1][1]
                    print(start_index, end_index)
                    config.print_with_time("Start fetching at : ")
                    query_for_start = 'SELECT index,ROLL,ODDO1,ODDO2,[F1H1, F1H2, F1H3, F1H4, F2H1, F2H2, F2H3, F2H4,F3H1, F3H2, F3H3, F3H4, F4H1, F4H2, F4H3,F4H4, F5H1, F5H2, F5H3, F5H4, F6H1, F6H2, F6H3, F6H4,F7H1, F7H2, F7H3, F7H4, F8H1, F8H2, F8H3, F8H4, F9H1, F9H2, F9H3, F9H4, F10H1,F10H2, F10H3, F10H4,F11H1, F11H2, F11H3, F11H4, F12H1, F12H2, F12H3, F12H4, F13H1, F13H2, F13H3,F13H4, F14H1, F14H2, F14H3, F14H4,F15H1, F15H2, F15H3, F15H4, F16H1, F16H2, F16H3, F16H4, F17H1, F17H2, F17H3,F17H4, F18H1, F18H2, F18H3, F18H4,F19H1, F19H2, F19H3, F19H4, F20H1, F20H2, F20H3, F20H4, F21H1, F21H2, F21H3,F21H4, F22H1, F22H2, F22H3, F22H4,F23H1, F23H2, F23H3, F23H4, F24H1, F24H2, F24H3, F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4,F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1,F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4] FROM ' + config.table_name + ' WHERE index>{} AND index<{} order by index'
                    query_job = client.query(query_for_start.format(start_index, end_index))
                    results = query_job.result()
                    # results.to_csv("C:/Users/Shradha Agarwal/Desktop/bpcl clock/raw_data.csv")
                    # print("result...", results)

                    data = []
                    self.index_tab8 = []
                    oddo_1 = []
                    oddo_2 = []
                    indexes = []
                    roll1 = []

                    for row in results:
                        self.index_tab8.append(row[0])
                        roll1.append(row[1])
                        oddo_1.append(row[2])
                        oddo_2.append(row[3])
                        data.append(row[4])
                        """
                        Swapping the Pitch data to Roll data
                        """

                    self.oddo1_tab8 = []
                    self.oddo2_tab8 = []
                    self.roll_t8 = []

                    """
                    Reference value will be consider
                    """
                    for odometer1 in oddo_1:
                        od1 = odometer1 - config.oddo1  ###16984.2 change According to run
                        self.oddo1_tab8.append(od1)
                    for odometer2 in oddo_2:
                        od2 = odometer2 - config.oddo2  ###17690.36 change According to run
                        self.oddo2_tab8.append(od2)

                    """
                    Reference value will be consider
                    """
                    for roll2 in roll1:
                        roll3 = roll2 - config.roll_value
                        self.roll_t8.append(roll3)

                    query_for_start = 'SELECT index,[F1P1, F2P2, F3P3, F4P4, F5P1, F6P2, F7P3, F8P4, F9P1, F10P2, F11P3, F12P4, F13P1, F14P2, F15P3, F16P4, F17P1, F18P2, F19P3, F20P4, F21P1, F22P2, F23P3, F24P4, F25P1, F26P2, F27P3, F28P4, F29P1, F30P2, F31P3, F32P4, F33P1, F34P2, F35P3, F36P4] FROM ' + config.table_name + ' WHERE index>{} AND index<{} order by index'
                    query_job = client.query(query_for_start.format(start_index, end_index))
                    results_1 = query_job.result()
                    data1 = []
                    self.index_hm_ori = []
                    for row1 in results_1:
                        self.index_hm_ori.append(row1[0])
                        data1.append(row1[1])

                    self.df_new_proximity_ori = pd.DataFrame(data1, columns=['F1P1', 'F2P2', 'F3P3', 'F4P4', 'F5P1', 'F6P2', 'F7P3', 'F8P4',
                                                                        'F9P1', 'F10P2', 'F11P3', 'F12P4', 'F13P1', 'F14P2', 'F15P3',
                                                                         'F16P4', 'F17P1', 'F18P2', 'F19P3', 'F20P4', 'F21P1', 'F22P2',
                                                                         'F23P3', 'F24P4', 'F25P1', 'F26P2', 'F27P3', 'F28P4', 'F29P1',
                                                                         'F30P2', 'F31P3', 'F32P4', 'F33P1', 'F34P2', 'F35P3', 'F36P4'])

                    self.df_new_tab8 = pd.DataFrame(data, columns=[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)])


                    df_elem = pd.DataFrame({"index": self.index_tab8, "ODDO1": self.oddo1_tab8})
                    frames = [df_elem, self.df_new_tab8]
                    df_new = pd.concat(frames, axis=1, join='inner')

                    for col in self.df_new_proximity_ori.columns:
                        df_new[col] = self.df_new_proximity_ori[col]

                    df_new.reset_index(inplace=True)
                    print("Plotted data", df_new)
                    df_new.to_pickle(folder_path + '/' + str(Weld_id) + '.pkl')
                    config.print_with_time("Succesfully saved to pickle file")

            self.GenerateGraph()

            with connection.cursor() as cursor:
################# defect fetched from defect_sensor_hm #################
                # Fetch_weld_detail = "select id,pipe_id,absolute_distance_oddo1,upstream_oddo1,defect_type,defect_classification,angle_hr_m,length,breadth,depth from defect_sensor_hm where runid='%s' and pipe_id='%s'"

################# defect fetched from defect_clock_hm #################
                Fetch_weld_detail = "select id,pipe_id,absolute_distance,upstream,defect_type,dimension_classification,orientation,length,Width,depth from defect_clock_hm where runid='%s' and pipe_id='%s'"

                cursor.execute(Fetch_weld_detail, (int(self.runid), int(self.Weld_id)))
                self.myTableWidget3.setRowCount(0)
                allSQLRows = cursor.fetchall()
                if allSQLRows:
                    for row_number, row_data in enumerate(allSQLRows):
                        self.myTableWidget3.insertRow(row_number)
                        for column_num, data in enumerate(row_data):
                            self.myTableWidget3.setItem(row_number, column_num,
                                                        QtWidgets.QTableWidgetItem(str(data)))
                            self.myTableWidget3.setContextMenuPolicy(Qt.CustomContextMenu)
                            self.myTableWidget3.customContextMenuRequested.connect(self.open_context_menu)
                            self.myTableWidget3.doubleClicked.connect(self.handle_table_double_click_pipe)

    def GenerateGraph(self):
        graph.generate_heat_map(self.canvas, self.full_screen, self.df_new_tab8,
                                self.line_select_callback3, self.project_name, self.Weld_id, self.figure,
                                self.lower_sensitivity, self.upper_sensitivity, self.oddo1_tab8, self.index_tab8)

    def box_selection_all_defect(self):
        try:
            # Clear existing patches and annotations on the figure
            ax = self.figure.gca()

            # Iterate over all rows in the table
            row_count = self.myTableWidget3.rowCount()
            if row_count == 0:
                QMessageBox.warning(self, "No Data", "The table is empty. No defects to display.")
                return

            for row_number in range(row_count):
                defect_id = self.myTableWidget3.item(row_number, 0).text()
                weld_id = self.Weld_id
                runid = self.runid

                with connection.cursor() as cursor:
                    # query_for_coordinates = "SELECT id, start_observation, end_observation, start_sensor, end_sensor, length, breadth from defect_sensor_hm WHERE pipe_id = %s AND runid = %s AND id = %s"
                    query_for_coordinates = "SELECT id, start_index, end_index, start_sensor, end_sensor, length, Width from defect_clock_hm WHERE pipe_id = %s AND runid = %s AND id = %s"
                    cursor.execute(query_for_coordinates, (weld_id, runid, defect_id))
                    result = cursor.fetchone()

                    id, start_index, end_index, y_start_hm, y_end_hm, length_odd1, breadth = result

                    if None in (start_index, end_index, y_start_hm, y_end_hm):
                        print(f"Warning: Invalid coordinates for defect ID {id}. Skipping.")
                        continue

                    # Calculate rectangle coordinates
                    rect_x = (start_index + end_index) / 2
                    rect_y = (y_start_hm + y_end_hm) / 2

                    # Draw the rectangle
                    rect = plt.Rectangle(
                        (start_index, y_start_hm),
                        end_index - start_index,
                        y_end_hm - y_start_hm,
                        linewidth=1, edgecolor='black', facecolor='none'
                    )
                    ax.add_patch(rect)

                    # Add the text annotation
                    text_x = rect_x
                    text_y = rect_y + (y_end_hm - y_start_hm) * 0.1  # Slightly above the box
                    ax.text(
                        text_x, text_y,
                        # f"ID: {id}\nL: {length_odd1}\nW: {breadth}",
                        f"ID: {id}",
                        color='black',
                        ha='center', va='center',
                        fontsize=10, weight='bold',
                        )
                    # print(f"Rectangle and text drawn for defect ID: {id}.")

            # Refresh the canvas to display all rectangles and annotations
            self.canvas.draw_idle()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to draw boxes for all defects: {str(e)}")

    def handle_table_double_click_pipe(self):
        weld_id = self.Weld_id
        runid = self.runid

        selected_row = self.myTableWidget3.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please double-click on a valid cell.")
            return

        defect_id = self.myTableWidget3.item(selected_row, 0).text()
        try:
            with connection.cursor() as cursor:
                query_for_coordinates = "SELECT id, start_observation, end_observation, start_sensor, end_sensor, length, breadth from defect_sensor_hm WHERE pipe_id = %s AND runid = %s AND id = %s"
                cursor.execute(query_for_coordinates, (weld_id, runid, defect_id))
                result = cursor.fetchone()
                print(f"Query Result: {result}")

                if not result:
                    QMessageBox.warning(self, "No Data", "No data found for the selected defect.")
                    return

                id, start_index, end_index, y_start_hm, y_end_hm, length_odd1, breadth = result

                # Calculate rectangle coordinates
                rect_x = (start_index + end_index) / 2
                rect_y = (y_start_hm + y_end_hm) / 2

                ax = self.figure.gca()
                # Draw the rectangle
                rect = plt.Rectangle(
                    (start_index, y_start_hm),
                    end_index - start_index,
                    y_end_hm - y_start_hm,
                    linewidth=1, edgecolor='black', facecolor='none'
                )
                ax.add_patch(rect)

                # Add the text annotation
                text_x = rect_x
                text_y = rect_y + (y_end_hm - y_start_hm) * 0.1  # Slightly above the box
                ax.text(
                    text_x, text_y,
                    f"ID: {id}\nL: {length_odd1}\nW: {breadth}",
                    color='black',
                    ha='center', va='center',
                    fontsize=10, weight='bold',
                )

                self.canvas.draw_idle()  # Ensure the canvas is updated.

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to draw box: {str(e)}")

    def open_context_menu(self, position):
        index = self.myTableWidget3.indexAt(position)
        if not index.isValid():
            return

        # Select the entire row
        self.myTableWidget3.selectRow(index.row())
        context_menu = QMenu()
        # context_menu = QtWidgets.QMenuBar()
        delete_action = QAction("Delete Row", self)
        # menuEdit = QtWidgets.QMenu(self.menubar)
        delete_action.triggered.connect(lambda: self.delete_row(index.row()))
        context_menu.addAction(delete_action)
        context_menu.exec_(self.myTableWidget3.viewport().mapToGlobal(position))

    def delete_row(self, row):
        if row < 0:
            return

        # Get the ID of the selected row
        id_item = self.myTableWidget3.item(row, 0)
        if id_item is None:
            return
        row_id = id_item.text()

        # Confirm deletion
        reply = QMessageBox.question(self, 'Delete Row', 'Are you sure you want to delete this row?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Delete the row from the database
            with connection.cursor() as cursor:
                # print("row_id....",row_id)
                Fetch_weld_detail = "DELETE from defect_sensor_hm WHERE id='%s'"
                # Execute query.
                cursor.execute(Fetch_weld_detail, (int(row_id)))
                # cursor.execute(f"DELETE from defect_sensor_hm WHERE id=",row_id)
                connection.commit()
                # connection.close()
                # Delete the row from the table widget
                self.myTableWidget3.removeRow(row)
                QMessageBox.information(self, "Information", "Row deleted successfully")

    def reset_btn_fun_pipe(self):
        if self.figure.gca().patches:
            for patch in self.figure.gca().patches:
                patch.remove()
            for text in self.figure.gca().texts:
                text.remove()
            self.canvas.draw()
            self.rect_start_pipe = None  # Store the starting point of the rectangle
            self.rect_end_pipe = None

    def line_select_callback3(self, eclick, erelease):
        self.rect_start_pipe = eclick.xdata, eclick.ydata
        self.rect_end_pipe = erelease.xdata, erelease.ydata
        self.draw_rectangle_3()

    def draw_rectangle_3(self):
        # Function to draw a rectangle on the Matplotlib plot
        if self.rect_start_pipe is not None and self.rect_end_pipe is not None:
            for patch in self.figure.gca().patches:
                patch.remove()
            x_start, y_start = self.rect_start_pipe
            x_end, y_end = self.rect_end_pipe
            if x_start is not None and y_start is not None and x_end is not None and y_end is not None:
                rect = plt.Rectangle(
                    (min(x_start, x_end), min(y_start, y_end)),
                    abs(x_end - x_start),
                    abs(y_end - y_start),
                    edgecolor='black',
                    linewidth=1,
                    fill=False
                )
                self.figure.gca().add_patch(rect)
                self.canvas.draw()
                self.show_name_dialog3()

    def show_name_dialog3(self):
        while True:
            name, ok = QInputDialog.getText(self, 'Enter Name', 'Enter the name of the drawn box:')
            if ok:
                if name.strip():  # Check if the entered name is not empty or just whitespace
                    x_start, y_start = self.rect_start_pipe
                    x_end, y_end = self.rect_end_pipe
                    runid = self.runid
                    pipe = self.Weld_id
                    self.index_hm_set = self.index_tab8
                    start_index15 = self.index_hm_set[round(x_start)]
                    end_index15 = self.index_hm_set[round(x_end)]
                    start_index_c = round(x_start)
                    end_index_c = round(x_end)
                    y_start15 = round(y_start)
                    y_end15 = round(y_end)
                    print("start_sensor", y_start15)
                    print("end_sensor", y_end15)
                    finial_defect_list=[]

                    """
                    Fetching data from Google Big Query each holl sensor
                    """
                    query_for_start = 'SELECT index,ODDO1,ODDO2,[F1H1 ,F1H2 ,F1H3 ,F1H4 ,F2H1 ,F2H2 ,F2H3 ,F2H4 ,F3H1 ,F3H2 ,F3H3 ,F3H4 ,F4H1 ,F4H2 ,F4H3 ,' \
                                      'F4H4 ,F5H1 ,F5H2 ,F5H3 ,F5H4 ,F6H1 ,F6H2 ,F6H3 ,F6H4 ,F7H1 ,F7H2 ,F7H3 ,F7H4 ,F8H1 ,F8H2 ,F8H3 ,' \
                                      'F8H4 ,F9H1 ,F9H2 ,F9H3 ,F9H4 ,F10H1 ,F10H2 ,F10H3 ,F10H4 ,F11H1 ,F11H2 ,F11H3 ,F11H4 ,F12H1 ,F12H2 ,F12H3 ,' \
                                      'F12H4 ,F13H1 ,F13H2 ,F13H3 ,F13H4 ,F14H1 ,F14H2 ,F14H3 ,F14H4 ,F15H1 ,F15H2 ,F15H3 ,F15H4 ,F16H1 ,F16H2 ,F16H3 ,' \
                                      'F16H4 ,F17H1 ,F17H2 ,F17H3 ,F17H4 ,F18H1 ,F18H2 ,F18H3 ,F18H4 ,F19H1 ,F19H2 ,F19H3 ,F19H4 ,F20H1 ,F20H2 ,F20H3 ,' \
                                      'F20H4 ,F21H1 ,F21H2 ,F21H3 ,F21H4 ,F22H1 ,F22H2 ,F22H3 ,F22H4 ,F23H1 ,F23H2 ,F23H3 ,F23H4 ,F24H1 ,F24H2 ,F24H3 ,' \
                                      'F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4,' \
                                      'F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1, ' \
                                      'F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4],ROLL FROM ' + config.table_name + ' WHERE index>={} AND index<={} AND runid={} order by index'
                    query_job = client.query(query_for_start.format(start_index15, end_index15, runid))
                    results = query_job.result()
                    """
                    End fetching data from Google Bigquery
                    """
                    index1 = []
                    oddo_1 = []
                    oddo_2 = []
                    holl_sensor = []
                    roll = []
                    for k in results:
                        index1.append(k[0])
                        oddo_1.append(k[1])
                        oddo_2.append(k[2])
                        holl_sensor.append(k[3])
                        roll.append(k[4])

                    self.oddo1_wp = []
                    self.oddo2_wp = []
                    roll4 = []
                    for odometer1 in oddo_1:
                        od1 = odometer1 - config.oddo1  ### change According to run
                        self.oddo1_wp.append(od1)
                    for odometer2 in oddo_2:
                        od2 = odometer2 - config.oddo2  ### change According to run
                        self.oddo2_wp.append(od2)
                    """
                    Reference value will be consider
                    """
                    for roll2 in roll:
                        roll3 = roll2 - config.roll_value
                        roll4.append(roll3)
                    """
                    Fetching data from Google Big Query each proximity sensor
                    """
                    query_for_start_proximity = 'SELECT index,[F1P1,F2P2,F3P3,F4P4,F5P1,F6P2,F7P3,F8P4,F9P1,F10P2,F11P3,F12P4,F13P1,F14P2,F15P3,F16P4,F17P1,F18P2,F19P3,F20P4,F21P1,F22P2,F23P3,F24P4, F25P1, F26P2, F27P3, F28P4, F29P1, F30P2, F31P3, F32P4, F33P1, F34P2, F35P3, F36P4] FROM ' + config.table_name + ' WHERE index>{} AND index<{} order by index'
                    query_job_proximity = client.query(query_for_start_proximity.format(start_index15, end_index15))
                    results_1 = query_job_proximity.result()
                    proximity = []
                    for row1 in results_1:
                        proximity.append(row1[1])
                    self.df_new_proximity = pd.DataFrame(proximity,
                                                         columns=['F1P1', 'F2P2', 'F3P3', 'F4P4', 'F5P1', 'F6P2', 'F7P3', 'F8P4',
                                                                  'F9P1', 'F10P2', 'F11P3', 'F12P4', 'F13P1', 'F14P2', 'F15P3',
                                                                  'F16P4', 'F17P1', 'F18P2', 'F19P3',
                                                                  'F20P4', 'F21P1', 'F22P2', 'F23P3', 'F24P4', 'F25P1', 'F26P2', 'F27P3', 'F28P4', 'F29P1', 'F30P2',
                                                                  'F31P3', 'F32P4', 'F33P1', 'F34P2', 'F35P3', 'F36P4'])


                    """
                    Calculate Upstream Distance oddo1 and oddo2
                    """
                    upstream_oddo1=self.oddo1_wp[0]-self.oddo1_tab8[0]
                    print("upstream_oddo1=>",upstream_oddo1)

                    """
                    Calculate length of the defect
                    """
                    length_of_defect_oddo1=round(self.oddo1_wp[-1]-self.oddo1_wp[0])
                    length_of_defect_oddo2 = round(self.oddo2_wp[-1] - self.oddo2_wp[0])
                    print("length_of_defect_oddo1=>",length_of_defect_oddo1)
                    print("length_of_defect_oddo2=>",length_of_defect_oddo2)

                    """
                    Calculate Abs.Distance of the defect
                    """
                    Abs_Distance=self.oddo1_wp[0]
                    print("Abs.distance_oddo1=>", Abs_Distance)

                    """
                    Calculate Width of the Defect
                    """
                    Width=Width_calculation(y_start15, y_end15)
                    Width=round(Width)
                    print("Width of Defect=>", Width)

                    """
                    Find the maximum value of each holl sensor
                    """

                    each_holl_sensor_max_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                  0, 0, 0, 0, 0, 0, 0, 0,
                                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                  0, 0, 0, 0, 0, 0, 0, 0,
                                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    # print("start_index", start_index15)
                    # print("end_index", end_index15)
                    # print("start_sensor", y_start15)
                    # print("end_sensor", y_end15)
                    for l, data in enumerate(holl_sensor):
                        for m, data1 in enumerate(data):
                            if m >= y_start15 - 1 and m < y_end15:
                                if data1 > each_holl_sensor_max_value[m]:
                                    each_holl_sensor_max_value[m] = data1
                    #print("maximum_value", each_holl_sensor_max_value)
                    """
                    Get rows of start_observation at the 0th Position of element in holl sensor 2d list
                    """
                    initial_observation = holl_sensor[0]
                    # print("base_value", initial_observation)
                    kx = []
                    for i2 in range(0, 144):
                        if i2 >= y_start15-1 and i2 <y_end15:
                            kx.append(initial_observation[i2])
                        else:
                            kx.append(0)
                    #print("initial_observation", kx)
                    """
                    Difference between max_value_list and initial_observation
                    """
                    zip_object = zip(each_holl_sensor_max_value, kx)
                    difference_list = []
                    for list1_i, list2_i in zip_object:
                        difference_list.append(list1_i - list2_i)
                    # print("difference list",difference_list)
                    """
                    Get max_value_difference_value
                    """

                    max_value_difference_value = max(difference_list)
                    # print("max_value_diiference_value",max_value_difference_value)

                    """
                    Get index max_value_difference_value
                    """
                    max_value_difference_index = difference_list.index(max_value_difference_value)
                    print("sensor_no", max_value_difference_index)
                    """
                    Check max_value_list inside the index and get max_value
                    """
                    max_value = each_holl_sensor_max_value[max_value_difference_index]
                    #print("max_value", max_value)

                    """
                    Check initial_observation inside the index and get base value
                    """
                    base_value=initial_observation[max_value_difference_index]
                    #print("base_value",base_value)

                    depth=(max_value-base_value)/base_value*100
                    depth=round(depth)
                    print("depth...",depth)

                    internal_external=internal_or_external(self.df_new_proximity, max_value_difference_index)
                    print("internal_external",internal_external)

                    """
                    .................Orientation Calculation..........................
                    """
                    angle = defect_angle_x(roll4, max_value_difference_index)
                    print("angle", angle)

                    """
                    Calculate latitude and longitude 
                    """
                    long, lat = lat_long(Abs_Distance, self.runid)
                    print("latitude", lat)
                    print("longitude", long)

                    thickness_pipe = config.pipe_thickness     ### Value Change according to wall thickness
                    dimension_classification=get_type_defect_1(thickness_pipe, runid, length_of_defect_oddo1, Width)
                    print("dimension_classification", dimension_classification)

                    finial_defect_list.append({"start_index": start_index_c, "end_index": end_index_c,
                                               "start_sensor": y_start15, "end_sensor": y_end15,
                                               "sensor_no": max_value_difference_index,
                                               "Absolute_distance": Abs_Distance, "Upstream": upstream_oddo1,
                                               "Pipe_length":self.pipe_len_8,
                                               "Feature_type":internal_external, "Feature_identification": name,
                                               "Dimension_classification": dimension_classification,
                                               "Orientation":angle, "WT":None,
                                               "length": length_of_defect_oddo1, "Width": Width, "Depth_mm": None,
                                               "Depth_percentage":depth, "latitude":lat, "longitude":long})
                    for i in finial_defect_list:
                        start_index = i['start_index']
                        end_index = i['end_index']
                        start_sensor = i['start_sensor']
                        end_sensor = i['end_sensor']
                        sensor_no = i['sensor_no']
                        Absolute_distance = round(i['Absolute_distance'], 2)
                        Upstream = round(i['Upstream'], 2)
                        Pipe_length = round(i['Pipe_length'], 2)
                        Feature_type = i['Feature_type']
                        Feature_identification = i['Feature_identification']
                        Dimension_classification = i['Dimension_classification']
                        Orientation = i['Orientation']
                        WT = i['WT']
                        length = i['length']
                        Width = i['Width']
                        Depth_mm=i['Depth_mm']
                        Depth_percentage=i['Depth_percentage']
                        latitude=i['latitude']
                        longitude=i['longitude']
                        """
                        Insert data into database
                        """
                        with connection.cursor() as cursor:
                            # query_defect_insert = "INSERT into defect_sensor_hm (runid,pipe_id,start_observation,end_observation,start_sensor,end_sensor,sensor_no,absolute_distance_oddo1,Pipe_length,upstream_oddo1,defect_type,type,defect_classification,angle_hr_m,pipe_thickness,length,breadth,depth,latitude,longitude) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

                            # cursor.execute(query_defect_insert, (
                            #     int(runid), pipe, start_index, end_index, start_sensor, end_sensor, sensor_no,
                            #     Absolute_distance, Pipe_length, Upstream, Feature_type, Feature_identification,
                            #     Dimension_classification,
                            #     Orientation, WT, length, Width, Depth_percentage,latitude,longitude))

                            query_defect_insert = "INSERT into defect_clock_hm(runid, pipe_id, pipe_length, start_index, end_index, start_sensor, end_sensor, absolute_distance, upstream, length, Width,depth, orientation, defect_type, dimension_classification,max_value, base_value, latitude, longitude) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                            cursor.execute(query_defect_insert, (
                                int(runid), pipe, Pipe_length, start_index, end_index,
                                    start_sensor, end_sensor, Absolute_distance,
                                    Upstream, length, Width, Depth_percentage, Orientation, Feature_type, Dimension_classification,
                                    latitude, longitude))


                            connection.commit()
                            QMessageBox.information(self, 'Success', 'Data saved')

                        with connection.cursor() as cursor:
################################## defect fetched from defect_sensor_hm ##################################
                            # Fetch_weld_detail = "select id,pipe_id,absolute_distance_oddo1,upstream_oddo1,defect_type,defect_classification,angle_hr_m,length,breadth,depth from defect_sensor_hm where runid='%s' and pipe_id='%s'"

################################## defect fetched from defect_clock_hm ##################################
                            Fetch_weld_detail = "select id,pipe_id,absolute_distance,upstream_oddo1,defect_type,dimension_classification,orientation,length,Width,max_value from defect_clock_hm where runid='%s' and pipe_id='%s'"

                            cursor.execute(Fetch_weld_detail, (int(self.runid), int(self.Weld_id)))
                            self.myTableWidget3.setRowCount(0)
                            allSQLRows = cursor.fetchall()
                            if allSQLRows:
                                for row_number, row_data in enumerate(allSQLRows):
                                    self.myTableWidget3.insertRow(row_number)
                                    for column_num, data in enumerate(row_data):
                                        self.myTableWidget3.setItem(row_number, column_num,
                                                                    QtWidgets.QTableWidgetItem(str(data)))
                                        self.myTableWidget3.setContextMenuPolicy(Qt.CustomContextMenu)
                                        self.myTableWidget3.customContextMenuRequested.connect(self.open_context_menu)
                                        self.myTableWidget3.doubleClicked.connect(self.handle_table_double_click_pipe)

                    break  # Exit the loop if a valid name is provided
                else:
                    QMessageBox.warning(self, 'Invalid Input', 'Please enter a name.')
            else:
                print('Operation canceled.')
                break

    """
---->Heatmap(sensor VS oddo) tab(6) functions ends here
    """

    """
---->Heatmap(clock VS oddo) tab(7) functions starts from here
    """
    def export_to_excel(self):
        """Export table data to an Excel file with a user-selected location and filename."""
        rows = self.myTableWidget_tab9.rowCount()
        columns = self.myTableWidget_tab9.columnCount()

        # Check if the table is empty
        if rows == 0 or columns == 0:
            QMessageBox.warning(self, 'Empty Table', 'The table is empty. Please add data before exporting.')
            return  # Exit the function early

        # Extract table data into a list of dictionaries (for easy conversion to DataFrame)
        data = []
        for row in range(rows):
            row_data = {}
            for col in range(columns):
                header = self.myTableWidget_tab9.horizontalHeaderItem(col).text()
                item = self.myTableWidget_tab9.item(row, col)
                row_data[header] = item.text() if item else ""
            data.append(row_data)

        # Convert the data to a pandas DataFrame
        df = pd.DataFrame(data)

        # Open a file dialog to choose the save location and filename
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Excel File",
            "",
            "Excel Files (*.xlsx);;All Files (*)",
            options=options
        )

        if file_path:  # If the user selects a file
            # Ensure the file has the correct extension
            if not file_path.endswith('.xlsx'):
                file_path += '.xlsx'

            # Save the DataFrame to the selected file
            df.to_excel(file_path, index=False)

            QMessageBox.information(self, 'Success', 'Data successfully saved')
        else:
            QMessageBox.warning(self, 'Cancelled', 'Save operation was cancelled.')

    def tab9_heatmap_next(self):
        current_index = self.combo_tab9.currentIndex()
        if current_index < self.combo_tab9.count() - 1:
            self.combo_tab9.setCurrentIndex(current_index + 1)
            self.tab9_heatmap()

    def tab9_heatmap_previous(self):
        current_index = self.combo_tab9.currentIndex()
        if current_index > 0:
            self.combo_tab9.setCurrentIndex(current_index - 1)
            self.tab9_heatmap()

    def tab9_heatmap(self):
        config.print_with_time("Pre graph analysis called")
        runid = self.runid
        Weld_id_tab9 = self.combo_tab9.currentText()
        self.Weld_id_tab9 = int(Weld_id_tab9)

        with connection.cursor() as cursor:
            # query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
            query = "SELECT start_index, end_index,start_oddo1,end_oddo1 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"
            cursor.execute(query, (self.runid, self.Weld_id_tab9, self.runid, self.Weld_id_tab9))
            result = cursor.fetchall()
            start_oddo1 = result[0][2]
            end_oddo1 = result[1][3]
            self.pipe_len_oddo1_chm = round(end_oddo1 - start_oddo1, 2)

            if not result:
                config.print_with_time("No data found for this pipe ID : ")
            else:
                """
                pkl file is found in local path 
                """
                path = config.clock_pkl + self.project_name + '/' + str(self.Weld_id_tab9) + '.pkl'

                if os.path.isfile(path):
                    config.print_with_time("File exist")
                    df_clock_holl = pd.read_pickle(path)

                    val_ori_sensVal = df_clock_holl[[f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]]
                    self.map_ori_sens_ind = df_clock_holl[[f"{h:02}:{m:02}_x" for h in range(12) for m in range(0, 60, 5)]]
                    self.map_ori_sens_ind.columns = self.map_ori_sens_ind.columns.str.rstrip('_x')

                    # clock_cols = [f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]
                    # window_length = 15
                    # polyorder = 2
                    # for col in clock_cols:
                    #     data = val_ori_sensVal[col].values
                    #     time_index = np.arange(len(val_ori_sensVal))
                    #     coefficients = np.polyfit(time_index, data, polyorder)
                    #     trend = np.polyval(coefficients, time_index)
                    #     data_dettrended = data - trend
                    #     data_denoised = savgol_filter(data_dettrended, window_length, polyorder)
                    #     val_ori_sensVal.loc[:len(val_ori_sensVal), col] = data_denoised

                    self.clock_col = val_ori_sensVal
                    self.clock_data_col = val_ori_sensVal.values.tolist()
                    self.mean_clock_data = val_ori_sensVal.mean().tolist()

                    df3 = ((val_ori_sensVal - self.mean_clock_data)/self.mean_clock_data) * 100

                    self.figure_tab9.clear()  # Clear the previous figure
                    ax2 = self.figure_tab9.add_subplot(111)
                    ax2.figure.subplots_adjust(bottom=0.151, left=0.060, top=0.820, right=1.000)

                    d1 = df3.transpose().astype(float)
                    # d1 = val_ori_sensVal.transpose().astype(float)
                    """
                    Pipewise ranges have been set
                    """
                    # heat_map_obj = sns.heatmap(d1, cmap='jet', ax=ax2)
                    # if Weld_id_tab9 == 2:
                    #     heat_map_obj = sns.heatmap(d1, cmap='jet', ax=ax2, vmin=-5, vmax=18)
                    # else:

                    heat_map_obj = sns.heatmap(d1, cmap='jet', ax=ax2, vmin=-5, vmax=18)

                    """
                    Pipewise ranges have been set
                    """

                    heat_map_obj.set(xlabel="Index", ylabel="Clock")

                    self.oddo1_li_chm = df_clock_holl['ODDO1'].tolist()
                    index_hm = list(df_clock_holl['index'])
                    self.index_chm = index_hm
                    # print("index_chm", self.index_chm)

                    ax2.set_xticklabels(ax2.get_xticklabels(), size=9)
                    ax2.set_yticklabels(ax2.get_yticklabels(), size=9)
                    ax3 = ax2.twiny()
                    oddo_val = [round(elem / 1000, 2) for elem in self.oddo1_li_chm]
                    num_ticks1 = len(ax2.get_xticks())  # Adjust the number of ticks based on your preference
                    # print(num_ticks1)
                    tick_positions1 = [int(i) for i in np.linspace(0, len(oddo_val) - 1, num_ticks1)]
                    # print(tick_positions1)
                    ax3.set_xticks(tick_positions1)
                    ax3.set_xticklabels([f'{oddo_val[i]:.2f}' for i in tick_positions1], rotation=90, size=9)
                    ax3.set_xlabel("Absolute Distance (m)", size=9)
                    def on_hover(event):
                        if event.xdata is not None and event.ydata is not None:
                            try:
                                x = int(event.xdata)
                                y = int(event.ydata)
                                index_value = index_hm[x]
                                clock_val = list(val_ori_sensVal.columns)[y]           ### It shows clock_column values ###
                                clock = self.map_ori_sens_ind.transpose().iloc[y, x]   ### It shows real time values, like clock values at particular point ###
                                value = d1.iloc[y, x]
                                z = self.oddo1_li_chm[x]
                                self.canvas_tab9.toolbar.set_message(f'Index={index_value:.0f},Abs.distance(m)={z/1000:.3f},Clock={clock_val},Value={value:.1f}')
                            except (IndexError, ValueError):
                                # Print a user-friendly message instead of showing an error
                                print("Hovering outside valid data range. No data available.")
                    self.figure_tab9.canvas.mpl_connect('motion_notify_event', on_hover)

                    """
------------------->Heatmap zoom functionality on mouse scroll
                    """
                    # Store original limits
                    # self.original_xlim = ax2.get_xlim()
                    # self.original_ylim = ax2.get_ylim()
                    #
                    # # Zooming functionality
                    # def on_scroll(event):
                    #     if event.xdata is not None and event.ydata is not None:
                    #         scale_factor = 1.1
                    #         cur_xlim = ax2.get_xlim()
                    #         cur_ylim = ax2.get_ylim()
                    #
                    #         xdata = event.xdata
                    #         ydata = event.ydata
                    #
                    #         if event.button == 'up':
                    #             scale_factor = 1 / scale_factor
                    #
                    #         new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
                    #         new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
                    #
                    #         relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
                    #         rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
                    #
                    #         ax2.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
                    #         ax2.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])
                    #
                    #         ax3.set_xlim(ax2.get_xlim())
                    #         self.canvas_heatmap.draw_idle()
                    #
                    # # Override reset button functionality
                    # def reset_view(event=None):
                    #     ax2.set_xlim(self.original_xlim)
                    #     ax2.set_ylim(self.original_ylim)
                    #     ax3.set_xlim(self.original_xlim)
                    #     self.canvas_heatmap.draw_idle()
                    #
                    # self.canvas_heatmap.toolbar.push_current()
                    # self.canvas_heatmap.toolbar.update()
                    # Connect the scroll event
                    # self.figure_heatmap.canvas.mpl_connect('scroll_event', on_scroll)
                    # toolbar_heatmap = self.canvas_heatmap.toolbar
                    # toolbar_heatmap.actions()[0].triggered.connect(reset_view) # Bind reset_view to the reset button

                    self.canvas_tab9.draw()  # Update the canvas with the new plot
                    rs = RectangleSelector(self.figure_tab9.gca(), self.line_select_callback_chm, useblit=True)
                    plt.connect('key_press_event', rs)
                    config.print_with_time("Plotted...")

                    # Show canvas, hide web engine
                    self.canvas_tab9.setVisible(True)
                    self.reset_btn_tab9.setVisible(True)
                    self.all_box_selection1.setVisible(True)
                    self.m_output.setVisible(False)

                    """
------------------->Plolty code for offline heatmap(clock VS oddo) plotting
                    """
                    # df_x = df_clock_holl[['00:00:00_x', '00:05:00_x', '00:10:00_x', '00:15:00_x', '00:20:00_x', '00:25:00_x', '00:30:00_x', '00:35:00_x', '00:40:00_x', '00:45:00_x', '00:50:00_x', '00:55:00_x', '01:00:00_x', '01:05:00_x', '01:10:00_x', '01:15:00_x', '01:20:00_x', '01:25:00_x', '01:30:00_x', '01:35:00_x', '01:40:00_x', '01:45:00_x', '01:50:00_x', '01:55:00_x', '02:00:00_x', '02:05:00_x', '02:10:00_x', '02:15:00_x', '02:20:00_x', '02:25:00_x', '02:30:00_x', '02:35:00_x', '02:40:00_x', '02:45:00_x', '02:50:00_x', '02:55:00_x', '03:00:00_x', '03:05:00_x', '03:10:00_x', '03:15:00_x', '03:20:00_x', '03:25:00_x', '03:30:00_x', '03:35:00_x', '03:40:00_x', '03:45:00_x', '03:50:00_x', '03:55:00_x', '04:00:00_x', '04:05:00_x', '04:10:00_x', '04:15:00_x', '04:20:00_x', '04:25:00_x', '04:30:00_x', '04:35:00_x', '04:40:00_x', '04:45:00_x', '04:50:00_x', '04:55:00_x', '05:00:00_x', '05:05:00_x', '05:10:00_x', '05:15:00_x', '05:20:00_x', '05:25:00_x', '05:30:00_x', '05:35:00_x', '05:40:00_x', '05:45:00_x', '05:50:00_x', '05:55:00_x', '06:00:00_x', '06:05:00_x', '06:10:00_x', '06:15:00_x', '06:20:00_x', '06:25:00_x', '06:30:00_x', '06:35:00_x', '06:40:00_x', '06:45:00_x', '06:50:00_x', '06:55:00_x', '07:00:00_x', '07:05:00_x', '07:10:00_x', '07:15:00_x', '07:20:00_x', '07:25:00_x', '07:30:00_x', '07:35:00_x', '07:40:00_x', '07:45:00_x', '07:50:00_x', '07:55:00_x', '08:00:00_x', '08:05:00_x', '08:10:00_x', '08:15:00_x', '08:20:00_x', '08:25:00_x', '08:30:00_x', '08:35:00_x', '08:40:00_x', '08:45:00_x', '08:50:00_x', '08:55:00_x', '09:00:00_x', '09:05:00_x', '09:10:00_x', '09:15:00_x', '09:20:00_x', '09:25:00_x', '09:30:00_x', '09:35:00_x', '09:40:00_x', '09:45:00_x', '09:50:00_x', '09:55:00_x', '10:00:00_x', '10:05:00_x', '10:10:00_x', '10:15:00_x', '10:20:00_x', '10:25:00_x', '10:30:00_x', '10:35:00_x', '10:40:00_x', '10:45:00_x', '10:50:00_x', '10:55:00_x', '11:00:00_x', '11:05:00_x', '11:10:00_x', '11:15:00_x', '11:20:00_x', '11:25:00_x', '11:30:00_x', '11:35:00_x', '11:40:00_x', '11:45:00_x', '11:50:00_x', '11:55:00_x']]
                    # df_x.columns = df_x.columns.str.rstrip('_x')
                    # # print(df_x)
                    #
                    # # df_x = df_x.applymap(lambda v: f"({v.strip('()').split(', ')[0]}, '{v.strip('()').split(', ')[1]}', '{v.strip('()').split(', ')[2]}')")
                    #
                    # df_clock_index = df_clock_holl['index']
                    # oddo1_tab9 = df_clock_holl['ODDO1']
                    #
                    # # self.figure_tab9.clear()
                    # # ax_1 = self.figure_tab9.add_subplot(111)
                    # # ax_1.figure.subplots_adjust(bottom=0.213, left=0.077, top=0.855, right=1.000)
                    #
                    # Config.print_with_time("Plotting...")
                    # d1 = (val_ori_sensVal.T).astype(float)
                    # fig = go.Figure(data=go.Heatmap(
                    #             x=[df_clock_index, oddo1_tab9],
                    #             y=d1.index,
                    #             z=d1,
                    #             zmin=-10000,
                    #             zmax=18000,
                    #             hovertemplate='Oddo: %{x}<br>Sensor no.: %{text[0]}<br>Actual Ori: %{text[2]}',
                    #             text=[[ast.literal_eval(item) if isinstance(item, str) else item for item in df_x[col]] for col in df_x.columns],
                    #             # text=[[item for item in df_x[col]] for col in df_x.columns],
                    #             colorscale='jet'))
                    #
                    # Config.print_with_time("Plot...")
                    #
                    # # fig = go.Figure(data=heatmap_trace)
                    # fig.update_layout(
                    #                     xaxis_title='Absolute Distance(m)',
                    #                     yaxis_title='Orientation',
                    #                     # title='Heatmap',
                    #                     # dragmode='select',  # Enable box selection mode
                    #                     # autosize=True
                    #                 )
                    #
                    # plotly.offline.plot(fig, filename='h_heatmap_ori.html', auto_open=False)
                    # file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "h_heatmap_ori.html"))
                    # self.m_output.load(QUrl.fromLocalFile(file_path))
                    # self.fig_plot = fig
                    # Config.print_with_time("Plotted...")

                else:
                    """
                    pkl file is not found than data fetch from GCP and save pkl file in local path
                    """
                    folder_path = config.clock_pkl + self.project_name
                    folder_path1 = config.weld_pipe_pkl + self.project_name
                    # print(folder_path)
                    config.print_with_time("File not exist")
                    for path in [folder_path, folder_path1]:
                        try:
                            os.makedirs(path)
                            config.print_with_time(f"Created folder: {path}")
                        except FileExistsError:
                            config.print_with_time(f"Folder already exists: {path}")
                        except Exception as e:
                            config.print_with_time(f"Error creating folder {path}: {e}")

                    start_index, end_index = result[0][0], result[1][1]
                    print(self.Weld_id_tab9)
                    print(start_index, end_index)
                    self.start_pipe_tab9, self.end_pipe_tab9 = start_index, end_index
                    config.print_with_time("Start fetching at : ")

                    query_for_start = 'SELECT index,ROLL,ODDO1,ODDO2,[F1H1, F1H2, F1H3, F1H4, F2H1, F2H2, F2H3, F2H4,F3H1, F3H2, F3H3, F3H4, F4H1, F4H2, F4H3,F4H4, F5H1, F5H2, F5H3, F5H4, F6H1, F6H2, F6H3, F6H4,F7H1, F7H2, F7H3, F7H4, F8H1, F8H2, F8H3, F8H4, F9H1, F9H2, F9H3, F9H4, F10H1,F10H2, F10H3, F10H4,F11H1, F11H2, F11H3, F11H4, F12H1, F12H2, F12H3, F12H4, F13H1, F13H2, F13H3,F13H4, F14H1, F14H2, F14H3, F14H4,F15H1, F15H2, F15H3, F15H4, F16H1, F16H2, F16H3, F16H4, F17H1, F17H2, F17H3,F17H4, F18H1, F18H2, F18H3, F18H4,F19H1, F19H2, F19H3, F19H4, F20H1, F20H2, F20H3, F20H4, F21H1, F21H2, F21H3,F21H4, F22H1, F22H2, F22H3, F22H4,F23H1, F23H2, F23H3, F23H4, F24H1, F24H2, F24H3, F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4,F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1,F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4], PITCH, YAW FROM ' + config.table_name + ' WHERE index>{} AND index<{} order by index'
                    query_job = client.query(query_for_start.format(start_index, end_index))
                    results = query_job.result()
                    # results.to_csv("C:/Users/shrey/Desktop/b.csv")
                    # print("result...", results)

                    config.print_with_time("End fetching  at : ")

                    data = []
                    self.index_tab9 = []
                    oddo_1 = []
                    oddo_2 = []
                    indexes = []
                    roll1 = []
                    pitch1 = []
                    yaw1 = []

                    config.print_with_time("Start of conversion at : ")
                    for row in results:
                        self.index_tab9.append(row[0])
                        roll1.append(row[1])
                        oddo_1.append(row[2])
                        oddo_2.append(row[3])
                        data.append(row[4])
                        pitch1.append(row[5])
                        yaw1.append(row[6])
                        """
                        Swapping the Pitch data to Roll data
                        """

                        # indexes.append(ranges(index_of_occurrences(row['frames'], 1)))

                    self.oddo1_tab9 = []
                    self.oddo2_tab9 = []
                    self.roll_t = []
                    self.pitch_t = []
                    self.yaw_t = []

                    """
                    Reference value will be consider 
                    """
                    for odometer1 in oddo_1:
                        od1 = odometer1 - config.oddo1  ###16984.2 change According to run
                        self.oddo1_tab9.append(od1)
                    for odometer2 in oddo_2:
                        od2 = odometer2 - config.oddo2  ###17690.36 change According to run
                        self.oddo2_tab9.append(od2)

                    """
                    Reference value will be consider
                    """
                    for i in roll1:
                        roll3 = i - config.roll_value
                        self.roll_t.append(roll3)
                    for j in pitch1:
                        pitch3 = j - config.pitch_value
                        self.pitch_t.append(pitch3)
                    for k in yaw1:
                        yaw3 = k - config.yaw_value
                        self.yaw_t.append(yaw3)

                    query_for_start = 'SELECT index,[F1P1,F2P2,F3P3,F4P4,F5P1,F6P2,F7P3,F8P4,F9P1,F10P2,F11P3,F12P4,F13P1,F14P2,F15P3,F16P4,F17P1,F18P2,F19P3,F20P4,F21P1,F22P2,F23P3,F24P4, F25P1, F26P2, F27P3, F28P4, F29P1, F30P2, F31P3, F32P4, F33P1, F34P2, F35P3, F36P4] FROM ' + config.table_name + ' WHERE index>{} AND index<{} order by index'
                    query_job = client.query(query_for_start.format(start_index, end_index))
                    results_1 = query_job.result()
                    data1 = []
                    self.index_hm_orientation = []
                    for row1 in results_1:
                        self.index_hm_orientation.append(row1[0])
                        data1.append(row1[1])
                    # print("start_index.....", start_index)

                    self.df_new_proximity_orientat = pd.DataFrame(data1,
                                                                  columns=['F1P1', 'F2P2', 'F3P3', 'F4P4', 'F5P1', 'F6P2', 'F7P3', 'F8P4',
                                                                  'F9P1', 'F10P2', 'F11P3', 'F12P4', 'F13P1', 'F14P2', 'F15P3',
                                                                  'F16P4', 'F17P1', 'F18P2', 'F19P3',
                                                                  'F20P4', 'F21P1', 'F22P2', 'F23P3', 'F24P4', 'F25P1', 'F26P2', 'F27P3', 'F28P4', 'F29P1', 'F30P2',
                                                                  'F31P3', 'F32P4', 'F33P1', 'F34P2', 'F35P3', 'F36P4'])

                    df_new_tab9 = pd.DataFrame(data, columns=[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)])

                    df_elem = pd.DataFrame({"index": self.index_tab9, "ODDO1": self.oddo1_tab9, "ROLL": self.roll_t, "PITCH": self.pitch_t, "YAW": self.yaw_t})
                    frames = [df_elem, df_new_tab9]
                    df_pipe = pd.concat(frames, axis=1, join='inner')
                    for col in self.df_new_proximity_orientat.columns:
                        df_pipe[col] = self.df_new_proximity_orientat[col]
                    # df_new.reset_index(inplace=True)
                    # print("Plotted data", df_pipe)
                    df_pipe.to_pickle(folder_path1 + '/' + str(Weld_id_tab9) + '.pkl')
                    config.print_with_time("Succesfully saved to sensor pickle file")

                    def extract_int_prefix(s):
                        m = re.match(r'^(\d+)', str(s))
                        return int(m.group(1)) if m else None

                    def get_first_last_integer_column(cols):
                        int_vals = [extract_int_prefix(col) for col in cols]
                        int_vals = [v for v in int_vals if v is not None]
                        if not int_vals:
                            return None, None
                        return min(int_vals), max(int_vals)

                    def manage_directory(directory_path):
                        # Create the directory if it doesn't exist
                        if not os.path.exists(directory_path):
                            os.makedirs(directory_path)
                            print(f"Directory created: {directory_path}")
                        else:
                            print(f"Directory already exists: {directory_path}")

                        # Delete all existing files in the directory
                        for filename in os.listdir(directory_path):
                            file_path = os.path.join(directory_path, filename)
                            try:
                                if os.path.isfile(file_path) or os.path.islink(file_path):
                                    os.unlink(file_path)
                                elif os.path.isdir(file_path):
                                    shutil.rmtree(file_path)
                            except Exception as e:
                                print(f"Failed to delete {file_path}. Reason: {e}")

                        print(f"All files deleted from directory: {directory_path}")

                    # ==============================================================================================================

                    def extract_features(row):
                        x = np.array(row['submatrix'])

                        # Basic stats
                        mean = np.mean(x)
                        std = np.std(x)
                        max_val = np.max(x)
                        min_val = np.min(x)

                        # FFT features
                        fft_vals = np.abs(np.fft.fft(x))
                        fft_features = fft_vals[:10]

                        # Threshold crossings
                        threshold = mean + 2 * std
                        threshold_crossings = np.sum(x > threshold)

                        # Z-score anomalies
                        z_scores = np.abs((x - mean) / (std + 1e-8))
                        anomaly_score = np.mean(z_scores > 3)

                        # CWT Median Feature using pywt.cwt
                        try:
                            x = np.array(x)
                            if x.ndim == 1:
                                side = int(np.sqrt(len(x)))
                                if side * side != len(x):
                                    raise ValueError("Not a perfect square")
                                mat = x.reshape(-1, side)
                            else:
                                mat = x
                        except:
                            mat = np.atleast_2d(x)

                        cwt_medians = []
                        for row_sig in mat:
                            row_sig = np.asarray(row_sig)
                            if row_sig.ndim != 1:
                                continue

                            N = len(row_sig)
                            if N < 5:
                                continue

                            signal_std = np.std(row_sig)
                            max_scale = min(N // 2, max(3, int(signal_std * 10)))
                            if max_scale < 1:
                                continue

                            widths = np.arange(1, max_scale + 1)
                            if len(widths) < 1:
                                continue

                            # ✅ FIXED: use 'gaus1' (not 'guass1') and unpack coeffs and freqs
                            coeffs, freqs = cwt(row_sig, widths, 'gaus1')
                            row_cwt_median = np.median(np.abs(coeffs))
                            cwt_medians.append(row_cwt_median)

                        cwt_final = np.median(cwt_medians) if cwt_medians else 0

                        return [mean, std, max_val, min_val, threshold_crossings, anomaly_score, cwt_final] + list(
                            fft_features)

                    # ==============================================================================================================
                    def model_width(model, folder_path):
                        query = "select id, speed, start_sensor, end_sensor, width_new2 from bb_new"
                        df_meta = pd.read_sql_query(query, connection)
                        df_meta.rename(columns={'id': 'def_no.', 'width_new2': 'pred_width'}, inplace=True)
                        #before
                        df_meta['def_no.'] = df_meta['def_no.'].astype(int)

                        #after
                        # df_meta['def_no.'] = df_meta['def_no.'].astype('Int64')  # Capital 'I'

                        print("Defect numbers in metadata:", df_meta['def_no.'].dropna().unique())
                        #before
                        # meta_dict = {
                        #     int(row['def_no.']): {
                        #         'speed': float(row['speed']),
                        #         'Start_sensor': float(row['start_sensor']),
                        #         'End_sensor': float(row['end_sensor']),
                        #         'pred_width': float(row['pred_width']),
                        #     }
                        #     for _, row in df_meta.iterrows()
                        # }
                        #after
                        meta_dict = {
                            int(row['def_no.']): {
                                'speed': float(row['speed']),
                                'Start_sensor': float(row['start_sensor']),
                                'End_sensor': float(row['end_sensor']),
                                'pred_width': float(row['pred_width']),
                            }
                            for _, row in df_meta.iterrows()
                        }

                        records = []

                        print("🔍 Matching submatrices in:", folder_path)
                        for filename in os.listdir(folder_path):
                            if filename.endswith('.csv') and filename.startswith("submatrix_ptt-"):
                                match = re.search(r'\((\d+),', filename)
                                if not match:
                                    print(f"❌ Skipping (no match): {filename}")
                                    continue

                                defect_no = int(match.group(1))

                                if defect_no not in meta_dict:
                                    print(f"⚠️ Defect {defect_no} not in metadata, skipping.")
                                    continue

                                file_path = os.path.join(folder_path, filename)
                                matrix = pd.read_csv(file_path, dtype=str)
                                matrix = matrix.apply(pd.to_numeric, errors='coerce').fillna(0)

                                flat = matrix.values.flatten().astype(np.float32)
                                flat = (flat - np.mean(flat)) / (np.std(flat) + 1e-8)

                                meta = meta_dict[defect_no]
                                record = {
                                    'filename': filename,
                                    'def_no.': defect_no,
                                    'submatrix': flat.tolist(),
                                    'speed': meta['speed'],
                                    'Start_sensor': meta['Start_sensor'],
                                    'End_sensor': meta['End_sensor'],
                                    'pred_width': meta['pred_width'],
                                }

                                records.append(record)
                        df_test = pd.DataFrame(records)
                        print("✅ Final test dataset shape:", df_test.shape)
                        print(df_test.shape)

                        if model != None:
                            print("Model successfully loaded ")
                        else:
                            print("error loading model")
                        filename = df_test['filename'] if 'filename' in df_test.columns else [f"sample_{i}" for i in
                                                                                              range(len(df_test))]
                        df_test.drop(columns=['filename'], inplace=True, errors='ignore')
                        # df_test['submatrix'] = df_test['submatrix'].apply(lambda s: [float(x) for x in ast.literal_eval(s)])
                        features = df_test.apply(extract_features, axis=1, result_type='expand')
                        feature_columns = ['mean', 'std', 'max', 'min', 'threshold_crossings', 'anomaly_score',
                                           'cwt_median'] + [f'fft_{i}' for i in range(10)]
                        print("Features shape:", features.shape)  # Should be (n_rows, 17)
                        print("Feature columns:", len(feature_columns))  # Should match number of columns

                        features.columns = feature_columns
                        print(feature_columns)
                        print(filename)
                        final_df = pd.concat([features, df_test[['speed', 'Start_sensor', 'End_sensor', 'pred_width']]],
                                             axis=1)
                        final_df.drop(columns=['std'], inplace=True)
                        print(final_df.columns)
                        final_df.rename(columns={"End_sensor": "End_Sensor"}, inplace=True)
                        # pred = model.predict(final_df)
                        pred = np.floor(model.predict(final_df)).astype(int)
                        cursor = connection.cursor()
                        for defect_no, pred_val in zip(df_test['def_no.'], pred):
                            cursor.execute("UPDATE bb_new SET width_statistical = %s WHERE id = %s",
                                           (int(pred_val), int(defect_no)))
                        connection.commit()

                    def breadth(start_sensor, end_sensor):
                        start_sensor1 = start_sensor + 1
                        end_sensor1 = end_sensor + 1
                        if start_sensor1 > end_sensor1 or start_sensor1 == end_sensor1:
                            return 0

                        outer_diameter_1 = config.outer_dia
                        thickness_1 = config.pipe_thickness
                        inner_diameter_1 = outer_diameter_1 - 2 * (thickness_1)
                        radius_1 = inner_diameter_1 / 2

                        theta_2 = config.theta_ang1
                        c_1 = math.radians(theta_2)
                        theta_3 = config.theta_ang2
                        d_1 = math.radians(theta_3)
                        theta_4 = config.theta_ang3
                        e_1 = math.radians(theta_4)

                        x1 = round(radius_1 * c_1, 1)
                        y1 = round(radius_1 * d_1, 1)
                        z1 = round(radius_1 * e_1, 1)
                        print("x1, y1, z1", x1, y1, z1)

                        bredth = 0
                        i = start_sensor1
                        while i < end_sensor1:
                            next_sensor = i
                            if next_sensor % 16 == 0 and next_sensor != end_sensor1:
                                bredth += z1
                            elif next_sensor % 4 == 0:
                                bredth += y1
                            else:
                                bredth += x1
                            i += 1
                        return bredth

                    # def calculate_energy_based_depth(defect_matrix, reference_matrix, pipe_thickness=5.5):
                    #     """
                    #         Estimate depth of defect using energy ratio method.
                    #
                    #         Parameters:
                    #         - defect_matrix (pd.DataFrame): Submatrix where defect is detected (from df3_raw)
                    #         - reference_matrix (pd.DataFrame): Clean reference region (before/after defect)
                    #         - pipe_thickness (float): Wall thickness of the pipe in mm
                    #         Returns:
                    #         - depth_val (float): Estimated depth as percentage of wall thickness
                    #     """
                    #     try:
                    #             if defect_matrix.empty or reference_matrix.empty:
                    #                 return 0
                    #
                    #             # defect_arr = normalize_matrix(defect_matrix.to_numpy())
                    #             # ref_arr = normalize_matrix(reference_matrix.to_numpy())
                    #
                    #             defect_arr = defect_matrix.to_numpy()
                    #             ref_arr = reference_matrix.to_numpy()
                    #
                    #             # Calculate signal energy: sum of squares
                    #             energy_defect = np.sum(np.square(defect_arr))
                    #             energy_ref = np.sum(np.square(ref_arr))
                    #             print("energy_defect:", energy_defect)
                    #             print("energy_ref:", energy_ref)
                    #
                    #             if energy_ref == 0 or pipe_thickness == 0:
                    #                 return 0
                    #
                    #                             # Depth is based on how much stronger the defect signal is
                    #                             # Apply power law scaling
                    #             scaling_exponent = 2.5  # try with this constant also (e.g., 2.4,2.8)
                    #                             # it is giving best with 2.6 with accuracy 72% for tolrence <=10 and for tolrence <=11 giving 77%.
                    #             ratio = energy_defect / energy_ref
                    #             print("ratio : ", ratio)
                    #
                    #             depth = ((ratio ** scaling_exponent) * 100) / pipe_thickness
                    #             print("depth:", depth)
                    #             return round(depth, 2)
                    #
                    #     except Exception as e:
                    #         print("Error in energy-based depth calculation:", e)
                    #         return 0



                    # from scipy.ndimage import gaussian_filter
                    #
                    # def calculate_energy_based_depth(defect_matrix, reference_matrix, pipe_thickness=7.1):              for 12 inch pipe wall thicknes 7.1 right code
                    #     """
                    #     Improved defect depth estimation for 7.1 mm pipe.
                    #     Focus: Higher accuracy by stable scaling.
                    #     """
                    #     try:
                    #         if defect_matrix.empty or reference_matrix.empty:
                    #             return 0
                    #
                    #         # Convert to numpy
                    #         defect_arr = defect_matrix.to_numpy().astype(float)
                    #         ref_arr = reference_matrix.to_numpy().astype(float)
                    #         # defect_arr = gaussian_filter(defect_matrix.to_numpy().T.astype(float), sigma=1.0)
                    #         # ref_arr = gaussian_filter(reference_matrix.to_numpy().T.astype(float), sigma=1.0)
                    #
                    #         # Apply Gaussian smoothing
                    #         defect_arr = gaussian_filter(defect_arr, sigma=1.0)
                    #         ref_arr = gaussian_filter(ref_arr, sigma=1.0)
                    #
                    #         # Energy calculation
                    #         energy_defect = np.sum(np.square(defect_arr))
                    #         energy_ref = np.sum(np.square(ref_arr))
                    #
                    #         if energy_ref == 0:
                    #             return 0
                    #
                    #         # Ratio
                    #         ratio = energy_defect / energy_ref
                    #
                    #         # --- Tuned Formula ---
                    #         scaling_exponent = 3.2  # a bit stronger than before
                    #         calibration_factor = 0.85  # reduce overshoot
                    #
                    #         depth = ((ratio ** scaling_exponent) * 100 / pipe_thickness) * calibration_factor
                    #
                    #         # Clamp between 0–100
                    #         depth = max(min(depth, 100), 0)
                    #
                    #         return round(depth, 2)
                    #
                    #     except Exception as e:
                    #         print("Error in depth calculation:", e)
                    #         return 0









                    # from scipy.ndimage import gaussian_filter
                    #
                    # def calculate_energy_based_depth(defect_matrix, reference_matrix, pipe_thickness=5.5):                   # for 12 inch pipe wall thickness 5.5 code
                    #
                    #     """
                    #     Improved defect depth estimation for 5.5 mm pipe.
                    #     Focus: Higher accuracy by stable scaling.
                    #     """
                    #     try:
                    #         if defect_matrix.empty or reference_matrix.empty:
                    #             return 0
                    #
                    #         # Convert to numpy
                    #         defect_arr = defect_matrix.to_numpy().astype(float)
                    #         ref_arr = reference_matrix.to_numpy().astype(float)
                    #         # defect_arr = gaussian_filter(defect_matrix.to_numpy().T.astype(float), sigma=1.0)
                    #         # ref_arr = gaussian_filter(reference_matrix.to_numpy().T.astype(float), sigma=1.0)
                    #
                    #         # Apply Gaussian smoothing
                    #         defect_arr = gaussian_filter(defect_arr, sigma=1.0)
                    #         ref_arr = gaussian_filter(ref_arr, sigma=1.0)
                    #
                    #         # Energy calculation
                    #         energy_defect = np.sum(np.square(defect_arr))
                    #         energy_ref = np.sum(np.square(ref_arr))
                    #
                    #         if energy_ref == 0:
                    #             return 0
                    #
                    #         # Ratio
                    #         ratio = energy_defect / energy_ref
                    #
                    #         # --- Tuned Formula ---
                    #         scaling_exponent = 2.8   # a bit stronger than before
                    #         calibration_factor = 0.95  # reduce overshoot
                    #
                    #         depth = ((ratio ** scaling_exponent) * 100 / pipe_thickness) * calibration_factor
                    #
                    #         # Clamp between 0–100
                    #         depth = max(min(depth, 100), 0)
                    #
                    #         return round(depth, 2)
                    #
                    #     except Exception as e:
                    #         print("Error in depth calculation:", e)
                    #         return 0




                    import numpy as np
                    from scipy.ndimage import gaussian_filter

                    def calculate_energy_based_depth(defect_matrix, reference_matrix, pipe_thickness=5.5,
                                                     scaling_exponent=3.0, calibration_factor=0.9,
                                                     min_energy_threshold=1e-6, debug=False):
                        """
                        Improved and robust defect depth estimation based on energy ratio method.
                        """
                        try:
                            if defect_matrix.empty or reference_matrix.empty:
                                return 0.0

                            # Convert to numpy arrays
                            defect_arr = defect_matrix.to_numpy().astype(float)
                            ref_arr = reference_matrix.to_numpy().astype(float)

                            # Apply Gaussian filter to smooth data
                            defect_arr = gaussian_filter(defect_arr, sigma=1.0)
                            ref_arr = gaussian_filter(ref_arr, sigma=1.0)

                            # Energy calculation
                            energy_defect = np.sum(np.square(defect_arr))
                            energy_ref = np.sum(np.square(ref_arr))

                            if debug:
                                print(f"Energy (defect): {energy_defect:.4f}, Energy (ref): {energy_ref:.4f}")

                            # Avoid division by zero or too small reference energy
                            if energy_ref < min_energy_threshold:
                                return 0.0

                            # Compute energy ratio
                            ratio = energy_defect / energy_ref

                            if debug:
                                print(f"Energy ratio: {ratio:.4f}")

                            # Depth estimation formula
                            depth = ((ratio ** scaling_exponent) * 100 / pipe_thickness) * calibration_factor

                            # Clamp between 0 and 100
                            depth = max(min(depth, 100), 0)

                            return round(depth, 2)

                        except Exception as e:
                            print("Error in depth calculation:", e)
                            return 0.0




                    def get_adaptive_sigma_refinement(length_percent):
                        """
                        Get refined sigma multipliers based on 5-part length percentage classification:
                        1-10%, 10-20%, 20-30%, 30-40%, 40%+
                        """
                        if 1 <= length_percent < 10:
                            sigma_multiplier = 0.6  # Less aggressive for very small defects
                            refinement_factor = 1.2
                            classification = "Very Small (1-10%)"
                        elif 10 <= length_percent < 20:
                            sigma_multiplier = 0.5  # Slightly more sensitive for small defects
                            refinement_factor = 0.9
                            classification = "Small (10-20%)"
                        elif 20 <= length_percent < 30:
                            sigma_multiplier = 1  # Standard sensitivity
                            refinement_factor = 1.0
                            classification = "Medium (20-30%)"
                        elif 30 <= length_percent < 40:
                            sigma_multiplier = 1.1  # Slightly less sensitive
                            refinement_factor = 0.9
                            classification = "Large (30-40%)"
                        elif length_percent >= 40:
                            sigma_multiplier = 1.2  # Less sensitive for largest defects
                            refinement_factor = 0.8
                            classification = "Very Large (40%+)"
                        else:
                            sigma_multiplier = 0.85
                            refinement_factor = 1.15
                            classification = "Below 1%"
                        return sigma_multiplier, refinement_factor, classification

                    def get_type_defect_1(geometrical_parameter, length_defect, width_defect):
                        L_ratio_W = length_defect / width_defect
                        if width_defect > 3 * geometrical_parameter and length_defect > 3 * geometrical_parameter:
                            type_of_defect = 'GENERAL'
                            return type_of_defect
                        elif (
                                6 * geometrical_parameter >= width_defect >= 1 * geometrical_parameter and 6 * geometrical_parameter >= length_defect >= 1 * geometrical_parameter) and (
                                0.5 < (L_ratio_W) < 2) and not (
                                width_defect >= 3 * geometrical_parameter and length_defect >= 3 * geometrical_parameter):
                            type_of_defect = 'PITTING'
                            return type_of_defect
                        elif (1 * geometrical_parameter <= width_defect < 3 * geometrical_parameter) and (
                                L_ratio_W >= 2):
                            type_of_defect = 'AXIAL GROOVING'
                            return type_of_defect
                        elif L_ratio_W <= 0.5 and 3 * geometrical_parameter > length_defect >= 1 * geometrical_parameter:
                            type_of_defect = 'CIRCUMFERENTIAL GROOVING'
                            return type_of_defect
                        elif 0 < width_defect < 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
                            type_of_defect = 'PINHOLE'
                            return type_of_defect
                        elif 0 < width_defect < 1 * geometrical_parameter and length_defect >= 1 * geometrical_parameter:
                            type_of_defect = 'AXIAL SLOTTING'
                            return type_of_defect
                        elif width_defect >= 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
                            type_of_defect = 'CIRCUMFERENTIAL SLOTTING'
                            return type_of_defect

                    def internal_or_external(df_new_proximity, x):
                        sensor_number = x + 1
                        if sensor_number % 4 == 0:
                            flapper_no = int(sensor_number / 4)
                        else:
                            flapper_no = int(sensor_number / 4) + 1
                        proximity_no = flapper_no % 4
                        if proximity_no == 0:
                            proximity_no = 4
                        proximity_index = 'F' + str(flapper_no) + 'P' + str(proximity_no)
                        print("Proximity_index", proximity_index)
                        maximum_depth_proximity_sensor = df_new_proximity[proximity_index]

                        c = maximum_depth_proximity_sensor.tolist()
                        minimum_value_proximity = min(c)
                        mean_value_proximtiy = mean(c)

                        print("mean_value_proximtiy", mean_value_proximtiy)
                        print("minimum value of proximity", minimum_value_proximity)

                        difference_mean = mean_value_proximtiy - minimum_value_proximity

                        print("difference_minimum2", difference_mean)
                        if difference_mean > 18000:
                            type = "Internal"
                            return type
                        else:
                            type = "External"
                            return type

                    def degrees_to_hours_minutes2(degrees):
                        if (degrees < 0):
                            degrees = degrees % 360
                        elif degrees >= 360:
                            degrees %= 360
                        degrees_per_second = 360 / (12 * 60 * 60)
                        total_seconds = degrees / degrees_per_second
                        hours = int(total_seconds // 3600)
                        minutes = int((total_seconds % 3600) // 60)
                        seconds = int(total_seconds % 60)
                        return f"{hours:02d}:{minutes:02d}"

                    df = pd.read_pickle(folder_path1 + '/' + str(Weld_id_tab9) + '.pkl')
                    data_x = df.fillna(method='ffill')
                    df_new_proximity = pd.DataFrame(df, columns=['F1P1', 'F2P2', 'F3P3', 'F4P4', 'F5P1', 'F6P2', 'F7P3',
                                                                 'F8P4',
                                                                 'F9P1', 'F10P2', 'F11P3', 'F12P4', 'F13P1', 'F14P2',
                                                                 'F15P3', 'F16P4',
                                                                 'F17P1', 'F18P2', 'F19P3', 'F20P4', 'F21P1', 'F22P2',
                                                                 'F23P3', 'F24P4',
                                                                 'F25P1', 'F26P2', 'F27P3', 'F28P4', 'F29P1', 'F30P2',
                                                                 'F31P3', 'F32P4',
                                                                 'F33P1', 'F34P2', 'F35P3', 'F36P4'])

                    roll = data_x['ROLL'].tolist()
                    roll1 = []
                    for i in roll:
                        roll1.append(i)
                    roll_dictionary = {'1': roll1}
                    angle = [round(i * 2.5, 1) for i in range(0, 144)]

                    for i in range(2, 145):
                        current_values = [round((value + angle[i - 1]), 2) for value in roll1]
                        roll_dictionary['{}'.format(i)] = current_values

                    clock_dictionary = {}
                    for key in roll_dictionary:
                        clock_dictionary[key] = [degrees_to_hours_minutes2(value) for value in roll_dictionary[key]]

                    Roll_hr = pd.DataFrame(clock_dictionary)
                    Roll_hr.columns = [f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]

                    oddometer1 = ((data_x['ODDO1'] - config.oddo1_ref) / 1000).round(3)
                    df3_raw = data_x[[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)]]
                    df2 = data_x[[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)]]
                    print("Calculating sigma thresholds using original proven method...")
                    mean1 = df2.mean().tolist()
                    standard_deviation = df2.std(axis=0, skipna=True).tolist()

                    mean_plus_1sigma = []
                    for i, data1 in enumerate(mean1):
                        sigma1 = data1 + (config.positive_sigma_col) * standard_deviation[i]
                        mean_plus_1sigma.append(sigma1)

                    mean_negative_3sigma = []
                    for i_2, data_3 in enumerate(mean1):
                        sigma_3 = data_3 - (config.negative_sigma) * standard_deviation[i_2]
                        mean_negative_3sigma.append(sigma_3)
                    for col, data in enumerate(df2.columns):
                        df2[data] = df2[data].apply(
                            lambda x: 1 if x > mean_plus_1sigma[col] else (-1 if x < mean_negative_3sigma[col] else 0))

                    clock_cols = [f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]
                    df2.columns = clock_cols
                    filtered_df1 = df2
                    # CONTINUE WITH ORIGINAL PROCESSING
                    df3_raw.columns = filtered_df1.columns
                    df1_aligned = filtered_df1.reindex(df3_raw.index)
                    result = df1_aligned * df3_raw
                    result = result.dropna()
                    result.reset_index(drop=True, inplace=True)

                    result_raw_df = result.mask(result == 0, df3_raw)
                    result_raw_df = result_raw_df.dropna()
                    result_raw_df.reset_index(drop=True, inplace=True)

                    mean_clock_data = result_raw_df.mean().tolist()
                    val_ori_raw = ((result_raw_df - mean_clock_data) / mean_clock_data) * 100
                    # Save CSV for PTT Software
                    ptt_csv = result.copy()
                    ptt_csv['ODDO1'] = data_x['ODDO1']
                    prefix = '_x'
                    for col in Roll_hr.columns:
                        ptt_csv[col + prefix] = Roll_hr[col]
                    for col in df_new_proximity.columns:
                        ptt_csv[col] = df_new_proximity[col]

                    # ORIGINAL CLUSTERING IMPLEMENTATION
                    t = result.transpose()
                    t_raw = val_ori_raw.transpose()
                    data_array = t.to_numpy(dtype=np.float64)

                    def dfs(matrix, x, y, visited, cluster):
                        """Perform DFS to find clusters, but only include positive values."""
                        stack = [(x, y)]
                        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                        while stack:
                            cx, cy = stack.pop()
                            if (cx, cy) in visited:
                                continue
                            if matrix[cx, cy] <= 0:
                                continue
                            visited.add((cx, cy))
                            cluster.append((cx, cy))
                            for dx, dy in directions:
                                nx, ny = cx + dx, cy + dy
                                if (0 <= nx < matrix.shape[0] and 0 <= ny < matrix.shape[1] and
                                        matrix[nx, ny] > 0 and (nx, ny) not in visited):
                                    stack.append((nx, ny))

                    # Find clusters of connected non-zero values and calculate bounding boxes
                    def merge_all_overlapping_boxes(boxes, max_distance=3):
                        merged = []
                        while boxes:
                            current = boxes.pop(0)
                            overlap_found = True
                            while overlap_found:
                                overlap_found = False
                                i = 0
                                while i < len(boxes):
                                    if do_boxes_overlap_or_close(current, boxes[i], max_distance):
                                        current = merge_boxes(current, boxes[i])
                                        boxes.pop(i)
                                        overlap_found = True
                                    else:
                                        i += 1
                            merged.append(current)
                        return merged

                    def do_boxes_overlap_or_close(box1, box2, max_distance=3):
                        return do_boxes_overlap(box1, box2) or boxes_are_close(box1, box2, max_distance)

                    def boxes_are_close(box1, box2, max_distance=3):
                        # Compute closest horizontal and vertical distances between boxes
                        h_dist = max(0, max(box1['start_col'] - box2['end_col'], box2['start_col'] - box1['end_col']))
                        v_dist = max(0, max(box1['start_row'] - box2['end_row'], box2['start_row'] - box1['end_row']))
                        return (h_dist + v_dist) <= max_distance

                    def do_boxes_overlap(box1, box2):
                        """Check if two bounding boxes overlap."""
                        return not (box1['end_row'] < box2['start_row'] or
                                    box1['start_row'] > box2['end_row'] or
                                    box1['end_col'] < box2['start_col'] or
                                    box1['start_col'] > box2['end_col'])

                    def merge_boxes(box1, box2):
                        """Merge two overlapping bounding boxes into one."""
                        return {
                            'start_row': min(box1['start_row'], box2['start_row']),
                            'end_row': max(box1['end_row'], box2['end_row']),
                            'start_col': min(box1['start_col'], box2['start_col']),
                            'end_col': max(box1['end_col'], box2['end_col'])
                        }

                    print("Performing clustering to detect defect regions...")
                    visited = set()
                    bounding_boxes = []

                    for i in range(data_array.shape[0]):
                        for j in range(data_array.shape[1]):
                            if data_array[i, j] != 0 and (i, j) not in visited:
                                cluster = []
                                dfs(data_array, i, j, visited, cluster)
                                if cluster:
                                    min_row = min(point[0] for point in cluster)
                                    max_row = max(point[0] for point in cluster)
                                    min_col = min(point[1] for point in cluster)
                                    max_col = max(point[1] for point in cluster)
                                    bounding_boxes.append(
                                        {'start_row': min_row, 'end_row': max_row, 'start_col': min_col,
                                         'end_col': max_col})
                    merged_boxes = merge_all_overlapping_boxes(bounding_boxes)
                    df_sorted = pd.DataFrame(merged_boxes).sort_values(by='start_col')

                    df_clock_holl_oddo1 = data_x['ODDO1']
                    oddo1_li = list(oddometer1)
                    sensor_numbers = list(range(1, len(t.index) + 1))  # 1 to 144
                    sensor_numbers = sensor_numbers[::-1]  # Reverse the list to go top=0 → bottom=144
                    # Create a 2D text matrix where each row has the same sensor number
                    text = np.array([[f"{sensor_no}"] * t.shape[1] for sensor_no in sensor_numbers])
                    figx112 = go.Figure(data=go.Heatmap(
                        z=t_raw,
                        y=t.index,
                        x=[t.columns, oddo1_li],
                        text=text,
                        hovertemplate='Oddo: %{x}<br>Clock:%{y}<br>Value: %{z}, sensor no: %{text}',
                        zmin=-5,
                        zmax=18,
                        colorscale='jet',
                    ))
                    print("Calculating threshold values for defect validation...")
                    max_submatrix_list = []
                    min_submatrix_list = []

                    for _, row in df_sorted.iterrows():
                        start_sensor = row['start_row']
                        end_sensor = row['end_row']
                        start_reading = row['start_col']
                        end_reading = row['end_col']
                        if start_sensor == end_sensor:
                            pass
                        else:
                            try:
                                submatrix = result.iloc[start_reading:end_reading + 1, start_sensor:end_sensor + 1]
                                submatrix = submatrix.apply(pd.to_numeric, errors='coerce')
                                if submatrix.isnull().values.any():
                                    continue
                                max_value = submatrix.max().max()
                                max_submatrix_list.append(max_value)
                                two_d_list = submatrix.values.tolist()
                                min_positive = min(x for row in two_d_list for x in row if x > 0)
                                min_submatrix_list.append(min_positive)
                            except Exception as e:
                                pass

                    max_of_all = max(max_submatrix_list)
                    min_of_all = min(min_submatrix_list)
                    threshold_value = round(min_of_all + (max_of_all - min_of_all) * config.defect_box_thresh)

                    print(f"Base threshold calculated: {threshold_value}")
                    print("Processing defects with 3-part length classification...")

                    # PROCESS DEFECTS WITH ADAPTIVE REFINEMENT
                    finial_defect_list = []
                    defect_counter = 1
                    submatrices_dict = {}
                    classification_stats = {
                        "Very Small (1-10%)": {"count": 0, "total_processed": 0},
                        "Small (10-20%)": {"count": 0, "total_processed": 0},
                        "Medium (20-30%)": {"count": 0, "total_processed": 0},
                        "Large (30-40%)": {"count": 0, "total_processed": 0},
                        "Very Large (40%+)": {"count": 0, "total_processed": 0},
                        "Below 1%": {"count": 0, "total_processed": 0}
                    }
                    for _, row in df_sorted.iterrows():
                        start_sensor = row['start_row']
                        end_sensor = row['end_row']
                        start_reading = row['start_col']
                        end_reading = row['end_col']
                        if start_sensor == end_sensor:
                            continue
                        try:
                            submatrix = result.iloc[start_reading:end_reading + 1, start_sensor:end_sensor + 1]
                            submatrix = submatrix.apply(pd.to_numeric, errors='coerce')
                            two_d_list = submatrix.values.tolist()
                            max_value = submatrix.max().max()
                            min_positive = min(x for row in two_d_list for x in row if x > 0)
                            # CALCULATE LENGTH_PERCENT FIRST
                            counter_difference = end_reading - start_reading
                            divid = int(counter_difference / 2)
                            center = start_reading + divid
                            factor = divid * config.l_per_1
                            start = int(center - factor)
                            end = int(center + factor)
                            length_percent = (df_clock_holl_oddo1[end] - df_clock_holl_oddo1[start])
                            sigma_multiplier, refinement_factor, classification = get_adaptive_sigma_refinement(length_percent)
                            adjusted_threshold = threshold_value * sigma_multiplier
                            valid_columns = 0
                            for col_idx in range(start_sensor, end_sensor + 1):
                                adaptive_sigma = mean1[col_idx] + (sigma_multiplier * standard_deviation[col_idx])
                                if submatrix.iloc[:, col_idx - start_sensor].max() > adaptive_sigma:
                                    valid_columns += 1
                                if valid_columns / (end_sensor - start_sensor + 1) < 0.3:
                                    print(f"✗ Defect rejected: Only {valid_columns} columns passed adaptive threshold")
                                    continue
                            classification_stats[classification]["total_processed"] += 1
                            print(f"Defect {defect_counter}: Length={length_percent:.1f}mm, Class={classification}, Threshold={adjusted_threshold:.1f}")
                            if (adjusted_threshold <= max_value <= max_of_all):
                                print(f"✓ Defect accepted with {classification} settings")

                                # CONTINUE WITH ALL ORIGINAL PROCESSING LOGIC
                                depth_old = (max_value - min_positive) / min_positive * 100
                                max_column = submatrix.max().idxmax()
                                max_index = submatrix.columns.get_loc(max_column)

                                start_oddo1 = df_clock_holl_oddo1[start_reading]
                                end_oddo1 = (df_clock_holl_oddo1[end_reading]) / 1000
                                time_sec = end_reading / 1500
                                speed = end_oddo1 / time_sec

                                base_value = mean1[max_index]
                                internal_external = internal_or_external(df_new_proximity, max_index)
                                absolute_distance = df_clock_holl_oddo1[start_reading]
                                upstream = df_clock_holl_oddo1[start_reading] - df_clock_holl_oddo1[0]
                                length = (df_clock_holl_oddo1[end_reading] - df_clock_holl_oddo1[start_reading])

                                counter_difference_1 = (end_sensor + 1) - (start_sensor + 1)
                                divid_1 = int(counter_difference_1 / 2)
                                center_1 = start_sensor + divid_1
                                factor1_1 = divid_1 * config.w_per_1
                                start1_1 = (int(center_1 - factor1_1)) - 1
                                end1_1 = (int(center_1 + factor1_1)) - 1

                                width = breadth(start_sensor, end_sensor)

                                geometrical_parameter = config.pipe_thickness
                                dimension_classification = get_type_defect_1(geometrical_parameter, length, width)

                                avg_counter = round((start + end) / 2)
                                avg_sensor = round((start1_1 + end1_1) / 2)
                                orientation = Roll_hr.iloc[avg_counter, avg_sensor]

                                inner_diameter = config.outer_dia - 2 * config.pipe_thickness
                                radius = inner_diameter / 2
                                x1 = round(radius * math.radians(config.theta_ang1), 1)
                                y1 = round(radius * math.radians(config.theta_ang2), 1)
                                z1 = round(radius * math.radians(config.theta_ang3), 1)

                                df_copy_submatrix = df3_raw.iloc[start_reading:end_reading + 1, start_sensor:end_sensor + 1]
                                ref_start = max(0, start_reading - (end_reading - start_reading))
                                ref_end = start_reading - 1
                                reference_matrix = df3_raw.iloc[ref_start:ref_end + 1, start_sensor:end_sensor + 1]
                                depth_val1 = calculate_energy_based_depth(df_copy_submatrix, reference_matrix,
                                                                          config.pipe_thickness)
                                depth_val1 = min(depth_val1, 100)

                            def replace_first_column(df_n, s_sensor, e_sensor):
                                s_sensor = s_sensor + 1
                                e_sensor = e_sensor + 1
                                # Generate new column names within the given range
                                new_columns = list(range(s_sensor, s_sensor + df_n.shape[1]))
                                # Assign new column names
                                df_n.columns = new_columns
                                # Drop the last column if it exceeds end_sensor
                                df_n = df_n.loc[:, df_n.columns <= e_sensor]
                                return df_n
                            df_duplicate = replace_first_column(df_copy_submatrix, start_sensor, end_sensor)
                            df_duplicate.columns = df_duplicate.columns.astype(str)

                            def process_csv_interpolate(df_dupe):
                                """
                                Like the original process_csv, but uses interpolation (linear or cubic)
                                instead of duplication for the new columns. Suffixes and column names are
                                generated exactly as in the original code, with robust end-case handling.
                                """
                                new_data = {}
                                next_col = None

                                # Use your previously computed distances
                                base = round(x1 / config.div_factor)
                                c = round(y1 / config.div_factor)
                                dee = round(z1 / config.div_factor)

                                c1 = c // 2
                                c2 = c - c1
                                dee1 = dee // 2
                                dee2 = dee - dee1

                                def generate_suffixes(n):
                                    return [chr(ord('a') + i) for i in range(int(n))]

                                base_suffixes = generate_suffixes(int(base))
                                c1_suffixes = generate_suffixes(int(c1))
                                c2_suffixes = generate_suffixes(int(c2))
                                dee1_suffixes = generate_suffixes(int(dee1))
                                dee2_suffixes = generate_suffixes(int(dee2))

                                for colu in df_dupe.columns:
                                    col_int = int(colu)
                                    next_col = str(col_int + 1)

                                    if next_col in df_dupe.columns:
                                        col_vals = df_dupe[colu].values
                                        next_col_vals = df_dupe[next_col].values

                                        def interpolate_between(a, b, n, kind='cubic'):
                                            # For short arrays, always use linear
                                            if n == 0:
                                                return np.empty((0, len(a)))
                                            x = np.array([0, 1])
                                            arr = np.vstack([a, b]).T
                                            interpolated = []
                                            for row in arr:
                                                # If both points are the same, just duplicate
                                                if np.allclose(row[0], row[1]):
                                                    interpolated.append(np.full(n, row[0]))
                                                    continue
                                                # Use cubic only if possible, otherwise linear
                                                if kind == 'cubic' and n >= 3:
                                                    try:
                                                        f = interp1d(x, row, kind='cubic', fill_value="extrapolate")
                                                    except Exception:
                                                        f = interp1d(x, row, kind='linear', fill_value="extrapolate")
                                                else:
                                                    f = interp1d(x, row, kind='linear', fill_value="extrapolate")
                                                xs = np.linspace(0, 1, n + 2)[1:-1] if n > 0 else []
                                                interpolated.append(f(xs) if len(xs) > 0 else [])
                                            return np.array(interpolated).T if n > 0 else np.empty((0, len(a)))

                                        # Special Case 1: Between flappers (multiples of 4, not 16)
                                        if col_int % 4 == 0 and col_int % 16 != 0:
                                            c1_interp = interpolate_between(col_vals, next_col_vals, len(c1_suffixes),
                                                                            kind='cubic')
                                            for idx, suffix in enumerate(c1_suffixes):
                                                new_data[f"{col_int}{suffix}_extra"] = c1_interp[idx] if c1_interp.shape[
                                                                                                             0] > 0 else col_vals
                                            c2_interp = interpolate_between(next_col_vals, col_vals, len(c2_suffixes),
                                                                            kind='cubic')
                                            for idx, suffix in enumerate(c2_suffixes):
                                                new_data[f"{int(next_col)}{suffix}_extra"] = c2_interp[idx] if \
                                                c2_interp.shape[0] > 0 else next_col_vals

                                        # Special Case 2: Between arms (multiples of 16)
                                        elif col_int % 16 == 0:
                                            dee1_interp = interpolate_between(col_vals, next_col_vals, len(dee1_suffixes),
                                                                              kind='cubic')
                                            for idx, suffix in enumerate(dee1_suffixes):
                                                new_data[f"{col_int}{suffix}_extra2"] = dee1_interp[idx] if \
                                                dee1_interp.shape[0] > 0 else col_vals
                                            dee2_interp = interpolate_between(next_col_vals, col_vals, len(dee2_suffixes),
                                                                              kind='cubic')
                                            for idx, suffix in enumerate(dee2_suffixes):
                                                new_data[f"{int(next_col)}{suffix}_extra2"] = dee2_interp[idx] if \
                                                dee2_interp.shape[0] > 0 else next_col_vals

                                        # Base case: Normal sensor spacing
                                        else:
                                            base_interp = interpolate_between(col_vals, next_col_vals, len(base_suffixes),
                                                                              kind='cubic')
                                            for idx, suffix in enumerate(base_suffixes):
                                                new_data[f"{col_int}{suffix}"] = base_interp[idx] if base_interp.shape[
                                                                                                         0] > 0 else col_vals

                                new_df_duplicate = pd.DataFrame(new_data, index=df_dupe.index)
                                return new_df_duplicate

                            def process_submatrix(df_diff):
                                if df_diff.isnull().values.any():
                                    return None

                                # try:
                                #     max_val = df_diff.max().max()
                                #     min_pos_val = df_diff[df_diff > 0].min().min()
                                #     signal_strength = np.log10(max_val + 1)  # Avoid log(0)
                                # except:
                                #     max_val = None
                                #     min_pos_val = None
                                #     signal_strength = 0

                                ### STDEV ON DEFECT MATRIX ROW-WISE ###
                                # print("df_diff", df_diff)
                                # df_diff = df_diff.applymap(lambda x: np.log(x) if x > 0 else np.nan)
                                # adaptive_sigma_row = get_adaptive_sigma_row_values(length_percent)
                                # ratio = round((max_val - min_pos_val) / (min_pos_val + 1e-5), 2)
                                # sigma_multiplier, _, _ = get_adaptive_sigma_refinement(length_percent)
                                # effective_positive_sigma_row = adaptive_sigma_row * positive_sigma_row

                                df_diff_mean = list(df_diff.median(axis=1))
                                df_std_dev = list(df_diff.std(axis=1, ddof=1))
                                mean_plus_std = list(
                                    map(lambda x, y: x + y * (config.positive_sigma_row), df_diff_mean, df_std_dev))
                                # mean_plus_std = list(map(lambda x, y: x * (positive_sigma_row), df_diff_mean, df_std_dev))
                                mean_plus_std_series = pd.Series(mean_plus_std, index=df_diff.index)
                                # mean_neg_std = list(map(lambda x, y: x - y * (negative_sigma_row), df_diff_mean, df_std_dev))
                                # mean_neg_std_series = pd.Series(mean_neg_std, index=df_diff.index)
                                # Apply the function row-wise
                                df_result = df_diff.apply(
                                    lambda row: row.map(lambda x: 1 if x > mean_plus_std_series[row.name] else 0), axis=1)

                                ### STDEV ON DEFECT MATRIX COLUMN-WISE ###
                                # df_diff_mean = df_diff.median(axis=0).tolist()
                                # df_std_dev = df_diff.std(axis=0, skipna=True, ddof=1).tolist()
                                # mean_plus_std = []
                                # for i_std, data_std in enumerate(df_diff_mean):
                                #     sigma_std_col = data_std + (positive_sigma_row * df_std_dev[i_std])
                                #     mean_plus_std.append(sigma_std_col)
                                # df_result = pd.DataFrame(index=df_diff.index)
                                # for col1_std, data1_std in enumerate(df_diff.columns):
                                #     df_result[data1_std] = df_diff[data1_std].apply(lambda x: 1 if x > mean_plus_std[col1_std] else 0)

                                count_ones_per_column = df_result.sum(axis=0)
                                first_col_with_1 = count_ones_per_column.ne(0).idxmax()
                                last_col_with_1 = count_ones_per_column[::-1].ne(0).idxmax()
                                first_col_with_1_idx = df_result.columns.get_loc(first_col_with_1)
                                last_col_with_1_idx = df_result.columns.get_loc(last_col_with_1)

                                df_between = df_result.iloc[:, first_col_with_1_idx:last_col_with_1_idx + 1]
                                # Count columns that have at least one '1'
                                num_cols_with_ones = (df_between == 1).any(axis=0).sum()
                                num_cols_between = last_col_with_1_idx - first_col_with_1_idx + 1

                                # Step 3: Count the number of columns to remove from start and end
                                num_cols_to_remove_start = first_col_with_1_idx
                                num_cols_to_remove_end = len(count_ones_per_column) - 1 - last_col_with_1_idx

                                width_1_only = round(num_cols_with_ones * config.div_factor)
                                width_0_yes = round(num_cols_between * config.div_factor)
                                print("width_1_only", width_1_only)
                                print("width_0_yes", width_0_yes)
                                trimmed_original_matrix = df_diff.iloc[:, first_col_with_1_idx: last_col_with_1_idx + 1]
                                new_start_sensor = start1_1 + num_cols_to_remove_start
                                new_end_sensor = end1_1 - num_cols_to_remove_end
                                return trimmed_original_matrix, width_1_only, width_0_yes, new_start_sensor, new_end_sensor

                            def slope_filter(df_diff):
                                refined_outputs = {}
                                width_0_no = 0
                                width_0_no1 = 0
                                try:
                                    if df_diff.isnull().values.any():
                                        return None
                                    # q1 = df_diff.quantile(0.25)
                                    # q3 = df_diff.quantile(0.75)
                                    # iqr = q3 - q1
                                    # iqr_threshold = iqr[iqr > 0].mean()
                                    # important_cols_iqr = iqr[iqr > iqr_threshold].index
                                    # refined_outputs['iqr'] = df_diff[important_cols_iqr]

                                    slope_strength = df_diff.diff().abs().sum()
                                    slope_threshold = slope_strength.mean() * (config.slope_per)
                                    important_cols_slope = slope_strength[slope_strength > slope_threshold].index
                                    refined_outputs['slope'] = df_diff[important_cols_slope]

                                    width_0_no = (len(important_cols_slope) - 1) * config.div_factor
                                    # width_0_no1 = (len(important_cols_iqr) - 1) * div_factor
                                except Exception as e:
                                    refined_outputs['slope'] = None
                                    # refined_outputs['iqr'] = None
                                    print("Method failed:", e)
                                return refined_outputs, width_0_no

                            modified_df = process_csv_interpolate(df_duplicate)
                            refined_output, width_slope = slope_filter(modified_df)
                            trimmed_matrix, width_1_only, width_0_yes, new_start_sensor, new_end_sensor = process_submatrix(modified_df)
                            new_start_sensor, new_end_sensor = get_first_last_integer_column(trimmed_matrix.columns)
                            mapped_start_sensor = len(t.index) - start_sensor
                            mapped_end_sensor = len(t.index) - end_sensor
                            if mapped_end_sensor < mapped_start_sensor:
                                mapped_start_sensor, mapped_end_sensor = mapped_end_sensor, mapped_start_sensor

                            width = breadth(mapped_start_sensor, mapped_end_sensor)

                            try:
                                depth_val = round((((length / width) * (max_value / base_value)) * 100) / config.pipe_thickness)
                            except:
                                depth_val = 0

                            if depth_val > 1 and width > 1 and length > 1:
                                classification_stats[classification]["count"] += 1
                                submatrices_dict[(defect_counter, start_sensor, end_sensor)] = modified_df

                                print(f"✓ Valid defect: depth={depth_val}%, width={width}mm, length={length}mm")

                                runid = 1
                                finial_defect_list.append({
                                    "runid": runid,
                                    "start_reading": start_reading,
                                    "end_reading": end_reading,
                                    "start_sensor": mapped_start_sensor,
                                    "end_sensor": mapped_end_sensor,
                                    "absolute_distance": absolute_distance,
                                    "upstream": upstream,
                                    "length": length,
                                    "length_percent": length_percent,
                                    "breadth": width,
                                    "width_new": width_slope,
                                    "width_new2": round(width_1_only, 0),
                                    "orientation": orientation,
                                    "defect_type": internal_external,
                                    "dimension_classification": dimension_classification,
                                    "depth": depth_val1,
                                    "depth_old": depth_old,
                                    "start_oddo1": start_oddo1,
                                    "end_oddo1": end_oddo1,
                                    "speed": speed,
                                    "Min_Val": min_positive,
                                    "Max_Val": max_value
                                })

                                # Color-code defects by classification
                                if classification == "Very Small (1-10%)":
                                    color = 'purple'
                                elif classification == "Small (10-20%)":
                                    color = 'red'
                                elif classification == "Medium (20-30%)":
                                    color = 'orange'
                                elif classification == "Large (30-40%)":
                                    color = 'yellow'
                                elif classification == "Very Large (40%+)":
                                    color = 'blue'
                                else:
                                    color = 'gray'

                                figx112.add_shape(
                                    type='rect',
                                    x0=start_reading - 0.5,
                                    x1=end_reading + 0.5,
                                    y0=start_sensor - 0.5,
                                    y1=end_sensor + 0.5,
                                    line=dict(color=color, width=2),
                                    fillcolor=f'rgba(255, 0, 0, 0.2)'
                                )

                                figx112.add_annotation(
                                    x=(start_reading + end_reading) / 2,
                                    y=start_sensor - 1,
                                    text=f"{defect_counter}({classification.split()[0]})",
                                    showarrow=False,
                                    font=dict(color=color, size=10),
                                    bgcolor="white",
                                    bordercolor="black",
                                    borderwidth=1
                                )

                                defect_counter += 1
                            else:
                                print(f"✗ Defect rejected: max_value={max_value} vs threshold={adjusted_threshold}")

                        except Exception as e:
                            print(f"Error processing defect: {str(e)}")
                            continue
                    print(f"\nTotal submatrices stored: {len(submatrices_dict)}")
                    output_dir = os.path.join(os.getcwd(), "ptt-22-01-2025(6)")
                    manage_directory(output_dir)
                    os.makedirs(output_dir, exist_ok=True)
                    for (defect_id, start_sensor, start_sensor), matrix in submatrices_dict.items():
                        filename = f"submatrix_ptt-1{defect_id, start_sensor, start_sensor}.csv"
                        filepath = os.path.join(output_dir, filename)
                        matrix.to_csv(filepath, index=False)
                        # print(f"Saved {filename}")

                    print(f"\n=== DEFECT CLASSIFICATION SUMMARY ===")
                    print(f"Total defects found: {len(finial_defect_list)}")
                    for classification, stats in classification_stats.items():
                        if stats["total_processed"] > 0:
                            acceptance_rate = (stats["count"] / stats["total_processed"]) * 100
                            print(
                                f"{classification}: {stats['count']}/{stats['total_processed']} defects ({acceptance_rate:.1f}% acceptance)")

                    # DATABASE INSERTION
                    print("\nInserting defects into database...")
                    with connection.cursor() as cursor:
                        for i in finial_defect_list:
                            runid = i['runid']
                            start_index = i['start_reading']
                            end_index = i['end_reading']
                            start_sensor = i['start_sensor']
                            end_sensor = i['end_sensor']
                            absolute_distance = round(i['absolute_distance'] / 1000, 3)
                            upstream = round(i['upstream'] / 1000, 3)
                            length = round(i['length'])
                            length_percent = round(i['length_percent'])

                            # Get corresponding trimmed_matrix (replace with your default if not found)
                            trimmed_matrix = submatrices_dict.get((runid, start_sensor, end_sensor), pd.DataFrame())

                            Width = round(i['breadth'])
                            width_new = round(i['width_new'])
                            width_new2 = round(i['width_new2'])
                            depth = round(i['depth'])
                           # print("DEBUG: i['depth'] =", i['depth'], type(i['depth']))
                            depth_old = round(i['depth_old'])
                            orientation = i['orientation']
                            defect_type = i['defect_type']
                            dimension_classification = i['dimension_classification']
                            start_oddo1 = i['start_oddo1']
                            end_oddo1 = i['end_oddo1']
                            speed = round(i['speed'], 2)
                            min_value = i['Min_Val']
                            max_value = i['Max_Val']

                            query_defect_insert = """
                                INSERT INTO bb_new(runid, start_index, end_index, start_sensor, end_sensor, absolute_distance,
                                upstream, length, length_percent, Width, width_new, width_new2,
                                depth, depth_old, orientation, defect_type, dimension_classification, start_oddo1, end_oddo1, speed,
                                Min_Val, Max_Val)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """

                            cursor.execute(query_defect_insert, (
                                int(runid), start_index, end_index, start_sensor, end_sensor, absolute_distance,
                                upstream,
                                length, length_percent, Width, width_new, width_new2,
                                depth, depth_old, orientation, defect_type, dimension_classification,
                                start_oddo1, end_oddo1, speed, min_value, max_value
                            ))

                            connection.commit()

                   # model_path = 'C:/Users/admin/PycharmProjects/GMFL_12_Inch_Desktop/models WT5.5new_model.pkl'
                    model_path = 'C:/Users/admin/PycharmProjects/GMFL_12_Inch_Desktop/rf_width_model.pkl'
                    model = joblib.load(model_path)  # ✅ Load actual model object
                    model_width(model, output_dir)

                    # FINAL VISUALIZATION
                    figx112.update_layout(
                        # title='Heatmap with 3-Part Adaptive Length Classification (purple: 1-10%, Red : 10-20%, Orange: 20-30%, Yellow : 30-40%, Blue: 40%+)',
                        xaxis_title='Odometer(m)',
                        yaxis_title='Orientation'
                    )

                    print(
                        f"\nProcessing complete! Found {len(finial_defect_list)} total defects using 3-part classification.")
                    print("Displaying visualization...")
                    figx112.show()

                    # roll_dictionary = {'1': roll1}
                    # angle = [round(i * 2.5, 1) for i in range(0, 144)]

                    #                     # df_processed = df_new_tab9.copy()
#                     sensor_columns = [f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)]
#                     df1_raw = df_new_tab9[[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)]]
#
#                     """
# ------------------->Roll Calculation correct code for testing
#                     """
#                     # Config.print_with_time("Roll calculation starts at : ")
#                     # map_ori_sens_ind, val_ori_sensVal = self.Roll_Calculation(df_new_tab9, self.roll_t)
#                     # # print(df_clock_tranpose)
#                     # Config.print_with_time("Roll calculation ends at : ")
#                     #
#                     # val_ori_sensVal_raw = val_ori_sensVal.copy()
#                     #
#                     # # val_ori_sensVal_raw.to_csv("C:/Users/Shradha Agarwal/Desktop/data/aaa_raw.csv")
#                     #
#                     # # clock_cols = list(val_ori_sensVal.columns)
#                     # # val_ori_sensVal = val_ori_sensVal.apply(pd.to_numeric, errors='coerce')
#                     # # window_length = 15
#                     # # polyorder = 2
#                     # # for col in clock_cols:
#                     # #     data = val_ori_sensVal[col].values
#                     # #     time_index = np.arange(len(val_ori_sensVal))
#                     # #     coefficients = np.polyfit(time_index, data, polyorder)
#                     # #     trend = np.polyval(coefficients, time_index)
#                     # #     data_dettrended = data - trend
#                     # #     data_denoised = savgol_filter(data_dettrended, window_length, polyorder)
#                     # #     val_ori_sensVal.loc[:len(val_ori_sensVal), col] = data_denoised
#                     #
#                     # column_means = val_ori_sensVal.abs().mean()
#                     # # column_means = val_ori_sensVal.mean()
#                     # # print("column_means", column_means)
#                     # sensor_mean = [int(i_x) for i_x in column_means]
#                     # standard_deviation = val_ori_sensVal.std(axis=0, skipna=True).tolist()
#                     # """
#                     # To Calculate upper thersold Value
#                     # """
#                     # mean_plus_1sigma = []
#                     # for i, data1 in enumerate(sensor_mean):
#                     #     sigma1 = data1 + (Config.positive_sigma) * standard_deviation[i]
#                     #     mean_plus_1sigma.append(sigma1)
#                     # # print("sigma1_positive",mean_plus_1sigma)
#                     #
#                     # """
#                     # To Calculate lower thersold value
#                     # """
#                     # mean_negative_3sigma = []
#                     # for i_2, data_3 in enumerate(sensor_mean):
#                     #     sigma_3 = data_3 - (Config.negative_sigma) * standard_deviation[i_2]
#                     #     mean_negative_3sigma.append(sigma_3)
#                     # # print("sigma3_negative",mean_negative_3sigma)
#                     #
#                     # """
#                     # Values above the upper threshold are considered as 1,
#                     # values below the lower threshold are considere
#                     # d as -1,
#                     # and values between the upper and lower thresholds are considered as 0.
#                     # """
#                     #
#                     # for col, data in enumerate(val_ori_sensVal.columns):
#                     #     val_ori_sensVal[data] = val_ori_sensVal[data].apply(
#                     #         lambda x: 1 if x > mean_plus_1sigma[col] else (-1 if x < mean_negative_3sigma[col] else 0)
#                     #     )
#                     #
#                     # # val_ori_sensVal.to_csv("C:/Users/Shradha Agarwal/Desktop/data/aaaaa.csv")
#                     #
#                     # # val_ori_sensVal = val_ori_sensVal.astype(int)
#                     # # row_sum = ((val_ori_sensVal.sum(axis=1)) / 144 * 100).round(2)
#                     # #
#                     # # # df_elem = pd.DataFrame({"index": self.index_tab9, "ODDO1": self.oddo1_tab9, "ODDO2": self.oddo2_tab9, "ROLL": self.roll_t})
#                     # #
#                     # # df_elem = pd.DataFrame({"ODDO1": self.oddo1_tab9, "row_sum": row_sum})
#                     # # frames = [df_elem, val_ori_sensVal]
#                     # # df_new = pd.concat(frames, axis=1, join='inner')
#                     # # df_new.loc[df_new['row_sum'] > 80, columns_to_modify] = 2
#                     # # print("df_new.....", df_new)
#                     #
#                     # val_ori_sensVal_sigma = val_ori_sensVal
#                     #
#                     # val_ori_sensVal_raw.columns = val_ori_sensVal_sigma.columns
#                     # df1_aligned = val_ori_sensVal_sigma.reindex(val_ori_sensVal_raw.index)
#                     # result_new = df1_aligned * val_ori_sensVal_raw
#                     # result_new = result_new.dropna()
#                     # result_new.reset_index(drop=True, inplace=True)
#                     # # print("result_new", result_new)
#                     #
#                     # result_raw_df = result_new.mask(result_new == 0, val_ori_sensVal_raw)
#                     # result_raw_df = result_raw_df.dropna()
#                     # result_raw_df.reset_index(drop=True, inplace=True)
#                     # # print("result_raw_df", result_raw_df)
#                     """
# ------------------->Roll Calculation correct code for testing
#                     """
#
#                     """
# ------------------->If applied above code then comment below on from here
#                     """
#                     # df_new_tab9 = df_new_tab9.apply(pd.to_numeric, errors='coerce')
#                     # window_length = 15
#                     # polyorder = 2
#                     #
#                     # for col in sensor_columns:
#                     #     time_index = np.arange(len(df_new_tab9))
#                     #     coefficients = np.polyfit(time_index, data, polyorder)
#                     #     trend = np.polyval(coefficients, time_index)
#                     #     data_dettrended = data - trend
#                     #     data_denoised = savgol_filter(data_dettrended, window_length, polyorder)
#                     #     df_new_tab9.loc[:len(df_new_tab9), col] = data_denoised
#
#                     # df_new_tab9.to_csv("C:/Users/Shradha Agarwal/Desktop/bpcl clock/data_denoised.csv")
#
#                     # df_new_tab9 = df_new_tab9.abs()
#                     # print("data_denoised...", df_new_tab9)
#
#                     roll_dictionary = {'1': self.roll_t}
#                     angle = [round(i*2.5, 1) for i in range(0, 144)]
#                     # print(len(angle))
#
#                     for i in range(2, 145):
#                         current_values = [round((value + angle[i - 1]), 2) for value in self.roll_t]
#                         roll_dictionary['{}'.format(i)] = current_values
#
#                     clock_dictionary = {}
#                     for key in roll_dictionary:
#                         clock_dictionary[key] = [self.degrees_to_hours_minutes(value) for value in roll_dictionary[key]]
#
#                     Roll_hr = pd.DataFrame(clock_dictionary)
#                     Roll_hr.columns = [f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]
#                     # print("Roll_hr", Roll_hr)
#
#                     """
# ------------------->Column wise standard deviation
#                     """
#                     # column_means = df_new_tab9.abs().mean()
#                     column_means = df_new_tab9.mean()
#                     # print("column_means", column_means)
#                     sensor_mean = [i_x for i_x in column_means]
#                     standard_deviation = df_new_tab9.std(axis=0, skipna=True).tolist()
#
#                     # column_means_row = df_new_tab9.abs().mean(axis=1)
#                     # # print("column_means", column_means)
#                     # sensor_mean_row = [int(i_x) for i_x in column_means_row]
#                     # standard_deviation_row = df_new_tab9.std(axis=1, skipna=True).tolist()
#                     """
#                     To Calculate upper thersold Value
#                     """
#                     mean_plus_1sigma = []
#                     for i, data1 in enumerate(sensor_mean):
#                         sigma1 = data1 + (Config.positive_sigma_col) * standard_deviation[i]
#                         mean_plus_1sigma.append(sigma1)
#                     # print("sigma1_positive",mean_plus_1sigma)
#
#                     """
#                     To Calculate lower thersold value
#                     """
#                     mean_negative_3sigma = []
#                     for i_2, data_3 in enumerate(sensor_mean):
#                         sigma_3 = data_3 - (Config.negative_sigma) * standard_deviation[i_2]
#                         mean_negative_3sigma.append(sigma_3)
#                     # print("sigma3_negative",mean_negative_3sigma)
#
#                     # """
#                     # To Calculate upper thersold Value row-wise
#                     # """
#                     # mean_plus_1sigma_row = []
#                     # for i, data1 in enumerate(sensor_mean_row):
#                     #     sigma1_row = data1 + (Config.positive_sigma_row) * standard_deviation_row[i]
#                     #     mean_plus_1sigma_row.append(sigma1_row)
#                     # # print("sigma1_positive",mean_plus_1sigma)
#
#                     """
#                     To Calculate lower thersold value row-wise
#                     """
#                     # mean_negative_3sigma_row = []
#                     # for i_2, data_3 in enumerate(sensor_mean_row):
#                     #     sigma_3_row = data_3 - (Config.negative_sigma) * standard_deviation_row[i_2]
#                     #     mean_negative_3sigma_row.append(sigma_3_row)
#                     # # print("sigma3_negative",mean_negative_3sigma)
#
#                     """
#                     Values above the upper threshold are considered as 1,
#                     values below the lower threshold are considere
#                     d as 1,
#                     and values between the upper and lower thresholds are considered as 0.
#                     """
#
#                     for col, data in enumerate(df_new_tab9.columns):
#                         df_new_tab9[data] = df_new_tab9[data].apply(
#                             lambda x: 1 if x > mean_plus_1sigma[col] else (-1 if x < mean_negative_3sigma[col] else 0)
#                         )
#
#                     """
# ------------------->Column wise and row wise standard deviation
#                     """
#
#                     # ---------------- COLUMN-WISE Processing ----------------
#                     ### **Step 1: Compute Column-Wise Mean & Standard Deviation**
#                     # column_means = df_new_tab9.abs().mean(axis=0)
#                     # sensor_mean = [int(i_x) for i_x in column_means]
#                     # std_dev_col = df_new_tab9.std(axis=0, skipna=True)
#                     #
#                     # # Column-wise upper and lower thresholds
#                     # mean_plus_1sigma_col = column_means + (Config.positive_sigma_col * std_dev_col)
#                     # mean_negative_3sigma_col = column_means - (Config.negative_sigma * std_dev_col)
#                     #
#                     # df_processed_col = df_new_tab9.copy()
#                     # for col, data in enumerate(df_processed_col.columns):
#                     #     df_processed_col[data] = df_processed_col[data].apply(
#                     #         lambda x: 1 if x > mean_plus_1sigma_col[col] else (-1 if x < mean_negative_3sigma_col[col] else 0)
#                     #     )
#                     # print("df_processed_col", df_processed_col)
#                     #
#                     # ### **Step 2: Compute Row-Wise Mean & Standard Deviation**
#                     # row_means = df_new_tab9.abs().mean(axis=1)
#                     # std_dev_row = df_new_tab9.std(axis=1, skipna=True)
#                     #
#                     # # Row-wise upper and lower thresholds
#                     # mean_plus_1sigma_row = row_means + (Config.positive_sigma_row * std_dev_row)
#                     # mean_negative_3sigma_row = row_means - (Config.negative_sigma * std_dev_row)
#                     #
#                     # df_processed_row = df_new_tab9.copy()
#                     # for col, data in enumerate(df_processed_row.columns):
#                     #     df_processed_row[data] = df_processed_row[data].apply(
#                     #         lambda x: 1 if x > mean_plus_1sigma_row[col] else (-1 if x < mean_negative_3sigma_row[col] else 0)
#                     #     )
#                     # print("df_processed_row", df_processed_row)
#                     #
#                     # # Convert DataFrames to NumPy arrays for faster processing
#                     # arr_row = df_processed_row.to_numpy()
#                     # arr_col = df_processed_col.to_numpy()
#                     #
#                     # # Optimized vectorized condition checks using NumPy
#                     # df_final = np.zeros_like(arr_row)  # Initialize with zeros
#                     #
#                     # mask_1 = (arr_row == 1) & (arr_col == 1)  # Mask where both are 1
#                     # mask_neg1 = (arr_row == -1) & (arr_col == -1)  # Mask where both are -1
#                     #
#                     # df_final[mask_1] = 1
#                     # df_final[mask_neg1] = -1
#                     #
#                     # clock_cols = [f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]
#                     # # Convert back to DataFrame
#                     # df_final = pd.DataFrame(df_final, columns=clock_cols, index=df_processed_col.index)
#                     # print(df_final)
#
#
#                     ### **Step 3: Apply Both Column-Wise and Row-Wise Processing in a Single DataFrame**
#                     # df_processed = df_new_tab9.copy()
#                     #
#                     # for i, row in df_processed.iterrows():
#                     #     for col in df_processed.columns:
#                     #         value = row[col]
#                     #         col_index = df_processed.columns.get_loc(col)
#                     #
#                     #         col_threshold_high = mean_plus_1sigma_col.iloc[col_index]
#                     #         col_threshold_low = mean_negative_3sigma_col.iloc[col_index]
#                     #         row_threshold_high = mean_plus_1sigma_row.iloc[i]
#                     #         row_threshold_low = mean_negative_3sigma_row.iloc[i]
#                     #
#                     #         if value > col_threshold_high and value > row_threshold_high:
#                     #             df_processed.at[i, col] = 1  # Mark as 1 if it exceeds either threshold
#                     #         elif value < col_threshold_low or value < row_threshold_low:
#                     #             df_processed.at[i, col] = -1  # Mark as -1 if below either threshold
#                     #         else:
#                     #             df_processed.at[i, col] = 0  # Otherwise, mark as 0
#                     # print("df_processed", df_processed)
#
#                     # # df_new_tab9.to_csv("C:/Users/Shradha Agarwal/Desktop/data/aaaaa.csv")
#
#                     # Config.print_with_time("Roll calculation starts at : ")
#                     # map_ori_sens_ind, val_ori_sensVal = self.Roll_Calculation(df_new_tab9, self.roll_t)
#                     # Config.print_with_time("Roll calculation ends at : ")
#
#                     # val_ori_sensVal = val_ori_sensVal.astype(int)
#                     # row_sum = ((val_ori_sensVal.sum(axis=1)) / 144 * 100).round(2)
#                     #
#                     # # df_elem = pd.DataFrame({"index": self.index_tab9, "ODDO1": self.oddo1_tab9, "ODDO2": self.oddo2_tab9, "ROLL": self.roll_t})
#                     #
#                     # df_elem = pd.DataFrame({"ODDO1": self.oddo1_tab9, "row_sum": row_sum})
#                     # frames = [df_elem, val_ori_sensVal]
#                     # df_new = pd.concat(frames, axis=1, join='inner')
#
#                     # df_new.loc[df_new['row_sum'] > 80, columns_to_modify] = 2
#                     # print("df_new.....", df_new)
#
#                     clock_cols = [f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]
#                     df_new_tab9.columns = clock_cols
#                     filtered_df1 = df_new_tab9
#
#                     df1_raw.columns = filtered_df1.columns
#                     df1_aligned = filtered_df1.reindex(df1_raw.index)
#                     result_new = df1_aligned * df1_raw
#                     result_new = result_new.dropna()
#                     # print("result",result)
#                     result_new.reset_index(drop=True, inplace=True)
#                     t = result_new.transpose()
#
#                     # result_new2.to_csv("C:/Users/Shradha Agarwal/Desktop/data/result_new2.csv")
#
#                     """
#                     for row_wise standard deviation
#                     Values above the upper threshold are considered as 1,
#                     values below the lower threshold are considere
#                     d as 1,
#                     and values between the upper and lower thresholds are considered as 0.
#                     """
#                     # Apply row-wise transformation
#                     # result_new2 = result_new2.apply(
#                     #     lambda row: row.apply(
#                     #         lambda x: (
#                     #             1 if x > 0 and x > mean_plus_1sigma_row[row.name] else
#                     #             (-1 if x > 0 and x < mean_negative_3sigma_row[row.name] else 0)
#                     #         )
#                     #     ),
#                     #     axis=1
#                     # )
#                     # result_new2 = result_new2.applymap(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
#                     # # result_new2.to_csv("C:/Users/Shradha Agarwal/Desktop/data/result_new2_row.csv")
#                     # df1.columns = result_new2.columns
#                     # df1_aligned_new = result_new2.reindex(df1.index)
#                     # result_new = df1_aligned_new * df1
#                     # result_new = result_new.dropna()
#                     # # print("result",result)
#                     # result_new.reset_index(drop=True, inplace=True)
#
#                     # result_new.to_csv("C:/Users/Shradha Agarwal/Desktop/data/result_new_row.csv")
#
#                     result_raw_df = result_new.mask(result_new == 0, df1_raw)
#                     result_raw_df = result_raw_df.dropna()
#                     # print("result_raw_df",result_raw_df)
#                     result_raw_df.reset_index(drop=True, inplace=True)
#
#                     mean_clock_data = result_raw_df.mean().tolist()
#                     val_ori_raw = ((result_raw_df - mean_clock_data) / mean_clock_data) * 100
#                     t_raw = val_ori_raw.transpose()
#
#                     # result_raw_df.to_csv("C:/Users/Shradha Agarwal/Desktop/data/result_raw_df.csv")
#                     """
# ------------------->If applied above code then comment above till here
#                     """
#
#                     frames = [df_elem, result_raw_df]
#                     df_new = pd.concat(frames, axis=1, join='inner')
#
#                     for col in self.df_new_proximity_orientat.columns:
#                         df_new[col] = self.df_new_proximity_orientat[col]
#
#                     for col in Roll_hr.columns:
#                         df_new[col + '_x'] = Roll_hr[col]
#
#                     df_new.to_pickle(folder_path + '/' + str(self.Weld_id_tab9) + '.pkl')
#                     Config.print_with_time("Succesfully saved to clock pickle file")
#
#                     result_new_transpose = result_new.transpose()
#                     # print("result_new_transpose", result_new_transpose)
#                     data_array = result_new_transpose.values.astype(np.float64)
#                     # print("hi")
#
#                     # def dfs(matrix, x, y, visited, cluster):
#                     #     stack = [(x, y)]
#                     #     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#                     #     while stack:
#                     #         cx, cy = stack.pop()
#                     #         if (cx, cy) in visited:
#                     #             continue
#                     #         visited.add((cx, cy))
#                     #         cluster.append((cx, cy))
#                     #         for dx, dy in directions:
#                     #             nx, ny = cx + dx, cy + dy
#                     #             if (0 <= nx < matrix.shape[0] and 0 <= ny < matrix.shape[1] and
#                     #                     matrix[nx, ny] != 0 and (nx, ny) not in visited):
#                     #                 stack.append((nx, ny))
#
#                     def dfs(matrix, x, y, visited, cluster):
#                         """Perform DFS to find clusters, but only include positive values."""
#                         stack = [(x, y)]
#                         directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
#                         while stack:
#                             cx, cy = stack.pop()
#                             if (cx, cy) in visited:
#                                 continue
#                             if matrix[cx, cy] <= 0:
#                                 continue
#                             visited.add((cx, cy))
#                             cluster.append((cx, cy))
#                             for dx, dy in directions:
#                                 nx, ny = cx + dx, cy + dy
#                                 if (0 <= nx < matrix.shape[0] and 0 <= ny < matrix.shape[1] and
#                                         matrix[nx, ny] > 0 and (nx, ny) not in visited):
#                                     stack.append((nx, ny))
#
#                     # def do_boxes_overlap(box1, box2):
#                     #     """Check if two bounding boxes overlap."""
#                     #     return not (box1['end_row'] < box2['start_row'] or
#                     #                 box1['start_row'] > box2['end_row'] or
#                     #                 box1['end_col'] < box2['start_col'] or
#                     #                 box1['start_col'] > box2['end_col'])
#                     #
#                     # # Find clusters of connected non-zero values and calculate bounding boxes
#                     # def merge_boxes(box1, box2):
#                     #     """Merge two overlapping bounding boxes into one."""
#                     #     return {
#                     #         'start_row': min(box1['start_row'], box2['start_row']),
#                     #         'end_row': max(box1['end_row'], box2['end_row']),
#                     #         'start_col': min(box1['start_col'], box2['start_col']),
#                     #         'end_col': max(box1['end_col'], box2['end_col'])
#                     #     }
#                     #
#                     # visited = set()
#                     # bounding_boxes = []
#                     # for i in range(data_array.shape[0]):
#                     #     for j in range(data_array.shape[1]):
#                     #         if data_array[i, j] > 0 and (i, j) not in visited:
#                     #             cluster = []
#                     #             dfs(data_array, i, j, visited, cluster)
#                     #             if cluster:  # Check if the cluster is not empty
#                     #                 min_row = min(point[0] for point in cluster)
#                     #                 max_row = max(point[0] for point in cluster)
#                     #                 min_col = min(point[1] for point in cluster)
#                     #                 max_col = max(point[1] for point in cluster)
#                     #                 bounding_boxes.append({'start_row': min_row, 'end_row': max_row,
#                     #                                        'start_col': min_col, 'end_col': max_col})
#                     #
#                     # merged_boxes = []
#                     # while bounding_boxes:
#                     #     box = bounding_boxes.pop(0)
#                     #     merged = False
#                     #     for i in range(len(merged_boxes)):
#                     #         if do_boxes_overlap(box, merged_boxes[i]):
#                     #             merged_boxes[i] = merge_boxes(box, merged_boxes[i])
#                     #             merged = True
#                     #             break
#                     #     if not merged:
#                     #         merged_boxes.append(box)
#                     # df_sorted = pd.DataFrame(merged_boxes).sort_values(by='start_col')
#                     # print("df_Sorted....", df_sorted)
#                     # df_sorted.to_csv("C:/Users/Shradha Agarwal/Desktop/data/df_sorted.csv")
#
#                     def merge_all_overlapping_boxes(boxes, max_distance=3):
#                         merged = []
#                         while boxes:
#                             current = boxes.pop(0)
#                             overlap_found = True
#                             while overlap_found:
#                                 overlap_found = False
#                                 i = 0
#                                 while i < len(boxes):
#                                     if do_boxes_overlap_or_close(current, boxes[i], max_distance):
#                                         current = merge_boxes(current, boxes[i])
#                                         boxes.pop(i)
#                                         overlap_found = True
#                                     else:
#                                         i += 1
#                             merged.append(current)
#                         return merged
#
#                     def do_boxes_overlap_or_close(box1, box2, max_distance=3):
#                         return do_boxes_overlap(box1, box2) or boxes_are_close(box1, box2, max_distance)
#
#                     def boxes_are_close(box1, box2, max_distance=3):
#                         # Compute closest horizontal and vertical distances between boxes
#                         h_dist = max(0, max(box1['start_col'] - box2['end_col'], box2['start_col'] - box1['end_col']))
#                         v_dist = max(0, max(box1['start_row'] - box2['end_row'], box2['start_row'] - box1['end_row']))
#                         return (h_dist + v_dist) <= max_distance
#
#                     def do_boxes_overlap(box1, box2):
#                         """Check if two bounding boxes overlap."""
#                         return not (box1['end_row'] < box2['start_row'] or
#                                     box1['start_row'] > box2['end_row'] or
#                                     box1['end_col'] < box2['start_col'] or
#                                     box1['start_col'] > box2['end_col'])
#
#                     def merge_boxes(box1, box2):
#                         """Merge two overlapping bounding boxes into one."""
#                         return {
#                             'start_row': min(box1['start_row'], box2['start_row']),
#                             'end_row': max(box1['end_row'], box2['end_row']),
#                             'start_col': min(box1['start_col'], box2['start_col']),
#                             'end_col': max(box1['end_col'], box2['end_col'])
#                         }
#
#                     def calculate_energy_based_depth(defect_matrix, reference_matrix, pipe_thickness=7.1):
#                         """
#                         Estimate depth of defect using energy ratio method.
#
#                         Parameters:
#                         - defect_matrix (pd.DataFrame): Submatrix where defect is detected (from df3_raw)
#                         - reference_matrix (pd.DataFrame): Clean reference region (before/after defect)
#                         - pipe_thickness (float): Wall thickness of the pipe in mm
#
#                         Returns:
#                         - depth_val (float): Estimated depth as percentage of wall thickness
#                         """
#                         try:
#                             if defect_matrix.empty or reference_matrix.empty:
#                                 return 0
#
#                             # defect_arr = normalize_matrix(defect_matrix.to_numpy())
#                             # ref_arr = normalize_matrix(reference_matrix.to_numpy())
#
#                             defect_arr = defect_matrix.to_numpy()
#                             ref_arr = reference_matrix.to_numpy()
#
#                             # Calculate signal energy: sum of squares
#                             energy_defect = np.sum(np.square(defect_arr))
#                             energy_ref = np.sum(np.square(ref_arr))
#                             print("energy_defect:", energy_defect)
#                             print("energy_ref:", energy_ref)
#
#                             if energy_ref == 0 or pipe_thickness == 0:
#                                 return 0
#
#                             # Depth is based on how much stronger the defect signal is
#                             # Apply power law scaling
#                             scaling_exponent = 2.6  # try with this constant also (e.g., 2.4,2.8)
#                             # it is giving best with 2.6 with accuracy 72% for tolrence <=10 and for tolrence <=11 giving 77%.
#                             ratio = energy_defect / energy_ref
#                             print("ratio : ", ratio)
#
#                             depth = ((ratio ** scaling_exponent) * 100) / pipe_thickness
#                             print("depth:", depth)
#
#                             return round(depth, 2)
#
#                         except Exception as e:
#                             print("Error in energy-based depth calculation:", e)
#                             return 0
#
#                     # CLUSTERING LOGIC
#                     print("Performing clustering to detect defect regions...")
#                     visited = set()
#                     bounding_boxes = []
#
#                     for i in range(data_array.shape[0]):
#                         for j in range(data_array.shape[1]):
#                             if data_array[i, j] != 0 and (i, j) not in visited:
#                                 cluster = []
#                                 dfs(data_array, i, j, visited, cluster)
#                                 if cluster:
#                                     min_row = min(point[0] for point in cluster)
#                                     max_row = max(point[0] for point in cluster)
#                                     min_col = min(point[1] for point in cluster)
#                                     max_col = max(point[1] for point in cluster)
#                                     bounding_boxes.append(
#                                         {'start_row': min_row, 'end_row': max_row, 'start_col': min_col,
#                                          'end_col': max_col})
#
#                     # Merge overlapping boxes
#                     # merged_boxes = []
#                     # while bounding_boxes:
#                     #     box = bounding_boxes.pop(0)
#                     #     merged = False
#                     #     for i in range(len(merged_boxes)):
#                     #         if do_boxes_overlap(box, merged_boxes[i]):
#                     #             merged_boxes[i] = merge_boxes(box, merged_boxes[i])
#                     #             merged = True
#                     #             break
#                     #     if not merged:
#                     #         merged_boxes.append(box)
#
#                     merged_boxes = merge_all_overlapping_boxes(bounding_boxes)
#                     df_sorted = pd.DataFrame(merged_boxes).sort_values(by='start_col')
#
#                     df_clock_holl_oddo1 = list(df_new['ODDO1'])
#                     df_clock_holl_oddo1_hov = list((df_new['ODDO1'] / 1000).round(3))
#
#                     self.figure_tab9.clear()
#                     ax_1 = self.figure_tab9.add_subplot(111)
#                     ax_1.figure.subplots_adjust(bottom=0.213, left=0.077, top=0.855, right=1.000)
#
#                     # d1 = ((df_new_1.set_index(df_clock_index)).T).astype(float)
#                     sensor_numbers = list(range(1, len(t.index) + 1))  # 1 to 144
#                     sensor_numbers = sensor_numbers[::-1]  # Reverse the list to go top=0 → bottom=144
#                     text = np.array([[f"{sensor_no}"] * t.shape[1] for sensor_no in sensor_numbers])
#
#                     heatmap_trace = go.Heatmap(x=[t_raw.columns, df_clock_holl_oddo1_hov],
#                                                y=t_raw.index,
#                                                z=t_raw,
#                                                zmin=-5,
#                                                zmax=18,
#                                                hovertemplate='Oddo: %{x}<br>Clock:%{y}<br>Value: %{z}, sensor no: %{text}',
#                                                # text=[[item for item in map_ori_sens_ind[col]] for col in
#                                                #      map_ori_sens_ind.columns],
#                                                colorscale='jet',
#
#                                                colorbar=dict(title='Value'))
#
#                     fig = go.Figure(data=heatmap_trace)
#                     fig.update_xaxes(title_text='Absolute Distance(m)',
#                                      # tickfont=dict(size=11),
#                                      dtick=1000,
#                                      # tickangle=0, showticklabels=True, ticklen=0
#                                      )
#                     fig.update_layout(
#                                     width=1700,
#                                     height=500,
#                                     )
#
#                     # missing_defects = [row for _, row in df_sorted.iterrows() if row not in bounding_boxes]
#                     # print("Excluded regions:", missing_defects)
#
#                     max_submatrix_list = []
#                     min_submatrix_list = []
#                     new_boxes = []
#                     for _, row in df_sorted.iterrows():
#                         start_sensor = row['start_row']
#                         end_sensor = row['end_row']
#                         start_reading = row['start_col']
#                         end_reading = row['end_col']
#                         if start_sensor == end_sensor:
#                             pass
#                         else:
#                             try:
#                                 submatrix = result_new.iloc[start_reading:end_reading + 1, start_sensor:end_sensor + 1]
#                                 submatrix = submatrix.apply(pd.to_numeric, errors='coerce')  # Ensure numeric data
#                                 if submatrix.isnull().values.any():
#                                     print("Submatrix contains NaN values, skipping this iteration.")
#                                     continue
#                                 max_value = submatrix.max().max()
#                                 max_submatrix_list.append(max_value)
#                                 two_d_list = submatrix.values.tolist()
#                                 min_positive = min(x for row in two_d_list for x in row if x > 0)
#                                 min_submatrix_list.append(min_positive)
#                             except Exception as e:
#                                 print(f"Error found 1: {str(e)}")
#                                 traceback.print_exc()
#                                 pass
#
#                     max_of_all = max(max_submatrix_list)  # Get the max of all submatrix max_values
#                     min_of_all = min(min_submatrix_list)
#                     threshold_value = round(min_of_all + (max_of_all - min_of_all) * Config.defectBox_threshold)
#                     # print("Max of all submatrices:", max_of_all)
#                     # print("Min of all submatrices:", min_of_all)
#                     # print("Threshold Value:", threshold_value)
#
#                     submatrices_dict = {}
#                     finial_defect_list = []
#                     defect_counter = 1
#                     # Statistics tracking for each classification
#                     classification_stats = {
#                         "Very Small (1-10%)": {"count": 0, "total_processed": 0},
#                         "Small (10-20%)": {"count": 0, "total_processed": 0},
#                         "Medium (20-30%)": {"count": 0, "total_processed": 0},
#                         "Large (30-40%)": {"count": 0, "total_processed": 0},
#                         "Very Large (40%+)": {"count": 0, "total_processed": 0},
#                         "Below 1%": {"count": 0, "total_processed": 0}
#                     }
#                     for _, row in df_sorted.iterrows():
#                         start_sensor = row['start_row']
#                         end_sensor = row['end_row']
#                         start_reading = row['start_col']
#                         end_reading = row['end_col']
#
#                         # start_sensor = row['start_col']
#                         # end_sensor = row['end_col']
#                         # start_reading = row['start_row']
#                         # end_reading = row['end_row']
#                         if start_sensor == end_sensor:
#                             continue
#                         else:
#                             try:
#                                 submatrix = df1_raw.iloc[start_reading:end_reading + 1, start_sensor:end_sensor + 1]
#                                 submatrix = submatrix.apply(pd.to_numeric, errors='coerce')  # Ensure numeric data
#                                 two_d_list = submatrix.values.tolist()
#                                 max_value = submatrix.max().max()
#                                 min_positive = min(x for row in two_d_list for x in row if x > 0)
#
#                                 counter_difference = end_reading - start_reading
#                                 # print("counter_difference", counter_difference)
#                                 divid = int(counter_difference / 2)
#                                 center = start_reading + divid
#                                 factor1 = divid * Config.l_per_1
#                                 start1 = int(center - factor1)
#                                 end1 = int(center + factor1)
#                                 l_per1 = (df_clock_holl_oddo1[end1] - df_clock_holl_oddo1[start1])
#
#                                 # APPLY 3-PART ADAPTIVE REFINEMENT
#                                 sigma_multiplier, refinement_factor, classification = get_adaptive_sigma_refinement(l_per1)
#                                 adjusted_threshold = threshold_value * sigma_multiplier
#
#                                 valid_columns = 0
#                                 for col_idx in range(start_sensor, end_sensor + 1):
#                                     adaptive_sigma = sensor_mean[col_idx] + (sigma_multiplier * standard_deviation[col_idx])
#                                     if submatrix.iloc[:, col_idx - start_sensor].max() > adaptive_sigma:
#                                         valid_columns += 1
#                                     if valid_columns / (end_sensor - start_sensor + 1) < 0.3:
#                                         print(
#                                             f"✗ Defect rejected: Only {valid_columns} columns passed adaptive threshold")
#                                         continue
#                                 # Track statistics
#                                 classification_stats[classification]["total_processed"] += 1
#
#                                 print(
#                                     f"Defect {defect_counter}: Length={l_per1:.1f}mm, Class={classification}, Threshold={adjusted_threshold:.1f}")
#
#                                 # if (threshold_value <= max_value <= max_of_all) or (threshold_value <= min_positive <= max_of_all):
#                                 if (adjusted_threshold <= max_value <= max_of_all):
#                                     print("max_value", max_value)
#                                     print("min_positive", min_positive)
#                                     print("Max of all submatrices:", max_of_all)
#                                     print("Threshold Value:", threshold_value)
#                                     print(".....................................................")
#
#                                     depth_old = (max_value-min_positive)/min_positive*100
#                                     print("depth_old", depth_old)
#
#                                     max_column = submatrix.max().idxmax()
#                                     max_index = submatrix.columns.get_loc(max_column)
#                                     print("max_index", max_index)
#                                     sub_matrix_list = list(submatrix[max_column])
#
#                                     # if all(val < 0 for val in sub_matrix_list):  # All values are negative
#                                     #     max_val = max(sub_matrix_list)
#                                     #     min_val = min(sub_matrix_list)
#                                     #     print("max_val,min_val", max_val, min_val)
#                                     # elif all(val > 0 for val in sub_matrix_list):  # All values are positive
#                                     #     max_val = max(sub_matrix_list)
#                                     #     min_val = min(sub_matrix_list)
#                                     #     print("max_val,min_val", max_val, min_val)
#                                     # else:
#                                     #     max_val = max(sub_matrix_list)
#                                     #     min_val = min(sub_matrix_list)
#                                     #     print("max_val,min_val", max_val, min_val)
#
#                                     print("start_sensor", start_sensor)
#                                     print("end_sensor", end_sensor)
#                                     print("start_reading", start_reading)
#                                     print("end_reading", end_reading)
#
#                                     # factor2 = divid * Config.l_per_2
#                                     # start2 = round(center - factor2)
#                                     # end2 = round(center + factor2)
#                                     # l_per2 = (df_clock_holl_oddo1[end2] - df_clock_holl_oddo1[start2])
#                                     #
#                                     # factor3 = divid * Config.l_per_3
#                                     # start3 = round(center - factor3)
#                                     # end3 = round(center + factor3)
#                                     # l_per3 = (df_clock_holl_oddo1[end3] - df_clock_holl_oddo1[start3])
#                                     #
#                                     # factor4 = divid * Config.l_per_4
#                                     # start4 = round(center - factor4)
#                                     # end4 = round(center + factor4)
#                                     # l_per4 = (df_clock_holl_oddo1[end4] - df_clock_holl_oddo1[start4])
#
#                                     # print("start1", start1)
#                                     # print("end1", end1)
#                                     # print("start2", start2)
#                                     # print("end2", end2)
#                                     # print("start3", start3)
#                                     # print("end3", end3)
#                                     # print("start4", start4)
#                                     # print("end4", end4)
#
#                                     defect_start_oddo = df_clock_holl_oddo1[start_reading]
#                                     defect_end_oddo = df_clock_holl_oddo1[end_reading]/1000
#                                     # print("defect_start_oddo", defect_start_oddo)
#                                     # print("defect_end_oddo", defect_end_oddo)
#                                     time_sec = end_reading/1500
#                                     speed = defect_end_oddo/time_sec
#                                     speed = defect_end_oddo/time_sec
#                                     print("speed(m/s)", speed)
#
#                                     base_value = sensor_mean[max_index]
#                                     print("base_value", base_value)
#                                     # max_col_index = submatrix.loc[max_row_index].idxmax()
#                                     # print("max_col_index....",max_col_index)
#
#                                     internal_external = internal_or_external(self.df_new_proximity_orientat, max_index)
#                                     print("internal_external", internal_external)
#
#                                     absolute_distance = (df_clock_holl_oddo1[start_reading])
#                                     print("absolute_distance", absolute_distance)
#                                     length = (df_clock_holl_oddo1[end_reading] - df_clock_holl_oddo1[start_reading])
#                                     print("length of defect", length)
#
#                                     """
#                                     Calculate latitude and longitude
#                                     """
#                                     long, lat = lat_long(absolute_distance, self.runid)
#                                     print("latitude", lat)
#                                     print("longitude", long)
#
#                                     upstream_oddo1 = (df_clock_holl_oddo1[start_reading] - df_clock_holl_oddo1[0])
#                                     print("upstream1", upstream_oddo1)
#
#                                     """
#                                     Calculate Wall thickness
#                                     """
#                                     # if self.Weld_id_tab9 == 2:
#                                     #     wt = 5.5
#                                     # else:
#                                     #     wt = Config.pipe_thickness
#
#                                     wt = Config.pipe_thickness
#
#                                     # pipe_length_oddo1 = (df_clock_holl_oddo1[-1] - df_clock_holl_oddo1[0])/1000
#                                     # print("pipe_length", pipe_length_oddo1)
#
#                                     # width = Width_calculation(start_sensor, end_sensor)
#                                     # print("breadth of defect", width)
#
#                                     # sen_diff = end_sensor - start_sensor
#                                     # if sen_diff > 2:
#                                     #     counter_difference_1 = (end_sensor + 1) - (start_sensor + 1)
#                                     #     divid_1 = int(counter_difference_1/2)
#                                     #     center_1 = start_sensor + divid_1
#                                     #     factor1_1 = divid_1 * Config.w_per_1
#                                     #     start1_1 = (int(center_1 - factor1_1)) - 1
#                                     #     end1_1 = (int(center_1 + factor1_1)) - 1
#                                     # else:
#                                     #     start1_1 = start_sensor
#                                     #     end1_1 = end_sensor
#                                     counter_difference_1 = (end_sensor + 1) - (start_sensor + 1)
#                                     divid_1 = int(counter_difference_1 / 2)
#                                     center_1 = start_sensor + divid_1
#                                     factor1_1 = divid_1 * Config.w_per_1
#                                     start1_1 = (int(center_1 - factor1_1)) - 1
#                                     end1_1 = (int(center_1 + factor1_1)) - 1
#                                     width = Width_calculation(start_sensor, end_sensor)
#                                     print("width_new", width)
#
#                                     df_copy_submatrix = df1_raw.iloc[start_reading:end_reading+1, start_sensor:end_sensor + 1]
#                                     ref_start = max(0, start_reading - (end_reading - start_reading))
#                                     ref_end = ref_end = start_reading - 1
#                                     reference_matrix = df1_raw.iloc[ref_start:ref_end + 1, start_sensor:end_sensor + 1]
#                                     depth_val2 = calculate_energy_based_depth(df_copy_submatrix, reference_matrix, pipe_thickness = Config.pipe_thickness)
#                                     depth_val2 = min(depth_val2, 100)
#
#                                     ############ Width modified code, duplicacy started from here ############
#                                     def replace_first_column(df_n, s_sensor, e_sensor):
#                                         s_sensor = s_sensor + 1
#                                         e_sensor = e_sensor + 1
#                                         # Generate new column names within the given range
#                                         new_columns = list(range(s_sensor, s_sensor + df_n.shape[1]))
#                                         # Assign new column names
#                                         df_n.columns = new_columns
#                                         # Drop the last column if it exceeds end_sensor
#                                         df_n = df_n.loc[:, df_n.columns <= e_sensor]
#                                         return df_n
#
#                                     # df_duplicate_std = replace_first_column(df_copy_submatrix, start_sensor, end_sensor)
#                                     # df_duplicate_std.columns = df_duplicate_std.columns.astype(str)
#                                     # print("df_duplicate", df_duplicate)
#
#                                     df_duplicate = replace_first_column(df_copy_submatrix, start_sensor, end_sensor)
#                                     # df_duplicate = replace_first_column(df_copy_submatrix, start1_1, end1_1)
#                                     df_duplicate.columns = df_duplicate.columns.astype(str)
#
#                                     outer_diameter_1 = Config.outer_dia  # 12-inch pipe
#                                     thickness_1 = Config.pipe_thickness  # Replace with Config.pipe_thickness if using from config
#                                     inner_diameter_1 = outer_diameter_1 - 2 * thickness_1
#                                     radius_1 = inner_diameter_1 / 2
#                                     theta_2 = Config.width_angle1  # approximate value for both pipes
#                                     c_1 = math.radians(theta_2)
#                                     theta_3 = Config.width_angle2  # approximate value for both pipes
#                                     d_1 = math.radians(theta_3)
#                                     theta_4 = Config.width_angle3  # 9.97 for thickness 5.5 and 9.53 for thickness 7.1
#                                     e_1 = math.radians(theta_4)  # Convert to radians
#                                     # print("c1, d1", c_1, d_1)
#                                     x1 = round(radius_1 * c_1, 1)
#                                     y1 = round(radius_1 * d_1, 1)
#                                     z1 = round(radius_1 * e_1, 1)
#
#                                     # def process_csv(df_dupe):
#                                     #     new_data = {}
#                                     #     next_col = None
#                                     #
#                                     #     base = round(x1 / Config.div_factor)
#                                     #     c = round(y1 / Config.div_factor)
#                                     #     dee = round(z1 / Config.div_factor)
#                                     #
#                                     #     # base1 = base//2
#                                     #     # base2 = base-base1
#                                     #
#                                     #     c1 = c//2
#                                     #     c2 = c-c1
#                                     #
#                                     #     dee1 = dee//2
#                                     #     dee2 = dee-dee1
#                                     #
#                                     #     def generate_suffixes(n):
#                                     #         return [chr(ord('a') + i) for i in range(n)]
#                                     #
#                                     #     base_suffixes = generate_suffixes(int(base))
#                                     #
#                                     #     # base1_suffixes = generate_suffixes(int(base1))
#                                     #     # base2_suffixes = generate_suffixes(int(base2))
#                                     #     c1_suffixes = generate_suffixes(int(c1))
#                                     #     c2_suffixes = generate_suffixes(int(c2))
#                                     #     dee1_suffixes = generate_suffixes(int(dee1))
#                                     #     dee2_suffixes = generate_suffixes(int(dee2))
#                                     #
#                                     #     """" without value_decrease in matrix """
#                                     #     for colu in df_dupe.columns:
#                                     #         col_int = int(colu)
#                                     #         next_col = str(col_int + 1)
#                                     #
#                                     #         if next_col in df_dupe.columns:
#                                     #             # Special Case 1
#                                     #             if col_int % 4 == 0 and col_int % 16 != 0:
#                                     #                 for idx, suffix in enumerate(c1_suffixes):
#                                     #                     # reduction = 1- ((idx+1)*Config.value_decrease_percent)
#                                     #                     # new_data[f"{col_int}{suffix}_extra"] = df_dupe[colu]*reduction
#                                     #                     new_data[f"{col_int}{suffix}_extra"] = df_dupe[colu]
#                                     #                 # for suffix in c2_suffixes:
#                                     #                 for idx, suffix in enumerate(c2_suffixes):
#                                     #                     # reduction = 1 - ((idx + 1) * Config.value_decrease_percent)
#                                     #                     # new_data[f"{int(next_col)}{suffix}_extra"] = df_dupe[next_col]*reduction
#                                     #                     new_data[f"{int(next_col)}{suffix}_extra"] = df_dupe[next_col]
#                                     #
#                                     #             # Special Case 2
#                                     #             elif col_int % 16 == 0:
#                                     #                 # for suffix in dee1_suffixes:
#                                     #                 for idx,suffix in enumerate(dee1_suffixes):
#                                     #                     # reduction = 1 - ((idx+1) * Config.value_decrease_percent)
#                                     #                     # new_data[f"{col_int}{suffix}_extra2"] = df_dupe[colu]*reduction
#                                     #                     new_data[f"{col_int}{suffix}_extra2"] = df_dupe[colu]
#                                     #                 # for suffix in dee2_suffixes:
#                                     #                 for idx, suffix in enumerate(dee2_suffixes):
#                                     #                     # reduction = 1 - ((idx + 1) * Config.value_decrease_percent)
#                                     #                     # new_data[f"{int(next_col)}{suffix}_extra2"] = df_dupe[next_col]*reduction
#                                     #                     new_data[f"{int(next_col)}{suffix}_extra2"] = df_dupe[next_col]
#                                     #
#                                     #             else:
#                                     #                 for idx,suffix in enumerate(base_suffixes):
#                                     #                     # reduction = 1- ((idx+1)*Config.value_decrease_percent)
#                                     #                     # new_data[f"{col_int}{suffix}"] = df_dupe[colu]*reduction
#                                     #                     new_data[f"{col_int}{suffix}"] = df_dupe[colu]
#                                     #
#                                     #     """" with value_decrease in matrix """
#                                     #     # for colu in df_dupe.columns:
#                                     #     #     # print(f"colu: {colu}, type: {type(colu)}")
#                                     #     #
#                                     #     #     col_int = int(colu)
#                                     #     #     next_col = str(col_int + 1)
#                                     #     #
#                                     #     #     if next_col in df_dupe.columns:
#                                     #     #         # Special Case 1
#                                     #     #         if col_int % 4 == 0 and col_int % 16 != 0:
#                                     #     #             for idx, suffix in enumerate(c1_suffixes):
#                                     #     #                 reduction = 1- ((idx+1)*Config.value_decrease_percent)
#                                     #     #                 new_data[f"{col_int}{suffix}_extra"] = df_dupe[colu]*reduction
#                                     #     #             # for suffix in c2_suffixes:
#                                     #     #             for idx, suffix in enumerate(c2_suffixes):
#                                     #     #                 reduction = 1 - ((idx + 1) * Config.value_decrease_percent)
#                                     #     #                 new_data[f"{int(next_col)}{suffix}_extra"] = df_dupe[next_col]*reduction
#                                     #     #
#                                     #     #         # Special Case 2
#                                     #     #         elif col_int % 16 == 0:
#                                     #     #             # for suffix in dee1_suffixes:
#                                     #     #             for idx,suffix in enumerate(dee1_suffixes):
#                                     #     #                 reduction = 1 - ((idx+1) * Config.value_decrease_percent)
#                                     #     #                 new_data[f"{col_int}{suffix}_extra2"] = df_dupe[colu]*reduction
#                                     #     #             # for suffix in dee2_suffixes:
#                                     #     #             for idx, suffix in enumerate(dee2_suffixes):
#                                     #     #                 reduction = 1 - ((idx + 1) * Config.value_decrease_percent)
#                                     #     #                 new_data[f"{int(next_col)}{suffix}_extra2"] = df_dupe[next_col]*reduction
#                                     #     #
#                                     #     #         else:
#                                     #     #             # Base duplication
#                                     #     #
#                                     #     #             # for suffix in base_suffixes:
#                                     #     #             for idx,suffix in enumerate(base_suffixes):
#                                     #     #                 reduction = 1- ((idx+1)*Config.value_decrease_percent)
#                                     #     #                 new_data[f"{col_int}{suffix}"] = df_dupe[colu]*reduction
#                                     #     #
#                                     #     #
#                                     #     #             # for suffix in base1_suffixes:
#                                     #     #             #     new_data[f"{col_int}{suffix}"] = df_dupe[colu]
#                                     #     #             # for suffix in base2_suffixes:
#                                     #     #             #     new_data[f"{int(next_col)}{suffix}"] = df_dupe[next_col]
#                                     #
#                                     #     new_df_duplicate = pd.DataFrame(new_data)
#                                     #     return new_df_duplicate
#                                     def extract_int_prefix(s):
#                                         m = re.match(r'^(\d+)', str(s))
#                                         return int(m.group(1)) if m else None
#
#                                     def get_first_last_integer_column(cols):
#                                         int_vals = [extract_int_prefix(col) for col in cols]
#                                         int_vals = [v for v in int_vals if v is not None]
#                                         if not int_vals:
#                                             return None, None
#                                         return min(int_vals), max(int_vals)
#
#                                     def process_csv_interpolate(df_dupe):
#                                         """
#                                         Like the original process_csv, but uses interpolation (linear or cubic)
#                                         instead of duplication for the new columns. Suffixes and column names are
#                                         generated exactly as in the original code, with robust end-case handling.
#                                         """
#                                         new_data = {}
#                                         next_col = None
#
#                                         # Use your previously computed distances
#                                         base = round(x1 / Config.div_factor)
#                                         c = round(y1 / Config.div_factor)
#                                         dee = round(z1 / Config.div_factor)
#
#                                         c1 = c // 2
#                                         c2 = c - c1
#                                         dee1 = dee // 2
#                                         dee2 = dee - dee1
#
#                                         def generate_suffixes(n):
#                                             return [chr(ord('a') + i) for i in range(int(n))]
#
#                                         base_suffixes = generate_suffixes(int(base))
#                                         c1_suffixes = generate_suffixes(int(c1))
#                                         c2_suffixes = generate_suffixes(int(c2))
#                                         dee1_suffixes = generate_suffixes(int(dee1))
#                                         dee2_suffixes = generate_suffixes(int(dee2))
#
#                                         for colu in df_dupe.columns:
#                                             col_int = int(colu)
#                                             next_col = str(col_int + 1)
#
#                                             if next_col in df_dupe.columns:
#                                                 col_vals = df_dupe[colu].values
#                                                 next_col_vals = df_dupe[next_col].values
#
#                                                 def interpolate_between(a, b, n, kind='cubic'):
#                                                     # For short arrays, always use linear
#                                                     if n == 0:
#                                                         return np.empty((0, len(a)))
#                                                     x = np.array([0, 1])
#                                                     arr = np.vstack([a, b]).T
#                                                     interpolated = []
#                                                     for row in arr:
#                                                         # If both points are the same, just duplicate
#                                                         if np.allclose(row[0], row[1]):
#                                                             interpolated.append(np.full(n, row[0]))
#                                                             continue
#                                                         # Use cubic only if possible, otherwise linear
#                                                         if kind == 'cubic' and n >= 3:
#                                                             try:
#                                                                 f = interp1d(x, row, kind='cubic',
#                                                                              fill_value="extrapolate")
#                                                             except Exception:
#                                                                 f = interp1d(x, row, kind='linear',
#                                                                              fill_value="extrapolate")
#                                                         else:
#                                                             f = interp1d(x, row, kind='linear',
#                                                                          fill_value="extrapolate")
#                                                         xs = np.linspace(0, 1, n + 2)[1:-1] if n > 0 else []
#                                                         interpolated.append(f(xs) if len(xs) > 0 else [])
#                                                     return np.array(interpolated).T if n > 0 else np.empty((0, len(a)))
#
#                                                 # Special Case 1: Between flappers (multiples of 4, not 16)
#                                                 if col_int % 4 == 0 and col_int % 16 != 0:
#                                                     c1_interp = interpolate_between(col_vals, next_col_vals,
#                                                                                     len(c1_suffixes), kind='cubic')
#                                                     for idx, suffix in enumerate(c1_suffixes):
#                                                         new_data[f"{col_int}{suffix}_extra"] = c1_interp[idx] if \
#                                                         c1_interp.shape[0] > 0 else col_vals
#                                                     c2_interp = interpolate_between(next_col_vals, col_vals,
#                                                                                     len(c2_suffixes), kind='cubic')
#                                                     for idx, suffix in enumerate(c2_suffixes):
#                                                         new_data[f"{int(next_col)}{suffix}_extra"] = c2_interp[idx] if \
#                                                         c2_interp.shape[0] > 0 else next_col_vals
#
#                                                 # Special Case 2: Between arms (multiples of 16)
#                                                 elif col_int % 16 == 0:
#                                                     dee1_interp = interpolate_between(col_vals, next_col_vals,
#                                                                                       len(dee1_suffixes), kind='cubic')
#                                                     for idx, suffix in enumerate(dee1_suffixes):
#                                                         new_data[f"{col_int}{suffix}_extra2"] = dee1_interp[idx] if \
#                                                         dee1_interp.shape[0] > 0 else col_vals
#                                                     dee2_interp = interpolate_between(next_col_vals, col_vals,
#                                                                                       len(dee2_suffixes), kind='cubic')
#                                                     for idx, suffix in enumerate(dee2_suffixes):
#                                                         new_data[f"{int(next_col)}{suffix}_extra2"] = dee2_interp[
#                                                             idx] if dee2_interp.shape[0] > 0 else next_col_vals
#
#                                                 # Base case: Normal sensor spacing
#                                                 else:
#                                                     base_interp = interpolate_between(col_vals, next_col_vals,
#                                                                                       len(base_suffixes), kind='cubic')
#                                                     for idx, suffix in enumerate(base_suffixes):
#                                                         new_data[f"{col_int}{suffix}"] = base_interp[idx] if \
#                                                         base_interp.shape[0] > 0 else col_vals
#
#                                         new_df_duplicate = pd.DataFrame(new_data, index=df_dupe.index)
#                                         return new_df_duplicate
#
#                                     def process_submatrix(df_diff):
#                                         if df_diff.isnull().values.any():
#                                             return None
#
#                                         # try:
#                                         #     max_val = df_diff.max().max()
#                                         #     min_pos_val = df_diff[df_diff > 0].min().min()
#                                         #     signal_strength = np.log10(max_val + 1)  # Avoid log(0)
#                                         # except:
#                                         #     max_val = None
#                                         #     min_pos_val = None
#                                         #     signal_strength = 0
#
#                                         ### STDEV ON DEFECT MATRIX ROW-WISE ###
#                                         # print("df_diff", df_diff)
#                                         # df_diff = df_diff.applymap(lambda x: np.log(x) if x > 0 else np.nan)
#                                         # adaptive_sigma_row = get_adaptive_sigma_row_values(length_percent)
#                                         # ratio = round((max_val - min_pos_val) / (min_pos_val + 1e-5), 2)
#                                         # sigma_multiplier, _, _ = get_adaptive_sigma_refinement(length_percent)
#                                         # effective_positive_sigma_row = adaptive_sigma_row * positive_sigma_row
#
#                                         df_diff_mean = list(df_diff.median(axis=1))
#                                         df_std_dev = list(df_diff.std(axis=1, ddof=1))
#                                         mean_plus_std = list(
#                                             map(lambda x, y: x + y * (Config.positive_sigma_row), df_diff_mean, df_std_dev))
#                                         # mean_plus_std = list(map(lambda x, y: x * (positive_sigma_row), df_diff_mean, df_std_dev))
#                                         mean_plus_std_series = pd.Series(mean_plus_std, index=df_diff.index)
#                                         # mean_neg_std = list(map(lambda x, y: x - y * (negative_sigma_row), df_diff_mean, df_std_dev))
#                                         # mean_neg_std_series = pd.Series(mean_neg_std, index=df_diff.index)
#                                         # Apply the function row-wise
#                                         df_result = df_diff.apply(lambda row: row.map(
#                                             lambda x: 1 if x > mean_plus_std_series[row.name] else 0), axis=1)
#
#                                         ### STDEV ON DEFECT MATRIX COLUMN-WISE ###
#                                         # df_diff_mean = df_diff.median(axis=0).tolist()
#                                         # df_std_dev = df_diff.std(axis=0, skipna=True, ddof=1).tolist()
#                                         # mean_plus_std = []
#                                         # for i_std, data_std in enumerate(df_diff_mean):
#                                         #     sigma_std_col = data_std + (positive_sigma_row * df_std_dev[i_std])
#                                         #     mean_plus_std.append(sigma_std_col)
#                                         # df_result = pd.DataFrame(index=df_diff.index)
#                                         # for col1_std, data1_std in enumerate(df_diff.columns):
#                                         #     df_result[data1_std] = df_diff[data1_std].apply(lambda x: 1 if x > mean_plus_std[col1_std] else 0)
#
#                                         count_ones_per_column = df_result.sum(axis=0)
#                                         first_col_with_1 = count_ones_per_column.ne(0).idxmax()
#                                         last_col_with_1 = count_ones_per_column[::-1].ne(0).idxmax()
#                                         first_col_with_1_idx = df_result.columns.get_loc(first_col_with_1)
#                                         last_col_with_1_idx = df_result.columns.get_loc(last_col_with_1)
#
#                                         df_between = df_result.iloc[:, first_col_with_1_idx:last_col_with_1_idx + 1]
#                                         # Count columns that have at least one '1'
#                                         num_cols_with_ones = (df_between == 1).any(axis=0).sum()
#                                         num_cols_between = last_col_with_1_idx - first_col_with_1_idx + 1
#
#                                         # Step 3: Count the number of columns to remove from start and end
#                                         num_cols_to_remove_start = first_col_with_1_idx
#                                         num_cols_to_remove_end = len(count_ones_per_column) - 1 - last_col_with_1_idx
#
#                                         width_1_only = round(num_cols_with_ones * Config.div_factor)
#                                         width_0_yes = round(num_cols_between * Config.div_factor)
#                                         print("width_1_only", width_1_only)
#                                         print("width_0_yes", width_0_yes)
#                                         trimmed_original_matrix = df_diff.iloc[:,
#                                                                   first_col_with_1_idx: last_col_with_1_idx + 1]
#                                         new_start_sensor = start1_1 + num_cols_to_remove_start
#                                         new_end_sensor = end1_1 - num_cols_to_remove_end
#                                         return trimmed_original_matrix, width_1_only, width_0_yes, new_start_sensor, new_end_sensor
#
#                                     modified_df = process_csv_interpolate(df_duplicate)
#                                     # if end1_1 - start1_1 > 2:
#                                     #     trimmed_matrix, width_1_only, width_0_yes, new_start_sensor, new_end_sensor = process_submatrix(modified_df)
#                                     #     print(trimmed_matrix.columns.to_list())
#                                     # else:
#                                     #     num_cols = len(modified_df.columns)
#                                     #     width_1_only = round(num_cols * Config.div_factor)
#                                     #     print(modified_df.columns.to_list())
#                                     trimmed_matrix, width_1_only, width_0_yes, new_start_sensor, new_end_sensor = process_submatrix(modified_df)
#                                     new_start_sensor, new_end_sensor = get_first_last_integer_column(
#                                         trimmed_matrix.columns)
#                                     mapped_start_sensor = len(result_new_transpose.index) - start_sensor
#                                     mapped_end_sensor = len(result_new_transpose.index) - end_sensor
#                                     if mapped_end_sensor < mapped_start_sensor:
#                                         mapped_start_sensor, mapped_end_sensor = mapped_end_sensor, mapped_start_sensor
#
#                                     print("start_reading", start_reading, 'end_sensor', end_sensor)
#                                     avg_counter = round((start1+end1)/2)
#                                     avg_sensor = round((start_sensor+end_sensor)/2)
#                                     orientation = Roll_hr.iloc[avg_counter, avg_sensor]
#                                     # k2 = map_ori_sens_ind.iloc[avg_counter, avg_sensor]
#                                     # orientation = k2[2]
#
#                                     # avg = round((start_sensor+end_sensor)/2)
#                                     # orientation = defect_angle_x(self.roll_t, avg)
#                                     # # orientation = df_new_tab9.columns[max_index]
#                                     print("orientation", orientation)
#
#                                     thickness_pipe = Config.pipe_thickness  ### Value Change according to wall thickness
#                                     dimension_classification = get_type_defect_1(thickness_pipe, runid,
#                                                                                  length, width)
#                                     print("dimension_classification", dimension_classification)
#
#                                     try:
#                                         ################# each pipe thickness can be change #################
#                                         depth_val = round((((length / width) * (max_value / base_value))*100)/Config.pipe_thickness)
#                                         print("depth_val", depth_val)
#                                     except:
#                                         depth_val = 0
#
#                                     if depth_val2 > 1 and width > 1 and length > 1:
#                                         # Save the submatrix with key as a tuple of coordinates
#                                         submatrices_dict[(Weld_id_tab9, defect_counter)] = submatrix
#
#                                         print("depth_old.....", depth_old)
#                                         runid = self.runid
#                                         finial_defect_list.append(
#                                             {"runid": runid, "start_reading": start_reading, "end_reading": end_reading,
#                                              "start_sensor": mapped_start_sensor,
#                                              "end_sensor": mapped_end_sensor,
#                                              "absolute_distance": absolute_distance, "upstream_oddo1": upstream_oddo1,
#                                              "length": length, "breadth": width, "width_new": width_1_only, 'orientation': orientation,
#                                              "dimension_classification": dimension_classification, "defect_type": internal_external,
#                                              "depth": depth_val2, "WT": wt,
#                                              "max_value": start1_1, "base_value": end1_1, "min_value": min_positive,
#                                              "l_per1": l_per1,
#                                              # "l_per2": l_per2, "l_per3": l_per3, "l_per4": l_per4,
#                                              "speed": speed, "latitude":lat, "longitude": long
#                                              })
#                                         # k={'start_reading':start_reading,'end_reading':end_reading,'start_sensor':start_sensor,'end_sensor':end_sensor,'','max_value':max_value}
#                                         # print(k)
#                                         fig.add_shape(
#                                             type='rect',
#                                             x0=start_reading - 0.5,  # Adjust for center of cells
#                                             x1=end_reading + 0.5,
#                                             y0=start_sensor - 0.5,
#                                             y1=end_sensor + 0.5,
#                                             line=dict(color='red', width=1),
#                                             fillcolor='rgba(255, 0, 0, 0.1)'  # Optional: transparent fill
#                                         )
#                                         fig.add_annotation(
#                                             x=(start_reading + end_reading) / 2,
#                                             y=start_sensor - 2,  # Position above the box; adjust if needed
#                                             text=str(defect_counter),
#                                             showarrow=False,
#                                             font=dict(color="red", size=12),
#                                             bgcolor="white",
#                                             bordercolor="black",
#                                             borderwidth=1
#                                         )
#
#                                         # Increment the counter only for valid (stored) defects
#                                         defect_counter += 1
#                                 else:
#                                     pass
#                             except Exception as e:
#                                 print(f"Error found: {str(e)}")
#                                 traceback.print_exc()
#                                 pass
#
#                     def manage_directory(directory_path):
#                         # Create the directory if it doesn't exist
#                         if not os.path.exists(directory_path):
#                             os.makedirs(directory_path)
#                             print(f"Directory created: {directory_path}")
#                         else:
#                             print(f"Directory already exists: {directory_path}")
#
#                         # Delete all existing files in the directory
#                         for filename in os.listdir(directory_path):
#                             file_path = os.path.join(directory_path, filename)
#                             try:
#                                 if os.path.isfile(file_path) or os.path.islink(file_path):
#                                     os.unlink(file_path)
#                                 elif os.path.isdir(file_path):
#                                     shutil.rmtree(file_path)
#                             except Exception as e:
#                                 print(f"Failed to delete {file_path}. Reason: {e}")
#
#                         print(f"All files deleted from directory: {directory_path}")
#
#                     # Print stored submatrices with their coordinates
#                     print(f"\nTotal submatrices stored: {len(submatrices_dict)}")
#                     output_dir_def = os.path.join(os.getcwd(), "defect_matrices")
#                     manage_directory(output_dir_def)
#                     os.makedirs(output_dir_def, exist_ok=True)
#                     for (weld_id, defect_id), matrix in submatrices_dict.items():
#                         filename = f"submatrix_ptt-1{defect_id, start_sensor, start_sensor}.csv"
#                         filepath = os.path.join(output_dir_def, filename)
#                         matrix.to_csv(filepath, index=False)
#                         # print(f"Saved {filename}")
#
#                     with connection.cursor() as cursor:
#                         for i in finial_defect_list:
#                             runid = i['runid']
#                             start_index = i['start_reading']
#                             end_index = i['end_reading']
#                             start_sensor = i['start_sensor']
#                             end_sensor = i['end_sensor']
#                             absolute_distance = round(i['absolute_distance']/1000, 3)
#                             upstream_oddo1 = round(i['upstream_oddo1']/1000, 3)
#                             length = round(i['length'])
#                             Width = round(i['breadth'])
#                             width_new = round(i['width_new'])
#                             depth = round(i['depth'])
#                             orientation = i['orientation']
#                             dimension_classification = i['dimension_classification']
#                             defect_type = i['defect_type']
#                             max_value = round(i['max_value'])
#                             base_value = round(i['base_value'])
#                             min_value = round(i['min_value'])
#                             l_per1 = round(i['l_per1'])
#                             # l_per2 = round(i['l_per2'])
#                             # l_per3 = round(i['l_per3'])
#                             # l_per4 = round(i['l_per4'])
#                             WT = i['WT']
#                             speed = round(i['speed'], 2)
#                             latitude = i['latitude']
#                             longitude = i['longitude']
#                             with connection.cursor() as cursor:
#                                 query_defect_insert = "INSERT into defect_clock_hm(runid, pipe_id, pipe_length, start_index, end_index, start_sensor, end_sensor, upstream, absolute_distance, orientation, length, Width,width_new,depth,max_value, min_value,l_per1, dimension_classification,defect_type, mean_value, WT, speed, latitude, longitude) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
#
#                                 cursor.execute(query_defect_insert, (
#                                     int(runid), self.Weld_id_tab9, self.pipe_len_oddo1_chm, start_index, end_index,
#                                     start_sensor, end_sensor, upstream_oddo1, absolute_distance, orientation,
#                                      length, Width,width_new, depth, max_value, min_value, l_per1, dimension_classification,
#                                      defect_type, base_value, WT, speed, latitude, longitude))
#                                 connection.commit()
#
#                     def extract_features(row):
#                         x = np.array(row['submatrix'])
#
#                         # Basic stats
#                         mean = np.mean(x)
#                         std = np.std(x)
#                         max_val = np.max(x)
#                         min_val = np.min(x)
#
#                         # FFT features
#                         fft_vals = np.abs(np.fft.fft(x))
#                         fft_features = fft_vals[:10]
#
#                         # Threshold crossings
#                         threshold = mean + 2 * std
#                         threshold_crossings = np.sum(x > threshold)
#
#                         # Z-score anomalies
#                         z_scores = np.abs((x - mean) / (std + 1e-8))
#                         anomaly_score = np.mean(z_scores > 3)
#
#                         # CWT Median Feature using pywt.cwt
#                         try:
#                             x = np.array(x)
#                             if x.ndim == 1:
#                                 side = int(np.sqrt(len(x)))
#                                 if side * side != len(x):
#                                     raise ValueError("Not a perfect square")
#                                 mat = x.reshape(-1, side)
#                             else:
#                                 mat = x
#                         except:
#                             mat = np.atleast_2d(x)
#
#                         cwt_medians = []
#                         for row_sig in mat:
#                             row_sig = np.asarray(row_sig)
#                             if row_sig.ndim != 1:
#                                 continue
#
#                             N = len(row_sig)
#                             if N < 5:
#                                 continue
#
#                             signal_std = np.std(row_sig)
#                             max_scale = min(N // 2, max(3, int(signal_std * 10)))
#                             if max_scale < 1:
#                                 continue
#
#                             widths = np.arange(1, max_scale + 1)
#                             if len(widths) < 1:
#                                 continue
#
#                             # ✅ FIXED: use 'gaus1' (not 'guass1') and unpack coeffs and freqs
#                             coeffs, freqs = cwt(row_sig, widths, 'gaus1')
#                             row_cwt_median = np.median(np.abs(coeffs))
#                             cwt_medians.append(row_cwt_median)
#
#                         cwt_final = np.median(cwt_medians) if cwt_medians else 0
#
#                         return [mean, std, max_val, min_val, threshold_crossings, anomaly_score, cwt_final] + list(fft_features)
#
#                     def model_width(model, folder_path):
#                         query = "select id, speed, start_sensor, end_sensor, width_new from defect_clock_hm"
#                         df_meta = pd.read_sql_query(query, connection)
#                         # df_meta.to_csv("df_meta.csv")
#                         df_meta.rename(columns={'id': 'def_no.', 'width_new': 'pred_width'}, inplace=True)
#                         df_meta['def_no.'] = df_meta['def_no.'].astype(int)
#                         meta_dict = {
#                             int(row['def_no.']): {
#                                 'speed': float(row['speed']),
#                                 'Start_sensor': float(row['start_sensor']),
#                                 'End_sensor': float(row['end_sensor']),
#                                 'pred_width': float(row['pred_width']),
#                             }
#                             for _, row in df_meta.iterrows()
#                         }
#
#                         records = []
#                         print("🔍 Matching submatrices in:", folder_path)
#
#                         for filename in os.listdir(folder_path):
#                             if filename.endswith('.csv') and filename.startswith("submatrix_ptt-"):
#                                 match = re.search(r'\((\d+),', filename)
#                                 if not match:
#                                     print(f"❌ Skipping (no match): {filename}")
#                                     continue
#
#                                 defect_no = int(match.group(1))
#
#                                 if defect_no not in meta_dict:
#                                     print(f"⚠️ Defect {defect_no} not in metadata, skipping.")
#                                     continue
#
#                                 file_path = os.path.join(folder_path, filename)
#                                 matrix = pd.read_csv(file_path, dtype=str)
#                                 matrix = matrix.apply(pd.to_numeric, errors='coerce').fillna(0)
#
#                                 flat = matrix.values.flatten().astype(np.float32)
#                                 flat = (flat - np.mean(flat)) / (np.std(flat) + 1e-8)
#
#                                 meta = meta_dict[defect_no]
#                                 record = {
#                                     'filename': filename,
#                                     'def_no.': defect_no,
#                                     'submatrix': flat.tolist(),
#                                     'speed': meta['speed'],
#                                     'Start_sensor': meta['Start_sensor'],
#                                     'End_sensor': meta['End_sensor'],
#                                     'pred_width': meta['pred_width'],
#                                 }
#
#                                 records.append(record)
#                         df_test = pd.DataFrame(records)
#                         print("✅ Final test dataset shape:", df_test.shape)
#                         print(df_test.shape)
#
#                         if model != None:
#                             print("Model successfully loaded ")
#                         else:
#                             print("error loading model")
#                         filename = df_test['filename'] if 'filename' in df_test.columns else [f"sample_{i}" for i in
#                                                                                               range(len(df_test))]
#                         df_test.drop(columns=['filename'], inplace=True, errors='ignore')
#                         # df_test['submatrix'] = df_test['submatrix'].apply(lambda s: [float(x) for x in ast.literal_eval(s)])
#                         features = df_test.apply(extract_features, axis=1, result_type='expand')
#                         feature_columns = ['mean', 'std', 'max', 'min', 'threshold_crossings', 'anomaly_score',
#                                            'cwt_median'] + [f'fft_{i}' for i in range(10)]
#                         features.columns = feature_columns
#                         print(feature_columns)
#                         print(filename)
#                         final_df = pd.concat([features, df_test[['speed', 'Start_sensor', 'End_sensor', 'pred_width']]],
#                                              axis=1)
#                         final_df.drop(columns=['std'], inplace=True)
#                         print(final_df.columns)
#                         final_df.rename(columns={"End_sensor": "End_Sensor"}, inplace=True)
#                         # pred = model.predict(final_df)
#                         pred = np.floor(model.predict(final_df)).astype(int)
#                         cursor = connection.cursor()
#                         for defect_no, pred_val in zip(df_test['def_no.'], pred):
#                             cursor.execute("UPDATE defect_clock_hm SET width_new = %s WHERE id = %s",
#                                            (int(pred_val), int(defect_no)))
#                         connection.commit()
#
#                     model = joblib.load("C:/Users/admin/PycharmProjects/GMFL_12_Inch_Desktop/rf_width_model.pkl")
#                     model_width(model, output_dir_def)
#
#                     df_new_1 = df_new[[f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]]

                    fig = figx112
                    self.fig_plot = fig

                    plotly.offline.plot(fig, filename='heatmap_new.html', auto_open=False)
                    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "heatmap_new.html"))
                    self.m_output.load(QUrl.fromLocalFile(file_path))

                    self.save_as_img(self.fig_plot, self.project_name, self.Weld_id_tab9)
                    config.print_with_time("End of conversion at : ")

                    # Show web engine, hide canvas
                    self.m_output.setVisible(True)
                    self.canvas_tab9.setVisible(False)
                    self.reset_btn_tab9.setVisible(False)
                    self.all_box_selection1.setVisible(False)

            print("hiiii")
            # QMessageBox.about(self, 'Pipe Analysis', 'Data Analysed Successfully')

            with connection.cursor() as cursor:
                Fetch_weld_detail = "select id,pipe_id,WT,absolute_distance,upstream,defect_type,dimension_classification,orientation,length,Width,depth from defect_clock_hm where runid='%s' and pipe_id='%s'"
                cursor.execute(Fetch_weld_detail, (self.runid, self.Weld_id_tab9))
                self.myTableWidget_tab9.setRowCount(0)
                allSQLRows = cursor.fetchall()
                try:
                    if allSQLRows:
                        for row_number, row_data in enumerate(allSQLRows):
                            self.myTableWidget_tab9.insertRow(row_number)
                            for column_num, data in enumerate(row_data):
                                self.myTableWidget_tab9.setItem(row_number, column_num,
                                                                QtWidgets.QTableWidgetItem(str(data)))
                        # self.myTableWidget_tab9.setEditTriggers(QAbstractItemView.NoEditTriggers)
                        self.myTableWidget_tab9.setContextMenuPolicy(Qt.CustomContextMenu)
                        self.myTableWidget_tab9.customContextMenuRequested.connect(self.open_context_menu_ori_tab9)
                        # Check canvas visibility before adding the double-click functionality
                        if self.canvas_tab9.isVisible():
                            self.myTableWidget_tab9.doubleClicked.connect(self.handle_table_double_click_chm)

                except pymysql.Error as e:
                    print(f"MySQL Error: {e}")

    def save_as_img(self, heat_map_obj, company_name, Weld_id):
        """
        This will save the plotted chat as a image format
            :param heat_map_obj:object of seaborn heatmap
            :param company_name:company name used to create folder
            :param Weld_id:Image of graph will be saved as pipe Id
        """
        # print(heat_map_obj)
        print(company_name)
        print(Weld_id)
        # figure = heat_map_obj.
        print("here1")
        img_path = config.image_folder + company_name
        img_name = str(Weld_id) + '.html'
        # img_name = str(lower_sensitivity + upper_sensitivity) + '.png'

        try:
            os.makedirs(img_path)
        except OSError as error:
            pass
        print("path", img_path + img_name)
        heat_map_obj.write_html(img_path + '/' + img_name)
        print("here 2")
        # im = Image.open(img_path + '/' + img_name)
        # im1 = im.rotate(360, expand=1)
        # im1.save(img_path + '/' + img_name)
        # # Setting the points for cropped image
        # left = 200
        # top = 100
        # right = 2400
        # bottom = 5000
        #
        # im = Image.open(img_path + '/' + img_name)
        # # #im1 = im.crop((left, top, right, bottom))
        # im1.save(img_path + '/' + img_name)

    def open_context_menu_ori_tab9(self, position):
        index = self.myTableWidget_tab9.indexAt(position)
        print("index", index)
        if not index.isValid():
            return

        # Select the entire row
        self.myTableWidget_tab9.selectRow(index.row())
        context_menu = QMenu()
        # context_menu = QtWidgets.QMenuBar()
        delete_action = QAction("Delete Row", self)
        # menuEdit = QtWidgets.QMenu(self.menubar)
        delete_action.triggered.connect(lambda: self.delete_row_ori_tab9(index.row()))
        context_menu.addAction(delete_action)
        context_menu.exec_(self.myTableWidget_tab9.viewport().mapToGlobal(position))

    def delete_row_ori_tab9(self, row):
        if row < 0:
            return

        # Get the ID of the selected row
        id_item = self.myTableWidget_tab9.item(row, 0)
        if id_item is None:
            return
        row_id = id_item.text()
        print("row_id", row_id)

        # Confirm deletion
        reply = QMessageBox.question(self, 'Delete Row', 'Are you sure you want to delete this row?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                connection2 = pymysql.connect(host='localhost', user='root', password='root', db='mfldesktop')
                # Delete the row from the database
                with connection2.cursor() as cursor:
                    # print("row_id....",row_id)
                    Fetch_weld_detail = "DELETE from defect_sensor_hm WHERE id='%s'"
                    # Execute query.
                    cursor.execute(Fetch_weld_detail, (int(row_id)))
                    # cursor.execute(f"DELETE from defect_sensor_hm WHERE id=",row_id)
                    connection2.commit()
                    # connection.close()
                    # Delete the row from the table widget
                    self.myTableWidget_tab9.removeRow(row)
                    QMessageBox.information(self, "Information", "Row deleted successfully")
            except:
                pass

    def all_box_selection_ori_heatmap(self):
        try:
            # Clear existing patches and annotations on the figure
            ax = self.figure_tab9.gca()

            # Iterate over all rows in the table
            row_count = self.myTableWidget_tab9.rowCount()
            if row_count == 0:
                QMessageBox.warning(self, "No Data", "The table is empty. No defects to display.")
                return

            for row_number in range(row_count):
                defect_id = self.myTableWidget_tab9.item(row_number, 0).text()
                weld_id = self.Weld_id_tab9
                runid = self.runid

                with connection.cursor() as cursor:
                    query_for_coordinates = "SELECT id, start_index, end_index, start_sensor, end_sensor from defect_clock_hm WHERE pipe_id = %s AND runid = %s AND id = %s"
                    cursor.execute(query_for_coordinates, (weld_id, runid, defect_id))
                    result = cursor.fetchone()

                    id, start_index, end_index, y_start_hm, y_end_hm = result

                    if None in (start_index, end_index, y_start_hm, y_end_hm):
                        print(f"Warning: Invalid coordinates for defect ID {id}. Skipping.")
                        continue

                    # # Calculate rectangle coordinates
                    # rect_x = (start_index + end_index) / 2
                    # rect_y = (y_start_hm + y_end_hm) / 2
                    #
                    # # Draw the rectangle
                    # rect = plt.Rectangle(
                    #     (start_index, y_start_hm),
                    #     end_index - start_index,
                    #     y_end_hm - y_start_hm,
                    #     linewidth=1, edgecolor='black', facecolor='none'
                    # )
                    # ax.add_patch(rect)

                    # Adjust for correct alignment with Plotly's rectangle dimensions
                    rect_x = start_index
                    rect_y = y_start_hm
                    rect_width = (end_index - start_index)  # Adjust for center alignment
                    rect_height = ((y_end_hm + 0.5) - (y_start_hm - 0.5))   # Adjust for center alignment

                    # Create and add the rectangle to the plot
                    rect = plt.Rectangle(
                        (rect_x, rect_y),  # Set bottom-left corner
                        rect_width,  # Width
                        rect_height,  # Height
                        linewidth=1, edgecolor='black', facecolor='none'
                    )
                    ax.add_patch(rect)

                    # Add the text annotation
                    text_x = start_index + (end_index - start_index)/2
                    text_y = rect_y - 2  # Slightly above the box
                    # text_y = rect_y + (y_end_hm - y_start_hm) * 0.1  # Slightly above the box
                    ax.text(
                        text_x, text_y,
                        # f"ID: {id}\nL: {length_odd1}\nW: {breadth}",
                        f"{id}",
                        color='white',
                        ha='center', va='center',
                        fontsize=9, weight='bold',
                        path_effects=[
                        path_effects.withStroke(linewidth=2, foreground='black')  # Black outline
                    ]
                        )
                    # print(f"Rectangle and text drawn for defect ID: {id}.")

            # Refresh the canvas to display all rectangles and annotations
            self.canvas_tab9.draw_idle()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to draw boxes for all defects: {str(e)}")

    def handle_table_double_click_chm(self):
        weld_id = self.Weld_id_tab9
        runid = self.runid

        selected_row = self.myTableWidget_tab9.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please double-click on a valid cell.")
            return

        defect_id = self.myTableWidget_tab9.item(selected_row, 0).text()
        try:
            with connection.cursor() as cursor:
                query_for_coordinates = "SELECT id, start_index, end_index, start_sensor, end_sensor, length, Width, depth from defect_clock_hm WHERE pipe_id = %s AND runid = %s AND id = %s"
                cursor.execute(query_for_coordinates, (weld_id, runid, defect_id))
                result = cursor.fetchone()
                print(f"Query Result: {result}")

                if not result:
                    QMessageBox.warning(self, "No Data", "No data found for the selected defect.")
                    return

                id, start_index, end_index, y_start_hm, y_end_hm, length_odd1, breadth, depth = result

                # Calculate rectangle coordinates
                rect_x = start_index - 0.5
                rect_y = y_start_hm - 0.5
                rect_width = (end_index - start_index) + 1  # Adjust for center alignment
                rect_height = (y_end_hm - y_start_hm) + 1.5  # Adjust for center alignment

                # Create and add the rectangle to the plot
                rect = plt.Rectangle(
                    (rect_x, rect_y),  # Set bottom-left corner
                    rect_width,  # Width
                    rect_height,  # Height
                    linewidth=1, edgecolor='black', facecolor='none'
                )
                ax = self.figure_tab9.gca()
                ax.add_patch(rect)

                # Add the text annotation
                text_x = start_index + (end_index - start_index)/2
                text_y = y_start_hm - 6  # Slightly above the box
                # text_y = rect_y + (y_end_hm - y_start_hm) * 0.1  # Slightly above the box
                ax.text(
                    text_x, text_y,
                    f"L: {length_odd1}\nW: {breadth}\nD: {depth}",
                    color='white',
                    ha='center', va='center',
                    fontsize=9, weight='bold',
                    path_effects=[
                        path_effects.withStroke(linewidth=2, foreground='black')  # Black outline
                    ]
                )

                self.canvas_tab9.draw_idle()  # Ensure the canvas is updated.

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to draw box: {str(e)}")

    def reset_btn_fun_chm(self):
        if self.figure_tab9.gca().patches:
            for patch in self.figure_tab9.gca().patches:
                patch.remove()
            for text in self.figure_tab9.gca().texts:
                text.remove()
            self.canvas_tab9.draw()
            self.rect_start_clockhm = None  # Store the starting point of the rectangle
            self.rect_end_clockhm = None

    def line_select_callback_chm(self, eclick, erelease):
        self.rect_start_chm = eclick.xdata, eclick.ydata
        self.rect_end_chm = erelease.xdata, erelease.ydata
        self.draw_rectangle_chm()

    def draw_rectangle_chm(self):
        # Function to draw a rectangle on the Matplotlib plot
        if self.rect_start_chm is not None and self.rect_end_chm is not None:
            for patch in self.figure_tab9.gca().patches:
                patch.remove()
            x_start, y_start = self.rect_start_chm
            x_end, y_end = self.rect_end_chm
            if x_start is not None and y_start is not None and x_end is not None and y_end is not None:
                rect = plt.Rectangle(
                    (min(x_start, x_end), min(y_start, y_end)),
                    abs(x_end - x_start),
                    abs(y_end - y_start),
                    edgecolor='black',
                    linewidth=1,
                    fill=False
                )
                self.figure_tab9.gca().add_patch(rect)
                self.canvas_tab9.draw()
                self.show_name_dialog_chm()

    def show_name_dialog_chm(self):
        while True:
            name, ok = QInputDialog.getText(self, 'Enter Name', 'Enter the name of the drawn box:')
            if ok:
                if name.strip():  # Check if the entered name is not empty or just whitespace
                    x_start, y_start = self.rect_start_chm
                    x_end, y_end = self.rect_end_chm
                    runid = self.runid
                    pipe = self.Weld_id_tab9
                    start_index15 = self.index_chm[round(x_start)]
                    end_index15 = self.index_chm[round(x_end)]
                    start_index_c = round(x_start)
                    end_index_c = round(x_end)
                    y_start15 = round(y_start)
                    y_end15 = round(y_end)
                    print("start_index15", start_index15)
                    print("end_index15", end_index15)
                    print("start_sensor", y_start15)
                    print("end_sensor", y_end15)
                    print("start_index_c", start_index_c)
                    print("end_index_c", end_index_c)

                    finial_defect_list = []

                    """
                    Fetching data from Google Big Query each holl sensor
                    """
                    query_for_start = 'SELECT index,ODDO1,ODDO2,[F1H1 ,F1H2 ,F1H3 ,F1H4 ,F2H1 ,F2H2 ,F2H3 ,F2H4 ,F3H1 ,F3H2 ,F3H3 ,F3H4 ,F4H1 ,F4H2 ,F4H3 ,' \
                                      'F4H4 ,F5H1 ,F5H2 ,F5H3 ,F5H4 ,F6H1 ,F6H2 ,F6H3 ,F6H4 ,F7H1 ,F7H2 ,F7H3 ,F7H4 ,F8H1 ,F8H2 ,F8H3 ,' \
                                      'F8H4 ,F9H1 ,F9H2 ,F9H3 ,F9H4 ,F10H1 ,F10H2 ,F10H3 ,F10H4 ,F11H1 ,F11H2 ,F11H3 ,F11H4 ,F12H1 ,F12H2 ,F12H3 ,' \
                                      'F12H4 ,F13H1 ,F13H2 ,F13H3 ,F13H4 ,F14H1 ,F14H2 ,F14H3 ,F14H4 ,F15H1 ,F15H2 ,F15H3 ,F15H4 ,F16H1 ,F16H2 ,F16H3 ,' \
                                      'F16H4 ,F17H1 ,F17H2 ,F17H3 ,F17H4 ,F18H1 ,F18H2 ,F18H3 ,F18H4 ,F19H1 ,F19H2 ,F19H3 ,F19H4 ,F20H1 ,F20H2 ,F20H3 ,' \
                                      'F20H4 ,F21H1 ,F21H2 ,F21H3 ,F21H4 ,F22H1 ,F22H2 ,F22H3 ,F22H4 ,F23H1 ,F23H2 ,F23H3 ,F23H4 ,F24H1 ,F24H2 ,F24H3 ,' \
                                      'F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4,' \
                                      'F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1, ' \
                                      'F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4],' \
                                      'ROLL FROM ' + config.table_name + ' WHERE index>={} AND index<={} AND runid={} order by index'
                    query_job = client.query(query_for_start.format(start_index15, end_index15, runid))
                    results = query_job.result()
                    """
                    End fetching data from Google Bigquery
                    """
                    index1 = []
                    oddo_1 = []
                    oddo_2 = []
                    holl_sensor = []
                    roll = []

                    for k in results:
                        index1.append(k[0])
                        oddo_1.append(k[1])
                        oddo_2.append(k[2])
                        holl_sensor.append(k[3])
                        roll.append(k[4])

                    # print('oddo1', oddo_1)

                    self.oddo1_chmd = []
                    self.oddo2_chmd = []
                    roll4 = []
                    for odometer1 in oddo_1:
                        od1 = odometer1 - config.oddo1  ### change According to run
                        self.oddo1_chmd.append(od1)
                    for odometer2 in oddo_2:
                        od2 = odometer2 - config.oddo2  ### change According to run
                        self.oddo2_chmd.append(od2)
                    """
                    Reference value will be consider
                    """
                    for roll2 in roll:
                        roll3 = roll2 - config.roll_value
                        roll4.append(roll3)
                    """
                    Fetching data from Google Big Query each proximity sensor
                    """
                    query_for_start_proximity = 'SELECT index,[F1P1,F2P2,F3P3,F4P4,F5P1,F6P2,F7P3,F8P4,F9P1,F10P2,F11P3,F12P4,F13P1,F14P2,F15P3,F16P4,F17P1,F18P2,F19P3,F20P4,F21P1,F22P2,F23P3,F24P4, F25P1, F26P2, F27P3, F28P4, F29P1, F30P2, F31P3, F32P4, F33P1, F34P2, F35P3, F36P4] FROM ' + config.table_name + ' WHERE index>{} AND index<{} order by index'
                    query_job_proximity = client.query(query_for_start_proximity.format(start_index15, end_index15))
                    results_1 = query_job_proximity.result()
                    proximity = []
                    for row1 in results_1:
                        proximity.append(row1[1])
                    self.df_new_proximity_chmd = pd.DataFrame(proximity,
                                                         columns=['F1P1', 'F2P2', 'F3P3', 'F4P4', 'F5P1', 'F6P2', 'F7P3', 'F8P4',
                                                                  'F9P1', 'F10P2', 'F11P3', 'F12P4', 'F13P1', 'F14P2', 'F15P3',
                                                                  'F16P4', 'F17P1', 'F18P2', 'F19P3',
                                                                  'F20P4', 'F21P1', 'F22P2', 'F23P3', 'F24P4', 'F25P1', 'F26P2', 'F27P3', 'F28P4', 'F29P1', 'F30P2',
                                                                  'F31P3', 'F32P4', 'F33P1', 'F34P2', 'F35P3', 'F36P4'])

                    # print("oddo1_chmd", self.oddo1_chmd)
                    # print("oddo1_li_chm", self.oddo1_li_chm)

                    submatrix = self.clock_col.iloc[start_index_c:end_index_c + 1, y_start15:y_end15 + 1]
                    # submatrix = submatrix.apply(pd.to_numeric, errors='coerce')  # Ensure numeric data
                    if submatrix.isnull().values.any():
                        print("Submatrix contains NaN values, skipping this iteration.")
                        continue
                    print(submatrix)
                    two_d_list = submatrix.values.tolist()

                    max_value = submatrix.max().max()
                    min_positive = min(x for row in two_d_list for x in row if x > 0)

                    depth_old = (max_value-min_positive)/min_positive*100
                    print("depth_old", depth_old)

                    """
                    Calculate Upstream Distance oddo1 and oddo2
                    """
                    upstream_oddo1=(self.oddo1_chmd[0]-self.oddo1_li_chm[0])/1000
                    print("upstream_oddo1=>", upstream_oddo1)

                    """
                    Calculate length of the defect
                    """
                    length_of_defect_oddo1=round(self.oddo1_chmd[-1] - self.oddo1_chmd[0])
                    length_of_defect_oddo2 = round(self.oddo2_chmd[-1] - self.oddo2_chmd[0])
                    print("length_of_defect_oddo1=>", length_of_defect_oddo1)
                    print("length_of_defect_oddo2=>", length_of_defect_oddo2)

                    """
                    Calculate Abs.Distance of the defect
                    """
                    Abs_Distance=(self.oddo1_chmd[0])/1000
                    print("Abs.distance_oddo1=>", Abs_Distance)

                    """
                    Calculate latitude and longitude 
                    """
                    long, lat = lat_long(Abs_Distance, self.runid)
                    print("latitude", lat)
                    print("longitude", long)

                    """
                    Calculate Width of the Defect
                    """
                    Width=Width_calculation(y_start15, y_end15)
                    Width=round(Width)
                    print("Width of Defect=>", Width)

                    counter_difference_1 = (y_end15 + 1) - (y_start15 + 1)
                    divid_1 = int(counter_difference_1/2)
                    center_1 = y_start15 + divid_1

                    factor1_1 = divid_1 * config.w_per_1
                    start1_1 = (int(center_1 - factor1_1)) - 1
                    end1_1 = (int(center_1 + factor1_1)) - 1

                    width_new = Width_calculation(start1_1, end1_1)
                    print("width_new", width_new)

                    """
                    Calculate Wall thickness
                    """
                    # if self.Weld_id_tab9 == 2:
                    #     wt = Config.pipe_thickness
                    # else:
                    #     wt = Config.pipe_thickness

                    wt = config.pipe_thickness

                    """
                    Find the maximum value of each holl sensor
                    """
                    each_holl_sensor_max_value = [i*0 for i in range(1, 145)]

                    for l, data in enumerate(self.clock_data_col):
                        # print("l", l)
                        # print("data", data)
                        for m, data1 in enumerate(data):
                            # print("m", m)
                            # print("data1", data1)
                            if m >= y_start15 - 1 and m < y_end15:
                                if data1 > each_holl_sensor_max_value[m]:
                                    each_holl_sensor_max_value[m] = data1
                    # print("maximum_value", each_holl_sensor_max_value)
                    """
                    Get rows of start_observation at the 0th Position of element in holl sensor 2d list
                    """
                    initial_observation = self.clock_data_col[0]
                    # print("base_value", initial_observation)
                    kx = []
                    for i2 in range(0, 144):
                        if i2 >= y_start15 - 1 and i2 < y_end15:
                            kx.append(initial_observation[i2])
                        else:
                            kx.append(0)
                    # print("initial_observation", kx)
                    """
                    Difference between max_value_list and initial_observation
                    """
                    zip_object = zip(each_holl_sensor_max_value, kx)
                    difference_list = []
                    for list1_i, list2_i in zip_object:
                        difference_list.append(list1_i - list2_i)
                    # print("difference list",difference_list)
                    """
                    Get max_value_difference_value
                    """
                    max_value_difference_value = max(difference_list)
                    # print("max_value_diiference_value",max_value_difference_value)
                    """
                    Get index max_value_difference_value
                    """
                    max_value_difference_index = difference_list.index(max_value_difference_value)
                    print("sensor_no", max_value_difference_index)
                    """
                    Check max_value_list inside the index and get max_value
                    """
                    max_value = self.mean_clock_data[max_value_difference_index]
                    print("max_value", max_value)
                    """
                    Check initial_observation inside the index and get base value
                    """
                    index_val = round((y_start15 + y_end15)/2)
                    base_value = self.mean_clock_data[index_val]
                    print("base_value", base_value)

                    # depth_old = abs(((max_value - base_value) / base_value) * 100)
                    # print("depth_old...", depth_old)

                    depth_new = round((((length_of_defect_oddo1 / Width) * (max_value / base_value)) * 100) / config.pipe_thickness, 2)
                    print("depth_new...", depth_new)

                    """
                    .................Orientation Calculation..........................
                    """
                    # angle = self.clock_col.columns[index_val]
                    # # angle = defect_angle_x(roll4, max_value_difference_index)
                    # print("angle", angle)

                    avg_counter = round((start_index_c + end_index_c)/2)
                    avg_sensor = round((y_start15+y_end15)/2)
                    angle = self.map_ori_sens_ind.iloc[avg_counter, avg_sensor]
                    # k2 = self.map_ori_sens_ind.iloc[avg_counter, avg_sensor]
                    # angle = k2[2]
                    print("angle", angle)

                    """
                    Calculate length_percent of the defect
                    """
                    counter_difference = end_index_c - start_index_c
                    # print("counter_difference", counter_difference)
                    divid = int(counter_difference/2)
                    center = start_index_c+divid

                    factor1 = divid * config.l_per_1
                    start1 = int(center - factor1)
                    end1 = int(center + factor1)
                    l_per1 = (self.oddo1_li_chm[end1] - self.oddo1_li_chm[start1])

                    factor2 = divid * config.l_per_2
                    start2 = int(center - factor2)
                    end2 = int(center + factor2)
                    l_per2 = (self.oddo1_li_chm[end2] - self.oddo1_li_chm[start2])

                    factor3 = divid * config.l_per_3
                    start3 = int(center - factor3)
                    end3 = int(center + factor3)
                    l_per3 = (self.oddo1_li_chm[end3] - self.oddo1_li_chm[start3])

                    factor4 = divid * config.l_per_4
                    start4 = int(center - factor4)
                    end4 = int(center + factor4)
                    l_per4 = (self.oddo1_li_chm[end4] - self.oddo1_li_chm[start4])

                    # print("start_percent", start_percent)
                    # print("end_percent", end_percent)
                    # print("length_percent=>", length_percent)

                    defect_start_oddo = self.oddo1_li_chm[start_index_c]
                    defect_end_oddo = self.oddo1_li_chm[end_index_c]/1000

                    print("defect_start_oddo", defect_start_oddo)
                    print("defect_end_oddo", defect_end_oddo)

                    time_sec = end_index15/1500

                    speed = defect_end_oddo/time_sec
                    print("speed(m/s)", speed)

                    """
                    Calculate defect_type of the defect
                    """
                    internal_external = internal_or_external(self.df_new_proximity_chmd, max_value_difference_index)
                    print("internal_external", internal_external)

                    """
                    Calculate dimension_classification of the defect
                    """
                    dimension_classification = get_type_defect_1(config.pipe_thickness, runid, length_of_defect_oddo1, Width)
                    print("dimension_classification", dimension_classification)

                    finial_defect_list.append({"runid": runid, "start_reading": start_index_c, "end_reading": end_index_c,
                                     "start_sensor": y_start15,
                                     "end_sensor": y_end15,
                                     "absolute_distance": Abs_Distance, "upstream_oddo1": upstream_oddo1,
                                     "length": length_of_defect_oddo1, "breadth": Width, "width_new": width_new, 'orientation': angle,
                                     "dimension_classification": dimension_classification, "defect_type": internal_external,
                                     "depth": depth_old, "WT":wt,
                                     "max_value": max_value, "base_value": base_value, "min_value": min_positive,
                                     "l_per1": l_per1,
                                     # "l_per2": l_per2,"l_per3": l_per3,"l_per4": l_per4,
                                     "speed": speed, "latitude":lat,"longitude":long
                                     })

                    for i in finial_defect_list:
                        runid = i['runid']
                        start_index = i['start_reading']
                        end_index = i['end_reading']
                        start_sensor = i['start_sensor']
                        end_sensor = i['end_sensor']
                        absolute_distance = round(i['absolute_distance'], 3)
                        upstream_oddo1 = round(i['upstream_oddo1'], 3)
                        length = round(i['length'])
                        Width = round(i['breadth'])
                        width_new = round(i['width_new'])
                        depth = round(i['depth'])
                        orientation = i['orientation']
                        dimension_classification = i['dimension_classification']
                        defect_type = i['defect_type']
                        max_value = round(i['max_value'])
                        base_value = round(i['base_value'])
                        min_value = round(i['min_value'])
                        l_per1 = round(i['l_per1'])
                        # l_per2 = round(i['l_per2'])
                        # l_per3 = round(i['l_per3'])
                        # l_per4 = round(i['l_per4'])
                        WT = i['WT']
                        speed = round(i['speed'], 2)
                        latitude = i['latitude']
                        longitude = i['longitude']
                        with connection.cursor() as cursor:
                            query_defect_insert = "INSERT into defect_clock_hm(runid, pipe_id, pipe_length, start_index, end_index, start_sensor, end_sensor, upstream, absolute_distance, orientation, length, Width, width_new, depth,max_value, min_value, l_per1, dimension_classification,defect_type, mean_value, WT, speed, latitude, longitude) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

                            cursor.execute(query_defect_insert, (
                                int(runid), self.Weld_id_tab9, self.pipe_len_oddo1_chm, start_index, end_index,
                                start_sensor, end_sensor, upstream_oddo1, absolute_distance, orientation,
                                 length, Width, width_new, depth, max_value, min_value, l_per1, dimension_classification,
                                defect_type,base_value,  WT, speed, latitude, longitude))

                        connection.commit()
                        QMessageBox.information(self, 'Success', 'Data saved')

                        with connection.cursor() as cursor:
                            Fetch_weld_detail = "select id,pipe_id,WT,absolute_distance,upstream,defect_type,dimension_classification,orientation,length,Width,depth from defect_clock_hm where runid='%s' and pipe_id='%s'"
                            # Execute query.
                            cursor.execute(Fetch_weld_detail, (int(self.runid), int(self.Weld_id_tab9)))
                            self.myTableWidget_tab9.setRowCount(0)
                            allSQLRows = cursor.fetchall()
                            if allSQLRows:
                                for row_number, row_data in enumerate(allSQLRows):
                                    self.myTableWidget_tab9.insertRow(row_number)
                                    for column_num, data in enumerate(row_data):
                                        self.myTableWidget_tab9.setItem(row_number, column_num,
                                                                    QtWidgets.QTableWidgetItem(str(data)))
                                        self.myTableWidget_tab9.setContextMenuPolicy(Qt.CustomContextMenu)
                                        self.myTableWidget_tab9.customContextMenuRequested.connect(self.open_context_menu_ori_tab9)
                                        self.myTableWidget_tab9.doubleClicked.connect(self.handle_table_double_click_chm)

                    break  # Exit the loop if a valid name is provided
                else:
                    QMessageBox.warning(self, 'Invalid Input', 'Please enter a name.')
            else:
                print('Operation canceled.')
                break

    """
---->Heatmap(clock VS oddo) tab(7) functions ends here
    """

    """
---->Graph tab(8) functions starts from here
    """
    def Magnetization(self):
        weld_id_1 = self.combo_graph.currentText()
        self.weld_id_1 = int(weld_id_1)
        runid = self.runid
        with connection.cursor() as cursor:
            # query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
            query = "SELECT start_index, end_index,start_oddo1,end_oddo1 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"
            cursor.execute(query, (self.runid, self.weld_id_1, self.runid, self.weld_id_1))
            result = cursor.fetchall()
            start_oddo1 = result[0][2]
            end_oddo1 = result[1][3]

            start_index, end_index = result[0][0], result[1][1]
            print(start_index, end_index)
            # Config.print_with_time("Start fetching at : ")

            query_for_start = 'SELECT index,ODDO1,ODDO2,[F1H1, F1H2, F1H3, F1H4, F2H1, F2H2, F2H3, F2H4,F3H1, F3H2, F3H3, F3H4, F4H1, F4H2, F4H3,F4H4, F5H1, F5H2, F5H3, F5H4, F6H1, F6H2, F6H3, F6H4,F7H1, F7H2, F7H3, F7H4, F8H1, F8H2, F8H3, F8H4, F9H1, F9H2, F9H3, F9H4, F10H1,F10H2, F10H3, F10H4,F11H1, F11H2, F11H3, F11H4, F12H1, F12H2, F12H3, F12H4, F13H1, F13H2, F13H3,F13H4, F14H1, F14H2, F14H3, F14H4,F15H1, F15H2, F15H3, F15H4, F16H1, F16H2, F16H3, F16H4, F17H1, F17H2, F17H3,F17H4, F18H1, F18H2, F18H3, F18H4,F19H1, F19H2, F19H3, F19H4, F20H1, F20H2, F20H3, F20H4, F21H1, F21H2, F21H3,F21H4, F22H1, F22H2, F22H3, F22H4,F23H1, F23H2, F23H3, F23H4, F24H1, F24H2, F24H3, F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4, F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1, F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4] FROM ' + config.table_name + ' WHERE index>{} AND index<{} order by index'
            query_job = client.query(query_for_start.format(start_index, end_index))
            results = query_job.result()
            data = []
            self.index_tab_m = []
            oddo_x = []
            oddo_y = []
            data1 = []

            config.print_with_time("Start of conversion at : ")
            for row in results:
                self.index_tab_m.append(row[0])
                oddo_x.append(row[1])
                oddo_y.append(row[2])
                data1.append(row[3])

            self.oddo1_tab_m = []
            self.oddo2_tab_m = []

            """
            Reference value will be consider 
            """
            for odometer1 in oddo_x:
                od1 = odometer1 - config.oddo1  ###16984.2 change According to run
                self.oddo1_tab_m.append(od1)
            for odometer2 in oddo_y:
                od2 = odometer2 - config.oddo2  ###17690.36 change According to run
                self.oddo2_tab_m.append(od2)

            oddometer = [round(x / 1000, 3) for x in self.oddo1_tab_m]
            df_new_tab9 = pd.DataFrame(data1, columns=[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)])
            mean_row_wise_dataframe = df_new_tab9.mean(axis=1)
            sensor_max_value = 65535        # maximum value of any sensor
            sensor_voltage_level = 3.3      # 3.3volt (currently fixed)
            # Senstivity of the sensor: miliTesla(mT) [this is variable and changed everytime when sensor are changed]
            sensor_senstivity = 50          # This senstivity value is 731 sensor used

            # 1mT = 10 Gauss
            # mT = mT * 10 Gauss
            # Gauss to magnetization: Gauss * 0.079

            multiply_by_factor_magnetization = ((((mean_row_wise_dataframe/sensor_max_value)*sensor_voltage_level)/sensor_senstivity)*10)*0.079

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[self.index_tab_m, oddometer], y=multiply_by_factor_magnetization))
            fig.update_xaxes(
                tickfont=dict(size=11),
                dtick=500,
                title_text="Absolute Distance(m))",
                tickangle=0, showticklabels=True, ticklen=0)
            fig.update_yaxes(
                title_text="Magnetization",
            )
            fig.update_layout(
                # dragmode='select',
                # width=1300,  # Set the width of the figure
                # height=300,  # Set the height of the figure
                title='Magnetization Graph'
            )

            config.print_with_time("End of conversion at : ")
            pio.write_html(fig, file='h_magnetization.html', auto_open=False)
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "h_magnetization.html"))
            self.m_output_graph.load(QUrl.fromLocalFile(file_path))

    def Velocity(self):
        print("hii")
        weld_id_1 = self.combo_graph.currentText()
        self.weld_id_1 = int(weld_id_1)
        runid = self.runid
        with connection.cursor() as cursor:
            # query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
            query = "SELECT start_index, end_index,start_oddo1,end_oddo1 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"
            cursor.execute(query, (self.runid, self.weld_id_1, self.runid, self.weld_id_1))
            result = cursor.fetchall()
            start_oddo1 = result[0][2]
            end_oddo1 = result[1][3]

            start_index, end_index = result[0][0], result[1][1]
            print(start_index, end_index)

            config.print_with_time("Start fetching at : ")
            query_for_start = 'SELECT index,ODDO1,ODDO2 FROM ' + config.table_name + ' WHERE index>{} AND index<{} order by index'
            query_job = client.query(query_for_start.format(start_index, end_index))
            results = query_job.result().to_dataframe()

            results['ODDO1'] = (results['ODDO1'] - config.oddo1) / 1000
            config.print_with_time("End fetching at : ")

            # filtered_df = results[(results['index'] >= start_index) & (results['index'] <= end_index)].copy()
            results['Seconds'] = ((results['index'] - start_index) // 150) + 1

            unique_seconds = results['Seconds'].unique()
            velocity_results = []

            for sec in unique_seconds:
                rows = results[results['Seconds'] == sec]
                # print(rows)
                if not rows.empty:
                    start = rows.iloc[0]['ODDO1']
                    end = rows.iloc[-1]['ODDO1']
                    occurrences = len(rows)
                    velo_result = (end - start) / (0.1)
                    velocity_results.append({'Seconds': sec, 'Start_oddo1': start, 'End_oddo1': end, 'Occurrences': occurrences, 'Result': velo_result})

            velocity_results_df = pd.DataFrame(velocity_results)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[velocity_results_df.index, round(velocity_results_df['Start_oddo1'], 3)], y=velocity_results_df['Result'], mode='lines', line=dict(color='blue')))

            # k = []
            # for i in range(len(results['ODDO1']) - 1):
            #     t = results['ODDO1'][i + 1] - results['ODDO1'][i]
            #     speed = t / 0.000666667
            #     k.append(speed)
            # last_value = k[-1]
            # k.append(last_value)
            # results['speed'] = k
            # oddometer = results['ODDO1'].round(2)
            # fig = go.Figure()
            # fig.add_trace(go.Scatter(x=[results.index, oddometer], y=results['speed'],line=dict(shape='spline')))

            fig.update_xaxes(
                tickfont=dict(size=11),
                dtick=5,
                title_text="Absolute Distance(m)",
                # showgrid=False,
                tickangle=0, showticklabels=True, ticklen=0
            )
            fig.update_yaxes(
                # range=[0,4],
                title_text="Speed(m/s)",
                # showgrid=False,
            )
            fig.update_layout(
                # dragmode='select',
                # width=1500,  # Set the width of the figure
                # height=400,  # Set the height of the figure
                title='Velocity Profile',
                xaxis=dict(title='Absolute Distance(m)'),
                yaxis=dict(title='Velocity (m/s)', range=[0, 3]),
            )

            pio.write_html(fig, file='h_velocity.html', auto_open=False)
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "h_velocity.html"))
            self.m_output_graph.load(QUrl.fromLocalFile(file_path))

    def Sensor_loss(self):
        print("hii")
        weld_id_1 = self.combo_graph.currentText()
        self.weld_id_1 = int(weld_id_1)
        runid = self.runid
        with connection.cursor() as cursor:
            # query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
            query = "SELECT start_index, end_index,start_oddo1,end_oddo1 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"
            cursor.execute(query, (self.runid, self.weld_id_1, self.runid, self.weld_id_1))
            result = cursor.fetchall()
            start_oddo1 = result[0][2]
            end_oddo1 = result[1][3]

            start_index, end_index = result[0][0], result[1][1]
            print(start_index, end_index)

            config.print_with_time("Start fetching at : ")
            query_for_start = 'SELECT ODDO1 FROM ' + config.table_name + ' WHERE index>{} AND index<{} order by index'
            query_job = client.query(query_for_start.format(start_index, end_index))
            results = query_job.result().to_dataframe()

            results['ODDO1'] = ((results['ODDO1'] - config.oddo1) / 1000).round(3)
            config.print_with_time("End fetching at : ")

            x_labels = results['ODDO1'].astype(str)
            fig = go.Figure()

            # Add a blank trace
            fig.add_trace(go.Scatter(x=x_labels, y=[None]*len(x_labels), mode='lines'))

            # Update x and y axes
            fig.update_xaxes(
                tickfont=dict(size=11),
                title_text="Absolute Distance(m)",
                tickangle=270, showticklabels=True, ticklen=0,
                showgrid=False,
                # dtick=300
            )
            fig.update_yaxes(
                tickfont=dict(size=11),
                title_text="Signal Loss (%)",
                range=[0, 100],
                dtick=10,
                # showgrid=False,
            )

            # Update layout
            fig.update_layout(
                # width=1300,  # Set the width of the figure
                # height=300,  # Set the height of the figure
                title="Sensor Loss Profile"
            )

            pio.write_html(fig, file='h_sensor_loss.html', auto_open=False)
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "h_sensor_loss.html"))
            self.m_output_graph.load(QUrl.fromLocalFile(file_path))

    def Temperature_profile(self):
        print("hi")

    """
---->Graph tab(8) functions ends here
    """

    """
---->Clock calculation starts from here
    """
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
        return f"{hours:02d}:{minutes:02d}"

    def Roll_Calculation(self, df_hall, roll):
        first_key_values = roll
        roll_dictionary = {'1': first_key_values}
        angle = [round(i*2.5, 1) for i in range(0, 144)]

        for i in range(2, 145):
            current_values = [round((value + angle[i - 1]), 2) for value in first_key_values]
            roll_dictionary['{}'.format(i)] = current_values

        clock_dictionary = {}
        for key in roll_dictionary:
            clock_dictionary[key] = [self.degrees_to_hours_minutes(value) for value in roll_dictionary[key]]

        Roll_hr = pd.DataFrame(clock_dictionary)
        df_hall.reset_index(inplace=True, drop=True)
        # df_hall.reset_index(inplace=True, drop=True)
        k=(df_hall.transpose()).astype(float)
        k.reset_index(inplace=True, drop=True)

        # Roll_hr = Roll_hr.rename(columns=dict(zip(Roll_hr.columns, df_hall.columns)))

        time_list = [timedelta(minutes=i * 5) for i in range(144)]
        time_ranges_2 = [(datetime.min + t).strftime('%H:%M') for t in time_list]

        def create_time_dict():
            time_dict = {key: [] for key in time_ranges_2}
            return time_dict

        def check_time_range(time_str):
            start_time = time_ranges_2[0]
            end_time_dt = datetime.strptime(time_ranges_2[1], '%H:%M') - timedelta(seconds=1)
            end_time = end_time_dt.strftime('%H:%M')

            time_to_check = datetime.strptime(time_str, '%H:%M')
            start_time_dt = datetime.strptime(start_time, '%H:%M')

            if start_time_dt <= time_to_check <= end_time_dt:
                return True
            else:
                return False

        time_dict_1 = create_time_dict()
        rang = list(time_dict_1.keys())

        for index, row in Roll_hr.iterrows():
            xl = list(row)
            xd = dict(row)
            xkeys = list(xd.keys())
            c = 0
            for s, d in xd.items():
                if check_time_range(d):
                    # print(s,d)
                    ind = xl.index(d)
                    # print(ind)
                    y = xl[ind:] + xl[:ind]
                    break

            curr = ind
            # ck = xkeys[curr]
            while True:
                ck = xkeys[curr]
                time_dict_1[rang[c]].append((curr, ck, xd[ck]))
                c += 1
                curr = (curr + 1) % len(xkeys)
                if curr == ind:
                    break

        map_ori_sens_ind = pd.DataFrame(time_dict_1)
        # print(map_ori_sens_ind)
        val_ori_sensVal = map_ori_sens_ind.copy()

        def extract_string(cell):
            return cell[1]

        val_ori_sensVal = val_ori_sensVal.applymap(extract_string)

        for r, e in val_ori_sensVal.iterrows():
            c = 0
            for col_name, tup_value in e.items():
                # print(r,col_name,tup_value)
                # cell_v = df_hall.at[r, tup_value]
                # print(cell_v)
                val_ori_sensVal.iloc[r, c] = tup_value
                c += 1
        return map_ori_sens_ind, val_ori_sensVal

    """
---->Clock calculation ends here
    """

    def reset_defect(self):
        runid = self.runid
        self.defect_list = []
        self.GenerateGraph()

    def add_defect(self):
        print("defect_list", self.defect_list)

    def insert_and_update_defect_to_db(self, d_list, runid, pipe_id):
        for defect in d_list:
            print(defect)
            with config.connection.cursor() as cursor:
                query_weld_insert = "INSERT INTO defectdetail (runid, pipe_id, defect_length, defect_breadth, defect_angle,defect_depth,type,x,y,category,min,max) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

                # Execute query.
                b = cursor.execute(query_weld_insert, (
                    int(runid), int(pipe_id), int(defect[2]), int(defect[3]), 0, 0, 'manual', int(defect[0]),
                    int(defect[1]), 'unknown', 0.0, 0.0))
                if b:
                    print("data is inserted successfully")
                else:
                    print("data is not inserted successfully")
                config.connection.commit()
        return

    def pip_info(self):
        try:
            config.print_with_time("pipe info method called")
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
                    path = './Data Frames/' + self.project_name + '/' + self.pipe_id + '.pkl'
                    print(path)
                    if os.path.isfile(path):
                        config.print_with_time("File exist")
                        self.df_pipe = pd.read_pickle(path)
                    else:
                        config.print_with_time("File not exist")
                        try:
                            os.mkdir('./Data Frames/' + self.project_name)
                        except:
                            config.print_with_time("Folder already exists")

                        pipe_start_file = fetched_data[0][3]
                        pipe_start_serial = fetched_data[0][4]
                        pipe_end_file = fetched_data[0][5]
                        pipe_end_serial = fetched_data[0][6]
                        query = 'select * from ' + config.table_name + ' where filename>={} and Serialno>={} and filename<={} and Serialno<={} and runid={} ORDER BY filename, Serialno'
                        query_job = client.query(
                            query.format(pipe_start_file, pipe_start_serial, pipe_end_file, pipe_end_serial, runid))
                        print(query.format(pipe_start_file, pipe_start_serial, pipe_end_file, pipe_end_serial, runid))
                        self.df_pipe = query_job.to_dataframe()
                        config.print_with_time("conversion to data frame is done")
                        self.df_pipe.to_pickle(path)
                        config.print_with_time("successfully  saved to pickle")
                    # self.df_pipe.to_csv('recods.csv)
                    config.info_msg("Data Successfully Loaded", "")
                    # self.pre_graph_analysis()
                else:
                    config.warning_msg("Data not Found", "")
        except OSError as error:
            config.warning_msg(OSError or "Network speed is very slow or invalid Pipe id", "")
            # logger.log_error(error or "Set_msg_body method failed with unknown Error")
            pass

    # def NextPipe(self):
    #     self.pipeLineNumberLineEdit.setText(str(int(self.pipe_id) + 1))
    #     self.pip_info()

    # def prev_pipe(self):
    #     self.pipeLineNumberLineEdit.setText(str(int(self.pipe_id) - 1))
    #     self.pip_info()


    def ShowWeldToPipe(self):
        with connection.cursor() as cursor:
            runid = self.runid
            try:
                Fetch_pipe_detail = "select id,runid,analytic_id,lower_sensitivity,upper_sensitivity, length, start_index,end_index from pipes where runid = '%s'"
                # Execute query.
                cursor.execute(Fetch_pipe_detail, (int(runid)))
                self.myTableWidget1.setRowCount(0)
                allSQLRows = cursor.fetchall()
                if allSQLRows:
                    for row_number, row_data in enumerate(allSQLRows):
                        self.myTableWidget1.insertRow(row_number)
                        for column_num, data in enumerate(row_data):
                            self.myTableWidget1.setItem(row_number, column_num, QtWidgets.QTableWidgetItem(str(data)))
                    self.myTableWidget1.setEditTriggers(QAbstractItemView.NoEditTriggers)
                else:
                    config.warning_msg("No record found", "")
                pipe_id_list = []
                pipe_id_list.clear()
                for i in allSQLRows:
                    pipe_id_list.append(str(i[0]))
                print("pipe_id_list", pipe_id_list)
            except:
                # logger.log_warning("error in show weld to pipe")
                pass


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
        runid = self.runid
        with connection.cursor() as cursor:
            try:
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
                    config.warning_msg("No record found", "")
                weld_id_list = []
                weld_id_list.clear()
                for i in allSQLRows:
                    weld_id_list.append(str(i[0]))
                print("weld_id_list", weld_id_list)
                self.combo.addItems(weld_id_list)
                self.combo_orientation.addItems(weld_id_list)
                self.combo_box.addItems(weld_id_list)
                self.combo_graph.addItems(weld_id_list)
                self.combo_box1.addItems(weld_id_list)
                self.combo_tab9.addItems(weld_id_list)

            except:
                # logger.log_error("Fetch Weld Detail has some error")
                pass
    # def WeldToPipe(self):
    #     if Config.no_weld_indicator:
    #         self.weldtoPipe = WeldToPipe.Query(self.runid, 1)
    #     else:
    #         self.weldtoPipe = WeldToPipe.Query(self.runid, self.analytic_id)

    def DefectList(self):
        runid = self.runid
        with connection.cursor() as cursor:
            try:
                Fetch_weld_detail = "select id,runid,start_observation,end_observation,start_sensor,end_sensor,angle,length,breadth,depth,type from defect_sensor_hm where runid='%s'"
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
                    config.warning_msg("No record found", "")
            except:
                # logger.log_error("Fetch DefectList has some error")
                pass


    def CreateWeld(self):
        try:
            self.sensitivity, okPressed = QInputDialog.getText(self, "Get integer", "sensitivity")
            if okPressed:
                pass
                # self.sensitivifty = self.sensitivity
            self.weldupdate = weld_update.Query_flow(self.runid, self.sensitivity)
        except:
            # logger.log_error("sensitivity is not found")
            pass

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
            config.warning_msg("DB Connection failed", "")


    def Typeofdefect(self):
        try:
            runid = self.runid
            try:
                self.thickness_pipe, okPressed = QInputDialog.getText(self, "Get integer", "thickness_pipe")
                if okPressed:
                    pass
                    thickness_pipe = float(self.thickness_pipe)
                    if thickness_pipe < 10.0:
                        geometrical_parameter = 10
                    else:
                        geometrical_parameter = thickness_pipe
                    get_type_defect(geometrical_parameter, runid)

            except:
                # logger.log_error("thickness_pipe is not found")
                pass
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


    def endcounter_to_startcounter(self):
        try:
            self.calculate_distance=endcounter_to_startcounter_distance.CalDistance(self.runid)
        except:
            QMessageBox.about(self, 'Info', 'Please select the runid')


    def AddWeld(self):
        try:
            self.AddData=AddWeld.AddWeldDetail(self.runid)
        except:
            QMessageBox.about(self, 'Info', 'Please select the runid')

######################################all values changes as per runs #############################
    def Erf(self):
        length_of_defect_L = 24
        od_of_pipe_D = 323
        pipe_thickness_T = 6.35
        depth_of_defect_d = 2.8575
        specified_minimum_yield_strength_of_material_at_ambient_condition_SMYS = 2498.3
        flow_stress = 1.1 * specified_minimum_yield_strength_of_material_at_ambient_condition_SMYS
        print("Sflow", flow_stress)

        z_factor = (length_of_defect_L * length_of_defect_L) / (od_of_pipe_D * pipe_thickness_T)
        print("Z_factor", z_factor)

        x = 1 + 0.8 * z_factor
        Building_stress_magmification_factor_M = pow(x, 1 / 2)
        print("Building_stress_magmification_factor_M", Building_stress_magmification_factor_M)
        y = 1 - 2 / 3 * depth_of_defect_d / pipe_thickness_T
        z = 1 - 2 / 3 * depth_of_defect_d / pipe_thickness_T / Building_stress_magmification_factor_M
        k = y / z
        print(y)
        print(z)
        print(k)

        if z_factor <= 20:
            Estimated_failure_stress_level_SF = flow_stress * k
            print("estimated_failure_stress", Estimated_failure_stress_level_SF)
        else:
            Estimated_failure_stress_level_SF = flow_stress * (1 - depth_of_defect_d / pipe_thickness_T)
            print("estimated_failure_stress", Estimated_failure_stress_level_SF)
        estimate_failure_pressure = (2 * Estimated_failure_stress_level_SF * pipe_thickness_T) / od_of_pipe_D
        print("estimate_failure_pressure", estimate_failure_pressure)
        safety_factor_SF = 1.39
        safe_operating_pressure_of_corroded_area_Ps = estimate_failure_pressure / safety_factor_SF
        print("safe_operating_pressure_of_corroded_area_Ps", safe_operating_pressure_of_corroded_area_Ps)
        MAOP = 11
        ERF = MAOP / safe_operating_pressure_of_corroded_area_Ps
        print("Estimate Repair Factor", ERF)

    def update_defect1(self):
        print("hii")
        runid = self.runid
        with connection.cursor() as cursor:
            """
            oddo1
            """
            fetch_row="select runid,start_observation,end_observation,absolute_distance_oddo1,pipe_id,sensor_no,upstream_oddo1,pipe_length,defect_type,type,defect_classification,angle_hr_m,pipe_thickness,length_odd1,breadth,depth,latitude,latitude from defect_sensor_hm where runid='%s' and depth>'%s'  order by absolute_distance_oddo1"
            """
            oddo2
            """
            # fetch_row = "select runid,absolute_distance,pipe_id,sensor_no,upstream_oddo2,pipe_length,defect_type,type,defect_classification,angle_hr_m,pipe_thickness,length,breadth,depth,latitude,longitude from defect_sensor_hm where runid='%s' and depth>'%s'  order by absolute_distance"
            cursor.execute(fetch_row, (int(runid), 0))
            allSQLRows = cursor.fetchall()
            print(allSQLRows)
            for i in allSQLRows:
                #print(i[0])
                Query1="INSERT INTO finaldefect (runid,start_observation,end_observation,Absolute_distance,Pipe_number,Sensor_number,Distance_to_Upstream,Pipe_length,Feature_type,Feature_identification,Dimensions_classification,Orientation_clock,WT,Length,Width,Depth,Latitude,Longitude) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17])
                cursor.execute(Query1)
            connection.commit()
            connection.close()


    def Create_pipe(self):
        try:
            runid=self.runid
            #print(runid)
            with connection.cursor() as cursor:
                fetch_last_row = "select runid,start_index,end_index,type,analytic_id,sensitivity,length,start_oddo1,end_oddo1,start_oddo2,end_oddo2 from temp_welds where runid='%s' order by start_index"
                # Execute query.
                f_data = []
                cursor.execute(fetch_last_row, (int(runid)))
                allSQLRows = cursor.fetchall()
                for i, row in enumerate(allSQLRows):
                    temp = {"start_index": row[1], "end_index": row[2], "weld_number": i + 1,
                            "type": row[3], "analytic_id": row[4], "sensitivity": row[5], "length": row[6], "start_oddo1": row[7], "end_oddo1": row[8], "start_oddo2": row[9], "end_oddo2": row[10], "runid": runid}

                    f_data.append(temp)
                    insert_weld_to_db(temp)
                last_index = 0
                last_oddo = 0
                pipes = []
                config.print_with_time("Generating Pipe")
                last_weld = f_data[-1]
                #print(f_data)
                for row in f_data:
                    oddo = row["start_oddo1"] if row["start_oddo1"] > row["start_oddo2"] else row["start_oddo2"]
                    length = oddo - last_oddo
                    obj = {"start_index": last_index, "end_index": row["start_index"], "length": length,
                           "analytic_id": row["analytic_id"], "runid": runid}
                    #print("obj...",obj)
                    pipes.append(obj)
                    last_index = row["end_index"]
                    last_oddo = row["end_oddo1"] if row["end_oddo1"] > row["end_oddo2"] else row["end_oddo2"]
                    insert_pipe_to_db(obj)
                last_pipe = get_last_pipe(runid, last_weld, last_weld['analytic_id'])
                insert_pipe_to_db(last_pipe)
                config.print_with_time("Pipe Generation completed")
                config.print_with_time("process end at : ")

            return
        except:
            QMessageBox.about(self, 'Info', 'Please select the runid')


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GMFL 12"))

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

        self.actionCreate_Project.setText(_translate("MainWindow", "New Project"))
        self.actionCreate_Project.triggered.connect(self.create_project)

        self.distance.setText(_translate("MainWindow", "Distance"))
        self.distance.triggered.connect(self.endcounter_to_startcounter)

        ########################## Call the type of defect ########################
        self.actiontypeofdefect.setText(_translate("MainWindow", "Dimensions Classification"))
        self.actiontypeofdefect.triggered.connect(self.Typeofdefect)

        ##################### call the Add weld ###############
        self.addweld.setText(_translate("MainWindow", "Add Weld"))
        self.addweld.triggered.connect(self.AddWeld)

        ##################### Create Pipe ###############
        self.create_pipe.setText(_translate("MainWindow", "Pipe Create"))
        self.create_pipe.triggered.connect(self.Create_pipe)

        ################### Final Defect ###############
        self.Update_defect.setText(_translate("MainWindow", "Final Defect"))
        self.Update_defect.triggered.connect(self.update_defect1)

        self.erf.setText(_translate("MainWindow", "Erf Calculation"))
        self.erf.triggered.connect(self.Erf)


def insert_weld_to_db(temp):
    #print("weld_obj", temp)
    """
        This will insert weld object to mysql database
        :param weld_obj : Object with value of  runid,analytic_id,sensitivity,start_index,end_index,start_oddo1,end_oddo1,start_oddo2,end_oddo2,length and weld_number
    """
    try:
        query_weld_insert = "INSERT INTO welds (weld_number,runid,start_index,end_index,type,analytic_id,sensitivity,length,start_oddo1,end_oddo1,start_oddo2,end_oddo2) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # print(runid, analytic_id, Sensitivity, start_file, end_file, start_sno, end_sno)
        with connection.cursor() as cursor:
            cursor.execute(query_weld_insert, (temp["weld_number"], temp["runid"], temp["start_index"], temp["end_index"], temp["type"], temp["analytic_id"], temp["sensitivity"], temp["length"], temp["start_oddo1"], temp["end_oddo1"], temp["start_oddo2"], temp["end_oddo2"]))
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
        query = "INSERT INTO Pipes (runid,analytic_id,length,start_index,end_index) VALUE(%s,%s," \
                "%s,%s,%s) "
        with connection.cursor() as cursor:
            cursor.execute(query,
                           (pipe_obj["runid"], pipe_obj["analytic_id"], pipe_obj["length"], pipe_obj["start_index"],
                            pipe_obj["end_index"]))
            connection.commit()
        return
    except:
        print("Error While Inserting weld for runid ")


def get_last_pipe(runid, weld_obj, analytic_id):
    """
        This will return the last pipe object to insert into mysql db
        :param runid: Id of the Project
    """
    query = "SELECT index,oddo1,oddo2 FROM `" + config.table_name + "` order by index desc LIMIT 1 "
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
    #print("nums",nums)
    """"
       This will merge the continues indexes and return a list that will contain list of start_index and end_index
           :param arr : List of indexes to merge
       """
    # gaps_bw_two_value=3
    # sequences = np.split(nums, np.array(np.where(np.diff(nums) > gaps_bw_two_value)[0]) + 1)
    # l = []
    # for s in sequences:
    #     if len(s) > 1:
    #         l.append((np.min(s), np.max(s)))
    #     else:
    #         pass
    #         #l.append(s[0])
    # return l

    try:
        gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s + 1 < e]
        edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
        return list(zip(edges, edges))
    except:
        print("Error while Grouping Index Range for defect")


def index_of_occurrences(arr, value):
    #print(arr)
    for i, data in enumerate(arr):
        if i == 128:
            arr[i] = 0
        elif i == 129:
            arr[i] = 0
        elif i == 130:
            arr[i] = 0
        elif i == 131:
            arr[i] = 0
    #print(arr)
    return [i for i, x in enumerate(arr) if x != 0]


def dimension_classification(type_of_defect, runid, defect_id):
    print(type_of_defect, runid)
    query = f'UPDATE finaldefect SET  Dimensions_classification="{type_of_defect}" WHERE runid="{runid}" and id={defect_id}'
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
#this is repeated function -------------------------------------------------------------------------------------------------------------
# def get_adaptive_sigma_refinement(length_percent):
#     """
#     Get refined sigma multipliers based on 5-part length percentage classification:
#     1-10%, 10-20%, 20-30%, 30-40%, 40%+
#     """
#     if 1 <= length_percent < 10:
#         sigma_multiplier = 0.6      # Less aggressive for very small defects
#         refinement_factor = 1.2
#         classification = "Very Small (1-10%)"
#     elif 10 <= length_percent < 20:
#         sigma_multiplier = 0.5      # Slightly more sensitive for small defects
#         refinement_factor = 0.9
#         classification = "Small (10-20%)"
#     elif 20 <= length_percent < 30:
#         sigma_multiplier = 1.0      # Standard sensitivity
#         refinement_factor = 1.0
#         classification = "Medium (20-30%)"
#     elif 30 <= length_percent < 40:
#         sigma_multiplier = 1.1      # Slightly less sensitive
#         refinement_factor = 0.9
#         classification = "Large (30-40%)"
#     elif length_percent >= 40:
#         sigma_multiplier = 1.2      # Less sensitive for largest defects
#         refinement_factor = 0.8
#         classification = "Very Large (40%+)"
#     else:
#         sigma_multiplier = 0.85
#         refinement_factor = 1.15
#         classification = "Below 1%"
#     return sigma_multiplier, refinement_factor, classification

# def get_type_defect_1(geometrical_parameter,runid,length_defect,width_defect):
#     L_ratio_W = length_defect / width_defect
#     if width_defect > 3 * geometrical_parameter and length_defect > 3 * geometrical_parameter:
#         type_of_defect = 'GENERAL'
#         return type_of_defect
#     elif (6 * geometrical_parameter >= width_defect >= 1 * geometrical_parameter and 6 * geometrical_parameter >= length_defect >= 1 * geometrical_parameter) and (
#             0.5 < (L_ratio_W) < 2) and not (
#             width_defect >= 3 * geometrical_parameter and length_defect >= 3 * geometrical_parameter):
#         type_of_defect = 'PITTING'
#         return type_of_defect
#     elif (1 * geometrical_parameter <= width_defect < 3 * geometrical_parameter) and (L_ratio_W >= 2):
#         type_of_defect = 'AXIAL GROOVING'
#         return type_of_defect
#     elif L_ratio_W <= 0.5 and 3 * geometrical_parameter > length_defect >= 1 * geometrical_parameter:
#         type_of_defect = 'CIRCUMFERENTIAL GROOVING'
#         return type_of_defect
#     elif 0 < width_defect < 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
#         type_of_defect = 'PINHOLE'
#         return type_of_defect
#     elif 0 < width_defect < 1 * geometrical_parameter and length_defect >= 1 * geometrical_parameter:
#         type_of_defect = 'AXIAL SLOTTING'
#         return type_of_defect
#     elif width_defect >= 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
#         type_of_defect = 'CIRCUMFERENTIAL SLOTTING'
#         return type_of_defect
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_type_defect(geometrical_parameter, runid):
    print(geometrical_parameter, runid)
    with connection.cursor() as cursor:
        try:
            Fetch_defect_detail = "select Length, Width, id from finaldefect where runid='%s'"
            cursor.execute(Fetch_defect_detail, (int(runid)))
            allSQLRows = cursor.fetchall()
            print("dhhdhf", allSQLRows)
            for i in allSQLRows:
                length_defect = i[0]
                width_defect = i[1]
                defect_id = i[2]
                L_ratio_W = length_defect / width_defect
                if width_defect >= 3 * geometrical_parameter and length_defect >= 3 * geometrical_parameter:
                    type_of_defect = 'GENERAL'
                elif (
                        6 * geometrical_parameter > width_defect >= 1 * geometrical_parameter and 6 * geometrical_parameter > length_defect >= 1 * geometrical_parameter) and (
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
                dimension_classification(type_of_defect, runid, defect_id)
        except:
            # logger.log_error("type of defect is not permissiable value")
            pass

def extract_raw_defects(arr):
    #print(arr)
    list_of_raw_defect = []
    temp_list = []
    for i, row in enumerate(arr):
        #print(row)
        if len(row) > 0:
            temp_list.append(i)
        elif len(temp_list) > 0:
            list_of_raw_defect.append({"start": temp_list[0], "end": temp_list[-1]})
            temp_list = []

    if len(temp_list) > 0:
        list_of_raw_defect.append({"start": temp_list[0], "end": temp_list[-1]})
        temp_list = []
    return list_of_raw_defect


def calculate_defect(raw_defects, pipe_data, number_of_sensor=144):
    # TODO pass number of sensor
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
    index_list = ranges(sensor_index)
    #print(index_list)
    for row in index_list:
        defects.append(
            {"start_observation": start, "end_observation": end, "start_sensor": row[0], "end_sensor": row[1]})
    return defects
    #print("hii")


def defect_length_calculator(df_new_proximity, data, defects, oddo1, oddo2, roll, runid, column_means):
    finial_defect_list = []
    defect_angle = []
    for i, defect in enumerate(defects):
        start, end, start_sensor, end_sensor = defect["start_observation"], defect["end_observation"], defect["start_sensor"], defect["end_sensor"]
        """
        Calculate in 12 inch MFL Tool
        """
        if start_sensor == end_sensor:
            pass
        else:
            print("..................................................")
            print("start-end observation",start,end)
            print("start-end sensor", start_sensor, end_sensor)

            """
            Calculate Upstream of the defect
            """
            upstream_odd2 = oddo2[end]-oddo2[0]
            #print("upstream_odd2....", upstream_odd2)

            upstream_odd1 = oddo1[end]-oddo1[0]
            #print("upstream_odd1....", upstream_odd1)


            """
            Calculate length and absolute distance of the defect
            """

            length = oddo2[end] - oddo2[start]

            absolute_length = oddo2[start]
            #print("absolute_distance_oddo2....", absolute_length)

            length1 = oddo1[end]-oddo1[start]
            absolute_length_1 = oddo1[start]
            #print("absolute_length_oddo1....", absolute_length_1)

            """
            Calculate latitude and longitude 
            """
            long, lat = lat_long(absolute_length_1, runid)
            print("latitude", lat)
            print("longitude", long)

            """
            Calculate Pipe_Thickness 
            """
            # pipethickness = pipethick(config)

            pipethickness = config.pipe_thickness

            """
            Calculate breadth of the defect
            """

            # def breadth():
            #     start_sensor1 = start_sensor+1
            #     end_sensor1 = end_sensor+1
            #     if start_sensor1 > end_sensor1:
            #         bredth = 0
            #         return bredth
            #
            #     else:
            #         if start_sensor1 == end_sensor1:
            #             bredth = 0
            #             return bredth
            #         else:
            #             outer_diameter_1 = 324  ############## outer_diametere 324 for 12 inch GMFL
            #             thickness_1 = 7.1  ################# each pipe thickness can be change old thickness 7.1 ############
            #             inner_diameter_1 = outer_diameter_1 - 2 * (thickness_1)
            #             radius_1 = inner_diameter_1 / 2
            #
            #             theta_2 = 1.74 ############ sensor to sensor  angle = 1.96 #########
            #             c_1 = math.radians(theta_2)  ########### c in calculated in radians ########
            #             theta_3 = 5.63  ########## flapper to flapper angle =10.61 ########
            #             d_1 = math.radians(theta_3)  ########### d in calculated in radians #####
            #
            #             x1 = radius_1 * c_1
            #             y1 = radius_1 * d_1
            #             count = 0
            #             if start_sensor1 == end_sensor1:
            #                 bredth = 0
            #                 return bredth
            #             else:
            #                 for i in range(start_sensor1, end_sensor1):
            #                     if i % 16 == 0:
            #                         count = count + 1
            #                         k = (y1 - x1) * count
            #                     else:
            #                         pass
            #                 try:
            #                     l = (end_sensor1 - start_sensor1) * x1
            #                     bredth = k + l
            #                     return bredth
            #                 except:
            #                     k = 0
            #                     l = (end_sensor1 - start_sensor1) * x1
            #                     bredth = k + l
            #                     return bredth


            """
            Calculate depth of the defect
            """
            if (absolute_length > 0):
                max_value_list, data_observation, data1, a, b = defect_max(data, start, end, start_sensor, end_sensor)
                #print("data_observation",data_observation)
                print("max_value_list....", max_value_list)
                #print("data observation",data_observation[0])
                """
                First row get start observation to end observation
                """
                #initial_observation_1 = data_observation[0]
                # initial_observation = []
                # for b in initial_observation_1:
                #     initial_observation.append(abs(b))
                # print("initial_observation", initial_observation)
                initial_observation_1 = [0 if k1 < 0 else k1 for k1 in data_observation[0]]
                #
                #
                # kx = []
                # for i2 in range(0, 128):
                #     if i2 >= a and i2 <= b:
                #         kx.append(initial_observation_1[i2])
                #     else:
                #         kx.append(0)
                #print("initial_observation", kx)

                """
                Difference between max_value_list and initial_observation
                """
                zip_object = zip(max_value_list, initial_observation_1)
                difference_list = []
                for list1_i, list2_i in zip_object:
                    difference_list.append(list1_i - list2_i)

                difference_list_1 = [0 if k2 < 0 else k2 for k2 in difference_list]
                print("difference_list1", difference_list_1)
                """
                Get max_value_difference_value
                """

                max_value_difference_value = max(difference_list_1)
                if max_value_difference_value == 0:
                    max_value = max(max_value_list)
                    max_value_difference_index = max_value_list.index(max_value)
                    print("max_value", max_value)
                    print("max_value_index", max_value_difference_index)
                else:
                    """
                    Get index max_value_difference_value
                    """
                    max_value_difference_index = difference_list.index(max_value_difference_value)
                    print("max_value_index", max_value_difference_index)
                    """
                    Check max_value_list inside the index and get max_value
                    """
                    max_value = max_value_list[max_value_difference_index]
                    print("max_value", max_value)

                    result = []
                    for sub_list in data1:
                        try:
                            result.append(sub_list[max_value_difference_index])
                        except IndexError:
                            result.append(None)
                    print("result....", result)


                    q1, q3 = np.percentile(result, [25, 25])
                    print("q1 q3", q1, q3)
                    start_point = np.argmax(result > q1)
                    end_point = len(result) - np.argmax(result[::-1] > q3) - 1

                    index_left_center = start_point + start
                    index_right_center = end_point + start
                    oddo_updated_left = oddo1[index_left_center]
                    oddo_updated_right = oddo1[index_right_center]

                    print("start_point", start_point)
                    print("end_point", end_point)
                    print("index_left_center", index_left_center)
                    print("index_right_center", index_right_center)
                    print("oddo_updated_left", oddo_updated_left)
                    print("oddo_updated_right", oddo_updated_right)

                    length = oddo_updated_right - oddo_updated_left
                    print("length_latest", length)

                    left_value = result[start_point]
                    right_value = result[end_point]
                    new_value = min(left_value, right_value)

                    def width_new():
                        first_sensor = None
                        last_sensor = None
                        for index in range(start_sensor, end_sensor + 1):
                            if new_value < max_value_list[index]:
                                first_sensor = index if first_sensor is None else first_sensor
                                last_sensor = index

                        print("left_value", left_value)
                        print("right_value", right_value)
                        print("new_value", new_value)
                        print("first_sensor", first_sensor)
                        print("last_sensor", last_sensor)

                        outer_diameter_1 = 324  ############## outer_diametere 324 for 12 inch GMFL
                        thickness_1 = config.pipe_thickness  ################# each pipe thickness can be change old thickness 7.1 ############
                        inner_diameter_1 = outer_diameter_1 - 2 * (thickness_1)
                        radius_1 = inner_diameter_1 / 2

                        theta_2 = 1.73 ############ sensor to sensor  angle = 1.73 #########
                        c_1 = math.radians(theta_2)  ########### c in calculated in radians ########
                        theta_3 = 4.52  ########## flapper to flapper angle = 4.52 ########
                        d_1 = math.radians(theta_3)  ########### d in calculated in radians #####

                        x1 = radius_1 * c_1
                        y1 = radius_1 * d_1
                        count = 0
                        if first_sensor == last_sensor:
                            breadth = 0
                            return breadth

                        else:
                            for i in range(first_sensor, last_sensor):
                                if i % 4 == 0:
                                    count = count + 1
                                    k = (y1 - x1) * count
                                else:
                                    pass
                            try:
                                l = (last_sensor - first_sensor) * x1
                                breadth = k + l
                                return breadth
                            except:
                                k = 0
                                l = (last_sensor - first_sensor) * x1
                                breadth = k + l
                                return breadth

                    """
                    Calculate new_depth of the defect

                    """
                    print("column_means", column_means)
                    base_value = column_means[max_value_difference_index]
                    try:
                        depth_val = (length / width_new()) * (max_value / base_value)

                        ############ For pipe thickness 7.5 #############
                        depth = round(((depth_val * 100) / config.pipe_thickness), 2)

                        ############ For pipe thickness 12.7 #############
                        # depth = round(((depth_val * 100)/12.7), 2)

                    except:
                        depth = float(0)

                    print("base_value", base_value)
                    print("depth", depth)

                    # def evaluate_polynomial(coefficients, x):
                    #     degree = len(coefficients) - 1
                    #     result_len = 0
                    #     for i in range(degree + 1):
                    #         result_len += coefficients[i] * (x ** (degree - i))
                    #     return int(result_len)

                    # ans_len = 0
                    # bredth = width_new()
                    # new_width = 0
                    # ans_depth = 0
                    #
                    ############# Coefficients of LENGTH for pipe thickness 7.4 ###############
                    # if int(length) <= 40 and int(length) >= 5:
                    #     coefficients = [4.72105390e-03, -3.47983873e-01, 8.09750603e+00, -2.56608581e+01]
                    #     # coefficients = [-1.11935387e-04, 1.13040083e-02, -4.15230050e-01, 6.81264193e+00, -4.67619456e+01, 1.18910052e+02]
                    #     ans_len =evaluate_polynomial(coefficients, int(length))
                    # elif int(length) > 40:
                    #     coefficients = [-2.28129067e-04, 4.01204794e-02, -1.31715742e+00, 3.78883022e+01]
                    #     # coefficients = [9.25350782e-10, 1.28969128e-07, 1.73778075e-05, 2.21800972e-03, 2.51147511e-01, 2.25391375e+01]
                    #     ans_len =evaluate_polynomial(coefficients, int(length))
                    # else:
                    #     ans_len = int(length)

                    ############# Coefficients of LENGTH for pipe thickness 12.7 ##############
                    # if int(length) <= 40 and int(length) >= 5:
                    #     coefficients = [4.72105390e-03, -3.47983873e-01, 8.09750603e+00, -2.56608581e+01]
                    #     # coefficients = [-1.11935387e-04, 1.13040083e-02, -4.15230050e-01, 6.81264193e+00, -4.67619456e+01, 1.18910052e+02]
                    #     ans_len =evaluate_polynomial(coefficients, int(length))
                    # elif int(length) > 40:
                    #     coefficients = [-2.28129067e-04, 4.01204794e-02, -1.31715742e+00, 3.78883022e+01]
                    #     # coefficients = [9.25350782e-10, 1.28969128e-07, 1.73778075e-05, 2.21800972e-03, 2.51147511e-01, 2.25391375e+01]
                    #     ans_len =evaluate_polynomial(coefficients, int(length))
                    # else:
                    #     ans_len = int(length)


                    ############# Coefficients of WIDTH for pipe thickness 7.4 ###############
                    # if int(bredth) <= 40 and int(bredth) >= 5:
                    #     coefficients = [4.72105390e-03, -3.47983873e-01, 8.09750603e+00, -2.56608581e+01]
                    #     # coefficients = [-1.11935387e-04, 1.13040083e-02, -4.15230050e-01, 6.81264193e+00, -4.67619456e+01, 1.18910052e+02]
                    #     new_width =evaluate_polynomial(coefficients, int(bredth))
                    # elif int(bredth) > 40:
                    #     coefficients = [-2.28129067e-04, 4.01204794e-02, -1.31715742e+00, 3.78883022e+01]
                    #     # coefficients = [9.25350782e-10, 1.28969128e-07, 1.73778075e-05, 2.21800972e-03, 2.51147511e-01, 2.25391375e+01]
                    #     new_width =evaluate_polynomial(coefficients, int(bredth))
                    # else:
                    #     new_width = int(bredth)

                    ############# Coefficients of WIDTH for pipe thickness 12.7 ##############
                    # if int(bredth) <= 40 and int(bredth) >= 5:
                    #     coefficients = [4.72105390e-03, -3.47983873e-01, 8.09750603e+00, -2.56608581e+01]
                    #     # coefficients = [-1.11935387e-04, 1.13040083e-02, -4.15230050e-01, 6.81264193e+00, -4.67619456e+01, 1.18910052e+02]
                    #     new_width =evaluate_polynomial(coefficients, int(bredth))
                    # elif int(length) > 40:
                    #     coefficients = [-2.28129067e-04, 4.01204794e-02, -1.31715742e+00, 3.78883022e+01]
                    #     # coefficients = [9.25350782e-10, 1.28969128e-07, 1.73778075e-05, 2.21800972e-03, 2.51147511e-01, 2.25391375e+01]
                    #     new_width =evaluate_polynomial(coefficients, int(bredth))
                    # else:
                    #     new_width = int(bredth)


                    ############# Coefficients of DEPTH for pipe thickness 7.4 ###############
                    # if int(depth) <= 40 and int(depth) >= 5:
                    #     coefficients = [4.72105390e-03, -3.47983873e-01, 8.09750603e+00, -2.56608581e+01]
                    #     # coefficients = [-1.11935387e-04, 1.13040083e-02, -4.15230050e-01, 6.81264193e+00, -4.67619456e+01, 1.18910052e+02]
                    #     ans_depth =evaluate_polynomial(coefficients, int(depth))
                    # elif int(depth) > 40:
                    #     coefficients = [-2.28129067e-04, 4.01204794e-02, -1.31715742e+00, 3.78883022e+01]
                    #     # coefficients = [9.25350782e-10, 1.28969128e-07, 1.73778075e-05, 2.21800972e-03, 2.51147511e-01, 2.25391375e+01]
                    #     ans_depth =evaluate_polynomial(coefficients, int(depth))
                    # else:
                    #     ans_depth = int(depth)

                    ############# Coefficients of DEPTH for pipe thickness 12.7 ##############
                    # if int(depth) <= 40 and int(depth) >= 5:
                    #     coefficients = [4.72105390e-03, -3.47983873e-01, 8.09750603e+00, -2.56608581e+01]
                    #     # coefficients = [-1.11935387e-04, 1.13040083e-02, -4.15230050e-01, 6.81264193e+00, -4.67619456e+01, 1.18910052e+02]
                    #     ans_depth =evaluate_polynomial(coefficients, int(depth))
                    # elif int(depth) > 40:
                    #     coefficients = [-2.28129067e-04, 4.01204794e-02, -1.31715742e+00, 3.78883022e+01]
                    #     # coefficients = [9.25350782e-10, 1.28969128e-07, 1.73778075e-05, 2.21800972e-03, 2.51147511e-01, 2.25391375e+01]
                    #     ans_depth =evaluate_polynomial(coefficients, int(depth))
                    # else:
                    #     ans_depth = int(depth)


                    # print("new length", ans_len)
                    # print("new width", new_width)
                    # print("new depth", ans_depth)


                each_holl_sensor = []
                for i in range(len(data1)):
                    """
                    Retrieving column data using sensor no or max_value_difference_index
                    """
                    each_holl_sensor.append(abs(data1[i][max_value_difference_index]))

                """
                Match index list
                """
                max_value_observation_index = []
                for j, match_data_value in enumerate(each_holl_sensor):
                    """
                    Retrieving index match the max_value and match_data_value
                    """
                    if match_data_value == max_value:
                        max_value_observation_index.append(j)
                    """
                    Index list get first index
                    """
                # print("max_value_observation_index",max_value_observation_index[0])
                depth_percentage_higher_value = max_value
                print("depth_percentage_higher_value", depth_percentage_higher_value)
                roll_position = roll[max_value_observation_index[0]]
                # print(depth_percentage_higher_value)
                print("roll position", roll_position)

                #################### sensor number ##########
                sensor_number = max_value_difference_index
                sensor_number = sensor_number + 1
                #print("start sensor: end sensor", a, b)
                #print("maxiumum depth of the sensor", sensor_number)

                """
                Internal and External defect calculation
                """
                mean_of_pipe_wise = df_new_proximity.mean()
                #print("mean_of_pipe_wise.......",mean_of_pipe_wise)
                average_value_list = mean_of_pipe_wise.values.tolist()
                average_value_list = [float(s) for s in average_value_list]
                #print("average_value_list", average_value_list)
                list_2d = df_new_proximity.values.tolist()
                index_1 = 0
                compare_list_mean = []
                while (index_1 < len(list_2d[0])):
                    x2 = []
                    for j, value in enumerate(list_2d):
                        if list_2d[j][index_1] <= average_value_list[index_1]:
                            x2.append(list_2d[j][index_1])
                    index_1 = index_1 + 1
                    #print("greater than aur equel average value",x2)
                    mean_value_of_compare_list = mean(x2)
                    compare_list_mean.append(mean_value_of_compare_list)
                print("compare_list_of_mean", compare_list_mean)

                """
                Noise difference each proximity sensor
                """
                zip_object_2 = zip(average_value_list, compare_list_mean)
                noise_difference_list = []
                for list1_4, list2_5 in zip_object_2:
                    noise_difference_list.append(list1_4 - list2_5)
                print("noise_difference list", noise_difference_list)

                if sensor_number % 4 == 0:
                    flapper_no = int(sensor_number/4)
                else:
                    flapper_no = int(sensor_number/4)+1
                proximity_no = flapper_no % 4
                if proximity_no == 0:
                    proximity_no = 4
                proximity_index = 'F'+str(flapper_no)+'P'+str(proximity_no)
                #print("proximity_index",proximity_index)
                b = df_new_proximity[start:end]
                #print("start_end_dataframe",b)
                proximity_one_column = b[proximity_index]
                c = proximity_one_column.values.tolist()
                # initial=c[0]
                # print("initial",initial)
                minimum_value_proximity = min(c)
                #print("minimum_value_proximity",minimum_value_proximity)

                single_proximity_average_value = compare_list_mean[int(flapper_no-1)]
                #print("single_proximity_average_value",single_proximity_average_value)

                if single_proximity_average_value > minimum_value_proximity:
                    type = "Internal"
                else:
                    type = "External"
                """
                End of Internal and External Defect
                """

                """
                Calculate orienatation hr:min:sec
                """
                sensor = sensor_number
                x = 1.59  ###### sensor to sensor angle between(x) 2.52 ex:1-2,2-3,3-4,5-6,6-7,7-8 ######
                y = 1.44  ######### flapper first sensor to flapper second first sensor ex:4-5,8-9,12-13,16-17 #####
                z = 2.71  ######## second flapper to 3 flapper angle ###########
                a = 9.08  ##### arm to arm angle ##############################
                b = int(sensor / 16)
                c = b * a
                d = int(sensor / 8)
                e = d - b
                f = e * z
                g = int(sensor / 4)
                h = g - (b + e)
                k = h * y
                l = sensor * x

                initial_calculation_of_each_sensor = (c + f + k + l)

                if roll_position > 0:
                    roll_position = roll_position + initial_calculation_of_each_sensor
                    if roll_position > 360:
                        roll_position = roll_position % 360
                else:
                    roll_position = 360 + roll_position
                    roll_position = roll_position + initial_calculation_of_each_sensor
                    if roll_position > 360:
                        roll_position = roll_position % 360
                    # angle = initial_calculation_of_each_sensor + roll_position
                    # print("angle rotation",angle)
                # print("angle", roll_position)
                h = roll_position / 30
                k = int(h)
                m = roll_position % 30
                minute = round(m)
                g = ':'
                angle_hr_min = str(k) + g + str(minute)
                # print(angle_hr_min)
                """
                End of Orientation
                """
                finial_defect_list.append({**defect, "start_index_q1": index_left_center, "end_index_q2": index_right_center,
                                           "angle": roll_position, "depth": depth, "defect_type": type,
                                           "length": length, "breadth": width_new(), "absolute_distance": absolute_length,
                                           "length_odd1": length1, "absolute_distance_oddo1": absolute_length_1,
                                           "sensor_no": sensor_number, "angle_hr_m": angle_hr_min, "defect_classification": "ex",
                                           "latitude": lat, "longitude": long, "pipe_thickness": pipethickness,
                                           "upstream_oddo1": upstream_odd1, "upstream_oddo2": upstream_odd2}) # TODO calculate breadth(same flapper or not)
    return finial_defect_list


def pipethick(config):
    tup1 = (
        "F1H1", "F1H2", "F1H3", "F1H4", "F2H1", "F2H2", "F2H3", "F2H4", "F3H1", "F3H2", "F3H3", "F3H4", "F4H1", "F4H2",
        "F4H3", "F4H4",
        "F5H1", "F5H2", "F5H3", "F5H4", "F6H1", "F6H2", "F6H3", "F6H4", "F7H1", "F7H2", "F7H3", "F7H4", "F8H1", "F8H2",
        "F8H3", "F8H4",
        "F9H1", "F9H2", "F9H3", "F9H4", "F10H1", "F10H2", "F10H3", "F10H4", "F11H1", "F11H2", "F11H3", "F11H4", "F12H1",
        "F12H2", "F12H3", "F12H4",
        "F13H1", "F13H2", "F13H3", "F13H4", "F14H1", "F14H2", "F14H3", "F14H4", "F15H1", "F15H2", "F15H3", "F15H4",
        "F16H1", "F16H2", "F16H3", "F16H4",
        "F17H1", "F17H2", "F17H3", "F17H4", "F18H1", "F18H2", "F18H3", "F18H4", "F19H1", "F19H2", "F19H3", "F19H4",
        "F20H1", "F20H2", "F20H3", "F20H4",
        "F21H1", "F21H2", "F21H3", "F21H4", "F22H1", "F22H2", "F22H3", "F22H4", "F23H1", "F23H2", "F23H3", "F23H4",
        "F24H1", "F24H2", "F24H3", "F24H4",
        "F25H1", "F25H2", "F25H3", "F25H4", "F26H1", "F26H2", "F26H3", "F26H4", "F27H1", "F27H2", "F27H3", "F27H4",
        "F28H1", "F28H2", "F28H3", "F28H4",
        "F29H1", "F29H2", "F29H3", "F29H4", "F30H1", "F30H2", "F30H3", "F30H4", "F31H1", "F31H2", "F31H3", "F31H4",
        "F32H1", "F32H2", "F32H3", "F32H4"
        "F33H1", "F33H2", "F33H3", "F33H4", "F34H1", "F34H2", "F34H3", "F34H4", "F35H1", "F35H2", "F35H3", "F35H4",
        "F36H1", "F36H2", "F36H3", "F36H4")

#########################choose ###############################################################
    f = json.loads(open('E:/MFL_desktop_web/mfl_10_inch_desktop/utils/pipe_60_base.json').read())
    # g = json.loads(open('C:/Users/admin/PycharmProjects/mfl_10_inch_desktop/utils/pipe_198_base.json').read())
    h = json.loads(open('E:/MFL_desktop_web/mfl_10_inch_desktop/utils/pipe_69_base.json').read())
    #print(f,h)
    thick_avg = []
    count = [0, 0]
    #print(f)
    #print(h)
    for i, data in enumerate(f):
        for j, data1 in enumerate(h):
            if i == j:
                a = (round(float(f[data])) + round(float(h[data1]))) / 2
                thick_avg.append(a)
                # print(1,j,data,data1)
                if a <= round(float(config[tup1[i]])):
                    count[0] = count[0] + 1
                else:
                    count[1] = count[1] + 1
                # print(count)
    #print(count)
    if count[0] > count[1]:
        return 6.35
    elif count[0] < count[1]:
        return 9.27
    else:
        return 0

def insert_defect_into_db(finial_defects, runid, pipe_id, lower_sensitivity, upper_sensitivity):
    # print("final_defects", finial_defects)
    with connection.cursor() as cursor:
        same_lw_up_check = cursor.execute('SELECT pipe_id,lower_sensitivity,upper_sensitivity from defect_sensor_hm where pipe_id="' + str(pipe_id) + '" and lower_sensitivity="' + str(lower_sensitivity) + '" and upper_sensitivity="' + str(upper_sensitivity) + '"')
        if same_lw_up_check:
            return 'HII'
    for i in finial_defects:
        start_observation = i['start_observation']
        end_observation = i['end_observation']
        start_index_q1 = i['start_index_q1']
        end_index_q2 = i['end_index_q2']
        start_sensor = i['start_sensor']
        end_sensor = i['end_sensor']
        sensor_no = i['sensor_no']
        angle = i['angle']
        angle_hr_min = i['angle_hr_m']
        length = round(i['length'])
        length_odd1 = round(i['length_odd1'])
        absolute_distance_odd1 = round(i['absolute_distance_oddo1'])
        depth = i['depth']
        defect_type = i['defect_type']
        defect_classification = i['defect_classification']
        breadth = round(i['breadth'])
        absolute_distance = round(i['absolute_distance'])
        pipe_thickness = i['pipe_thickness']
        type = 'system'
        latitude = i['latitude']
        longitude = i['longitude']
        upstream_oddo1 = round(i['upstream_oddo1'])
        upstream_oddo2 = round(i['upstream_oddo2'])
        with connection.cursor() as cursor:
            query_defect_insert = "INSERT into defect_sensor_hm (runid, pipe_id, start_observation, end_observation, start_index_q1, end_index_q2, start_sensor, end_sensor, sensor_no, angle, angle_hr_m, length, breadth, depth,defect_type, type, lower_sensitivity, upper_sensitivity, absolute_distance, defect_classification, length_odd1, absolute_distance_oddo1, latitude, longitude, pipe_thickness,upstream_oddo1,upstream_oddo2) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

            cursor.execute(query_defect_insert, (
                int(runid), pipe_id, start_observation, end_observation, start_index_q1, end_index_q2, start_sensor, end_sensor, sensor_no, angle, angle_hr_min, length,
                breadth, depth, defect_type, type, lower_sensitivity, upper_sensitivity, absolute_distance, defect_classification, length_odd1,
                absolute_distance_odd1, latitude, longitude, pipe_thickness, upstream_oddo1, upstream_oddo2))

            connection.commit()


def lat_long(absolute_length, runid):
    with connection.cursor() as cursor:
        query = """
        SELECT id, runid, pipe_id, start_index, absolute_distance_oddo1, Latitude, Longitude 
        FROM dgps_segment 
        WHERE runid=%s
        ORDER BY absolute_distance_oddo1
        """
        cursor.execute(query, (runid,))
        result = cursor.fetchall()

    if not result:
        print(f"No data found for runid: {runid}")
        return None, None  # Ensures no unpacking error

    # Convert database result into a dictionary
    data_dict = {
        'id': [],
        'runid': [],
        'pipe_id': [],
        'start_index': [],
        'absolute_distance_oddo1': [],
        'Latitude': [],
        'Longitude': []
    }

    for row in result:
        data_dict['id'].append(row[0])
        data_dict['runid'].append(row[1])
        data_dict['pipe_id'].append(row[2])
        data_dict['start_index'].append(row[3])
        data_dict['absolute_distance_oddo1'].append(row[4])
        data_dict['Latitude'].append(row[5])
        data_dict['Longitude'].append(row[6])

    # Now using the same logic with the dynamically fetched data
    absolute_distances = data_dict['absolute_distance_oddo1']

    for j, distance in enumerate(absolute_distances):
        if absolute_length < distance:
            return data_dict['Longitude'][j], data_dict['Latitude'][j]

        elif distance < absolute_length and absolute_distances[j + 1] > absolute_length:
            A = distance
            B = absolute_distances[j + 1]
            C = absolute_length
            m = C - A
            n = B - C

            x1 = ((m * data_dict['Longitude'][j + 1]) + (n * data_dict['Longitude'][j])) / (m + n)
            y1 = ((m * data_dict['Latitude'][j + 1]) + (n * data_dict['Latitude'][j])) / (m + n)

            return x1, y1

        elif absolute_length > absolute_distances[j + 1]:
            if j == len(absolute_distances) - 2:
                return data_dict['Longitude'][j + 1], data_dict['Latitude'][j + 1]

    return None, None  # If no match is found, return (None, None)


# def lat_long(absolute_length):
#     dict = {
#             'id': [1, 2, 3, 4],
#
#             'runid': [14, 14, 14, 14],
#
#             'pipe_id': [2, 2, 3, 4],
#
#             'start_index': [11042, 18329, 25577, 40088],
#
#             'absolute_distance_oddo1': [2.811999999999898, 2946.7119999999995, 5969.911, 12054.15],
#
#             'Latitude': [16.62374724, 16.62371681, 16.62368934, 16.62368959],
#
#             'Longitude': [82.35859973, 82.35861139, 82.35858726, 82.35858762]
#         }
#
#     b = dict['absolute_distance_oddo1']
#     for j, data in enumerate(b):
#         if absolute_length < data:
#             print("first:", dict['Latitude'][j])
#             print("first:", dict['Longitude'][j])
#             print("first1 oddo:", data)
#             return (dict['Longitude'][j],dict['Latitude'][j])
#             break
#         ################ lies between absolute distance #############
#         elif data < absolute_length and b[j + 1] > absolute_length:
#             print("first1:", dict['Latitude'][j])
#             print("first1:", dict['Longitude'][j])
#             print("first1 oddo:", data)
#             print("second1:", dict['Latitude'][j + 1])
#             print("second1:", dict['Longitude'][j + 1])
#             print("second1 oddo:", b[j + 1])
#             A = data
#             B = b[j + 1]
#             C = absolute_length
#             m = C - A
#             n = B - C
#             x1 = ((m * dict['Longitude'][j + 1]) + (n * dict['Longitude'][j])) / (m + n)
#             y1 = ((m * dict['Latitude'][j + 1]) + (n * dict['Latitude'][j])) / (m + n)
#             # print("F Longitude:", x1)
#             # print("F Latitude:", y1)
#             return (x1, y1)
#             break
#         elif absolute_length > b[j + 1]:
#             if j == len(b) - 2:
#                 print("first2:", dict['Latitude'][j + 1])
#                 print("first2:", dict['Longitude'][j + 1])
#                 print("first2 oddo:", b[j + 1])
#                 return (dict['Longitude'][j + 1],dict['Latitude'][j + 1])
#                 break


def internal_or_external(df_new_proximity, x):
    sensor_number = x+1
    if sensor_number % 4 == 0:
        flapper_no = int(sensor_number / 4)
    else:
        flapper_no = int(sensor_number / 4) + 1

    proximity_no = flapper_no % 4
    if proximity_no == 0:
        proximity_no = 4
    proximity_index = 'F' + str(flapper_no) + 'P' + str(proximity_no)
    print("Proximity_index",proximity_index)
    maximum_depth_proximity_sensor = df_new_proximity[proximity_index]

    c = maximum_depth_proximity_sensor.tolist()
    minimum_value_proximity = min(c)
    mean_value_proximtiy=mean(c)

    print("mean_value_proximtiy", mean_value_proximtiy)
    print("minimum value of proximity",minimum_value_proximity)

    difference_mean = mean_value_proximtiy - minimum_value_proximity

    print("difference_minimum2", difference_mean)
    if difference_mean < 5000:
        type = "Internal"
        return type
    else:
        type = "External"
        return type
    # mean_of_proximity = df_new_proximity.mean()
    # print("mean_of_defect", mean_of_proximity)
    # average_value_list = mean_of_proximity.values.tolist()
    # average_value_list = [float(s) for s in average_value_list]
    # # print("average_value_list", average_value_list)
    # list_2d = df_new_proximity.values.tolist()
    # index_1 = 0
    # compare_list_mean = []
    # while (index_1 < len(list_2d[0])):
    #     x2 = []
    #     for j, value in enumerate(list_2d):
    #         if list_2d[j][index_1] < average_value_list[index_1]:
    #             x2.append(list_2d[j][index_1])
    #     index_1 = index_1 + 1
    #     mean_value_of_compare_list = mean(x2)
    #     compare_list_mean.append(mean_value_of_compare_list)
    # print("compare_list_of_mean", compare_list_mean)
    # ############# noise_difference_each_proximity_sensore ###############
    # zip_object_2 = zip(average_value_list, compare_list_mean)
    # noise_difference_list = []
    # for list1_4, list2_5 in zip_object_2:
    #     noise_difference_list.append(list1_4 - list2_5)
    # print("noise_difference list", noise_difference_list)


def defect_angle_x(roll_x, sensor):
    roll_angle=list(roll_x)
    roll_position=roll_angle[0]
    print("roll_postion and sensor", roll_position, sensor)
    x = 1.73            ################# x 1.73 for 12 inch and 1.74  for 14 inch pipe #################
    y = 3.30            ################# y 3.30 for 12 inch and 3.37 for 14 inch pipe #################
    z = 4.52            ################# z 4.52 for 12 inch and 5.63 for 14 inch pipe #################
    a = 8.2             ################# a 8.2 for 12 inch and 6.5 for 14 inch pipe #################
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
    start_sensor1, end_sensor1 = start_sensor1+1, end_sensor1+1
    if start_sensor1 > end_sensor1 or start_sensor1 == end_sensor1:
        return 0

    outer_diameter_1 = config.outer_dia  # 12-inch pipe
    thickness_1 = config.pipe_thickness  # Replace with Config.pipe_thickness if using from config
    inner_diameter_1 = outer_diameter_1 - 2 * (thickness_1)
    radius_1 = inner_diameter_1 / 2

    theta_2 = config.width_angle1               # approximate value for both pipes
    c_1 = math.radians(theta_2)
    theta_3 = config.width_angle2               # approximate value for both pipes
    d_1 = math.radians(theta_3)
    theta_4 = config.width_angle3             # 9.97 for thickness 5.5 and 9.53 for thickness 7.1
    e_1 = math.radians(theta_4)  # Convert to radians
    # print("c1, d1", c_1, d_1)

    x1 = round(radius_1 * c_1, 1)
    y1 = round(radius_1 * d_1, 1)
    z1 = round(radius_1 * e_1, 1)  # Distance for sensors at multiples of 16
    print("x1, y1, z1", x1, y1, z1)

    bredth = 0
    i = start_sensor1
    while i < end_sensor1:
        # next_sensor = i + 1
        next_sensor = i
        if next_sensor % 16 == 0 and next_sensor != end_sensor1:
            bredth += z1
            # print(f"{i} → {next_sensor:<10} z1 (because {next_sensor} is a multiple of 16)")
        elif next_sensor % 4 == 0:  # If the next sensor is a multiple of 4 (but not 16)
            bredth += y1
            # print(f"{i} → {next_sensor:<10} (y1 - x1) (because {next_sensor} is a multiple of 4)")
        else:
            bredth += x1
            # print(f"{i} → {next_sensor:<10} x1")
        i += 1  # Move to the next sensor
    return bredth

    # if start_sensor1 > end_sensor1:
    #     bredth = 0
    #     return bredth
    #
    # else:
    #     if start_sensor1 == end_sensor1:
    #         bredth = 0
    #         return bredth
    #     else:
    #         outer_diameter_1 = 324                     ################# outer_diametere 324 for 12 inch and 355 for 14 inch pipe #################
    #         thickness_1 = Config.pipe_thickness        ################# each pipe thickness can be change old thickness 6.4 ############
    #         inner_diameter_1 = outer_diameter_1 - 2 * (thickness_1)
    #         radius_1 = inner_diameter_1 / 2
    #
    #         theta_2 = 1.73              ################# theta_2 1.73 for 12 inch and 1.74 for 14 inch pipe - (sensor to sensor) #################
    #         c_1 = math.radians(theta_2)  ########### c in calculated in radians ########
    #         theta_3 = 3.3              ################# theta_3 4.52 for 12 inch and 5.63 for 14 inch pipe - (flapper to flapper)  #################
    #         d_1 = math.radians(theta_3)  ########### d in calculated in radians #####
    #
    #         x1 = radius_1 * c_1  ###### sensor to sensor angle between(x) 1.58 ex:1-2,2-3,3-4,5-6,6-7,7-8 ######
    #         y1 = radius_1 * d_1
    #         # print("sensor to sensor length", x1)
    #         # print("falpper within sensor to next flapper sensor length", y1)
    #         count = 0
    #         if start_sensor1 == end_sensor1:
    #             bredth = 0
    #             return bredth
    #         else:
    #             for i in range(start_sensor1, end_sensor1):
    #                 if i % 4 == 0:
    #                     count = count + 1
    #                     k = (y1 - x1) * count
    #                 else:
    #                     pass
    #             try:
    #                 l = (end_sensor1 - start_sensor1) * x1
    #                 bredth = k + l
    #                 return bredth
    #             except:
    #                 k = 0
    #                 l = (end_sensor1 - start_sensor1) * x1
    #                 bredth = k + l
    #                 return bredth


def defect_max(data, start, end, a, b):
    data_observation = []
    max = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    data1 = data[start:end]
    # df=pd.DataFrame(data1)
    # df.to_csv('E:/MFL_10_Inch/mfl_10_inch_desktop/a.csv')
    for row in data1:
        data_observation.append(row)
        for y, data2 in enumerate(row):
            """
            Check data range b/w start_sensor=a and end_sensor=b
            """
            if y > a - 1 and y < b + 1:
                if data2 >= max[y]:
                    max[y] = data2
    return (max, data_observation, data1, a, b)

# def sensor_number(p,max_value):
#     print(p,max_value)
#     for t, dat in enumerate(p):
#         if p[t] == max_value:
#             sensor_number = t
#     return sensor_number

def get_defect_list_from_db(runid, pipe_id):
    # runid = self.runid
    # pipe_id = self.pipe_id
    defects = []
    with connection.cursor() as cursor:
        try:
            Fetch_weld_detail = "select * from defect_sensor_hm where runid='%s' and pipe_id='%s'"
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
            # logger.log_error("Error during fetching defects from db for runid = " + runid)
            return []

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    # app.exec_()



# if __name__ == "__main__":
#     print("✅ Entering main GUI loop...")
#     window = QtWidgets.QMainWindow()
#     window.setWindowTitle("GMFL 12-Inch Desktop")
#     window.resize(800, 600)
#     label = QLabel("GUI started successfully!", alignment=Qt.AlignCenter)
#     window.setCentralWidget(label)
#     window.show()
#
#     # Run the app loop
#     exit_code = app.exec_()
#     print("✅ Exited event loop, exit code =", exit_code)




