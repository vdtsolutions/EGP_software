import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QUrl
from .widgets.graph_app_gui import GraphApp


class GraphTab(QtWidgets.QWidget):
    """
    Child class for the 'Graph1' tab (tab_8).
    Handles its own layout and UI, but calls methods from the parent window.
    Parent must define: Magnetization(), Velocity(), Temperature_profile(),
    Sensor_loss(), Graph_app().
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.config = self.parent.config
        self.pipetally = self.parent.pipetally
        print(f" grapthtab pipetally (saved version0: {self.pipetally}")
        print(f"GraphTab pipetally (live): {self.parent.pipetally}")

        # ---------- CREATE TAB WIDGET ----------
        self.Graph1 = QtWidgets.QWidget()
        self.Graph1.setObjectName("tab_8")
        self.Graph1.setStyleSheet("background-color: #EDF6FF;")

        # ---------- MAIN LAYOUT ----------
        self.hb_graph = QtWidgets.QHBoxLayout(self.Graph1)
        self.vb_graph = QtWidgets.QVBoxLayout()
        self.hb_graph.addLayout(self.vb_graph, 75)

        # ---------- MATPLOTLIB FIGURE ----------
        self.figure_x_graph = plt.figure(figsize=(25, 8))
        self.canvas_x_graph = FigureCanvas(self.figure_x_graph)
        self.toolbar_x_graph = NavigationToolbar(self.canvas_x_graph, self.Graph1)

        # ---------- WEB VIEW ----------
        self.m_output_graph = QtWebEngineWidgets.QWebEngineView(self.Graph1)

        # ---------- COMBO BOX ----------
        self.combo_graph = QtWidgets.QComboBox()
        self.combo_graph.setObjectName("Pipe_id")
        self.combo_graph.setCurrentText("Pipe_id")

        # ---------- BUTTONS ----------
        # self.button_x5_mgraph = QtWidgets.QPushButton("Magnetization")
        # self.button_x5_mgraph.setFixedSize(100, 40)
        # self.button_x5_mgraph.clicked.connect(lambda: Magnetization(self))
        #
        # self.button_x5_vgraph = QtWidgets.QPushButton("Velocity")
        # self.button_x5_vgraph.setFixedSize(100, 40)
        # self.button_x5_vgraph.clicked.connect(lambda: Velocity(self))
        #
        # self.button_x5_tgraph = QtWidgets.QPushButton("Temperature")
        # self.button_x5_tgraph.setFixedSize(110, 40)
        # self.button_x5_tgraph.clicked.connect(lambda: Temperature_profile(self))
        #
        # self.button_x5_slgraph = QtWidgets.QPushButton("Sensor Loss")
        # self.button_x5_slgraph.setFixedSize(110, 40)
        # self.button_x5_slgraph.clicked.connect(lambda: Sensor_loss(self))
        #
        # self.button_x5_dfgraph = QtWidgets.QPushButton("Graph Records")
        # self.button_x5_dfgraph.setFixedSize(120, 40)
        # self.button_x5_dfgraph.clicked.connect(lambda: Graph_app(self))

        # ---------- SUB LAYOUTS ----------
        # self.hbox_5_graph = QtWidgets.QHBoxLayout()
        self.hbox_6_graph = QtWidgets.QHBoxLayout()
        # self.vb_graph.addLayout(self.hbox_5_graph, 20)
        self.vb_graph.addLayout(self.hbox_6_graph, 40)

        # ---------- TOP ROW CONTROLS ----------
        # self.hbox_5_graph.addWidget(self.toolbar_x_graph)
        # self.hbox_5_graph.addWidget(self.combo_graph)
        # self.hbox_5_graph.addWidget(self.button_x5_mgraph)
        # self.hbox_5_graph.addWidget(self.button_x5_vgraph)
        # self.hbox_5_graph.addWidget(self.button_x5_slgraph)
        # self.hbox_5_graph.addWidget(self.button_x5_tgraph)
        # self.hbox_5_graph.addWidget(self.button_x5_dfgraph)
        # self.button_x5_dfgraph.hide()

        # ---------- MAIN CONTENT ----------
        self.hbox_6_graph.addWidget(self.m_output_graph)

        # ---------- FINAL LAYOUT ----------
        self.setLayout(self.hb_graph)




    # ---------- Utility helpers ----------
    def load_html(self, html_path: str):
        """Display a local HTML file inside the webview."""
        self.m_output_graph.load(QUrl.fromLocalFile(html_path))

    def set_pipe_ids(self, items):
        """Populate the combo box with pipe IDs."""
        self.combo_graph.clear()
        self.combo_graph.addItems([str(x) for x in items])

    def get_selected_pipe_id(self):
        """Return the selected pipe id."""
        return self.combo_graph.currentText()

    def get_figure(self):
        """Return the matplotlib figure."""
        return self.figure_x_graph

    def get_canvas(self):
        """Return the matplotlib canvas."""
        return self.canvas_x_graph

    def Graph_app(self):
        print("Loading GraphApp...")

        try:
            while self.hbox_6_graph.count():
                child = self.hbox_6_graph.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            self.graph_app_widget = GraphApp(self)

            # 🔥 AUTO-LOAD PIPETALLY HERE
            self.graph_app_widget.load_file()

            self.hbox_6_graph.addWidget(self.graph_app_widget)
            print("GraphApp loaded successfully.")

        except Exception as e:
            print("Error loading GraphApp:", e)

