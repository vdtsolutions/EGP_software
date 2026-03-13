from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector

import egp_soft_based_on_mfl.Components.style1 as Style
from .widgets.helper_func import select_weld
from .widgets.weld_selection_loader_worker import WeldSelectionWorker
from .widgets.weld_selector import weld_selection
from ...utils.loaderdialog.loader_dialog import LoaderDialog


class WeldSelectionTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # keep reference to parent (MainWindow) so we can call its logic if needed
        self.parent = parent
        self.config = self.parent.config

        self.setObjectName("tab_2")
        self.setStyleSheet("background-color: #EDF6FF;")

        # ---------------------------
        # widgets
        # ---------------------------

        # matplotlib figure/canvas/toolbar
        self.figure_x15 = plt.figure(figsize=(25, 8))
        self.canvas_x15 = FigureCanvas(self.figure_x15)
        self.toolbar_x15 = NavigationToolbar(self.canvas_x15, self)

        # input fields
        # input fields
        self.start15 = QLineEdit()
        self.end15 = QLineEdit()

        self.start15.setFixedWidth(120)
        self.end15.setFixedWidth(120)

        self.start15.setPlaceholderText("Start Index")
        self.end15.setPlaceholderText("End Index")

        # button
        self.button_x15 = QPushButton('Weld Selection')
        self.button_x15.resize(50, 50)
        self.button_x15.setStyleSheet(Style.btn_type_primary)

        self.button_x15.setEnabled(False)

        # connect button -> original logic
        self.button_x15.clicked.connect(self.handle_weld_selection)
        self.start15.textChanged.connect(self.validate_inputs)
        self.end15.textChanged.connect(self.validate_inputs)

        # ---------------------------
        # layouts
        # ---------------------------

        # Top row: toolbar + start/end + button  (this was hbox_15)
        self.hbox_15 = QHBoxLayout()
        self.hbox_15.addWidget(self.toolbar_x15)
        self.hbox_15.addStretch()  # push next widgets to right
        self.hbox_15.addWidget(self.start15)
        self.hbox_15.addWidget(self.end15)
        self.hbox_15.addWidget(self.button_x15)

        # Bottom row: canvas  (this was hbox_16)
        self.hbox_16 = QHBoxLayout()
        self.hbox_16.addWidget(self.canvas_x15)

        # Main vertical layout that stacks rows (this was vb15)
        self.vb15 = QVBoxLayout()
        self.vb15.addLayout(self.hbox_15)
        self.vb15.addLayout(self.hbox_16)

        # Tell Qt how to split space vertically:
        # row 0 (controls row) = small
        # row 1 (canvas row)   = expand
        self.vb15.setStretch(0, 0)
        self.vb15.setStretch(1, 1)

        # Set the main layout ONCE, on the tab widget itself.
        # This replaces hb15.addLayout(...)/setLayout(hbox_15) weirdness.
        self.setLayout(self.vb15)

        # optional: keep references to what you had for compatibility
        self.hb15 = QHBoxLayout()  # only if other code expects self.hb15 to exist
        # NOTE: we are not using self.hb15 as the widget's layout anymore.
        # Keeping it here only if you reference self.hb15 elsewhere.

    def refresh_view(self):
        """
        Force-repaint and force-relayout this tab after we mutate table/canvas
        in a callback that involved modal dialogs. This mimics 'switch tab away
        and come back' without actually switching tabs.
        """
        # 1. Ask Qt to recompute layout geometry
        if self.layout() is not None:
            self.layout().invalidate()
            self.layout().activate()

        # 2. Force Matplotlib canvas redraw if it exists
        if hasattr(self, "canvas") and self.canvas is not None:
            try:
                self.canvas.draw()
                self.canvas.update()
            except Exception as e:
                print("canvas refresh error:", e)

        if hasattr(self, "canvas_x15") and self.canvas_x15 is not None:
            try:
                self.canvas_x15.draw()
                self.canvas_x15.update()
            except Exception as e:
                print("canvas_x15 refresh error:", e)

        # 3. Force table to repaint if present
        if hasattr(self, "myTableWidget3") and self.myTableWidget3 is not None:
            self.myTableWidget3.viewport().update()
            self.myTableWidget3.update()

        # 4. Force this tab widget to repaint
        self.update()
        self.repaint()

        # 5. Force parent tabwidget (the QTabWidget in main window) to relayout this page
        if hasattr(self, "parent") and self.parent is not None:
            # parent could be Ui_MainWindow (QMainWindow-ish)
            # but we really want the tab widget that holds this tab
            if hasattr(self.parent, "tabWidget"):
                tw = self.parent.tabWidget
                # get currently active index and re-set it to itself
                idx = tw.currentIndex()
                tw.setCurrentIndex(idx)
                tw.update()
                tw.repaint()

            # also repaint parent directly
            self.parent.update()
            self.parent.repaint()

    def func(self, a):
        # print(a)
        query_for_start = 'SELECT * FROM ' + self.config.table_name + ' WHERE index>={} AND  index<={} order by index'
        query_job = self.config.client.query(query_for_start.format(a[0], a[1]))
        l1 = query_job.result().to_dataframe()
        return l1

    def validate_inputs(self):

        start_text = self.start15.text().strip()
        end_text = self.end15.text().strip()

        # Disable only if fields empty
        if not start_text or not end_text:
            self.button_x15.setEnabled(False)
            return

        # Disable if not integers
        if not start_text.isdigit() or not end_text.isdigit():
            self.button_x15.setEnabled(False)
            return

        # Both integers → enable button
        self.button_x15.setEnabled(True)

    def handle_weld_selection(self):

        start_val = int(self.start15.text())
        end_val = int(self.end15.text())

        if start_val >= end_val:
            QMessageBox.warning(
                self,
                "Invalid Range",
                "Start index must be smaller than End index."
            )
            return

        self.run_weld_selection()

    def run_weld_selection(self):

        self.loader = LoaderDialog(self, "Loading Weld Selection")

        self.worker = WeldSelectionWorker(self)

        # loader updates
        self.worker.progress.connect(self.loader.update_progress)
        self.worker.message.connect(self.loader.update_status)

        # worker → renderer
        self.worker.finished.connect(self.weld_selection_finished)

        self.loader.show()
        self.worker.start()

    def weld_selection_finished(self, df_plot_data1):

        if df_plot_data1 is None:
            self.loader.close()
            return

        self.loader.update_status("Rendering plot...")
        self.loader.update_progress(95)

        QtWidgets.QApplication.processEvents()

        index = df_plot_data1['index']

        self.figure_x15.clear()
        self.ax15 = self.figure_x15.add_subplot(111)

        self.ax15.clear()

        res = self.config.sensor_columns_hall_sensor

        self.a2 = []

        for i, data in enumerate(res):
            self.ax15.plot(index, (df_plot_data1[data] + i * 1400).to_numpy(), label=i)
            self.a2.append(df_plot_data1[data] + i * 1400)

        self.ax15.set_ylabel('Hall Sensor')

        self.canvas_x15.draw()

        self.rs2 = RectangleSelector(
            self.ax15,
            lambda eclick, erelease: select_weld(self, eclick, erelease),
            useblit=True
        )

        plt.connect('key_press_event', self.rs2)

        self.weld_selection_load_finished()

    def weld_selection_load_finished(self):

        self.loader.update_progress(100)
        self.loader.update_status("Completed")

        QtCore.QTimer.singleShot(300, self.loader.close)

