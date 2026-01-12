# import os
# import sys
# import uuid
# import tempfile
# import pickle
# import runpy
#
# import pandas as pd
#
#
# # 🔧 HARD-CODED PATHS – EDIT THESE
# DIG_SHEET_PATH = r"D:\Anubhav\vdt_backend\GMFL_12_Inch_Desktop\Components\dig\dig_sheet.py"
#
# # Your actual pipe tally CSV:
# PIPE_TALLY_CSV = r"D:\Anubhav\vdt_backend\GMFL_12_Inch_Desktop\backend_data\Pipe_Tally_8inch (1).xlsx"
#
# # Your project_root:
# PROJECT_ROOT   = r"D:\Anubhav\pickle9"
#
#
# # -------------------------------------------------
# # SAME TEMP DUMP FUNC YOUR APP USES
# # -------------------------------------------------
# def _dump_tally_to_temp(df: pd.DataFrame) -> str:
#     """
#     Dump the pipe_tally DataFrame to a unique temp .pkl file
#     and return the file path.
#     """
#     p = os.path.join(tempfile.gettempdir(), f"pipe_tally_{uuid.uuid4().hex}.pkl")
#     with open(p, "wb") as f:
#         pickle.dump(df, f)
#     print(f"✅ Temp pipe_tally.pkl written to: {p}")
#     return p
#
#
# def main():
#
#     # 1. Sanity check paths
#     if not os.path.exists(DIG_SHEET_PATH):
#         raise FileNotFoundError(f"dig_sheet.py not found at: {DIG_SHEET_PATH}")
#
#     if not os.path.exists(PIPE_TALLY_CSV):
#         raise FileNotFoundError(f"Pipe tally CSV not found: {PIPE_TALLY_CSV}")
#
#     # 2. Load CSV → DataFrame
#     print(f"📥 Loading CSV pipe_tally from: {PIPE_TALLY_CSV}")
#     df = pd.read_excel(PIPE_TALLY_CSV)
#
#     print(f"   Loaded rows: {len(df)}")
#
#     # 3. Dump DataFrame → TEMP .PKL (same as app)
#     temp_pkl = _dump_tally_to_temp(df)
#
#     # 4. Prepare arguments for dig_sheet.py
#     sys.argv = [DIG_SHEET_PATH, temp_pkl, PROJECT_ROOT]
#
#     print("\n▶ Running dig_sheet.py with:")
#     print(f"   tally_pkl    = {temp_pkl}")
#     print(f"   project_root = {PROJECT_ROOT}")
#     print("-" * 70)
#
#     # 5. Execute dig_sheet.py AS MAIN
#     runpy.run_path(DIG_SHEET_PATH, run_name="__main__")
#
#
# if __name__ == "__main__":
#     main()
#
import os
import pickle
import uuid
import tempfile
import pandas as pd
from GMFL_12_Inch_Desktop.Components.dig.dig_sheet import Digsheet


class DigsheetRunnerSimple:
    """
    Minimal runner class:
    - Converts Excel → temp PKL
    - Launches Digsheet
    """

    def __init__(self, parent=None):
        # reserved for future use (PyQt parent etc.)
        self.parent = parent

    def xlsx_to_temp_pkl(self, xlsx_path: str) -> str:
        """Convert Excel to a temporary pickle file."""
        df = pd.read_excel(xlsx_path)

        temp_path = os.path.join(
            tempfile.gettempdir(),
            f"pipe_tally_{uuid.uuid4().hex}.pkl"
        )

        with open(temp_path, "wb") as f:
            pickle.dump(df, f)

        print(f"✅ Temp file: {temp_path}")
        return temp_path

    def run_digsheet(self, xlsx_path: str, project_root: str):
        """
        Full pipeline:
          1. Excel → PKL
          2. Launch Digsheet with the PKL
        """
        pkl_path = self.xlsx_to_temp_pkl(xlsx_path)

        app = Digsheet(
            pipe_tally_file=pkl_path,
            project_root=project_root,
            # parent=self.parent   # optional use later
        )

        app.run()   # runs Tkinter window


runner = DigsheetRunnerSimple()

runner.run_digsheet(
    r"D:\Anubhav\vdt_backend\GMFL_12_Inch_Desktop\backend_data\Pipe_Tally_8inch (1).xlsx",
    r"D:\Anubhav\pickle9"
)

