import numpy as np
import pandas as pd
from google.cloud import bigquery, bigquery_storage_v1
import json
# from GMFL_12_Inch_Desktop.Components.self.configs import self.config as self.config
#
# connection = self.config.connection
# company_list = []  # list of companies
# credentials = self.config.credentials
# project_id = self.config.project_id
# client = bigquery.Client(credentials=credentials, project=project_id)
# self.config = json.loads(open(r'D:\Anubhav\vdt_backend\GMFL_12_Inch_Desktop\utils\proximity_base_value.json').read())


# def fetch_orientation_df_from_gcp(self, result, client, table_name=None):
#     """
#     Rebuilds df_new from BigQuery for Tab-5 orientation when pickle is missing/corrupt.
#     Uses the same SQL, offsets, HH:MM renaming, and 1400-stagger logic.
#
#     Args:
#         result: rows from the prior welds query (expects at least two rows).
#         client: BigQuery client.
#         table_name: Optional override for self.config.table_name.
#
#     Returns:
#         pd.DataFrame (df_new) with columns: index, ODDO1, ODDO2, and HH:MM (00:00..11:55)
#         or None if nothing fetched.
#     """
#     self.config.print_with_time("Fetching from GCP (pickle missing or corrupt)...")
#
#     if not result or len(result) < 2:
#         self.config.print_with_time("❌ Not enough weld rows to determine start/end indices.")
#         return None
#
#     start_index, end_index = result[0][0], result[1][1]
#     tbl = table_name or self.config.table_name
#
#
#     query_for_start = (
#             "SELECT index,ROLL,ODDO1,ODDO2,["
#             + self.config.sensor_str_hall +
#             f"] FROM {tbl} WHERE index>{start_index} AND index<{end_index} ORDER BY index"
#     )
#
#     query_job = client.query(query_for_start)
#     results = query_job.result()
#
#     data, index_orientation, oddo_1, oddo_2, roll1 = [], [], [], [], []
#     for row in results:
#         index_orientation.append(row[0])
#         roll1.append(row[1])
#         oddo_1.append(row[2])
#         oddo_2.append(row[3])
#         data.append(row[4])
#
#     if not index_orientation:
#         self.config.print_with_time("⚠️ No rows returned from GCP for the requested range.")
#         return None
#
#     oddo1_tab_orientation = [v - self.config.oddo1 for v in oddo_1]
#     oddo2_tab_orientation = [v - self.config.oddo2 for v in oddo_2]
#
#     # Build sensor block -> rename to HH:MM (00:00..11:55), then stagger each column by 1400*i
#     df_new_t5 = pd.DataFrame(data, columns=[f'F{i}H{j}' for i in range(1, self.config.F_columns + 1) for j in range(1, 5)])
#     df_new_t5.columns = [f"{h:02}:{int(m):02}" for h in range(12) for m in np.arange(0, 60, self.config.minute)]
#     for i, col in enumerate(df_new_t5.columns):
#         df_new_t5[col] = df_new_t5[col] + i * 1400
#
#     df_elem = pd.DataFrame({
#         "index": index_orientation,
#         "ODDO1": oddo1_tab_orientation,
#         "ODDO2": oddo2_tab_orientation
#     })
#
#     df_new = pd.concat([df_elem, df_new_t5], axis=1, join='inner')
#     return df_new
from google.oauth2 import service_account
try:
    from google.cloud.bigquery_storage_v1 import BigQueryReadClient
except ImportError:
    # fallback for environments where Pycharm uses wrong interpreter
    import importlib
    BigQueryReadClient = importlib.import_module(
        "google.cloud.bigquery_storage_v1"
    ).BigQueryReadClient

def fetch_orientation_df_from_gcp(self, result, client, table_name=None):
    """
    FAST BigQuery Storage API version of Tab-5 orientation fetch.
    Rebuilds df_new from GCP using exact old logic.
    """

    self.config.print_with_time("Fetching Tab-5 orientation from GCP...")

    # -----------------------------------------------------------
    # Validate input weld rows
    # -----------------------------------------------------------
    if not result or len(result) < 2:
        self.config.print_with_time("❌ Not enough weld rows to determine start/end indices.")
        return None

    start_index, end_index = result[0][0], result[1][1]
    tbl = table_name or self.config.table_name

    # -----------------------------------------------------------
    # STORAGE API AUTH
    # -----------------------------------------------------------
    credentials = service_account.Credentials.from_service_account_file(
        "./utils/Authorization.json",
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/bigquery",
            "https://www.googleapis.com/auth/bigquery.readonly",
        ]
    )

    # Create shared storage client if not present
    if not hasattr(self, "_bqstorage_client") or self._bqstorage_client is None:
        self._bqstorage_client = bigquery_storage_v1.BigQueryReadClient(credentials=credentials)

    bqstorage_client = self._bqstorage_client

    # -----------------------------------------------------------
    # Build QUERY (same SQL as old)
    # -----------------------------------------------------------
    query_sql = (
        "SELECT index, ROLL, ODDO1, ODDO2, ["
        + self.config.sensor_str_hall +
        f"] AS HALL_DATA FROM {tbl} "
        f"WHERE index>{start_index} AND index<{end_index} ORDER BY index"
    )

    # -----------------------------------------------------------
    # Execute using STORAGE API → FAST
    # -----------------------------------------------------------
    self.config.print_with_time("Sending orientation query...")

    df_main = client.query(query_sql).to_dataframe(bqstorage_client=bqstorage_client)
    df_main = df_main.sort_values("index").reset_index(drop=True)

    self.config.print_with_time(f"Orientation rows fetched → {len(df_main)}")

    if df_main.empty:
        self.config.print_with_time("⚠️ No rows returned from GCP for orientation.")
        return None

    # -----------------------------------------------------------
    # Extract original values EXACT like old code
    # -----------------------------------------------------------
    index_orientation = df_main["index"].tolist()
    roll1 = df_main["ROLL"].tolist()
    oddo_1 = df_main["ODDO1"].tolist()
    oddo_2 = df_main["ODDO2"].tolist()
    hall_arrays = df_main["HALL_DATA"].tolist()

    # Reference subtract
    oddo1_tab_orientation = [v - self.config.oddo1 for v in oddo_1]
    oddo2_tab_orientation = [v - self.config.oddo2 for v in oddo_2]

    # -----------------------------------------------------------
    # Build sensor block (same as old)
    # -----------------------------------------------------------
    hall_cols = [
        f'F{i}H{j}'
        for i in range(1, self.config.F_columns + 1)
        for j in range(1, 5)
    ]

    df_new_t5 = pd.DataFrame(hall_arrays, columns=hall_cols)

    # Build HH:MM column names (00:00..11:55)
    hhmm_cols = [
        f"{h:02}:{int(m):02}"
        for h in range(12)
        for m in np.arange(0, 60, self.config.minute)
    ]

    df_new_t5.columns = hhmm_cols

    # Add 1400-stagger
    for i, col in enumerate(df_new_t5.columns):
        df_new_t5[col] = df_new_t5[col] + i * 1400

    # -----------------------------------------------------------
    # Build df_elem
    # -----------------------------------------------------------
    df_elem = pd.DataFrame({
        "index": index_orientation,
        "ODDO1": oddo1_tab_orientation,
        "ODDO2": oddo2_tab_orientation
    })

    # -----------------------------------------------------------
    # SAFE MERGE (positional align)
    # -----------------------------------------------------------
    df_new = pd.concat(
        [df_elem.reset_index(drop=True),
         df_new_t5.reset_index(drop=True)],
        axis=1
    )

    return df_new
