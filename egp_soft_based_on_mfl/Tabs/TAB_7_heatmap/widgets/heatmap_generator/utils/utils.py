import math
import re
import os
import numpy as np
from google.cloud import bigquery_storage_v1
from google.oauth2 import service_account

from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.pipelines.depth_calculation_pipeline import \
    compute_depth
from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.pipelines.dimension_classification import \
    dimension_class
from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.pipelines.internal_or_external import \
    internal_or_external
from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.pipelines.interpolate_data import \
    process_csv_interpolate
from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.pipelines.length_calculation_pipeline import \
    calculate_length_percent
from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.pipelines.orientation_pipeline import \
    get_orientation
from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.pipelines.width_calculation_pipeline import \
    breadth, process_submatrix

try:
    from google.cloud.bigquery_storage_v1 import BigQueryReadClient
except ImportError:
    # fallback for environments where Pycharm uses wrong interpreter
    import importlib
    BigQueryReadClient = importlib.import_module(
        "google.cloud.bigquery_storage_v1"
    ).BigQueryReadClient




# ==========================
# GLOBALS FOR MULTIPROCESSING
# ==========================
G_CONFIG = None
G_RESULT = None
G_DF_CLOCK = None
G_THRESHOLD = None
G_MAX_OF_ALL = None
G_DF3_RAW = None
G_MEAN1 = None
G_DF_NEW_PROX = None
G_ROLL_HR = None
G_PIPE_ID = None
G_RUNID = None
G_WALL_THICKNESS = None
G_PIPE_LEN = None
G_LENGTH_INDEX = None



def init_defect_worker(
    config,
    result, df_clock_holl_oddo1, threshold_value,
    max_of_all, df3_raw, mean1,
    df_new_proximity, Roll_hr,
    pipe_id, runid, wall_thickness,
    pipe_len_oddo1_chm, length_index,
):
    global G_CONFIG, G_RESULT, G_DF_CLOCK, G_THRESHOLD,G_MAX_OF_ALL, G_DF3_RAW, G_MEAN1, G_DF_NEW_PROX, G_ROLL_HR, G_PIPE_ID, G_RUNID, G_WALL_THICKNESS,G_PIPE_LEN, G_LENGTH_INDEX

    G_CONFIG = config
    G_RESULT = result
    G_DF_CLOCK = df_clock_holl_oddo1
    G_THRESHOLD = threshold_value
    G_MAX_OF_ALL = max_of_all
    G_DF3_RAW = df3_raw
    G_MEAN1 = mean1
    G_DF_NEW_PROX = df_new_proximity
    G_ROLL_HR = Roll_hr
    G_PIPE_ID = pipe_id
    G_RUNID = runid
    G_WALL_THICKNESS = wall_thickness
    G_PIPE_LEN = pipe_len_oddo1_chm
    G_LENGTH_INDEX = length_index


def create_folders(self, *paths):
    """
    Create multiple folders safely.

    Parameters
    ----------
    *paths : str
        One or more folder paths to create.

    Example
    -------
    create_folders(folder_path, folder_path1)
    """
    for path in paths:
        try:
            os.makedirs(path)
            self.config.print_with_time(f"Created folder: {path}")
        except FileExistsError:
            self.config.print_with_time(f"Folder already exists: {path}")
        except Exception as e:
            self.config.print_with_time(f"Error creating folder {path}: {e}")



import pandas as pd

# def fetch_and_save_tab9_data(self, client, start_index, end_index, folder_path1, Weld_id_tab9):
#     """
#     This function wraps the original tab9 data fetch, reference adjustment,
#     dataframe build, and pickle save logic into a reusable unit.
#
#     It keeps the same variable names and logging messages as the original code.
#     """
#
#     self.config.print_with_time("Start fetching at : ")
#
#     # query_for_start = (
#     #     'SELECT index,ROLL,ODDO1,ODDO2,[F1H1, F1H2, F1H3, F1H4, F2H1, F2H2, F2H3, F2H4,'
#     #     'F3H1, F3H2, F3H3, F3H4, F4H1, F4H2, F4H3,F4H4, F5H1, F5H2, F5H3, F5H4, '
#     #     'F6H1, F6H2, F6H3, F6H4,F7H1, F7H2, F7H3, F7H4, F8H1, F8H2, F8H3, F8H4, '
#     #     'F9H1, F9H2, F9H3, F9H4, F10H1,F10H2, F10H3, F10H4,F11H1, F11H2, F11H3, F11H4, '
#     #     'F12H1, F12H2, F12H3, F12H4, F13H1, F13H2, F13H3,F13H4, F14H1, F14H2, F14H3, '
#     #     'F14H4,F15H1, F15H2, F15H3, F15H4, F16H1, F16H2, F16H3, F16H4, F17H1, F17H2, '
#     #     'F17H3,F17H4, F18H1, F18H2, F18H3, F18H4,F19H1, F19H2, F19H3, F19H4, '
#     #     'F20H1, F20H2, F20H3, F20H4, F21H1, F21H2, F21H3,F21H4, F22H1, F22H2, F22H3, '
#     #     'F22H4,F23H1, F23H2, F23H3, F23H4, F24H1, F24H2, F24H3, F24H4, '
#     #     'F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, '
#     #     'F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4,'
#     #     'F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, '
#     #     'F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, '
#     #     'F33H1,F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, '
#     #     'F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4], '
#     #     'PITCH, YAW FROM ' + self.config.table_name +
#     #     ' WHERE index>{} AND index<{} order by index'
#     # )
#
#     query_for_start = (
#             "SELECT index, ROLL, ODDO1, ODDO2, ["
#             + self.config.sensor_str_hall +
#             "], PITCH, YAW FROM "
#             + self.config.table_name +
#             " WHERE index>{} AND index<{} ORDER BY index"
#     )
#
#     query_job = client.query(query_for_start.format(start_index, end_index))
#     results = query_job.result()
#
#     self.config.print_with_time("End fetching  at : ")
#
#     data = []
#     index_tab9 = []
#     oddo_1 = []
#     oddo_2 = []
#     indexes = []
#     roll1 = []
#     pitch1 = []
#     yaw1 = []
#
#     self.config.print_with_time("Start of conversion at : ")
#     for row in results:
#         index_tab9.append(row[0])
#         roll1.append(row[1])
#         oddo_1.append(row[2])
#         oddo_2.append(row[3])
#         data.append(row[4])
#         pitch1.append(row[5])
#         yaw1.append(row[6])
#         # indexes.append(ranges(index_of_occurrences(row['frames'], 1)))
#
#     oddo1_tab9 = []
#     oddo2_tab9 = []
#     roll_t = []
#     pitch_t = []
#     yaw_t = []
#
#     """
#     Reference value will be consider
#     """
#     for odometer1 in oddo_1:
#         od1 = odometer1 - self.config.oddo1  ###16984.2 change According to run
#         oddo1_tab9.append(od1)
#     for odometer2 in oddo_2:
#         od2 = odometer2 - self.config.oddo2  ###17690.36 change According to run
#         oddo2_tab9.append(od2)
#
#     """
#     Reference value will be consider
#     """
#     for i in roll1:
#         roll3 = i - self.config.roll_value
#         roll_t.append(roll3)
#     for j in pitch1:
#         pitch3 = j - self.config.pitch_value
#         pitch_t.append(pitch3)
#     for k in yaw1:
#         yaw3 = k - self.config.yaw_value
#         yaw_t.append(yaw3)
#
#     # query_for_start = (
#     #     'SELECT index,[F1P1,F2P2,F3P3,F4P4,F5P1,F6P2,F7P3,F8P4,'
#     #     'F9P1,F10P2,F11P3,F12P4,F13P1,F14P2,F15P3,F16P4,'
#     #     'F17P1,F18P2,F19P3,F20P4,F21P1,F22P2,F23P3,F24P4, '
#     #     'F25P1, F26P2, F27P3, F28P4, F29P1, F30P2, F31P3, F32P4, '
#     #     'F33P1, F34P2, F35P3, F36P4] FROM ' + self.config.table_name +
#     #     ' WHERE index>{} AND index<{} order by index'
#     # )
#     query_for_start = (
#             "SELECT index, ["
#             + self.config.sensor_str_prox +
#             "] FROM "
#             + self.config.table_name +
#             " WHERE index>{} AND index<{} ORDER BY index"
#     )
#
#     query_job = client.query(query_for_start.format(start_index, end_index))
#     results_1 = query_job.result()
#
#     data1 = []
#     index_hm_orientation = []
#     for row1 in results_1:
#         index_hm_orientation.append(row1[0])
#         data1.append(row1[1])
#
#     self_df_new_proximity_orientat = pd.DataFrame(
#         data1,
#         columns=self.config.sensor_columns_prox
#     )
#
#     df_new_tab9 = pd.DataFrame(
#         data,
#         columns=[f'F{i}H{j}' for i in range(1, self.config.F_columns + 1) for j in range(1, 5)]
#     )
#
#     df_elem = pd.DataFrame({
#         "index": index_tab9,
#         "ODDO1": oddo1_tab9,
#         "ROLL": roll_t,
#         "PITCH": pitch_t,
#         "YAW": yaw_t
#     })
#
#     frames = [df_elem, df_new_tab9]
#     df_pipe = pd.concat(frames, axis=1, join='inner')
#
#     for col in self_df_new_proximity_orientat.columns:
#         df_pipe[col] = self_df_new_proximity_orientat[col]
#
#     file_path = folder_path1 + '/' + str(Weld_id_tab9) + '.pkl'
#     df_pipe.to_pickle(file_path)
#     self.config.print_with_time(f"Succesfully saved to sensor pickle file path is: {file_path}")
#
#
#
#     # return things you may still want to use outside
#     return {
#         "file_path": file_path,
#         "df_pipe": df_pipe,
#         "index_tab9": index_tab9,
#         "index_hm_orientation": index_hm_orientation,
#         "df_elem": df_elem,
#         "df_new_proximity_orientat": self_df_new_proximity_orientat
#     }





#optimized version from 90 sec to just 20-25 sec time

def fetch_and_save_tab9_data(self, client, start_index, end_index, folder_path1, Weld_id_tab9):
    """
    Optimized — uses BigQuery Storage API.
    Naming, logic, output = IDENTICAL to old code.
    """
    credentials = service_account.Credentials.from_service_account_file(
        "./utils/Authorization.json",
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/bigquery",
            "https://www.googleapis.com/auth/bigquery.readonly",
        ]
    )

    # -----------------------------------------------------------
    # Init Storage API client ONCE (reuses client each call)
    # -----------------------------------------------------------
    self.config.print_with_time("Start of conversion at : ")
    if not hasattr(self, "_bqstorage_client") or self._bqstorage_client is None:
        self._bqstorage_client = BigQueryReadClient()


    bqstorage_client = bigquery_storage_v1.BigQueryReadClient(credentials=credentials)

    # -----------------------------------------------------------
    # 1️⃣ FIRST QUERY — using Storage API
    # -----------------------------------------------------------
    self.config.print_with_time("⏳[1] Start building first-query SQL")

    query_for_start = (
        "SELECT index, ROLL, ODDO1, ODDO2, ["
        + self.config.sensor_str_hall +
        "] AS HALL_DATA, PITCH, YAW "
        "FROM " + self.config.table_name + " "
        "WHERE index>{} AND index<{}"
    )

    self.config.print_with_time("🚀[2] Start sending first query (Storage API)")
    query_job = client.query(query_for_start.format(start_index, end_index))

    self.config.print_with_time("📥[3] Start to_dataframe() for first query")
    results = query_job.to_dataframe(bqstorage_client=bqstorage_client)
    self.config.print_with_time(f"📤[4] results fetched → {len(results)} rows")

    # df_main starts as copied results (same naming convention)
    self.config.print_with_time("🧱[5] Creating df_main")
    df_main = results.copy()
    # 🔧 Ensure same ordering as old BigQuery Iterator
    df_main = df_main.sort_values("index").reset_index(drop=True)
    # -----------------------------------------------------------
    # Expand HALL_DATA array → F1H1...F36H4
    # -----------------------------------------------------------
    self.config.print_with_time("🧩[6] Expanding HALL_DATA")

    hall_cols = [
        f'F{i}H{j}'
        for i in range(1, self.config.F_columns + 1)
        for j in range(1, 5)
    ]

    df_hall = pd.DataFrame(df_main["HALL_DATA"].tolist(), columns=hall_cols)

    df_main = pd.concat([df_main.drop(columns=["HALL_DATA"]), df_hall], axis=1)

    # -----------------------------------------------------------
    # Reference subtraction (same logic as before)
    # -----------------------------------------------------------
    self.config.print_with_time("🧮[7] Applying reference subtraction")

    df_main["ODDO1"] -= self.config.oddo1
    df_main["ODDO2"] -= self.config.oddo2
    df_main["ROLL"] -= self.config.roll_value
    df_main["PITCH"] -= self.config.pitch_value
    df_main["YAW"] -= self.config.yaw_value

    self.config.print_with_time("📘[8] First-query data prepared")

    # -----------------------------------------------------------
    # 2️⃣ SECOND QUERY — using Storage API
    # -----------------------------------------------------------
    self.config.print_with_time("⏳[9] Start building prox-query SQL")

    query_for_start = (
        "SELECT index, ["
        + self.config.sensor_str_prox +
        "] AS PROX_DATA "
        "FROM " + self.config.table_name + " "
        "WHERE index>{} AND index<{}"
    )

    self.config.print_with_time("🚀[10] Start sending prox query (Storage API)")
    query_job = client.query(query_for_start.format(start_index, end_index))

    self.config.print_with_time("📥[11] Start to_dataframe() for prox query")
    results_1 = query_job.to_dataframe(bqstorage_client=bqstorage_client)
    self.config.print_with_time(f"📤[12] results_1 fetched → {len(results_1)} rows")

    # -----------------------------------------------------------
    # Expand PROX_DATA array → prox sensor columns
    # -----------------------------------------------------------
    self.config.print_with_time("🧩[13] Expanding PROX_DATA")

    prox_df = pd.DataFrame(
        results_1["PROX_DATA"].tolist(),
        columns=self.config.sensor_columns_prox
    )
    prox_df.insert(0, "index", results_1["index"])
    # 🔧 Ensure proximities are in correct index order
    prox_df = prox_df.sort_values("index").reset_index(drop=True)

    self.config.print_with_time("📘[14] Proximity expansion complete")

    # -----------------------------------------------------------
    # Keep original variable conventions
    # -----------------------------------------------------------
    self.config.print_with_time("🔁[15] Restoring original variables")

    index_tab9 = df_main["index"].tolist()
    index_hm_orientation = results_1["index"].tolist()

    df_elem = df_main[["index", "ODDO1", "ROLL", "PITCH", "YAW"]].copy()

    self_df_new_proximity_orientat = prox_df[self.config.sensor_columns_prox].copy()

    # -----------------------------------------------------------
    # Merge (same logic)
    # -----------------------------------------------------------
    self.config.print_with_time("🔗[16] Merging df_main + prox_df")

    df_pipe = df_main.merge(prox_df, on="index", how="inner")

    self.config.print_with_time("📘[17] Merge complete")

    # -----------------------------------------------------------
    # Save pickle (same output as before)
    # -----------------------------------------------------------
    self.config.print_with_time("💾[18] Saving pickle file")

    file_path = folder_path1 + '/' + str(Weld_id_tab9) + '.pkl'
    df_pipe.to_pickle(file_path)

    self.config.print_with_time(f"✅[19] Saved → {file_path}")

    # -----------------------------------------------------------
    # Return structure identical to old code
    # -----------------------------------------------------------
    return {
        "file_path": file_path,
        "df_pipe": df_pipe,
        "index_tab9": index_tab9,
        "index_hm_orientation": index_hm_orientation,
        "df_elem": df_elem,
        "df_new_proximity_orientat": self_df_new_proximity_orientat,
    }




def process_weld_data_to_create_data_array_for_clustering(self, folder_path1, Weld_id_tab9):
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
        columns=self.config.sensor_columns_prox
    )

    # Build roll_dictionary and convert to clock words
    roll = data_x['ROLL'].tolist()
    roll1 = []
    for i in roll:
        roll1.append(i)

    roll_dictionary = {'1': roll1}
    angle = [round(i * self.config.degree, 1) for i in range(0, self.config.num_of_sensors)]

    for i in range(2, self.config.num_of_sensors + 1):
        current_values = [round((value + angle[i - 1]), 2) for value in roll1]
        roll_dictionary['{}'.format(i)] = current_values

    clock_dictionary = {}
    for key in roll_dictionary:
        clock_dictionary[key] = [degrees_to_hours_minutes2(value) for value in roll_dictionary[key]]

    Roll_hr = pd.DataFrame(clock_dictionary)
    # Roll_hr.columns = [f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, self.config.minute)]
    Roll_hr.columns =  [f"{h:02}:{int(m):02}" for h in range(12) for m in np.arange(0, 60, self.config.minute)]

    # odometer in km
    oddometer1 = ((data_x['ODDO1'] - self.config.oddo1_ref) / 1000).round(3)

    # Hall sensor frames
    df3_raw = data_x[[f'F{i}H{j}' for i in range(1, self.config.F_columns + 1) for j in range(1, 5)]]
    df2 = data_x[[f'F{i}H{j}' for i in range(1, self.config.F_columns + 1) for j in range(1, 5)]]

    print("Calculating sigma thresholds using original proven method...")
    mean1 = df2.mean().tolist()
    standard_deviation = df2.std(axis=0, skipna=True).tolist()

    mean_plus_1sigma = []
    for i, data1 in enumerate(mean1):
        sigma1 = data1 + (self.config.positive_sigma_col) * standard_deviation[i]
        mean_plus_1sigma.append(sigma1)

    mean_negative_3sigma = []
    for i_2, data_3 in enumerate(mean1):
        sigma_3 = data_3 - (self.config.negative_sigma) * standard_deviation[i_2]
        mean_negative_3sigma.append(sigma_3)

    for col, data_col in enumerate(df2.columns):
        df2[data_col] = df2[data_col].apply(
            lambda x: 1 if x > mean_plus_1sigma[col] else (
                -1 if x < mean_negative_3sigma[col] else 0))

    clock_cols = [f"{h:02}:{int(m):02}" for h in range(12) for m in np.arange(0, 60, self.config.minute)]
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


# def get_adaptive_sigma_refinement(length_percent):
#     """
#     Get refined sigma multipliers based on 5-part length percentage classification:
#     1-10%, 10-20%, 20-30%, 30-40%, 40%+
#     """
#     if 1 <= length_percent < 10:
#         sigma_multiplier = 0.6  # Less aggressive for very small defects
#         refinement_factor = 1.2
#         classification = "Very Small (1-10%)"
#     elif 10 <= length_percent < 20:
#         sigma_multiplier = 0.5  # Slightly more sensitive for small defects
#         refinement_factor = 0.9
#         classification = "Small (10-20%)"
#     elif 20 <= length_percent < 30:
#         sigma_multiplier = 1  # Standard sensitivity
#         refinement_factor = 1.0
#         classification = "Medium (20-30%)"
#     elif 30 <= length_percent < 40:
#         sigma_multiplier = 1.1  # Slightly less sensitive
#         refinement_factor = 0.9
#         classification = "Large (30-40%)"
#     elif length_percent >= 40:
#         sigma_multiplier = 1.2  # Less sensitive for largest defects
#         refinement_factor = 0.8
#         classification = "Very Large (40%+)"
#     else:
#         sigma_multiplier = 0.85
#         refinement_factor = 1.15
#         classification = "Below 1%"
#     return sigma_multiplier, refinement_factor, classification


# def get_adaptive_sigma_refinement(length_percent):
#     """
#     Get refined sigma multipliers based on 5-part length percentage classification:
#     1-10%, 10-20%, 20-30%, 30-40%, 40%+
#     """
#     if 1 <= length_percent < 10:
#         sigma_multiplier = 0.5  # Less aggressive for very small defects
#         refinement_factor = 0.8
#         classification = "Very Small (1-10%)"
#     elif 10 <= length_percent < 20:
#         sigma_multiplier = 0.8  # Slightly more sensitive for small defects
#         refinement_factor = 0.9
#         classification = "Small (10-20%)"
#     elif 20 <= length_percent < 30:
#         sigma_multiplier = 1.1  # Standard sensitivity
#         refinement_factor = 1.0
#         classification = "Medium (20-30%)"
#     elif 30 <= length_percent < 40:
#         sigma_multiplier = 1.4  # Slightly less sensitive
#         refinement_factor = 0.9
#         classification = "Large (30-40%)"
#     elif length_percent >= 40:
#         sigma_multiplier = 1.6  # Less sensitive for largest defects
#         refinement_factor = 0.8
#         classification = "Very Large (40%+)"
#     else:
#         sigma_multiplier = 0.85
#         refinement_factor = 1.15
#         classification = "Below 1%"
#     return sigma_multiplier, refinement_factor, classification

def extract_int_prefix(s):
    m = re.match(r'^(\d+)', str(s))
    return int(m.group(1)) if m else None


def get_first_last_integer_column(cols):
    int_vals = [extract_int_prefix(col) for col in cols]
    int_vals = [v for v in int_vals if v is not None]
    if not int_vals:
        return None, None
    return min(int_vals), max(int_vals)


def replace_first_column(df_n, s_sensor, e_sensor):
    s_sensor = s_sensor + 1
    e_sensor = e_sensor + 1
    # Generate new column names within the given range
    new_columns = list(range(s_sensor, s_sensor + df_n.shape[1]))
    # Assign new column names
    df_n.columns = new_columns
    # Drop the last column if it exceeds end_sensor
    df_n = df_n.loc[:, df_n.columns <= e_sensor]
    return df_n





def save_clock_pkl(self, df_elem, result_raw_df, Roll_hr, folder_path, df_new_proximity_orientat):
    frames = [df_elem, result_raw_df]
    df_new = pd.concat(frames, axis=1, join='inner')

    for col in df_new_proximity_orientat.columns:
        df_new[col] = df_new_proximity_orientat[col]

    for col in Roll_hr.columns:
        df_new[col + '_x'] = Roll_hr[col]

    df_new.to_pickle(folder_path + '/' + str(self.Weld_id_tab9) + '.pkl')
    self.config.print_with_time("Succesfully saved to clock pickle file")



def defect_summary(finial_defect_list, classification_stats):
    print(f"Total defects found: {len(finial_defect_list)}")
    for classification, stats in classification_stats.items():
        if stats["total_processed"] > 0:
            acceptance_rate = (stats["count"] / stats["total_processed"]) * 100
            print(
                f"{classification}: {stats['count']}/{stats['total_processed']} defects ({acceptance_rate:.1f}% acceptance)")


def process_defects(self, df_sorted, result, df_clock_holl_oddo1, threshold_value, classification_stats,defect_counter
                    , max_of_all, df3_raw, mean1, df_new_proximity, Roll_hr, t, submatrices_dict, finial_defect_list,
                    pipe_id, runid, wall_thickness, figx112):

    for row in df_sorted.itertuples(index=False):

        self.config.print_with_time("Row fetched")

        # start_sensor = row['start_row']
        # end_sensor = row['end_row']
        # start_reading = row['start_col']
        # end_reading = row['end_col']
        start_sensor = row.start_row
        end_sensor = row.end_row
        start_reading = row.start_col
        end_reading = row.end_col

        if start_sensor == end_sensor:
            continue

        try:
            # ---------------------------------------------------------
            self.config.print_with_time("Creating submatrix")
            submatrix = result.iloc[start_reading:end_reading + 1, start_sensor:end_sensor + 1]

            # self.config.print_with_time("Applying to_numeric on submatrix")
            # submatrix = submatrix.apply(pd.to_numeric, errors='coerce')

            # self.config.print_with_time("Computing two_d_list")
            # two_d_list = submatrix.values.tolist()
            #
            # self.config.print_with_time("Calculating max/min")
            # max_value = submatrix.max().max()
            # min_positive = min(x for row in two_d_list for x in row if x > 0)

            self.config.print_with_time("Calculating max/min")
            # max_value stays same
            max_value = submatrix.max().max()

            # FAST vectorized min-positive
            positive_vals = submatrix[submatrix > 0]
            min_positive = positive_vals.min().min()

            # ---------------------------------------------------------
            self.config.print_with_time("Calculating length_percent")
            length_percent, start, end, length = calculate_length_percent(
                df_clock_holl_oddo1=df_clock_holl_oddo1,
                start_reading=start_reading,
                end_reading=end_reading,
                l_per_1=self.config.l_per_1
            )

            # ---------------------------------------------------------
            self.config.print_with_time("Adaptive sigma refinement")
            sigma_multiplier, refinement_factor, classification = \
                self.config.get_adaptive_sigma_refinement(length_percent)
            adjusted_threshold = threshold_value * sigma_multiplier

            # ---------------------------------------------------------
            # self.config.print_with_time("Valid column loop")
            # valid_columns = 0
            # for col_idx in range(start_sensor, end_sensor + 1):
            #     adaptive_sigma = mean1[col_idx] + (sigma_multiplier * standard_deviation[col_idx])
            #     if submatrix.iloc[:, col_idx - start_sensor].max() > adaptive_sigma:
            #         valid_columns += 1
            #
            #     if valid_columns / (end_sensor - start_sensor + 1) < 0.3:
            #         print(
            #             f"✗ Defect rejected: Only {valid_columns} columns passed adaptive threshold")
            #         continue

            classification_stats[classification]["total_processed"] += 1

            # ---------------------------------------------------------
            self.config.print_with_time("Printing defect basic info")
            print(
                f"Defect {defect_counter}: Length={length_percent:.1f}mm, "
                f"Class={classification}, Threshold={adjusted_threshold:.1f}"
            )

            if (adjusted_threshold <= max_value <= max_of_all):
                print(f"✓ Defect accepted with {classification} settings")

                # ---------------------------------------------------------------
                self.config.print_with_time("Calculating depth_old")
                depth_old = (max_value - min_positive) / min_positive * 100

                # ---------------------------------------------------------------
                self.config.print_with_time("Running compute_depth")
                depth_val1, df_copy_submatrix = compute_depth(
                    self,
                    df_raw=df3_raw,
                    start_reading=start_reading,
                    end_reading=end_reading,
                    start_sensor=start_sensor,
                    end_sensor=end_sensor,
                    pipe_thickness=self.config.pipe_thickness,
                )

                self.config.print_with_time("Computing max_index")
                max_column = submatrix.max().idxmax()
                max_index = submatrix.columns.get_loc(max_column)

                # ---------------------------------------------------------------
                self.config.print_with_time("Calculating start/end oddo + speed")
                start_oddo1 = df_clock_holl_oddo1[start_reading]
                end_oddo1 = (df_clock_holl_oddo1[end_reading]) / 1000
                time_sec = end_reading / 1500
                speed = end_oddo1 / time_sec

                base_value = mean1[max_index]

                # ---------------------------------------------------------------
                self.config.print_with_time("Internal/external detection")
                internal_external = internal_or_external(df_new_proximity, max_index)

                # ---------------------------------------------------------------
                self.config.print_with_time("Absolute + upstream distance calc")
                absolute_distance = df_clock_holl_oddo1[start_reading]
                upstream = df_clock_holl_oddo1[start_reading] - df_clock_holl_oddo1[0]

                counter_difference_1 = (end_sensor + 1) - (start_sensor + 1)
                divid_1 = int(counter_difference_1 / 2)
                center_1 = start_sensor + divid_1
                factor1_1 = divid_1 * self.config.w_per_1

                start1_1 = (int(center_1 - factor1_1)) - 1
                end1_1 = (int(center_1 + factor1_1)) - 1

                # ---------------------------------------------------------------
                self.config.print_with_time("Breadth() initial width calc")
                width = breadth(self, start_sensor, end_sensor)

                # ---------------------------------------------------------------
                self.config.print_with_time("Dimension classification")
                dimension_classification = dimension_class(self.config.pipe_thickness, length, width)

                # ---------------------------------------------------------------
                self.config.print_with_time("Orientation calculation")
                orientation = get_orientation(Roll_hr, start, end, start1_1, end1_1)

                inner_diameter = self.config.outer_dia - 2 * self.config.pipe_thickness
                radius = inner_diameter / 2
                x1 = round(radius * math.radians(self.config.theta_ang1), 1)
                y1 = round(radius * math.radians(self.config.theta_ang2), 1)
                z1 = round(radius * math.radians(self.config.theta_ang3), 1)

            # ---------------------------------------------------------
            self.config.print_with_time("Replace first column")
            df_duplicate = replace_first_column(df_copy_submatrix, start_sensor, end_sensor)
            df_duplicate.columns = df_duplicate.columns.astype(str)

            # ---------------------------------------------------------
            self.config.print_with_time("Interpolating modified df")
            modified_df = process_csv_interpolate(self, df_duplicate, x1, y1, z1)

            # ---------------------------------------------------------
            self.config.print_with_time("Running process_submatrix")
            trimmed_matrix, width_1_only, width_0_yes, new_start_sensor, new_end_sensor = \
                process_submatrix(self, modified_df, start1_1, end1_1)

            new_start_sensor, new_end_sensor = get_first_last_integer_column(trimmed_matrix.columns)

            # ---------------------------------------------------------
            mapped_start_sensor = len(t.index) - start_sensor
            mapped_end_sensor = len(t.index) - end_sensor

            if mapped_end_sensor < mapped_start_sensor:
                mapped_start_sensor, mapped_end_sensor = mapped_end_sensor, mapped_start_sensor

            # ---------------------------------------------------------
            self.config.print_with_time("Breadth() final width calc")
            width = breadth(self, mapped_start_sensor, mapped_end_sensor)

            # ---------------------------------------------------------
            self.config.print_with_time("Depth rounding calculation")
            try:
                depth_val = round(
                    (((length / width) * (max_value / base_value)) * 100) / self.config.pipe_thickness
                )
            except:
                depth_val = 0

            if depth_val > 1 and width > 1 and length > 1:
                classification_stats[classification]["count"] += 1
                submatrices_dict[(defect_counter, start_sensor, end_sensor)] = modified_df

                print(f"✓ Valid defect: depth={depth_val}%, width={width}mm, length={length}mm")

                # ---------------------------------------------------------
                self.config.print_with_time("Appending defect to list")
                finial_defect_list.append({
                    "pipe_id": pipe_id,
                    "runid": runid,
                    "defect_id": defect_counter,
                    "start_reading": start_reading,
                    "end_reading": end_reading,
                    "start_sensor": start_sensor,
                    "end_sensor": end_sensor,
                    "absolute_distance": absolute_distance,
                    "upstream": upstream,
                    "length": length,
                    "length_percent": length_percent,
                    "breadth": width,
                    "width_new2": round(width_1_only, 0),
                    "orientation": orientation,
                    "defect_type": internal_external,
                    "dimension_classification": dimension_classification,
                    "depth": depth_val1,
                    "depth_old": depth_old,
                    "start_oddo1": start_oddo1,
                    "end_oddo1": end_oddo1,
                    "speed": speed,
                    "Min_Val": min_positive,
                    "Max_Val": max_value,
                    "wall_thickness": wall_thickness,
                    "pipe_length": self.pipe_len_oddo1_chm
                })

                # ---------------------------------------------------------
                self.config.print_with_time("Adding heatmap annotation + rectangle")
                if classification == "Very Small (1-10%)":
                    color = 'purple'
                elif classification == "Small (10-20%)":
                    color = 'red'
                elif classification == "Medium (20-30%)":
                    color = 'orange'
                elif classification == "Large (30-40%)":
                    color = 'yellow'
                elif classification == "Very Large (40%+)":
                    color = 'blue'
                else:
                    color = 'gray'

                figx112.add_shape(
                    type='rect',
                    x0=start_reading - 0.5,
                    x1=end_reading + 0.5,
                    y0=start_sensor - 0.5,
                    y1=end_sensor + 0.5,
                    line=dict(color=color, width=2),
                    fillcolor=f'rgba(255, 0, 0, 0.2)'
                )

                figx112.add_annotation(
                    x=(start_reading + end_reading) / 2,
                    y=start_sensor - 1,
                    text=f"{defect_counter}({classification.split()[0]})",
                    showarrow=False,
                    font=dict(color=color, size=10),
                    bgcolor="white",
                    bordercolor="black",
                    borderwidth=1
                )

                defect_counter += 1
            else:
                print(f"✗ Defect rejected: max_value={max_value} vs threshold={adjusted_threshold}")

        except Exception as e:
            print(f"Error processing defect: {str(e)}")
            continue








def process_single_defect(self,config, result, df_clock_holl_oddo1, threshold_value, classification_stats,defect_counter
                    , max_of_all, df3_raw, mean1, df_new_proximity, Roll_hr, t, submatrices_dict, finial_defect_list,
                    pipe_id, runid, wall_thickness, figx112, row):
        print("processing single defect at a time")
        self.config.print_with_time("Row fetched")

        # start_sensor = row['start_row']
        # end_sensor = row['end_row']
        # start_reading = row['start_col']
        # end_reading = row['end_col']
        start_sensor = row.start_row
        end_sensor = row.end_row
        start_reading = row.start_col
        end_reading = row.end_col

        if start_sensor == end_sensor:
            return None

        try:
            # ---------------------------------------------------------
            self.config.print_with_time("Creating submatrix")
            submatrix = result.iloc[start_reading:end_reading + 1, start_sensor:end_sensor + 1]

            # self.config.print_with_time("Applying to_numeric on submatrix")
            # submatrix = submatrix.apply(pd.to_numeric, errors='coerce')

            # self.config.print_with_time("Computing two_d_list")
            # two_d_list = submatrix.values.tolist()
            #
            # self.config.print_with_time("Calculating max/min")
            # max_value = submatrix.max().max()
            # min_positive = min(x for row in two_d_list for x in row if x > 0)

            self.config.print_with_time("Calculating max/min")
            # max_value stays same
            max_value = submatrix.max().max()

            # FAST vectorized min-positive
            positive_vals = submatrix[submatrix > 0]
            min_positive = positive_vals.min().min()

            # ---------------------------------------------------------
            self.config.print_with_time("Calculating length_percent")
            length_percent, start, end, length = calculate_length_percent(
                df_clock_holl_oddo1=df_clock_holl_oddo1,
                start_reading=start_reading,
                end_reading=end_reading,
                l_per_1=self.config.l_per_1
            )

            # ---------------------------------------------------------
            self.config.print_with_time("Adaptive sigma refinement")
            sigma_multiplier, refinement_factor, classification = \
                self.config.get_adaptive_sigma_refinement(length_percent)
            adjusted_threshold = threshold_value * sigma_multiplier

            # ---------------------------------------------------------
            # self.config.print_with_time("Valid column loop")
            # valid_columns = 0
            # for col_idx in range(start_sensor, end_sensor + 1):
            #     adaptive_sigma = mean1[col_idx] + (sigma_multiplier * standard_deviation[col_idx])
            #     if submatrix.iloc[:, col_idx - start_sensor].max() > adaptive_sigma:
            #         valid_columns += 1
            #
            #     if valid_columns / (end_sensor - start_sensor + 1) < 0.3:
            #         print(
            #             f"✗ Defect rejected: Only {valid_columns} columns passed adaptive threshold")
            #         continue

            classification_stats[classification]["total_processed"] += 1

            # ---------------------------------------------------------
            self.config.print_with_time("Printing defect basic info")
            print(
                f"Defect {defect_counter}: Length={length_percent:.1f}mm, "
                f"Class={classification}, Threshold={adjusted_threshold:.1f}"
            )

            if (adjusted_threshold <= max_value <= max_of_all):
                print(f"✓ Defect accepted with {classification} settings")

                # ---------------------------------------------------------------
                self.config.print_with_time("Calculating depth_old")
                depth_old = (max_value - min_positive) / min_positive * 100

                # ---------------------------------------------------------------
                self.config.print_with_time("Running compute_depth")
                depth_val1, df_copy_submatrix = compute_depth(
                    config,
                    df_raw=df3_raw,
                    start_reading=start_reading,
                    end_reading=end_reading,
                    start_sensor=start_sensor,
                    end_sensor=end_sensor,
                    pipe_thickness=self.config.pipe_thickness,
                )

                self.config.print_with_time("Computing max_index")
                max_column = submatrix.max().idxmax()
                max_index = submatrix.columns.get_loc(max_column)

                # ---------------------------------------------------------------
                self.config.print_with_time("Calculating start/end oddo + speed")
                start_oddo1 = df_clock_holl_oddo1[start_reading]
                end_oddo1 = (df_clock_holl_oddo1[end_reading]) / 1000
                time_sec = end_reading / 1500
                speed = end_oddo1 / time_sec

                base_value = mean1[max_index]

                # ---------------------------------------------------------------
                self.config.print_with_time("Internal/external detection")
                internal_external = internal_or_external(df_new_proximity, max_index)

                # ---------------------------------------------------------------
                self.config.print_with_time("Absolute + upstream distance calc")
                absolute_distance = df_clock_holl_oddo1[start_reading]
                upstream = df_clock_holl_oddo1[start_reading] - df_clock_holl_oddo1[0]

                counter_difference_1 = (end_sensor + 1) - (start_sensor + 1)
                divid_1 = int(counter_difference_1 / 2)
                center_1 = start_sensor + divid_1
                factor1_1 = divid_1 * self.config.w_per_1

                start1_1 = (int(center_1 - factor1_1)) - 1
                end1_1 = (int(center_1 + factor1_1)) - 1

                # ---------------------------------------------------------------
                self.config.print_with_time("Breadth() initial width calc")
                width = breadth(config, start_sensor, end_sensor)

                # ---------------------------------------------------------------
                self.config.print_with_time("Dimension classification")
                dimension_classification = dimension_class(self.config.pipe_thickness, length, width)

                # ---------------------------------------------------------------
                self.config.print_with_time("Orientation calculation")
                orientation = get_orientation(Roll_hr, start, end, start1_1, end1_1)

                inner_diameter = self.config.outer_dia - 2 * self.config.pipe_thickness
                radius = inner_diameter / 2
                x1 = round(radius * math.radians(self.config.theta_ang1), 1)
                y1 = round(radius * math.radians(self.config.theta_ang2), 1)
                z1 = round(radius * math.radians(self.config.theta_ang3), 1)

            # ---------------------------------------------------------
            self.config.print_with_time("Replace first column")
            df_duplicate = replace_first_column(df_copy_submatrix, start_sensor, end_sensor)
            df_duplicate.columns = df_duplicate.columns.astype(str)

            # ---------------------------------------------------------
            self.config.print_with_time("Interpolating modified df")
            modified_df = process_csv_interpolate(config, df_duplicate, x1, y1, z1)

            # ---------------------------------------------------------
            self.config.print_with_time("Running process_submatrix")
            trimmed_matrix, width_1_only, width_0_yes, new_start_sensor, new_end_sensor = \
                process_submatrix(config, modified_df, start1_1, end1_1)

            # new_start_sensor, new_end_sensor = get_first_last_integer_column(trimmed_matrix.columns)

            # ---------------------------------------------------------
            mapped_start_sensor = len(t.index) - start_sensor
            mapped_end_sensor = len(t.index) - end_sensor

            if mapped_end_sensor < mapped_start_sensor:
                mapped_start_sensor, mapped_end_sensor = mapped_end_sensor, mapped_start_sensor

            # ---------------------------------------------------------
            self.config.print_with_time("Breadth() final width calc")
            width = breadth(config, mapped_start_sensor, mapped_end_sensor)

            # ---------------------------------------------------------
            self.config.print_with_time("Depth rounding calculation")
            try:
                depth_val = round(
                    (((length / width) * (max_value / base_value)) * 100) / self.config.pipe_thickness
                )
            except:
                depth_val = 0

            if depth_val > 1 and width > 1 and length > 1:
                classification_stats[classification]["count"] += 1
                submatrices_dict[(defect_counter, start_sensor, end_sensor)] = modified_df

                print(f"✓ Valid defect: depth={depth_val}%, width={width}mm, length={length}mm")

                # ---------------------------------------------------------
                self.config.print_with_time("Appending defect to list")
                finial_defect_list.append({
                    "pipe_id": pipe_id,
                    "runid": runid,
                    "defect_id": defect_counter,
                    "start_reading": start_reading,
                    "end_reading": end_reading,
                    "start_sensor": start_sensor,
                    "end_sensor": end_sensor,
                    "absolute_distance": absolute_distance,
                    "upstream": upstream,
                    "length": length,
                    "length_percent": length_percent,
                    "breadth": width,
                    "width_new2": round(width_1_only, 0),
                    "orientation": orientation,
                    "defect_type": internal_external,
                    "dimension_classification": dimension_classification,
                    "depth": depth_val1,
                    "depth_old": depth_old,
                    "start_oddo1": start_oddo1,
                    "end_oddo1": end_oddo1,
                    "speed": speed,
                    "Min_Val": min_positive,
                    "Max_Val": max_value,
                    "wall_thickness": wall_thickness,
                    "pipe_length": self.pipe_len_oddo1_chm
                })

                # ---------------------------------------------------------
                self.config.print_with_time("Adding heatmap annotation + rectangle")
                if classification == "Very Small (1-10%)":
                    color = 'purple'
                elif classification == "Small (10-20%)":
                    color = 'red'
                elif classification == "Medium (20-30%)":
                    color = 'orange'
                elif classification == "Large (30-40%)":
                    color = 'yellow'
                elif classification == "Very Large (40%+)":
                    color = 'blue'
                else:
                    color = 'gray'

                figx112.add_shape(
                    type='rect',
                    x0=start_reading - 0.5,
                    x1=end_reading + 0.5,
                    y0=start_sensor - 0.5,
                    y1=end_sensor + 0.5,
                    line=dict(color=color, width=2),
                    fillcolor=f'rgba(255, 0, 0, 0.2)'
                )

                figx112.add_annotation(
                    x=(start_reading + end_reading) / 2,
                    y=start_sensor - 1,
                    text=f"{defect_counter}({classification.split()[0]})",
                    showarrow=False,
                    font=dict(color=color, size=10),
                    bgcolor="white",
                    bordercolor="black",
                    borderwidth=1
                )

                # defect_counter += 1
                return True
            else:
                print(f"✗ Defect rejected: max_value={max_value} vs threshold={adjusted_threshold}")
                return False

        except Exception as e:
            print(f"Error processing defect: {str(e)}")
            return None







# def compute_defect_data(
#     self, result, df_clock_holl_oddo1, threshold_value,
#     max_of_all, df3_raw, mean1, df_new_proximity, Roll_hr, t,
#     pipe_id, runid, wall_thickness, row
# ):
#     print("processing single defect at a time")
#     self.config.print_with_time("Row fetched")
#
#     start_sensor = row.start_row
#     end_sensor = row.end_row
#     start_reading = row.start_col
#     end_reading = row.end_col
#
#     if start_sensor == end_sensor:
#         return {"accepted": False}
#
#     try:
#         # ---------------------------------------------------------
#         self.config.print_with_time("Creating submatrix")
#         submatrix = result.iloc[start_reading:end_reading + 1, start_sensor:end_sensor + 1]
#
#         self.config.print_with_time("Calculating max/min")
#         max_value = submatrix.max().max()
#         positive_vals = submatrix[submatrix > 0]
#         min_positive = positive_vals.min().min()
#
#         # ---------------------------------------------------------
#         self.config.print_with_time("Calculating length_percent")
#         length_percent, start, end, length = calculate_length_percent(
#             df_clock_holl_oddo1=df_clock_holl_oddo1,
#             start_reading=start_reading,
#             end_reading=end_reading,
#             l_per_1=self.config.l_per_1
#         )
#
#         # ---------------------------------------------------------
#         self.config.print_with_time("Adaptive sigma refinement")
#         sigma_multiplier, refinement_factor, classification = \
#             self.config.get_adaptive_sigma_refinement(length_percent)
#
#         adjusted_threshold = threshold_value * sigma_multiplier
#
#         # ---------------------------------------------------------
#         # threshold part
#         threshold_pass = (adjusted_threshold <= max_value <= max_of_all)
#
#         # Prepare variables that will be filled later
#         depth_old = None
#         df_copy_submatrix = None
#         max_index = None
#         start_oddo1 = None
#         end_oddo1 = None
#         speed = None
#         base_value = None
#         internal_external = None
#         absolute_distance = None
#         upstream = None
#         dimension_classification = None
#         orientation = None
#         x1 = y1 = z1 = None
#         df_duplicate = None
#         modified_df = None
#         trimmed_matrix = None
#         width_1_only = None
#         width_0_yes = None
#         new_start_sensor = None
#         new_end_sensor = None
#         width = None
#         depth_val1 = None
#
#         # ---------------------------------------------------------
#         if threshold_pass:
#             self.config.print_with_time("Calculating depth_old")
#             depth_old = (max_value - min_positive) / min_positive * 100
#
#             self.config.print_with_time("Running compute_depth")
#             depth_val1, df_copy_submatrix = compute_depth(
#                 self,
#                 df_raw=df3_raw,
#                 start_reading=start_reading,
#                 end_reading=end_reading,
#                 start_sensor=start_sensor,
#                 end_sensor=end_sensor,
#                 pipe_thickness=self.config.pipe_thickness,
#             )
#
#             self.config.print_with_time("Computing max_index")
#             max_column = submatrix.max().idxmax()
#             max_index = submatrix.columns.get_loc(max_column)
#
#             self.config.print_with_time("Calculating start/end oddo + speed")
#             start_oddo1 = df_clock_holl_oddo1[start_reading]
#             end_oddo1 = (df_clock_holl_oddo1[end_reading]) / 1000
#             time_sec = end_reading / 1500
#             speed = end_oddo1 / time_sec
#
#             base_value = mean1[max_index]
#
#             self.config.print_with_time("Internal/external detection")
#             internal_external = internal_or_external(df_new_proximity, max_index)
#
#             self.config.print_with_time("Absolute + upstream distance calc")
#             absolute_distance = df_clock_holl_oddo1[start_reading]
#             upstream = df_clock_holl_oddo1[start_reading] - df_clock_holl_oddo1[0]
#
#             counter_difference_1 = (end_sensor + 1) - (start_sensor + 1)
#             divid_1 = int(counter_difference_1 / 2)
#             center_1 = start_sensor + divid_1
#             factor1_1 = divid_1 * self.config.w_per_1
#
#             start1_1 = (int(center_1 - factor1_1)) - 1
#             end1_1 = (int(center_1 + factor1_1)) - 1
#
#             self.config.print_with_time("Breadth() initial width calc")
#             width = breadth(self, start_sensor, end_sensor)
#
#             self.config.print_with_time("Dimension classification")
#             dimension_classification = dimension_class(self.config.pipe_thickness, length, width)
#
#             self.config.print_with_time("Orientation calculation")
#             orientation = get_orientation(Roll_hr, start, end, start1_1, end1_1)
#
#             inner_diameter = self.config.outer_dia - 2 * self.config.pipe_thickness
#             radius = inner_diameter / 2
#             x1 = round(radius * math.radians(self.config.theta_ang1), 1)
#             y1 = round(radius * math.radians(self.config.theta_ang2), 1)
#             z1 = round(radius * math.radians(self.config.theta_ang3), 1)
#
#             self.config.print_with_time("Replace first column")
#             df_duplicate = replace_first_column(df_copy_submatrix, start_sensor, end_sensor)
#             df_duplicate.columns = df_duplicate.columns.astype(str)
#
#             self.config.print_with_time("Interpolating modified df")
#             modified_df = process_csv_interpolate(self, df_duplicate, x1, y1, z1)
#
#             self.config.print_with_time("Running process_submatrix")
#             trimmed_matrix, width_1_only, width_0_yes, new_start_sensor, new_end_sensor = \
#                 process_submatrix(self, modified_df, start1_1, end1_1)
#
#             new_start_sensor, new_end_sensor = \
#                 get_first_last_integer_column(trimmed_matrix.columns)
#
#             mapped_start_sensor = len(t.index) - start_sensor
#             mapped_end_sensor = len(t.index) - end_sensor
#             if mapped_end_sensor < mapped_start_sensor:
#                 mapped_start_sensor, mapped_end_sensor = mapped_end_sensor, mapped_start_sensor
#
#             self.config.print_with_time("Breadth() final width calc")
#             width = breadth(self, mapped_start_sensor, mapped_end_sensor)
#
#             # final depth
#             try:
#                 depth_val = round(
#                     (((length / width) * (max_value / base_value)) * 100)
#                     / self.config.pipe_thickness
#                 )
#             except:
#                 depth_val = 0
#
#             final_accept = (
#                 threshold_pass
#                 and depth_val > 1
#                 and width > 1
#                 and length > 1
#             )
#
#         else:
#             final_accept = False
#
#         # ---------------------------------------------------------
#         # RETURN all variables EXACTLY as-is
#         return {
#             "accepted": final_accept,
#             "classification": classification,
#             "start_sensor": start_sensor,
#             "end_sensor": end_sensor,
#             "start_reading": start_reading,
#             "end_reading": end_reading,
#             "absolute_distance": absolute_distance,
#             "upstream": upstream,
#             "length": length,
#             "length_percent": length_percent,
#             "breadth": width,
#             "width_new2": None if width_1_only is None else round(width_1_only, 0),
#             "orientation": orientation,
#             "defect_type": internal_external,
#             "dimension_classification": dimension_classification,
#             "depth": depth_val1,
#             "depth_old": depth_old,
#             "start_oddo1": start_oddo1,
#             "end_oddo1": end_oddo1,
#             "speed": speed,
#             "Min_Val": min_positive,
#             "Max_Val": max_value,
#             "pipe_id": pipe_id,
#             "runid": runid,
#             "wall_thickness": wall_thickness,
#             "pipe_length": self.pipe_len_oddo1_chm,
#             "modified_df": modified_df
#         }
#
#     except Exception as e:
#         print(f"Error in compute_defect_data: {str(e)}")
#         return {"accepted": False, "error": str(e)}


def compute_defect_data(
    config, result, df_clock_holl_oddo1, threshold_value,
    max_of_all, df3_raw, mean1, df_new_proximity, Roll_hr, t,
    pipe_id, runid, wall_thickness, row,pipe_len_oddo1_chm
):
    print("processing single defect at a time")
    # self.config.print_with_time("Row fetched")

    start_sensor = row.start_row
    end_sensor = row.end_row
    start_reading = row.start_col
    end_reading = row.end_col

    if start_sensor == end_sensor:
        return {"accepted": False}

    try:
        # ---------------------------------------------------------
        # self.config.print_with_time("Creating submatrix")
        submatrix = result.iloc[start_reading:end_reading + 1, start_sensor:end_sensor + 1]

        # self.config.print_with_time("Calculating max/min")
        max_value = submatrix.max().max()
        positive_vals = submatrix[submatrix > 0]
        min_positive = positive_vals.min().min()

        # ---------------------------------------------------------
        # self.config.print_with_time("Calculating length_percent")
        length_percent, start, end, length = calculate_length_percent(
            df_clock_holl_oddo1=df_clock_holl_oddo1,
            start_reading=start_reading,
            end_reading=end_reading,
            l_per_1=config["l_per_1"]
        )

        # ---------------------------------------------------------
        # self.config.print_with_time("Adaptive sigma refinement")
        sigma_multiplier, refinement_factor, classification = \
            config["get_adaptive_sigma_refinement"](length_percent)

        adjusted_threshold = threshold_value * sigma_multiplier

        # ---------------------------------------------------------
        # threshold part
        threshold_pass = (adjusted_threshold <= max_value <= max_of_all)

        # Prepare variables that will be filled later
        depth_old = None
        df_copy_submatrix = None
        max_index = None
        start_oddo1 = None
        end_oddo1 = None
        speed = None
        base_value = None
        internal_external = None
        absolute_distance = None
        upstream = None
        dimension_classification = None
        orientation = None
        x1 = y1 = z1 = None
        df_duplicate = None
        modified_df = None
        trimmed_matrix = None
        width_1_only = None
        width_0_yes = None
        new_start_sensor = None
        new_end_sensor = None
        width = None
        depth_val1 = None

        # ---------------------------------------------------------
        if threshold_pass:
            # self.config.print_with_time("Calculating depth_old")
            depth_old = (max_value - min_positive) / min_positive * 100

            # self.config.print_with_time("Running compute_depth")
            depth_val1, df_copy_submatrix = compute_depth(
                config,
                df_raw=df3_raw,
                start_reading=start_reading,
                end_reading=end_reading,
                start_sensor=start_sensor,
                end_sensor=end_sensor,
                pipe_thickness=config["pipe_thickness"],
            )

            # self.config.print_with_time("Computing max_index")
            max_column = submatrix.max().idxmax()
            max_index = submatrix.columns.get_loc(max_column)

            # self.config.print_with_time("Calculating start/end oddo + speed")
            start_oddo1 = df_clock_holl_oddo1[start_reading]
            end_oddo1 = (df_clock_holl_oddo1[end_reading]) / 1000
            time_sec = end_reading / 1500
            speed = end_oddo1 / time_sec

            base_value = mean1[max_index]

            # self.config.print_with_time("Internal/external detection")
            internal_external = internal_or_external(df_new_proximity, max_index)

            # self.config.print_with_time("Absolute + upstream distance calc")
            absolute_distance = df_clock_holl_oddo1[start_reading]
            upstream = df_clock_holl_oddo1[start_reading] - df_clock_holl_oddo1[0]

            counter_difference_1 = (end_sensor + 1) - (start_sensor + 1)
            divid_1 = int(counter_difference_1 / 2)
            center_1 = start_sensor + divid_1
            factor1_1 = divid_1 * config["w_per_1"]

            start1_1 = (int(center_1 - factor1_1)) - 1
            end1_1 = (int(center_1 + factor1_1)) - 1

            # self.config.print_with_time("Breadth() initial width calc")
            width = breadth(config, start_sensor, end_sensor)

            # self.config.print_with_time("Dimension classification")
            dimension_classification = dimension_class(config["pipe_thickness"], length, width)

            # self.config.print_with_time("Orientation calculation")
            orientation = get_orientation(Roll_hr, start, end, start1_1, end1_1)

            inner_diameter = config["outer_dia"] - 2 * config["pipe_thickness"]
            radius = inner_diameter / 2
            x1 = round(radius * math.radians(config["theta_ang1"]), 1)
            y1 = round(radius * math.radians(config["theta_ang2"]), 1)
            z1 = round(radius * math.radians(config["theta_ang3"]), 1)

            # self.config.print_with_time("Replace first column")
            df_duplicate = replace_first_column(df_copy_submatrix, start_sensor, end_sensor)
            df_duplicate.columns = df_duplicate.columns.astype(str)

            # self.config.print_with_time("Interpolating modified df")
            modified_df = process_csv_interpolate(config, df_duplicate, x1, y1, z1)

            # self.config.print_with_time("Running process_submatrix")
            trimmed_matrix, width_1_only, width_0_yes, new_start_sensor, new_end_sensor = \
                process_submatrix(config, modified_df, start1_1, end1_1)

            new_start_sensor, new_end_sensor = \
                get_first_last_integer_column(trimmed_matrix.columns)

            mapped_start_sensor = len(t.index) - start_sensor
            mapped_end_sensor = len(t.index) - end_sensor
            if mapped_end_sensor < mapped_start_sensor:
                mapped_start_sensor, mapped_end_sensor = mapped_end_sensor, mapped_start_sensor

            # self.config.print_with_time("Breadth() final width calc")
            width = breadth(config, mapped_start_sensor, mapped_end_sensor)

            # final depth
            try:
                depth_val = round(
                    (((length / width) * (max_value / base_value)) * 100)
                    / config["pipe_thickness"]
                )
            except:
                depth_val = 0

            final_accept = (
                threshold_pass
                and depth_val > 1
                and width > 1
                and length > 1
            )

        else:
            final_accept = False

        print("ACCEPT? =", final_accept,
              "| max_value =", max_value,
              "| adjusted_threshold =", adjusted_threshold,
              "| length =", length,
              "| width =", width)

        # ---------------------------------------------------------
        # RETURN all variables EXACTLY as-is
        return {
            "accepted": final_accept,
            "classification": classification,
            "start_sensor": start_sensor,
            "end_sensor": end_sensor,
            "start_reading": start_reading,
            "end_reading": end_reading,
            "absolute_distance": absolute_distance,
            "upstream": upstream,
            "length": length,
            "length_percent": length_percent,
            "breadth": width,
            "width_new2": None if width_1_only is None else round(width_1_only, 0),
            "orientation": orientation,
            "defect_type": internal_external,
            "dimension_classification": dimension_classification,
            "depth": depth_val1,
            "depth_old": depth_old,
            "start_oddo1": start_oddo1,
            "end_oddo1": end_oddo1,
            "speed": speed,
            "Min_Val": min_positive,
            "Max_Val": max_value,
            "pipe_id": pipe_id,
            "runid": runid,
            "wall_thickness": wall_thickness,
            "pipe_length": pipe_len_oddo1_chm,
            "modified_df": modified_df
        }

    except Exception as e:
        print(f"Error in compute_defect_data: {str(e)}")
        return {"accepted": False, "error": str(e)}


def compute_defect_data_multicore1(args):
    (
        config,
        result, df_clock_holl_oddo1, threshold_value,
        max_of_all, df3_raw, mean1,
        df_new_proximity, Roll_hr,
        pipe_id, runid, wall_thickness,
        row_tuple, pipe_len_oddo1_chm, length_index
    ) = args

    try:
        (start_sensor, end_sensor, start_reading, end_reading) = row_tuple


        if start_sensor == end_sensor:
            return {"accepted": False}

        # ---------------------------------------------------------
        submatrix = result.iloc[start_reading:end_reading + 1, start_sensor:end_sensor + 1]

        max_value = submatrix.max().max()
        positive_vals = submatrix[submatrix > 0]
        min_positive = positive_vals.min().min()

        # ---------------------------------------------------------
        length_percent, start, end, length = calculate_length_percent(
            df_clock_holl_oddo1=df_clock_holl_oddo1,
            start_reading=start_reading,
            end_reading=end_reading,
            l_per_1=config["l_per_1"]
        )

        # ---------------------------------------------------------
        # Adaptive sigma
        sigma_multiplier, refinement_factor, classification = \
            config["get_adaptive_sigma_refinement"](length_percent)

        adjusted_threshold = threshold_value * sigma_multiplier
        threshold_pass = (adjusted_threshold <= max_value <= max_of_all)

        # PREP fields
        df_copy_submatrix = None
        width = None
        width_1_only = None
        orientation = None
        internal_external = None
        base_value = None

        if threshold_pass:
            depth_old = (max_value - min_positive) / min_positive * 100

            # ---------------------------------------------------------
            depth_val1, df_copy_submatrix = compute_depth(
                config,
                df_raw=df3_raw,
                start_reading=start_reading,
                end_reading=end_reading,
                start_sensor=start_sensor,
                end_sensor=end_sensor,
                pipe_thickness=config["pipe_thickness"],
            )

            # ---------------------------------------------------------
            # max index
            max_column = submatrix.max().idxmax()
            max_index = submatrix.columns.get_loc(max_column)

            # ---------------------------------------------------------
            start_oddo1 = df_clock_holl_oddo1[start_reading]
            end_oddo1 = df_clock_holl_oddo1[end_reading] / 1000
            time_sec = end_reading / 1500
            speed = end_oddo1 / time_sec

            base_value = mean1[max_index]

            internal_external = internal_or_external(df_new_proximity, max_index)

            absolute_distance = df_clock_holl_oddo1[start_reading]
            upstream = df_clock_holl_oddo1[start_reading] - df_clock_holl_oddo1[0]

            # Width initial
            width = breadth(config, start_sensor, end_sensor)

            dimension_classification = dimension_class(config["pipe_thickness"], length, width)

            # ---------------------------------------------------------
            # Orientation
            center_offset = (end_sensor - start_sensor) / 2
            center = start_sensor + center_offset
            w_factor = center_offset * config["w_per_1"]

            start1_1 = int(center - w_factor) - 1
            end1_1 = int(center + w_factor) - 1

            orientation = get_orientation(Roll_hr, start, end, start1_1, end1_1)

            # Pipe geometry
            inner_diameter = config["outer_dia"] - 2 * config["pipe_thickness"]
            radius = inner_diameter / 2

            x1 = round(radius * math.radians(config["theta_ang1"]), 1)
            y1 = round(radius * math.radians(config["theta_ang2"]), 1)
            z1 = round(radius * math.radians(config["theta_ang3"]), 1)

            # ---------------------------------------------------------
            # Modify df
            df_duplicate = replace_first_column(df_copy_submatrix, start_sensor, end_sensor)
            df_duplicate.columns = df_duplicate.columns.astype(str)

            modified_df = process_csv_interpolate(config,df_duplicate, x1, y1, z1)

            trimmed_matrix, width_1_only, width_0_yes, new_start_sensor, new_end_sensor = \
                process_submatrix(config, modified_df, start1_1, end1_1)

            new_start_sensor, new_end_sensor = get_first_last_integer_column(trimmed_matrix.columns)

            mapped_start_sensor = length_index - start_sensor
            mapped_end_sensor = length_index - end_sensor
            if mapped_end_sensor < mapped_start_sensor:
                mapped_start_sensor, mapped_end_sensor = mapped_end_sensor, mapped_start_sensor

            width = breadth(config, mapped_start_sensor, mapped_end_sensor)

            # final depth
            try:
                depth_val = round(
                    (((length / width) * (max_value / base_value)) * 100)
                    / config["pipe_thickness"]
                )
            except:
                depth_val = 0

            final_accept = (
                threshold_pass and depth_val > 1 and width > 1 and length > 1
            )

        else:
            final_accept = False
            absolute_distance = upstream = None
            dimension_classification = None
            orientation = None
            internal_external = None
            depth_val1 = depth_old = None
            # modified_df = None

        print("ACCEPT? =", final_accept,
              "| max_value =", max_value,
              "| adjusted_threshold =", adjusted_threshold,
              "| length =", length,
              "| width =", width)

        # ---------------------------------------------------------
        return {
            "accepted": final_accept,
            "classification": classification,
            "start_sensor": start_sensor,
            "end_sensor": end_sensor,
            "start_reading": start_reading,
            "end_reading": end_reading,
            "absolute_distance": absolute_distance,
            "upstream": upstream,
            "length": length,
            "length_percent": length_percent,
            "breadth": width,
            "width_new2": None if width_1_only is None else round(width_1_only, 0),
            "orientation": orientation,
            "defect_type": internal_external,
            "dimension_classification": dimension_classification,
            "depth": depth_val1,
            "depth_old": depth_old,
            "start_oddo1": start_oddo1,
            "end_oddo1": end_oddo1,
            "speed": speed,
            "Min_Val": min_positive,
            "Max_Val": max_value,
            "pipe_id": pipe_id,
            "runid": runid,
            "wall_thickness": wall_thickness,
            "pipe_length": pipe_len_oddo1_chm,
            # "modified_df": modified_df,
        }

    except Exception as e:
        return {"accepted": False, "error": str(e)}



# def compute_defect_data_multicore(row_tuple):
#     """
#     Worker that processes a single defect using globally shared objects.
#     Only receives a small row_tuple: (start_sensor, end_sensor, start_reading, end_reading)
#     """
#
#     # global (G_CONFIG, G_RESULT, G_DF_CLOCK, G_THRESHOLD,
#     #         G_MAX_OF_ALL, G_DF3_RAW, G_MEAN1,
#     #         G_DF_NEW_PROX, G_ROLL_HR,
#     #         G_PIPE_ID, G_RUNID, G_WALL_THICKNESS,
#     #         G_PIPE_LEN, G_LENGTH_INDEX)
#     global G_CONFIG, G_RESULT, G_DF_CLOCK, G_THRESHOLD,G_MAX_OF_ALL, G_DF3_RAW, G_MEAN1, G_DF_NEW_PROX, G_ROLL_HR, G_PIPE_ID, G_RUNID, G_WALL_THICKNESS,G_PIPE_LEN, G_LENGTH_INDEX
#
#
#     try:
#         (start_sensor, end_sensor, start_reading, end_reading) = row_tuple
#
#         if start_sensor == end_sensor:
#             return {"accepted": False}
#
#         # Short-hands for speed + readability
#         config           = G_CONFIG
#         result           = G_RESULT
#         df_clock_holl_oddo1 = G_DF_CLOCK
#         threshold_value  = G_THRESHOLD
#         max_of_all       = G_MAX_OF_ALL
#         df3_raw          = G_DF3_RAW
#         mean1            = G_MEAN1
#         df_new_proximity = G_DF_NEW_PROX
#         Roll_hr          = G_ROLL_HR
#         pipe_id          = G_PIPE_ID
#         runid            = G_RUNID
#         wall_thickness   = G_WALL_THICKNESS
#         pipe_len_oddo1_chm = G_PIPE_LEN
#         length_index     = G_LENGTH_INDEX
#
#         # ---------------------------------------------------------
#         # SUBMATRIX
#         submatrix = result.iloc[start_reading:end_reading + 1,
#                                 start_sensor:end_sensor + 1]
#
#         max_value = submatrix.max().max()
#         positive_vals = submatrix[submatrix > 0]
#         min_positive = positive_vals.min().min()
#
#         # ---------------------------------------------------------
#         # LENGTH %
#         length_percent, start, end, length = calculate_length_percent(
#             df_clock_holl_oddo1=df_clock_holl_oddo1,
#             start_reading=start_reading,
#             end_reading=end_reading,
#             l_per_1=config["l_per_1"]
#         )
#
#         # ---------------------------------------------------------
#         # ADAPTIVE SIGMA
#         sigma_multiplier, refinement_factor, classification = \
#             config["get_adaptive_sigma_refinement"](length_percent)
#
#         adjusted_threshold = threshold_value * sigma_multiplier
#         threshold_pass = (adjusted_threshold <= max_value <= max_of_all)
#
#         # Prep
#         df_copy_submatrix = None
#         width = None
#         width_1_only = None
#         orientation = None
#         internal_external = None
#         base_value = None
#
#         if threshold_pass:
#             depth_old = (max_value - min_positive) / min_positive * 100
#
#             # DEPTH
#             depth_val1, df_copy_submatrix = compute_depth(
#                 config,
#                 df_raw=df3_raw,
#                 start_reading=start_reading,
#                 end_reading=end_reading,
#                 start_sensor=start_sensor,
#                 end_sensor=end_sensor,
#                 pipe_thickness=config["pipe_thickness"],
#             )
#
#             # MAX INDEX
#             max_column = submatrix.max().idxmax()
#             max_index = submatrix.columns.get_loc(max_column)
#
#             start_oddo1 = df_clock_holl_oddo1[start_reading]
#             end_oddo1   = df_clock_holl_oddo1[end_reading] / 1000
#             time_sec    = end_reading / 1500
#             speed       = end_oddo1 / time_sec
#
#             base_value = mean1[max_index]
#
#             internal_external = internal_or_external(df_new_proximity, max_index)
#
#             absolute_distance = df_clock_holl_oddo1[start_reading]
#             upstream = df_clock_holl_oddo1[start_reading] - df_clock_holl_oddo1[0]
#
#             # WIDTH (initial)
#             width = breadth(config, start_sensor, end_sensor)
#             dimension_classification = dimension_class(
#                 config["pipe_thickness"], length, width
#             )
#
#             # ---------------------------------------------------------
#             # ORIENTATION
#             center_offset = (end_sensor - start_sensor) / 2
#             center = start_sensor + center_offset
#             w_factor = center_offset * config["w_per_1"]
#
#             start1_1 = int(center - w_factor) - 1
#             end1_1   = int(center + w_factor) - 1
#
#             orientation = get_orientation(
#                 Roll_hr, start, end, start1_1, end1_1
#             )
#
#             # PIPE GEOMETRY
#             inner_diameter = config["outer_dia"] - 2 * config["pipe_thickness"]
#             radius = inner_diameter / 2
#
#             x1 = round(radius * math.radians(config["theta_ang1"]), 1)
#             y1 = round(radius * math.radians(config["theta_ang2"]), 1)
#             z1 = round(radius * math.radians(config["theta_ang3"]), 1)
#
#             # MODIFY DF
#             df_duplicate = replace_first_column(
#                 df_copy_submatrix, start_sensor, end_sensor
#             )
#             df_duplicate.columns = df_duplicate.columns.astype(str)
#
#             modified_df = process_csv_interpolate(config, df_duplicate, x1, y1, z1)
#
#             trimmed_matrix, width_1_only, width_0_yes, \
#             new_start_sensor, new_end_sensor = process_submatrix(
#                 config, modified_df, start1_1, end1_1
#             )
#
#             new_start_sensor, new_end_sensor = \
#                 get_first_last_integer_column(trimmed_matrix.columns)
#
#             mapped_start_sensor = length_index - start_sensor
#             mapped_end_sensor   = length_index - end_sensor
#             if mapped_end_sensor < mapped_start_sensor:
#                 mapped_start_sensor, mapped_end_sensor = \
#                     mapped_end_sensor, mapped_start_sensor
#
#             width = breadth(config, mapped_start_sensor, mapped_end_sensor)
#
#             # FINAL DEPTH
#             try:
#                 depth_val = round(
#                     (((length / width) * (max_value / base_value)) * 100)
#                     / config["pipe_thickness"]
#                 )
#             except:
#                 depth_val = 0
#
#             final_accept = (
#                 threshold_pass and depth_val > 1 and width > 1 and length > 1
#             )
#
#         else:
#             final_accept = False
#             absolute_distance = upstream = None
#             dimension_classification = None
#             orientation = None
#             internal_external = None
#             depth_val1 = depth_old = None
#             speed = None
#             start_oddo1 = None
#             end_oddo1 = None
#             modified_df = None
#
#         print("ACCEPT? =", final_accept,
#               "| max_value =", max_value,
#               "| adjusted_threshold =", adjusted_threshold,
#               "| length =", length,
#               "| width =", width)
#         # ---------------------------------------------------------
#         return {
#             "accepted": final_accept,
#             "classification": classification,
#             "start_sensor": start_sensor,
#             "end_sensor": end_sensor,
#             "start_reading": start_reading,
#             "end_reading": end_reading,
#             "absolute_distance": absolute_distance,
#             "upstream": upstream,
#             "length": length,
#             "length_percent": length_percent,
#             "breadth": width,
#             "width_new2": None if width_1_only is None else round(width_1_only, 0),
#             "orientation": orientation,
#             "defect_type": internal_external,
#             "dimension_classification": dimension_classification,
#             "depth": depth_val1,
#             "depth_old": depth_old,
#             "start_oddo1": start_oddo1,
#             "end_oddo1": end_oddo1,
#             "speed": speed,
#             "Min_Val": min_positive,
#             "Max_Val": max_value,
#             "pipe_id": pipe_id,
#             "runid": runid,
#             "wall_thickness": wall_thickness,
#             "pipe_length": pipe_len_oddo1_chm,
#             "modified_df": modified_df,
#         }
#
#     except Exception as e:
#         return {"accepted": False, "error": str(e)}


# def apply_defect_result(
#     self,
#     res,
#     classification_stats,
#     defect_counter,
#     submatrices_dict,
#     finial_defect_list,
#     figx112
# ):
#     if "classification" in res and res["classification"]:
#         classification_stats[res["classification"]]["total_processed"] += 1
#
#     if not res["accepted"]:
#         return defect_counter
#
#     classification = res["classification"]
#     classification_stats[classification]["count"] += 1
#
#     start_sensor = res["start_sensor"]
#     end_sensor = res["end_sensor"]
#     start_reading = res["start_reading"]
#     end_reading = res["end_reading"]
#     modified_df = res["modified_df"]
#
#     # SAVE MATRIX
#     submatrices_dict[
#         (defect_counter, start_sensor, end_sensor)
#     ] = modified_df
#
#     # APPEND DEFECT
#     finial_defect_list.append({
#         "pipe_id": res["pipe_id"],
#         "runid": res["runid"],
#         "defect_id": defect_counter,
#         "start_reading": start_reading,
#         "end_reading": end_reading,
#         "start_sensor": start_sensor,
#         "end_sensor": end_sensor,
#         "absolute_distance": res["absolute_distance"],
#         "upstream": res["upstream"],
#         "length": res["length"],
#         "length_percent": res["length_percent"],
#         "breadth": res["breadth"],
#         "width_new2": res["width_new2"],
#         "orientation": res["orientation"],
#         "defect_type": res["defect_type"],
#         "dimension_classification": res["dimension_classification"],
#         "depth": res["depth"],
#         "depth_old": res["depth_old"],
#         "start_oddo1": res["start_oddo1"],
#         "end_oddo1": res["end_oddo1"],
#         "speed": res["speed"],
#         "Min_Val": res["Min_Val"],
#         "Max_Val": res["Max_Val"],
#         "wall_thickness": res["wall_thickness"],
#         "pipe_length": res["pipe_length"]
#     })
#
#     # COLOR EXACT SAME LOGIC
#     if classification == "Very Small (1-10%)":
#         color = 'purple'
#     elif classification == "Small (10-20%)":
#         color = 'red'
#     elif classification == "Medium (20-30%)":
#         color = 'orange'
#     elif classification == "Large (30-40%)":
#         color = 'yellow'
#     elif classification == "Very Large (40%+)":
#         color = 'blue'
#     else:
#         color = 'gray'
#
#     figx112.add_shape(
#         type='rect',
#         x0=start_reading - 0.5,
#         x1=end_reading + 0.5,
#         y0=start_sensor - 0.5,
#         y1=end_sensor + 0.5,
#         line=dict(color=color, width=2),
#         fillcolor=f'rgba(255, 0, 0, 0.2)'
#     )
#
#     figx112.add_annotation(
#         x=(start_reading + end_reading) / 2,
#         y=start_sensor - 1,
#         text=f"{defect_counter}({classification.split()[0]})",
#         showarrow=False,
#         font=dict(color=color, size=10),
#         bgcolor="white",
#         bordercolor="black",
#         borderwidth=1
#     )
#
#     return defect_counter + 1



