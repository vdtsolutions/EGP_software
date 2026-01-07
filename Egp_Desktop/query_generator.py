import json
from google.cloud import bigquery
import Components.config as Config

connection = Config.connection
credentials = Config.credentials
project_id = Config.project_id
client = bigquery.Client(credentials=credentials, project=project_id)
#config = json.loads(open('./utils/sensor_value - Copy.json').read())

def get_pipe(lower_sensitivity,upper_sensitivity,runid, start_index, end_index,pipe_id):
    """
        This will return a query(string type) for bigquery that will fetch welds raw-data
        :sensitivity : Sensitivity of the Weld
        :runid : Id of the Project
    """
    tup1 = ('proximity1', 'proximity2', 'proximity3', 'proximity4', 'proximity5', 'proximity6', 'proximity7', 'proximity8',
                                                    'proximity9', 'proximity10', 'proximity11', 'proximity12', 'proximity13', 'proximity14', 'proximity15',
                                                    'proximity16', 'proximity17', 'proximity18')
    with connection.cursor() as cursor:
        query = "SELECT proximity1, proximity2, proximity3, proximity4, proximity5, proximity6, proximity7, proximity8,proximity9, proximity10, proximity11, proximity12, proximity13, proximity14, proximity15,proximity16, proximity17, proximity18 FROM base_value where pipe_id={}".format(pipe_id)
        cursor.execute(query)
        result = cursor.fetchone()
        print(result)
    # config = json.loads(open('./utils/sensor_value_update.json').read())
    config = {tup1[i]: result[i] for i, _ in enumerate(tup1)}
    base_values = []

    base_values.append(float(config["proximity1"]))

    base_values.append(float(config["proximity2"]))

    base_values.append(float(config["proximity3"]))

    base_values.append(float(config["proximity4"]))

    base_values.append(float(config["proximity5"]))

    base_values.append(float(config["proximity6"]))

    base_values.append(float(config["proximity7"]))

    base_values.append(float(config["proximity8"]))

    base_values.append(float(config["proximity9"]))

    base_values.append(float(config["proximity10"]))

    base_values.append(float(config["proximity11"]))

    base_values.append(float(config["proximity12"]))

    base_values.append(float(config["proximity13"]))

    base_values.append(float(config["proximity14"]))

    base_values.append(float(config["proximity15"]))

    base_values.append(float(config["proximity16"]))

    base_values.append(float(config["proximity17"]))

    base_values.append(float(config["proximity18"]))

    # base_values.append(float(config["F19P3"]))

    # base_values.append(float(config["F20P4"]))

    # base_values.append(float(config["F21P1"]))

    # base_values.append(float(config["F22P2"]))

    # base_values.append(float(config["F23P3"]))

    # base_values.append(float(config["F24P4"]))

    function = 'CREATE TEMPORARY FUNCTION test(arr ARRAY<INT64>) RETURNS ARRAY<INT64> LANGUAGE js AS " ' \
               'let upper_sensitivity=' + upper_sensitivity + ';let lower_sensitivity=' + lower_sensitivity + ';let ' \
                                                                                                              'base=' + str(
        base_values) + ';for(let i=0;i<18;i++){if(arr[i] >= upper_sensitivity * parseInt(base[i]) || arr[i] <= parseInt(base[i]) * lower_sensitivity){arr[i]= ((arr[i]-parseInt(base[i]))/parseInt(base[i]))*100000}else{arr[i]=0.0}}' \
                       'return arr;\";' \
                       ' '

    to_execute = 'SELECT index,oddo1,oddo2,ROLL,test([proximity1 ,proximity2 ,proximity3 ,proximity4 ,proximity5 ,proximity6 ,proximity7 ,proximity8 ,proximity9 ,proximity10 ,proximity11 ,proximity12 ,proximity13 ,proximity14 ,proximity15 ,' \
                 'proximity16 ,proximity17 ,proximity18]) as frames FROM ' + Config.table_name + ' where index>{} and index<{} order by index'

    query_to_run = function + to_execute.format(start_index, end_index)
    # print(query_to_run)
    return query_to_run
