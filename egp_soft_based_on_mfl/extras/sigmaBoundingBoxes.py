import os
import plotly.graph_objs as go
import pandas as pd
import re
from scipy.ndimage import label, find_objects
import statistics
from datetime import datetime, timedelta
import numpy as np
from scipy.stats import gmean
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
import math
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pymysql
from statistics import mean
import plotly.io as pio
import cv2
from scipy.ndimage import binary_dilation, binary_erosion
from sklearn.cluster import DBSCAN
import warnings
warnings.filterwarnings('ignore')

connection = pymysql.connect(host='localhost', user='root', password='Thehero2004', db='vdt')

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
        sigma_multiplier = 0.9      # Slightly more sensitive for small defects
        refinement_factor = 1.1
        classification = "Small (10-20%)"
    elif 20 <= length_percent < 30:
        sigma_multiplier = 1.0      # Standard sensitivity
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
df = pd.read_pickle("D:/VDT/PTT_csv/GMFL_12inch_04-02-2025_PTT(6)/3.pkl")

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
        
        # APPLY 5-PART ADAPTIVE REFINEMENT
        sigma_multiplier, refinement_factor, classification = get_adaptive_sigma_refinement(length_percent)
        
        # LESS STRICT ADAPTIVE THRESHOLD VALIDATION
        valid_columns = 0
        total_columns = end_sensor - start_sensor + 1
        
        for col_idx in range(start_sensor, end_sensor + 1):
            # Calculate adaptive sigma1 for this column
            adaptive_sigma1 = mean1[col_idx] + sigma_multiplier * standard_deviation[col_idx]
            
            # Check if any value in this column exceeds the adaptive threshold
            if submatrix.iloc[:, col_idx - start_sensor].max() > adaptive_sigma1:
                valid_columns += 1
        
        # REDUCE THRESHOLD TO 30% OF COLUMNS (was 50%)
        if valid_columns / total_columns < 0.3:
            print(f"✗ Defect rejected: Only {valid_columns} columns passed adaptive threshold (need {int(total_columns * 0.3)})")
            continue
        
        adjusted_threshold = threshold_value * sigma_multiplier
        
        # Track statistics
        classification_stats[classification]["total_processed"] += 1
        
        print(f"Defect {defect_counter}: Length={length_percent:.1f}mm, Class={classification}, Threshold={adjusted_threshold:.1f}")
        
        if (adjusted_threshold <= max_value <= max_of_all):
            print(f"✓ Defect accepted with {classification} settings")
            
            # Continue with your existing processing logic...
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
            
            try:
                depth_val = round((((length / width) * (max_value / base_value))*100)/pipe_thickness)
            except:
                depth_val = 0
            
            if depth_val > 1 and width > 1 and length > 1:
                classification_stats[classification]["count"] += 1
                
                print(f"✓ Valid defect: depth={depth_val}%, width={width}mm, length={length}mm")
                
                runid = 1
                finial_defect_list.append(
                    {"runid": runid, "start_reading": start_reading, "end_reading": end_reading,
                     "start_sensor": start1_1, "end_sensor": end1_1, "absolute_distance": absolute_distance,
                     "upstream": upstream, "length": length, "length_percent": length_percent,
                     "breadth": width, 'width_new': 0, 'width_new2': 0,
                     'orientation': orientation, 'defect_type': internal_external,
                     "dimension_classification": dimension_classification, "depth": depth_val,
                     "depth_old": depth_old, "start_oddo1": start_oddo1, "end_oddo1": end_oddo1,
                     "speed": speed, "Min_Val": min_positive, "Max_Val": max_value,
                     "adaptive_threshold": adjusted_threshold, "sigma_multiplier": sigma_multiplier,
                     "length_classification": classification
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

# PRINT CLASSIFICATION STATISTICS
print(f"\n=== DEFECT CLASSIFICATION SUMMARY ===")
print(f"Total defects found: {len(finial_defect_list)}")
for classification, stats in classification_stats.items():
    if stats["total_processed"] > 0:
        acceptance_rate = (stats["count"] / stats["total_processed"]) * 100
        print(f"{classification}: {stats['count']}/{stats['total_processed']} defects ({acceptance_rate:.1f}% acceptance)")

# DATABASE INSERTION
print("\nInserting defects into database...")
with connection.cursor() as cursor:
    for i in finial_defect_list:
        runid = i['runid']
        start_index = i['start_reading']
        end_index = i['end_reading']
        start_sensor = i['start_sensor']
        end_sensor = i['end_sensor']
        absolute_distance = round(i['absolute_distance']/1000, 3)
        upstream = round(i['upstream']/1000, 3)
        length = round(i['length'])
        length_percent = round(i['length_percent'])
        Width = round(i['breadth'])
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
        
        query_defect_insert = "INSERT INTO defect_local_hm(runid, start_index, end_index, start_sensor, end_sensor, absolute_distance, upstream, length, length_percent, Width, width_new, width_new2, depth,depth_old, orientation, defect_type, dimension_classification, start_oddo1, end_oddo1, speed, Min_Val, Max_Val) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

        cursor.execute(query_defect_insert, (
            int(runid), start_index, end_index, start_sensor, end_sensor, absolute_distance, upstream,
            length, length_percent, Width, width_new, width_new2, depth, depth_old, orientation, 
            defect_type, dimension_classification, start_oddo1, end_oddo1, speed, min_value, max_value))

        connection.commit()

# FINAL VISUALIZATION
figx112.update_layout(
    title='Heatmap with 3-Part Adaptive Length Classification (purple: 1-10%, Red : 10-20%, Orange: 20-30%, Yellow : 30-40%, Blue: 40%+)',
    xaxis_title='Odometer(m)',
    yaxis_title='Orientation'
)

print(f"\nProcessing complete! Found {len(finial_defect_list)} total defects using 3-part classification.")
print("Displaying visualization...")
figx112.show()
