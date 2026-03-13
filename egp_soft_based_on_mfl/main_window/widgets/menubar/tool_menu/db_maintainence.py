from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
import pandas as pd


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




def databasetool(self):
    dlg = DBToolDialog(self)
    dlg.exec_()