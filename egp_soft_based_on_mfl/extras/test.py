import pandas as pd

df = pd.read_pickle("C:/Users/admin/PycharmProjects/GMFL_12_Inch_Desktop/rf_width_model.pkl")

df1 = pd.DataFrame(df)
print(df1)
df1.to_csv("C:/Users/admin/PycharmProjects/GMFL_12_Inch_Desktop/abhchd.csv")




# import pandas as pd
# import os
# from functools import reduce
# from google.oauth2 import service_account
# from google.cloud import bigquery
# import pandas as pd
# import plotly.express as px
# import time
# import plotly.graph_objs as go
# import numpy as np
# from multiprocessing import Process, freeze_support
# import multiprocessing
# import shutil
# import Components.config as Config
#
# credentials = Config.credentials
# project_id = Config.project_id
# client = bigquery.Client(credentials=credentials, project=project_id)
# runid=54
#
# ###################### Magnetization Api ###################
# # query_for_start = 'SELECT ODDO1,ODDO2 FROM ' + Config.table_name + ' WHERE runid={}'
# # query_job = client.query(query_for_start.format(runid))
# # results_start = query_job.result()
# # oddo1 = []
# # oddo2 = []
# # for row in results_start:
# #     # print(row)
# #     oddo1.append(row['ODDO1'])
# #     oddo2.append(row['ODDO2'])
# # i=0
# # x_oddo2=dict()
# # y_sensor=dict()
# # for j,data in enumerate(oddo2):
# #     if j==i+10000:
# #         x_oddo2[j]=data
# #         query_for_start = 'SELECT [F1H1, F1H2, F1H3, F1H4,F2H1, F2H2, F2H3, F2H4,F3H1, F3H2, F3H3, F3H4,F4H1, F4H2, F4H3,F4H4,F5H1, F5H2, F5H3, F5H4,F6H1, F6H2, F6H3, F6H4,F7H1, F7H2, F7H3, F7H4,F8H1, F8H2, F8H3, F8H4, F9H1, F9H2, F9H3, F9H4,F10H1, F10H2, F10H3, F10H4,F11H1, F11H2, F11H3, F11H4,F12H1, F12H2, F12H3, F12H4,F13H1, F13H2, F13H3, F13H4,F14H1, F14H2, F14H3, F14H4,F15H1, F15H2, F15H3, F15H4,F16H1, F16H2, F16H3, F16H4,F17H1, F17H2, F17H3, F17H4,F18H1, F18H2, F18H3, F18H4,F19H1, F19H2, F19H3, F19H4,F20H1, F20H2, F20H3, F20H4,F21H1, F21H2, F21H3, F21H4,F22H1, F22H2, F22H3, F22H4,F23H1, F23H2, F23H3, F23H4,F24H1, F24H2, F24H3, F24H4] FROM ' + Config.table_name + ' WHERE index={} order by index'
# #         query_job = client.query(query_for_start.format(j))
# #         results_1 = query_job.result()
# #         for row1 in results_1:
# #             y_sensor[j]=np.mean(row1[0])
# #         i=i+10000
# # print("oddo2",x_oddo2)
# # print("sensor",y_sensor)
# # list1 = list(x_oddo2.items())
# # list2=list(y_sensor.items())
# # x1=[]
# # y1=[]
# # x2=[]
# # y2=[]
# # for i in list1:
# #     x1.append(i[0])
# #     y1.append(i[1])
# # for j in list2:
# #     x2.append(j[0])
# #     y2.append(j[1])
# # print(x1)
# # print(y1)
# # print(x2)
# # print(y2)
# ########################### end of Magnetization Api ##########################
#
#
#
# # client = bigquery.Client(credentials=credentials, project=project_id)
# # dataset_ref = client.dataset('Raw_data')
# # table_ref = dataset_ref.table('Main_8_copy')
# # runid=27
# # processed_data_id = 'datafusiontest-273706.Processed_data.' + 'Main_8_copy_' + str(runid)
# # view_id = 'datafusiontest-273706.Processed_data.' + 'Main_8_copy_x' + str(runid)
# # view = bigquery.Table(view_id)
# # print("<<<<<<<<<<<<<<<<<<")
# # view.view_query = f"SELECT *, ROW_NUMBER() OVER (ORDER BY filename,Serialno) AS index FROM `{processed_data_id}` " \
# #                   f"order by filename,Serialno "
# # #view.view_query = f"SELECT * FROM `{processed_data_id}`"
# #
# # # Make an API request to create the view.
# # view = client.create_table(view)
# # print(f"Created {view.table_type}: {str(view.reference)}")