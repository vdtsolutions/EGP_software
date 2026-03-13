from datetime import datetime
import os

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMessageBox


xyz = QWebEngineView
no_weld_indicator = False

#folder locations for saving
weld_pipe_pkl = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'DataFrames1') + '/'
clock_pkl = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'ClockDataFrames') + '/'
roll_pkl_lc = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'DataFrames_rollLC') + '/'
image_folder = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'Charts') + '/'

google_earth_pro = "C:\Program Files\Google\Google Earth Pro\client\googleearth.exe"



# -----------------------------------------------------
#               💬 MESSAGE BOX HELPERS
# -----------------------------------------------------

def set_msg_body(Title, Description, icon, WindowTitle):
    try:
        msg = QMessageBox()
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

def reset_runtime():
    global connection, client, credentials, shared_dataset_ref
    global table_name, source_table_id

    connection = None
    client = None
    credentials = None
    shared_dataset_ref = None
    table_name = None
    source_table_id = None
