import math
from google.cloud import bigquery
import json
from statistics import mean
from egp_soft_based_on_mfl.Components.Configs import config_old as config

connection = config.connection
company_list = []  # list of companies
credentials = config.credentials
project_id = config.project_id
client = bigquery.Client(credentials=credentials, project=project_id)
# config = json.loads(open(r'D:\Anubhav\vdt_backend\egp_soft_based_on_mfl\utils\proximity_base_value.json').read())

def internal_or_external(df_new_proximity, x):
    sensor_number = x+1
    if sensor_number % 4 == 0:
        flapper_no = int(sensor_number / 4)
    else:
        flapper_no = int(sensor_number / 4) + 1

    proximity_no = flapper_no % 4
    if proximity_no == 0:
        proximity_no = 4
    proximity_index = 'F' + str(flapper_no) + 'P' + str(proximity_no)
    print("Proximity_index",proximity_index)
    maximum_depth_proximity_sensor = df_new_proximity[proximity_index]

    c = maximum_depth_proximity_sensor.tolist()
    minimum_value_proximity = min(c)
    mean_value_proximtiy=mean(c)

    print("mean_value_proximtiy", mean_value_proximtiy)
    print("minimum value of proximity",minimum_value_proximity)

    difference_mean = mean_value_proximtiy - minimum_value_proximity

    print("difference_minimum2", difference_mean)
    if difference_mean < 5000:
        type = "Internal"
        return type
    else:
        type = "External"
        return type




def lat_long(absolute_length, runid):
    with connection.cursor() as cursor:
        query = """
        SELECT id, runid, pipe_id, start_index, absolute_distance_oddo1, Latitude, Longitude 
        FROM dgps_segment 
        WHERE runid=%s
        ORDER BY absolute_distance_oddo1
        """
        cursor.execute(query, (runid,))
        result = cursor.fetchall()

    if not result:
        print(f"No data found for runid: {runid}")
        return None, None  # Ensures no unpacking error

    # Convert database result into a dictionary
    data_dict = {
        'id': [],
        'runid': [],
        'pipe_id': [],
        'start_index': [],
        'absolute_distance_oddo1': [],
        'Latitude': [],
        'Longitude': []
    }

    for row in result:
        data_dict['id'].append(row[0])
        data_dict['runid'].append(row[1])
        data_dict['pipe_id'].append(row[2])
        data_dict['start_index'].append(row[3])
        data_dict['absolute_distance_oddo1'].append(row[4])
        data_dict['Latitude'].append(row[5])
        data_dict['Longitude'].append(row[6])

    # Now using the same logic with the dynamically fetched data
    absolute_distances = data_dict['absolute_distance_oddo1']

    for j, distance in enumerate(absolute_distances):
        if absolute_length < distance:
            return data_dict['Longitude'][j], data_dict['Latitude'][j]

        elif distance < absolute_length and absolute_distances[j + 1] > absolute_length:
            A = distance
            B = absolute_distances[j + 1]
            C = absolute_length
            m = C - A
            n = B - C

            x1 = ((m * data_dict['Longitude'][j + 1]) + (n * data_dict['Longitude'][j])) / (m + n)
            y1 = ((m * data_dict['Latitude'][j + 1]) + (n * data_dict['Latitude'][j])) / (m + n)

            return x1, y1

        elif absolute_length > absolute_distances[j + 1]:
            if j == len(absolute_distances) - 2:
                return data_dict['Longitude'][j + 1], data_dict['Latitude'][j + 1]

    return None, None  # If no match is found, return (None, None)



def Width_calculation(start_sensor1, end_sensor1):
    start_sensor1, end_sensor1 = start_sensor1+1, end_sensor1+1
    if start_sensor1 > end_sensor1 or start_sensor1 == end_sensor1:
        return 0

    outer_diameter_1 = config.outer_dia  # 12-inch pipe
    thickness_1 = config.pipe_thickness  # Replace with Config.pipe_thickness if using from config
    inner_diameter_1 = outer_diameter_1 - 2 * (thickness_1)
    radius_1 = inner_diameter_1 / 2

    theta_2 = config.theta_ang1               # approximate value for both pipes
    c_1 = math.radians(theta_2)
    theta_3 = config.theta_ang2               # approximate value for both pipes
    d_1 = math.radians(theta_3)
    theta_4 = config.theta_ang3             # 9.97 for thickness 5.5 and 9.53 for thickness 7.1
    e_1 = math.radians(theta_4)  # Convert to radians
    # print("c1, d1", c_1, d_1)

    x1 = round(radius_1 * c_1, 1)
    y1 = round(radius_1 * d_1, 1)
    z1 = round(radius_1 * e_1, 1)  # Distance for sensors at multiples of 16
    print("x1, y1, z1", x1, y1, z1)

    bredth = 0
    i = start_sensor1
    while i < end_sensor1:
        # next_sensor = i + 1
        next_sensor = i
        if next_sensor % 16 == 0 and next_sensor != end_sensor1:
            bredth += z1
            # print(f"{i} → {next_sensor:<10} z1 (because {next_sensor} is a multiple of 16)")
        elif next_sensor % 4 == 0:  # If the next sensor is a multiple of 4 (but not 16)
            bredth += y1
            # print(f"{i} → {next_sensor:<10} (y1 - x1) (because {next_sensor} is a multiple of 4)")
        else:
            bredth += x1
            # print(f"{i} → {next_sensor:<10} x1")
        i += 1  # Move to the next sensor
    return bredth


def get_type_defect_1(geometrical_parameter,runid,length_defect,width_defect):
    L_ratio_W = length_defect / width_defect
    if width_defect > 3 * geometrical_parameter and length_defect > 3 * geometrical_parameter:
        type_of_defect = 'GENERAL'
        return type_of_defect
    elif (6 * geometrical_parameter >= width_defect >= 1 * geometrical_parameter and 6 * geometrical_parameter >= length_defect >= 1 * geometrical_parameter) and (
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