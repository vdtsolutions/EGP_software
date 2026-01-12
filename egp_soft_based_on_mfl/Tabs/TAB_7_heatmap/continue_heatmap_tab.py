import time

from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QTableWidget,
    QWidget, )
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import os
from pathlib import Path



from .widgets.helper_func import reset_btn_fun_chm, all_box_selection_ori_heatmap, export_to_excel, \
    open_context_menu_ori_tab9, handle_table_double_click_chm
from .widgets.heatmap_generator.tab9_heatmap import tab9_heatmap
from .widgets.next_prev_btn import tab9_heatmap_previous, tab9_heatmap_next
from ...Components.dig.runners.disgheet_abs_runner import DigsheetABSRunner

GMFL_ROOT = Path(__file__).resolve().parents[2]


def gmfl_path(relative):
    """Return absolute path inside GMFL backend_data/temp folder."""
    temp_dir = GMFL_ROOT / "backend_data" / "data_generated" / "temp"
    os.makedirs(temp_dir, exist_ok=True)  # make sure folder exists
    return str(temp_dir / relative)

class SimpleWorker(QtCore.QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @QtCore.pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)



class HeatmapProgressDialog(QtWidgets.QDialog):
    cancelled = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.WindowMinimizeButtonHint
            | QtCore.Qt.WindowTitleHint
        )

        self.setWindowTitle("Analyzing Pipe…")
        self.setModal(False)
        self.setFixedSize(300, 140)

        self.is_cancelling = False   # 🔥 NEW FLAG

        vbox = QtWidgets.QVBoxLayout(self)

        self.status_label = QtWidgets.QLabel("Starting…")
        self.progress = QtWidgets.QProgressBar()
        self.progress.setRange(0, 100)

        self.time_label = QtWidgets.QLabel("Time: 0s")

        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancelled.emit)

        vbox.addWidget(self.status_label)
        vbox.addWidget(self.progress)
        vbox.addWidget(self.time_label)
        vbox.addWidget(self.cancel_btn)

        self.start_time = time.time()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(500)

    def update_timer(self):
        if self.is_cancelling:
            return  # 🔥 freeze time
        elapsed = int(time.time() - self.start_time)
        self.time_label.setText(f"Time: {elapsed}s")

    def update_status(self, text):
        if self.is_cancelling:
            return  # 🔥 don't change "Cancelling…"
        self.status_label.setText(text)

    def update_progress(self, val):
        if self.is_cancelling:
            return  # 🔥 freeze progress bar
        self.progress.setValue(val)

    def show_cancelling(self):
        self.is_cancelling = True
        self.status_label.setText("Cancelling…")
        self.cancel_btn.setEnabled(False)
        self.timer.stop()  # 🔥 freeze time completely

        self.progress.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #555;
                    background: #d0d0d0;
                    height: 22px;
                    border-radius: 4px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #a6a6a6;   /* grey inactive */
                    width: 20px;
                    margin: 1px;
                }
            """)

    def finish(self):
        self.accept()



class HeatmapWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)
    status = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.tab = None

    @QtCore.pyqtSlot()
    def run(self):
        try:
            # Worker thread reads its own thread interruption state
            thread = QtCore.QThread.currentThread()

            html_path = self.tab.tab9_heatmap_threadsafe(
                self.status,
                self.progress,
                lambda: thread.isInterruptionRequested()  # 🔥 check interruption
            )

            self.finished.emit(html_path)

        except Exception as e:
            self.status.emit(f"Error: {e}")
            self.finished.emit("")



class ContinueHeatmapTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # keep pointer to parent MainWindow so we can call parent.runid etc.
        self.threadpool = QtCore.QThreadPool()

        self.parent = parent
        self.selected_defect_no = None
        self.selected_abs_distance = None
        self.digsheet_runner = DigsheetABSRunner(parent=self)
        self.selected_pipe_inch= self.parent.selected_inch
        PROFESSIONAL_BUTTON_STYLE = """
               QPushButton {
                   font-size: 13px;
                   font-family: 'Segoe UI', Arial;
                   font-weight: 600;
                   padding: 4px 14px;
                   color: white;
                   background-color: #618691;
                   border: 1px solid #050505;
                   border-radius: 0px;  /* rectangular */
               }
               QPushButton:hover {
                   background-color: #050505;
                   border-color: #102F9A;
               }
               QPushButton:pressed {
                   background-color: #153CC0;
                   border-color: #0C267B;
               }
               """
        # config_loader.set_config(self.parent.config)
        self.config = self.parent.config
        print(f"inside continue tab: {self.config.pipe_thickness}")
        # ---------- widget metadata ----------
        self.setObjectName("tab_7")
        self.setStyleSheet("background-color: #EDF6FF;")

        # ---------- main container layouts ----------
        self.hbox_con_hm = QHBoxLayout(self)
        self.vbox_con_hm = QVBoxLayout()

        # attach vbox into outer hbox just like before
        self.hbox_con_hm.addLayout(self.vbox_con_hm)

        # We'll build 3 horizontal rows inside vbox_con_hm,
        self.hbox_con_hm_1 = QHBoxLayout()  # top row: toolbar, combos, buttons
        self.hbox_con_hm_2 = QHBoxLayout()  # middle row: canvas + html view
        self.hbox_con_hm_3 = QHBoxLayout()  # bottom row: table

        # ---------- core widgets ----------

        # web output view
        self.m_output = QtWebEngineWidgets.QWebEngineView(self)

        # matplotlib figure/canvas/toolbar for tab9
        self.figure_tab9 = plt.figure(figsize=(20, 6))
        self.canvas_tab9 = FigureCanvas(self.figure_tab9)
        self.toolbar_tab9 = NavigationToolbar(self.canvas_tab9, self)

        # reset button
        self.reset_btn_tab9 = QPushButton("Reset")
        self.reset_btn_tab9.setStyleSheet(PROFESSIONAL_BUTTON_STYLE)
        self.reset_btn_tab9.clicked.connect(lambda: reset_btn_fun_chm(self))
        self.reset_btn_tab9.setVisible(True)  # initially hidden

        # defect selection button
        self.all_box_selection1 = QPushButton("Defect Selection")
        self.all_box_selection1.setStyleSheet(PROFESSIONAL_BUTTON_STYLE)
        self.all_box_selection1.clicked.connect(lambda: all_box_selection_ori_heatmap(self))
        self.all_box_selection1.setVisible(True)  # initially hidden

        # combo box for pipe/weld id, same name you used
        self.combo_tab9 = QComboBox()

        # analysis button
        self.Analaysis_btn_tab9 = QPushButton("Analysis")
        self.Analaysis_btn_tab9.setStyleSheet(PROFESSIONAL_BUTTON_STYLE)
        self.Analaysis_btn_tab9.clicked.connect(self.run_analysis_thread)

        # pagination / export buttons
        self.next_btn_hm = QPushButton("Next")
        self.next_btn_hm.setStyleSheet("background-color: white; color: black;")
        self.next_btn_hm.clicked.connect(lambda: tab9_heatmap_next(self))

        self.prev_btn_hm = QPushButton("Previous")
        self.prev_btn_hm.setStyleSheet("background-color: white; color: black;")
        self.prev_btn_hm.clicked.connect(lambda: tab9_heatmap_previous(self))

        self.digsheet_btn = QPushButton("Generate Dig")
        self.digsheet_btn.setStyleSheet(PROFESSIONAL_BUTTON_STYLE)
        self.digsheet_btn.setDisabled(True)
        self.digsheet_btn.clicked.connect(self.digsheet_abs_runner)


        self.export_btn_hm = QPushButton("Export Sheet")
        self.export_btn_hm.setStyleSheet("background-color: white; color: black;")
        self.export_btn_hm.clicked.connect(lambda: export_to_excel(self))

        # layout to hold prev / export / next horizontally with spacing
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_btn_hm)      # left
        button_layout.addStretch(1)
        button_layout.addWidget(self.export_btn_hm)    # middle
        button_layout.addStretch(1)
        button_layout.addWidget(self.next_btn_hm)      # right

        # wrap button_layout in a QWidget so we can add it to vbox_con_hm
        button_layout_widget = QWidget()
        button_layout_widget.setLayout(button_layout)

        # bottom table
        self.myTableWidget_tab9 = QTableWidget()
        self.myTableWidget_tab9.setGeometry(QtCore.QRect(30, 600, 1300, 235))
        self.myTableWidget_tab9.setRowCount(30)
        self.myTableWidget_tab9.setColumnCount(11)

        # set the same column widths as original
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

        # column headers
        self.myTableWidget_tab9.setHorizontalHeaderLabels([
            'Defect_id',
            'Pipe_id',
            'WT(mm)',
            'Absolute distance(m)',
            'Upstream(m)',
            'Feature type',
            'Dimensions classification',
            'Orientation clock(hr:min)',
            'Length(mm)',
            'Width(mm)',
            'Depth(%)'
        ])

        # make table read-only
        self.myTableWidget_tab9.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )

        # ---------- assemble rows ----------

        # Row 1 (controls row at top)
        # toolbar | combo | Analysis | Defect Selection | Reset
        self.hbox_con_hm_1.addWidget(self.toolbar_tab9)
        self.hbox_con_hm_1.addWidget(self.combo_tab9)
        self.hbox_con_hm_1.addWidget(self.Analaysis_btn_tab9)
        self.hbox_con_hm_1.addWidget(self.all_box_selection1)
        self.hbox_con_hm_1.addWidget(self.reset_btn_tab9)
        self.hbox_con_hm_1.addWidget(self.digsheet_btn)

        # Row 2 (middle view area)
        self.hbox_con_hm_2.addWidget(self.canvas_tab9)
        self.hbox_con_hm_2.addWidget(self.m_output)

        # Row 3 (bottom table)
        self.hbox_con_hm_3.addWidget(self.myTableWidget_tab9)

        # Now add rows to the main vertical layout.
        self.vbox_con_hm.addLayout(self.hbox_con_hm_1)
        self.vbox_con_hm.addLayout(self.hbox_con_hm_2)
        self.vbox_con_hm.addLayout(self.hbox_con_hm_3)

        # Then add the button row widget (prev/export/next) under everything
        self.vbox_con_hm.addWidget(button_layout_widget)

        # ---------- stretch / proportions ----------
        self.vbox_con_hm.setStretch(0, 10)   # hbox_con_hm_1
        self.vbox_con_hm.setStretch(1, 70)   # hbox_con_hm_2
        self.vbox_con_hm.setStretch(2, 20)   # hbox_con_hm_3

        # ---------- initial visibility ----------
        self.canvas_tab9.setVisible(False)
        self.m_output.setVisible(False)

        self.myTableWidget_tab9.clicked.connect(self.handle_row_click_tab9)
        self.myTableWidget_tab9.doubleClicked.connect(lambda: handle_table_double_click_chm(self))
        self.myTableWidget_tab9.customContextMenuRequested.connect(lambda: open_context_menu_ori_tab9(self))

    def digsheet_abs_runner(self):
        print(f"running digsheet usin button: defectNO--  {self.selected_defect_no} . abs_value : {self.selected_abs_distance}")
        print(f" pipetally path: {self.parent.pipetally}")
        # runner = DigsheetABSRunner()  # 👈 NO parent provided

        self.digsheet_runner.run(
            self.parent.pipetally,
            "240.456"
            # r"D:\Anubhav\pickle9"
        )

    def handle_row_click_tab9(self, index):
        row = index.row()
        defect_no_item = self.myTableWidget_tab9.item(row, 0)
        abs_dist_item = self.myTableWidget_tab9.item(row, 3)

        if defect_no_item and abs_dist_item:
            self.selected_defect_no = defect_no_item.text()
            self.selected_abs_distance = abs_dist_item.text()

            self.digsheet_btn.setEnabled(True)
            self.digsheet_btn.setStyleSheet("background:#00ff88;color:black;font-weight:bold;")

            print("🟢 DIG ENABLED →", self.selected_defect_no)
            print("🔍 CLICK SELECTED")
            print("   Defect No:", self.selected_defect_no)
            print("   Absolute Distance:", self.selected_abs_distance)

    @QtCore.pyqtSlot(str)
    def _slot_update_webview(self, html_path):
        self.update_webview(html_path)



    @QtCore.pyqtSlot(str)
    def _slot_worker_finished(self, html_path):

        if html_path == "__CANCELLED__":
            self.progress_dialog.finish()
            self.Analaysis_btn_tab9.setEnabled(True)
            print("🔥 Analysis cancelled by user.")
            self.show_cancelled_popup()
            return

        # ---- CASE 1: PKL MODE (fast) ----
        if html_path == "__USE_LOCAL_PKL__":
            self._run_pkl_mode_with_progress()
            self.Analaysis_btn_tab9.setEnabled(True)
            return

        # ---- CASE 2: Heavy work mode ----
        self.progress_dialog.finish()

        if html_path:
            self.update_webview(html_path)

        self.Analaysis_btn_tab9.setEnabled(True)

    def show_cancelled_popup(self):
        msg = QtWidgets.QMessageBox(self)

        # Title
        msg.setWindowTitle("Cancelled")

        # Text
        msg.setText("Process cancelled successfully.")

        # OK button only
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        # Remove minimize/maximize buttons
        msg.setWindowFlags(
            QtCore.Qt.Dialog |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint  # only close button
        )

        msg.exec_()

    def _run_pkl_mode_with_progress(self):
        """Shows smooth progress bar for PKL loading mode."""

        dlg = self.progress_dialog  # reuse the same dialog
        dlg.status_label.setText("Loading PKL data…")
        dlg.progress.setValue(0)
        dlg.show()

        start = time.time()
        target_duration = 1.0  # keep dialog visible min 1 sec

        # Smooth progress 0 → 90
        for i in range(0, 91, 5):
            dlg.update_progress(i)
            QtWidgets.QApplication.processEvents()
            QtCore.QThread.msleep(30)

        # Ensure at least 1 sec
        elapsed = time.time() - start
        remaining = target_duration - elapsed
        if remaining > 0:
            QtCore.QThread.msleep(int(remaining * 1000))

        # Finish
        dlg.update_status("Completed.")
        dlg.update_progress(100)
        QtWidgets.QApplication.processEvents()
        QtCore.QThread.msleep(150)

        dlg.finish()



        # NOW draw matplotlib plot normally
        tab9_heatmap(self, None, None, lambda: False)
        self._post_pkl_ui_updates()

    def _post_pkl_ui_updates(self):
        """Show PKL result on canvas + fill SQL table just like heavy mode."""

        # SHOW the matplotlib canvas
        self.canvas_tab9.setVisible(True)

        # HIDE the HTML webview
        self.m_output.setVisible(False)

        # Show important buttons
        self.reset_btn_tab9.setVisible(True)
        self.all_box_selection1.setVisible(True)

        # Enable Analysis button
        self.Analaysis_btn_tab9.setEnabled(True)

        # --- Fill SQL table ---
        with self.config.connection.cursor() as cursor:
            Fetch_weld_detail = """
                SELECT id,pipe_id, WT, Absolute_distance,Upstream,
                       feature_type,Orientation,
                       length,Width,depth
                FROM dent_clock_hm
                WHERE runid=%s AND pipe_id=%s
            """
            cursor.execute(Fetch_weld_detail, (self.runid, self.Weld_id_tab9))
            rows = cursor.fetchall()

            self.myTableWidget_tab9.setRowCount(0)

            for r, row_data in enumerate(rows):
                self.myTableWidget_tab9.insertRow(r)
                for c, value in enumerate(row_data):
                    self.myTableWidget_tab9.setItem(
                        r, c,
                        QtWidgets.QTableWidgetItem(str(value))
                    )

    # def run_analysis_thread(self):
    #     self.current_progress = 0
    #
    #     self.Analaysis_btn_tab9.setEnabled(False)
    #
    #     # Create progress dialog
    #     self.progress_dialog = HeatmapProgressDialog(self)
    #     self.progress_dialog.setModal(False)
    #     self.progress_dialog.show()
    #
    #     # Create worker + thread
    #     self.worker = HeatmapWorker()
    #     self.worker.tab = self  # give worker access to tab
    #     self.progress_dialog.cancelled.connect(self.worker.cancel)
    #
    #     self.thread = QtCore.QThread()
    #
    #     self.worker.moveToThread(self.thread)
    #
    #     # connect signals
    #     self.thread.started.connect(self.worker.run)
    #     self.worker.progress.connect(self.progress_dialog.update_progress)
    #     self.worker.status.connect(self.progress_dialog.update_status)
    #
    #     self.worker.finished.connect(self._slot_worker_finished)
    #     self.worker.finished.connect(self.thread.quit)
    #     self.worker.finished.connect(self.worker.deleteLater)
    #     self.thread.finished.connect(self.thread.deleteLater)
    #
    #     self.thread.start()

    def run_analysis_thread(self):
        self.current_progress = 0
        self.Analaysis_btn_tab9.setEnabled(False)

        # progress dialog
        self.progress_dialog = HeatmapProgressDialog(self)
        self.progress_dialog.setModal(False)
        self.progress_dialog.show()

        # worker + thread
        self.worker = HeatmapWorker()
        self.worker.tab = self

        self.thread = QtCore.QThread()
        self.worker.moveToThread(self.thread)

        # start
        self.thread.started.connect(self.worker.run)

        # connect worker -> GUI
        self.worker.progress.connect(self.progress_dialog.update_progress)
        self.worker.status.connect(self.progress_dialog.update_status)

        # finished handling
        self.worker.finished.connect(self._slot_worker_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # CANCEL: request interruption
        self.progress_dialog.cancelled.connect(lambda: self.thread.requestInterruption())

        self.progress_dialog.cancelled.connect(self._user_requested_cancel)

        self.thread.start()

    def _user_requested_cancel(self):
        # Tell worker thread to stop
        self.thread.requestInterruption()

        # Update dialog UI immediately
        self.progress_dialog.show_cancelling()

    def background_analysis(self):
        html_path = tab9_heatmap(self)
        print("🔥 FINAL RETURN:", html_path)

        QtCore.QMetaObject.invokeMethod(
            self,
            "_slot_update_webview",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, html_path)
        )

    def update_webview(self, html_path):
        print("Updating WebEngine safely on main thread:", html_path)

        # Load HTML
        self.m_output.load(QUrl.fromLocalFile(html_path))
        self.m_output.setVisible(True)

        # Hide canvas
        self.canvas_tab9.setVisible(False)

        # Show buttons
        self.reset_btn_tab9.setVisible(True)
        self.all_box_selection1.setVisible(True)

        # Enable button again
        self.Analaysis_btn_tab9.setEnabled(True)

        # 🟢 SQL TABLE FILLING BLOCK GOES HERE
        with self.config.connection.cursor() as cursor:
            Fetch_weld_detail = "select id,pipe_id,`WT(mm)`,absolute_distance,upstream,defect_type,dimension_classification,orientation,length,Width_final,depth_new from defect_clock_hm where runid='%s' and pipe_id='%s'"
            cursor.execute(Fetch_weld_detail, (self.runid, self.Weld_id_tab9))
            self.myTableWidget_tab9.setRowCount(0)
            allSQLRows = cursor.fetchall()

            if allSQLRows:
                for row_number, row_data in enumerate(allSQLRows):
                    self.myTableWidget_tab9.insertRow(row_number)
                    for column_num, data in enumerate(row_data):
                        self.myTableWidget_tab9.setItem(
                            row_number, column_num,
                            QtWidgets.QTableWidgetItem(str(data))
                        )



    def tab9_heatmap_threadsafe(self, status_callback, progress_callback, cancel_check):
        """
        Worker thread:
        - If PKL exists -> DO NOT run tab9_heatmap here
          return special marker so main thread will handle it.
        - If PKL missing -> run heavy backend part normally.
        """

        Weld_id = int(self.combo_tab9.currentText())
        pkl_path = (
                self.config.clock_pkl +
                self.parent.project_name + '/' +
                str(Weld_id) + '.pkl'
        )

        # 🔥 CASE 1: PKL already exists → GUI branch → MUST run on main thread
        if os.path.isfile(pkl_path):
            return "__USE_LOCAL_PKL__"

        # 🔥 CASE 2: No PKL → heavy backend → safe to run in worker thread
        status_callback.emit("Loading data…")
        progress_callback.emit(5)

        html_path = tab9_heatmap(self, status_callback, progress_callback, cancel_check)
        return html_path

    def smooth_progress(self, progress_callback, target):
        current = self.current_progress

        # Move 1% at a time for smooth animation
        step = 1 if target > current else -1

        for val in range(current, target, step):
            progress_callback.emit(val)
            QtCore.QThread.msleep(8)  # controls speed (8ms is smooth & fast)

        self.current_progress = target
        progress_callback.emit(target)







