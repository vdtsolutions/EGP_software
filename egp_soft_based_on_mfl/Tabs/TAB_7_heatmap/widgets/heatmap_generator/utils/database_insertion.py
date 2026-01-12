import pandas as pd


def insert_defects_to_db_bb_new(connection, finial_defect_list, submatrices_dict):
    """
    Inserts defect records into the bb_new table.

    Args:
        connection: Active MySQL connection object.
        finial_defect_list: List of dictionaries containing defect data.
        submatrices_dict: Dictionary containing submatrices keyed by (runid, start_sensor, end_sensor).
    """
    print("inside insert defects into db fucntuion")
    with connection.cursor() as cursor:
        for i in finial_defect_list:
            pipe_id = i['pipe_id']
            runid = i['runid']
            pipe_length = i['pipe_length']
            start_index = i['start_reading']
            end_index = i['end_reading']
            start_sensor = i['start_sensor']
            end_sensor = i['end_sensor']
            absolute_distance = round(i['absolute_distance'] / 1000, 3)
            upstream = round(i['upstream'] / 1000, 3)
            length = round(i['length'])
            length_percent = round(i['length_percent'])

            # Get corresponding trimmed_matrix (replace with your default if not found)
            trimmed_matrix = submatrices_dict.get((runid, start_sensor, end_sensor), pd.DataFrame())

            Width = round(i['breadth'])
            # width_new = round(i['width_new'])
            width_new2 = round(i['width_new2'])
            depth_new = round(i['depth'])
            depth_old = round(i['depth_old'])
            orientation = i['orientation']
            defect_type = i['defect_type']
            dimension_classification = i['dimension_classification']
            start_oddo1 = i['start_oddo1']
            end_oddo1 = i['end_oddo1']
            speed = round(i['speed'], 2)
            min_value = i['Min_Val']
            max_value = i['Max_Val']
            WT_mm = i['wall_thickness']


            query_defect_insert = """
                INSERT INTO bb_new(pipe_id, runid, pipe_length, start_index, end_index, start_sensor, end_sensor, absolute_distance,
                upstream, length, length_percent, Width, width_new2,
                depth_old, depth_new, orientation, defect_type, dimension_classification, start_oddo1, end_oddo1, speed,
                Min_Val, Max_Val, `WT(mm)`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            try:
                cursor.execute(query_defect_insert, (
                    pipe_id, int(runid), pipe_length, start_index, end_index, start_sensor, end_sensor,
                    absolute_distance, upstream, length, length_percent,
                    Width, width_new2, depth_old, depth_new, orientation,
                    defect_type, dimension_classification, start_oddo1, end_oddo1,
                    speed, min_value, max_value, WT_mm
                ))

                connection.commit()
            except Exception as e:
                print(f"error inserting data: {e}")




def insert_defects_to_db_defect_clock_hm(connection, finial_defect_list, submatrices_dict):
    """
    Inserts defect records into the defect_clock_hm table.

    Args:
        connection: Active MySQL connection object.
        finial_defect_list: List of dictionaries containing defect data.
        submatrices_dict: Dictionary containing submatrices keyed by (runid, start_sensor, end_sensor).
    """
    print("inside insert defects into db fucntuion")
    with connection.cursor() as cursor:
        for i in finial_defect_list:
            pipe_id = i['pipe_id']
            runid = i['runid']
            defect_id = i['defect_id']
            pipe_length = i['pipe_length']
            start_index = i['start_reading']
            end_index = i['end_reading']
            start_sensor = i['start_sensor']
            end_sensor = i['end_sensor']
            absolute_distance = round(i['absolute_distance'] / 1000, 3)
            upstream = round(i['upstream'] / 1000, 3)
            length = round(i['length'])
            length_percent = round(i['length_percent'])

            # Get corresponding trimmed_matrix (replace with your default if not found)
            trimmed_matrix = submatrices_dict.get((runid, start_sensor, end_sensor), pd.DataFrame())

            Width = round(i['breadth'])
            # width_new = round(i['width_new'])
            width_new2 = round(i['width_new2'])
            depth_new = round(i['depth'])
            depth_old = round(i['depth_old'])
            orientation = i['orientation']
            defect_type = i['defect_type']
            dimension_classification = i['dimension_classification']
            start_oddo1 = i['start_oddo1']
            end_oddo1 = i['end_oddo1']
            speed = round(i['speed'], 2)
            min_value = i['Min_Val']
            max_value = i['Max_Val']
            WT_mm = i['wall_thickness']

            query_defect_insert = """
                INSERT INTO defect_clock_hm(runid, pipe_id, defect_id, pipe_length, start_index, end_index, start_sensor, end_sensor,upstream, 
                absolute_distance, length, length_percent, Width, width_new2,
                 depth_old, depth_new ,orientation, defect_type, dimension_classification, start_oddo1, end_oddo1, speed,
                min_value, max_value, `WT(mm)`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            try:
                cursor.execute(query_defect_insert, (
                    int(runid), pipe_id, defect_id, pipe_length, start_index, end_index, start_sensor, end_sensor,
                    upstream, absolute_distance, length, length_percent,
                    Width, width_new2, depth_old, depth_new,  orientation,
                    defect_type, dimension_classification, start_oddo1, end_oddo1,
                    speed, min_value, max_value, WT_mm
                ))

                connection.commit()
            except Exception as e:
                print(f"error inserting data: {e}")