# frontend/tabs/tab_ShowData.py
from PyQt5 import QtWidgets
from .widgets.ShowWeld import ShowWeldSelection
from .widgets.WeldTable import WeldTable
from .widgets.create_weld import CreateWeldButton
from .widgets.weld_pipe_table import FetchWeldToPipe, FetchWeldToPipeButton
from .widgets.defect_pipe_table import FetchDefectList, FetchDefectListButton
from PyQt5.QtWidgets import QAbstractItemView


class TabShowData(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # main window
        self.config = self.parent.config
        self.pipetally = self.parent.pipetally
        print(f" insinde tab3 pipetally path: {self.pipetally}")

        self.setObjectName("tab_3")
        self.setStyleSheet("background-color: #EDF6FF;")

        layout = QtWidgets.QVBoxLayout(self)



        # --- Weld data table (now self-contained class) ---
        self.myTableWidget = WeldTable(self)
        self.myTableWidget.bind_double_click(self.viewClicked)
        layout.addWidget(self.myTableWidget)

        # --- Fetch Weld button ---
        self.ShowWeld = ShowWeldSelection(self)
        layout.addWidget(self.ShowWeld)

        # --- weld to pipe table ---
        self.myTableWidget1 = FetchWeldToPipe(self)
        layout.addWidget(self.myTableWidget1)

        # --- weld to pipe button ---
        self.Show_Weld_to_Pipe = FetchWeldToPipeButton(self)
        layout.addWidget(self.Show_Weld_to_Pipe)

        # --- defect table ---
        self.myTableWidget2 = FetchDefectList(self)
        layout.addWidget(self.myTableWidget2)

        # --- defect table button ---
        self.Show_Defect_list = FetchDefectListButton(self)
        layout.addWidget(self.Show_Defect_list)

        # --- create weld button ---
        self.CreateWeldSection = CreateWeldButton(self)
        layout.addWidget(self.CreateWeldSection)

        self.setLayout(layout)

    # --- Logic for fetching and populating weld data ---
    def Show_Weld(self):
        runid = self.parent.runid
        try:
            with self.config.connection.cursor() as cursor:
                query = (
                    "select weld_number,runid,analytic_id,sensitivity,length,"
                    "start_index,end_index,start_oddo1,end_oddo1,start_oddo2,end_oddo2 "
                    "from welds where runid=%s and id>%s"
                )
                cursor.execute(query, (int(runid), 1))
                rows = cursor.fetchall()

                table = self.myTableWidget
                table.setRowCount(0)

                if rows:
                    for r, row_data in enumerate(rows):
                        table.insertRow(r)
                        for c, data in enumerate(row_data):
                            table.setItem(r, c, QtWidgets.QTableWidgetItem(str(data)))
                else:
                    self.config.warning_msg("No record found", "")

                weld_ids = [str(i[0]) for i in rows]
                print("weld_id_list:", weld_ids)
                # Update Graph tab weld dropdown
                if self.parent.Graph1 is not None:
                    try:
                        self.parent.Graph1.combo_graph.clear()
                        self.parent.Graph1.combo_graph.addItems(weld_ids)
                    except Exception as e:
                        print("GraphTab weld update failed:", e)

                # combos belong to main window
                self.parent.tab_line1.combo.addItems(weld_ids)
                self.parent.tab_line_orientation.combo_orientation.addItems(weld_ids)
                self.parent.tab_visualize.combo_box.addItems(weld_ids)
                # self.parent.Graph1.combo_graph.addItems(weld_ids)
                # self.parent.combo_box1.addItems(weld_ids)
                self.parent.continue_heatmap_tab.combo_tab9.addItems(weld_ids)

                self.parent.weld_loaded = True
                self.parent.try_enable_advanced_tabs()
                self.try_enable_graph_tab()



        except Exception as e:
            print("Error in Show_Weld:", e)
            self.config.warning_msg("Error fetching weld data", str(e))

    def try_enable_graph_tab(self):
        if self.parent.weld_loaded and self.parent.pipe_loaded and self.parent.pipetally_loaded:
            self.parent.right_tabWidget.setTabEnabled(self.parent.graph_tab_index, True)
            print(f" heatmap_index : {self.parent.heatmap_tab_index}")
            self.parent.right_tabWidget.setTabEnabled(self.parent.heatmap_tab_index, True)
            print("Graph Tab and heatmap ENABLED")
        else:
            print("Graph nd heatmap waiting… weld:", self.parent.weld_loaded,
                  "pipe:", self.parent.pipe_loaded,
                  "pipetally:", self.parent.pipetally_loaded)

    def ShowWeldToPipe(self):
        """
        Populate the Weld→Pipe table for the selected run.
        """
        main = self.parent  # access main window
        runid = getattr(main, "runid", None)
        if runid is None:
            self.config.warning_msg("No RunID loaded", "")
            return

        try:
            with self.config.connection.cursor() as cursor:
                query = (
                    "SELECT id, runid, analytic_id, lower_sensitivity, "
                    "upper_sensitivity, length, start_index, end_index "
                    "FROM pipes WHERE runid = %s"
                )
                cursor.execute(query, (int(runid),))
                rows = cursor.fetchall()

                table = self.myTableWidget1
                table.setRowCount(0)

                if rows:
                    for r, row_data in enumerate(rows):
                        table.insertRow(r)
                        for c, data in enumerate(row_data):
                            table.setItem(r, c, QtWidgets.QTableWidgetItem(str(data)))
                    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                else:
                    self.config.warning_msg("No record found", "")

                pipe_ids = [str(i[0]) for i in rows]
                print("pipe_id_list:", pipe_ids)
                # Update Graph tab pipe dropdown (only if GraphTab has such combo)
                if self.parent.Graph1 is not None and hasattr(self.parent.Graph1, "combo_pipe"):
                    try:
                        self.parent.Graph1.combo_pipe.clear()
                        self.parent.Graph1.combo_pipe.addItems(pipe_ids)
                    except Exception as e:
                        print("GraphTab pipe update failed:", e)

                self.parent.pipe_loaded = True
                self.parent.try_enable_advanced_tabs()
                self.try_enable_graph_tab()



        except Exception as e:
            print("Error in ShowWeldToPipe:", e)
            self.config.warning_msg("Error fetching weld-to-pipe data", str(e))

    def DefectList(self):
        """
        Fetch and populate defect list table for the selected run ID.
        """
        main = self.parent  # main window reference
        runid = getattr(main, "runid", None)
        if runid is None:
            self.config.warning_msg("No RunID loaded", "")
            return

        try:
            with self.config.connection.cursor() as cursor:
                query = (
                    "SELECT id, runid, start_observation, end_observation, "
                    "start_sensor, end_sensor, angle, length, breadth, depth, type "
                    "FROM defect_sensor_hm WHERE runid = %s"
                )
                cursor.execute(query, (int(runid),))
                rows = cursor.fetchall()

                table = self.myTableWidget2  # your FetchDefectList instance
                table.setRowCount(0)

                if rows:
                    for row_number, row_data in enumerate(rows):
                        table.insertRow(row_number)
                        for column_num, data in enumerate(row_data):
                            table.setItem(row_number, column_num, QtWidgets.QTableWidgetItem(str(data)))
                    table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                else:
                    self.config.warning_msg("No record found", "")

                print(f"[DEBUG] Fetched {len(rows)} defect records for runid {runid}")

        except Exception as e:
            print("Error in DefectList:", e)
            self.config.warning_msg("Error fetching defect list", str(e))


    def viewClicked(self):
        list = []
        list.clear()
        for i in range(0, 8):
            list.append(self.myTableWidget.item(self.myTableWidget.currentRow(), i).text())
        self.analytic_id = list[1]


