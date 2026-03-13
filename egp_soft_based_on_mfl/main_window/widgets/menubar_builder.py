from PyQt5 import QtWidgets


from .menubar.file_menu.create_project import create_project
from .menubar.file_menu.distance import endcounter_to_startcounter
from .menubar.file_menu.exit import exit_app
from .menubar.file_menu.load_pipetally import load_pipetally
from .menubar.tool_menu.db_maintainence import databasetool
from .menubar.tool_menu.xyz_mapping import open_google_earth
from .menubar.view_menu.addweld import AddWeld
from .menubar.view_menu.createpipe import Create_pipe
from .menubar.view_menu.dimension_classification import Typeofdefect
from .menubar.view_menu.erf_calculation import Erf
from .menubar.view_menu.final_defect import update_defect1


def build_menubar(self, MainWindow):

    self.menubar = QtWidgets.QMenuBar(MainWindow)


    MainWindow.setMenuBar(self.menubar)

    # Menu titles
    self.menuFile = QtWidgets.QMenu("File", MainWindow)
    # self.menuEdit = QtWidgets.QMenu("Edit", MainWindow)
    self.menuView = QtWidgets.QMenu("View", MainWindow)
    self.menuSearch = QtWidgets.QMenu("Search", MainWindow)
    self.menuTools = QtWidgets.QMenu("Tools", MainWindow)
    self.menuhelp = QtWidgets.QMenu("Help", MainWindow)

    # Add menus to bar
    self.menubar.addMenu(self.menuFile)
    # self.menubar.addMenu(self.menuEdit)
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
    self.actionCreate_Project = QtWidgets.QAction("Create Project", MainWindow)
    self.actionLoadPipetally = QtWidgets.QAction("Load Pipetally", MainWindow)
    self.exitwindow = QtWidgets.QAction("Exit", MainWindow)
    self.addweld = QtWidgets.QAction("Add Weld", MainWindow)
    self.create_pipe = QtWidgets.QAction("Create Pipe", MainWindow)
    # self.actiontypeofdefect = QtWidgets.QAction("Dimensions Classification", MainWindow)
    # self.erf = QtWidgets.QAction("Erf Calculation", MainWindow)
    self.distance = QtWidgets.QAction("Distance", MainWindow)
    self.Update_defect = QtWidgets.QAction("Final Dent", MainWindow)
    self.databasetool = QtWidgets.QAction("DB Maintainance", MainWindow)
    self.xyzmapping =   QtWidgets.QAction("XYZ Mapping", MainWindow)

    self.menuFile.addAction(self.actionCreate_Project)
    self.menuFile.addAction(self.actionLoadPipetally)
    self.menuFile.addAction(self.exitwindow)
    self.menuView.addAction(self.addweld)
    self.menuView.addAction(self.create_pipe)
    self.menuView.addAction(self.distance)
    # self.menuView.addAction(self.actiontypeofdefect)
    # self.menuView.addAction(self.erf)
    self.menuView.addAction(self.Update_defect)
    self.menuTools.addAction(self.databasetool)
    self.menuTools.addAction(self.xyzmapping)

    # Connect actions (your original logic)
    self.actionCreate_Project.triggered.connect(lambda: create_project(self))
    self.actionLoadPipetally.triggered.connect(lambda: load_pipetally(self))
    self.exitwindow.triggered.connect(lambda: exit_app(self))

    self.addweld.triggered.connect(lambda: AddWeld(self))
    self.create_pipe.triggered.connect(lambda: Create_pipe(self))
    self.distance.triggered.connect(lambda: endcounter_to_startcounter(self))
    # self.actiontypeofdefect.triggered.connect(lambda: Typeofdefect(self))
    # self.erf.triggered.connect(lambda: Erf(self))
    self.Update_defect.triggered.connect(lambda: update_defect1(self))


    self.databasetool.triggered.connect(lambda : databasetool(self))
    self.xyzmapping.triggered.connect(lambda : open_google_earth(self))

    self.menubar.setVisible(False)






























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
