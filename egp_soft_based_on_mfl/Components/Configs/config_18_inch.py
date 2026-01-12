import json
import os
import pymysql
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox, QLabel
from google.oauth2 import service_account
from google.cloud import storage
# import Components.logger as logger
from datetime import datetime
from google.cloud import bigquery
from PyQt5.QtWebEngineWidgets import QWebEngineView

xyz = QWebEngineView
no_weld_indicator = False

connection = pymysql.connect(host='localhost', user='root', password='byy184', db='mfldesktop18')
credentials = service_account.Credentials.from_service_account_file('./utils/Authorization.json')
storage_client = storage.Client.from_service_account_json('./utils/GCS_Auth.json')
sensor_values = json.loads(open('./utils/sensor_value_update.json').read())

#Source table, project_id  configuration
source_dataset_id = 'Processed_data'
source_table_id = 'Main_8_copy_x58'
project_id = 'quantum-theme-334609'

#table configuration
table_name = project_id + '.'+source_dataset_id + '.'+source_table_id

#model configuration
model_location = r"D:\Anubhav\vdt_backend\GMFL_12_Inch_Desktop\backend_data\models WT5.5\ML_MODEL_PKL\rf_width_model.pkl"

#num of sensors, f_columns
num_of_sensors = 192
F_columns = int(num_of_sensors/4)

"""
Reference value will be consider
"""
oddo1 = 0
oddo2 = 0
roll_value = 0
pitch_value = 0
yaw_value = 0
pipe_thickness = 12.7

positive_sigma_col = 1.2
positive_sigma_row = 0.5
negative_sigma = 3
defect_box_thresh = 0.35

outer_dia = 457
#theta angle configuration
theta_ang1 = 1.1
theta_ang2 = 4.1
theta_ang3 = 9.7

w_per_1 = 0.55
oddo1_ref = 0
div_factor = 1.15
slope_per = 0.65

#degree, minute configuration
minute = 720/num_of_sensors
degree = minute/2

#location for folders
weld_pipe_pkl = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'DataFrames1') + '/'          #for line chart (counter v sensor) and pipe visualization(heatmap)
clock_pkl     = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'ClockDataFrames') + '/'      #for heatmap ( distance v orientation)
roll_pkl_lc   = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'DataFrames_rollLC') + '/'    #for line chart (absolute dist. vs orientation)
image_folder  = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'Charts') + '/'               #for saving charts/maps/graphs/plots

#l per configurations
""" <!----------    Different length percentages but not stored in db, only in front    ----------!>    """
l_per_1 = 0.76                               ##### 24% length percentage in clock heatmap calculation #####
l_per_2 = 0.74                              ##### 26% length percentage in clock heatmap calculation #####
l_per_3 = 0.72                              ##### 28% length percentage in clock heatmap calculation #####
l_per_4 = 0.70                              ##### 30% length percentage in clock heatmap calculation #####

client = bigquery.Client(credentials=credentials, project=project_id)
shared_dataset_ref = client.get_dataset(source_dataset_id)

print(shared_dataset_ref)
app = QtWidgets.QApplication([])
print("generated app ")
msg = QMessageBox()
print("mssage box created ")

#generarting hall sensor columns as list and string
sensor_columns_hall_sensor = [f"F{i}H{j}" for i in range(1, F_columns + 1) for j in range(1, 5)]

sensor_str_hall = ", ".join(sensor_columns_hall_sensor)

#generarting proximity sensor columns as list and string
sensor_columns_prox = [f"F{i}P{(i - 1) % 4 + 1}" for i in range(1, F_columns + 1)]
sensor_str_prox = ", ".join(sensor_columns_prox)

def error_msg(Title, Description):
    """
    Method that will show a alert box for Error
    :param Title: Title of the Box
    :param Description: Description of the Box
    :return: void type
    """
    set_msg_body(Title, Description, QMessageBox.Critical, "Critical")

def info_msg(Title, Description):
    set_msg_body(Title, Description, QMessageBox.Information, "Information")

def warning_msg(Title, Description):
    set_msg_body(Title, Description, QMessageBox.Warning, "Warning")

def set_msg_body(Title, Description, icon, WindowTitle):
    try:
        msg.setIcon(icon)
        msg.setText(Title)
        msg.setInformativeText(Description)
        msg.setWindowTitle(WindowTitle)
        msg.exec_()
        app.exec_()
    except OSError as error:
        # logger.log_error(error or "Set_msg_body method failed with unknown Error")
        pass

def print_with_time(msg):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(msg, dt_string)



def get_adaptive_sigma_refinement(length_percent):
    """
    Get refined sigma multipliers based on 5-part length percentage classification:
    1-10%, 10-20%, 20-30%, 30-40%, 40%+
    """
    if 1 <= length_percent < 10:
        sigma_multiplier = 0.5  # Less aggressive for very small defects
        refinement_factor = 0.8
        classification = "Very Small (1-10%)"
    elif 10 <= length_percent < 20:
        sigma_multiplier = 0.8  # Slightly more sensitive for small defects
        refinement_factor = 0.9
        classification = "Small (10-20%)"
    elif 20 <= length_percent < 30:
        sigma_multiplier = 1.1  # Standard sensitivity
        refinement_factor = 1.0
        classification = "Medium (20-30%)"
    elif 30 <= length_percent < 40:
        sigma_multiplier = 1.4  # Slightly less sensitive
        refinement_factor = 0.9
        classification = "Large (30-40%)"
    elif length_percent >= 40:
        sigma_multiplier = 1.6  # Less sensitive for largest defects
        refinement_factor = 0.8
        classification = "Very Large (40%+)"
    else:
        sigma_multiplier = 0.85
        refinement_factor = 1.15
        classification = "Below 1%"
    return sigma_multiplier, refinement_factor, classification