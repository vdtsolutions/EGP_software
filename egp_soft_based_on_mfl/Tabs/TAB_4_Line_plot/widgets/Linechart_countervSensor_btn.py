from google.cloud import bigquery, bigquery_storage_v1
import os
import pandas as pd
import json
# from  GMFL_12_Inch_Desktop.Components.self.configs import self.config as self.config
from google.oauth2 import service_account

from .helper_functions import plot_linechart_sensor

try:
    from google.cloud.bigquery_storage_v1 import BigQueryReadClient
except ImportError:
    # fallback for environments where Pycharm uses wrong interpreter
    import importlib
    BigQueryReadClient = importlib.import_module(
        "google.cloud.bigquery_storage_v1"
    ).BigQueryReadClient
# connection = self.config.connection
# credentials = self.config.credentials
# project_id = self.config.project_id
# client = bigquery.Client(credentials=credentials, project=project_id)
# self.config = json.loads(open('./utils/proximity_base_value.json').read())

"""
----->Line chart tab(4) all functions starts from here
"""

def Line_chart1(self):
    runid = self.parent.runid
    weld_id = self.combo.currentText()
    self.parent.weld_id = int(weld_id)
    p = self.parent.project_name
    print(p)
    with self.config.connection.cursor() as cursor:
        # query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
        query = "SELECT start_index, end_index,start_oddo1,end_oddo1 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"

        cursor.execute(query, (runid, self.parent.weld_id, runid, self.parent.weld_id))
        result = cursor.fetchall()
        if result:
            path = self.config.weld_pipe_pkl + self.parent.project_name + '/' + str(weld_id) + '.pkl'
            print(path)
            if os.path.isfile(path):
                self.config.print_with_time("File exist")
                df_pipe = pd.read_pickle(path)
                # print(self.df_pipe)

                plot_linechart_sensor(self,df_pipe)

            else:
                folder_path = self.config.weld_pipe_pkl + self.parent.project_name
                print(folder_path)
                self.config.print_with_time("File not exist")
                try:
                    os.makedirs(folder_path)

                except:
                    self.config.print_with_time("Folder already exists")
                start_index, end_index = result[0][0], result[1][1]
                print("start index and end index", start_index, end_index)
                # self.config.print_with_time("Start fetching at : ")
                #
                #
                # query_for_start = (
                #         "SELECT index, ROLL, ODDO1, ODDO2, ["
                #         + self.config.sensor_str_hall +
                #         "], PITCH, YAW FROM "
                #         + self.config.table_name +
                #         " WHERE index>{} AND index<{} ORDER BY index"
                # )
                # # query_for_start = 'SELECT index,ROLL,ODDO1,ODDO2,[F1H1, F1H2, F1H3, F1H4, F2H1, F2H2, F2H3, F2H4,F3H1, F3H2, F3H3, F3H4, F4H1, F4H2, F4H3,F4H4, F5H1, F5H2, F5H3, F5H4, F6H1, F6H2, F6H3, F6H4,F7H1, F7H2, F7H3, F7H4, F8H1, F8H2, F8H3, F8H4, F9H1, F9H2, F9H3, F9H4, F10H1,F10H2, F10H3, F10H4,F11H1, F11H2, F11H3, F11H4, F12H1, F12H2, F12H3, F12H4, F13H1, F13H2, F13H3,F13H4, F14H1, F14H2, F14H3, F14H4,F15H1, F15H2, F15H3, F15H4, F16H1, F16H2, F16H3, F16H4, F17H1, F17H2, F17H3,F17H4, F18H1, F18H2, F18H3, F18H4,F19H1, F19H2, F19H3, F19H4, F20H1, F20H2, F20H3, F20H4, F21H1, F21H2, F21H3,F21H4, F22H1, F22H2, F22H3, F22H4,F23H1, F23H2, F23H3, F23H4, F24H1, F24H2, F24H3, F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4,F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1,F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4],PITCH,YAW FROM ' + self.config.table_name + ' WHERE index>{} AND index<{} order by index'
                # query_job = self.config.client.query(query_for_start.format(start_index, end_index))
                # results = query_job.result()
                #
                # data = []
                # index_t4 = []
                # oddo_1 = []
                # oddo_2 = []
                # # indexes = []
                # roll1 = []
                # pitch1 = []
                # yaw1 = []
                #
                # for row in results:
                #     index_t4.append(row[0])
                #     roll1.append(row[1])
                #     oddo_1.append(row[2])
                #     oddo_2.append(row[3])
                #     data.append(row[4])
                #     pitch1.append(row[5])
                #     yaw1.append(row[6])
                #     """
                #     Swapping the Pitch data to Roll data
                #     """
                #
                # oddo1_t4 = []
                # oddo2_t4 = []
                # roll_t4 = []
                # pitch_t4 = []
                # yaw_t4 = []
                #
                # """
                # Reference value will be consider
                # """
                # for odometer1 in oddo_1:
                #     od1 = odometer1 - self.config.oddo1  ###16984.2 change According to run
                #     oddo1_t4.append(od1)
                # for odometer2 in oddo_2:
                #     od2 = odometer2 - self.config.oddo2  ###17690.36 change According to run
                #     oddo2_t4.append(od2)
                #
                # """
                # Reference value will be consider
                # """
                # for roll2 in roll1:
                #     roll3 = roll2 - self.config.roll_value
                #     roll_t4.append(roll3)
                #
                # for pitch2 in pitch1:
                #     pitch3 = pitch2 - self.config.pitch_value
                #     pitch_t4.append(pitch3)
                #
                # for yaw2 in yaw1:
                #     yaw3 = yaw2 - self.config.yaw_value
                #     yaw_t4.append(yaw3)
                #
                #
                # # query_for_start = 'SELECT index,[F1P1, F2P2, F3P3, F4P4, F5P1, F6P2, F7P3, F8P4, F9P1, F10P2, F11P3, F12P4, F13P1, F14P2, F15P3, F16P4, F17P1, F18P2, F19P3, F20P4, F21P1, F22P2, F23P3, F24P4, F25P1, F26P2, F27P3, F28P4, F29P1, F30P2, F31P3, F32P4, F33P1, F34P2, F35P3, F36P4] FROM ' + self.config.table_name + ' WHERE index>{} AND index<{} order by index'
                # query_for_start = (
                #         "SELECT index, ["
                #         + self.config.sensor_str_prox +
                #         "] FROM "
                #         + self.config.table_name +
                #         " WHERE index>{} AND index<{} ORDER BY index"
                # )
                # query_job = self.config.client.query(query_for_start.format(start_index, end_index))
                # results_1 = query_job.result()
                # data1 = []
                # index_lc = []
                # for row1 in results_1:
                #     index_lc.append(row1[0])
                #     data1.append(row1[1])
                #
                # df_new_proximity_lc = pd.DataFrame(data1, columns=self.config.sensor_columns_prox)
                #
                # df_new_t4 = pd.DataFrame(data, columns=[f'F{i}H{j}' for i in range(1, self.config.F_columns + 1) for j in range(1, 5)])
                #
                # df_elem = pd.DataFrame(
                #     {"index": index_t4, "ODDO1": oddo_1, "ROLL": roll_t4, "PITCH": pitch_t4, "YAW": yaw_t4})
                # frames = [df_elem, df_new_t4]
                # df_pipe = pd.concat(frames, axis=1, join='inner')
                #
                # for col in df_new_proximity_lc.columns:
                #     df_pipe[col] = df_new_proximity_lc[col]
                #
                # # df_new.reset_index(inplace=True)
                # # print("Plotted data", df_pipe)
                # df_pipe.to_pickle(folder_path + '/' + str(weld_id) + '.pkl')
                # self.config.print_with_time("Succesfully saved to pickle file")
                # self.config.print_with_time("End fetching  at : ")
                credentials = self.config.credentials
                project_id = self.config.project_id
                client = bigquery.Client(credentials=credentials, project=project_id)
                # def fetch_and_save_tab9_data(self, client, start_index, end_index, folder_path1, Weld_id_tab9):
                #     """
                #     Optimized — uses BigQuery Storage API.
                #     Naming, logic, output = IDENTICAL to old code.
                #     """
                #     credentials = service_account.Credentials.from_service_account_file(
                #         "./utils/Authorization.json",
                #         scopes=[
                #             "https://www.googleapis.com/auth/cloud-platform",
                #             "https://www.googleapis.com/auth/bigquery",
                #             "https://www.googleapis.com/auth/bigquery.readonly",
                #         ]
                #     )
                #
                #     # -----------------------------------------------------------
                #     # Init Storage API client ONCE (reuses client each call)
                #     # -----------------------------------------------------------
                #     self.config.print_with_time("Start of conversion at : ")
                #     if not hasattr(self, "_bqstorage_client") or self._bqstorage_client is None:
                #         self._bqstorage_client = BigQueryReadClient()
                #
                #     bqstorage_client = bigquery_storage_v1.BigQueryReadClient(credentials=credentials)
                #
                #     # -----------------------------------------------------------
                #     # 1️⃣ FIRST QUERY — using Storage API
                #     # -----------------------------------------------------------
                #     self.config.print_with_time("⏳[1] Start building first-query SQL")
                #
                #     query_for_start = (
                #             "SELECT index, ROLL, ODDO1, ODDO2, ["
                #             + self.config.sensor_str_hall +
                #             "] AS HALL_DATA, PITCH, YAW "
                #             "FROM " + self.config.table_name + " "
                #                                                "WHERE index>{} AND index<{}"
                #     )
                #
                #     self.config.print_with_time("🚀[2] Start sending first query (Storage API)")
                #     query_job = client.query(query_for_start.format(start_index, end_index))
                #
                #     self.config.print_with_time("📥[3] Start to_dataframe() for first query")
                #     results = query_job.to_dataframe(bqstorage_client=bqstorage_client)
                #     self.config.print_with_time(f"📤[4] results fetched → {len(results)} rows")
                #
                #     # df_main starts as copied results (same naming convention)
                #     self.config.print_with_time("🧱[5] Creating df_main")
                #     df_main = results.copy()
                #     # 🔧 Ensure same ordering as old BigQuery Iterator
                #     df_main = df_main.sort_values("index").reset_index(drop=True)
                #     # -----------------------------------------------------------
                #     # Expand HALL_DATA array → F1H1...F36H4
                #     # -----------------------------------------------------------
                #     self.config.print_with_time("🧩[6] Expanding HALL_DATA")
                #
                #     hall_cols = [
                #         f'F{i}H{j}'
                #         for i in range(1, self.config.F_columns + 1)
                #         for j in range(1, 5)
                #     ]
                #
                #     df_hall = pd.DataFrame(df_main["HALL_DATA"].tolist(), columns=hall_cols)
                #
                #     df_main = pd.concat([df_main.drop(columns=["HALL_DATA"]), df_hall], axis=1)
                #
                #     # -----------------------------------------------------------
                #     # Reference subtraction (same logic as before)
                #     # -----------------------------------------------------------
                #     self.config.print_with_time("🧮[7] Applying reference subtraction")
                #
                #     df_main["ODDO1"] -= self.config.oddo1
                #     df_main["ODDO2"] -= self.config.oddo2
                #     df_main["ROLL"] -= self.config.roll_value
                #     df_main["PITCH"] -= self.config.pitch_value
                #     df_main["YAW"] -= self.config.yaw_value
                #
                #     self.config.print_with_time("📘[8] First-query data prepared")
                #
                #     # -----------------------------------------------------------
                #     # 2️⃣ SECOND QUERY — using Storage API
                #     # -----------------------------------------------------------
                #     self.config.print_with_time("⏳[9] Start building prox-query SQL")
                #
                #     query_for_start = (
                #             "SELECT index, ["
                #             + self.config.sensor_str_prox +
                #             "] AS PROX_DATA "
                #             "FROM " + self.config.table_name + " "
                #                                                "WHERE index>{} AND index<{}"
                #     )
                #
                #     self.config.print_with_time("🚀[10] Start sending prox query (Storage API)")
                #     query_job = client.query(query_for_start.format(start_index, end_index))
                #
                #     self.config.print_with_time("📥[11] Start to_dataframe() for prox query")
                #     results_1 = query_job.to_dataframe(bqstorage_client=bqstorage_client)
                #     self.config.print_with_time(f"📤[12] results_1 fetched → {len(results_1)} rows")
                #
                #     # -----------------------------------------------------------
                #     # Expand PROX_DATA array → prox sensor columns
                #     # -----------------------------------------------------------
                #     self.config.print_with_time("🧩[13] Expanding PROX_DATA")
                #
                #     prox_df = pd.DataFrame(
                #         results_1["PROX_DATA"].tolist(),
                #         columns=self.config.sensor_columns_prox
                #     )
                #     prox_df.insert(0, "index", results_1["index"])
                #     # 🔧 Ensure proximities are in correct index order
                #     prox_df = prox_df.sort_values("index").reset_index(drop=True)
                #
                #     self.config.print_with_time("📘[14] Proximity expansion complete")
                #
                #     # -----------------------------------------------------------
                #     # Keep original variable conventions
                #     # -----------------------------------------------------------
                #     self.config.print_with_time("🔁[15] Restoring original variables")
                #
                #     index_tab9 = df_main["index"].tolist()
                #     index_hm_orientation = results_1["index"].tolist()
                #
                #     df_elem = df_main[["index", "ODDO1", "ROLL", "PITCH", "YAW"]].copy()
                #
                #     self_df_new_proximity_orientat = prox_df[self.config.sensor_columns_prox].copy()
                #
                #     # -----------------------------------------------------------
                #     # Merge (same logic)
                #     # -----------------------------------------------------------
                #     self.config.print_with_time("🔗[16] Merging df_main + prox_df")
                #
                #     df_pipe = df_main.merge(prox_df, on="index", how="inner")
                #
                #     self.config.print_with_time("📘[17] Merge complete")
                #
                #     # -----------------------------------------------------------
                #     # Save pickle (same output as before)
                #     # -----------------------------------------------------------
                #     self.config.print_with_time("💾[18] Saving pickle file")
                #
                #     file_path = folder_path1 + '/' + str(Weld_id_tab9) + '.pkl'
                #     df_pipe.to_pickle(file_path)
                #
                #     self.config.print_with_time(f"✅[19] Saved → {file_path}")
                #
                #     # -----------------------------------------------------------
                #     # Return structure identical to old code
                #     # -----------------------------------------------------------
                #     return {
                #         "file_path": file_path,
                #         "df_pipe": df_pipe,
                #         "index_tab9": index_tab9,
                #         "index_hm_orientation": index_hm_orientation,
                #         "df_elem": df_elem,
                #         "df_new_proximity_orientat": self_df_new_proximity_orientat,
                #     }
                def fetch_tab4_data_fast(self, start_index, end_index, folder_path, weld_id):
                    """
                    EXACT old Tab-4 logic, but using BigQuery Storage API for speed.
                    Output is IDENTICAL to your old code.
                    """

                    self.config.print_with_time("Start fetching at : ")

                    # -----------------------------------------------------------
                    # AUTH + shared Storage API client
                    # -----------------------------------------------------------
                    credentials = service_account.Credentials.from_service_account_file(
                        "./utils/Authorization.json",
                        scopes=[
                            "https://www.googleapis.com/auth/cloud-platform",
                            "https://www.googleapis.com/auth/bigquery",
                            "https://www.googleapis.com/auth/bigquery.readonly",
                        ]
                    )

                    if not hasattr(self, "_bqstorage_client") or self._bqstorage_client is None:
                        self._bqstorage_client = bigquery_storage_v1.BigQueryReadClient(credentials=credentials)

                    bqstorage_client = self._bqstorage_client
                    client = self.config.client

                    # -----------------------------------------------------------
                    # 1️⃣ FIRST QUERY — HALL DATA
                    # -----------------------------------------------------------
                    query_1 = (
                            "SELECT index, ROLL, ODDO1, ODDO2, ["
                            + self.config.sensor_str_hall +
                            "] AS HALL_DATA, PITCH, YAW FROM "
                            + self.config.table_name +
                            " WHERE index>{} AND index<{} ORDER BY index"
                    ).format(start_index, end_index)

                    self.config.print_with_time("Sending HALL query…")
                    df_main = client.query(query_1).to_dataframe(bqstorage_client=bqstorage_client)
                    df_main = df_main.sort_values("index").reset_index(drop=True)

                    self.config.print_with_time(f"HALL rows fetched → {len(df_main)}")

                    # Extract lists EXACTLY like your old code did
                    index_t4 = df_main["index"].tolist()
                    oddo_1 = df_main["ODDO1"].tolist()
                    oddo_2 = df_main["ODDO2"].tolist()
                    roll1 = df_main["ROLL"].tolist()
                    pitch1 = df_main["PITCH"].tolist()
                    yaw1 = df_main["YAW"].tolist()
                    hall_arrays = df_main["HALL_DATA"].tolist()

                    # Reference subtraction (same logic as old)
                    oddo1_t4 = [(v - self.config.oddo1) for v in oddo_1]
                    oddo2_t4 = [(v - self.config.oddo2) for v in oddo_2]
                    roll_t4 = [(v - self.config.roll_value) for v in roll1]
                    pitch_t4 = [(v - self.config.pitch_value) for v in pitch1]
                    yaw_t4 = [(v - self.config.yaw_value) for v in yaw1]

                    # Expand HALL arrays → df_new_t4
                    hall_cols = [
                        f'F{i}H{j}'
                        for i in range(1, self.config.F_columns + 1)
                        for j in range(1, 5)
                    ]
                    df_new_t4 = pd.DataFrame(hall_arrays, columns=hall_cols)

                    # df_elem (exact same structure as old code)
                    df_elem = pd.DataFrame({
                        "index": index_t4,
                        "ODDO1": oddo_1,  # RAW ODDO1 (old behavior)
                        "ROLL": roll_t4,
                        "PITCH": pitch_t4,
                        "YAW": yaw_t4
                    })

                    # -----------------------------------------------------------
                    # 2️⃣ SECOND QUERY — PROX DATA
                    # -----------------------------------------------------------
                    query_2 = (
                            "SELECT index, ["
                            + self.config.sensor_str_prox +
                            "] AS PROX_DATA FROM "
                            + self.config.table_name +
                            " WHERE index>{} AND index<{} ORDER BY index"
                    ).format(start_index, end_index)

                    self.config.print_with_time("Sending PROX query…")
                    df_prox = client.query(query_2).to_dataframe(bqstorage_client=bqstorage_client)
                    df_prox = df_prox.sort_values("index").reset_index(drop=True)

                    self.config.print_with_time(f"PROX rows fetched → {len(df_prox)}")

                    prox_arrays = df_prox["PROX_DATA"].tolist()

                    df_new_proximity_lc = pd.DataFrame(
                        prox_arrays,
                        columns=self.config.sensor_columns_prox
                    )
                    df_new_proximity_lc.insert(0, "index", df_prox["index"].tolist())

                    # -----------------------------------------------------------
                    # MERGE SAFELY (NO join='inner')
                    # Row alignment is POSITIONAL to avoid Storage API quirks
                    # -----------------------------------------------------------
                    df_pipe = pd.concat(
                        [df_elem.reset_index(drop=True),
                         df_new_t4.reset_index(drop=True)],
                        axis=1
                    )

                    # Attach PROX columns (also align by row position)
                    df_new_proximity_lc = df_new_proximity_lc.reset_index(drop=True)

                    for col in df_new_proximity_lc.columns:
                        if col != "index":
                            df_pipe[col] = df_new_proximity_lc[col]

                    # -----------------------------------------------------------
                    # FINAL GUARANTEED index column (NO CRASH, ALWAYS PRESENT)
                    # -----------------------------------------------------------
                    if "index" in df_pipe.columns:
                        df_pipe["index"] = index_t4[:len(df_pipe)]
                    else:
                        df_pipe.insert(0, "index", index_t4[:len(df_pipe)])

                    # -----------------------------------------------------------
                    # SAVE PKL
                    # -----------------------------------------------------------
                    file_path = folder_path + '/' + str(weld_id) + '.pkl'
                    df_pipe.to_pickle(file_path)

                    self.config.print_with_time("Successfully saved pickle file")
                    self.config.print_with_time("End fetching at : ")

                    return {
                        "df_pipe": df_pipe,
                        "df_elem": df_elem,
                        "df_new_t4": df_new_t4,
                        "df_new_proximity_lc": df_new_proximity_lc,
                        "file_path": file_path,
                        "index_t4": index_t4
                    }

                self.config.print_with_time("STARTING FETCHING AT : ")
                result = fetch_tab4_data_fast(self, start_index, end_index, folder_path, weld_id)
                self.config.print_with_time("ENDING FETCHING AT : ")

                self.config.print_with_time("starting plotting at : ")
                df_pipe = result["df_pipe"]
                plot_linechart_sensor(self, df_pipe)
                self.config.print_with_time("Ending plotting at : ")
        else:
            self.config.print_with_time("No data found for this pipe ID : ")



