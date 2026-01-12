from PyQt5.QtCore import Qt
import os
import pandas as pd
from PyQt5 import QtWidgets
from google.cloud import bigquery
import json

from .helper_func import GenerateGraph, handle_table_double_click_pipe, open_context_menu
# from GMFL_12_Inch_Desktop.Components.self.configs import self.config as self.config
# #
# # import GMFL_12_Inch_Desktop.Components.graph as graph
#
# self.config.connection = self.config.self.config.connection
# company_list = []  # list of companies
# credentials = self.config.credentials
# project_id = self.config.project_id
# client = bigquery.Client(credentials=credentials, project=project_id)
# self.config = json.loads(open(r'D:\Anubhav\vdt_backend\GMFL_12_Inch_Desktop\utils\proximity_base_value.json').read())


def pre_graph_analysis(self):
    self.config.print_with_time("Pre graph analysis called")
    runid = self.parent.runid
    Weld_id = self.combo_box.currentText()
    self.Weld_id = int(Weld_id)
    self.lower_sensitivity = self.lower_Sensitivity_combo_box.currentText()
    self.upper_sensitivity = self.upper_Sensitivity_combo_box.currentText()

    with self.config.connection.cursor() as cursor:
        # query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
        query = "SELECT start_index, end_index,start_oddo1,end_oddo1 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"
        cursor.execute(query, (self.parent.runid, self.Weld_id, self.parent.runid, self.Weld_id))
        result = cursor.fetchall()
        start_oddo1 = result[0][2]
        end_oddo1 = result[1][3]
        self.pipe_len_8 = end_oddo1 - start_oddo1
        print("Weld_pipe_Length", self.pipe_len_8)

        if not result:
            self.config.print_with_time("No data found for this pipe ID : ")
        else:
            """
            pkl file is found in local path
            """
            path = self.config.weld_pipe_pkl + self.parent.project_name + '/' + str(self.Weld_id) + '.pkl'
            if os.path.isfile(path):
                self.config.print_with_time("File exist")
                df_new_8 = pd.read_pickle(path)

                self.index_tab8 = df_new_8['index']
                self.oddo1_tab8 = (df_new_8['ODDO1'] - self.config.oddo1)
                self.df_new_tab8 = pd.DataFrame(df_new_8, columns=[f'F{i}H{j}' for i in range(1, self.config.F_columns + 1)
                                                                   for j in range(1, 5)])

            else:
                """
                pkl file is not found than data fetch from GCP and save pkl file in local path
                """
                folder_path = self.config.weld_pipe_pkl + self.parent.project_name
                print(folder_path)
                self.config.print_with_time("File not exist")
                try:
                    os.makedirs(folder_path)
                except:
                    self.config.print_with_time("Folder already exists")

                start_index, end_index = result[0][0], result[1][1]
                print(start_index, end_index)
                self.config.print_with_time("Start fetching at : ")
                # query_for_start1 = 'SELECT index,ROLL,ODDO1,ODDO2,[F1H1, F1H2, F1H3, F1H4, F2H1, F2H2, F2H3, F2H4,F3H1, F3H2, F3H3, F3H4, F4H1, F4H2, F4H3,F4H4, F5H1, F5H2, F5H3, F5H4, F6H1, F6H2, F6H3, F6H4,F7H1, F7H2, F7H3, F7H4, F8H1, F8H2, F8H3, F8H4, F9H1, F9H2, F9H3, F9H4, F10H1,F10H2, F10H3, F10H4,F11H1, F11H2, F11H3, F11H4, F12H1, F12H2, F12H3, F12H4, F13H1, F13H2, F13H3,F13H4, F14H1, F14H2, F14H3, F14H4,F15H1, F15H2, F15H3, F15H4, F16H1, F16H2, F16H3, F16H4, F17H1, F17H2, F17H3,F17H4, F18H1, F18H2, F18H3, F18H4,F19H1, F19H2, F19H3, F19H4, F20H1, F20H2, F20H3, F20H4, F21H1, F21H2, F21H3,F21H4, F22H1, F22H2, F22H3, F22H4,F23H1, F23H2, F23H3, F23H4, F24H1, F24H2, F24H3, F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4,F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1,F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4] FROM ' + self.config.table_name + ' WHERE index>{} AND index<{} order by index'
                query_for_start = (
                        "SELECT index,ROLL, ODDO1, ODDO2, ["
                        + self.config.sensor_str_hall +
                        "] FROM "
                        + self.config.table_name +
                        " WHERE index>={} AND index<={} ORDER BY index"
                )

                query_job = self.config.client.query(query_for_start.format(start_index, end_index))
                results = query_job.result()
                # results.to_csv("C:/Users/Shradha Agarwal/Desktop/bpcl clock/raw_data.csv")
                # print("result...", results)

                data = []
                self.index_tab8 = []
                oddo_1 = []
                oddo_2 = []
                indexes = []
                roll1 = []

                for row in results:
                    self.index_tab8.append(row[0])
                    roll1.append(row[1])
                    oddo_1.append(row[2])
                    oddo_2.append(row[3])
                    data.append(row[4])
                    """
                    Swapping the Pitch data to Roll data
                    """

                self.oddo1_tab8 = []
                self.oddo2_tab8 = []
                self.roll_t8 = []

                """
                Reference value will be consider
                """
                for odometer1 in oddo_1:
                    od1 = odometer1 - self.config.oddo1  ###16984.2 change According to run
                    self.oddo1_tab8.append(od1)
                for odometer2 in oddo_2:
                    od2 = odometer2 - self.config.oddo2  ###17690.36 change According to run
                    self.oddo2_tab8.append(od2)

                """
                Reference value will be consider
                """
                for roll2 in roll1:
                    roll3 = roll2 - self.config.roll_value
                    self.roll_t8.append(roll3)

                # query_for_start = 'SELECT index,[F1P1, F2P2, F3P3, F4P4, F5P1, F6P2, F7P3, F8P4, F9P1, F10P2, F11P3, F12P4, F13P1, F14P2, F15P3, F16P4, F17P1, F18P2, F19P3, F20P4, F21P1, F22P2, F23P3, F24P4, F25P1, F26P2, F27P3, F28P4, F29P1, F30P2, F31P3, F32P4, F33P1, F34P2, F35P3, F36P4] FROM ' + self.config.table_name + ' WHERE index>{} AND index<{} order by index'
                query_for_start = (
                        "SELECT index,["
                        + self.config.sensor_str_prox +
                        "] FROM "
                        + self.config.table_name +
                        " WHERE index>={} AND index<={} ORDER BY index"
                )
                query_job = self.config.client.query(query_for_start.format(start_index, end_index))
                results_1 = query_job.result()
                data1 = []
                self.index_hm_ori = []
                for row1 in results_1:
                    self.index_hm_ori.append(row1[0])
                    data1.append(row1[1])

                self.df_new_proximity_ori = pd.DataFrame(data1, columns=self.config.sensor_columns_prox)

                self.df_new_tab8 = pd.DataFrame(data, columns=[f'F{i}H{j}' for i in range(1, self.config.F_columns + 1)
                                                               for j in range(1, 5)])

                df_elem = pd.DataFrame({"index": self.index_tab8, "ODDO1": self.oddo1_tab8})
                frames = [df_elem, self.df_new_tab8]
                df_new = pd.concat(frames, axis=1, join='inner')

                for col in self.df_new_proximity_ori.columns:
                    df_new[col] = self.df_new_proximity_ori[col]

                df_new.reset_index(inplace=True)
                # print("Plotted data", df_new)
                df_new.to_pickle(folder_path + '/' + str(Weld_id) + '.pkl')
                self.config.print_with_time("Succesfully saved to pickle file")

        # self.parent.GenerateGraph()
        self.config.print_with_time("starting generatring graph  at : ")
        GenerateGraph(self)
        self.config.print_with_time("ending generatring graph  at : ")
        with self.config.connection.cursor() as cursor:
            ################# defect fetched from defect_sensor_hm #################
            # Fetch_weld_detail = "select id,pipe_id,absolute_distance_oddo1,upstream_oddo1,defect_type,defect_classification,angle_hr_m,length,breadth,depth from defect_sensor_hm where runid='%s' and pipe_id='%s'"

            ################# defect fetched from defect_clock_hm #################
            Fetch_weld_detail = "select id,pipe_id,absolute_distance,upstream,defect_type,dimension_classification,orientation,length,width_final,depth_new from defect_clock_hm where runid='%s' and pipe_id='%s'"

            cursor.execute(Fetch_weld_detail, (int(self.parent.runid), int(self.Weld_id)))
            self.myTableWidget3.setRowCount(0)
            allSQLRows = cursor.fetchall()
            if allSQLRows:
                for row_number, row_data in enumerate(allSQLRows):
                    self.myTableWidget3.insertRow(row_number)
                    for column_num, data in enumerate(row_data):
                        self.myTableWidget3.setItem(row_number, column_num,
                                                    QtWidgets.QTableWidgetItem(str(data)))
                        self.myTableWidget3.setContextMenuPolicy(Qt.CustomContextMenu)
                        self.myTableWidget3.customContextMenuRequested.connect(lambda: open_context_menu(self))
                        self.myTableWidget3.doubleClicked.connect(lambda: handle_table_double_click_pipe(self))


