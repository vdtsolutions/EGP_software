import os
import pandas as pd
from egp_soft_based_on_mfl.Components.Configs import config_universal
from egp_soft_based_on_mfl.utils.loaderdialog.loader_dialog import BaseWorker
from .helper_func import GenerateGraph, handle_table_double_click_pipe, open_context_menu



class PreGraphWorker(BaseWorker):

    def __init__(self, tab):
        super().__init__()
        self.tab = tab

    def run(self):

        tab = self.tab

        if self.isInterruptionRequested():
            return

        self.message.emit("Initializing weld analysis...")
        self.progress.emit(5)

        config_universal.print_with_time("Pre graph analysis called")

        runid = tab.parent.runid
        Weld_id = tab.combo_box.currentText()

        tab.Weld_id = int(Weld_id)
        tab.lower_sensitivity = tab.lower_Sensitivity_combo_box.currentText()
        tab.upper_sensitivity = tab.upper_Sensitivity_combo_box.currentText()

        self.message.emit("Reading weld information...")
        self.progress.emit(10)

        with tab.config.connection.cursor() as cursor:

            query = """
            SELECT start_index, end_index,start_oddo1,end_oddo1
            FROM welds
            WHERE runid=%s
            AND id IN (%s,(SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s))
            ORDER BY id
            """

            cursor.execute(query, (runid, tab.Weld_id, runid, tab.Weld_id))
            result = cursor.fetchall()

        if not result:
            config_universal.print_with_time("No data found for this pipe ID")
            self.finished.emit(None)
            return

        start_oddo1 = result[0][2]
        end_oddo1 = result[1][3]

        tab.pipe_len_8 = end_oddo1 - start_oddo1

        self.message.emit("Checking cached weld data...")
        self.progress.emit(25)

        path = (
            config_universal.weld_pipe_pkl
            + tab.parent.project_name
            + "/"
            + str(tab.Weld_id)
            + ".pkl"
        )

        if os.path.isfile(path):

            config_universal.print_with_time("File exist")

            df_new_8 = pd.read_pickle(path)

            tab.index_tab8 = df_new_8['index']
            tab.oddo1_tab8 = df_new_8['ODDO1']

            tab.df_new_tab8 = pd.DataFrame(
                df_new_8,
                columns=[
                    f'F{i}H{j}'
                    for i in range(1, tab.config.F_columns + 1)
                    for j in range(1, 5)
                ]
            )

        else:

            self.message.emit("Fetching sensor data from cloud...")
            self.progress.emit(45)

            folder_path = config_universal.weld_pipe_pkl + tab.parent.project_name

            os.makedirs(folder_path, exist_ok=True)

            start_index, end_index = result[0][0], result[1][1]

            query_for_start = (
                "SELECT index,ROLL, ODDO1, ODDO2,["
                + tab.config.sensor_str_hall +
                "] FROM "
                + tab.config.table_name +
                " WHERE index>={} AND index<={} ORDER BY index"
            )

            query_job = tab.config.client.query(
                query_for_start.format(start_index, end_index)
            )

            results = query_job.result()

            data = []
            tab.index_tab8 = []
            oddo_1 = []
            oddo_2 = []
            roll1 = []

            for row in results:

                tab.index_tab8.append(row[0])
                roll1.append(row[1])
                oddo_1.append(row[2])
                oddo_2.append(row[3])
                data.append(row[4])

            self.message.emit("Processing hall sensors...")
            self.progress.emit(60)

            tab.oddo1_tab8 = []
            tab.oddo2_tab8 = []
            tab.roll_t8 = []

            for odometer1 in oddo_1:
                tab.oddo1_tab8.append(odometer1 - tab.config.oddo1)

            for odometer2 in oddo_2:
                tab.oddo2_tab8.append(odometer2 - tab.config.oddo2)

            for roll2 in roll1:
                tab.roll_t8.append(roll2 - tab.config.roll_value)

            self.message.emit("Processing proximity sensors...")
            self.progress.emit(70)

            query_for_start = (
                "SELECT index,["
                + tab.config.sensor_str_prox +
                "] FROM "
                + tab.config.table_name +
                " WHERE index>={} AND index<={} ORDER BY index"
            )

            query_job = tab.config.client.query(
                query_for_start.format(start_index, end_index)
            )

            results_1 = query_job.result()

            data1 = []
            tab.index_hm_ori = []

            for row1 in results_1:

                tab.index_hm_ori.append(row1[0])
                data1.append(row1[1])

            tab.df_new_proximity_ori = pd.DataFrame(
                data1,
                columns=tab.config.sensor_columns_prox
            )

            tab.df_new_tab8 = pd.DataFrame(
                data,
                columns=[
                    f'F{i}H{j}'
                    for i in range(1, tab.config.F_columns + 1)
                    for j in range(1, 5)
                ]
            )

            self.message.emit("Preparing weld dataset...")
            self.progress.emit(80)

            df_elem = pd.DataFrame({
                "index": tab.index_tab8,
                "ODDO1": tab.oddo1_tab8
            })

            df_new = pd.concat([df_elem, tab.df_new_tab8], axis=1, join='inner')

            for col in tab.df_new_proximity_ori.columns:
                df_new[col] = tab.df_new_proximity_ori[col]

            df_new.reset_index(inplace=True)

            df_new.to_pickle(folder_path + '/' + str(tab.Weld_id) + '.pkl')

            config_universal.print_with_time("Successfully saved to pickle file")

        if self.isInterruptionRequested():
            return

        self.message.emit("Generating weld graph...")
        self.progress.emit(90)

        config_universal.print_with_time("starting generating graph")

        GenerateGraph(tab)

        config_universal.print_with_time("ending generating graph")

        if self.isInterruptionRequested():
            return

        self.message.emit("Loading defect data...")
        self.progress.emit(95)

        with tab.config.connection.cursor() as cursor:

            Fetch_weld_detail = """
            select id,pipe_id,absolute_distance,upstream,defect_type,
            dimension_classification,orientation,length,width_final,depth_new
            from dent_clock_hm
            where runid=%s and pipe_id=%s
            """

            cursor.execute(Fetch_weld_detail, (int(runid), int(tab.Weld_id)))

            defects = cursor.fetchall()

        self.progress.emit(100)
        self.message.emit("Completed")

        self.finished.emit(defects)