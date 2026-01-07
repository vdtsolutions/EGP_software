import pandas as pd
import os
from functools import reduce
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import time
from multiprocessing import Process, freeze_support
import multiprocessing
import shutil
import Components.config as Config

credentials = Config.credentials
project_id = Config.project_id
client = bigquery.Client(credentials=credentials, project=project_id)
#print(client)
# client = bigquery.Client(credentials=credentials, project=project_id)
############ You can create the Egp_raw_data(dataset) and create table(Egp_1_copy) in google bigquery manually##########
dataset_ref = client.dataset('Egp_raw_data')
table_ref = dataset_ref.table('Egp_1_copy')
runid=1
processed_data_id='datafusiontest-317009.Egp_processed_data.' + 'Egp_copy_' + str(runid)
############### You can create the dataset(Egp_processed_data) in google bigquery manually but table create automatically(Egp_copy_+runid)############
query ='create or replace table '+ processed_data_id +' as SELECT * FROM `datafusiontest-317009.Egp_raw_data.Egp_1_copy` where runid={} AND proximity1 IS NOT NULL AND proximity2 IS NOT NULL AND proximity3 IS NOT NULL AND proximity4 IS NOT NULL AND proximity5 IS NOT NULL AND proximity6 IS NOT NULL AND proximity7 IS NOT NULL AND proximity8 IS NOT NULL AND proximity9 IS NOT NULL AND proximity10 IS NOT NULL AND proximity11 IS NOT NULL AND proximity12 IS NOT NULL AND proximity13 IS NOT NULL AND proximity14 IS NOT NULL AND proximity15 IS NOT NULL AND proximity16 IS NOT NULL AND proximity17 IS NOT NULL AND proximity18 IS NOT NULL AND ODDO1 IS NOT NULL AND ODDO2 IS NOT NULL'
print(type(runid))
runid_specific_table = client.query(query.format(runid))
print("runid_specific_table", runid_specific_table)
view_id = 'datafusiontest-317009.Egp_processed_data.' + 'Egp_1_copy_x' + str(runid)
view = bigquery.Table(view_id)

#################### You can create the view table using  processed_data_id and sorted by filename and Serialno and add new row index #######
view.view_query = f"SELECT *, ROW_NUMBER() OVER (ORDER BY filename,Serialno) AS index FROM `{processed_data_id}` order by filename,Serialno"
# Make an API request to create the view.

view1=client.create_table(view)
print(view1)

