from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTimer



from egp_soft_based_on_mfl.Components.Configs import config_loader
from egp_soft_based_on_mfl.Components.Configs.config_loader import get_inch_config
from egp_soft_based_on_mfl.Tabs.TAB_1_update_form.tab_update import UpdateTab
from egp_soft_based_on_mfl.Tabs.TAB_2_weld_selection.tab_weld_selection import WeldSelectionTab
from egp_soft_based_on_mfl.Tabs.TAB_3_Data_table.tab_ShowData import TabShowData
from egp_soft_based_on_mfl.Tabs.TAB_4_Line_plot.tab_line1 import LinePlotTab
from egp_soft_based_on_mfl.Tabs.TAB_5_Line_plot_abs_vs_ori.tab_line_orientation import Tab5LineOrientation
from egp_soft_based_on_mfl.Tabs.TAB_6_Pipe_visualization.tab_visualize import VisualizeTab
from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.continue_heatmap_tab import ContinueHeatmapTab
import egp_soft_based_on_mfl.Components.style1 as Style



class ClickableTabBar(QtWidgets.QTabBar):
    clicked = QtCore.pyqtSignal(int)

    def mousePressEvent(self, event):
        index = self.tabAt(event.pos())
        self.clicked.emit(index)
        super().mousePressEvent(event)


def init_tab(self):
    self.right_tabWidget = QtWidgets.QTabWidget()
    DISABLED_TAB_STYLE = """
    QTabBar::tab:disabled {
        background: #e6e6e6;
        color: #999999;
        border-color: #dcdcdc;
    }
    """

    custom_bar = ClickableTabBar()
    self.right_tabWidget.setTabBar(custom_bar)
    custom_bar.clicked.connect(lambda index: handle_tab_click(self, index))

    self.right_tabWidget.setStyleSheet(Style.tab_bar_style + DISABLED_TAB_STYLE)



    # Load config
    self.config = get_inch_config(self.selected_inch)
    config_loader.set_config(self.config)

    # Create tabs
    self.tab_update = UpdateTab(self)
    self.tab_weld_selection = WeldSelectionTab(self)
    self.tab_showData = TabShowData(self)
    self.tab_line1 = LinePlotTab(self)
    self.tab_line_orientation = Tab5LineOrientation(self)
    self.tab_visualize = VisualizeTab(self)
    self.continue_heatmap_tab = ContinueHeatmapTab(self)

    self.Graph1 = None  # GraphTab will be created later
    self.pipetally_loaded = False

    # Add tabs
    self.right_tabWidget.addTab(self.tab_update, "Update")
    self.right_tabWidget.addTab(self.tab_weld_selection, "Weld Selection")
    self.right_tabWidget.addTab(self.tab_showData, "Data Table")
    self.right_tabWidget.addTab(self.tab_line1.tab_line1, "Counter vs Sensor")
    self.right_tabWidget.addTab(self.tab_line_orientation, "Absolute vs Orientation")
    self.right_tabWidget.addTab(self.tab_visualize, "Pipe Visualization")
    # self.right_tabWidget.addTab(self.continue_heatmap_tab, "Heatmap")
    self.heatmap_tab_index = self.right_tabWidget.addTab(
        self.continue_heatmap_tab,
        "Heatmap"
    )
    self.right_tabWidget.setTabEnabled(self.heatmap_tab_index, False)

    # Graph placeholder (disabled)
    self.graph_placeholder = QtWidgets.QWidget()
    graph_index = self.right_tabWidget.addTab(self.graph_placeholder, "Graph")
    self.right_tabWidget.setTabEnabled(graph_index, False)
    self.graph_tab_index = graph_index

    # Disable tabs 4–8 initially
    self.tabs_to_lock = [3, 4, 5]
    self.tabs_to_unlock = [3, 4, 5]
    for idx in self.tabs_to_lock:
        self.right_tabWidget.setTabEnabled(idx, False)

    # Flags
    self.weld_loaded = False
    self.pipe_loaded = False

    # Replace tab bar
    while self.tabbar_container.count():
        c = self.tabbar_container.takeAt(0)
        if c.widget():
            c.widget().deleteLater()

    self.tabbar_container.addWidget(self.right_tabWidget)

    # Replace main content
    while self.main_container.count():
        c = self.main_container.takeAt(0)
        if c.widget():
            c.widget().deleteLater()

    # Re-connect tab-change signal for Graph tab logic (it needed to be done as graphh app is sperate app)
    self.right_tabWidget.currentChanged.connect(
        lambda index: on_right_tab_changed(self, index)
    )

def handle_tab_click(self, index):
    if self.right_tabWidget.isTabEnabled(index):
        return

    tab_text = self.right_tabWidget.tabText(index)

    print("CLICKED TAB:", index, repr(tab_text))

    if tab_text in ["Graph", "Heatmap - Abs vs Orientation"]:
        handle_graph_tab_locked(self)
        return

    QtWidgets.QMessageBox.warning(
        self,
        "Tab Locked",
        "Please load Weld and Pipe tables in the Data Table tab first."
    )


def handle_graph_tab_locked(self):
    """
    Shows smart warnings depending on what is loaded
    for the Graph tab.
    """

    missing_pipetally = not self.pipetally_loaded
    missing_weld = not self.weld_loaded
    missing_pipe = not self.pipe_loaded

    # CASE 1 → NOTHING loaded
    if missing_pipetally and missing_weld and missing_pipe:
        QtWidgets.QMessageBox.warning(
            self,
            "Graph Locked",
            "Please load Pipetally from File in menubar AND Weld + Pipe tables from Data Table tab First."
        )
        return

    # CASE 2 → Pipetally loaded, but tables missing
    if not missing_pipetally and (missing_weld or missing_pipe):
        QtWidgets.QMessageBox.warning(
            self,
            "Graph Locked",
            "Please load Weld + Pipe tables in the Data Table tab first."
        )
        return

    # CASE 3 → Tables loaded, pipetally missing
    if missing_pipetally and (not missing_weld and not missing_pipe):
        QtWidgets.QMessageBox.warning(
            self,
            "Graph Locked",
            "Please load Pipetally from File menu first."
        )
        return

    # CASE 4 → Everything loaded (unlikely here because tab stays disabled)
    QtWidgets.QMessageBox.information(
        self,
        "Graph Info",
        "All data loaded, Graph tab will unlock automatically."
    )


def on_right_tab_changed(self, index):
    current_tab = self.right_tabWidget.widget(index)

    if current_tab is self.Graph1:
        print("📈 Graph tab activated → launching Graph_app...")
        QTimer.singleShot(0, lambda: self.Graph1.Graph_app())

