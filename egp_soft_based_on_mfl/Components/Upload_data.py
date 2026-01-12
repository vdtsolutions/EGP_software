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
from ..Components.Configs import config_old as Config

credentials = Config.credentials
project_id = Config.project_id
client = bigquery.Client(credentials=credentials, project=project_id)
# client = bigquery.Client(credentials=credentials, project=project_id)
dataset_ref = client.dataset('Raw_data_12inch_gmfl')
table_ref = dataset_ref.table('Main_12_copy')
# directory = 'D:/Battery_test1'


column_list = [['Serialno', 'ROLL', 'PITCH', 'YAW', 'ODDO1', 'ODDO1_SPEED', 'ODDO2', 'ODDO2_SPEED', 'VELOCITY',
                'BATTERY_PERCENTAGE',
                'BATTERY_VOLTAGE', 'TEMP1', 'TEMP2'],
               ['Serialno', 'F1H1', 'F1H2', 'F1H3', 'F1H4', 'F1P1', 'F2H1', 'F2H2', 'F2H3',
                'F2H4', 'F2P2', 'F3H1', 'F3H2', 'F3H3', 'F3H4', 'F3P3', 'F4H1', 'F4H2', 'F4H3',
                'F4H4', 'F4P4'],
               ['Serialno', 'F5H1', 'F5H2', 'F5H3', 'F5H4', 'F5P1', 'F6H1', 'F6H2', 'F6H3',
                                  'F6H4', 'F6P2', 'F7H1', 'F7H2', 'F7H3', 'F7H4', 'F7P3', 'F8H1', 'F8H2', 'F8H3',
                                  'F8H4', 'F8P4'],
               ['Serialno', 'F9H1', 'F9H2', 'F9H3', 'F9H4', 'F9P1', 'F10H1', 'F10H2', 'F10H3',
                    'F10H4', 'F10P2', 'F11H1', 'F11H2', 'F11H3', 'F11H4', 'F11P3', 'F12H1',
                'F12H2', 'F12H3', 'F12H4', 'F12P4'],
               ['Serialno', 'F13H1', 'F13H2', 'F13H3', 'F13H4', 'F13P1', 'F14H1', 'F14H2',
                'F14H3', 'F14H4', 'F14P2', 'F15H1', 'F15H2', 'F15H3', 'F15H4', 'F15P3',
                'F16H1', 'F16H2', 'F16H3', 'F16H4', 'F16P4'],
               ['Serialno', 'F17H1', 'F17H2', 'F17H3', 'F17H4', 'F17P1', 'F18H1', 'F18H2',
                'F18H3', 'F18H4', 'F18P2', 'F19H1', 'F19H2', 'F19H3', 'F19H4', 'F19P3',
                'F20H1', 'F20H2', 'F20H3', 'F20H4', 'F20P4'],
               ['Serialno', 'F21H1', 'F21H2', 'F21H3', 'F21H4', 'F21P1', 'F22H1', 'F22H2',
                'F22H3', 'F22H4', 'F22P2', 'F23H1', 'F23H2', 'F23H3', 'F23H4', 'F23P3',
                'F24H1', 'F24H2', 'F24H3', 'F24H4', 'F24P4'],
               ['Serialno', 'F25H1', 'F25H2', 'F25H3', 'F25H4', 'F25P1', 'F26H1', 'F26H2',
                    'F26H3', 'F26H4', 'F26P2', 'F27H1', 'F27H2', 'F27H3', 'F27H4', 'F27P3',
                        'F28H1', 'F28H2', 'F28H3', 'F28H4', 'F28P4'],
                ['Serialno', 'F29H1', 'F29H2', 'F29H3', 'F29H4', 'F29P1', 'F30H1', 'F30H2',
                                    'F30H3', 'F30H4', 'F30P2', 'F31H1', 'F31H2', 'F31H3', 'F31H4', 'F31P3',
                                        'F32H1', 'F32H2', 'F32H3', 'F32H4', 'F32P4'],
                ['Serialno', 'F33H1', 'F33H2', 'F33H3', 'F33H4', 'F33P1', 'F34H1', 'F34H2',
                            'F34H3', 'F34H4', 'F34P2', 'F35H1', 'F35H2', 'F35H3', 'F35H4', 'F35P3',
                                    'F36H1', 'F36H2', 'F36H3', 'F36H4', 'F36P4']]


def break_into_chunks(list):
    number_of_list = 2
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
            df = pd.read_csv(directory + "\\" + controller + "\\" + file, names=column_list[i])
            last_column = column_list[i][-1]
            print(file)
            df['Serialno'] = df['Serialno'].str.replace(r'\D', '').astype(int)
            df[last_column] = df[last_column].str.replace(r'\D', '').astype(int)
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
    processed_data_id = 'quantum-theme-334609.Processed_data.' + 'Main_12_copy_' + str(runid)
    query = 'create or replace table ' + processed_data_id + ' as SELECT * FROM `quantum-theme-334609.Raw_data_12inch_gmfl.Main_12_copy_1` where runid={} AND F1H1 IS NOT NULL AND F1H2 IS NOT NULL ' \
                                                             'AND F1H3 IS NOT NULL AND F1H4 IS NOT NULL AND F1P1 IS NOT NULL AND F2H1 IS NOT NULL AND F2H2 IS NOT NULL AND F2H3 IS NOT NULL ' \
                                                             'AND F2H4 IS NOT NULL AND F2P2 IS NOT NULL AND F3H1 IS NOT NULL AND F3H2 IS NOT NULL AND F3H3 IS NOT NULL AND F3H4 IS NOT NULL AND ' \
                                                             'F3P3 IS NOT NULL AND F4H1 IS NOT NULL AND F4H2 IS NOT NULL AND F4H3 IS NOT NULL AND F4H4 IS NOT NULL AND F4P4 IS NOT NULL AND F5H1 ' \
                                                             'IS NOT NULL AND F5H2 IS NOT NULL AND F5H3 IS NOT NULL AND F5H4 IS NOT NULL AND F5P1 IS NOT NULL AND F6H1 IS NOT NULL AND F6H2 IS NOT NULL ' \
                                                             'AND F6H3 IS NOT NULL AND F6H4 IS NOT NULL AND F6P2 IS NOT NULL AND F7H1 IS NOT NULL AND F7H2 IS NOT NULL AND F7H3 IS NOT NULL AND F7H4 IS ' \
                                                             'NOT NULL AND F7P3 IS NOT NULL AND F8H1 IS NOT NULL AND F8H2 IS NOT NULL AND F8H3 IS NOT NULL AND F8H4 IS NOT NULL AND F8P4 IS NOT NULL AND ' \
                                                             'F9H1 IS NOT NULL AND F9H2 IS NOT NULL AND F9H3 IS NOT NULL AND F9H4 IS NOT NULL AND F9P1 IS NOT NULL AND F10H1 IS NOT NULL AND F10H2 IS NOT NULL ' \
                                                             'AND F10H3 IS NOT NULL AND F10H4 IS NOT NULL AND F10P2 IS NOT NULL AND F11H1 IS NOT NULL AND F11H2 IS NOT NULL AND F11H3 IS NOT NULL AND F11H4 IS NOT NULL ' \
                                                             'AND F11P3 IS NOT NULL AND F12H1 IS NOT NULL AND F12H2 IS NOT NULL AND F12H3 IS NOT NULL AND F12H4 IS NOT NULL AND F12P4 IS NOT NULL AND F13H1 IS NOT NULL ' \
                                                             'AND F13H2 IS NOT NULL AND F13H3 IS NOT NULL AND F13H4 IS NOT NULL AND F13P1 IS NOT NULL AND F14H1 IS NOT NULL AND F14H2 IS NOT NULL AND F14H3 IS NOT NULL ' \
                                                             'AND F14H4 IS NOT NULL AND F14P2 IS NOT NULL AND F15H1 IS NOT NULL AND F15H2 IS NOT NULL AND F15H3 IS NOT NULL AND F15H4 IS NOT NULL AND F15P3 IS NOT NULL ' \
                                                             'AND F16H1 IS NOT NULL AND F16H2 IS NOT NULL AND F16H3 IS NOT NULL AND F16H4 IS NOT NULL AND F16P4 IS NOT NULL AND F17H1 IS NOT NULL AND F17H2 IS NOT NULL ' \
                                                             'AND F17H3 IS NOT NULL AND F17H4 IS NOT NULL AND F17P1 IS NOT NULL AND F18H1 IS NOT NULL AND F18H2 IS NOT NULL AND F18H3 IS NOT NULL AND F18H4 IS NOT NULL ' \
                                                             'AND F18P2 IS NOT NULL AND F19H1 IS NOT NULL AND F19H2 IS NOT NULL AND F19H3 IS NOT NULL AND F19H4 IS NOT NULL AND F19P3 IS NOT NULL AND F20H1 IS NOT NULL ' \
                                                             'AND F20H2 IS NOT NULL AND F20H3 IS NOT NULL AND F20H4 IS NOT NULL AND F20P4 IS NOT NULL AND F21H1 IS NOT NULL AND F21H2 IS NOT NULL AND F21H3 IS NOT NULL ' \
                                                             'AND F21H4 IS NOT NULL AND F21P1 IS NOT NULL AND F22H1 IS NOT NULL AND F22H2 IS NOT NULL AND F22H3 IS NOT NULL AND F22H4 IS NOT NULL AND F22P2 IS NOT NULL ' \
                                                             'AND F23H1 IS NOT NULL AND F23H2 IS NOT NULL AND F23H3 IS NOT NULL AND F23H4 IS NOT NULL AND F23P3 IS NOT NULL AND F24H1 IS NOT NULL AND F24H2 IS NOT NULL ' \
                                                             'AND F24H3 IS NOT NULL AND F24H4 IS NOT NULL AND F24P4 IS NOT NULL AND F25H1 IS NOT NULL AND F25H2 IS NOT NULL AND F25H3 IS NOT NULL AND F25H4 IS NOT NULL ' \
                                                             'AND F25P1 IS NOT NULL AND F26H1 IS NOT NULL AND F26H2 IS NOT NULL AND F26H3 IS NOT NULL AND F26H4 IS NOT NULL AND F26P2 IS NOT NULL AND F27H1 IS NOT NULL ' \
                                                             'AND F27H2 IS NOT NULL AND F27H3 IS NOT NULL AND F27H4 IS NOT NULL AND F27P3 IS NOT NULL AND F28H1 IS NOT NULL AND F28H2 IS NOT NULL AND F28H3 IS NOT NULL ' \
                                                             'AND F28H4 IS NOT NULL AND F28P4 IS NOT NULL AND F29H1 IS NOT NULL AND F29H2 IS NOT NULL AND F29H3 IS NOT NULL AND F29H4 IS NOT NULL AND F29P1 IS NOT NULL ' \
                                                             'AND F30H1 IS NOT NULL AND F30H2 IS NOT NULL AND F30H3 IS NOT NULL AND F30H4 IS NOT NULL AND F30P2 IS NOT NULL AND F31H1 IS NOT NULL ' \
                                                             'AND F31H2 IS NOT NULL AND F31H3 IS NOT NULL AND F31H4 IS NOT NULL AND F31P3 IS NOT NULL AND F32H1 IS NOT NULL AND F32H2 IS NOT NULL AND F32H3 IS NOT NULL ' \
                                                             'AND F32H4 IS NOT NULL AND F32P4 IS NOT NULL AND F33H1 IS NOT NULL AND F33H2 IS NOT NULL AND F33H3 IS NOT NULL AND F33H4 IS NOT NULL AND F33P1 IS NOT NULL ' \
                                                            'AND F34H1 IS NOT NULL AND F34H2 IS NOT NULL AND F34H3 IS NOT NULL AND F34H4 IS NOT NULL AND F34P2 IS NOT NULL AND F35H1 IS NOT NULL ' \
                                                            'AND F35H2 IS NOT NULL AND F35H3 IS NOT NULL AND F35H4 IS NOT NULL AND F36P3 IS NOT NULL AND F36H1 IS NOT NULL AND F36H2 IS NOT NULL AND F36H3 IS NOT NULL ' \
                                                            'AND F36H4 IS NOT NULL AND F36P4 IS NOT NULL AND ODDO1 IS NOT NULL AND ODDO2 IS NOT NULL'

    runid_specific_table = client.query(query.format(runid))
    print("runid_specific_table", runid_specific_table)
    view_id = 'quantum-theme-334609.Processed_data.' + 'Main_12_copy_x' + str(runid)
    view = bigquery.Table(view_id)
    print("<<<<<<<<<<<<<<<<<<")
    view.view_query = f"SELECT *, ROW_NUMBER() OVER (ORDER BY filename,Serialno) AS index FROM `{processed_data_id}` order by filename,Serialno"
    # view.view_query = 'CREATE OR REPLACE VIEW  ' + view_id + ' AS SELECT * FROM ' + processed_data_id

    # Make an API request to create the view.
    view = client.create_table(view)
    print(f"Created {view.table_type}: {str(view.reference)}")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>")

def upload_data(dir, runid):
    print("runid", runid)
    query = 'Delete FROM `quantum-theme-334609.Raw_data_12inch_gmfl.Main_12_copy` where runid={}'
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
        directory_csv = os.path.join("D:/results12gmfl/", str(runid))
        if os.path.exists(directory_csv):
            shutil.rmtree(directory_csv)
            print('deleted')
        os.makedirs(directory_csv)
        print('created')
    array_of_processes = []
    for i, file in enumerate(file_list):
        process_obj = Process(target=main_thread, args=(file, controller_list, directory, runid, directory_csv))
        process_obj.start()
        array_of_processes.append(process_obj)
    print(array_of_processes)

    for process in array_of_processes:
        process.join()
    create_project_table(runid)
    print("Process end at : ", time.ctime())
