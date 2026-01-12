import json
import os
import pymysql
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLabel
from google.oauth2 import service_account
from google.cloud import storage
import Components.logger as logger
from datetime import datetime
from google.cloud import bigquery
from PyQt5.QtWebEngineWidgets import QWebEngineView
xyz=QWebEngineView
# print(xyz)
no_weld_indicator = False
connection = pymysql.connect(host='localhost', user='root', password='byy184', db='egp12inch')
credentials = service_account.Credentials.from_service_account_file('./utils/Authorization.json')
storage_client = storage.Client.from_service_account_json('./utils/GCS_Auth.json')
sensor_values = json.loads(open('./utils/sensor_value_update.json').read())
print(connection)
source_dataset_id = 'Egp_processed_data_12inch_without_time'
source_table_id = 'Egp_12_copy_x1'
project_id = 'quantum-theme-334609'
table_name = project_id + '.'+source_dataset_id + '.'+source_table_id
client = bigquery.Client(credentials=credentials, project=project_id)
shared_dataset_ref = client.get_dataset(source_dataset_id)
app = QtWidgets.QApplication([])
msg = QMessageBox()
"""
Reference value will be consider
"""
oddo1 = 1022.5864486
oddo2 = 0
oddo1_ref = oddo1
roll_value = -5.43
pipe_thickness = 5.5
# pkl_path = os.getcwd() + '/DataFrames/'
weld_pipe_pkl = os.getcwd() + '/DataFrames1/'
roll_pkl_lc = os.getcwd() + '/DataFrames_rollLC/'
clock_pkl = os.getcwd() + '/ClockDataFrames/'
pitch_value = 54
yaw_value = 23
num_of_sensors = 48
F_columns = int(num_of_sensors / 4)
minute = 720 / num_of_sensors
degree = minute / 2

positive_sigma_col = 1.70
positive_sigma_row = 0.45
negative_sigma = 3
defect_box_thresh = 0.25
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
        logger.log_error(error or "Set_msg_body method failed with unknown Error")


def print_with_time(msg):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(msg, dt_string)
