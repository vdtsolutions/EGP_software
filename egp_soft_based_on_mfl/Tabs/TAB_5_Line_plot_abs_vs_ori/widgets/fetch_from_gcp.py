import numpy as np
import pandas as pd
from google.cloud import bigquery, bigquery_storage_v1
from google.oauth2 import service_account

from egp_soft_based_on_mfl.Components.Configs import config_universal

try:
    from google.cloud.bigquery_storage_v1 import BigQueryReadClient
except ImportError:
    # fallback for environments where Pycharm uses wrong interpreter
    import importlib
    BigQueryReadClient = importlib.import_module(
        "google.cloud.bigquery_storage_v1"
    ).BigQueryReadClient

def fetch_orientation_df_from_gcp(self, result,table_name=None):
    """
    FAST BigQuery Storage API version of Tab-5 orientation fetch.
    Rebuilds df_new from GCP using exact old logic.
    """
    client = self.config.client
    config_universal.print_with_time("Fetching Tab-5 orientation from GCP...")

    # -----------------------------------------------------------
    # Validate input weld rows
    # -----------------------------------------------------------
    if not result or len(result) < 2:
        config_universal.print_with_time("❌ Not enough weld rows to determine start/end indices.")
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
    config_universal.print_with_time("Sending orientation query...")

    df_main = client.query(query_sql).to_dataframe(bqstorage_client=bqstorage_client)
    df_main = df_main.sort_values("index").reset_index(drop=True)

    config_universal.print_with_time(f"Orientation rows fetched → {len(df_main)}")

    if df_main.empty:
        config_universal.print_with_time("⚠️ No rows returned from GCP for orientation.")
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
