# import os
# import pickle
# import tempfile
# import subprocess
# import pandas as pd
# import sys
#

# -----------------------------
# 🔧 Hardcoded inputs
# -----------------------------
# XLSX_PATH = r"D:\Anubhav\vdt_backend\egp_soft_based_on_mfl\backend_data\Pipe_Tally_8inch (1).xlsx"
# PROJECT_ROOT = r"D:\Anubhav\pickle9"
# DIGSHEET_ABS_PY = r"D:\Anubhav\vdt_backend\egp_soft_based_on_mfl\Components\dig\digsheet_abs.py"
# ABS_DISTANCE = "240.456"


# def xlsx_to_temp_pkl(xlsx_path):
#     df = pd.read_excel(xlsx_path)
#     temp_path = os.path.join(
#         tempfile.gettempdir(),
#         f"pipe_tally_{next(tempfile._get_candidate_names())}.pkl"
#     )
#     with open(temp_path, "wb") as f:
#         pickle.dump(df, f)
#     return temp_path
#
#
# def run_with_debug(cmd):
#     print("\n🔍 Running with DEBUG…\n")
#     print(" ".join(cmd))
#     print("\n-------------------------------------------\n")
#
#     # Run process and CAPTURE ITS OUTPUT
#     process = subprocess.Popen(
#         cmd,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True
#     )
#
#     out, err = process.communicate()
#
#     print("📤 STDOUT:\n", out)
#     print("\n❌ STDERR:\n", err)
#
#     if err.strip():
#         print("\n❗ ERROR DETECTED — digsheet failed to launch.")
#     else:
#         print("\n✔ No errors detected — Tkinter window should be visible.")
#
#
# if __name__ == "__main__":
#     pkl_path = xlsx_to_temp_pkl(XLSX_PATH)
#
#     cmd = [
#         sys.executable,
#         DIGSHEET_ABS_PY,
#         pkl_path,
#         ABS_DISTANCE,
#         PROJECT_ROOT
#     ]
#
#     run_with_debug(cmd)


# import os
# import pickle
# import tempfile
# import pandas as pd

# XLSX_PATH = r"D:\Anubhav\vdt_backend\egp_soft_based_on_mfl\backend_data\Pipe_Tally_8inch (1).xlsx"
# PROJECT_ROOT = r"D:\Anubhav\pickle9"
# DIGSHEET_ABS_PY = r"D:\Anubhav\vdt_backend\egp_soft_based_on_mfl\Components\dig\digsheet_abs.py"
# ABS_DISTANCE = "240.456"
#
# def run_digsheet(xlsx_path, digsheet_py, abs_distance, project_root):
#     """Full pipeline: XLSX → temp PKL → Run digsheet with debug."""
#
#     # ------------------------------
#     # 1. Convert XLSX → Temporary PKL
#     # ------------------------------
#     df = pd.read_excel(xlsx_path)
#     temp_pkl = os.path.join(
#         tempfile.gettempdir(),
#         f"pipe_tally_{next(tempfile._get_candidate_names())}.pkl"
#     )
#     with open(temp_pkl, "wb") as f:
#         pickle.dump(df, f)
#
#     print(f"\n📥 XLSX Loaded: {xlsx_path}")
#     print(f"📦 Temp PKL created at: {temp_pkl}\n")
#
#     # ------------------------------
#     # 2. Build command
#     # ------------------------------
#     cmd = [
#         sys.executable,
#         digsheet_py,
#         temp_pkl,
#         abs_distance,
#         project_root
#     ]
#
#     print("▶ Running digsheet with command:")
#     print(" ", " ".join(cmd))
#     print("\n-------------------------------------------\n")
#
#     # ------------------------------
#     # 3. Launch with DEBUG output
#     # ------------------------------
#     process = subprocess.Popen(
#         cmd,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True
#     )
#
#     out, err = process.communicate()
#
#     print("📤 STDOUT:\n", out)
#     print("\n❌ STDERR:\n", err)
#
#     if err.strip():
#         print("\n❗ ERROR DETECTED — digsheet script failed.")
#     else:
#         print("\n✔ No errors — Tkinter digsheet window should be visible.\n")
#
#     return temp_pkl  # in case caller needs it
#
#
# run_digsheet(
#     xlsx_path=XLSX_PATH,
#     digsheet_py=DIGSHEET_ABS_PY,
#     abs_distance=ABS_DISTANCE,
#     project_root=PROJECT_ROOT
# )


#
# import os
# import pickle
# import uuid
# import tempfile
# import pandas as pd
# from egp_soft_based_on_mfl.Components.dig.digsheet_abs import DigsheetABS
#
# xls_path = r"D:\Anubhav\vdt_backend\egp_soft_based_on_mfl\backend_data\Pipe_Tally_8inch (1).xlsx"
# abs_value = "240.456"
# project_root = r"D:\Anubhav\pickle9"
#
# def xlsx_to_temp_pkl(xlsx_path: str) -> str:
#     df = pd.read_excel(xlsx_path)
#     temp_path = os.path.join(
#         tempfile.gettempdir(),
#         f"pipe_tally_{uuid.uuid4().hex}.pkl"
#     )
#     with open(temp_path, "wb") as f:
#         pickle.dump(df, f)
#
#     print(f"✅ Temp pipe_tally.pkl created: {temp_path}")
#     return temp_path
#
#
# def run_digsheet(xlsx_path: str, abs_value: str, project_root: str):
#     pkl_path = xlsx_to_temp_pkl(xlsx_path)
#     app = DigsheetABS(pkl_path, abs_value, project_root)
#     app.run()   # opens the window
#
#
# run_digsheet(xls_path, abs_value, project_root)




import os
import pickle
import uuid
import tempfile
import threading
import pandas as pd

from egp_soft_based_on_mfl.Components.dig.digsheet_abs import DigsheetABS


class DigsheetABSRunner:
    """
    A clean reusable runner class for launching DigsheetABS.
    Allows optional parent injection for future integration.
    """

    def __init__(self, parent=None):
        """
        parent → your PyQt MainWindow or any object you want to pass
                 to the digsheet later.
        """
        self.parent = parent

    # -------------------------
    # Excel → Temp Pickle
    # -------------------------
    def xlsx_to_temp_pkl(self, xlsx_path: str) -> str:
        df = pd.read_excel(xlsx_path)

        temp_path = os.path.join(
            tempfile.gettempdir(),
            f"pipe_tally_{uuid.uuid4().hex}.pkl"
        )

        with open(temp_path, "wb") as f:
            pickle.dump(df, f)

        print(f"✅ Temp pipe_tally.pkl created: {temp_path}")
        return temp_path

    # -------------------------
    # Run directly in the same thread (blocking)
    # -------------------------
    def run(self, xlsx_path: str, abs_value: str):
        """
        Runs the DigsheetABS normally (blocking).
        """
        defect_no = getattr(self.parent, "selected_defect_no", None)
        abs_dist = getattr(self.parent, "selected_abs_distance", None)
        config = getattr(self.parent, "config", None)

        # print(f"[RUN] Defect no from parent = {defect_no}")
        # print(f"[RUN] ABS distance from parent = {abs_dist}")
        # print(f"CONFIG INSIDE DIG: {config.pipe_thickness}")

        pkl_path = self.xlsx_to_temp_pkl(xlsx_path)

        app = DigsheetABS(
            pkl_path,
            abs_value,
            project_root=None,
            parent=self.parent   # Optional parent injection
        )

        return app.run()

    # -------------------------
    # Run safely from a PyQt button using a thread
    # -------------------------
    def run_in_thread(self, xlsx_path: str, abs_value: str, project_root: str):
        """
        Launches the DigsheetABS window in a separate thread.
        Perfect for PyQt so UI never freezes.
        """

        def _worker():
            self.run(xlsx_path, abs_value, project_root)

        t = threading.Thread(target=_worker, daemon=True)
        t.start()
        return t


# def digsheet_abs_runner(self):
#     runner = DigsheetABSRunner()  # 👈 NO parent provided
#
#     runner.run(
#         r"D:\Anubhav\vdt_backend\egp_soft_based_on_mfl\backend_data\Pipe_Tally_8inch (1).xlsx",
#         "240.456",
#         r"D:\Anubhav\pickle9"
#     )

# digsheet_abs_runner(self=None)