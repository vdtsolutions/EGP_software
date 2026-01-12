from google.cloud import bigquery
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import json
# from  GMFL_12_Inch_Desktop.Components.Configs import config as config


# connection = config.connection
# credentials = config.credentials
# project_id = config.project_id
# client = bigquery.Client(credentials=credentials, project=project_id)
# config = json.loads(open('./utils/proximity_base_value.json').read())





def feature_selection_func(self):
    if self.rect_start_1 is not None and self.rect_end_1 is not None:
        print("hi rect start1 func")
        while True:
            name, ok = QtWidgets.QInputDialog.getText(self.tab_line1, 'Enter Name', 'Enter the name of the drawn box:')
            if ok:
                if name.strip():  # Check if the entered name is not empty or just whitespace
                    x_start, y_start = self.rect_start_1
                    x_end, y_end = self.rect_end_1
                    runid = self.parent.runid
                    pipe = self.parent.weld_id
                    index_k = self.index.tolist()
                    start_index15 = index_k[round(x_start)]
                    end_index15 = index_k[round(x_end)]
                    # start_index15 = round(x_start)
                    # end_index15 = round(x_end)
                    print(start_index15, end_index15, name)
                    query_for_start = 'SELECT ODDO1,ODDO2 FROM ' + self.config.table_name + ' WHERE index>={} AND index<={} AND runid={} order by index'
                    query_job = self.config.client.query(
                        query_for_start.format(int(start_index15), int(end_index15), runid))
                    results = query_job.result()
                    oddo1 = []
                    oddo2 = []
                    for row in results:
                        oddo1.append(row[0])
                        oddo2.append(row[1])
                    # print(oddo1)
                    # print(oddo2)
                    start_oddo1 = oddo1[0] - self.config.oddo1
                    end_oddo1 = oddo1[-1] - self.config.oddo1
                    start_oddo2 = oddo2[0] - self.config.oddo2
                    end_oddo2 = oddo2[-1] - self.config.oddo2
                    length_oddo1 = end_oddo1 - start_oddo1
                    length_oddo2 = end_oddo2 - start_oddo2
                    with self.config.connection.cursor() as cursor:
                        type = 'manual'
                        query_weld_insert = "INSERT INTO anomalies (runid, start_index, end_index,type,start_oddo1,end_oddo1,start_oddo2,end_oddo2,length_oddo1,length_oddo2,feature_name,Pipe_No) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                            runid, start_index15, end_index15, type, start_oddo1, end_oddo1,
                            start_oddo2, end_oddo2, length_oddo1, length_oddo2, name, pipe)

                        # Execute query.
                        b = cursor.execute(query_weld_insert)
                        self.config.connection.commit()
                        QMessageBox.information(self.tab_line1, 'Success', 'Data saved')
                    break  # Exit the loop if a valid name is provided
                else:
                    QMessageBox.warning(self.tab_line1, 'Invalid Input', 'Please enter a name.')
            else:
                print('Operation canceled.')
                break
    else:
        QMessageBox.warning(self.tab_line1, 'Invalid Input',
                            'Select RectangleSelection of Marking, then press the button for base value')