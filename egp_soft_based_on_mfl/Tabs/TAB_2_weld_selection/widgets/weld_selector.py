from matplotlib.widgets import RectangleSelector
# from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

import os, json
from google.cloud import bigquery
import matplotlib.pyplot as plt
import pandas as pd
from .helper_func import func, select_weld
from egp_soft_based_on_mfl.Components.Configs import config_old as config

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"D:\Anubhav\EGP_software\EGP_software\egp_soft_based_on_mfl\utils\GCS_Auth.json"
connection = config.connection
credentials = config.credentials
project_id = config.project_id
client = bigquery.Client(credentials=credentials, project=project_id)
# config = json.loads(open(r'D:\Anubhav\vdt_backend\egp_soft_based_on_mfl\utils\proximity_base_value.json').read())




def weld_selection(self):
    runid = self.parent.runid
    start15 = int(self.start15.text())
    end15 = int(self.end15.text())
    print(start15, end15)
    """
    Old Code
    """
    # query_for_start = 'SELECT * FROM ' + Config.table_name + ' WHERE index>{} AND index<{} AND runid={} order by index'
    # query_job = client.query(query_for_start.format(start15, end15, runid))
    # df_plot_data1 = query_job.result().to_dataframe()
    # print(df_plot_data1)
    """
    New Code
    """
    future = []
    config.print_with_time("Start_time")
    # executor = ProcessPoolExecutor(10)
    executor = ThreadPoolExecutor(max_workers=10)
    x = 20000
    while start15 < end15:
        future.append(executor.submit(func , self, [start15 + 1, start15 + x]))
        # print(start_index + 1, " ", start_index + x)
        start15 = start15 + x

    d1 = []
    for x in future:
        df = x.result()
        d1.append(df)

    df_plot_data1 = pd.concat(d1)

    index = df_plot_data1['index']
    self.figure_x15.clear()
    self.ax15 = self.figure_x15.add_subplot(111)

    # discards the old graph
    self.ax15.clear()
    res = self.config.sensor_columns_hall_sensor
    self.a2 = []
    for i, data in enumerate(res):
        self.ax15.plot(index, (df_plot_data1[data] + i * 1400).to_numpy(), label=i)
        self.a2.append(df_plot_data1[data] + i * 1400)
    self.ax15.set_ylabel('Hall Sensor')
    self.canvas_x15.draw()
    config.print_with_time("End_time")
    self.rs2 = RectangleSelector(self.ax15, lambda eclick, erelease: select_weld(self, eclick, erelease), useblit=True)
    plt.connect('key_press_event', self.rs2)



