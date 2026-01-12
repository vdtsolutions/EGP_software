from egp_soft_based_on_mfl.main_window.widgets.menubar_builder import build_menubar
from PyQt5 import QtCore, QtWidgets, QtGui

def setupUi(self, MainWindow):
    """
    Main UI initializer for the application.

    - Creates the main window and applies the blurred VDT wallpaper.
    - Sets up two primary screens (Screen 1 = Landing Page, Screen 2 = Main Tabs)
      using a QStackedLayout for smooth switching.
    - Initializes all shared state variables (config, selected inch, project name).
    - Builds and attaches the menubar (hidden by default until a project is loaded).
    - Adds both screens into the stacked layout and sets Screen 1 as the starting view.
    """
    MainWindow.setObjectName("MainWindow")
    MainWindow.resize(1700, 900)
    MainWindow.showMaximized()

    self.config = None
    self.selected_inch = None
    self.project_name = ""
    self.pipetally = None

    # ---------- CENTRAL WIDGET WITH BACKGROUND ----------
    self.centralwidget = QtWidgets.QWidget(MainWindow)
    self.centralwidget.setObjectName("centralwidget")
    self.centralwidget.setStyleSheet("""
        QWidget#centralwidget {
            background-image: url('D:/Anubhav/vdt_backend/egp_soft_based_on_mfl/Components/icons/vdt_blur.png');
            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
        }
    """)
    MainWindow.setCentralWidget(self.centralwidget)

    # ---------- STACKED SCREENS ----------
    self.stack = QtWidgets.QStackedLayout()
    self.centralwidget.setLayout(self.stack)

    self.build_screen1()
    self.build_screen2()

    self.stack.addWidget(self.screen1)  # index 0
    self.stack.addWidget(self.screen2)  # index 1
    self.stack.setCurrentIndex(0)

    # ---------- MENUBAR ----------
    build_menubar(self, MainWindow)
    self.menubar.setVisible(False)

    QtCore.QMetaObject.connectSlotsByName(MainWindow)