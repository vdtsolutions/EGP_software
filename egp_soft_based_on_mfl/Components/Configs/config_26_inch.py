import json
import os
import pymysql
from datetime import datetime
from google.oauth2 import service_account
from google.cloud import storage
from google.cloud import bigquery
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView

# -----------------------------------------
# GLOBAL CONSTANTS (SAFE FOR BOTH GUI + WORKERS)
# -----------------------------------------

xyz = QWebEngineView
no_weld_indicator = False

# DB / GCP / GUI — will be initialized lazily inside init_runtime()
connection = None
credentials = None
storage_client = None
client = None
shared_dataset_ref = None
sensor_values = None
app = None
msg = None

#localdb connection for mysql
host = 'localhost'
user='root'
password='byy184'
db_mysql='egp12inch'

# Source & table configuration
source_dataset_id = 'Egp_26inch_processed_data'
source_table_id = 'Egp_26_copy_x1'
project_id = 'quantum-theme-334609'
table_name = f"{project_id}.{source_dataset_id}.{source_table_id}"



# Number of sensors
num_of_sensors = 48
F_columns = int(num_of_sensors / 4)

# Reference values
oddo1 = 1029.4711
oddo2 = 0
roll_value = -17.08
pitch_value = -1.15
yaw_value = 75.91
oddo1_ref = oddo1
# Pipe configefewflol
pipe_thickness = 5.5
outer_dia = 324

# Sigma values
positive_sigma_col = 1.70
positive_sigma_row = 0.45
negative_sigma = 3
defect_box_thresh = 0.25

# Sliding window / geometrical constants
w_per_1 = 0.55

div_factor = 1.15
slope_per = 0.65

# Degree/minute config
minute = 720 / num_of_sensors
degree = minute / 2

# Depth calculation config
scaling_exponent = 2.9
calibration_factor = 0.82
min_energy_threshold = 1e-6



# Length percentage constants
l_per_1 = 0.76
l_per_2 = 0.74
l_per_3 = 0.72
l_per_4 = 0.70

# Theta angle configuration
theta_ang1 = 1.7
theta_ang2 = 3.4
theta_ang3 = 9.7


#variable based on inch type
def get_adaptive_sigma_refinement(length_percent):
    """
    Returns sigma multiplier + refinement + classification
    based on 5-part defect length categorization.
    """
    if 1 <= length_percent < 10:
        return 0.6, 1.2, "Very Small (1-10%)"
    elif 10 <= length_percent < 20:
        return 0.5, 0.9, "Small (10-20%)"
    elif 20 <= length_percent < 30:
        return 1.0, 1.0, "Medium (20-30%)"
    elif 30 <= length_percent < 40:
        return 1.1, 0.9, "Large (30-40%)"
    elif length_percent >= 40:
        return 1.2, 0.8, "Very Large (40%+)"
    else:
        return 0.85, 1.15, "Below 1%"







#-----------FUNCTIONNS AND VARIABLES THAT NEED NOT TO BE CHANGE AND SHOULD BE IN EVERY CONFIG--------------------

# Folder locations
weld_pipe_pkl = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'DataFrames1') + '/'
clock_pkl = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'ClockDataFrames') + '/'
roll_pkl_lc = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'DataFrames_rollLC') + '/'
image_folder = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'Charts') + '/'

# Model configuration
model_location = os.path.join(
    os.getcwd(),
    'egp_soft_based_on_mfl',
    'backend_data',
    'models_ML',
    'ML_MODEL_PKL',
    'rf_width_model.pkl'
)

# Dynamically generate sensor columns
sensor_columns_hall_sensor = [
    f"F{i}H{j}" for i in range(1, F_columns + 1) for j in range(1, 4 + 1)
]
sensor_str_hall = ", ".join(sensor_columns_hall_sensor)

sensor_columns_prox = [
    f"F{i}P{((i - 1) % 4) + 1}" for i in range(1, F_columns + 1)
]
sensor_str_prox = ", ".join(sensor_columns_prox)

# -----------------------------------------------------
#               🔥 RUNTIME INITIALIZATION
# -----------------------------------------------------

def init_runtime():
    """
    Initialize ALL heavy components:
    - MySQL DB
    - GCP Storage Client
    - BigQuery Client
    - Sensor JSON
    - QApplication + QMessageBox

    SAFE: GUI calls this ONCE.
    WORKERS SHOULD NEVER CALL THIS.
    """
    global connection, credentials, storage_client
    global client, shared_dataset_ref
    global sensor_values, app, msg

    # Already initialized
    if client is not None:
        return

    # Load sensor JSON
    with open('./utils/sensor_value_update.json', 'r') as f:
        sensor_values = json.load(f)

    # DB connection
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db_mysql
    )

    # GCP clients
    credentials = service_account.Credentials.from_service_account_file('./utils/Authorization.json')
    storage_client = storage.Client.from_service_account_json('./utils/GCS_Auth.json')

    # BigQuery
    client = bigquery.Client(credentials=credentials, project=project_id)
    shared_dataset_ref = client.get_dataset(source_dataset_id)
    print(shared_dataset_ref)

    # Qt (GUI only)
    app = QtWidgets.QApplication([])
    print("generated app")
    msg = QMessageBox()
    print("mssage box created")


# -----------------------------------------------------
#               💬 MESSAGE BOX HELPERS
# -----------------------------------------------------

def set_msg_body(Title, Description, icon, WindowTitle):
    global app, msg
    try:
        if app is None or msg is None:
            init_runtime()  # GUI fallback

        msg.setIcon(icon)
        msg.setText(Title)
        msg.setInformativeText(Description)
        msg.setWindowTitle(WindowTitle)
        msg.exec_()
    except Exception:
        pass

def error_msg(Title, Description):
    set_msg_body(Title, Description, QMessageBox.Critical, "Critical")

def info_msg(Title, Description):
    set_msg_body(Title, Description, QMessageBox.Information, "Information")

def warning_msg(Title, Description):
    set_msg_body(Title, Description, QMessageBox.Warning, "Warning")


# -----------------------------------------------------
#               ⏱️ UTIL FUNCTIONS
# -----------------------------------------------------

def print_with_time(message: str):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"{message} {now}")


