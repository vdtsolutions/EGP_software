import os

import numpy as np
import pandas as pd
from google.cloud import bigquery_storage_v1, bigquery
from google.oauth2 import service_account
try:
    from google.cloud.bigquery_storage_v1 import BigQueryReadClient
except ImportError:
    # fallback for environments where Pycharm uses wrong interpreter
    import importlib
    BigQueryReadClient = importlib.import_module(
        "google.cloud.bigquery_storage_v1"
    ).BigQueryReadClient


    # Source & table configuration
source_dataset_id = 'Egp_26inch_processed_data'
source_table_id = 'Egp_26_copy_x1'
project_id = 'quantum-theme-334609'
table_name = f"{project_id}.{source_dataset_id}.{source_table_id}"

credentials = service_account.Credentials.from_service_account_file(r'D:\Anubhav\EGP_software\EGP_software\egp_soft_based_on_mfl\utils\Authorization.json')
client = bigquery.Client(credentials=credentials, project=project_id)


# start_index = 25000
# end_index = 26000
selected_inch = 26
runid = 1
# pipe_id = 1
folder_path1 = r"D:\Anubhav\data_egp\circular_dent_maker\modular_maker\data_pkl"
folder_path = r"D:\Anubhav\data_egp\circular_dent_maker\modular_maker\data_clock"
os.makedirs(folder_path, exist_ok=True)
# Weld_id_tab9 = 2
oddo1 = 1029.4711
oddo2 = 0
roll_value = -17.08
pitch_value = -1.15
yaw_value = 75.91
num_of_sensors = 48
F_columns = int(num_of_sensors / 4)

sensor_columns_hall_sensor = [
    f"F{i}H{j}" for i in range(1, F_columns + 1) for j in range(1, 4 + 1)
]
sensor_str_hall = ", ".join(sensor_columns_hall_sensor)

sensor_columns_prox = [
    f"F{i}P{((i - 1) % 4) + 1}" for i in range(1, F_columns + 1)
]
sensor_str_prox = ", ".join(sensor_columns_prox)

positive_sigma_col = 1.70
positive_sigma_row = 0.45
negative_sigma = 3
defect_box_thresh = 0.25


minute = 720 / num_of_sensors
degree = minute / 2

oddo1_ref = oddo1


def fetch_gcp_data_combined_strict(
    client,
    start_index,
    end_index,

    # ---- CSV params (UNCHANGED) ----
    selected_inch,
    runid,
    pipe_id,

    # ---- TAB9 params (UNCHANGED) ----
    folder_path1,
    Weld_id_tab9,

    # ---- BigQuery ----

):
    """
    STRICT combination of:
    - fetch_gcp_data_by_index_range
    - fetch_and_save_tab9_data

    NO LOGIC CHANGES.
    """

    # --------------------------------------------------
    # Credentials
    # --------------------------------------------------
    credentials = service_account.Credentials.from_service_account_file(
        r"/egp_soft_based_on_mfl/utils/Authorization.json",
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/bigquery",
            "https://www.googleapis.com/auth/bigquery.readonly",
        ]
    )
    bqstorage_client = BigQueryReadClient(credentials=credentials)

    # ==================================================
    # 🔹 PART 1 — EXACT CSV FUNCTION
    # ==================================================
    csv_query = (
        "SELECT * "
        "FROM " + table_name + " "
        "WHERE index > {} AND index < {} "
        "ORDER BY index"
    )

    df_csv = client.query(
        csv_query.format(start_index, end_index)
    ).to_dataframe(bqstorage_client=bqstorage_client)

    base_dir = "fetched_data"
    save_dir = os.path.join(
        base_dir,
        f"inch={selected_inch}",
        f"runid={runid}"
    )
    os.makedirs(save_dir, exist_ok=True)

    csv_file_name = f"runid_{runid}_pipeid_{pipe_id}.csv"
    csv_file_path = os.path.join(save_dir, csv_file_name)

    df_csv.to_csv(csv_file_path, index=False)

    # ==================================================
    # 🔹 PART 2 — EXACT TAB9 FUNCTION
    # ==================================================

    # ---------- First query
    hall_query = (
        "SELECT index, ROLL, ODDO1, ODDO2, ["
        + sensor_str_hall +
        "] AS HALL_DATA, PITCH, YAW "
        "FROM " + table_name + " "
        "WHERE index>{} AND index<{}"
    )

    results = client.query(
        hall_query.format(start_index, end_index)
    ).to_dataframe(bqstorage_client=bqstorage_client)

    df_main = results.sort_values("index").reset_index(drop=True)

    hall_cols = [
        f"F{i}H{j}"
        for i in range(1, F_columns + 1)
        for j in range(1, 5)
    ]
    df_hall = pd.DataFrame(df_main["HALL_DATA"].tolist(), columns=hall_cols)
    df_main = pd.concat([df_main.drop(columns="HALL_DATA"), df_hall], axis=1)

    # Reference subtraction (IDENTICAL)
    df_main["ODDO1"] -= oddo1
    df_main["ODDO2"] -= oddo2
    df_main["ROLL"] -= roll_value
    df_main["PITCH"] -= pitch_value
    df_main["YAW"] -= yaw_value

    # ---------- Second query
    prox_query = (
        "SELECT index, ["
        + sensor_str_prox +
        "] AS PROX_DATA "
        "FROM " + table_name + " "
        "WHERE index>{} AND index<{}"
    )

    results_1 = client.query(
        prox_query.format(start_index, end_index)
    ).to_dataframe(bqstorage_client=bqstorage_client)

    prox_df = pd.DataFrame(
        results_1["PROX_DATA"].tolist(),
        columns=sensor_columns_prox
    )
    prox_df.insert(0, "index", results_1["index"])
    prox_df = prox_df.sort_values("index").reset_index(drop=True)

    # ---------- REQUIRED outputs (UNCHANGED)
    index_tab9 = df_main["index"].tolist()
    index_hm_orientation = results_1["index"].tolist()

    df_elem = df_main[["index", "ODDO1", "ROLL", "PITCH", "YAW"]].copy()
    df_new_proximity_orientat = prox_df[sensor_columns_prox].copy()

    df_pipe = df_main.merge(prox_df, on="index", how="inner")

    # ---------- Save PKL
    os.makedirs(folder_path1, exist_ok=True)
    pkl_path = os.path.join(folder_path1, f"{Weld_id_tab9}.pkl")
    df_pipe.to_pickle(pkl_path)

    # ==================================================
    # ✅ RETURN = UNION OF BOTH ORIGINAL RETURNS
    # ==================================================
    return {
        # CSV side
        "csv_file_path": csv_file_path,
        "csv_rows_fetched": len(df_csv),
        "csv_dataframe": df_csv,

        # TAB9 side
        "pkl_file_path": pkl_path,
        "df_pipe": df_pipe,
        "index_tab9": index_tab9,
        "index_hm_orientation": index_hm_orientation,
        "df_elem": df_elem,
        "df_new_proximity_orientat": df_new_proximity_orientat,
    }


def process_weld_data_to_create_data_array_for_clustering(folder_path1, Weld_id_tab9):
    """
    Generates processed hall & proximity data arrays for clustering
    from the saved weld sensor pickle file (.pkl).

    Performs:
    - data cleaning
    - roll & clock mapping
    - sigma-based hall classification
    - anomaly extraction
    - cluster-ready data array creation
    """

    # Load dataframe from pickle and forward fill
    df = pd.read_pickle(folder_path1 + '/' + str(Weld_id_tab9) + '.pkl')
    data_x = df.fillna(method='ffill')

    # Slice proximity data
    df_new_proximity = pd.DataFrame(
        df,
        columns=sensor_columns_prox
    )

    # Build roll_dictionary and convert to clock words
    roll = data_x['ROLL'].tolist()
    roll1 = []
    for i in roll:
        roll1.append(i)

    roll_dictionary = {'1': roll1}
    angle = [round(i * degree, 1) for i in range(0, num_of_sensors)]

    for i in range(2, num_of_sensors + 1):
        current_values = [round((value + angle[i - 1]), 2) for value in roll1]
        roll_dictionary['{}'.format(i)] = current_values

    clock_dictionary = {}
    for key in roll_dictionary:
        clock_dictionary[key] = [degrees_to_hours_minutes2(value) for value in roll_dictionary[key]]

    Roll_hr = pd.DataFrame(clock_dictionary)
    # Roll_hr.columns = [f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, self.config.minute)]
    Roll_hr.columns = [f"{h:02}:{int(m):02}" for h in range(12) for m in np.arange(0, 60, minute)]

    # odometer in km
    oddometer1 = ((data_x['ODDO1'] - oddo1_ref) / 1000).round(3)

    # Hall sensor frames
    df3_raw = data_x[[f'F{i}H{j}' for i in range(1, F_columns + 1) for j in range(1, 5)]]
    df2 = data_x[
        [f'F{i}H{j}' for i in range(1, F_columns + 1) for j in range(1, 5)]
    ].copy()

    # print("Calculating sigma thresholds using original proven method...")
    mean1 = df2.mean().tolist()
    standard_deviation = df2.std(axis=0, skipna=True).tolist()

    mean_plus_1sigma = []
    for i, data1 in enumerate(mean1):
        sigma1 = data1 + (positive_sigma_col) * standard_deviation[i]
        mean_plus_1sigma.append(sigma1)

    mean_negative_3sigma = []
    for i_2, data_3 in enumerate(mean1):
        sigma_3 = data_3 - (negative_sigma) * standard_deviation[i_2]
        mean_negative_3sigma.append(sigma_3)

    for col, data_col in enumerate(df2.columns):
        df2[data_col] = df2[data_col].apply(
            lambda x: 1 if x > mean_plus_1sigma[col] else (
                -1 if x < mean_negative_3sigma[col] else 0))

    clock_cols = [f"{h:02}:{int(m):02}" for h in range(12) for m in np.arange(0, 60, minute)]
    df2.columns = clock_cols
    filtered_df1 = df2

    # Align raw to classified, multiply to keep signed magnitude
    df3_raw.columns = filtered_df1.columns
    df1_aligned = filtered_df1.reindex(df3_raw.index)
    result = df1_aligned * df3_raw
    result = result.dropna()
    result.reset_index(drop=True, inplace=True)

    result_raw_df = result.mask(result == 0, df3_raw)
    result_raw_df = result_raw_df.dropna()
    result_raw_df.reset_index(drop=True, inplace=True)

    mean_clock_data = result_raw_df.mean().tolist()
    val_ori_raw = ((result_raw_df - mean_clock_data) / mean_clock_data) * 100

    # Build PTT csv-style structure
    ptt_csv = result.copy()
    ptt_csv['ODDO1'] = data_x['ODDO1']
    prefix = '_x'
    for col in Roll_hr.columns:
        ptt_csv[col + prefix] = Roll_hr[col]
    for col in df_new_proximity.columns:
        ptt_csv[col] = df_new_proximity[col]

    # Prep clustering data
    t = result.transpose()
    t_raw = val_ori_raw.transpose()
    data_array = t.to_numpy(dtype=np.float64)

    # return whatever the rest of pipeline uses
    return {
        "df": df,
        "data_x": data_x,
        "df_new_proximity": df_new_proximity,
        "Roll_hr": Roll_hr,
        "oddometer1": oddometer1,
        "result": result,
        "result_raw_df": result_raw_df,
        "val_ori_raw": val_ori_raw,
        "ptt_csv": ptt_csv,
        "t": t,
        "t_raw": t_raw,
        "data_array": data_array,
        "mean1": mean1,
        "standard_deviation": standard_deviation,
        "df_new_proximity": df_new_proximity,
        "Roll_hr": Roll_hr,
        "df3_raw": df3_raw
        }

def degrees_to_hours_minutes2(degrees):
    if (degrees < 0):
        degrees = degrees % 360
    elif degrees >= 360:
        degrees %= 360
    degrees_per_second = 360 / (12 * 60 * 60)
    total_seconds = degrees / degrees_per_second
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{hours:02d}:{minutes:02d}"






def save_clock_pkl(df_elem, result_raw_df, Roll_hr, folder_path, df_new_proximity_orientat, Weld_id_tab9):
    frames = [df_elem, result_raw_df]
    df_new = pd.concat(frames, axis=1, join='inner')

    for col in df_new_proximity_orientat.columns:
        df_new[col] = df_new_proximity_orientat[col]

    for col in Roll_hr.columns:
        df_new[col + '_x'] = Roll_hr[col]

    df_new.to_pickle(folder_path + '/' + str(Weld_id_tab9) + '.pkl')
    # self.config.print_with_time("Succesfully saved to clock pickle file")





# def gcp_fetch_clock():
#     print("running gcp fetch pipeline")
#     result_pkl = fetch_gcp_data_combined_strict(
#         client,
#         start_index,
#         end_index,
#
#         # ---- CSV params (UNCHANGED) ----
#         selected_inch,
#         runid,
#         pipe_id,
#
#         # ---- TAB9 params (UNCHANGED) ----
#         folder_path1,
#         Weld_id_tab9=1
#
#         # ---- BigQuery ----
#
#     )
#     df_elem = result_pkl["df_elem"]
#     df_new_proximity_orientat = result_pkl["df_new_proximity_orientat"]
#
#     processed_data_array = process_weld_data_to_create_data_array_for_clustering(folder_path1, Weld_id_tab9=1)
#     result_raw_df = processed_data_array["result_raw_df"]
#     Roll_hr = processed_data_array["Roll_hr"]
#     save_clock_pkl(df_elem, result_raw_df, Roll_hr, folder_path, df_new_proximity_orientat)

# gcp_fetch_clock()



import os

def gcp_fetch_clock(start_index, end_index, Weld_id_tab9):
    print("▶ running gcp fetch pipeline")
    pipe_id = Weld_id_tab9

    tab9_pkl_path = os.path.join(folder_path1, f"{Weld_id_tab9}.pkl")
    clock_pkl_path = os.path.join(folder_path, f"{Weld_id_tab9}.pkl")

    # --------------------------------------------------
    # STEP 1 — TAB9 PKL (GCP FETCH)
    # --------------------------------------------------
    if os.path.exists(tab9_pkl_path):
        print(f"✅ TAB9 PKL exists → skipping GCP fetch: {tab9_pkl_path}")

        # minimal load to preserve downstream logic
        df_pipe = pd.read_pickle(tab9_pkl_path)

        df_elem = df_pipe[["index", "ODDO1", "ROLL", "PITCH", "YAW"]].copy()
        df_new_proximity_orientat = df_pipe[sensor_columns_prox].copy()

    else:
        print("❌ TAB9 PKL missing → running GCP fetch")

        result_pkl = fetch_gcp_data_combined_strict(
            client,
            start_index,
            end_index,

            # ---- CSV params ----
            selected_inch,
            runid,
            pipe_id,

            # ---- TAB9 params ----
            folder_path1,
            Weld_id_tab9
        )

        df_elem = result_pkl["df_elem"]
        df_new_proximity_orientat = result_pkl["df_new_proximity_orientat"]

    # --------------------------------------------------
    # STEP 2 — CLOCK PKL (PROCESS + SAVE)
    # --------------------------------------------------
    if os.path.exists(clock_pkl_path):
        print(f"✅ CLOCK PKL exists → skipping processing + save: {clock_pkl_path}")
        return

    print("❌ CLOCK PKL missing → processing & saving clock PKL")

    processed_data_array = process_weld_data_to_create_data_array_for_clustering(
        folder_path1,
        Weld_id_tab9
    )

    result_raw_df = processed_data_array["result_raw_df"]
    Roll_hr = processed_data_array["Roll_hr"]

    save_clock_pkl(
        df_elem,
        result_raw_df,
        Roll_hr,
        folder_path,
        df_new_proximity_orientat,
        Weld_id_tab9
    )

    print(f"✅ CLOCK PKL saved at: {clock_pkl_path}")
