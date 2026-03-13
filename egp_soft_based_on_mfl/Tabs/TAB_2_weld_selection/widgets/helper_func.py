from PyQt5.QtWidgets import QMessageBox

import os, json
from google.cloud import bigquery

from google.oauth2 import service_account
from google.cloud import bigquery_storage_v1
# def func(self, a):
#     # print(a)
#     query_for_start = 'SELECT * FROM ' + self.config.table_name + ' WHERE index>={} AND  index<={} order by index'
#     query_job = self.config.client.query(query_for_start.format(a[0], a[1]))
#     l1 = query_job.result().to_dataframe()
#     return l1

def func(self, a):
    credentials = service_account.Credentials.from_service_account_file(
        "./utils/Authorization.json",
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/bigquery",
            "https://www.googleapis.com/auth/bigquery.readonly",
        ]
    )
    bqstorage_client = bigquery_storage_v1.BigQueryReadClient(credentials=credentials)
    query = (
        "SELECT index, "
        + self.config.sensor_str_hall +
        " FROM " + self.config.table_name +
        " WHERE index >= {} AND index <= {} ORDER BY index"
    )

    query_job = self.config.client.query(query.format(a[0], a[1]))

    l1 = query_job.result().to_dataframe(
        bqstorage_client=bqstorage_client
    )

    return l1


def select_weld(self, eclick, erelease):
    runid = self.parent.runid
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    start_index15 = round(x1)
    end_index15 = round(x2)
    print(start_index15, end_index15)
    query_for_start = 'SELECT ODDO1,ODDO2 FROM ' + self.config.table_name + ' WHERE index>{} AND index<{} AND runid={} order by index'
    query_job = self.config.client.query(query_for_start.format(int(start_index15), int(end_index15), runid))
    results = query_job.result()
    print(results)
    oddo1 = []
    oddo2 = []
    for row in results:
        oddo1.append(row[0])
        oddo2.append(row[1])
    print(oddo1)
    print(oddo2)
    start_oddo1 = oddo1[0]
    end_oddo1 = oddo1[-1]
    start_oddo2 = oddo2[0]
    end_oddo2 = oddo2[-1]
    weld_length = end_oddo1 - start_oddo1 if end_oddo1 >= end_oddo2 else end_oddo2 - start_oddo2

    # if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
    #     print("start_index15: ", start_index15)
    #     print("end_index15: ", end_index15)
    #     QMessageBox.about(self, 'Sucess', 'Data Saved Successfully')
    #     self.hide()
    # else:
    #     print("data is not inserted successfully")
    #     QMessageBox.warning(self, 'Invalid', 'Please select again')

    # with self.config.connection.cursor() as cursor:
    #
    #     type = 'manual'
    #     # weld_number = 1
    #     analytic_id = 1
    #     sensitivity = 1
    #     query_weld_insert = "INSERT INTO temp_welds (runid,analytic_id,sensitivity,start_index,end_index,type,start_oddo1,end_oddo1,start_oddo2,end_oddo2,length) VALUES('{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}')".format(
    #         runid, analytic_id, sensitivity, start_index15, end_index15, type, start_oddo1, end_oddo1,
    #         start_oddo2, end_oddo2, weld_length)
    #
    #     # Execute query.
    #     b = cursor.execute(query_weld_insert)
    #     self.config.connection.commit()
    #     if b:
    #         QMessageBox.about(self, 'Insert', 'Data Inserted Successfully')
    #         # self.hide()
    #         # self.refresh_view()
    #     else:
    #         print("data is not inserted successfully")
    with self.config.connection.cursor() as cursor:
        try:
            type = 'manual'
            analytic_id = 1
            sensitivity = 1

            query = """
            INSERT INTO temp_welds 
            (runid, analytic_id, sensitivity, start_index, end_index, type,
             start_oddo1, end_oddo1, start_oddo2, end_oddo2, length)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

            cursor.execute(query, (
                runid, analytic_id, sensitivity,
                int(start_index15), int(end_index15), type,
                start_oddo1, end_oddo1,
                start_oddo2, end_oddo2, weld_length
            ))

            self.config.connection.commit()
            QMessageBox.information(self, "Success", "Weld saved successfully")

        except Exception as e:
            self.config.connection.rollback()
            QMessageBox.critical(self, "DB ERROR", str(e))
            return

    # print(start_index15)
    # print(end_index15)