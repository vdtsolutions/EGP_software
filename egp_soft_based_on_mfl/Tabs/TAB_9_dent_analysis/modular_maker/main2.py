# main.py
import sys
import pandas as pd
import pymysql

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QFrame, QSplitter,
    QLabel, QStackedLayout
)

from egp_soft_based_on_mfl.Tabs.TAB_9_dent_analysis.modular_maker.circular_view import CircleWidget
from egp_soft_based_on_mfl.Tabs.TAB_9_dent_analysis.modular_maker.data_table import DataTable
from egp_soft_based_on_mfl.Tabs.TAB_9_dent_analysis.modular_maker.heatmap_widget import HeatmapWidget
# from egp_soft_based_on_mfl.main_window.modular_maker.main import DEPTH_MOVED
from egp_soft_based_on_mfl.Tabs.TAB_9_dent_analysis.modular_maker.toolbar import VDTToolbar

USE_HEATMAP = True   # toggle later if needed

# START_INDEX = 25000
# END_INDEX = 26000

Depth_col = "Depth"

ALL_HALLS = [
    "F1H1","F1H2","F1H3","F1H4",
    "F2H1","F2H2","F2H3","F2H4",
    "F3H1","F3H2","F3H3","F3H4",
    "F4H1","F4H2","F4H3","F4H4",
    "F5H1","F5H2","F5H3","F5H4",
    "F6H1","F6H2","F6H3","F6H4",
    "F7H1","F7H2","F7H3","F7H4",
    "F8H1","F8H2","F8H3","F8H4",
    "F9H1","F9H2","F9H3","F9H4",
    "F10H1","F10H2","F10H3","F10H4",
    "F11H1","F11H2","F11H3","F11H4",
    "F12H1","F12H2","F12H3","F12H4"
]

WORKING_HALLS = [
    "F1H1","F1H2","F1H3","F1H4",
    "F2H1","F2H2","F2H3","F2H4",
    "F3H1","F3H2",
    "F5H1","F5H2","F5H3","F5H4",
    "F6H1","F6H2","F6H3","F6H4",
    "F7H1","F7H2",
    "F9H1","F9H2","F9H3","F9H4",
    "F10H1","F10H2","F10H3","F10H4",
    "F11H1","F11H2"
]

threshold = 100
host = 'localhost'
user='root'
password='byy184'
db_mysql='egp12inch'


def compute_depth_fast_debug(
    self,
    calib_lut,
    working_halls,
    reference_values,   # kept only for logging / sanity, not used in logic
    clicked_values,
    threshold=threshold
):
    depth_moved = {}

    print("\n================ FAST DEPTH DEBUG =================", flush=True)
    print(f"[DEBUG] Threshold = ±{threshold}", flush=True)
    print(f"[DEBUG] Working halls count = {len(working_halls)}", flush=True)

    for hall in working_halls:
        print("\n--------------------------------------------", flush=True)
        print(f"[DEBUG] HALL = {hall}", flush=True)

        # default
        depth = 0

        # ---------- SANITY CHECKS ----------
        if hall not in clicked_values:
            print("[DEBUG] ❌ Missing clicked value → depth=0", flush=True)
            depth_moved[hall] = 0
            continue

        if hall not in calib_lut:
            print("[DEBUG] ❌ Missing LUT for hall → depth=0", flush=True)
            depth_moved[hall] = 0
            continue

        clicked_val = int(clicked_values[hall])
        lut = calib_lut[hall]

        low = clicked_val - threshold
        high = clicked_val + threshold

        print(f"[DEBUG] Clicked value = {clicked_val}", flush=True)
        print(f"[DEBUG] Clicked-centred range = [{low}, {high}]", flush=True)
        print(f"[DEBUG] LUT keys count = {len(lut)}", flush=True)

        # ---------- FIND LUT VALUES INSIDE RANGE ----------
        candidates = []
        for key, d in lut.items():
            if low <= key <= high:
                candidates.append((key, d))

        if not candidates:
            print("[DEBUG] ❌ No calibration value inside range → depth=0", flush=True)
            depth_moved[hall] = 0
            print("[DEBUG] FINAL DEPTH = 0", flush=True)
            continue

        print(
            f"[DEBUG] ✅ Calibration values in range: "
            f"{[(k, abs(clicked_val - k)) for k, _ in candidates]}",
            flush=True
        )

        # ---------- PICK CLOSEST ----------
        closest_key, closest_depth = min(
            candidates,
            key=lambda x: abs(clicked_val - x[0])
        )

        diff = abs(clicked_val - closest_key)

        print(
            f"[DEBUG] ✅ Closest calibration key = {closest_key} "
            f"(diff={diff})",
            flush=True
        )
        print(
            f"[DEBUG] ✅ DEPTH SELECTED = {closest_depth}",
            flush=True
        )

        depth_moved[hall] = closest_depth
        print(f"[DEBUG] FINAL DEPTH = {closest_depth}", flush=True)

    # ---------- SUMMARY ----------
    print("\n================ FINAL DEPTH_MOVED =================", flush=True)

    halls = list(depth_moved.keys())
    depths = list(depth_moved.values())

    print("HALL : " + " | ".join(f"{h:>6}" for h in halls), flush=True)
    print("DEPTH: " + " | ".join(f"{d:>6}" for d in depths), flush=True)

    print("===================================================\n", flush=True)

    print(f"[SELECT] index from heatmap = {self.pipe_index}", flush=True)
    print(f"values of hall at index={self.pipe_index} is hall values = [{self.measured}]")

    return depth_moved





def make_placeholder(text):
    label = QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("""
        QLabel {
            color: #666;
            font-size: 16px;
            font-weight: 500;
        }
    """)
    return label


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Circular Dent Visualizer (Modular)")

        self.data_df = None
        self.raw_df = None
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db_mysql
        )
        query = "SELECT * FROM dent_calibration"

        self.calibrated_df = pd.read_sql(query, self.connection)

        # Keep behavior identical to Excel version
        self.calibrated_df.columns = self.calibrated_df.columns.str.strip()
        ref_row = self.calibrated_df.loc[
            self.calibrated_df["ID"] == "A"
            ].iloc[0]

        reference_values = {
            h: float(ref_row[h])
            for h in WORKING_HALLS
            if h in ref_row.index and not pd.isna(ref_row[h])
        }
        minute_step = 15

        visual_labels = self.build_visual_labels_from_all_halls(
            all_halls=ALL_HALLS,
            working_halls=WORKING_HALLS,
            minute_step=minute_step
        )

        # ---------------- CIRCLE VIEW ----------------
        self.circle = CircleWidget(
            ALL_HALLS,
            WORKING_HALLS,
            reference_values,
            {},
            visual_labels=visual_labels  # ✅ ADD THIS
        )

        self.circle_placeholder = make_placeholder(
            "Please select weld and click Analyse button"
        )

        import re

        print("\n================ CALIBRATION SANITY CHECK ================", flush=True)

        # 1️⃣ Working halls count
        print(f"[SANITY] WORKING_HALLS count = {len(WORKING_HALLS)}", flush=True)

        # 2️⃣ Detect hall-like columns in calibrated Excel (F<number>H<number>)
        hall_pattern = re.compile(r"^F\d+H\d+$")
        excel_hall_cols = [
            c for c in self.calibrated_df.columns
            if hall_pattern.match(c)
        ]

        print(f"[SANITY] Excel hall columns count = {len(excel_hall_cols)}", flush=True)

        # 3️⃣ Missing halls
        missing = sorted(set(WORKING_HALLS) - set(excel_hall_cols))
        extra = sorted(set(excel_hall_cols) - set(WORKING_HALLS))

        print(f"[SANITY] Missing halls in Excel = {missing}", flush=True)
        print(f"[SANITY] Extra halls in Excel = {extra}", flush=True)

        print("========================================================\n", flush=True)

        # ---------------- BUILD CALIBRATION LUT ----------------
        print("\n================ BUILDING CALIBRATION LUT ================", flush=True)

        self.calib_lut = {}

        for hall in WORKING_HALLS:
            if hall not in self.calibrated_df.columns:
                print(f"[LUT] ❌ {hall} column missing", flush=True)
                continue

            lut = {}
            for _, row in self.calibrated_df.iterrows():
                val = row[hall]
                if not pd.isna(val):
                    lut[int(val)] = row[Depth_col]

            self.calib_lut[hall] = lut

            sample = list(lut.items())
            print(f"[LUT] {hall}: size={len(lut)} sample={sample}", flush=True)

        print("================ LUT BUILD COMPLETE =====================\n", flush=True)

        circle_container = QWidget()
        self.circle_stack = QStackedLayout(circle_container)
        self.circle_stack.setContentsMargins(0, 0, 0, 0)

        self.circle_stack.addWidget(self.circle_placeholder)  # index 0
        self.circle_stack.addWidget(self.circle)              # index 1
        self.circle_stack.setCurrentIndex(0)                  # placeholder first

        circle_frame = QFrame()
        circle_frame.setFrameShape(QFrame.StyledPanel)
        circle_layout = QVBoxLayout(circle_frame)
        circle_layout.setContentsMargins(8, 8, 8, 8)
        circle_layout.addWidget(circle_container)

        # ---------------- HEATMAP / TABLE ----------------
        self.selector_placeholder = make_placeholder(
            "Please select weld and click Analyse button"
        )

        if USE_HEATMAP:
            self.selector = HeatmapWidget(self.apply_row_index)
        else:
            self.selector = DataTable(
                self.data_df,
                25000,
                26000,
                ALL_HALLS,
                self.apply_row_index
            )

        selector_container = QWidget()
        self.selector_stack = QStackedLayout(selector_container)
        self.selector_stack.setContentsMargins(0, 0, 0, 0)

        self.selector_stack.addWidget(self.selector_placeholder)  # index 0
        self.selector_stack.addWidget(self.selector)              # index 1
        self.selector_stack.setCurrentIndex(0)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(selector_container)
        splitter.setStretchFactor(0, 1)

        # ---------------- TOOLBAR ----------------
        self.toolbar = VDTToolbar(main_window=self)


        # ---------------- MAIN LAYOUT ----------------
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.toolbar)     # toolbar
        main_layout.addWidget(circle_frame, 3)  # circle
        main_layout.addWidget(splitter, 2)      # table/heatmap

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def build_visual_labels_from_all_halls(self, all_halls, working_halls, minute_step):
        """
        Build time labels based on ALL_HALLS timeline,
        then pick only WORKING_HALLS from it.
        """

        timeline_labels = {}
        total_minutes = 0

        # Step 1: build timeline for ALL_HALLS
        for hall in all_halls:
            total_minutes += minute_step
            mm = total_minutes % 60
            hh = (total_minutes // 60) % 24
            timeline_labels[hall] = f"{hh:02d}:{mm:02d}"

        # Step 2: pick only working halls
        visual_labels = {
            hall: timeline_labels[hall]
            for hall in working_halls
            if hall in timeline_labels
        }

        return visual_labels

    # ---------------- ACTIVATE ANALYSIS VIEW ----------------
    def show_analysis_views(self):
        self.circle_stack.setCurrentIndex(1)
        self.selector_stack.setCurrentIndex(1)

        # 🔥 APPLY FIRST CSV ROW IMMEDIATELY
        # self.apply_row_index(0)

    # ---------------- DATA APPLY ----------------
    def apply_row_index(self, pipe_index):
        self.pipe_index = pipe_index
        print(f"[SELECT] index from heatmap = {pipe_index}", flush=True)

        # Safety check
        if self.raw_df is None:
            print("❌ raw PKL not loaded")
            return

        # Pick the SAME row using index
        row = self.raw_df[self.raw_df["index"] == pipe_index]

        if row.empty:
            print(f"❌ index {pipe_index} not found in raw PKL")
            return

        row = row.iloc[0]

        measured = {
            h: float(row[h])
            for h in ALL_HALLS
            if h in row
        }
        self.measured = measured
        print(f"values of hall at index={pipe_index} is hall values = [{measured}]")

        # compute depth using SAME index
        depth_moved = compute_depth_fast_debug(
            self,
            calib_lut=self.calib_lut,
            working_halls=WORKING_HALLS,
            reference_values=self.circle.reference_values,
            clicked_values=measured,
            threshold=threshold
        )

        # from circular_dent_maker.modular_maker.circular_view import DEPTH_MOVED
        from .circular_view import DEPTH_MOVED
        DEPTH_MOVED.clear()
        DEPTH_MOVED.update(depth_moved)

        self.circle.set_target_values(measured)

        # update circle
        # self.circle.set_target_values(measured)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     w = MainWindow()
#     w.resize(1300, 900)
#     w.show()
#     sys.exit(app.exec_())
def run_standalone():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(1300, 900)
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_standalone()
