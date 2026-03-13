import os

import pandas as pd
from google.cloud import bigquery, bigquery_storage_v1
from egp_soft_based_on_mfl.Components.Configs import config_universal
from egp_soft_based_on_mfl.utils.loaderdialog.loader_dialog import BaseWorker
from google.oauth2 import service_account
try:
    from google.cloud.bigquery_storage_v1 import BigQueryReadClient
except ImportError:
    # fallback for environments where Pycharm uses wrong interpreter
    import importlib
    BigQueryReadClient = importlib.import_module(
        "google.cloud.bigquery_storage_v1"
    ).BigQueryReadClient

class LineChart1Worker(BaseWorker):

    def __init__(self, tab):
        super().__init__()
        self.tab = tab

    def run(self):

        tab = self.tab

        runid = tab.parent.runid
        weld_id = tab.combo.currentText()

        tab.parent.weld_id = int(weld_id)
        p = tab.parent.project_name

        self.smooth_progress(0, 10, "Checking weld data...")

        with tab.config.connection.cursor() as cursor:

            query = """
            SELECT start_index, end_index,start_oddo1,end_oddo1
            FROM welds
            WHERE runid=%s AND id IN (%s,
            (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s))
            ORDER BY id
            """

            cursor.execute(query, (runid, tab.parent.weld_id, runid, tab.parent.weld_id))
            result = cursor.fetchall()

            if not result:
                self.finished.emit(None)
                return

            path = (
                config_universal.weld_pipe_pkl
                + tab.parent.project_name
                + '/'
                + str(weld_id)
                + '.pkl'
            )

            if os.path.isfile(path):

                config_universal.print_with_time("File exist")
                df_pipe = pd.read_pickle(path)

                self.progress.emit(90)

                self.finished.emit(df_pipe)
                return

            folder_path = config_universal.weld_pipe_pkl + tab.parent.project_name

            os.makedirs(folder_path, exist_ok=True)

            start_index, end_index = result[0][0], result[1][1]

            self.smooth_progress(10, 40, "Fetching BigQuery data...")

            result_fetch = self.fetch_tab4_data_fast(
                start_index,
                end_index,
                folder_path,
                weld_id
            )

            df_pipe = result_fetch["df_pipe"]

            self.progress.emit(90)

            self.finished.emit(df_pipe)

    def fetch_tab4_data_fast(self, start_index, end_index, folder_path, weld_id):

        tab = self.tab

        config_universal.print_with_time("Start fetching at : ")

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
        client = tab.config.client

        # -----------------------------------------------------------
        # 1️⃣ HALL QUERY
        # -----------------------------------------------------------

        query_1 = (
                "SELECT index, ROLL, ODDO1, ODDO2, ["
                + tab.config.sensor_str_hall +
                "] AS HALL_DATA, PITCH, YAW FROM "
                + tab.config.table_name +
                " WHERE index>{} AND index<{} ORDER BY index"
        ).format(start_index, end_index)

        df_main = client.query(query_1).to_dataframe(bqstorage_client=bqstorage_client)
        df_main = df_main.sort_values("index").reset_index(drop=True)

        index_t4 = df_main["index"].tolist()
        oddo_1 = df_main["ODDO1"].tolist()
        roll1 = df_main["ROLL"].tolist()
        pitch1 = df_main["PITCH"].tolist()
        yaw1 = df_main["YAW"].tolist()

        hall_arrays = df_main["HALL_DATA"].tolist()

        oddo1_t4 = [(v - tab.config.oddo1) for v in oddo_1]
        roll_t4 = [(v - tab.config.roll_value) for v in roll1]
        pitch_t4 = [(v - tab.config.pitch_value) for v in pitch1]
        yaw_t4 = [(v - tab.config.yaw_value) for v in yaw1]

        hall_cols = [
            f'F{i}H{j}'
            for i in range(1, tab.config.F_columns + 1)
            for j in range(1, 5)
        ]

        df_new_t4 = pd.DataFrame(hall_arrays, columns=hall_cols)

        df_elem = pd.DataFrame({
            "index": index_t4,
            "ODDO1": oddo1_t4,
            "ROLL": roll_t4,
            "PITCH": pitch_t4,
            "YAW": yaw_t4
        })

        # -----------------------------------------------------------
        # 2️⃣ PROX QUERY
        # -----------------------------------------------------------

        query_2 = (
                "SELECT index, ["
                + tab.config.sensor_str_prox +
                "] AS PROX_DATA FROM "
                + tab.config.table_name +
                " WHERE index>{} AND index<{} ORDER BY index"
        ).format(start_index, end_index)

        df_prox = client.query(query_2).to_dataframe(bqstorage_client=bqstorage_client)
        df_prox = df_prox.sort_values("index").reset_index(drop=True)

        prox_arrays = df_prox["PROX_DATA"].tolist()

        df_new_proximity_lc = pd.DataFrame(
            prox_arrays,
            columns=tab.config.sensor_columns_prox
        )

        df_new_proximity_lc.insert(0, "index", df_prox["index"].tolist())

        # -----------------------------------------------------------
        # MERGE DATA
        # -----------------------------------------------------------

        df_pipe = pd.concat(
            [df_elem.reset_index(drop=True),
             df_new_t4.reset_index(drop=True)],
            axis=1
        )

        df_new_proximity_lc = df_new_proximity_lc.reset_index(drop=True)

        for col in df_new_proximity_lc.columns:
            if col != "index":
                df_pipe[col] = df_new_proximity_lc[col]

        # -----------------------------------------------------------
        # FINAL INDEX SAFETY
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

        config_universal.print_with_time("Successfully saved pickle file")
        config_universal.print_with_time("End fetching at : ")

        return {
            "df_pipe": df_pipe,
            "df_elem": df_elem,
            "df_new_t4": df_new_t4,
            "df_new_proximity_lc": df_new_proximity_lc,
            "file_path": file_path,
            "index_t4": index_t4
        }


