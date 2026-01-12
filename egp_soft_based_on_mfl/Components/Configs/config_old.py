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

# connection = pymysql.connect(host='localhost', user='root', password='byy184', db='gmfldesktop12')
# credentials = service_account.Credentials.from_service_account_file('./utils/Authorization.json')
# storage_client = storage.Client.from_service_account_json('./utils/GCS_Auth.json')
# sensor_values = json.loads(open('./utils/sensor_value_update.json').read())
connection = pymysql.connect(host='localhost', user='root', password='byy184', db='mfldesktop')
credentials = service_account.Credentials.from_service_account_file('./utils/Authorization.json')
storage_client = storage.Client.from_service_account_json('./utils/GCS_Auth.json')
sensor_values = json.loads(open('./utils/sensor_value_update.json').read())


#Source table, project_id  configuration
# source_dataset_id = 'Processed_data_12inch_gmfl_without_time'
# source_table_id = 'Main_12_copy_x18'
# project_id = 'quantum-theme-334609'
source_dataset_id = 'Processed_data'
source_table_id = 'Main_8_copy_x58'
project_id = 'quantum-theme-334609'

#table configuration
table_name = project_id + '.'+source_dataset_id + '.'+source_table_id

#model configuration
# model_location = r"D:\Anubhav\vdt_backend\GMFL_12_Inch_Desktop\backend_data\models WT5.5\ML_MODEL_PKL\rf_width_model.pkl"
model_location = r"D:\Anubhav\vdt_backend\GMFL_12_Inch_Desktop\backend_data\models WT5.5\ML_MODEL_PKL\rf_width_model.pkl"
#num of sensors, f_columns
num_of_sensors = 96
F_columns = int(num_of_sensors/4)

"""
Reference value will be consider
"""
# oddo1 = 828.294
# oddo2 = 0
oddo1 = -1018
oddo2 = 0

# roll_value = -43.00
# pitch_value = -1.94
# yaw_value = 79.23

roll_value = -15.09
pitch_value = 0.31
yaw_value = 69.0

# pipe_thickness = 7.1                    ##### pipe_thickness changed accoridng to pipes #####

pipe_thickness = 12.7

# positive_sigma_col = 1.70                   ##### positive sigma standard deviation for defect calculation in clock heatmap #####
# positive_sigma_row = 0.45                      ##### positive sigma standard deviation for defect calculation in clock heatmap #####
# negative_sigma = 3                          ##### negative sigma standard deviation for defect calculation in clock heatmap #####

positive_sigma_col = 1.2
positive_sigma_row = 0.5
negative_sigma = 3

# defect_box_thresh = 0.25
defect_box_thresh = 0.35

# outer_dia = 324
outer_dia = 219

w_per_1 = 0.55

oddo1_ref = -1018

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


#theta angle configuration
# theta_ang1 = 1.7
# theta_ang2 = 3.4
# theta_ang3 = 9.7
#
# width_angle1 = 1.7                         ################# 1.7 for 12 inch(7.1 WT) and 1.60 for 14 inch(14.3 WT) pipe #################
# width_angle2 = 3.4                         ################# 3.4 for 12 inch(7.1 WT) and 3.19 for 14 inch(14.3 WT) #################
# width_angle3 = 9.7                        ################# 9.7 for 12 inch(7.1 WT) and 11.32 for 14 inch(14.3 WT) #################

theta_ang1 = 2.6
theta_ang2 = 6.2
theta_ang3 = 11.1

# width_angle1 = 2.6
# width_angle2 =6.2
# width_angle3 = 11.1


client = bigquery.Client(credentials=credentials, project=project_id)
shared_dataset_ref = client.get_dataset(source_dataset_id)


print(shared_dataset_ref)
app = QtWidgets.QApplication([])
print("generated app ")
msg = QMessageBox()
print("mssage box created ")



# Dynamically generate all sensor columns for hall sensors
sensor_columns_hall_sensor = [f"F{i}H{j}" for i in range(1, F_columns + 1) for j in range(1, 5)]

sensor_str_hall = ", ".join(sensor_columns_hall_sensor)

#generarting proximity sensor columns
sensor_columns_prox = [f"F{i}P{(i - 1) % 4 + 1}" for i in range(1, F_columns + 1)]
sensor_str_prox = ", ".join(sensor_columns_prox)


# query_for_start = 'SELECT index,ROLL,ODDO1,ODDO2,[F1H1, F1H2, F1H3, F1H4, F2H1, F2H2, F2H3, F2H4,F3H1, F3H2, F3H3, F3H4, F4H1, F4H2, F4H3,F4H4, F5H1, F5H2, F5H3, F5H4, F6H1, F6H2, F6H3, F6H4,F7H1, F7H2, F7H3, F7H4, F8H1, F8H2, F8H3, F8H4, F9H1, F9H2, F9H3, F9H4, F10H1,F10H2, F10H3, F10H4,F11H1, F11H2, F11H3, F11H4, F12H1, F12H2, F12H3, F12H4, F13H1, F13H2, F13H3,F13H4, F14H1, F14H2, F14H3, F14H4,F15H1, F15H2, F15H3, F15H4, F16H1, F16H2, F16H3, F16H4, F17H1, F17H2, F17H3,F17H4, F18H1, F18H2, F18H3, F18H4,F19H1, F19H2, F19H3, F19H4, F20H1, F20H2, F20H3, F20H4, F21H1, F21H2, F21H3,F21H4, F22H1, F22H2, F22H3, F22H4,F23H1, F23H2, F23H3, F23H4, F24H1, F24H2, F24H3, F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4,F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1,F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4],PITCH,YAW FROM ' + Config.table_name + ' WHERE index>{} AND index<{} order by index'

# query_for_start = (
#                         "SELECT index, ROLL, ODDO1, ODDO2, ["
#                         + Config.sensor_str_hall +
#                         "], PITCH, YAW FROM "
#                         + Config.table_name +
#                         " WHERE index>{} AND index<{} ORDER BY index"
#                 )









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









#
# import json
# import os
# import pymysql
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import *
# from PyQt5.QtWidgets import QMessageBox, QLabel
# from google.oauth2 import service_account
# from google.cloud import storage
# # import Components.logger as logger
# from datetime import datetime
# from google.cloud import bigquery
# from PyQt5.QtWebEngineWidgets import QWebEngineView
#
#
# xyz = QWebEngineView
# no_weld_indicator = False
#
# connection = pymysql.connect(host='localhost', user='root', password='byy184', db='gmfldesktop12')
# credentials = service_account.Credentials.from_service_account_file('./utils/Authorization.json')
# storage_client = storage.Client.from_service_account_json('./utils/GCS_Auth.json')
# sensor_values = json.loads(open('./utils/sensor_value_update.json').read())
#
#
# #Source table, project_id  configuration
# source_dataset_id = 'Processed_data_12inch_gmfl_without_time'
# source_table_id = 'Main_12_copy_x18'
# project_id = 'quantum-theme-334609'
#
# #table configuration
# table_name = project_id + '.'+source_dataset_id + '.'+source_table_id
#
# #model configuration
# model_location = r"D:\Anubhav\vdt_backend\GMFL_12_Inch_Desktop\backend_data\models WT5.5\ML_MODEL_PKL\rf_width_model.pkl"
#
# #num of sensors, f_columns
# num_of_sensors = 144
# F_columns = int(num_of_sensors/4)
#
# """
# Reference value will be consider
# """
# oddo1 = 828.294
# oddo2 = 0
#
#
# roll_value = -43.00
# pitch_value = -1.94
# yaw_value = 79.23
#
#
# pipe_thickness = 7.1                    ##### pipe_thickness changed accoridng to pipes #####
#
#
# positive_sigma_col = 1.70                   ##### positive sigma standard deviation for defect calculation in clock heatmap #####
# positive_sigma_row = 0.45                      ##### positive sigma standard deviation for defect calculation in clock heatmap #####
# negative_sigma = 3                          ##### negative sigma standard deviation for defect calculation in clock heatmap #####
#
#
#
# defect_box_thresh = 0.25
#
#
# outer_dia = 324
#
# w_per_1 = 0.55
#
# oddo1_ref = -1018
#
# div_factor = 1.15
#
# slope_per = 0.65
#
#
# #degree, minute configuration
# minute = 720/num_of_sensors
# degree = minute/2
#
#
# #location for folders
# weld_pipe_pkl = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'DataFrames1') + '/'          #for line chart (counter v sensor) and pipe visualization(heatmap)
# clock_pkl     = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'ClockDataFrames') + '/'      #for heatmap ( distance v orientation)
# roll_pkl_lc   = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'DataFrames_rollLC') + '/'    #for line chart (absolute dist. vs orientation)
# image_folder  = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'Charts') + '/'               #for saving charts/maps/graphs/plots
#
#
#
# #l per configurations
# """ <!----------    Different length percentages but not stored in db, only in front    ----------!>    """
# l_per_1 = 0.76                               ##### 24% length percentage in clock heatmap calculation #####
# l_per_2 = 0.74                              ##### 26% length percentage in clock heatmap calculation #####
# l_per_3 = 0.72                              ##### 28% length percentage in clock heatmap calculation #####
# l_per_4 = 0.70                              ##### 30% length percentage in clock heatmap calculation #####
#
#
# #theta angle configuration
# theta_ang1 = 1.7
# theta_ang2 = 3.4
# theta_ang3 = 9.7
#
#
#
#
# client = bigquery.Client(credentials=credentials, project=project_id)
# shared_dataset_ref = client.get_dataset(source_dataset_id)
#
#
# print(shared_dataset_ref)
# app = QtWidgets.QApplication([])
# print("generated app ")
# msg = QMessageBox()
# print("mssage box created ")
#
#
#
# # Dynamically generate all sensor columns for hall sensors
# sensor_columns_hall_sensor = [f"F{i}H{j}" for i in range(1, F_columns + 1) for j in range(1, 5)]
#
# sensor_str_hall = ", ".join(sensor_columns_hall_sensor)
#
# #generarting proximity sensor columns
# sensor_columns_prox = [f"F{i}P{(i - 1) % 4 + 1}" for i in range(1, F_columns + 1)]
# sensor_str_prox = ", ".join(sensor_columns_prox)
#
#
# # query_for_start = 'SELECT index,ROLL,ODDO1,ODDO2,[F1H1, F1H2, F1H3, F1H4, F2H1, F2H2, F2H3, F2H4,F3H1, F3H2, F3H3, F3H4, F4H1, F4H2, F4H3,F4H4, F5H1, F5H2, F5H3, F5H4, F6H1, F6H2, F6H3, F6H4,F7H1, F7H2, F7H3, F7H4, F8H1, F8H2, F8H3, F8H4, F9H1, F9H2, F9H3, F9H4, F10H1,F10H2, F10H3, F10H4,F11H1, F11H2, F11H3, F11H4, F12H1, F12H2, F12H3, F12H4, F13H1, F13H2, F13H3,F13H4, F14H1, F14H2, F14H3, F14H4,F15H1, F15H2, F15H3, F15H4, F16H1, F16H2, F16H3, F16H4, F17H1, F17H2, F17H3,F17H4, F18H1, F18H2, F18H3, F18H4,F19H1, F19H2, F19H3, F19H4, F20H1, F20H2, F20H3, F20H4, F21H1, F21H2, F21H3,F21H4, F22H1, F22H2, F22H3, F22H4,F23H1, F23H2, F23H3, F23H4, F24H1, F24H2, F24H3, F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4,F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1,F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4],PITCH,YAW FROM ' + Config.table_name + ' WHERE index>{} AND index<{} order by index'
#
# # query_for_start = (
# #                         "SELECT index, ROLL, ODDO1, ODDO2, ["
# #                         + Config.sensor_str_hall +
# #                         "], PITCH, YAW FROM "
# #                         + Config.table_name +
# #                         " WHERE index>{} AND index<{} ORDER BY index"
# #                 )
#
#
#
#
#
#
#
#
#
# def error_msg(Title, Description):
#     """
#     Method that will show a alert box for Error
#     :param Title: Title of the Box
#     :param Description: Description of the Box
#     :return: void type
#     """
#     set_msg_body(Title, Description, QMessageBox.Critical, "Critical")
#
#
# def info_msg(Title, Description):
#     set_msg_body(Title, Description, QMessageBox.Information, "Information")
#
#
# def warning_msg(Title, Description):
#     set_msg_body(Title, Description, QMessageBox.Warning, "Warning")
#
#
# def set_msg_body(Title, Description, icon, WindowTitle):
#     try:
#         msg.setIcon(icon)
#         msg.setText(Title)
#         msg.setInformativeText(Description)
#         msg.setWindowTitle(WindowTitle)
#         msg.exec_()
#         app.exec_()
#     except OSError as error:
#         # logger.log_error(error or "Set_msg_body method failed with unknown Error")
#         pass
#
# def print_with_time(msg):
#     now = datetime.now()
#     dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#     print(msg, dt_string)
#


