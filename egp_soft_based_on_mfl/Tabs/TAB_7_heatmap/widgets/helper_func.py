from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QMessageBox, QFileDialog, QMenu, QAction, QInputDialog,
)
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from google.cloud import bigquery
import json
import pandas as pd
import os
import pymysql

from egp_soft_based_on_mfl.utils.common_helper_func import lat_long, Width_calculation, internal_or_external, get_type_defect_1



def reset_btn_fun_chm(self):
    if self.figure_tab9.gca().patches:
        for patch in self.figure_tab9.gca().patches:
            patch.remove()
        for text in self.figure_tab9.gca().texts:
            text.remove()
        self.canvas_tab9.draw()
        self.rect_start_clockhm = None  # Store the starting point of the rectangle
        self.rect_end_clockhm = None


def all_box_selection_ori_heatmap(self):
    try:
        # Clear existing patches and annotations on the figure
        ax = self.figure_tab9.gca()

        # Iterate over all rows in the table
        row_count = self.myTableWidget_tab9.rowCount()
        if row_count == 0:
            QMessageBox.warning(self, "No Data", "The table is empty. No defects to display.")
            return

        for row_number in range(row_count):
            defect_id = self.myTableWidget_tab9.item(row_number, 0).text()
            weld_id = self.Weld_id_tab9
            runid = self.parent.runid

            with self.config.connection.cursor() as cursor:
                query_for_coordinates = "SELECT id, start_index, end_index, start_sensor, end_sensor from defect_clock_hm WHERE pipe_id = %s AND runid = %s AND id = %s"
                cursor.execute(query_for_coordinates, (weld_id, runid, defect_id))
                result = cursor.fetchone()

                id, start_index, end_index, y_start_hm, y_end_hm = result

                if None in (start_index, end_index, y_start_hm, y_end_hm):
                    print(f"Warning: Invalid coordinates for defect ID {id}. Skipping.")
                    continue

                # # Calculate rectangle coordinates
                # rect_x = (start_index + end_index) / 2
                # rect_y = (y_start_hm + y_end_hm) / 2
                #
                # # Draw the rectangle
                # rect = plt.Rectangle(
                #     (start_index, y_start_hm),
                #     end_index - start_index,
                #     y_end_hm - y_start_hm,
                #     linewidth=1, edgecolor='black', facecolor='none'
                # )
                # ax.add_patch(rect)

                # Adjust for correct alignment with Plotly's rectangle dimensions
                rect_x = start_index
                rect_y = y_start_hm
                rect_width = (end_index - start_index)  # Adjust for center alignment
                rect_height = ((y_end_hm + 0.5) - (y_start_hm - 0.5))   # Adjust for center alignment

                # rect_x = start_index + 0.5
                # rect_y = y_start_hm - 0.5
                # rect_width = (end_index + 0.5) - (start_index - 0.5)
                # rect_height = (y_end_hm + 0.5) - (y_start_hm - 0.5)


                # Create and add the rectangle to the plot
                rect = plt.Rectangle(
                    (rect_x, rect_y),  # Set bottom-left corner
                    rect_width,  # Width
                    rect_height,  # Height
                    linewidth=1, edgecolor='black', facecolor='none'
                )
                ax.add_patch(rect)

                # Add the text annotation
                text_x = start_index + (end_index - start_index)/2
                text_y = rect_y - 2  # Slightly above the box
                # text_y = rect_y + (y_end_hm - y_start_hm) * 0.1  # Slightly above the box
                ax.text(
                    text_x, text_y,
                    # f"ID: {id}\nL: {length_odd1}\nW: {breadth}",
                    f"{id}",
                    color='white',
                    ha='center', va='center',
                    fontsize=9, weight='bold',
                    path_effects=[
                    path_effects.withStroke(linewidth=2, foreground='black')  # Black outline
                ]
                    )
                # print(f"Rectangle and text drawn for defect ID: {id}.")

        # Refresh the canvas to display all rectangles and annotations
        self.canvas_tab9.draw_idle()

    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to draw boxes for all defects: {str(e)}")


def export_to_excel(self):
    """Export table data to an Excel file with a user-selected location and filename."""
    rows = self.myTableWidget_tab9.rowCount()
    columns = self.myTableWidget_tab9.columnCount()

    # Check if the table is empty
    if rows == 0 or columns == 0:
        QMessageBox.warning(self, 'Empty Table', 'The table is empty. Please add data before exporting.')
        return  # Exit the function early

    # Extract table data into a list of dictionaries (for easy conversion to DataFrame)
    data = []
    for row in range(rows):
        row_data = {}
        for col in range(columns):
            header = self.myTableWidget_tab9.horizontalHeaderItem(col).text()
            item = self.myTableWidget_tab9.item(row, col)
            row_data[header] = item.text() if item else ""
        data.append(row_data)

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Open a file dialog to choose the save location and filename
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getSaveFileName(
        self,
        "Save Excel File",
        "",
        "Excel Files (*.xlsx);;All Files (*)",
        options=options
    )

    if file_path:  # If the user selects a file
        # Ensure the file has the correct extension
        if not file_path.endswith('.xlsx'):
            file_path += '.xlsx'

        # Save the DataFrame to the selected file
        df.to_excel(file_path, index=False)

        QMessageBox.information(self, 'Success', 'Data successfully saved')
    else:
        QMessageBox.warning(self, 'Cancelled', 'Save operation was cancelled.')





def open_context_menu_ori_tab9(self, position):
    index = self.myTableWidget_tab9.indexAt(position)
    print("index", index)
    if not index.isValid():
        return

    # Select the entire row
    self.myTableWidget_tab9.selectRow(index.row())
    context_menu = QMenu()
    # context_menu = QtWidgets.QMenuBar()
    delete_action = QAction("Delete Row", self)
    # menuEdit = QtWidgets.QMenu(self.menubar)
    delete_action.triggered.connect(lambda: delete_row_ori_tab9(self, index.row()))
    context_menu.addAction(delete_action)
    context_menu.exec_(self.myTableWidget_tab9.viewport().mapToGlobal(position))


def delete_row_ori_tab9(self, row):
    if row < 0:
        return

    # Get the ID of the selected row
    id_item = self.myTableWidget_tab9.item(row, 0)
    if id_item is None:
        return
    row_id = id_item.text()
    print("row_id", row_id)

    # Confirm deletion
    reply = QMessageBox.question(self, 'Delete Row', 'Are you sure you want to delete this row?',
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    if reply == QMessageBox.Yes:
        try:
            connection2 = pymysql.connect(host='localhost', user='root', password='root', db='mfldesktop')
            # Delete the row from the database
            with connection2.cursor() as cursor:
                # print("row_id....",row_id)
                Fetch_weld_detail = "DELETE from defect_sensor_hm WHERE id='%s'"
                # Execute query.
                cursor.execute(Fetch_weld_detail, (int(row_id)))
                # cursor.execute(f"DELETE from defect_sensor_hm WHERE id=",row_id)
                connection2.commit()
                # connection.close()
                # Delete the row from the table widget
                self.myTableWidget_tab9.removeRow(row)
                QMessageBox.information(self, "Information", "Row deleted successfully")
        except:
            pass


from PyQt5.QtCore import QMetaObject, Qt, Q_ARG

def handle_console_message(self, level, msg, line, source):
    msg = msg.strip()

    if msg.startswith("SELECTED_BOX_BOUNDS:"):
        try:
            import json
            box = json.loads(msg.replace("SELECTED_BOX_BOUNDS:", ""))
            print("📦 [Plotly] Selection received:", box)

            # Dummy event objects (same as before)
            class EClick:
                def __init__(self, x, y):
                    self.xdata = x
                    self.ydata = y

            class ERelease:
                def __init__(self, x, y):
                    self.xdata = x
                    self.ydata = y

            eclick = EClick(box["x0"], box["y1"])
            erelease = ERelease(box["x1"], box["y0"])

            # ✅ Invoke the function on the Qt GUI thread
            QMetaObject.invokeMethod(
                self,
                "run_line_select_callback_chm",
                Qt.QueuedConnection,
                Q_ARG(object, eclick),
                Q_ARG(object, erelease)
            )

        except Exception as e:
            print(f"❌ [BridgeError] Failed to parse selection: {e}")

    elif msg.startswith("MODE_TOGGLE:"):
        print(f"🎛️ {msg}")




def line_select_callback_chm(self, eclick, erelease):
    print("✅ [Triggered] line_select_callback_chm now running...")
    self.rect_start_chm = eclick.xdata, eclick.ydata
    self.rect_end_chm = erelease.xdata, erelease.ydata
    draw_rectangle_chm(self)


def draw_rectangle_chm(self):
    # Function to draw a rectangle on the Matplotlib plot
    if self.rect_start_chm is not None and self.rect_end_chm is not None:
        for patch in self.figure_tab9.gca().patches:
            patch.remove()
        x_start, y_start = self.rect_start_chm
        x_end, y_end = self.rect_end_chm
        if x_start is not None and y_start is not None and x_end is not None and y_end is not None:
            rect = plt.Rectangle(
                (min(x_start, x_end), min(y_start, y_end)),
                abs(x_end - x_start),
                abs(y_end - y_start),
                edgecolor='black',
                linewidth=1,
                fill=False
            )
            self.figure_tab9.gca().add_patch(rect)
            self.canvas_tab9.draw()
            show_name_dialog_chm(self)



def show_name_dialog_chm(self):
    credentials = self.config.credentials
    project_id = self.config.project_id
    client = bigquery.Client(credentials=credentials, project=project_id)
    while True:
        name, ok = QInputDialog.getText(self, 'Enter Name', 'Enter the name of the drawn box:')
        if ok:
            if name.strip():  # Check if the entered name is not empty or just whitespace
                x_start, y_start = self.rect_start_chm
                x_end, y_end = self.rect_end_chm
                runid = self.runid
                pipe = self.Weld_id_tab9
                start_index15 = self.index_chm[round(x_start)]
                end_index15 = self.index_chm[round(x_end)]
                start_index_c = round(x_start)
                end_index_c = round(x_end)
                y_start15 = round(y_start)
                y_end15 = round(y_end)
                print("start_index15", start_index15)
                print("end_index15", end_index15)
                print("start_sensor", y_start15)
                print("end_sensor", y_end15)
                print("start_index_c", start_index_c)
                print("end_index_c", end_index_c)

                finial_defect_list = []

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
                #                   'F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4],' \
                #                   'ROLL FROM ' + Config.table_name + ' WHERE index>={} AND index<={} AND runid={} order by index'
                query_for_start = (
                        "SELECT index, ODDO1, ODDO2, ["
                        + self.config.sensor_str_hall +
                        "], ROLL FROM "
                        + self.config.table_name +
                        " WHERE index>={} AND index<={} AND runid={} ORDER BY index"
                )
                query_job = client.query(query_for_start.format(start_index15, end_index15, runid))
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

                # print('oddo1', oddo_1)

                self.oddo1_chmd = []
                self.oddo2_chmd = []
                roll4 = []
                for odometer1 in oddo_1:
                    od1 = odometer1 - self.config.oddo1  ### change According to run
                    self.oddo1_chmd.append(od1)
                for odometer2 in oddo_2:
                    od2 = odometer2 - self.config.oddo2  ### change According to run
                    self.oddo2_chmd.append(od2)
                """
                Reference value will be consider
                """
                for roll2 in roll:
                    roll3 = roll2 - self.config.roll_value
                    roll4.append(roll3)
                """
                Fetching data from Google Big Query each proximity sensor
                """
                # query_for_start_proximity = 'SELECT index,[F1P1,F2P2,F3P3,F4P4,F5P1,F6P2,F7P3,F8P4,F9P1,F10P2,F11P3,F12P4,F13P1,F14P2,F15P3,F16P4,F17P1,F18P2,F19P3,F20P4,F21P1,F22P2,F23P3,F24P4, F25P1, F26P2, F27P3, F28P4, F29P1, F30P2, F31P3, F32P4, F33P1, F34P2, F35P3, F36P4] FROM ' + config.table_name + ' WHERE index>{} AND index<{} order by index'
                query_for_start_proximity = (
                        "SELECT index,["
                        + self.config.sensor_str_prox +
                        "] FROM "
                        + self.config.table_name +
                        " WHERE index>={} AND index<={} ORDER BY index"
                )
                query_job_proximity = client.query(query_for_start_proximity.format(start_index15, end_index15))
                results_1 = query_job_proximity.result()
                proximity = []
                for row1 in results_1:
                    proximity.append(row1[1])
                self.df_new_proximity_chmd = pd.DataFrame(proximity,
                                                          columns=self.config.sensor_columns_prox)

                # print("oddo1_chmd", self.oddo1_chmd)
                # print("oddo1_li_chm", self.oddo1_li_chm)

                submatrix = self.clock_col.iloc[start_index_c:end_index_c + 1, y_start15:y_end15 + 1]
                # submatrix = submatrix.apply(pd.to_numeric, errors='coerce')  # Ensure numeric data
                if submatrix.isnull().values.any():
                    print("Submatrix contains NaN values, skipping this iteration.")
                    continue
                print(submatrix)
                two_d_list = submatrix.values.tolist()

                max_value = submatrix.max().max()
                min_positive = min(x for row in two_d_list for x in row if x > 0)

                depth_old = (max_value-min_positive)/min_positive*100
                print("depth_old", depth_old)

                """
                Calculate Upstream Distance oddo1 and oddo2
                """
                upstream_oddo1=(self.oddo1_chmd[0]-self.oddo1_li_chm[0])/1000
                print("upstream_oddo1=>", upstream_oddo1)

                """
                Calculate length of the defect
                """
                length_of_defect_oddo1=round(self.oddo1_chmd[-1] - self.oddo1_chmd[0])
                length_of_defect_oddo2 = round(self.oddo2_chmd[-1] - self.oddo2_chmd[0])
                print("length_of_defect_oddo1=>", length_of_defect_oddo1)
                print("length_of_defect_oddo2=>", length_of_defect_oddo2)

                """
                Calculate Abs.Distance of the defect
                """
                Abs_Distance=(self.oddo1_chmd[0])/1000
                print("Abs.distance_oddo1=>", Abs_Distance)

                """
                Calculate latitude and longitude 
                """
                long, lat = lat_long(Abs_Distance, self.runid)
                print("latitude", lat)
                print("longitude", long)

                """
                Calculate Width of the Defect
                """
                Width=Width_calculation(y_start15, y_end15)
                Width=round(Width)
                print("Width of Defect=>", Width)

                counter_difference_1 = (y_end15 + 1) - (y_start15 + 1)
                divid_1 = int(counter_difference_1/2)
                center_1 = y_start15 + divid_1

                factor1_1 = divid_1 * self.config.w_per_1
                start1_1 = (int(center_1 - factor1_1)) - 1
                end1_1 = (int(center_1 + factor1_1)) - 1

                width_new = Width_calculation(start1_1, end1_1)
                print("width_new", width_new)

                """
                Calculate Wall thickness
                """
                # if self.Weld_id_tab9 == 2:
                #     wt = Config.pipe_thickness
                # else:
                #     wt = Config.pipe_thickness

                wt = self.config.pipe_thickness

                """
                Find the maximum value of each holl sensor
                """
                each_holl_sensor_max_value = [i*0 for i in range(1, 145)]

                for l, data in enumerate(self.clock_data_col):
                    # print("l", l)
                    # print("data", data)
                    for m, data1 in enumerate(data):
                        # print("m", m)
                        # print("data1", data1)
                        if m >= y_start15 - 1 and m < y_end15:
                            if data1 > each_holl_sensor_max_value[m]:
                                each_holl_sensor_max_value[m] = data1
                # print("maximum_value", each_holl_sensor_max_value)
                """
                Get rows of start_observation at the 0th Position of element in holl sensor 2d list
                """
                initial_observation = self.clock_data_col[0]
                # print("base_value", initial_observation)
                kx = []
                for i2 in range(0, self.config.num_of_sensors):
                    if i2 >= y_start15 - 1 and i2 < y_end15:
                        kx.append(initial_observation[i2])
                    else:
                        kx.append(0)
                # print("initial_observation", kx)
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
                max_value = self.mean_clock_data[max_value_difference_index]
                print("max_value", max_value)
                """
                Check initial_observation inside the index and get base value
                """
                index_val = round((y_start15 + y_end15)/2)
                base_value = self.mean_clock_data[index_val]
                print("base_value", base_value)

                # depth_old = abs(((max_value - base_value) / base_value) * 100)
                # print("depth_old...", depth_old)

                depth_new = round((((length_of_defect_oddo1 / Width) * (max_value / base_value)) * 100) / self.config.pipe_thickness, 2)
                print("depth_new...", depth_new)

                """
                .................Orientation Calculation..........................
                """
                # angle = self.clock_col.columns[index_val]
                # # angle = defect_angle_x(roll4, max_value_difference_index)
                # print("angle", angle)

                avg_counter = round((start_index_c + end_index_c)/2)
                avg_sensor = round((y_start15+y_end15)/2)
                angle = self.map_ori_sens_ind.iloc[avg_counter, avg_sensor]
                # k2 = self.map_ori_sens_ind.iloc[avg_counter, avg_sensor]
                # angle = k2[2]
                print("angle", angle)

                """
                Calculate length_percent of the defect
                """
                counter_difference = end_index_c - start_index_c
                # print("counter_difference", counter_difference)
                divid = int(counter_difference/2)
                center = start_index_c+divid

                factor1 = divid * self.config.l_per_1
                start1 = int(center - factor1)
                end1 = int(center + factor1)
                l_per1 = (self.oddo1_li_chm[end1] - self.oddo1_li_chm[start1])

                factor2 = divid * self.config.l_per_2
                start2 = int(center - factor2)
                end2 = int(center + factor2)
                l_per2 = (self.oddo1_li_chm[end2] - self.oddo1_li_chm[start2])

                factor3 = divid * self.config.l_per_3
                start3 = int(center - factor3)
                end3 = int(center + factor3)
                l_per3 = (self.oddo1_li_chm[end3] - self.oddo1_li_chm[start3])

                factor4 = divid * self.config.l_per_4
                start4 = int(center - factor4)
                end4 = int(center + factor4)
                l_per4 = (self.oddo1_li_chm[end4] - self.oddo1_li_chm[start4])

                # print("start_percent", start_percent)
                # print("end_percent", end_percent)
                # print("length_percent=>", length_percent)

                defect_start_oddo = self.oddo1_li_chm[start_index_c]
                defect_end_oddo = self.oddo1_li_chm[end_index_c]/1000

                print("defect_start_oddo", defect_start_oddo)
                print("defect_end_oddo", defect_end_oddo)

                time_sec = end_index15/1500

                speed = defect_end_oddo/time_sec
                print("speed(m/s)", speed)

                """
                Calculate defect_type of the defect
                """
                internal_external = internal_or_external(self.df_new_proximity_chmd, max_value_difference_index)
                print("internal_external", internal_external)

                """
                Calculate dimension_classification of the defect
                """
                dimension_classification = get_type_defect_1(self.config.pipe_thickness, runid, length_of_defect_oddo1, Width)
                print("dimension_classification", dimension_classification)

                finial_defect_list.append({"runid": runid, "start_reading": start_index_c, "end_reading": end_index_c,
                                 "start_sensor": y_start15,
                                 "end_sensor": y_end15,
                                 "absolute_distance": Abs_Distance, "upstream_oddo1": upstream_oddo1,
                                 "length": length_of_defect_oddo1, "breadth": Width, "width_new": width_new, 'orientation': angle,
                                 "dimension_classification": dimension_classification, "defect_type": internal_external,
                                 "depth": depth_old, "WT":wt,
                                 "max_value": max_value, "base_value": base_value, "min_value": min_positive,
                                 "l_per1": l_per1,
                                 # "l_per2": l_per2,"l_per3": l_per3,"l_per4": l_per4,
                                 "speed": speed, "latitude":lat,"longitude":long
                                 })

                for i in finial_defect_list:
                    runid = i['runid']
                    start_index = i['start_reading']
                    end_index = i['end_reading']
                    start_sensor = i['start_sensor']
                    end_sensor = i['end_sensor']
                    absolute_distance = round(i['absolute_distance'], 3)
                    upstream_oddo1 = round(i['upstream_oddo1'], 3)
                    length = round(i['length'])
                    Width = round(i['breadth'])
                    width_new = round(i['width_new'])
                    depth = round(i['depth'])
                    orientation = i['orientation']
                    dimension_classification = i['dimension_classification']
                    defect_type = i['defect_type']
                    max_value = round(i['max_value'])
                    base_value = round(i['base_value'])
                    min_value = round(i['min_value'])
                    l_per1 = round(i['l_per1'])
                    # l_per2 = round(i['l_per2'])
                    # l_per3 = round(i['l_per3'])
                    # l_per4 = round(i['l_per4'])
                    WT = i['WT']
                    speed = round(i['speed'], 2)
                    latitude = i['latitude']
                    longitude = i['longitude']
                    with self.config.connection.cursor() as cursor:
                        query_defect_insert = "INSERT into defect_clock_hm(runid, pipe_id, pipe_length, start_index, end_index, start_sensor, end_sensor, upstream, absolute_distance, orientation, length, Width, width_final, depth_new,max_value, min_value, l_per1, dimension_classification,defect_type, mean_value, `WT(mm)`, speed, latitude, longitude) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

                        cursor.execute(query_defect_insert, (
                            int(runid), self.Weld_id_tab9, self.pipe_len_oddo1_chm, start_index, end_index,
                            start_sensor, end_sensor, upstream_oddo1, absolute_distance, orientation,
                             length, Width, width_new, depth, max_value, min_value, l_per1, dimension_classification,
                            defect_type,base_value,  WT, speed, latitude, longitude))

                    self.config.connection.commit()
                    QMessageBox.information(self, 'Success', 'Data saved')

                    with self.config.connection.cursor() as cursor:
                        Fetch_weld_detail = "select id,pipe_id,`WT(mm)`,absolute_distance,upstream,defect_type,dimension_classification,orientation,length,width_final,depth_new from defect_clock_hm where runid='%s' and pipe_id='%s'"
                        # Execute query.
                        cursor.execute(Fetch_weld_detail, (int(self.runid), int(self.Weld_id_tab9)))
                        self.myTableWidget_tab9.setRowCount(0)
                        allSQLRows = cursor.fetchall()
                        if allSQLRows:
                            for row_number, row_data in enumerate(allSQLRows):
                                self.myTableWidget_tab9.insertRow(row_number)
                                for column_num, data in enumerate(row_data):
                                    self.myTableWidget_tab9.setItem(row_number, column_num,
                                                                QtWidgets.QTableWidgetItem(str(data)))
                                    self.myTableWidget_tab9.setContextMenuPolicy(Qt.CustomContextMenu)
                                    self.myTableWidget_tab9.customContextMenuRequested.connect(lambda position: open_context_menu_ori_tab9(self, position))
                                    self.myTableWidget_tab9.doubleClicked.connect(lambda: handle_table_double_click_chm(self))

                break  # Exit the loop if a valid name is provided
            else:
                QMessageBox.warning(self, 'Invalid Input', 'Please enter a name.')
        else:
            print('Operation canceled.')
            break


def handle_table_double_click_chm(self):
    weld_id = self.Weld_id_tab9
    runid = self.parent.runid

    selected_row = self.myTableWidget_tab9.currentRow()
    if selected_row == -1:
        QMessageBox.warning(self, "No Selection", "Please double-click on a valid cell.")
        return

    defect_id = self.myTableWidget_tab9.item(selected_row, 0).text()
    try:
        with self.config.connection.cursor() as cursor:
            query_for_coordinates = "SELECT id, start_index, end_index, start_sensor, end_sensor, length, Width, depth_new from defect_clock_hm WHERE pipe_id = %s AND runid = %s AND id = %s"
            cursor.execute(query_for_coordinates, (weld_id, runid, defect_id))
            result = cursor.fetchone()
            print(f"Query Result: {result}")

            if not result:
                QMessageBox.warning(self, "No Data", "No data found for the selected defect.")
                return

            id, start_index, end_index, y_start_hm, y_end_hm, length_odd1, breadth, depth = result

            # Calculate rectangle coordinates
            rect_x = start_index - 0.5
            rect_y = y_start_hm - 0.5
            rect_width = (end_index - start_index) + 1  # Adjust for center alignment
            rect_height = (y_end_hm - y_start_hm) + 1.5  # Adjust for center alignment

            # Create and add the rectangle to the plot
            rect = plt.Rectangle(
                (rect_x, rect_y),  # Set bottom-left corner
                rect_width,  # Width
                rect_height,  # Height
                linewidth=1, edgecolor='black', facecolor='none'
            )
            ax = self.figure_tab9.gca()
            ax.add_patch(rect)

            # Add the text annotation
            text_x = start_index + (end_index - start_index)/2
            text_y = y_start_hm - 6  # Slightly above the box
            # text_y = rect_y + (y_end_hm - y_start_hm) * 0.1  # Slightly above the box
            ax.text(
                text_x, text_y,
                f"L: {length_odd1}\nW: {breadth}\nD: {depth}",
                color='white',
                ha='center', va='center',
                fontsize=9, weight='bold',
                path_effects=[
                    path_effects.withStroke(linewidth=2, foreground='black')  # Black outline
                ]
            )

            self.canvas_tab9.draw_idle()  # Ensure the canvas is updated.

    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to draw box: {str(e)}")


def save_as_img(self, heat_map_obj, company_name, Weld_id):
    """
    This will save the plotted chat as a image format
        :param heat_map_obj:object of seaborn heatmap
        :param company_name:company name used to create folder
        :param Weld_id:Image of graph will be saved as pipe Id
    """
    # print(heat_map_obj)
    print(company_name)
    print(Weld_id)
    # figure = heat_map_obj.
    print("here1")
    img_path = os.path.join(self.config.image_folder, company_name)
    img_name = f"{Weld_id}.html"
    os.makedirs(img_path, exist_ok=True)
    full_path = os.path.join(img_path, img_name)
    full_path = os.path.normpath(full_path)
    print(f"saving html at : {full_path}")
    heat_map_obj.write_html(full_path)
    print("here 2")



from PyQt5.QtCore import pyqtSlot

@pyqtSlot(object, object)
def run_line_select_callback_chm(self, eclick, erelease):
    """Safe bridge to call line_select_callback_chm() on GUI thread."""
    print("✅ [MainThread] Executing line_select_callback_chm")
    try:
        self.line_select_callback_chm(eclick, erelease)
    except Exception as e:
        print(f"❌ [MainThread Error] {e}")
