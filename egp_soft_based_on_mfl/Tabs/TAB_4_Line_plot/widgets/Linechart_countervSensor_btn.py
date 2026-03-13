from google.cloud import bigquery, bigquery_storage_v1
import os
import pandas as pd
import json
# from  egp_soft_based_on_mfl.Components.self.configs import self.config as self.config
from google.oauth2 import service_account

from egp_soft_based_on_mfl.Components.Configs import config_universal
from egp_soft_based_on_mfl.utils.loaderdialog.loader_dialog import LoaderDialog
from .helper_functions import plot_linechart_sensor
from .tab4_loading_dialog_worker import LineChart1Worker

try:
    from google.cloud.bigquery_storage_v1 import BigQueryReadClient
except ImportError:
    # fallback for environments where Pycharm uses wrong interpreter
    import importlib
    BigQueryReadClient = importlib.import_module(
        "google.cloud.bigquery_storage_v1"
    ).BigQueryReadClient


"""
----->Line chart tab(4) all functions starts from here
"""

# def Line_chart1(self):
#     runid = self.parent.runid
#     weld_id = self.combo.currentText()
#     self.parent.weld_id = int(weld_id)
#     p = self.parent.project_name
#     print(p)
#     with self.config.connection.cursor() as cursor:
#         # query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
#         query = "SELECT start_index, end_index,start_oddo1,end_oddo1 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"
#
#         cursor.execute(query, (runid, self.parent.weld_id, runid, self.parent.weld_id))
#         result = cursor.fetchall()
#         if result:
#             path = config_universal.weld_pipe_pkl + self.parent.project_name + '/' + str(weld_id) + '.pkl'
#             print(path)
#             if os.path.isfile(path):
#                 config_universal.print_with_time("File exist")
#                 df_pipe = pd.read_pickle(path)
#                 # print(self.df_pipe)
#
#                 plot_linechart_sensor(self,df_pipe)
#
#             else:
#                 folder_path = config_universal.weld_pipe_pkl + self.parent.project_name
#                 print(folder_path)
#                 config_universal.print_with_time("File not exist")
#                 try:
#                     os.makedirs(folder_path)
#
#                 except:
#                     config_universal.print_with_time("Folder already exists")
#                 start_index, end_index = result[0][0], result[1][1]
#                 print("start index and end index", start_index, end_index)
#                 credentials = self.config.credentials
#                 project_id = self.config.project_id
#                 client = bigquery.Client(credentials=credentials, project=project_id)
#
#
#                 def fetch_tab4_data_fast(self, start_index, end_index, folder_path, weld_id):
#                     """
#                     EXACT old Tab-4 logic, but using BigQuery Storage API for speed.
#                     Output is IDENTICAL to your old code.
#                     """
#
#                     config_universal.print_with_time("Start fetching at : ")
#
#                     # -----------------------------------------------------------
#                     # AUTH + shared Storage API client
#                     # -----------------------------------------------------------
#                     credentials = service_account.Credentials.from_service_account_file(
#                         "./utils/Authorization.json",
#                         scopes=[
#                             "https://www.googleapis.com/auth/cloud-platform",
#                             "https://www.googleapis.com/auth/bigquery",
#                             "https://www.googleapis.com/auth/bigquery.readonly",
#                         ]
#                     )
#
#                     if not hasattr(self, "_bqstorage_client") or self._bqstorage_client is None:
#                         self._bqstorage_client = bigquery_storage_v1.BigQueryReadClient(credentials=credentials)
#
#                     bqstorage_client = self._bqstorage_client
#                     client = self.config.client
#
#                     # -----------------------------------------------------------
#                     # 1️⃣ FIRST QUERY — HALL DATA
#                     # -----------------------------------------------------------
#                     query_1 = (
#                             "SELECT index, ROLL, ODDO1, ODDO2, ["
#                             + self.config.sensor_str_hall +
#                             "] AS HALL_DATA, PITCH, YAW FROM "
#                             + self.config.table_name +
#                             " WHERE index>{} AND index<{} ORDER BY index"
#                     ).format(start_index, end_index)
#
#                     config_universal.print_with_time("Sending HALL query…")
#                     df_main = client.query(query_1).to_dataframe(bqstorage_client=bqstorage_client)
#                     df_main = df_main.sort_values("index").reset_index(drop=True)
#
#                     config_universal.print_with_time(f"HALL rows fetched → {len(df_main)}")
#
#                     # Extract lists EXACTLY like your old code did
#                     index_t4 = df_main["index"].tolist()
#                     oddo_1 = df_main["ODDO1"].tolist()
#                     oddo_2 = df_main["ODDO2"].tolist()
#                     roll1 = df_main["ROLL"].tolist()
#                     pitch1 = df_main["PITCH"].tolist()
#                     yaw1 = df_main["YAW"].tolist()
#                     hall_arrays = df_main["HALL_DATA"].tolist()
#
#                     # Reference subtraction (same logic as old)
#                     oddo1_t4 = [(v - self.config.oddo1) for v in oddo_1]
#                     oddo2_t4 = [(v - self.config.oddo2) for v in oddo_2]
#                     roll_t4 = [(v - self.config.roll_value) for v in roll1]
#                     pitch_t4 = [(v - self.config.pitch_value) for v in pitch1]
#                     yaw_t4 = [(v - self.config.yaw_value) for v in yaw1]
#
#                     # Expand HALL arrays → df_new_t4
#                     hall_cols = [
#                         f'F{i}H{j}'
#                         for i in range(1, self.config.F_columns + 1)
#                         for j in range(1, 5)
#                     ]
#                     df_new_t4 = pd.DataFrame(hall_arrays, columns=hall_cols)
#
#                     # df_elem (exact same structure as old code)
#                     df_elem = pd.DataFrame({
#                         "index": index_t4,
#                         "ODDO1": oddo1_t4,  # RAW ODDO1 (old behavior)
#                         "ROLL": roll_t4,
#                         "PITCH": pitch_t4,
#                         "YAW": yaw_t4
#                     })
#
#                     # -----------------------------------------------------------
#                     # 2️⃣ SECOND QUERY — PROX DATA
#                     # -----------------------------------------------------------
#                     query_2 = (
#                             "SELECT index, ["
#                             + self.config.sensor_str_prox +
#                             "] AS PROX_DATA FROM "
#                             + self.config.table_name +
#                             " WHERE index>{} AND index<{} ORDER BY index"
#                     ).format(start_index, end_index)
#
#                     config_universal.print_with_time("Sending PROX query…")
#                     df_prox = client.query(query_2).to_dataframe(bqstorage_client=bqstorage_client)
#                     df_prox = df_prox.sort_values("index").reset_index(drop=True)
#
#                     config_universal.print_with_time(f"PROX rows fetched → {len(df_prox)}")
#
#                     prox_arrays = df_prox["PROX_DATA"].tolist()
#
#                     df_new_proximity_lc = pd.DataFrame(
#                         prox_arrays,
#                         columns=self.config.sensor_columns_prox
#                     )
#                     df_new_proximity_lc.insert(0, "index", df_prox["index"].tolist())
#
#                     # -----------------------------------------------------------
#                     # MERGE SAFELY (NO join='inner')
#                     # Row alignment is POSITIONAL to avoid Storage API quirks
#                     # -----------------------------------------------------------
#                     df_pipe = pd.concat(
#                         [df_elem.reset_index(drop=True),
#                          df_new_t4.reset_index(drop=True)],
#                         axis=1
#                     )
#
#                     # Attach PROX columns (also align by row position)
#                     df_new_proximity_lc = df_new_proximity_lc.reset_index(drop=True)
#
#                     for col in df_new_proximity_lc.columns:
#                         if col != "index":
#                             df_pipe[col] = df_new_proximity_lc[col]
#
#                     # -----------------------------------------------------------
#                     # FINAL GUARANTEED index column (NO CRASH, ALWAYS PRESENT)
#                     # -----------------------------------------------------------
#                     if "index" in df_pipe.columns:
#                         df_pipe["index"] = index_t4[:len(df_pipe)]
#                     else:
#                         df_pipe.insert(0, "index", index_t4[:len(df_pipe)])
#
#                     # -----------------------------------------------------------
#                     # SAVE PKL
#                     # -----------------------------------------------------------
#                     file_path = folder_path + '/' + str(weld_id) + '.pkl'
#                     df_pipe.to_pickle(file_path)
#
#                     config_universal.print_with_time("Successfully saved pickle file")
#                     config_universal.print_with_time("End fetching at : ")
#
#                     return {
#                         "df_pipe": df_pipe,
#                         "df_elem": df_elem,
#                         "df_new_t4": df_new_t4,
#                         "df_new_proximity_lc": df_new_proximity_lc,
#                         "file_path": file_path,
#                         "index_t4": index_t4
#                     }
#
#                 config_universal.print_with_time("STARTING FETCHING AT : ")
#                 result = fetch_tab4_data_fast(self, start_index, end_index, folder_path, weld_id)
#                 config_universal.print_with_time("ENDING FETCHING AT : ")
#
#                 config_universal.print_with_time("starting plotting at : ")
#                 df_pipe = result["df_pipe"]
#                 plot_linechart_sensor(self, df_pipe)
#                 config_universal.print_with_time("Ending plotting at : ")
#         else:
#             config_universal.print_with_time("No data found for this pipe ID : ")


def Line_chart1(self):
    self.loader = LoaderDialog(self.tab_line1, "Generating Line Chart")

    self.worker = LineChart1Worker(self)

    self.worker.progress.connect(self.loader.update_progress)
    self.worker.message.connect(self.loader.update_status)

    self.worker.finished.connect(self.Line_chart1_finished)
    self.worker.finished.connect(self.worker.deleteLater)

    self.loader.show()
    self.worker.start()
