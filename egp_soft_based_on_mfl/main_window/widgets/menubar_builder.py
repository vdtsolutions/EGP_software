from PyQt5 import QtCore, QtWidgets, QtGui
from .menubar.File_funcs import create_project, endcounter_to_startcounter
from .menubar.View_func import Typeofdefect, AddWeld, Create_pipe, update_defect1, Erf
from ...Tabs.TAB_8_graphs.Graph1 import GraphTab


def build_menubar(self, MainWindow):

    self.menubar = QtWidgets.QMenuBar(MainWindow)


    MainWindow.setMenuBar(self.menubar)

    # Menu titles
    self.menuFile = QtWidgets.QMenu("File", MainWindow)
    self.menuEdit = QtWidgets.QMenu("Edit", MainWindow)
    self.menuView = QtWidgets.QMenu("View", MainWindow)
    self.menuSearch = QtWidgets.QMenu("Search", MainWindow)
    self.menuTools = QtWidgets.QMenu("Tools", MainWindow)
    self.menuhelp = QtWidgets.QMenu("Help", MainWindow)

    # Add menus to bar
    self.menubar.addMenu(self.menuFile)
    self.menubar.addMenu(self.menuEdit)
    self.menubar.addMenu(self.menuView)
    self.menubar.addMenu(self.menuSearch)
    self.menubar.addMenu(self.menuTools)
    self.menubar.addMenu(self.menuhelp)

    # Menubar style
    self.menubar.setStyleSheet("""
            QMenuBar {
                background-color: #ffffff;
                color: #000000;          /* <-- text always black */
            }
            QMenuBar::item {
                background: transparent;
                color: #000000;
            }
            QMenuBar::item:selected {
                background: #E6E6E6;
                color: #000000;
            }
        """)

    # Actions
    self.actionCreate_Project = QtWidgets.QAction("New Project", MainWindow)
    self.distance = QtWidgets.QAction("Distance", MainWindow)
    self.actionLoadPipetally = QtWidgets.QAction("Load Pipetally", MainWindow)
    self.actiontypeofdefect = QtWidgets.QAction("Dimensions Classification", MainWindow)
    self.addweld = QtWidgets.QAction("Add Weld", MainWindow)
    self.create_pipe = QtWidgets.QAction("Create Pipe", MainWindow)
    self.Update_defect = QtWidgets.QAction("Final Defect", MainWindow)
    self.erf = QtWidgets.QAction("Erf Calculation", MainWindow)
    self.databasetool = QtWidgets.QAction("DB Maintainance", MainWindow)

    self.menuFile.addAction(self.actionCreate_Project)
    self.menuFile.addAction(self.distance)
    self.menuFile.addAction(self.actionLoadPipetally)
    self.menuView.addAction(self.actiontypeofdefect)
    self.menuView.addAction(self.addweld)
    self.menuView.addAction(self.create_pipe)
    self.menuView.addAction(self.Update_defect)
    self.menuTools.addAction(self.erf)
    self.menuTools.addAction(self.databasetool)

    # Connect actions (your original logic)
    self.actionCreate_Project.triggered.connect(lambda: create_project(self))
    self.distance.triggered.connect(lambda: endcounter_to_startcounter(self))
    self.actiontypeofdefect.triggered.connect(lambda: Typeofdefect(self))
    self.addweld.triggered.connect(lambda: AddWeld(self))
    self.create_pipe.triggered.connect(lambda: Create_pipe(self))
    self.Update_defect.triggered.connect(lambda: update_defect1(self))
    self.erf.triggered.connect(lambda: Erf(self))
    self.actionLoadPipetally.triggered.connect(lambda: load_pipetally(self))
    self.databasetool.triggered.connect(lambda : databasetool(self))

    self.menubar.setVisible(False)





def load_pipetally(self):
    from PyQt5.QtWidgets import QFileDialog

    file_path, _ = QFileDialog.getOpenFileName(
        self,
        "Select Pipetally File",
        "",
        "Excel Files (*.xlsx *.xls *.csv);;All Files (*)"
    )

    if not file_path:
        return

    self.pipetally = file_path
    print("Pipetally loaded:", self.pipetally)

    # Mark pipetally as loaded
    self.pipetally_loaded = True

    # -------------------------------------------------------
    # CREATE GRAPH TAB (ONLY ONCE)
    # -------------------------------------------------------
    if self.Graph1 is None:
        self.Graph1 = GraphTab(self)

        # Remove placeholder
        self.right_tabWidget.removeTab(self.graph_tab_index)

        # Insert actual GraphTab
        self.graph_tab_index = self.right_tabWidget.insertTab(
            self.graph_tab_index,
            self.Graph1,
            "Graph"
        )

        # Keep Graph tab locked initially
        self.right_tabWidget.setTabEnabled(self.graph_tab_index, False)

        print("GraphTab created and locked.")

        # -------------------------------------------------------------
        # 🔥 LATE POPULATE GRAPH TAB IF TABLES WERE ALREADY LOADED
        # -------------------------------------------------------------
        # Populate weld IDs if weld table was loaded before GraphTab creation
        if self.weld_loaded:
            try:
                weld_ids = [
                    self.tab_showData.myTableWidget.item(r, 0).text()
                    for r in range(self.tab_showData.myTableWidget.rowCount())
                ]
                self.Graph1.combo_graph.clear()
                self.Graph1.combo_graph.addItems(weld_ids)
                print("GraphTab welds populated (late-load).")
            except Exception as e:
                print("Populate graph weld failed:", e)

        # Populate pipe IDs if pipe table was loaded before GraphTab creation
        if self.pipe_loaded and hasattr(self.Graph1, "combo_pipe"):
            try:
                pipe_ids = [
                    self.tab_showData.myTableWidget1.item(r, 0).text()
                    for r in range(self.tab_showData.myTableWidget1.rowCount())
                ]
                self.Graph1.combo_pipe.clear()
                self.Graph1.combo_pipe.addItems(pipe_ids)
                print("GraphTab pipes populated (late-load).")
            except Exception as e:
                print("Populate graph pipe failed:", e)

    # -------------------------------------------------------
    # NOW APPLY UNLOCK RULES
    # -------------------------------------------------------
    try_enable_graph_tab(self)

def try_enable_graph_tab(self):
    if self.weld_loaded and self.pipe_loaded and self.pipetally_loaded:
        self.right_tabWidget.setTabEnabled(self.graph_tab_index, True)
        print(f" heatmap_index : {self.heatmap_tab_index}")
        self.right_tabWidget.setTabEnabled(self.heatmap_tab_index, True)
        print("Graph Tab ENABLED")
    else:
        print("Graph waiting… weld:", self.weld_loaded,
              "pipe:", self.pipe_loaded,
              "pipetally:", self.pipetally_loaded)




def databasetool(self):
    dlg = DBToolDialog(self)
    dlg.exec_()



from PyQt5 import QtWidgets, QtCore, QtGui
import pandas as pd
import numpy as np


class ModernStatusDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, title="Processing", message="Please wait...", mode="loading"):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
        self.setModal(True)
        self.setFixedSize(420, 240)

        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(45)
        shadow.setOffset(0, 12)
        shadow.setColor(QtGui.QColor(0, 0, 0, 180))
        self.setGraphicsEffect(shadow)

        self.setStyleSheet("""
            QDialog {
                background-color: #1F222A;
                border-radius: 20px;
            }
            QLabel { color: #DDE1EB; font: 11pt 'Segoe UI'; }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 20)
        layout.setSpacing(18)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        title_label = QtWidgets.QLabel(title)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font: 600 15pt 'Segoe UI'; color: white;")
        layout.addWidget(title_label)

        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.icon_label)

        self.msg = QtWidgets.QLabel(message)
        self.msg.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.msg)

        self.close_btn = QtWidgets.QPushButton("Close")
        self.close_btn.setFixedHeight(36)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #4C8DFF;
                color: white;
                border-radius: 10px;
                font: 11pt 'Segoe UI';
            }
            QPushButton:hover { background-color: #3A78E5; }
        """)
        self.close_btn.clicked.connect(self.accept)
        self.close_btn.hide()
        layout.addWidget(self.close_btn)

        if mode == "loading":
            self.start_loading_animation()
        elif mode == "success":
            self.show_success_animation()

    def start_loading_animation(self):
        movie = QtGui.QMovie(":/qt-project.org/styles/commonstyle/images/qt_spinner.mng")
        self.icon_label.setMovie(movie)
        movie.start()

    def show_success_animation(self):
        self.icon_label.setText("✔")
        self.icon_label.setStyleSheet("font: 48pt 'Segoe UI'; color: #4CAF50;")
        self.close_btn.show()

    def set_success(self, message="Completed"):
        self.msg.setText(message)
        self.show_success_animation()



class DBToolDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setModal(True)
        self.setFixedSize(500, 680)

        # ───── Light white + blue theme ─────
        self.setStyleSheet("""
            QDialog { background-color: #F4F6FA; }
            QLabel { font: 11pt 'Segoe UI'; color: #1B1F27; }

            QFrame#card {
                background-color: #FFFFFF;
                border-radius: 14px;
                border: 1px solid #D9DEE8;
            }

            QFrame#line {
                border-top: 1px solid #E5E8EF;
                margin-top: 12px;
                margin-bottom: 12px;
            }

            QLabel#sectionTitle {
                font: 600 12.5pt 'Segoe UI';
            }

            QLabel#muted {
                color: #59606D;
                font: 10pt 'Segoe UI';
            }

            QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #C9CEDA;
                border-radius: 8px;
                padding: 6px 10px;
                font: 10pt 'Segoe UI';
                min-height: 30px;
            }

            QPushButton {
                background-color: #3B7BFF;
                color: white;
                border-radius: 8px;
                padding: 6px 20px;
                font: 10pt 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #2F67D8;
            }

            QPushButton#secondary {
                background-color: #E7EAF1;
                color: #1B1F27;
                border-radius: 8px;
                padding: 6px 20px;
            }
            QPushButton#secondary:hover {
                background-color: #DDE2EB;
            }

            QFrame.infoCard {
                background-color: #F7F9FC;
                border-radius: 12px;
                border: 1px solid #E3E7EF;
            }
        """)

        main = QtWidgets.QVBoxLayout(self)
        main.setContentsMargins(1, 1, 1, 1)  # <--- FIX: Add soft spacing around card
        main.setSpacing(0)

        # Main card container
        card = QtWidgets.QFrame()
        card.setObjectName("card")
        card.setMinimumWidth(500)
        card.setStyleSheet("""
            QFrame#card {
                background-color: #FFFFFF;
                border-radius: 16px;
                border: 1px solid #D9DEE8;
            }
        """)

        # Card internal layout
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(26, 26, 26, 26)  # <--- FIX: More premium spacing
        layout.setSpacing(20)

        # ───── Title ─────
        title = QtWidgets.QLabel("Database Tools")
        title.setStyleSheet("font: 600 17pt 'Segoe UI';")
        layout.addWidget(title)

        # ───── Project + DB info cards (FIXED CLEAN UI) ─────
        info_row = QtWidgets.QHBoxLayout()
        info_row.setSpacing(16)

        # ====== PROJECT CARD ======
        project_frame = QtWidgets.QFrame()
        project_frame.setObjectName("infoCard")
        project_frame.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        project_frame.setMinimumHeight(130)  # <--- FIX 1: prevent collapsing
        project_frame.setMinimumWidth(200)

        p_layout = QtWidgets.QVBoxLayout(project_frame)
        p_layout.setContentsMargins(14, 12, 14, 12)  # <--- FIX 2: real padding
        p_layout.setSpacing(6)

        project_label = QtWidgets.QLabel("Project Details")
        project_label.setStyleSheet("font: 600 11pt 'Segoe UI'; color: #2F3A4A;")

        project_name, project_inch = self._get_project_details()

        p_layout.addWidget(project_label)
        p_layout.addWidget(self._muted_label(f"Name: {project_name}"))
        p_layout.addWidget(self._muted_label(f"Inch: {project_inch}"))
        p_layout.addStretch(1)  # <--- FIX 3

        info_row.addWidget(project_frame, stretch=1)

        # ====== DATABASE CARD ======
        db_frame = QtWidgets.QFrame()
        db_frame.setObjectName("infoCard")
        db_frame.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        db_frame.setMinimumHeight(130)
        db_frame.setMinimumWidth(200)

        d_layout = QtWidgets.QVBoxLayout(db_frame)
        d_layout.setContentsMargins(14, 12, 14, 12)
        d_layout.setSpacing(6)

        db_label = QtWidgets.QLabel("Database Details")
        db_label.setStyleSheet("font: 600 11pt 'Segoe UI'; color: #2F3A4A;")

        db_name = self._get_db_details()

        d_layout.addWidget(db_label)
        d_layout.addWidget(self._muted_label(f"Name: {db_name}"))
        # d_layout.addWidget(self._muted_label(f"Table: {table_name}"))
        # if host:
        #     d_layout.addWidget(self._muted_label(f"Host: {host}"))

        d_layout.addStretch(1)  # <--- FIX 4

        info_row.addWidget(db_frame, stretch=1)

        # layout.addLayout(info_row)
        info_row_wrapper = QtWidgets.QVBoxLayout()
        info_row_wrapper.addLayout(info_row)
        info_row_wrapper.addSpacing(25)  # <--- FIX: add gap below cards
        info_row_wrapper.addStretch(2)
        layout.addLayout(info_row_wrapper)
        # ───── Divider ─────
        line = QtWidgets.QFrame()
        line.setObjectName("line")
        layout.addWidget(line)

        # ───── Table Actions section ─────
        sec1 = QtWidgets.QLabel("Table Actions")
        sec1.setObjectName("sectionTitle")
        layout.addWidget(sec1)

        self.table_combo = QtWidgets.QComboBox()
        self.load_tables()
        layout.addWidget(self.table_combo)

        row1 = QtWidgets.QHBoxLayout()
        row1.addWidget(self._btn("Truncate Table", self.truncate_any_table))
        row1.addWidget(self._btn("Export CSV", self.export_any_table))
        layout.addLayout(row1)

        # ───── Divider ─────
        line2 = QtWidgets.QFrame()
        line2.setObjectName("line")
        layout.addWidget(line2)

        # ───── Temp Welds section ─────
        sec2 = QtWidgets.QLabel("Temp Welds Management")
        sec2.setObjectName("sectionTitle")
        layout.addWidget(sec2)

        status_row = QtWidgets.QHBoxLayout()
        self.temp_status_badge = QtWidgets.QLabel("")
        self.temp_status_badge.setAlignment(QtCore.Qt.AlignCenter)
        self.temp_status_badge.setFixedHeight(22)
        self.temp_status_badge.setMinimumWidth(70)

        self.temp_status_label = QtWidgets.QLabel("")
        self.temp_status_label.setObjectName("muted")

        status_row.addWidget(self.temp_status_badge)
        status_row.addSpacing(8)
        status_row.addWidget(self.temp_status_label)
        status_row.addStretch(1)
        layout.addLayout(status_row)

        self.temp_info = QtWidgets.QLabel("")
        self.temp_info.setObjectName("muted")
        layout.addWidget(self.temp_info)

        row2 = QtWidgets.QHBoxLayout()
        self.btn_temp_truncate = self._btn("Truncate temp_welds", self.truncate_temp_weld)
        self.btn_temp_import = self._btn("Import CSV", self.import_temp_weld_csv)
        row2.addWidget(self.btn_temp_truncate)
        row2.addWidget(self.btn_temp_import)
        layout.addLayout(row2)

        self.refresh_temp_weld_status()

        # ───── Close button ─────
        close_btn = QtWidgets.QPushButton("Close")
        close_btn.setObjectName("secondary")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=QtCore.Qt.AlignRight)

        main.addWidget(card, alignment=QtCore.Qt.AlignCenter)

    # ---------- helpers ----------

    def _muted_label(self, text):
        lbl = QtWidgets.QLabel(text)
        lbl.setObjectName("muted")
        lbl.setWordWrap(True)
        lbl.setMaximumWidth(220)

        # 🔥 IMPORTANT: FORCE QT TO RESIZE THE ROW
        lbl.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        lbl.setMinimumHeight(lbl.sizeHint().height())

        return lbl

    def _btn(self, text, func):
        btn = QtWidgets.QPushButton(text)
        btn.clicked.connect(func)
        return btn

    def _get_project_details(self):
        # Try various options safely
        name = None
        inch = None

        if hasattr(self.parent, "combo_project"):
            name = self.parent.combo_project.currentText() or None
        if hasattr(self.parent, "selected_project"):
            name = getattr(self.parent, "selected_project") or name

        if hasattr(self.parent, "selected_inch"):
            inch = getattr(self.parent, "selected_inch")
        elif hasattr(self.parent, "combo_inch"):
            inch = self.parent.combo_inch.currentText()

        if not name:
            name = "Not selected"
        if not inch:
            inch = "Not selected"
        return name, inch

    def _get_db_details(self):
        # cfg = getattr(self.parent, "config", None)
        # if cfg is None:
        #     return "Unknown", "Unknown", None

        # db_name = getattr(cfg, "project_id", None) or getattr(cfg, "database", "Unknown")
        # table_name = getattr(cfg, "table_name", "Unknown")
        # host = getattr(cfg, "mysql_host", None) or getattr(cfg, "host", None)
        db_name = self.parent.config.db_mysql

        return db_name

    # ---------- core actions ----------

    def load_tables(self):
        try:
            with self.parent.config.connection.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = [row[0] for row in cursor.fetchall()]
                self.table_combo.addItems(tables)
        except Exception as e:
            self.table_combo.addItem(f"Error: {e}")

    def truncate_any_table(self):
        table = self.table_combo.currentText()
        truncate_table_modern(self.parent, table)
        if table == "temp_welds":
            self.refresh_temp_weld_status()

    def export_any_table(self):
        table = self.table_combo.currentText()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export CSV", f"{table}.csv", "CSV Files (*.csv)"
        )
        if not path:
            return

        dlg = ModernStatusDialog(self, title="Exporting CSV", message=f"Exporting {table}...", mode="loading")
        dlg.show()
        QtWidgets.QApplication.processEvents()

        try:
            df = pd.read_sql(f"SELECT * FROM `{table}`", self.parent.config.connection)
            df.to_csv(path, index=False)
            dlg.set_success("CSV export complete!")
        except Exception as e:
            dlg.msg.setText(str(e))
            dlg.icon_label.setText("⚠")
            dlg.close_btn.show()

    def refresh_temp_weld_status(self):
        try:
            df = pd.read_sql("SELECT * FROM temp_welds", self.parent.config.connection)

            if df.empty:
                # Empty state
                self.temp_status_badge.setText("EMPTY")
                self.temp_status_badge.setStyleSheet(
                    "background-color: #9CA3AF; color: white; border-radius: 10px; padding: 2px 8px; font: 10pt 'Segoe UI';"
                )
                self.temp_status_label.setText("Temp weld table has no data.")
                self.temp_info.setText("Rows: 0\nRunIDs: None")
                self.btn_temp_import.setEnabled(True)
            else:
                runids = df["runid"].dropna().unique()
                self.temp_status_badge.setText("ACTIVE")
                self.temp_status_badge.setStyleSheet(
                    "background-color: #35C46A; color: white; border-radius: 10px; padding: 2px 8px; font: 10pt 'Segoe UI';"
                )
                self.temp_status_label.setText("Temp weld data is loaded.")
                self.temp_info.setText(
                    f"Rows: {len(df)}\nRunIDs: {', '.join(map(str, runids))}"
                )
                self.btn_temp_import.setEnabled(False)

        except Exception as e:
            self.temp_status_badge.setText("UNKNOWN")
            self.temp_status_badge.setStyleSheet(
                "background-color: #F9C74F; color: #1B1F27; border-radius: 10px; padding: 2px 8px; font: 10pt 'Segoe UI';"
            )
            self.temp_status_label.setText("Could not read temp_welds.")
            self.temp_info.setText(f"Error: {e}")
            self.btn_temp_import.setEnabled(False)

    def truncate_temp_weld(self):
        truncate_table_modern(self.parent, "temp_welds")
        self.refresh_temp_weld_status()

    def import_temp_weld_csv(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv)"
        )
        if not path:
            return

        dlg = ModernStatusDialog(self, title="Importing CSV", message="Processing file...", mode="loading")
        dlg.show()
        QtWidgets.QApplication.processEvents()

        try:
            # detect separator
            with open(path, "r") as f:
                first_line = f.readline()
            sep = ";" if ";" in first_line else ","

            df = pd.read_csv(path, sep=sep)

            mysql_cols = [
                'weld_number', 'runid', 'analytic_id', 'sensitivity', 'length',
                'start_index', 'end_index', 'start_oddo1', 'end_oddo1',
                'start_oddo2', 'end_oddo2', 'created_by', 'modified_by',
                'temp_weld_id', 'type'
            ]

            common = [c for c in df.columns if c in mysql_cols]
            if not common:
                dlg.msg.setText("CSV has no valid temp_welds columns.")
                dlg.icon_label.setText("⚠")
                dlg.close_btn.show()
                return

            df = df[common]
            df = df.replace({np.nan: None, "nan": None, "NaN": None, "": None, " ": None})
            df = df.where(pd.notnull(df), None)

            col_str = ", ".join(f"`{c}`" for c in common)
            placeholders = ", ".join(["%s"] * len(common))
            query = f"INSERT INTO temp_welds ({col_str}) VALUES ({placeholders})"

            data = df.values.tolist()

            with self.parent.config.connection.cursor() as cursor:
                cursor.executemany(query, data)
            self.parent.config.connection.commit()

            dlg.set_success("Import completed!")

        except Exception as e:
            dlg.msg.setText(str(e))
            dlg.icon_label.setText("⚠")
            dlg.close_btn.show()

        self.refresh_temp_weld_status()



def truncate_table_modern(self, table_name: str):
    if not table_name:
        return

    dlg = ModernStatusDialog(
        self,
        title="Truncating Table",
        message=f"Truncating '{table_name}'...",
        mode="loading"
    )
    dlg.show()
    QtWidgets.QApplication.processEvents()

    try:
        with self.config.connection.cursor() as cursor:
            cursor.execute(f"TRUNCATE TABLE `{table_name}`")
        self.config.connection.commit()
        dlg.set_success(f"'{table_name}' truncated successfully!")
    except Exception as e:
        dlg.msg.setText(str(e))
        dlg.icon_label.setText("⚠")
        dlg.icon_label.setStyleSheet("font: 42pt; color: #FF5555;")
        dlg.close_btn.show()



# class DBToolDialog(QtWidgets.QDialog):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
#         self.setWindowTitle("Database Tools")
#         self.setModal(True)
#         self.setFixedSize(520, 560)
#
#         self.setStyleSheet("""
#             QDialog { background-color: #1F222A; border-radius: 16px; }
#             QLabel { color: #DDE1EB; font: 11pt 'Segoe UI'; }
#             QComboBox {
#                 background-color: #272B35; color: #E5E7F0;
#                 padding: 6px; border-radius: 8px; border: 1px solid #3A3F4D;
#             }
#             QPushButton {
#                 background-color: #4C8DFF; color: white;
#                 padding: 8px 14px; border-radius: 10px; font: 10pt 'Segoe UI';
#             }
#             QPushButton:hover { background-color: #3C78E0; }
#         """)
#
#         layout = QtWidgets.QVBoxLayout(self)
#         layout.setContentsMargins(22, 22, 22, 22)
#         layout.setSpacing(20)
#
#         # ─────────────────────────────
#         title = QtWidgets.QLabel("Database Maintenance")
#         title.setStyleSheet("font: 600 15pt 'Segoe UI'; color: white;")
#         layout.addWidget(title)
#
#         # ─────────────────────────────
#         # TABLE DROPDOWN
#         self.table_combo = QtWidgets.QComboBox()
#         self.load_tables()
#         layout.addWidget(QtWidgets.QLabel("Select Table"))
#         layout.addWidget(self.table_combo)
#
#         # ─────────────────────────────
#         # BUTTON ROW (TRUNCATE + EXPORT)
#         row = QtWidgets.QHBoxLayout()
#         btn_truncate = QtWidgets.QPushButton("Truncate Table")
#         btn_export = QtWidgets.QPushButton("Export CSV")
#
#         btn_truncate.clicked.connect(self.truncate_any_table)
#         btn_export.clicked.connect(self.export_any_table)
#
#         row.addWidget(btn_truncate)
#         row.addWidget(btn_export)
#         layout.addLayout(row)
#
#         # ============================================
#         # ALWAYS SHOW TEMP_WELDS INFO
#         # ============================================
#         separator = QtWidgets.QFrame()
#         separator.setFrameShape(QtWidgets.QFrame.HLine)
#         separator.setStyleSheet("color: #333;")
#         layout.addWidget(separator)
#
#         self.temp_title = QtWidgets.QLabel("Temp Welds Status")
#         self.temp_title.setStyleSheet("font: 600 13pt 'Segoe UI'; color: white;")
#         layout.addWidget(self.temp_title)
#
#         self.temp_info = QtWidgets.QLabel("")
#         self.temp_info.setStyleSheet("font: 10.5pt 'Segoe UI'; color: #A0A4B0;")
#         layout.addWidget(self.temp_info)
#
#         # temp_weld buttons
#         self.btn_temp_truncate = QtWidgets.QPushButton("Truncate temp_welds")
#         self.btn_temp_import = QtWidgets.QPushButton("Import CSV to temp_welds")
#         self.btn_temp_import.setEnabled(False)
#
#         self.btn_temp_truncate.clicked.connect(self.truncate_temp_weld)
#         self.btn_temp_import.clicked.connect(self.import_temp_weld_csv)
#
#         layout.addWidget(self.btn_temp_truncate)
#         layout.addWidget(self.btn_temp_import)
#
#         # Load status at start
#         self.refresh_temp_weld_status()
#
#         # Close button
#         close_btn = QtWidgets.QPushButton("Close")
#         close_btn.clicked.connect(self.close)
#         layout.addWidget(close_btn)
#
#     # ─────────────────────────────────────────────
#     def load_tables(self):
#         try:
#             with self.parent.config.connection.cursor() as cursor:
#                 cursor.execute("SHOW TABLES")
#                 tables = [row[0] for row in cursor.fetchall()]
#                 self.table_combo.addItems(tables)
#         except Exception as e:
#             self.table_combo.addItem(f"ERROR: {e}")
#
#     # ─────────────────────────────────────────────
#     def truncate_any_table(self):
#         table = self.table_combo.currentText()
#         truncate_table_modern(self.parent, table)
#         if table == "temp_welds":
#             self.refresh_temp_weld_status()
#
#     # ─────────────────────────────────────────────
#     def export_any_table(self):
#         table = self.table_combo.currentText()
#
#         path, _ = QtWidgets.QFileDialog.getSaveFileName(
#             self, "Save CSV", f"{table}.csv", "CSV Files (*.csv)"
#         )
#         if not path:
#             return
#
#         dlg = ModernStatusDialog(self, title="Exporting CSV", message=f"Exporting {table}...", mode="loading")
#         dlg.show()
#         QtWidgets.QApplication.processEvents()
#
#         try:
#             import pandas as pd
#             q = f"SELECT * FROM `{table}`"
#             df = pd.read_sql(q, self.parent.config.connection)
#             df.to_csv(path, index=False)
#             dlg.set_success("CSV Exported Successfully!")
#         except Exception as e:
#             dlg.msg.setText(f"Error: {e}")
#             dlg.icon_label.setText("⚠")
#             dlg.close_btn.show()
#
#     # ─────────────────────────────────────────────
#     def refresh_temp_weld_status(self):
#         try:
#             import pandas as pd
#             df = pd.read_sql("SELECT * FROM temp_welds", self.parent.config.connection)
#
#             if df.empty:
#                 self.temp_info.setText("Rows: 0\nRunIDs: None")
#                 self.btn_temp_import.setEnabled(True)
#             else:
#                 runids = df["runid"].unique()
#                 self.temp_info.setText(
#                     f"Rows: {len(df)}\nRunIDs: {', '.join(map(str, runids))}"
#                 )
#                 self.btn_temp_import.setEnabled(False)
#         except Exception as e:
#             self.temp_info.setText(f"Error: {e}")
#
#     # ─────────────────────────────────────────────
#     def truncate_temp_weld(self):
#         truncate_table_modern(self.parent, "temp_welds")
#         self.refresh_temp_weld_status()
#
#     # ─────────────────────────────────────────────
#     def import_temp_weld_csv(self):
#         path, _ = QtWidgets.QFileDialog.getOpenFileName(
#             self, "Select CSV File", "", "CSV Files (*.csv)"
#         )
#         if not path:
#             return
#
#         dlg = ModernStatusDialog(
#             self, title="Importing CSV",
#             message="Importing into temp_welds...",
#             mode="loading"
#         )
#         dlg.show()
#         QtWidgets.QApplication.processEvents()
#
#         try:
#             import pandas as pd
#             import numpy as np
#
#             # Auto-detect separator
#             with open(path, 'r') as f:
#                 first_line = f.readline()
#             sep = ';' if ';' in first_line else ','
#
#             df = pd.read_csv(path, sep=sep)
#
#             # Allowed table columns (MySQL)
#             table_cols = [
#                 'weld_number', 'runid', 'analytic_id', 'sensitivity', 'length',
#                 'start_index', 'end_index', 'start_oddo1', 'end_oddo1',
#                 'start_oddo2', 'end_oddo2', 'created_by',
#                 'modified_by', 'temp_weld_id', 'type'
#             ]
#
#             # Keep only columns that match table
#             common_cols = [c for c in df.columns if c in table_cols]
#             if not common_cols:
#                 dlg.msg.setText("CSV has no valid temp_welds columns.")
#                 dlg.icon_label.setText("⚠")
#                 dlg.close_btn.show()
#                 return
#
#             df = df[common_cols]
#
#             # 🔥 MOST IMPORTANT PART: CLEAN ALL VALUES 🔥
#             df = df.replace({np.nan: None, "nan": None, "NaN": None, "": None, " ": None})
#
#             # Convert all numeric values safely
#             for col in df.columns:
#                 df[col] = df[col].apply(
#                     lambda x: None if (isinstance(x, str) and not x.strip().isdigit()) else x
#                 )
#
#             # Ensure Python None used, not numpy types
#             df = df.where(pd.notnull(df), None)
#
#             # Prepare insert
#             col_string = ", ".join(f"`{c}`" for c in common_cols)
#             placeholders = ", ".join(["%s"] * len(common_cols))
#             query = f"INSERT INTO temp_welds ({col_string}) VALUES ({placeholders})"
#
#             data = df.values.tolist()
#
#             with self.parent.config.connection.cursor() as cursor:
#                 cursor.executemany(query, data)
#
#             self.parent.config.connection.commit()
#
#             dlg.set_success("Import Completed Successfully!")
#
#         except Exception as e:
#             dlg.msg.setText(str(e))
#             dlg.icon_label.setText("⚠")
#             dlg.close_btn.show()
#
#         self.refresh_temp_weld_status()
