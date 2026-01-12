from pathlib import Path

from google.cloud import bigquery
import json
import os

from .render_linechart_tab5 import render_linechart_tab5
from .fetch_from_gcp import fetch_orientation_df_from_gcp
from .helper_functions import safe_read_pickle, save_pickle_safely, fetch_weld_range
# from GMFL_12_Inch_Desktop.Components.Configs import config as config
#
# connection = config.connection
# company_list = []  # list of companies
# credentials = config.credentials
# project_id = config.project_id
# client = bigquery.Client(credentials=credentials, project=project_id)
# config = json.loads(open(r'D:\Anubhav\vdt_backend\GMFL_12_Inch_Desktop\utils\proximity_base_value.json').read())

# Dynamically locate the GMFL root (2 levels above this file)
GMFL_ROOT = Path(__file__).resolve().parents[3]


def gmfl_path(relative):
    """Return absolute path inside GMFL backend_data/temp folder."""
    temp_dir = GMFL_ROOT / "backend_data" / "data_generated" / "temp"
    os.makedirs(temp_dir, exist_ok=True)  # make sure folder exists
    return str(temp_dir / relative)



def Line_chart_orientation(self):
    runid = self.parent.runid
    weld_num = self.combo_orientation.currentText()
    self.weld_num = int(weld_num)

    with self.config.connection.cursor() as cursor:
        #check if weld are fecthed or not / if not present
        result = fetch_weld_range(self, cursor, self.parent.runid, self.weld_num)
        if result is None:
            return

        start_oddo1 = result[0][2]
        end_oddo1 = result[1][3]
        print(f"weld idP: {weld_num}")

        # --- Pickle path setup ---
        path = Path(self.config.roll_pkl_lc) / self.parent.project_name.strip() / f"{self.weld_num}.pkl"
        os.makedirs(path.parent, exist_ok=True)
        print(f"path for pkl line chart orientation: {path}")

        # --- SAFE READ PICKLE ---
        df_clock_holl = safe_read_pickle(self, path)

        #CASE 1 -- Data is already there -----
        if df_clock_holl is not None:
            self.config.print_with_time("Loaded data from existing pickle.")

            # make the linechart if data exist already
            render_linechart_tab5(self, df_clock_holl)

            self.config.print_with_time("Plotted from pickle.")
            return

        #CASE 2 -- NO DATA --- first fetching then plot ---
        df_new = fetch_orientation_df_from_gcp(self, result, self.config.client)        #fetch the data from GCP
        ok = save_pickle_safely(self, path, df_new)                               #save the fecth data local SAFELY IMP

        #plot the chart using fetched data
        render_linechart_tab5(self, df_new)
        self.config.print_with_time("Plotted...")


