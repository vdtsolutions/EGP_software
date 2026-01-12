import re
import Components.config as Config
import pandas as pd


# Defect length calculation function
def calculate_lengths_of_defects_in_pipe(df):
    column_sum = []
    df_hue = df
    # Sum of column is calculated
    for column in df_hue.columns:
        column_sum.append(df_hue[column].sum())
    start_of_length_ind = 0
    count_of_empty_obs = 0
    start_of_length_param = []
    for i, j in enumerate(column_sum):
        if j == 0 and start_of_length_ind == 0:
            pass
        elif j != 0 and start_of_length_ind == 0:
            start_of_length_ind = 1
            start_of_length_param.append(i)
        elif start_of_length_ind != 0 and count_of_empty_obs < 3:
            if i == len(column_sum) - 1:
                start_of_length_param.append(i - count_of_empty_obs - 1)
            if j == 0:
                count_of_empty_obs += 1
            else:
                count_of_empty_obs = 0
        elif start_of_length_ind != 0 and count_of_empty_obs >= 3:
            start_of_length_ind = 0
            start_of_length_param.append(i - count_of_empty_obs - 1)
            count_of_empty_obs = 0
    # Defect Breadth calculation
    i = 0
    end_points_of_defect = []
    while i < len(start_of_length_param):
        for j in range(start_of_length_param[i], start_of_length_param[i + 1] + 1):
            end_point_of_breadth = []
            lowerbound_ind = 0
            upperbound_ind = 0
            index_dict = {}
            for k, index in enumerate(df_hue.index):
                index_dict[k] = index
                if df_hue[j][index] == 0 and lowerbound_ind == 0 and upperbound_ind == 0:
                    pass
                elif df_hue[j][index] != 0 and lowerbound_ind == 0 and upperbound_ind == 0:
                    lowerbound_ind = 1
                    end_point_of_breadth.append(k)
                elif lowerbound_ind != 0:
                    if df_hue[j][index] == 0 and upperbound_ind == 1:
                        continue
                    elif df_hue[j][index] == 0 and upperbound_ind == 0:
                        upperbound_ind = 1
                        end_point_of_breadth.append(k - 1)
                    else:
                        end_point_of_breadth.append(k)
                        upperbound_ind = 0

        end_points_of_defect.append(index_dict[min(end_point_of_breadth)])
        end_points_of_defect.append(index_dict[max(end_point_of_breadth)])
        i += 2

    return start_of_length_param, end_points_of_defect


def insert_and_update_defect_to_db(defect_list, runid, pipe_id):
    print("start from here", pipe_id)
    with Config.connection.cursor() as cursor:
        a = cursor.execute(
            "DELETE FROM defectdetail WHERE  runid=" + str(runid) + " and type='system' and pipe_id=" + str(pipe_id))
        cursor.close()
        for defect in defect_list:
            with Config.connection.cursor() as cursor:
                query_weld_insert = "INSERT INTO defectdetail (runid, pipe_id, defect_length, defect_breadth, defect_angle,defect_depth,type,x,y,category,min,max,actual_length,actual_breadth,defect_from_start,defect_from_pipe) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

                # Execute query.
                b = cursor.execute(query_weld_insert, (
                    int(runid), int(pipe_id), int(defect[2]), int(defect[3]), 0, 0, 'system', int(defect[0]),
                    int(defect[1]), defect[4], float(defect[5]), float(defect[6]), float(defect[7]), float(defect[8]),float(defect[9]),float(defect[10])))
                if b:
                    print("data is inserted successfully")
                else:
                    print("data is not inserted successfully")
                Config.connection.commit()
        return


def indentify_defect_type(df, sensor_from, sensor_to, observation_from, observation_to):
    print(sensor_to, sensor_from, observation_to, observation_from)
    print(df.index)
    # df.to_csv('report.csv')
    extractedColumn = df.loc[observation_from:observation_to, sensor_from:sensor_to]

    proximity_column = []
    column_proximity = []
    for column in extractedColumn.columns:
        if re.search('[P]', column):
            column_proximity.append(column)
            proximity_column.append('I' if extractedColumn[column].mean() > 500 else 'E')

        # print(extractedColumn)

    df_meta = pd.read_json("../utils/sensor_value_update.json", typ='series')
    df_meta = df_meta.to_frame('0').transpose()
    defect_pipe_hole = extractedColumn.drop(column_proximity, axis=1)
    defect_percentage = pd.DataFrame()
    for i in defect_pipe_hole.index:
        for column in defect_pipe_hole.columns:
            defect_percentage[column] = defect_pipe_hole[column].apply(lambda x: (x - df_meta[column][0]) / 100)

    print(defect_percentage)
    maxValue = (defect_percentage.max()).max()
    minValue = (defect_percentage.min()).min()

    print("max and min ", maxValue, minValue)
    if proximity_column.count('I') > proximity_column.count('E'):
        return {"type": 'internal', "max": maxValue, "min": minValue}
    else:
        return {"type": 'external', "max": maxValue, "min": minValue}


def get_defect_list(df_hue, runid, pipe_id, df_pipe):
    defect_length_list, defect_breadth_list = calculate_lengths_of_defects_in_pipe(df_hue)

    converted_defect_breadth_list = []
    for element in defect_breadth_list:
        s_element = re.split('[H F]', element)
        num = (int(s_element[1]) - 1) * 4
        num += int(s_element[2])
        converted_defect_breadth_list.append(num)

    i = 0
    defect_list = []
    while i < len(defect_length_list):
        print("actual length")
        # actual length of defect wrt Pipe length
        defect_from_start = df_pipe.iloc[defect_length_list[i]]['ODDO1']
        defect_from_pipe=df_pipe.iloc[0]['ODDO1']
        actual_length = df_pipe.iloc[defect_length_list[i + 1]]['ODDO1'] - defect_from_start
        print(actual_length)
        defect_data = indentify_defect_type(df_pipe, defect_breadth_list[i], defect_breadth_list[i + 1],
                                            defect_length_list[i], defect_length_list[i + 1])
        print(defect_data)
        print(defect_data['type'])
        defect_type = defect_data['type']
        minValue = defect_data['min']
        maxValue = defect_data['max']

        temp_defect_list = []
        temp_defect_list.append(defect_length_list[i])
        temp_defect_list.append(converted_defect_breadth_list[i] - 1)
        temp_defect_list.append(defect_length_list[i + 1] - defect_length_list[i] + 1)
        temp_defect_list.append(converted_defect_breadth_list[i + 1] - converted_defect_breadth_list[i] + 1)
        i += 2
        temp_defect_list.append(defect_type)
        temp_defect_list.append(minValue)
        temp_defect_list.append(maxValue)
        temp_defect_list.append(actual_length)
        temp_defect_list.append(0.0)  # todo add breadth length

        temp_defect_list.append(defect_from_start)
        temp_defect_list.append(defect_from_pipe)
        print(temp_defect_list)
        defect_list.append(temp_defect_list)

    # actual_length=

    insert_and_update_defect_to_db(defect_list, runid, pipe_id)
    # TODO save breadth
    return defect_list

# #
# d_list = [[2, 3, 42, 12], [1, 4, 4, 3]]
# insert_and_update_defect_to_db(d_list, 1, 2)
