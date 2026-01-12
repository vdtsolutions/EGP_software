from google.cloud import bigquery
import Components.config as Config
from google.cloud import bigquery

import Components.config as Config

connection = Config.connection
credentials = Config.credentials
project_id = Config.project_id
source_dataset_id = Config.source_dataset_id
source_table_id = Config.source_table_id
client = bigquery.Client(credentials=credentials, project=project_id)
def get_weld(lower, upper, runid, start_index, end_index,weld_id):
    print("lower_sensitivity and upper_sensitivity", lower, upper, runid, start_index, end_index, weld_id)
    """
        This will return a query(string type) for bigquery that will fetch welds raw-data
        :sensitivity : Sensitivity of the Weld
        :runid : Id of the Project
    """
    tup1 = (
        "F1H1", "F1H2", "F1H3", "F1H4", "F2H1", "F2H2", "F2H3", "F2H4", "F3H1", "F3H2", "F3H3", "F3H4", "F4H1", "F4H2",
        "F4H3", "F4H4",
        "F5H1", "F5H2", "F5H3", "F5H4", "F6H1", "F6H2", "F6H3", "F6H4", "F7H1", "F7H2", "F7H3", "F7H4", "F8H1", "F8H2",
        "F8H3", "F8H4",
        "F9H1", "F9H2", "F9H3", "F9H4", "F10H1", "F10H2", "F10H3", "F10H4", "F11H1", "F11H2", "F11H3", "F11H4", "F12H1",
        "F12H2", "F12H3", "F12H4",
        "F13H1", "F13H2", "F13H3", "F13H4", "F14H1", "F14H2", "F14H3", "F14H4", "F15H1", "F15H2", "F15H3", "F15H4",
        "F16H1", "F16H2", "F16H3", "F16H4",
        "F17H1", "F17H2", "F17H3", "F17H4", "F18H1", "F18H2", "F18H3", "F18H4", "F19H1", "F19H2", "F19H3", "F19H4",
        "F20H1", "F20H2", "F20H3", "F20H4",
        "F21H1", "F21H2", "F21H3", "F21H4", "F22H1", "F22H2", "F22H3", "F22H4", "F23H1", "F23H2", "F23H3", "F23H4",
        "F24H1", "F24H2", "F24H3", "F24H4",
        "F25H1", "F25H2", "F25H3", "F25H4", "F26H1", "F26H2", "F26H3", "F26H4", "F27H1", "F27H2", "F27H3", "F27H4",
        "F28H1", "F28H2", "F28H3", "F28H4",
        "F29H1", "F29H2", "F29H3", "F29H4", "F30H1", "F30H2", "F30H3", "F30H4", "F31H1", "F31H2", "F31H3", "F31H4",
        "F32H1", "F32H2", "F32H3", "F32H4",
        "F33H1", "F33H2", "F33H3", "F33H4", "F34H1", "F34H2", "F34H3", "F34H4", "F35H1", "F35H2", "F35H3", "F35H4",
        "F36H1", "F36H2", "F36H3", "F36H4",
    )

    #print(tup1)
    with connection.cursor() as cursor:
        query = "SELECT F1H1 ,F1H2 ,F1H3 ,F1H4 ,F2H1 ,F2H2 ,F2H3 ,F2H4 ,F3H1 ,F3H2 ,F3H3 ,F3H4 ,F4H1 ,F4H2 ,F4H3,F4H4 ,F5H1 ,F5H2 ,F5H3 ,F5H4 ,F6H1 ,F6H2 ,F6H3 ,F6H4 ,F7H1 ,F7H2 ,F7H3 ,F7H4 ,F8H1 ,F8H2 ,F8H3 ,F8H4 ,F9H1 ,F9H2 ,F9H3 ,F9H4 ,F10H1 ,F10H2 ,F10H3 ,F10H4 ,F11H1 ,F11H2 ,F11H3 ,F11H4 ,F12H1 ,F12H2 ,F12H3 ,F12H4 ,F13H1 ,F13H2 ,F13H3 ,F13H4 ,F14H1 ,F14H2 ,F14H3 ,F14H4 ,F15H1 ,F15H2 ,F15H3 ,F15H4 ,F16H1 ,F16H2 ,F16H3 ,F16H4 ,F17H1 ,F17H2 ,F17H3 ,F17H4 ,F18H1 ,F18H2 ,F18H3 ,F18H4 ,F19H1 ,F19H2 ,F19H3 ,F19H4 ,F20H1 ,F20H2 ,F20H3 ,F20H4 ,F21H1 ,F21H2 ,F21H3 ,F21H4 ,F22H1 ,F22H2 ,F22H3 ,F22H4 ,F23H1 ,F23H2 ,F23H3 ,F23H4, F24H1, F24H2, F24H3, F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4, F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1, F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4  FROM base_value where pipe_id={}".format(
            weld_id)
        cursor.execute(query)
        result = cursor.fetchone()
        print(result)
    # config = json.loads(open('./utils/sensor_value_update.json').read())
    config = {tup1[i]: result[i] for i, _ in enumerate(tup1)}
    #print(config)


    base_values = []
    base_values.append(float(config["F1H1"]))
    base_values.append(float(config["F1H2"]))
    base_values.append(float(config["F1H3"]))
    base_values.append(float(config["F1H4"]))
    # base_values.append(float(config["F1P1"]))
    base_values.append(float(config["F2H1"]))
    base_values.append(float(config["F2H2"]))
    base_values.append(float(config["F2H3"]))
    base_values.append(float(config["F2H4"]))
    # base_values.append(float(config["F2P2"]))
    base_values.append(float(config["F3H1"]))
    base_values.append(float(config["F3H2"]))
    base_values.append(float(config["F3H3"]))
    base_values.append(float(config["F3H4"]))
    # base_values.append(float(config["F3P3"]))
    base_values.append(float(config["F4H1"]))
    base_values.append(float(config["F4H2"]))
    base_values.append(float(config["F4H3"]))
    base_values.append(float(config["F4H4"]))
    # base_values.append(float(config["F4P4"]))
    base_values.append(float(config["F5H1"]))
    base_values.append(float(config["F5H2"]))
    base_values.append(float(config["F5H3"]))
    base_values.append(float(config["F5H4"]))
    # base_values.append(float(config["F5P1"]))
    base_values.append(float(config["F6H1"]))
    base_values.append(float(config["F6H2"]))
    base_values.append(float(config["F6H3"]))
    base_values.append(float(config["F6H4"]))
    # base_values.append(float(config["F6P2"]))
    base_values.append(float(config["F7H1"]))
    base_values.append(float(config["F7H2"]))
    base_values.append(float(config["F7H3"]))
    base_values.append(float(config["F7H4"]))
    # base_values.append(float(config["F7P3"]))
    base_values.append(float(config["F8H1"]))
    base_values.append(float(config["F8H2"]))
    base_values.append(float(config["F8H3"]))
    base_values.append(float(config["F8H4"]))
    # base_values.append(float(config["F8P4"]))
    base_values.append(float(config["F9H1"]))
    base_values.append(float(config["F9H2"]))
    base_values.append(float(config["F9H3"]))
    base_values.append(float(config["F9H4"]))
    # base_values.append(float(config["F9P1"]))
    base_values.append(float(config["F10H1"]))
    base_values.append(float(config["F10H2"]))
    base_values.append(float(config["F10H3"]))
    base_values.append(float(config["F10H4"]))
    # base_values.append(float(config["F10P2"]))
    base_values.append(float(config["F11H1"]))
    base_values.append(float(config["F11H2"]))
    base_values.append(float(config["F11H3"]))
    base_values.append(float(config["F11H4"]))
    # base_values.append(float(config["F11P3"]))
    base_values.append(float(config["F12H1"]))
    base_values.append(float(config["F12H2"]))
    base_values.append(float(config["F12H3"]))
    base_values.append(float(config["F12H4"]))
    # base_values.append(float(config["F12P4"]))
    base_values.append(float(config["F13H1"]))
    base_values.append(float(config["F13H2"]))
    base_values.append(float(config["F13H3"]))
    base_values.append(float(config["F13H4"]))
    # base_values.append(float(config["F13P1"]))
    base_values.append(float(config["F14H1"]))
    base_values.append(float(config["F14H2"]))
    base_values.append(float(config["F14H3"]))
    base_values.append(float(config["F14H4"]))
    # base_values.append(float(config["F14P2"]))
    base_values.append(float(config["F15H1"]))
    base_values.append(float(config["F15H2"]))
    base_values.append(float(config["F15H3"]))
    base_values.append(float(config["F15H4"]))
    # base_values.append(float(config["F15P3"]))
    base_values.append(float(config["F16H1"]))
    base_values.append(float(config["F16H2"]))
    base_values.append(float(config["F16H3"]))
    base_values.append(float(config["F16H4"]))
    # base_values.append(float(config["F16P4"]))
    base_values.append(float(config["F17H1"]))
    base_values.append(float(config["F17H2"]))
    base_values.append(float(config["F17H3"]))
    base_values.append(float(config["F17H4"]))
    # base_values.append(float(config["F17P1"]))
    base_values.append(float(config["F18H1"]))
    base_values.append(float(config["F18H2"]))
    base_values.append(float(config["F18H3"]))
    base_values.append(float(config["F18H4"]))
    # base_values.append(float(config["F18P2"]))
    base_values.append(float(config["F19H1"]))
    base_values.append(float(config["F19H2"]))
    base_values.append(float(config["F19H3"]))
    base_values.append(float(config["F19H4"]))
    # base_values.append(float(config["F19P3"]))
    base_values.append(float(config["F20H1"]))
    base_values.append(float(config["F20H2"]))
    base_values.append(float(config["F20H3"]))
    base_values.append(float(config["F20H4"]))
    # base_values.append(float(config["F20P4"]))
    base_values.append(float(config["F21H1"]))
    base_values.append(float(config["F21H2"]))
    base_values.append(float(config["F21H3"]))
    base_values.append(float(config["F21H4"]))
    # base_values.append(float(config["F21P1"]))
    base_values.append(float(config["F22H1"]))
    base_values.append(float(config["F22H2"]))
    base_values.append(float(config["F22H3"]))
    base_values.append(float(config["F22H4"]))
    # base_values.append(float(config["F22P2"]))
    base_values.append(float(config["F23H1"]))
    base_values.append(float(config["F23H2"]))
    base_values.append(float(config["F23H3"]))
    base_values.append(float(config["F23H4"]))
    # base_values.append(float(config["F23P3"]))
    base_values.append(float(config["F24H1"]))
    base_values.append(float(config["F24H2"]))
    base_values.append(float(config["F24H3"]))
    base_values.append(float(config["F24H4"]))
    # base_values.append(float(config["F24P4"]))
    base_values.append(float(config["F25H1"]))
    base_values.append(float(config["F25H2"]))
    base_values.append(float(config["F25H3"]))
    base_values.append(float(config["F25H4"]))
    # base_values.append(float(config["F25P1"]))
    base_values.append(float(config["F26H1"]))
    base_values.append(float(config["F26H2"]))
    base_values.append(float(config["F26H3"]))
    base_values.append(float(config["F26H4"]))
    # base_values.append(float(config["F26P2"]))
    base_values.append(float(config["F27H1"]))
    base_values.append(float(config["F27H2"]))
    base_values.append(float(config["F27H3"]))
    base_values.append(float(config["F27H4"]))
    # base_values.append(float(config["F27P3"]))
    base_values.append(float(config["F28H1"]))
    base_values.append(float(config["F28H2"]))
    base_values.append(float(config["F28H3"]))
    base_values.append(float(config["F28H4"]))
    # base_values.append(float(config["F28P4"]))
    base_values.append(float(config["F29H1"]))
    base_values.append(float(config["F29H2"]))
    base_values.append(float(config["F29H3"]))
    base_values.append(float(config["F29H4"]))
    # base_values.append(float(config["F29P1"]))
    base_values.append(float(config["F30H1"]))
    base_values.append(float(config["F30H2"]))
    base_values.append(float(config["F30H3"]))
    base_values.append(float(config["F30H4"]))
    # base_values.append(float(config["F30P2"]))
    base_values.append(float(config["F31H1"]))
    base_values.append(float(config["F31H2"]))
    base_values.append(float(config["F31H3"]))
    base_values.append(float(config["F31H4"]))
    # base_values.append(float(config["F31P3"]))
    base_values.append(float(config["F32H1"]))
    base_values.append(float(config["F32H2"]))
    base_values.append(float(config["F32H3"]))
    base_values.append(float(config["F32H4"]))
    # base_values.append(float(config["F32P4"]))
    base_values.append(float(config["F33H1"]))
    base_values.append(float(config["F33H2"]))
    base_values.append(float(config["F33H3"]))
    base_values.append(float(config["F33H4"]))
    # base_values.append(float(config["F33P1"]))
    base_values.append(float(config["F34H1"]))
    base_values.append(float(config["F34H2"]))
    base_values.append(float(config["F34H3"]))
    base_values.append(float(config["F34H4"]))
    # base_values.append(float(config["F34P2"]))
    base_values.append(float(config["F35H1"]))
    base_values.append(float(config["F35H2"]))
    base_values.append(float(config["F35H3"]))
    base_values.append(float(config["F35H4"]))
    # base_values.append(float(config["F35P3"]))
    base_values.append(float(config["F36H1"]))
    base_values.append(float(config["F36H2"]))
    base_values.append(float(config["F36H3"]))
    base_values.append(float(config["F36H4"]))
    # base_values.append(float(config["F36P4"]))
    #print("base_values",base_values)
    #print("base value",base_values)
    function = 'CREATE TEMPORARY FUNCTION test(arr ARRAY<INT64>) RETURNS ARRAY<INT64> LANGUAGE js AS " ' \
               'let upper_sensitivity=' + upper + ';let lower_sensitivity=' + lower + ';let ' \
        'base=' + str(base_values) + ';for(let i=0;i<144;i++){if(arr[i] >= upper_sensitivity * base[i] || arr[i] <= base[i] * lower_sensitivity){arr[i]= ((arr[i]-base[i])/base[i])*100}else{arr[i]=0.0}}' \
                       'return arr;\";' \
                       ' '

    to_execute = 'SELECT index,oddo1,oddo2,ROLL,test([F1H1 ,F1H2 ,F1H3 ,F1H4 ,F2H1 ,F2H2 ,F2H3 ,F2H4 ,F3H1 ,F3H2 ,F3H3 ,F3H4 ,F4H1 ,F4H2 ,F4H3 ,' \
                 'F4H4 ,F5H1 ,F5H2 ,F5H3 ,F5H4 ,F6H1 ,F6H2 ,F6H3 ,F6H4 ,F7H1 ,F7H2 ,F7H3 ,F7H4 ,F8H1 ,F8H2 ,F8H3 ,' \
                 'F8H4 ,F9H1 ,F9H2 ,F9H3 ,F9H4 ,F10H1 ,F10H2 ,F10H3 ,F10H4 ,F11H1 ,F11H2 ,F11H3 ,F11H4 ,F12H1 ,F12H2 ,F12H3 ,' \
                 'F12H4 ,F13H1 ,F13H2 ,F13H3 ,F13H4 ,F14H1 ,F14H2 ,F14H3 ,F14H4 ,F15H1 ,F15H2 ,F15H3 ,F15H4 ,F16H1 ,F16H2 ,F16H3 ,' \
                 'F16H4 ,F17H1 ,F17H2 ,F17H3 ,F17H4 ,F18H1 ,F18H2 ,F18H3 ,F18H4 ,F19H1 ,F19H2 ,F19H3 ,F19H4 ,F20H1 ,F20H2 ,F20H3 ,' \
                 'F20H4 ,F21H1 ,F21H2 ,F21H3 ,F21H4 ,F22H1 ,F22H2 ,F22H3 ,F22H4 ,F23H1 ,F23H2 ,F23H3 ,F23H4 ,F24H1 ,F24H2 ,F24H3 ,' \
                 'F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4 , F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4,' \
                 'F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4 ,' \
                 'F33H1, F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4 ]) as frames FROM ' + Config.table_name + ' where index>{} and index<{} order by index'

    query_to_run = function + to_execute.format(start_index, end_index)
    return query_to_run, config