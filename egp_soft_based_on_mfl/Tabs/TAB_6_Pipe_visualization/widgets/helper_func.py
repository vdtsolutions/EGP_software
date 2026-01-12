from PyQt5.QtWidgets import QMessageBox, QInputDialog, QMenu, QAction
from PyQt5 import QtWidgets
import egp_soft_based_on_mfl.Components.graph as graph
import egp_soft_based_on_mfl.Components.report_generator as Report
from google.cloud import bigquery
import json
import matplotlib.pyplot as plt
import pandas as pd
from PyQt5.QtCore import Qt

from egp_soft_based_on_mfl.main_window.widgets.helper_func import full_screen
from egp_soft_based_on_mfl.utils.common_helper_func import Width_calculation, lat_long, internal_or_external

# from egp_soft_based_on_mfl.Components.self.configs import self.config as self.config
# self.config.connection = self.config.self.config.connection
# company_list = []  # list of companies
# credentials = self.config.credentials
# project_id = self.config.project_id
# client = bigquery.Client(credentials=credentials, project=project_id)
# self.config = json.loads(open(r'D:\Anubhav\vdt_backend\egp_soft_based_on_mfl\utils\proximity_base_value.json').read())

def box_selection_all_defect(self):
    try:
        # Clear existing patches and annotations on the figure
        ax = self.figure.gca()

        # Iterate over all rows in the table
        row_count = self.myTableWidget3.rowCount()
        if row_count == 0:
            QMessageBox.warning(self, "No Data", "The table is empty. No defects to display.")
            return

        for row_number in range(row_count):
            defect_id = self.myTableWidget3.item(row_number, 0).text()
            weld_id = self.Weld_id
            runid = self.parent.runid

            with self.config.connection.cursor() as cursor:
                # query_for_coordinates = "SELECT id, start_observation, end_observation, start_sensor, end_sensor, length, breadth from defect_sensor_hm WHERE pipe_id = %s AND runid = %s AND id = %s"
                query_for_coordinates = "SELECT id, start_index, end_index, start_sensor, end_sensor, length, Width from defect_clock_hm WHERE pipe_id = %s AND runid = %s AND id = %s"
                cursor.execute(query_for_coordinates, (weld_id, runid, defect_id))
                result = cursor.fetchone()

                id, start_index, end_index, y_start_hm, y_end_hm, length_odd1, breadth = result

                if None in (start_index, end_index, y_start_hm, y_end_hm):
                    print(f"Warning: Invalid coordinates for defect ID {id}. Skipping.")
                    continue

                # Calculate rectangle coordinates
                rect_x = (start_index + end_index) / 2
                rect_y = (y_start_hm + y_end_hm) / 2

                # Draw the rectangle
                rect = plt.Rectangle(
                    (start_index, y_start_hm),
                    end_index - start_index,
                    y_end_hm - y_start_hm,
                    linewidth=1, edgecolor='black', facecolor='none'
                )
                ax.add_patch(rect)

                # Add the text annotation
                text_x = rect_x
                text_y = rect_y + (y_end_hm - y_start_hm) * 0.1  # Slightly above the box
                ax.text(
                    text_x, text_y,
                    # f"ID: {id}\nL: {length_odd1}\nW: {breadth}",
                    f"ID: {id}",
                    color='black',
                    ha='center', va='center',
                    fontsize=10, weight='bold',
                )
                # print(f"Rectangle and text drawn for defect ID: {id}.")

        # Refresh the canvas to display all rectangles and annotations
        self.canvas.draw_idle()

    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to draw boxes for all defects: {str(e)}")


def GenerateGraph(self):
    graph.generate_heat_map(self.canvas, self.parent.full_screen, self.df_new_tab8,
                            lambda eclick, erelease: line_select_callback3(self), self.parent.project_name, self.Weld_id, self.figure,
                            self.lower_sensitivity, self.upper_sensitivity, self.oddo1_tab8, self.index_tab8)




def generate_report(self):
    Report.generate(self.parent.project_name, self.runid)


def handle_table_double_click_pipe(self):
    weld_id = self.Weld_id
    runid = self.parent.runid

    selected_row = self.myTableWidget3.currentRow()
    if selected_row == -1:
        QMessageBox.warning(self, "No Selection", "Please double-click on a valid cell.")
        return

    defect_id = self.myTableWidget3.item(selected_row, 0).text()
    try:
        with self.config.connection.cursor() as cursor:
            query_for_coordinates = "SELECT id, start_observation, end_observation, start_sensor, end_sensor, length, breadth from defect_sensor_hm WHERE pipe_id = %s AND runid = %s AND id = %s"
            cursor.execute(query_for_coordinates, (weld_id, runid, defect_id))
            result = cursor.fetchone()
            print(f"Query Result: {result}")

            if not result:
                QMessageBox.warning(self, "No Data", "No data found for the selected defect.")
                return

            id, start_index, end_index, y_start_hm, y_end_hm, length_odd1, breadth = result

            # Calculate rectangle coordinates
            rect_x = (start_index + end_index) / 2
            rect_y = (y_start_hm + y_end_hm) / 2

            ax = self.figure.gca()
            # Draw the rectangle
            rect = plt.Rectangle(
                (start_index, y_start_hm),
                end_index - start_index,
                y_end_hm - y_start_hm,
                linewidth=1, edgecolor='black', facecolor='none'
            )
            ax.add_patch(rect)

            # Add the text annotation
            text_x = rect_x
            text_y = rect_y + (y_end_hm - y_start_hm) * 0.1  # Slightly above the box
            ax.text(
                text_x, text_y,
                f"ID: {id}\nL: {length_odd1}\nW: {breadth}",
                color='black',
                ha='center', va='center',
                fontsize=10, weight='bold',
            )

            self.canvas.draw_idle()  # Ensure the canvas is updated.

    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to draw box: {str(e)}")



def GenerateGraph(self):
    graph.generate_heat_map(self, self.canvas, lambda: full_screen(self.parent), self.df_new_tab8,
                            lambda eclick, erelease: line_select_callback3(self, eclick, erelease),
                            self.parent.project_name, self.Weld_id, self.figure,
                            self.lower_sensitivity, self.upper_sensitivity, self.oddo1_tab8, self.index_tab8)


def line_select_callback3(self, eclick, erelease):
    self.rect_start_pipe = eclick.xdata, eclick.ydata
    self.rect_end_pipe = erelease.xdata, erelease.ydata
    draw_rectangle_3(self)

def draw_rectangle_3(self):
    # Function to draw a rectangle on the Matplotlib plot
    if self.rect_start_pipe is not None and self.rect_end_pipe is not None:
        for patch in self.figure.gca().patches:
            patch.remove()
        x_start, y_start = self.rect_start_pipe
        x_end, y_end = self.rect_end_pipe
        if x_start is not None and y_start is not None and x_end is not None and y_end is not None:
            rect = plt.Rectangle(
                (min(x_start, x_end), min(y_start, y_end)),
                abs(x_end - x_start),
                abs(y_end - y_start),
                edgecolor='black',
                linewidth=1,
                fill=False
            )
            self.figure.gca().add_patch(rect)
            self.canvas.draw()
            show_name_dialog3(self)


def show_name_dialog3(self):
    while True:
        name, ok = QInputDialog.getText(self, 'Enter Name', 'Enter the name of the drawn box:')
        if ok:
            if name.strip():  # Check if the entered name is not empty or just whitespace
                x_start, y_start = self.rect_start_pipe
                x_end, y_end = self.rect_end_pipe
                runid = self.parent.runid
                pipe = self.Weld_id
                self.index_hm_set = self.index_tab8
                start_index15 = self.index_hm_set[round(x_start)]
                end_index15 = self.index_hm_set[round(x_end)]
                start_index_c = round(x_start)
                end_index_c = round(x_end)
                y_start15 = round(y_start)
                y_end15 = round(y_end)
                print("start_sensor", y_start15)
                print("end_sensor", y_end15)
                finial_defect_list=[]

                """
                Fetching data from Google Big Query each holl sensor
                """
                # query_for_start = 'SELECT index,ODDO1,ODDO2,[F1H1 ,F1H2 ,F1H3 ,F1H4 ,F2H1 ,F2H2 ,F2H3 ,F2H4 ,F3H1 ,F3H2 ,F3H3 ,F3H4 ,F4H1 ,F4H2 ,F4H3 ,' \
                #                   'F4H4 ,F5H1 ,F5H2 ,F5H3 ,F5H4 ,F6H1 ,F6H2 ,F6H3 ,F6H4 ,F7H1 ,F7H2 ,F7H3 ,F7H4 ,F8H1 ,F8H2 ,F8H3 ,' \
                #                   'F8H4 ,F9H1 ,F9H2 ,F9H3 ,F9H4 ,F10H1 ,F10H2 ,F10H3 ,F10H4 ,F11H1 ,F11H2 ,F11H3 ,F11H4 ,F12H1 ,F12H2 ,F12H3 ,' \
                #                   'F12H4 ,F13H1 ,F13H2 ,F13H3 ,F13H4 ,F14H1 ,F14H2 ,F14H3 ,F14H4 ,F15H1 ,F15H2 ,F15H3 ,F15H4 ,F16H1 ,F16H2 ,F16H3 ,' \
                #                   'F16H4 ,F17H1 ,F17H2 ,F17H3 ,F17H4 ,F18H1 ,F18H2 ,F18H3 ,F18H4 ,F19H1 ,F19H2 ,F19H3 ,F19H4 ,F20H1 ,F20H2 ,F20H3 ,' \
                #                   'F20H4 ,F21H1 ,F21H2 ,F21H3 ,F21H4 ,F22H1 ,F22H2 ,F22H3 ,F22H4 ,F23H1 ,F23H2 ,F23H3 ,F23H4 ,F24H1 ,F24H2 ,F24H3 ,' \
                #                   'F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4,' \
                #                   'F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1, ' \
                #                   'F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4],ROLL FROM ' + self.config.table_name + ' WHERE index>={} AND index<={} AND runid={} order by index'
                query_for_start = (
                        "SELECT index, ODDO1, ODDO2, ["
                        + self.config.sensor_str_hall +
                        "], ROLL FROM "
                        + self.config.table_name +
                        " WHERE index>={} AND index<={} AND runid={} ORDER BY index"
                )
                query_job = self.config.client.query(query_for_start.format(start_index15, end_index15, runid))
                results = query_job.result()
                """
                End fetching data from Google Bigquery
                """
                index1 = []
                oddo_1 = []
                oddo_2 = []
                holl_sensor = []
                roll = []
                for k in results:
                    index1.append(k[0])
                    oddo_1.append(k[1])
                    oddo_2.append(k[2])
                    holl_sensor.append(k[3])
                    roll.append(k[4])

                self.oddo1_wp = []
                self.oddo2_wp = []
                roll4 = []
                for odometer1 in oddo_1:
                    od1 = odometer1 - self.config.oddo1  ### change According to run
                    self.oddo1_wp.append(od1)
                for odometer2 in oddo_2:
                    od2 = odometer2 - self.config.oddo2  ### change According to run
                    self.oddo2_wp.append(od2)
                """
                Reference value will be consider
                """
                for roll2 in roll:
                    roll3 = roll2 - self.config.roll_value
                    roll4.append(roll3)
                """
                Fetching data from Google Big Query each proximity sensor
                """
                # query_for_start_proximity = 'SELECT index,[F1P1,F2P2,F3P3,F4P4,F5P1,F6P2,F7P3,F8P4,F9P1,F10P2,F11P3,F12P4,F13P1,F14P2,F15P3,F16P4,F17P1,F18P2,F19P3,F20P4,F21P1,F22P2,F23P3,F24P4, F25P1, F26P2, F27P3, F28P4, F29P1, F30P2, F31P3, F32P4, F33P1, F34P2, F35P3, F36P4] FROM ' + self.config.table_name + ' WHERE index>{} AND index<{} order by index'
                query_for_start_proximity = (
                        "SELECT index, ["
                        + self.config.sensor_str_prox +
                        "] FROM "
                        + self.config.table_name +
                        " WHERE index>{} AND index<{} ORDER BY index"
                )
                query_job_proximity = self.config.client.query(query_for_start_proximity.format(start_index15, end_index15))
                results_1 = query_job_proximity.result()
                proximity = []
                for row1 in results_1:
                    proximity.append(row1[1])
                self.df_new_proximity = pd.DataFrame(proximity,
                                                     columns=self.config.sensor_columns_prox)


                """
                Calculate Upstream Distance oddo1 and oddo2
                """
                upstream_oddo1=self.oddo1_wp[0]-self.oddo1_tab8[0]
                print("upstream_oddo1=>",upstream_oddo1)

                """
                Calculate length of the defect
                """
                length_of_defect_oddo1=round(self.oddo1_wp[-1]-self.oddo1_wp[0])
                length_of_defect_oddo2 = round(self.oddo2_wp[-1] - self.oddo2_wp[0])
                print("length_of_defect_oddo1=>",length_of_defect_oddo1)
                print("length_of_defect_oddo2=>",length_of_defect_oddo2)

                """
                Calculate Abs.Distance of the defect
                """
                Abs_Distance=self.oddo1_wp[0]
                print("Abs.distance_oddo1=>", Abs_Distance)

                """
                Calculate Width of the Defect
                """
                Width=Width_calculation(y_start15, y_end15)
                Width=round(Width)
                print("Width of Defect=>", Width)

                """
                Find the maximum value of each holl sensor
                """

                # each_holl_sensor_max_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                #                               0, 0, 0, 0, 0, 0, 0, 0,
                #                               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                #                               0, 0, 0, 0, 0, 0, 0, 0,
                #                               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                #                               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                #                               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                each_holl_sensor_max_value = [0] * self.config.num_of_sensors
                # print("start_index", start_index15)
                # print("end_index", end_index15)
                # print("start_sensor", y_start15)
                # print("end_sensor", y_end15)
                for l, data in enumerate(holl_sensor):
                    for m, data1 in enumerate(data):
                        if m >= y_start15 - 1 and m < y_end15:
                            if data1 > each_holl_sensor_max_value[m]:
                                each_holl_sensor_max_value[m] = data1
                #print("maximum_value", each_holl_sensor_max_value)
                """
                Get rows of start_observation at the 0th Position of element in holl sensor 2d list
                """
                initial_observation = holl_sensor[0]
                # print("base_value", initial_observation)
                kx = []
                for i2 in range(0, self.config.num_of_sensors):
                    if i2 >= y_start15-1 and i2 <y_end15:
                        kx.append(initial_observation[i2])
                    else:
                        kx.append(0)
                #print("initial_observation", kx)
                """
                Difference between max_value_list and initial_observation
                """
                zip_object = zip(each_holl_sensor_max_value, kx)
                difference_list = []
                for list1_i, list2_i in zip_object:
                    difference_list.append(list1_i - list2_i)
                # print("difference list",difference_list)
                """
                Get max_value_difference_value
                """

                max_value_difference_value = max(difference_list)
                # print("max_value_diiference_value",max_value_difference_value)

                """
                Get index max_value_difference_value
                """
                max_value_difference_index = difference_list.index(max_value_difference_value)
                print("sensor_no", max_value_difference_index)
                """
                Check max_value_list inside the index and get max_value
                """
                max_value = each_holl_sensor_max_value[max_value_difference_index]
                #print("max_value", max_value)

                """
                Check initial_observation inside the index and get base value
                """
                base_value=initial_observation[max_value_difference_index]
                #print("base_value",base_value)

                depth=(max_value-base_value)/base_value*100
                depth=round(depth)
                print("depth...",depth)

                internal_external=internal_or_external(self.df_new_proximity, max_value_difference_index)
                print("internal_external",internal_external)

                """
                .................Orientation Calculation..........................
                """
                angle = defect_angle_x(roll4, max_value_difference_index)
                print("angle", angle)

                """
                Calculate latitude and longitude 
                """
                long, lat = lat_long(Abs_Distance, self.runid)
                print("latitude", lat)
                print("longitude", long)

                thickness_pipe = self.config.pipe_thickness     ### Value Change according to wall thickness
                dimension_classification=get_type_defect_2(thickness_pipe, runid, length_of_defect_oddo1, Width)
                print("dimension_classification", dimension_classification)

                finial_defect_list.append({"start_index": start_index_c, "end_index": end_index_c,
                                           "start_sensor": y_start15, "end_sensor": y_end15,
                                           "sensor_no": max_value_difference_index,
                                           "Absolute_distance": Abs_Distance, "Upstream": upstream_oddo1,
                                           "Pipe_length":self.pipe_len_8,
                                           "Feature_type":internal_external, "Feature_identification": name,
                                           "Dimension_classification": dimension_classification,
                                           "Orientation":angle, "WT":None,
                                           "length": length_of_defect_oddo1, "Width": Width, "Depth_mm": None,
                                           "Depth_percentage":depth, "latitude":lat, "longitude":long})
                for i in finial_defect_list:
                    start_index = i['start_index']
                    end_index = i['end_index']
                    start_sensor = i['start_sensor']
                    end_sensor = i['end_sensor']
                    sensor_no = i['sensor_no']
                    Absolute_distance = round(i['Absolute_distance'], 2)
                    Upstream = round(i['Upstream'], 2)
                    Pipe_length = round(i['Pipe_length'], 2)
                    Feature_type = i['Feature_type']
                    Feature_identification = i['Feature_identification']
                    Dimension_classification = i['Dimension_classification']
                    Orientation = i['Orientation']
                    WT = i['WT']
                    length = i['length']
                    Width = i['Width']
                    Depth_mm=i['Depth_mm']
                    Depth_percentage=i['Depth_percentage']
                    latitude=i['latitude']
                    longitude=i['longitude']
                    """
                    Insert data into database
                    """
                    with self.config.connection.cursor() as cursor:
                        # query_defect_insert = "INSERT into defect_sensor_hm (runid,pipe_id,start_observation,end_observation,start_sensor,end_sensor,sensor_no,absolute_distance_oddo1,Pipe_length,upstream_oddo1,defect_type,type,defect_classification,angle_hr_m,pipe_thickness,length,breadth,depth,latitude,longitude) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

                        # cursor.execute(query_defect_insert, (
                        #     int(runid), pipe, start_index, end_index, start_sensor, end_sensor, sensor_no,
                        #     Absolute_distance, Pipe_length, Upstream, Feature_type, Feature_identification,
                        #     Dimension_classification,
                        #     Orientation, WT, length, Width, Depth_percentage,latitude,longitude))

                        query_defect_insert = "INSERT into defect_clock_hm(runid, pipe_id, pipe_length, start_index, end_index, start_sensor, end_sensor, absolute_distance, upstream, length, Width_final,depth_new, orientation, defect_type, dimension_classification, latitude, longitude) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                        cursor.execute(query_defect_insert, (
                            int(runid), pipe, Pipe_length, start_index, end_index,
                                start_sensor, end_sensor, Absolute_distance,
                                Upstream, length, Width, Depth_percentage, Orientation, Feature_type, Dimension_classification,
                                latitude, longitude))


                        self.config.connection.commit()
                        QMessageBox.information(self, 'Success', 'Data saved')

                    with self.config.connection.cursor() as cursor:
################################## defect fetched from defect_sensor_hm ##################################
                        # Fetch_weld_detail = "select id,pipe_id,absolute_distance_oddo1,upstream_oddo1,defect_type,defect_classification,angle_hr_m,length,breadth,depth from defect_sensor_hm where runid='%s' and pipe_id='%s'"

################################## defect fetched from defect_clock_hm ##################################
                        Fetch_weld_detail = "select id,pipe_id,absolute_distance,upstream,defect_type,dimension_classification,orientation,length,Width,depth_new from defect_clock_hm where runid='%s' and pipe_id='%s'"

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

                break  # Exit the loop if a valid name is provided
            else:
                QMessageBox.warning(self, 'Invalid Input', 'Please enter a name.')
        else:
            print('Operation canceled.')
            break

def open_context_menu(self, position):
    index = self.myTableWidget3.indexAt(position)
    if not index.isValid():
        return

    # Select the entire row
    self.myTableWidget3.selectRow(index.row())
    context_menu = QMenu()
    # context_menu = QtWidgets.QMenuBar()
    delete_action = QAction("Delete Row", self)
    # menuEdit = QtWidgets.QMenu(self.menubar)
    delete_action.triggered.connect(lambda: delete_row(self, index.row()))
    context_menu.addAction(delete_action)
    context_menu.exec_(self.myTableWidget3.viewport().mapToGlobal(position))

def delete_row(self, row):
    if row < 0:
        return

    # Get the ID of the selected row
    id_item = self.myTableWidget3.item(row, 0)
    if id_item is None:
        return
    row_id = id_item.text()

    # Confirm deletion
    reply = QMessageBox.question(self, 'Delete Row', 'Are you sure you want to delete this row?',
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    if reply == QMessageBox.Yes:
        # Delete the row from the database
        with self.config.connection.cursor() as cursor:
            # print("row_id....",row_id)
            Fetch_weld_detail = "DELETE from defect_sensor_hm WHERE id='%s'"
            # Execute query.
            cursor.execute(Fetch_weld_detail, (int(row_id)))
            # cursor.execute(f"DELETE from defect_sensor_hm WHERE id=",row_id)
            self.config.connection.commit()
            # self.config.connection.close()
            # Delete the row from the table widget
            self.myTableWidget3.removeRow(row)
            QMessageBox.information(self, "Information", "Row deleted successfully")


def defect_angle_x(roll_x, sensor):
    roll_angle=list(roll_x)
    roll_position=roll_angle[0]
    print("roll_postion and sensor", roll_position, sensor)
    x = 1.73            ################# x 1.73 for 12 inch and 1.74  for 14 inch pipe #################
    y = 3.30            ################# y 3.30 for 12 inch and 3.37 for 14 inch pipe #################
    z = 4.52            ################# z 4.52 for 12 inch and 5.63 for 14 inch pipe #################
    a = 8.2             ################# a 8.2 for 12 inch and 6.5 for 14 inch pipe #################
    b = int(sensor / 16)
    c = b * a

    d = int(sensor / 8)
    e = d - b
    f = e * z

    g = int(sensor / 4)
    h = g - (b + e)
    i = h * y

    j = sensor * x
    # roll_position = 0.15
    initial_calculation_of_each_sensor = c + f + i + j
    print("a", initial_calculation_of_each_sensor)
    if roll_position > 0:
        # print(roll_position)
        roll_position = roll_position + initial_calculation_of_each_sensor
        if roll_position > 360:
            print(roll_position)
            roll_position = roll_position % 360
    else:
        roll_position = 360 + roll_position
        roll_position = roll_position + initial_calculation_of_each_sensor
        if roll_position > 360:
            roll_position = roll_position % 360
            angle = initial_calculation_of_each_sensor + roll_position
            print("angle rotation", angle)
            print("angle", roll_position)
    adsmd = roll_position / 30
    k = int(adsmd)
    m = int(roll_position % 30)
    g = ':'
    angle_hr_min = str(k) + g + str(m)
    return angle_hr_min


def get_type_defect_2(geometrical_parameter,runid,length_defect,width_defect):
    L_ratio_W = length_defect / width_defect
    if width_defect > 3 * geometrical_parameter and length_defect > 3 * geometrical_parameter:
        type_of_defect = 'GENERAL'
        return type_of_defect
    elif (6 * geometrical_parameter >= width_defect >= 1 * geometrical_parameter and 6 * geometrical_parameter >= length_defect >= 1 * geometrical_parameter) and (
            0.5 < (L_ratio_W) < 2) and not (
            width_defect >= 3 * geometrical_parameter and length_defect >= 3 * geometrical_parameter):
        type_of_defect = 'PITTING'
        return type_of_defect
    elif (1 * geometrical_parameter <= width_defect < 3 * geometrical_parameter) and (L_ratio_W >= 2):
        type_of_defect = 'AXIAL GROOVING'
        return type_of_defect
    elif L_ratio_W <= 0.5 and 3 * geometrical_parameter > length_defect >= 1 * geometrical_parameter:
        type_of_defect = 'CIRCUMFERENTIAL GROOVING'
        return type_of_defect
    elif 0 < width_defect < 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
        type_of_defect = 'PINHOLE'
        return type_of_defect
    elif 0 < width_defect < 1 * geometrical_parameter and length_defect >= 1 * geometrical_parameter:
        type_of_defect = 'AXIAL SLOTTING'
        return type_of_defect
    elif width_defect >= 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
        type_of_defect = 'CIRCUMFERENTIAL SLOTTING'
        return type_of_defect