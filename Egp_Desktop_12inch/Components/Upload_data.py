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
# client = bigquery.Client(credentials=credentials, project=project_id)
dataset_ref = client.dataset('Egp_raw_data')
table_ref = dataset_ref.table('Egp_1_copy')
# directory = 'D:/Battery_test1'


column_list = [['Serialno', 'ROLL', 'PITCH', 'YAW', 'ODDO1', 'ODDO1_SPEED', 'ODDO2', 'ODDO2_SPEED', 'VELOCITY',
                'BATTERY_PERCENTAGE',
                'BATTERY_VOLTAGE', 'TEMP1', 'TEMP2'],
               ['Serialno', 'proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5', 'proximity6'],
               ['Serialno', 'proximity7', 'proximity8', 'proximity9', 'proximity10', 'proximity11', 'proximity12'],
               ['Serialno', 'proximity13', 'proximity14', 'proximity15', 'proximity16', 'proximity17', 'proximity18']]


def break_into_chunks(list):
    number_of_list = 3
    n = round(len(list) / number_of_list)
    x = [list[i:i + n] for i in range(0, len(list), n)]
    if len(x) != number_of_list:
        x[number_of_list - 1] = x[number_of_list] + x[number_of_list - 1]
        x.pop(-1)
    return x

def main_thread(files, controller_list, directory, runid, directory_csv):
    count = 0
    print("process start")
    print(controller_list)
    start_time = time.ctime()
    for file in files:
        Dataframes = []
        for i, controller in enumerate(controller_list):
            if controller =='DAC_MAIN_MCU':
                df = pd.read_csv(directory + "\\" + controller + "\\" + file, names=column_list[i])
                last_column = column_list[i][-1]
                #print("Serial No:",df['Serialno'])
                df['Serialno'] = df['Serialno'].str.replace(r'\D', '').astype(int)
                df[last_column] = df[last_column].str.replace(r'\D', '').astype(int)
                df['filename'] = int(file.split('-')[1].split('.')[0])
                Dataframes.append(df)
            else:
                df = pd.read_csv(directory + "\\" + controller + "\\" + file, names=column_list[i])
                last_column = column_list[i][-1]
                df['filename'] = int(file.split('-')[1].split('.')[0])
                Dataframes.append(df)
        df_merged = reduce(lambda left, right: pd.merge(left, right, on=['filename', 'Serialno'],
                                                        how='outer'), Dataframes)
        df_merged['runid'] = runid
        df_merged.to_csv(directory_csv + '/' + file.split('.')[0] + ".csv")

        a = client.load_table_from_dataframe(df_merged, table_ref).result()
        if a:
            print("Data upload")

        else:
            print(" Data not upload")
    end_time = time.ctime()
    print("start:", start_time)
    print("end:", end_time)
    count += 1
    print("count", count)


def create_project_table(runid):
    #################### In google bigquery you can select project(datafusiontest-317009) inside the dataset(Raw_data_1) and tabel(Main_8_copy_1)
    #################### Remove the null rows in the table using the runid ##########
    ########### Create the New processed_data_id using Previous Raw_data ############
    processed_data_id='quantum-theme-334609.Egp_processed_data.' + 'Egp_copy_' + str(runid)
    query = 'create or replace table ' + processed_data_id + ' as SELECT * FROM `quantum-theme-334609.Egp_raw_data.Egp_1_copy` where runid={} AND proximity1  IS NOT NULL AND proximity2  IS NOT NULL ' \
                                                             'AND proximity3  IS NOT NULL AND proximity4  IS NOT NULL AND proximity5 IS NOT NULL AND proximity6 IS NOT NULL AND proximity7 IS NOT NULL AND proximity8 IS NOT NULL ' \
                                                             'AND proximity9 IS NOT NULL AND proximity10 IS NOT NULL AND proximity11 IS NOT NULL AND proximity12 IS NOT NULL AND proximity13 IS NOT NULL AND proximity14 IS NOT NULL AND ' \
                                                             'proximity15 IS NOT NULL AND proximity16 IS NOT NULL AND proximity17 IS NOT NULL AND proximity18 IS NOT NULL AND ODDO1 IS NOT NULL AND ODDO2 IS NOT NULL'
    runid_specific_table = client.query(query.format(runid))
    print("runid_specific_table", runid_specific_table)
    view_id = 'quantum-theme-334609.Egp_processed_data.' + 'Egp_1_copy_x' + str(runid)
    view = bigquery.Table(view_id)
    #################### You can create the view table using  processed_data_id and sorted by filename and Serialno and add new row index #######
    view.view_query = f"SELECT *, ROW_NUMBER() OVER (ORDER BY filename,Serialno) AS index FROM `{processed_data_id}` order by filename,Serialno"
    # Make an API request to create the view.
    client.create_table(view)



def upload_data(dir, runid):
    print("runid", runid)
    query = 'Delete FROM `quantum-theme-334609.Egp_raw_data.Egp_1_copy` where runid={}'
    delete_query_for_existing_record = client.query(query.format(runid))
    print("delete query executed", delete_query_for_existing_record)

    directory = dir
    # print(directory)
    file_list = []
    controller_list = []
    for controller in os.listdir(directory):
        controller_list.append(controller)
    pd.set_option('display.max_columns', 40)
    for files in os.listdir(directory + '\\' + controller_list[0]):
        file_list.append(files)

    file_list = break_into_chunks(file_list)

    print("Process start at : ", time.ctime())
    if __name__ == '__main__':
        freeze_support()
    else:
        freeze_support()
        directory_csv = os.path.join("D:/result/", str(runid))
        if os.path.exists(directory_csv):
            shutil.rmtree(directory_csv)
            print('deleted')
        os.makedirs(directory_csv)
        print('created')
    array_of_processes=[]
    for i,file in enumerate(file_list):
        process_obj=Process(target=main_thread, args=(file, controller_list, directory, runid, directory_csv))
        process_obj.start()
        array_of_processes.append(process_obj)
    print(array_of_processes)

    for process in array_of_processes:
        process.join()
    create_project_table(runid)
    print("Process end at : ", time.ctime())
