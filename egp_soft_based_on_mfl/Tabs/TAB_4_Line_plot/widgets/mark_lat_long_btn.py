from PyQt5.QtWidgets import QMessageBox
from google.cloud import bigquery
import json
# from GMFL_12_Inch_Desktop.Components.self.configs import self.config as self.config
# connection = self.config.connection
# credentials = self.config.credentials
# project_id = self.config.project_id
# client = bigquery.Client(credentials=credentials, project=project_id)
# self.config = json.loads(open('./utils/proximity_base_value.json').read())


def mark_lat_long(self):
    try:
        # print("[DEBUG] mark_lat_long called")
        # print(f"[DEBUG] rect_start_1={self.rect_start_1}, rect_end_1={self.rect_end_1}")

        if self.rect_start_1 is not None and self.rect_end_1 is not None:
            x1, y1 = min(self.rect_start_1[0], self.rect_end_1[0]), \
                     min(self.rect_start_1[1], self.rect_end_1[1])
            x2, y2 = x1 + abs(self.rect_end_1[0] - self.rect_start_1[0]), \
                     y1 + abs(self.rect_end_1[1] - self.rect_start_1[1])
            lat_mark = self.latitude.text().strip()
            long_mark = self.logitude.text().strip()
            # print(f"[DEBUG] lat_mark={lat_mark}, long_mark={long_mark}")

            if lat_mark and long_mark:
                # print("[DEBUG] Entering DB logic")
                index = getattr(self, "index", None)
                if index is None:
                    raise ValueError("self.index not found in class scope")

                start_index = index.iloc[int(self.rect_start_1[0])]
                end_index = index.iloc[int(self.rect_end_1[0])]
                runid = getattr(self.parent, "runid", None)
                weld_id = getattr(self.parent, "weld_id", None)

                if runid is None or weld_id is None:
                    raise ValueError("Missing runid or weld_id in class")

                # print(f"[DEBUG] runid={runid}, weld_id={weld_id}")
                # print(f"[DEBUG] start_index={start_index}, end_index={end_index}")

                query_for_start = 'SELECT * FROM ' + self.config.table_name + ' WHERE index={}'
                query_job = self.config.client.query(query_for_start.format(start_index))
                results_1 = query_job.result()

                oddo1, oddo2 = [], []
                for row1 in results_1:
                    oddo1.append(row1['ODDO1'])
                    oddo2.append(row1['ODDO2'])
                # print(f"[DEBUG] Raw oddo1={oddo1}, oddo2={oddo2}")

                if not oddo1 or not oddo2:
                    raise ValueError("Empty oddo1/oddo2 fetched from query")

                oddo1 = oddo1[0] - self.config.oddo1
                oddo2 = oddo2[0] - self.config.oddo2
                # print(f"[DEBUG] Adjusted oddo1={oddo1}, oddo2={oddo2}")

                with self.config.connection.cursor() as cursor:
                    same_lw_up_check = cursor.execute(
                        'SELECT absolute_distance_oddo1, absolute_distance_oddo2 FROM dgps_segment '
                        'WHERE absolute_distance_oddo1=%s AND absolute_distance_oddo2=%s',
                        (oddo1, oddo2)
                    )

                    # print(f"[DEBUG] same_lw_up_check={same_lw_up_check}")

                    if same_lw_up_check:
                        print("[DEBUG] Duplicate entry found, skipping insert.")
                        return 'HII'

                    query_pipe_insert = (
                        "INSERT INTO dgps_segment (runid, pipe_id, start_index, "
                        "absolute_distance_oddo2, absolute_distance_oddo1, Latitude, Longitude) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    )
                    cursor.execute(query_pipe_insert, (
                        int(runid), int(weld_id), int(start_index),
                        oddo2, oddo1, lat_mark, long_mark
                    ))
                    self.config.connection.commit()
                    # print("[DEBUG] Data inserted successfully.")

                QMessageBox.information(self.tab_line1, 'Success', 'Data saved')

            else:
                QMessageBox.warning(self.tab_line1, 'Invalid Input', 'Enter any value')

        else:
            QMessageBox.warning(
                self.tab_line1,
                'Invalid Input',
                'Select RectangleSelection of Marking, then press the button for Lat And Long'
            )

    except Exception as e:
        import traceback
        err_details = traceback.format_exc()
        print("========== [DEBUG] mark_lat_long ERROR ==========")
        print(err_details)
        print("==================================================")
        QMessageBox.critical(self.tab_line1, 'Error', f'Error in mark_lat_long:\n{str(e)}')