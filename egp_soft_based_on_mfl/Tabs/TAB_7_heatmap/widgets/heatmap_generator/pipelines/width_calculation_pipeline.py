import math
import os
import re
import joblib
from pywt import cwt
import numpy as np
import pandas as pd




#-------WIDTH--------CALCULATION
def breadth(config, start_sensor, end_sensor):
    start_sensor1 = start_sensor + 1
    end_sensor1 = end_sensor + 1
    if start_sensor1 > end_sensor1 or start_sensor1 == end_sensor1:
        return 0

    outer_diameter_1 = config["outer_dia"]
    thickness_1 = config["pipe_thickness"]
    print(f"thickness 1: {thickness_1}")
    inner_diameter_1 = outer_diameter_1 - 2 * (thickness_1)
    radius_1 = inner_diameter_1 / 2

    theta_2 = config["theta_ang1"]
    c_1 = math.radians(theta_2)
    theta_3 = config["theta_ang2"]
    d_1 = math.radians(theta_3)
    theta_4 = config["theta_ang3"]
    e_1 = math.radians(theta_4)

    x1 = round(radius_1 * c_1, 1)
    y1 = round(radius_1 * d_1, 1)
    z1 = round(radius_1 * e_1, 1)
    print("x1, y1, z1", x1, y1, z1)

    bredth = 0
    i = start_sensor1
    while i < end_sensor1:
        next_sensor = i
        if next_sensor % 16 == 0 and next_sensor != end_sensor1:
            bredth += z1
        elif next_sensor % 4 == 0:
            bredth += y1
        else:
            bredth += x1
        i += 1
    return bredth


#-------------WIDTH_new---CALCULATION-------------- width_0_no=>width_slope=>width_new
# def slope_filter(df_diff):
#     refined_outputs = {}
#     width_0_no = 0
#     width_0_no1 = 0
#     try:
#         if df_diff.isnull().values.any():
#             return None
#         # q1 = df_diff.quantile(0.25)
#         # q3 = df_diff.quantile(0.75)
#         # iqr = q3 - q1
#         # iqr_threshold = iqr[iqr > 0].mean()
#         # important_cols_iqr = iqr[iqr > iqr_threshold].index
#         # refined_outputs['iqr'] = df_diff[important_cols_iqr]
#
#         slope_strength = df_diff.diff().abs().sum()
#         slope_threshold = slope_strength.mean() * (config.slope_per)
#         important_cols_slope = slope_strength[slope_strength > slope_threshold].index
#         refined_outputs['slope'] = df_diff[important_cols_slope]
#
#         width_0_no = (len(important_cols_slope) - 1) * config.div_factor
#         # width_0_no1 = (len(important_cols_iqr) - 1) * div_factor
#     except Exception as e:
#         refined_outputs['slope'] = None
#         # refined_outputs['iqr'] = None
#         print("Method failed:", e)
#     return refined_outputs, width_0_no




#---------WIDTH_NEW2----------CALCULATION
def process_submatrix(config, df_diff, start1_1, end1_1):
    if df_diff.isnull().values.any():
        return None

    # try:
    #     max_val = df_diff.max().max()
    #     min_pos_val = df_diff[df_diff > 0].min().min()
    #     signal_strength = np.log10(max_val + 1)  # Avoid log(0)
    # except:
    #     max_val = None
    #     min_pos_val = None
    #     signal_strength = 0

    ### STDEV ON DEFECT MATRIX ROW-WISE ###
    # print("df_diff", df_diff)
    # df_diff = df_diff.applymap(lambda x: np.log(x) if x > 0 else np.nan)
    # adaptive_sigma_row = get_adaptive_sigma_row_values(length_percent)
    # ratio = round((max_val - min_pos_val) / (min_pos_val + 1e-5), 2)
    # sigma_multiplier, _, _ = get_adaptive_sigma_refinement(length_percent)
    # effective_positive_sigma_row = adaptive_sigma_row * positive_sigma_row

    df_diff_mean = list(df_diff.median(axis=1))
    df_std_dev = list(df_diff.std(axis=1, ddof=1))
    mean_plus_std = list(
        map(lambda x, y: x + y * (config["positive_sigma_row"]), df_diff_mean, df_std_dev))
    # mean_plus_std = list(map(lambda x, y: x * (positive_sigma_row), df_diff_mean, df_std_dev))
    mean_plus_std_series = pd.Series(mean_plus_std, index=df_diff.index)
    # mean_neg_std = list(map(lambda x, y: x - y * (negative_sigma_row), df_diff_mean, df_std_dev))
    # mean_neg_std_series = pd.Series(mean_neg_std, index=df_diff.index)
    # Apply the function row-wise
    df_result = df_diff.apply(
        lambda row: row.map(lambda x: 1 if x > mean_plus_std_series[row.name] else 0),
        axis=1)

    ### STDEV ON DEFECT MATRIX COLUMN-WISE ###
    # df_diff_mean = df_diff.median(axis=0).tolist()
    # df_std_dev = df_diff.std(axis=0, skipna=True, ddof=1).tolist()
    # mean_plus_std = []
    # for i_std, data_std in enumerate(df_diff_mean):
    #     sigma_std_col = data_std + (positive_sigma_row * df_std_dev[i_std])
    #     mean_plus_std.append(sigma_std_col)
    # df_result = pd.DataFrame(index=df_diff.index)
    # for col1_std, data1_std in enumerate(df_diff.columns):
    #     df_result[data1_std] = df_diff[data1_std].apply(lambda x: 1 if x > mean_plus_std[col1_std] else 0)

    count_ones_per_column = df_result.sum(axis=0)
    first_col_with_1 = count_ones_per_column.ne(0).idxmax()
    last_col_with_1 = count_ones_per_column[::-1].ne(0).idxmax()
    first_col_with_1_idx = df_result.columns.get_loc(first_col_with_1)
    last_col_with_1_idx = df_result.columns.get_loc(last_col_with_1)

    df_between = df_result.iloc[:, first_col_with_1_idx:last_col_with_1_idx + 1]
    # Count columns that have at least one '1'
    num_cols_with_ones = (df_between == 1).any(axis=0).sum()
    num_cols_between = last_col_with_1_idx - first_col_with_1_idx + 1

    # Step 3: Count the number of columns to remove from start and end
    num_cols_to_remove_start = first_col_with_1_idx
    num_cols_to_remove_end = len(count_ones_per_column) - 1 - last_col_with_1_idx

    width_1_only = round(num_cols_with_ones * config["div_factor"])
    width_0_yes = round(num_cols_between * config["div_factor"])
    print("width_1_only", width_1_only)
    print("width_0_yes", width_0_yes)
    trimmed_original_matrix = df_diff.iloc[:,
                              first_col_with_1_idx: last_col_with_1_idx + 1]
    new_start_sensor = start1_1 + num_cols_to_remove_start
    new_end_sensor = end1_1 - num_cols_to_remove_end
    return trimmed_original_matrix, width_1_only, width_0_yes, new_start_sensor, new_end_sensor





#width calculation with use of model - machine learning --- best width out of all --- it uses some features along with
# width_new2 that gets calculated using above method
def ML_width_calc(self, output_dir, runid, pipe_id):
    print("inside ml calc ")
    try:
        model_path = self.config.model_location
    except Exception as e:
        print(f"model path error : {e}")

    model = joblib.load(model_path)  # ✅ Load actual model object
    model_width(self, model, output_dir, runid, pipe_id)



def model_width(self, model, folder_path, runid, pipe_id):
    # query = "select id, speed, start_sensor, end_sensor, width_new2 from bb_new"
    query = "select defect_id, runid, pipe_id, speed,start_index, end_index, start_sensor, end_sensor, width_new2 from defect_clock_hm"
    df_meta = pd.read_sql_query(query, self.config.connection)
    df_meta.rename(columns={'defect_id': 'def_no.', 'width_new2': 'pred_width'}, inplace=True)
    # before
    # df_meta['def_no.'] = df_meta['def_no.'].astype(int)

    df_meta = df_meta.dropna(subset=['def_no.'])  # skip rows with missing defect_id
    df_meta['def_no.'] = df_meta['def_no.'].astype(int)

    # start_index = df_meta['start_index']
    # end_index = df_meta['end_index']
    # runid = df_meta['runid']
    # pipe_id = df_meta['pipe_id']
    # after
    # df_meta['def_no.'] = df_meta['def_no.'].astype('Int64')  # Capital 'I'

    print("Defect numbers in metadata:", df_meta['def_no.'].dropna().unique())
    # before
    # meta_dict = {
    #     int(row['def_no.']): {
    #         'speed': float(row['speed']),
    #         'Start_sensor': float(row['start_sensor']),
    #         'End_sensor': float(row['end_sensor']),
    #         'pred_width': float(row['pred_width']),
    #     }
    #     for _, row in df_meta.iterrows()
    # }
    # after
    meta_dict = {
        int(row['def_no.']): {
            'speed': float(row['speed']),
            'Start_sensor': float(row['start_sensor']),
            'End_sensor': float(row['end_sensor']),
            'pred_width': float(row['pred_width']),
        }
        for _, row in df_meta.iterrows()
    }

    records = []

    print("🔍 Matching submatrices in:", folder_path)
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv') and filename.startswith("submatrix_ptt-"):
            match = re.search(r'\((\d+),', filename)
            if not match:
                print(f"❌ Skipping (no match): {filename}")
                continue

            defect_no = int(match.group(1))

            if defect_no not in meta_dict:
                print(f"⚠️ Defect {defect_no} not in metadata, skipping.")
                continue

            file_path = os.path.join(folder_path, filename)
            matrix = pd.read_csv(file_path, dtype=str)
            matrix = matrix.apply(pd.to_numeric, errors='coerce').fillna(0)

            flat = matrix.values.flatten().astype(np.float32)
            flat = (flat - np.mean(flat)) / (np.std(flat) + 1e-8)

            meta = meta_dict[defect_no]
            record = {
                'filename': filename,
                'def_no.': defect_no,
                'submatrix': flat.tolist(),
                'speed': meta['speed'],
                'Start_sensor': meta['Start_sensor'],
                'End_sensor': meta['End_sensor'],
                'pred_width': meta['pred_width'],
            }

            records.append(record)
    df_test = pd.DataFrame(records)
    print("✅ Final test dataset shape:", df_test.shape)
    print(df_test.shape)

    if model != None:
        print("Model successfully loaded ")
    else:
        print("error loading model")
    filename = df_test['filename'] if 'filename' in df_test.columns else [f"sample_{i}" for i in
                                                                          range(len(df_test))]
    df_test.drop(columns=['filename'], inplace=True, errors='ignore')
    # df_test['submatrix'] = df_test['submatrix'].apply(lambda s: [float(x) for x in ast.literal_eval(s)])
    features = df_test.apply(extract_features, axis=1, result_type='expand')
    feature_columns = ['mean', 'std', 'max', 'min', 'threshold_crossings', 'anomaly_score',
                       'cwt_median'] + [f'fft_{i}' for i in range(10)]
    print("Features shape:", features.shape)  # Should be (n_rows, 17)
    print("Feature columns:", len(feature_columns))  # Should match number of columns

    features.columns = feature_columns
    print(feature_columns)
    print(filename)
    final_df = pd.concat(
        [features, df_test[['speed', 'Start_sensor', 'End_sensor', 'pred_width']]],
        axis=1)
    final_df.drop(columns=['std'], inplace=True)
    print(final_df.columns)
    final_df.rename(columns={"End_sensor": "End_Sensor"}, inplace=True)
    # pred = model.predict(final_df)
    pred = np.floor(model.predict(final_df)).astype(int)
    cursor = self.config.connection.cursor()
    # for defect_no, pred_val in zip(df_test['def_no.'], pred):
    #     # cursor.execute("UPDATE bb_new SET width_final = %s WHERE id = %s",
    #     #                (int(pred_val), int(defect_no)))
    #
    #     cursor.execute("UPDATE defect_clock_hm SET width_final = %s WHERE id = %s",
    #                    (int(pred_val), int(defect_no)))

    for defect_no, pred_val in zip(df_test['def_no.'], pred):
        # ✅ Sanity check for null/NaN predictions
        if pd.isna(pred_val):
            print(f"⚠️ Skipped NULL prediction for defect_no={defect_no}")
            continue

        try:
            cursor.execute(
                "UPDATE defect_clock_hm SET width_final = %s WHERE defect_id = %s AND runid = %s AND pipe_id = %s",
                (float(pred_val), int(defect_no), int(runid), int(pipe_id))
            )
            if cursor.rowcount == 0:
                print(f"⚠️ No row found for defect_id={defect_no}")
        except Exception as e:
            print(f"❌ Error updating defect_id={defect_no}: {e}")

    # for idx, row in df_test.iterrows():
    #     defect_no = int(row['def_no.'])
    #     pred_val = row['pred']
    #     runid = int(row['runid'])
    #     start_index = int(row['start_index'])
    #     end_index = int(row['end_index'])
    #
    #     if pd.isna(pred_val):
    #         print(f"⚠️ NULL WARNING: pred_val is NaN for defect_no={defect_no}")
    #         continue
    #
    #     cursor.execute(
    #         "UPDATE defect_clock_hm SET width_final=%s WHERE runid=%s AND start_index=%s AND end_index=%s",
    #         (float(pred_val), runid, start_index, end_index)
    #     )

    self.config.connection.commit()


def extract_features(row):
    x = np.array(row['submatrix'])

    # Basic stats
    mean = np.mean(x)
    std = np.std(x)
    max_val = np.max(x)
    min_val = np.min(x)

    # FFT features
    # fft_vals = np.abs(np.fft.fft(x))
    # FFT features
    fft_vals = np.abs(np.fft.fft(x))
    print(f" length fft: {len(fft_vals)}")
    # 🔥 Always make exactly 10 FFT features, pad with zeros if needed
    fft_features = np.zeros(10, dtype=float)
    n = min(10, len(fft_vals))
    fft_features[:n] = fft_vals[:n]

    # fft_features = fft_vals[:10]

    # Threshold crossings
    threshold = mean + 2 * std
    threshold_crossings = np.sum(x > threshold)

    # Z-score anomalies
    z_scores = np.abs((x - mean) / (std + 1e-8))
    anomaly_score = np.mean(z_scores > 3)

    # CWT Median Feature using pywt.cwt
    try:
        x = np.array(x)
        if x.ndim == 1:
            side = int(np.sqrt(len(x)))
            if side * side != len(x):
                raise ValueError("Not a perfect square")
            mat = x.reshape(-1, side)
        else:
            mat = x
    except:
        mat = np.atleast_2d(x)

    cwt_medians = []
    for row_sig in mat:
        row_sig = np.asarray(row_sig)
        if row_sig.ndim != 1:
            continue

        N = len(row_sig)
        if N < 5:
            continue

        signal_std = np.std(row_sig)
        max_scale = min(N // 2, max(3, int(signal_std * 10)))
        if max_scale < 1:
            continue

        widths = np.arange(1, max_scale + 1)
        if len(widths) < 1:
            continue

        # ✅ FIXED: use 'gaus1' (not 'guass1') and unpack coeffs and freqs
        coeffs, freqs = cwt(row_sig, widths, 'gaus1')
        row_cwt_median = np.median(np.abs(coeffs))
        cwt_medians.append(row_cwt_median)

    cwt_final = np.median(cwt_medians) if cwt_medians else 0

    return [mean, std, max_val, min_val, threshold_crossings, anomaly_score, cwt_final] + list(
        fft_features)