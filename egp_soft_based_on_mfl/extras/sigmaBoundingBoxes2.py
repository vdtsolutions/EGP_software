from scipy.interpolate import interp1d
import os
import plotly.graph_objs as go
import pandas as pd
import re
from scipy.ndimage import label, find_objects
import shutil
from datetime import datetime, timedelta
import numpy as np
from scipy.stats import gmean
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
import math
from math import floor
from pywt import cwt
import pymysql
from statistics import mean
import plotly.io as pio
import joblib
import warnings
warnings.filterwarnings('ignore')

connection = pymysql.connect(host='localhost', user='root', password='Thehero2004', db='vdt')
model = joblib.load("DLModeling/rf_width_model.pkl")

oddo1_ref = 0
roll_ref = 0
pipe_thickness = 7.1
outer_dia = 324
theta_ang1 = 1.7
theta_ang2 = 3.4
theta_ang3 = 9.7

# KEEP ORIGINAL WORKING SIGMA VALUES FOR INITIAL DETECTION
positive_sigma_col = 1.2
negative_sigma_col = 3
positive_sigma_row = 0.45
negative_sigma_row = 3

slope_per = 0.65
defect_box_thresh = 0.35
l_per1 = 0.76
w_per1 = 0.55
div_factor = 1.15
value_decreae_per = 0.02

def extract_int_prefix(s):
    m = re.match(r'^(\d+)', str(s))
    return int(m.group(1)) if m else None

def get_first_last_integer_column(cols):
    int_vals = [extract_int_prefix(col) for col in cols]
    int_vals = [v for v in int_vals if v is not None]
    if not int_vals:
        return None, None
    return min(int_vals), max(int_vals)

#==============================================================================================================
def process_submatrix_quantile(df_diff, quantile=0.9):
    if df_diff.isnull().values.any():
        return None

    row_thresholds = df_diff.quantile(q=quantile, axis=1)
    df_result = df_diff.gt(row_thresholds, axis=0).astype(int)

    count_ones_per_column = df_result.sum(axis=0)
    if count_ones_per_column.max() == 0:
        return df_diff, 0, 0, None, None

    first_col_with_1 = count_ones_per_column.ne(0).idxmax()
    last_col_with_1 = count_ones_per_column[::-1].ne(0).idxmax()
    first_idx = df_result.columns.get_loc(first_col_with_1)
    last_idx = df_result.columns.get_loc(last_col_with_1)

    df_between = df_result.iloc[:, first_idx:last_idx + 1]
    num_cols_with_ones = (df_between == 1).any(axis=0).sum()
    num_cols_total = last_idx - first_idx + 1

    width_1 = round(num_cols_with_ones * div_factor)
    width_0 = round(num_cols_total * div_factor)
    trimmed_matrix = df_diff.iloc[:, first_idx:last_idx + 1]

    return trimmed_matrix, width_1, width_0, first_idx, last_idx
#==============================================================================================================

def manage_directory(directory_path):
    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory created: {directory_path}")
    else:
        print(f"Directory already exists: {directory_path}")

    # Delete all existing files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

    print(f"All files deleted from directory: {directory_path}")
    
#==============================================================================================================

def extract_features(row):
    x = np.array(row['submatrix'])

    # Basic stats
    mean = np.mean(x)
    std = np.std(x)
    max_val = np.max(x)
    min_val = np.min(x)

    # FFT features
    fft_vals = np.abs(np.fft.fft(x))
    fft_features = fft_vals[:10]

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

    return [mean, std, max_val, min_val, threshold_crossings, anomaly_score, cwt_final] + list(fft_features)
#==============================================================================================================
def model_width(model,folder_path):
    query = "select id, speed, start_sensor, end_sensor, width_new2 from bbnew"
    df_meta = pd.read_sql_query(query, connection)
    df_meta.rename(columns={'id':'def_no.','width_new2':'pred_width'}, inplace = True)
    df_meta['def_no.'] = df_meta['def_no.'].astype(int)
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
    filename = df_test['filename'] if 'filename' in df_test.columns else [f"sample_{i}" for i in range(len(df_test))]
    df_test.drop(columns=['filename'], inplace=True, errors='ignore')
    #df_test['submatrix'] = df_test['submatrix'].apply(lambda s: [float(x) for x in ast.literal_eval(s)])
    features = df_test.apply(extract_features, axis=1, result_type='expand')
    feature_columns = ['mean', 'std', 'max', 'min', 'threshold_crossings', 'anomaly_score','cwt_median'] + [f'fft_{i}' for i in range(10)]
    features.columns = feature_columns
    print(feature_columns)
    print(filename)
    final_df = pd.concat([features, df_test[['speed','Start_sensor','End_sensor', 'pred_width']]], axis=1)
    final_df.drop(columns= ['std'], inplace= True)
    print(final_df.columns)
    final_df.rename(columns={"End_sensor": "End_Sensor"}, inplace=True)
    pred = model.predict(final_df)
    pred = np.floor(model.predict(final_df)).astype(int)
    cursor = connection.cursor()
    for defect_no, pred_val in zip(df_test['def_no.'], pred):
        cursor.execute("UPDATE bbnew SET width_new2 = %s WHERE id = %s",
        (int(pred_val), int(defect_no)))
    connection.commit()
    
#==============================================================================================================

def get_adaptive_sigma_refinement(length_percent):
    """
    Get refined sigma multipliers based on 5-part length percentage classification:
    1-10%, 10-20%, 20-30%, 30-40%, 40%+
    """
    if 1 <= length_percent < 10:
        sigma_multiplier = 0.6      # Less aggressive for very small defects
        refinement_factor = 1.2
        classification = "Very Small (1-10%)"
    elif 10 <= length_percent < 20:
        sigma_multiplier = 0.5   # Slightly more sensitive for small defects
        refinement_factor = 0.9
        classification = "Small (10-20%)"
    elif 20 <= length_percent < 30:
        sigma_multiplier = 1     # Standard sensitivity
        refinement_factor = 1.0
        classification = "Medium (20-30%)"
    elif 30 <= length_percent < 40:
        sigma_multiplier = 1.1      # Slightly less sensitive
        refinement_factor = 0.9
        classification = "Large (30-40%)"
    elif length_percent >= 40:
        sigma_multiplier = 1.2      # Less sensitive for largest defects
        refinement_factor = 0.8
        classification = "Very Large (40%+)"
    else:
        sigma_multiplier = 0.85
        refinement_factor = 1.15
        classification = "Below 1%"
    return sigma_multiplier, refinement_factor, classification

#==============================================================================================================

def get_adaptive_sigma_row_values(length_percent):

    """
    Adaptive row sigma multiplier based on both defect length percentage and signal contrast.
    Higher signal contrast → less strict (more sensors kept)
    Lower signal contrast → more strict (more sensors filtered)
    """

    # Default baseline value
    base_value = 0.45

    # Compute signal strength modifier
    signal_modifier = 0.9

    # Length-based adjustment
    if 1 <= length_percent < 10:
        base_value = 0.5
    elif 10 <= length_percent < 20:
        base_value = 1
    elif 20 <= length_percent < 30:
        base_value = 1.7
    elif 30 <= length_percent < 40:
        base_value = 1.7
    elif length_percent >= 40:
        base_value = 1
    else:
        base_value = 0.45  # Default

    # Final adaptive value
    adaptive_value = (base_value * signal_modifier)
    return adaptive_value


#==============================================================================================================

def get_type_defect_1(geometrical_parameter, length_defect, width_defect):
    L_ratio_W = length_defect / width_defect
    if width_defect > 3 * geometrical_parameter and length_defect > 3 * geometrical_parameter:
        type_of_defect = 'GENERAL'
        return type_of_defect
    elif (
            6 * geometrical_parameter >= width_defect >= 1 * geometrical_parameter and 6 * geometrical_parameter >= length_defect >= 1 * geometrical_parameter) and (
            0.5 < (L_ratio_W) < 2) and not (
            width_defect >= 3 * geometrical_parameter and length_defect >= 3 * geometrical_parameter):
        type_of_defect = 'PITTING'
        return type_of_defect
    elif (1 * geometrical_parameter <= width_defect < 3 * geometrical_parameter) and (L_ratio_W >= 2):
        type_of_defect = 'AXIAL GROOVING'
        return type_of_defect
    elif L_ratio_W <= 0.5 and 3 * geometrical_parameter > length_defect >= 1 * geometrical_parameter:
        type_of_defect = 'CIRCUMFERENTIAL GROOVING'
        return type_of_defect
    elif 0 < width_defect < 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
        type_of_defect = 'PINHOLE'
        return type_of_defect
    elif 0 < width_defect < 1 * geometrical_parameter and length_defect >= 1 * geometrical_parameter:
        type_of_defect = 'AXIAL SLOTTING'
        return type_of_defect
    elif width_defect >= 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
        type_of_defect = 'CIRCUMFERENTIAL SLOTTING'
        return type_of_defect

def internal_or_external(df_new_proximity, x):
    sensor_number = x + 1
    if sensor_number % 4 == 0:
        flapper_no = int(sensor_number / 4)
    else:
        flapper_no = int(sensor_number / 4) + 1
    proximity_no = flapper_no % 4
    if proximity_no == 0:
        proximity_no = 4
    proximity_index = 'F' + str(flapper_no) + 'P' + str(proximity_no)
    print("Proximity_index", proximity_index)
    maximum_depth_proximity_sensor = df_new_proximity[proximity_index]

    c = maximum_depth_proximity_sensor.tolist()
    minimum_value_proximity = min(c)
    mean_value_proximtiy = mean(c)

    print("mean_value_proximtiy", mean_value_proximtiy)
    print("minimum value of proximity", minimum_value_proximity)

    difference_mean = mean_value_proximtiy - minimum_value_proximity

    print("difference_minimum2", difference_mean)
    if difference_mean > 18000:
        type = "Internal"
        return type
    else:
        type = "External"
        return type

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

def breadth(start_sensor, end_sensor):
    start_sensor1 = start_sensor + 1
    end_sensor1 = end_sensor + 1
    if start_sensor1 > end_sensor1 or start_sensor1 == end_sensor1:
        return 0

    outer_diameter_1 = outer_dia
    thickness_1 = pipe_thickness
    inner_diameter_1 = outer_diameter_1 - 2 * (thickness_1)
    radius_1 = inner_diameter_1 / 2

    theta_2 = theta_ang1
    c_1 = math.radians(theta_2)
    theta_3 = theta_ang2
    d_1 = math.radians(theta_3)
    theta_4 = theta_ang3
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

# READ DATA AND PREPROCESSING
df = pd.read_pickle('D:/VDT/GMFL_12inch_22-01-2025_PTT(6)/3.pkl')

data_x = df.fillna(method='ffill')
df_new_proximity = pd.DataFrame(df, columns=['F1P1', 'F2P2', 'F3P3', 'F4P4', 'F5P1', 'F6P2', 'F7P3', 'F8P4',
                                             'F9P1', 'F10P2', 'F11P3', 'F12P4', 'F13P1', 'F14P2', 'F15P3', 'F16P4',
                                             'F17P1', 'F18P2', 'F19P3', 'F20P4', 'F21P1', 'F22P2', 'F23P3', 'F24P4',
                                             'F25P1', 'F26P2', 'F27P3', 'F28P4', 'F29P1', 'F30P2', 'F31P3', 'F32P4',
                                             'F33P1', 'F34P2', 'F35P3', 'F36P4'])

roll = data_x['ROLL'].tolist()
roll1 = []
for i in roll:
    roll1.append(i - (roll_ref))

roll_dictionary = {'1': roll1}
angle = [round(i*2.5, 1) for i in range(0, 144)]

for i in range(2, 145):
    current_values = [round((value + angle[i - 1]), 2) for value in roll1]
    roll_dictionary['{}'.format(i)] = current_values

clock_dictionary = {}
for key in roll_dictionary:
    clock_dictionary[key] = [degrees_to_hours_minutes2(value) for value in roll_dictionary[key]]

Roll_hr = pd.DataFrame(clock_dictionary)
Roll_hr.columns = [f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]

oddometer1 = ((data_x['ODDO1'] - oddo1_ref)/1000).round(3)
df3_raw = data_x[[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)]]
df2 = data_x[[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)]]

# ORIGINAL WORKING SIGMA CALCULATION
print("Calculating sigma thresholds using original proven method...")
mean1 = df2.mean().tolist()
standard_deviation = df2.std(axis=0, skipna=True).tolist()

mean_plus_1sigma = []
for i, data1 in enumerate(mean1):
    sigma1 = data1 + (positive_sigma_col) * standard_deviation[i]
    mean_plus_1sigma.append(sigma1)

mean_negative_3sigma = []
for i_2, data_3 in enumerate(mean1):
    sigma_3 = data_3 - (negative_sigma_col) * standard_deviation[i_2]
    mean_negative_3sigma.append(sigma_3)

# APPLY ORIGINAL FILTERING LOGIC
for col, data in enumerate(df2.columns):
    df2[data] = df2[data].apply(
        lambda x: 1 if x > mean_plus_1sigma[col] else (-1 if x < mean_negative_3sigma[col] else 0))

clock_cols = [f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]
df2.columns = clock_cols
filtered_df1 = df2

# CONTINUE WITH ORIGINAL PROCESSING
df3_raw.columns = filtered_df1.columns
df1_aligned = filtered_df1.reindex(df3_raw.index)
result = df1_aligned * df3_raw
result = result.dropna()
result.reset_index(drop=True, inplace=True)

result_raw_df = result.mask(result == 0, df3_raw)
result_raw_df = result_raw_df.dropna()
result_raw_df.reset_index(drop=True, inplace=True)

mean_clock_data = result_raw_df.mean().tolist()
val_ori_raw = ((result_raw_df - mean_clock_data)/mean_clock_data) * 100

# Save CSV for PTT Software
ptt_csv = result.copy()
ptt_csv['ODDO1'] = data_x['ODDO1']
prefix = '_x'
for col in Roll_hr.columns:
    ptt_csv[col + prefix] = Roll_hr[col]
for col in df_new_proximity.columns:
    ptt_csv[col] = df_new_proximity[col]

# ORIGINAL CLUSTERING IMPLEMENTATION
t = result.transpose()
t_raw = val_ori_raw.transpose()
data_array = t.to_numpy(dtype=np.float64)

def dfs(matrix, x, y, visited, cluster):
    """Perform DFS to find clusters, but only include positive values."""
    stack = [(x, y)]
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        if matrix[cx, cy] <= 0:
            continue
        visited.add((cx, cy))
        cluster.append((cx, cy))
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if (0 <= nx < matrix.shape[0] and 0 <= ny < matrix.shape[1] and
                    matrix[nx, ny] > 0 and (nx, ny) not in visited):
                stack.append((nx, ny))

# Find clusters of connected non-zero values and calculate bounding boxes
def merge_all_overlapping_boxes(boxes, max_distance=3):
    merged = []
    while boxes:
        current = boxes.pop(0)
        overlap_found = True
        while overlap_found:
            overlap_found = False
            i = 0
            while i < len(boxes):
                if do_boxes_overlap_or_close(current, boxes[i], max_distance):
                    current = merge_boxes(current, boxes[i])
                    boxes.pop(i)
                    overlap_found = True
                else:
                    i += 1
        merged.append(current)
    return merged

def do_boxes_overlap_or_close(box1, box2, max_distance=3):
    return do_boxes_overlap(box1, box2) or boxes_are_close(box1, box2, max_distance)

def boxes_are_close(box1, box2, max_distance=3):
    # Compute closest horizontal and vertical distances between boxes
    h_dist = max(0, max(box1['start_col'] - box2['end_col'], box2['start_col'] - box1['end_col']))
    v_dist = max(0, max(box1['start_row'] - box2['end_row'], box2['start_row'] - box1['end_row']))
    return (h_dist + v_dist) <= max_distance

def do_boxes_overlap(box1, box2):
    """Check if two bounding boxes overlap."""
    return not (box1['end_row'] < box2['start_row'] or
                box1['start_row'] > box2['end_row'] or
                box1['end_col'] < box2['start_col'] or
                box1['start_col'] > box2['end_col'])

def merge_boxes(box1, box2):
    """Merge two overlapping bounding boxes into one."""
    return {
        'start_row': min(box1['start_row'], box2['start_row']),
        'end_row': max(box1['end_row'], box2['end_row']),
        'start_col': min(box1['start_col'], box2['start_col']),
        'end_col': max(box1['end_col'], box2['end_col'])
    }

# CLUSTERING LOGIC
print("Performing clustering to detect defect regions...")
visited = set()
bounding_boxes = []

for i in range(data_array.shape[0]):
    for j in range(data_array.shape[1]):
        if data_array[i, j] != 0 and (i, j) not in visited:
            cluster = []
            dfs(data_array, i, j, visited, cluster)
            if cluster:
                min_row = min(point[0] for point in cluster)
                max_row = max(point[0] for point in cluster)
                min_col = min(point[1] for point in cluster)
                max_col = max(point[1] for point in cluster)
                bounding_boxes.append({'start_row': min_row, 'end_row': max_row, 'start_col': min_col, 'end_col': max_col})

# Merge overlapping boxes
# merged_boxes = []
# while bounding_boxes:
#     box = bounding_boxes.pop(0)
#     merged = False
#     for i in range(len(merged_boxes)):
#         if do_boxes_overlap(box, merged_boxes[i]):
#             merged_boxes[i] = merge_boxes(box, merged_boxes[i])
#             merged = True
#             break
#     if not merged:
#         merged_boxes.append(box)
merged_boxes = merge_all_overlapping_boxes(bounding_boxes)
df_sorted = pd.DataFrame(merged_boxes).sort_values(by='start_col')

# INITIALIZE VISUALIZATION
df_clock_holl_oddo1 = data_x['ODDO1']
oddo1_li = list(oddometer1)
sensor_numbers = list(range(1, len(t.index) + 1))  # 1 to 144
sensor_numbers = sensor_numbers[::-1]  # Reverse the list to go top=0 → bottom=144
# Create a 2D text matrix where each row has the same sensor number
text = np.array([[f"{sensor_no}"] * t.shape[1] for sensor_no in sensor_numbers])


figx112 = go.Figure(data=go.Heatmap(
    z=t_raw,
    y=t.index,
    x=[t.columns, oddo1_li],
    text = text,
    hovertemplate='Oddo: %{x}<br>Clock:%{y}<br>Value: %{z}, sensor no: %{text}',
    zmin=-5,
    zmax=18,
    colorscale='jet',
))

# CALCULATE THRESHOLD VALUES
print("Calculating threshold values for defect validation...")
max_submatrix_list = []
min_submatrix_list = []

for _, row in df_sorted.iterrows():
    start_sensor = row['start_row']
    end_sensor = row['end_row']
    start_reading = row['start_col']
    end_reading = row['end_col']
    if start_sensor == end_sensor:
        pass
    else:
        try:
            submatrix = result.iloc[start_reading:end_reading + 1, start_sensor:end_sensor + 1]
            submatrix = submatrix.apply(pd.to_numeric, errors='coerce')
            if submatrix.isnull().values.any():
                continue
            max_value = submatrix.max().max()
            max_submatrix_list.append(max_value)
            two_d_list = submatrix.values.tolist()
            min_positive = min(x for row in two_d_list for x in row if x > 0)
            min_submatrix_list.append(min_positive)
        except Exception as e:
            pass

max_of_all = max(max_submatrix_list)
min_of_all = min(min_submatrix_list)
threshold_value = round(min_of_all + (max_of_all - min_of_all) * defect_box_thresh)

print(f"Base threshold calculated: {threshold_value}")
print("Processing defects with 3-part length classification...")

# PROCESS DEFECTS WITH ADAPTIVE REFINEMENT
finial_defect_list = []
defect_counter = 1
submatrices_dict = {}

# Statistics tracking for each classification
classification_stats = {
    "Very Small (1-10%)": {"count": 0, "total_processed": 0},
    "Small (10-20%)": {"count": 0, "total_processed": 0},
    "Medium (20-30%)": {"count": 0, "total_processed": 0},
    "Large (30-40%)": {"count": 0, "total_processed": 0},
    "Very Large (40%+)": {"count": 0, "total_processed": 0},
    "Below 1%": {"count": 0, "total_processed": 0}
}
for _, row in df_sorted.iterrows():
    start_sensor = row['start_row']
    end_sensor = row['end_row']
    start_reading = row['start_col']
    end_reading = row['end_col']
    
    if start_sensor == end_sensor:
        continue
        
    try:
        submatrix = result.iloc[start_reading:end_reading + 1, start_sensor:end_sensor + 1]
        submatrix = submatrix.apply(pd.to_numeric, errors='coerce')
        two_d_list = submatrix.values.tolist()
        max_value = submatrix.max().max()
        min_positive = min(x for row in two_d_list for x in row if x > 0)
        
        # CALCULATE LENGTH_PERCENT FIRST
        counter_difference = end_reading-start_reading
        divid = int(counter_difference/2)
        center = start_reading+divid
        factor = divid*l_per1
        start = int(center-factor)
        end = int(center+factor)
        
        length_percent = (df_clock_holl_oddo1[end] - df_clock_holl_oddo1[start])
        
        # APPLY 3-PART ADAPTIVE REFINEMENT
        sigma_multiplier, refinement_factor, classification = get_adaptive_sigma_refinement(length_percent)
        adjusted_threshold = threshold_value * sigma_multiplier
        
        valid_columns = 0
        for col_idx in range(start_sensor, end_sensor + 1):
            adaptive_sigma = mean1[col_idx] + (sigma_multiplier * standard_deviation[col_idx])
            if submatrix.iloc[:, col_idx - start_sensor].max() > adaptive_sigma:
                valid_columns += 1
            if valid_columns/(end_sensor - start_sensor + 1) < 0.3:
                print(f"✗ Defect rejected: Only {valid_columns} columns passed adaptive threshold")
                continue
        # Track statistics
        classification_stats[classification]["total_processed"] += 1
        
        print(f"Defect {defect_counter}: Length={length_percent:.1f}mm, Class={classification}, Threshold={adjusted_threshold:.1f}")
        
        if (adjusted_threshold <= max_value <= max_of_all):
            print(f"✓ Defect accepted with {classification} settings")
            
            # CONTINUE WITH ALL ORIGINAL PROCESSING LOGIC
            depth_old = (max_value-min_positive)/min_positive*100
            max_column = submatrix.max().idxmax()
            max_index = submatrix.columns.get_loc(max_column)
            
            start_oddo1 = df_clock_holl_oddo1[start_reading]
            end_oddo1 = (df_clock_holl_oddo1[end_reading])/1000
            time_sec = end_reading/1500
            speed = end_oddo1/time_sec
            
            base_value = mean1[max_index]
            internal_external = internal_or_external(df_new_proximity, max_index)
            absolute_distance = df_clock_holl_oddo1[start_reading]
            upstream = df_clock_holl_oddo1[start_reading] - df_clock_holl_oddo1[0]
            length = (df_clock_holl_oddo1[end_reading] - df_clock_holl_oddo1[start_reading])
            
            counter_difference_1 = (end_sensor + 1) - (start_sensor + 1)
            divid_1 = int(counter_difference_1/2)
            center_1 = start_sensor + divid_1
            factor1_1 = divid_1 * w_per1
            start1_1 = (int(center_1 - factor1_1)) - 1
            end1_1 = (int(center_1 + factor1_1)) - 1
            
            width = breadth(start_sensor, end_sensor)
            
            geometrical_parameter = pipe_thickness
            dimension_classification = get_type_defect_1(geometrical_parameter, length, width)
            
            avg_counter = round((start+end)/2)
            avg_sensor = round((start1_1+end1_1)/2)
            orientation = Roll_hr.iloc[avg_counter, avg_sensor]
            
            inner_diameter = outer_dia - 2 * pipe_thickness
            radius = inner_diameter / 2
            x1 = round(radius * math.radians(theta_ang1), 1)
            y1 = round(radius * math.radians(theta_ang2), 1)
            z1 = round(radius * math.radians(theta_ang3), 1)

            df_copy_submatrix = df3_raw.iloc[start_reading:end_reading+1, start_sensor:end_sensor + 1]

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
            
            df_duplicate = replace_first_column(df_copy_submatrix, start_sensor, end_sensor)
            df_duplicate.columns = df_duplicate.columns.astype(str)
            
            def process_csv_interpolate(df_dupe):
                    """
                    Like the original process_csv, but uses interpolation (linear or cubic)
                    instead of duplication for the new columns. Suffixes and column names are
                    generated exactly as in the original code, with robust end-case handling.
                    """
                    new_data = {}
                    next_col = None

                    # Use your previously computed distances
                    base = round(x1 / div_factor)
                    c = round(y1 / div_factor)
                    dee = round(z1 / div_factor)

                    c1 = c // 2
                    c2 = c - c1
                    dee1 = dee // 2
                    dee2 = dee - dee1

                    def generate_suffixes(n):
                        return [chr(ord('a') + i) for i in range(int(n))]

                    base_suffixes = generate_suffixes(int(base))
                    c1_suffixes = generate_suffixes(int(c1))
                    c2_suffixes = generate_suffixes(int(c2))
                    dee1_suffixes = generate_suffixes(int(dee1))
                    dee2_suffixes = generate_suffixes(int(dee2))

                    for colu in df_dupe.columns:
                        col_int = int(colu)
                        next_col = str(col_int + 1)

                        if next_col in df_dupe.columns:
                            col_vals = df_dupe[colu].values
                            next_col_vals = df_dupe[next_col].values

                            def interpolate_between(a, b, n, kind='cubic'):
                                # For short arrays, always use linear
                                if n == 0:
                                    return np.empty((0, len(a)))
                                x = np.array([0, 1])
                                arr = np.vstack([a, b]).T
                                interpolated = []
                                for row in arr:
                                    # If both points are the same, just duplicate
                                    if np.allclose(row[0], row[1]):
                                        interpolated.append(np.full(n, row[0]))
                                        continue
                                    # Use cubic only if possible, otherwise linear
                                    if kind == 'cubic' and n >= 3:
                                        try:
                                            f = interp1d(x, row, kind='cubic', fill_value="extrapolate")
                                        except Exception:
                                            f = interp1d(x, row, kind='linear', fill_value="extrapolate")
                                    else:
                                        f = interp1d(x, row, kind='linear', fill_value="extrapolate")
                                    xs = np.linspace(0, 1, n + 2)[1:-1] if n > 0 else []
                                    interpolated.append(f(xs) if len(xs) > 0 else [])
                                return np.array(interpolated).T if n > 0 else np.empty((0, len(a)))

                            # Special Case 1: Between flappers (multiples of 4, not 16)
                            if col_int % 4 == 0 and col_int % 16 != 0:
                                c1_interp = interpolate_between(col_vals, next_col_vals, len(c1_suffixes), kind='cubic')
                                for idx, suffix in enumerate(c1_suffixes):
                                    new_data[f"{col_int}{suffix}_extra"] = c1_interp[idx] if c1_interp.shape[0] > 0 else col_vals
                                c2_interp = interpolate_between(next_col_vals, col_vals, len(c2_suffixes), kind='cubic')
                                for idx, suffix in enumerate(c2_suffixes):
                                    new_data[f"{int(next_col)}{suffix}_extra"] = c2_interp[idx] if c2_interp.shape[0] > 0 else next_col_vals

                            # Special Case 2: Between arms (multiples of 16)
                            elif col_int % 16 == 0:
                                dee1_interp = interpolate_between(col_vals, next_col_vals, len(dee1_suffixes), kind='cubic')
                                for idx, suffix in enumerate(dee1_suffixes):
                                    new_data[f"{col_int}{suffix}_extra2"] = dee1_interp[idx] if dee1_interp.shape[0] > 0 else col_vals
                                dee2_interp = interpolate_between(next_col_vals, col_vals, len(dee2_suffixes), kind='cubic')
                                for idx, suffix in enumerate(dee2_suffixes):
                                    new_data[f"{int(next_col)}{suffix}_extra2"] = dee2_interp[idx] if dee2_interp.shape[0] > 0 else next_col_vals

                            # Base case: Normal sensor spacing
                            else:
                                base_interp = interpolate_between(col_vals, next_col_vals, len(base_suffixes), kind='cubic')
                                for idx, suffix in enumerate(base_suffixes):
                                    new_data[f"{col_int}{suffix}"] = base_interp[idx] if base_interp.shape[0] > 0 else col_vals

                    new_df_duplicate = pd.DataFrame(new_data, index=df_dupe.index)
                    return new_df_duplicate
            
            def process_submatrix(df_diff):
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
                    #adaptive_sigma_row = get_adaptive_sigma_row_values(length_percent)
                    # ratio = round((max_val - min_pos_val) / (min_pos_val + 1e-5), 2)
                    # sigma_multiplier, _, _ = get_adaptive_sigma_refinement(length_percent)
                    #effective_positive_sigma_row = adaptive_sigma_row * positive_sigma_row

                    df_diff_mean = list(df_diff.median(axis=1))
                    df_std_dev = list(df_diff.std(axis=1, ddof=1))
                    mean_plus_std = list(map(lambda x, y: x + y * (positive_sigma_row), df_diff_mean, df_std_dev))
                    # mean_plus_std = list(map(lambda x, y: x * (positive_sigma_row), df_diff_mean, df_std_dev))
                    mean_plus_std_series = pd.Series(mean_plus_std, index=df_diff.index)
                    # mean_neg_std = list(map(lambda x, y: x - y * (negative_sigma_row), df_diff_mean, df_std_dev))
                    # mean_neg_std_series = pd.Series(mean_neg_std, index=df_diff.index)
                    # Apply the function row-wise
                    df_result = df_diff.apply(lambda row: row.map(lambda x: 1 if x > mean_plus_std_series[row.name] else 0), axis=1)

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

                    width_1_only = round(num_cols_with_ones * div_factor)
                    width_0_yes = round(num_cols_between * div_factor)
                    print("width_1_only", width_1_only)
                    print("width_0_yes", width_0_yes)
                    trimmed_original_matrix = df_diff.iloc[:, first_col_with_1_idx: last_col_with_1_idx + 1]
                    new_start_sensor = start1_1+num_cols_to_remove_start
                    new_end_sensor = end1_1-num_cols_to_remove_end
                    return trimmed_original_matrix, width_1_only, width_0_yes, new_start_sensor, new_end_sensor

            def slope_filter(df_diff):
                    refined_outputs = {}
                    width_0_no = 0
                    width_0_no1 = 0
                    try:
                        if df_diff.isnull().values.any():
                            return None
                        # q1 = df_diff.quantile(0.25)
                        # q3 = df_diff.quantile(0.75)
                        # iqr = q3 - q1
                        # iqr_threshold = iqr[iqr > 0].mean()
                        # important_cols_iqr = iqr[iqr > iqr_threshold].index
                        # refined_outputs['iqr'] = df_diff[important_cols_iqr]

                        slope_strength = df_diff.diff().abs().sum()
                        slope_threshold = slope_strength.mean() * (slope_per)
                        important_cols_slope = slope_strength[slope_strength > slope_threshold].index
                        refined_outputs['slope'] = df_diff[important_cols_slope]

                        width_0_no = (len(important_cols_slope) - 1) * div_factor
                        # width_0_no1 = (len(important_cols_iqr) - 1) * div_factor
                    except Exception as e:
                        refined_outputs['slope'] = None
                        # refined_outputs['iqr'] = None
                        print("Method failed:", e)
                    return refined_outputs, width_0_no

            modified_df = process_csv_interpolate(df_duplicate)
            refined_output, width_slope = slope_filter(modified_df)
            trimmed_matrix, width_1_only, width_0_yes, new_start_sensor, new_end_sensor = process_submatrix(modified_df)
            _,width_est,_,_,_ = process_submatrix_quantile(modified_df,quantile=0.9)
            print(trimmed_matrix.columns.to_list())
            new_start_sensor,new_end_sensor = get_first_last_integer_column(trimmed_matrix.columns)
            mapped_start_sensor = len(t.index) - start_sensor
            mapped_end_sensor = len(t.index) - end_sensor
            if mapped_end_sensor<mapped_start_sensor:
                mapped_start_sensor,mapped_end_sensor = mapped_end_sensor,mapped_start_sensor
                
            width = breadth(mapped_start_sensor,mapped_end_sensor)

            try:
                depth_val = round((((length / width) * (max_value / base_value))*100)/pipe_thickness)
            except:
                depth_val = 0
            
            if depth_val > 1 and width > 1 and length > 1:
                classification_stats[classification]["count"] += 1
                submatrices_dict[(defect_counter, start_sensor, end_sensor)] = modified_df
                
                print(f"✓ Valid defect: depth={depth_val}%, width={width}mm, length={length}mm")
                                
                 # ✅ ADD THIS LINE HERE: calculate hybrid width from trimmed matrix
                runid = 1
                finial_defect_list.append({
                        "runid": runid,
                        "start_reading": start_reading,
                        "end_reading": end_reading,
                        "start_sensor": mapped_start_sensor,
                        "end_sensor": mapped_end_sensor,
                        "absolute_distance": absolute_distance,
                        "upstream": upstream,
                        "length": length,
                        "length_percent": length_percent,
                        "breadth": width,
                        "width_statistical": width_est,  # ✅ Add this line
                        "width_new": width_slope,
                        "width_new2": round(width_1_only, 0),
                        "orientation": orientation,
                        "defect_type": internal_external,
                        "dimension_classification": dimension_classification,
                        "depth": depth_val,
                        "depth_old": depth_old,
                        "start_oddo1": start_oddo1,
                        "end_oddo1": end_oddo1,
                        "speed": speed,
                        "Min_Val": min_positive,
                        "Max_Val": max_value
                    })
                
                 # Color-code defects by classification
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
    
print(f"\nTotal submatrices stored: {len(submatrices_dict)}")
output_dir = os.path.join(os.getcwd(), "ptt-22-01-2025(6)")
manage_directory(output_dir)
os.makedirs(output_dir, exist_ok=True)
for (defect_id, start_sensor, start_sensor), matrix in submatrices_dict.items():
    filename = f"submatrix_ptt-1{defect_id, start_sensor, start_sensor}.csv"
    filepath = os.path.join(output_dir, filename)
    matrix.to_csv(filepath, index=False)
    # print(f"Saved {filename}")

# PRINT CLASSIFICATION STATISTICS
print(f"\n=== DEFECT CLASSIFICATION SUMMARY ===")
print(f"Total defects found: {len(finial_defect_list)}")
for classification, stats in classification_stats.items():
    if stats["total_processed"] > 0:
        acceptance_rate = (stats["count"] / stats["total_processed"]) * 100
        print(f"{classification}: {stats['count']}/{stats['total_processed']} defects ({acceptance_rate:.1f}% acceptance)")

# DATABASE INSERTION
print("\nInserting defects into database...")
with (connection.cursor() as cursor):
    for i in finial_defect_list:
        runid = i['runid']
        start_index = i['start_reading']
        end_index = i['end_reading']
        start_sensor = i['start_sensor']
        end_sensor = i['end_sensor']
        absolute_distance = round(i['absolute_distance'] / 1000, 3)
        upstream = round(i['upstream'] / 1000, 3)
        length = round(i['length'])
        length_percent = round(i['length_percent'])

        # Get corresponding trimmed_matrix (replace with your default if not found)
        trimmed_matrix = submatrices_dict.get((runid, start_sensor, end_sensor), pd.DataFrame())

        Width = round(i['breadth'])  
        width_statistical = round(i['width_statistical'])  
        width_new = round(i['width_new'])
        width_new2 = round(i['width_new2'])
        depth = round(i['depth'])
        depth_old = round(i['depth_old'])
        orientation = i['orientation']
        defect_type = i['defect_type']
        dimension_classification = i['dimension_classification']
        start_oddo1 = i['start_oddo1']
        end_oddo1 = i['end_oddo1']
        speed = round(i['speed'], 2)
        min_value = i['Min_Val']
        max_value = i['Max_Val']

        
        query_defect_insert = """
            INSERT INTO bbnew(runid, start_index, end_index, start_sensor, end_sensor, absolute_distance,
            upstream, length, length_percent, Width, width_new, width_new2, width_statistical,
            depth, depth_old, orientation, defect_type, dimension_classification, start_oddo1, end_oddo1, speed,
            Min_Val, Max_Val)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query_defect_insert, (
            int(runid), start_index, end_index, start_sensor, end_sensor, absolute_distance, upstream,
            length, length_percent, Width, width_new, width_new2, width_statistical,
            depth, depth_old, orientation, defect_type, dimension_classification,
            start_oddo1, end_oddo1, speed, min_value, max_value
        ))

        connection.commit()

model_width(model, output_dir)

# FINAL VISUALIZATION
figx112.update_layout(
    title='Heatmap with 3-Part Adaptive Length Classification (purple: 1-10%, Red : 10-20%, Orange: 20-30%, Yellow : 30-40%, Blue: 40%+)',
    xaxis_title='Odometer(m)',
    yaxis_title='Orientation'
)

print(f"\nProcessing complete! Found {len(finial_defect_list)} total defects using 3-part classification.")
print("Displaying visualization...")
figx112.show()
