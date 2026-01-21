import pymysql
from PyQt5.QtWidgets import QFrame, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QComboBox, QMessageBox
from PyQt5.QtCore import Qt

#localdb connection for mysql
# from circular_dent_maker.modular_maker.gcp import gcp_fetch_clock
# from circular_dent_maker.modular_maker.workers import FetchDataWorker
from egp_soft_based_on_mfl.Tabs.TAB_9_dent_analysis.modular_maker.workers import FetchDataWorker

host = 'localhost'
user='root'
password='byy184'
db_mysql='egp12inch'
folder_path = r"D:\Anubhav\data_egp\circular_dent_maker\modular_maker\data_clock"
folder_path1 = r"D:\Anubhav\data_egp\circular_dent_maker\modular_maker\data_pkl"

class VDTToolbar(QFrame):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window


        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db_mysql
        )
        self.selected_pipe_id = None

        self.setFixedHeight(38)
        self.setStyleSheet("""
            QFrame{
                background:#f3f3f3;
                border-bottom:1px solid #cfcfcf;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(6)

        def make_btn(text):
            b = QPushButton(text)
            b.setCursor(Qt.PointingHandCursor)
            b.setFixedHeight(26)
            b.setStyleSheet("""
                QPushButton{
                    background:#fafafa;
                    color:#222;
                    border:1px solid #bdbdbd;
                    font-size:11px;
                    padding:0 14px;
                }
                QPushButton:hover{background:#eaeaea;}
                QPushButton:pressed{background:#dcdcdc;}
            """)
            return b

        # --- First tool ---
        self.tool_btn = make_btn("Load Pipe Id")


        #dropdown
        self.mode_box = QComboBox()
        self.mode_box.setFixedHeight(26)
        self.mode_box.setEnabled(False)
        self.tool_btn.clicked.connect(self.build_pipe_id_index_mapping)
        self.mode_box.currentTextChanged.connect(self.pipe_selected)

        #create mesh button
        self.create_mesh_btn = make_btn("Analyse")
        self.create_mesh_btn.setEnabled(False)

        self.reset_btn = make_btn("Reset")
        self.reset_btn.clicked.connect(self.main_window.circle.reset_points)
        #insert into layout
        layout.addWidget(self.tool_btn)
        layout.addWidget(self.mode_box)
        layout.addWidget(self.create_mesh_btn)
        layout.addWidget(self.reset_btn)

        self.create_mesh_btn.clicked.connect(self.fetch_data)

        # spacer for future tools
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

    # def load_tool_modes(self):
    #     self.mode_box.clear()
    #
    #     cursor = self.connection.cursor()
    #     cursor.execute("SELECT id FROM welds ORDER BY id")
    #     rows = cursor.fetchall()
    #
    #     values = [str(r[0]) for r in rows]
    #
    #     self.mode_box.addItems(values)
    #     self.mode_box.setEnabled(True)
    #     self.mode_box.showPopup()


        self.update()
    def build_pipe_id_index_mapping(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, start_index, end_index FROM welds ORDER BY id"
        )
        rows = cursor.fetchall()

        # Reset state
        self.pipe_id_index_map = {}
        self.mode_box.clear()
        self.selected_pipe_id = None
        self.create_mesh_btn.setEnabled(False)

        if len(rows) < 2:
            return

        # 🔹 ADD PLACEHOLDER
        self.mode_box.addItem("Select")  # index 0 (dummy)

        # Build mapping + populate dropdown (ids 2 → N)
        for i in range(1, len(rows)):
            prev_id, prev_start, _ = rows[i - 1]
            curr_id, _, curr_end = rows[i]

            self.pipe_id_index_map[curr_id] = {
                "start_index": prev_start,
                "end_index": curr_end
            }

            self.mode_box.addItem(str(curr_id))

        # Set placeholder as default
        self.mode_box.setCurrentIndex(0)
        self.mode_box.setEnabled(True)

    def pipe_selected(self, value):
        if value == "Select":
            self.selected_pipe_id = None
            self.create_mesh_btn.setEnabled(False)
            return

        pipe_id = int(value)
        self.selected_pipe_id = pipe_id

        self.indices = self.pipe_id_index_map[pipe_id]
        self.start_index = self.indices['start_index']
        self.end_index = self.indices['end_index']
        self.weld_id = pipe_id
        print(
            f"weld selected id={pipe_id}: "
            f"start_index={self.start_index}, "
            f"end_index={self.end_index}"
        )

        self.create_mesh_btn.setEnabled(True)


    # def fetch_data(self):
    #     if not self.selected_pipe_id:
    #         return
    #
    #     # 1️⃣ Generate PKLs if needed
    #     gcp_fetch_clock(
    #         self.start_index,
    #         self.end_index,
    #         self.weld_id
    #     )
    #
    #     # 2️⃣ RAW PKL → circle
    #     raw_pkl_path = os.path.join(folder_path1, f"{self.weld_id}.pkl")
    #     df = pd.read_pickle(raw_pkl_path)
    #     df.columns = df.columns.str.strip()   # 🔥 REQUIRED
    #
    #     self.main_window.raw_df = df
    #     self.main_window.data_df = df
    #
    #     # 3️⃣ CLOCK PKL → heatmap
    #     clock_pkl_path = os.path.join(folder_path, f"{self.weld_id}.pkl")
    #     self.main_window.selector.load_from_pkl(clock_pkl_path)
    #
    #     # 4️⃣ Force Qt layout refresh (matplotlib + stacked layout)
    #     self.main_window.selector.setMinimumHeight(400)
    #     self.main_window.selector.updateGeometry()
    #
    #     # 5️⃣ Show analysis UI
    #     self.main_window.show_analysis_views()

    def on_fetch_done(self, raw_df, clock_pkl_path):
        self.loader.close()

        self.main_window.raw_df = raw_df
        self.main_window.data_df = raw_df

        self.main_window.selector.load_from_pkl(clock_pkl_path)
        self.main_window.show_analysis_views()

        self.create_mesh_btn.setEnabled(True)

    def on_fetch_error(self, msg):
        self.loader.close()
        self.create_mesh_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", msg)

    def fetch_data(self):
        if not self.selected_pipe_id:
            return

        self.create_mesh_btn.setEnabled(False)

        self.loader = LoaderDialog(self)
        self.loader.show()

        self.worker = FetchDataWorker(
            start_index=self.start_index,
            end_index=self.end_index,
            weld_id=self.weld_id,
            raw_folder=folder_path1,
            clock_folder=folder_path
        )

        self.worker.progress.connect(self.loader.set_text)
        self.worker.finished.connect(self.on_fetch_done)
        self.worker.error.connect(self.on_fetch_error)

        self.worker.start()


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar


class LoaderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Processing")
        self.setModal(True)
        self.setFixedSize(300, 100)

        layout = QVBoxLayout(self)

        self.label = QLabel("Starting…")
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # infinite loader

        layout.addWidget(self.label)
        layout.addWidget(self.progress)

    def set_text(self, text):
        self.label.setText(text)
