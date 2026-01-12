from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns
from matplotlib.widgets import RectangleSelector
import math
import plotly.graph_objs as go
from kaleido.scopes import plotly
from PyQt5.QtCore import Qt, QUrl
from pathlib import Path
import plotly.offline
import pymysql

from .utils.worker_defect import init_defect_worker, apply_defect_result, compute_defect_data_multicore
from ..helper_func import line_select_callback_chm, open_context_menu_ori_tab9, handle_table_double_click_chm, \
    save_as_img
import numpy as np
from google.cloud import bigquery


from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.utils.utils import create_folders, \
    fetch_and_save_tab9_data, process_weld_data_to_create_data_array_for_clustering, save_clock_pkl, process_defects, \
    process_single_defect, compute_defect_data, compute_defect_data_multicore1
from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.pipelines.clustering_filter_pipeline import find_defect_regions_using_clustering
from .pipelines.calculate_base_threshold import calculate_defect_threshold
from .pipelines.length_calculation_pipeline import calculate_length_percent
from .pipelines.width_calculation_pipeline import breadth, process_submatrix, ML_width_calc
from .pipelines.interpolate_data import process_csv_interpolate
from .pipelines.depth_calculation_pipeline import compute_depth
from .pipelines.dimension_classification import dimension_class
from .utils.utils import get_first_last_integer_column, replace_first_column, defect_summary
from .utils.data_manager import manage_directory, save_submatrices
from .pipelines.orientation_pipeline import get_orientation
from .utils.database_insertion import insert_defects_to_db_defect_clock_hm
from .pipelines.internal_or_external import internal_or_external



GMFL_ROOT = Path(__file__).resolve().parents[4]


def gmfl_path(relative):
    """Return absolute path inside GMFL backend_data/temp folder."""
    temp_dir = GMFL_ROOT / "backend_data" / "data_generated" / "temp"
    os.makedirs(temp_dir, exist_ok=True)  # make sure folder exists
    return str(temp_dir / relative)


def process_batch(batch_rows):
    """
    Runs compute_defect_data_multicore on a batch of row-tuples.
    Uses global shared variables from init_defect_worker().
    """
    out = []
    for row_tuple in batch_rows:
        try:
            res = compute_defect_data_multicore(row_tuple)
            out.append(res)
        except Exception as e:
            out.append({"accepted": False, "error": str(e)})
    return out

def chunk_list(data, n):
    """Split list into n chunks as evenly as possible."""
    if n <= 0:
        return [data]
    k, m = divmod(len(data), n)
    return [
        data[i*k + min(i, m):(i+1)*k + min(i+1, m)]
        for i in range(n)
    ]


# def tab9_heatmap(self):
#     credentials = self.config.credentials
#     project_id = self.config.project_id
#     client = bigquery.Client(credentials=credentials, project=project_id)
#     self.config.print_with_time("Pre graph analysis called")
#     runid = self.parent.runid
#     self.runid = self.parent.runid
#     Weld_id_tab9 = self.combo_tab9.currentText()
#     self.Weld_id_tab9 = int(Weld_id_tab9)
#     wall_thickness = self.config.pipe_thickness
#     pipe_id = self.Weld_id_tab9
#     with self.config.connection.cursor() as cursor:
#         # query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
#         query = "SELECT start_index, end_index,start_oddo1,end_oddo1 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"
#         cursor.execute(query, (self.runid, self.Weld_id_tab9, self.runid, self.Weld_id_tab9))
#         result = cursor.fetchall()
#         start_oddo1 = result[0][2]
#         end_oddo1 = result[1][3]
#         self.pipe_len_oddo1_chm = round(end_oddo1 - start_oddo1, 2)
#         pipe_len_oddo1_chm = self.pipe_len_oddo1_chm
#
#         if not result:
#             self.config.print_with_time("No data found for this pipe ID : ")
#         else:
#             """
#             pkl file is found in local path
#             """
#             path = self.config.clock_pkl + self.parent.project_name + '/' + str(self.Weld_id_tab9) + '.pkl'
#
#             if os.path.isfile(path):
#                 self.config.print_with_time("File exist")
#                 df_clock_holl = pd.read_pickle(path)
#                 [f"{h:02}:{int(m):02}" for h in range(12) for m in np.arange(0, 60, self.config.minute)]
#                 # val_ori_sensVal = df_clock_holl[[f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]]
#                 val_ori_sensVal = df_clock_holl[[f"{h:02}:{int(m):02}" for h in range(12) for m in np.arange(0, 60, self.config.minute)]]
#                 # self.map_ori_sens_ind = df_clock_holl[[f"{h:02}:{m:02}_x" for h in range(12) for m in range(0, 60, 5)]]
#                 self.map_ori_sens_ind = df_clock_holl[[f"{h:02}:{int(m):02}_x" for h in range(12) for m in np.arange(0, 60, self.config.minute)]]
#                 self.map_ori_sens_ind.columns = self.map_ori_sens_ind.columns.str.rstrip('_x')
#                 self.clock_col = val_ori_sensVal
#                 self.clock_data_col = val_ori_sensVal.values.tolist()
#                 self.mean_clock_data = val_ori_sensVal.mean().tolist()
#
#                 df3 = ((val_ori_sensVal - self.mean_clock_data) / self.mean_clock_data) * 100
#
#                 self.figure_tab9.clear()  # Clear the previous figure
#                 ax2 = self.figure_tab9.add_subplot(111)
#                 ax2.figure.subplots_adjust(bottom=0.151, left=0.060, top=0.820, right=1.000)
#                 d1 = df3.transpose().astype(float)
#                 #
#                 heat_map_obj = sns.heatmap(
#                     d1,
#                     cmap='jet',
#                     ax=ax2,
#                     vmin=-5, vmax=18,
#                     square=False,
#                     cbar_kws={'shrink': 0.8, 'pad': 0.005}
#                 )
#                 #
#                 # # Optional manual nudge
#                 cbar = heat_map_obj.collections[0].colorbar
#                 cbar.ax.set_position([0.955, 0.12, 0.02, 0.76])
#                 #
#                 # heat_map_obj.set(xlabel="Index", ylabel="Clock")
#
#                 """
#                 Pipewise ranges have been set
#                 """
#
#                 heat_map_obj.set(xlabel="Index", ylabel="Clock")
#
#                 self.oddo1_li_chm = df_clock_holl['ODDO1'].tolist()
#                 index_hm = list(df_clock_holl['index'])
#                 self.index_chm = index_hm
#                 # print("index_chm", self.index_chm)
#
#                 ax2.set_xticklabels(ax2.get_xticklabels(), size=9)
#                 ax2.set_yticklabels(ax2.get_yticklabels(), size=9)
#                 ax3 = ax2.twiny()
#                 oddo_val = [round(elem / 1000, 2) for elem in self.oddo1_li_chm]
#                 num_ticks1 = len(ax2.get_xticks())  # Adjust the number of ticks based on your preference
#                 # print(num_ticks1)
#                 tick_positions1 = [int(i) for i in np.linspace(0, len(oddo_val) - 1, num_ticks1)]
#                 # print(tick_positions1)
#                 ax3.set_xticks(tick_positions1)
#                 ax3.set_xticklabels([f'{oddo_val[i]:.2f}' for i in tick_positions1], rotation=90, size=9)
#                 ax3.set_xlabel("Absolute Distance (m)", size=9)
#
#                 def on_hover(event):
#                     if event.xdata is not None and event.ydata is not None:
#                         try:
#                             x = int(event.xdata)
#                             y = int(event.ydata)
#                             index_value = index_hm[x]
#                             clock_val = list(val_ori_sensVal.columns)[y]  ### It shows clock_column values ###
#                             clock = self.map_ori_sens_ind.transpose().iloc[
#                                 y, x]  ### It shows real time values, like clock values at particular point ###
#                             value = d1.iloc[y, x]
#                             z = self.oddo1_li_chm[x]
#                             self.canvas_tab9.toolbar.set_message(
#                                 f'Index={index_value:.0f},Abs.distance(m)={z / 1000:.3f},Clock={clock_val},'
#                                 f'Value={value:.1f}')
#                         except (IndexError, ValueError):
#                             # Print a user-friendly message instead of showing an error
#                             print("Hovering outside valid data range. No data available.")
#
#                 self.figure_tab9.canvas.mpl_connect('motion_notify_event', on_hover)
#
#                 self.canvas_tab9.draw()  # Update the canvas with the new plot
#                 rs = RectangleSelector(self.figure_tab9.gca(), lambda eclick, erelease: line_select_callback_chm(self, eclick, erelease), useblit=True)
#                 plt.connect('key_press_event', rs)
#                 self.config.print_with_time("Plotted...")
#
#                 # Show canvas, hide web engine
#                 self.canvas_tab9.setVisible(True)
#                 self.reset_btn_tab9.setVisible(True)
#                 self.all_box_selection1.setVisible(True)
#                 self.m_output.setVisible(False)
#
#             else:
#                 """
#                 pkl file is not found than data fetch from GCP and save pkl file in local path
#                 """
#                 # folder_path = self.config.clock_pkl + self.project_name
#                 folder_path1 = self.config.weld_pipe_pkl + self.parent.project_name
#                 folder_path = self.config.clock_pkl + self.parent.project_name
#                 Wall_thickness = self.config.pipe_thickness
#                 # print(folder_path)
#                 self.config.print_with_time("File not exist")
#
#                 #create folder if doesnt exist
#                 create_folders(self, folder_path, folder_path1)
#
#                 start_index, end_index = result[0][0], result[1][1]
#                 print(self.Weld_id_tab9)
#                 print(start_index, end_index)
#                 self.start_pipe_tab9, self.end_pipe_tab9 = start_index, end_index
#
#                 #fetch and save data from gcp
#                 out = fetch_and_save_tab9_data(self, client, start_index, end_index, folder_path1, self.Weld_id_tab9)
#                 df_elem = out["df_elem"]
#                 df_new_proximity_orientat = out["df_new_proximity_orientat"]
#
#
#                 # Process data_array which gives inputs for finding defect region using clustering and heatmap data and
#                 #name of function needs to be adjusted
#
#                 processed_data_array = process_weld_data_to_create_data_array_for_clustering(self, folder_path1, self.Weld_id_tab9)
#
#
#                 #value extraction from the processed_data_array pipeline
#                 visited = set()
#                 bounding_boxes = []
#                 data_array = processed_data_array["data_array"]
#                 oddometer1 = processed_data_array["oddometer1"]
#                 data_x = processed_data_array["data_x"]
#                 t_raw = processed_data_array["t_raw"]
#                 mean1 = processed_data_array["mean1"]
#                 standard_deviation = processed_data_array["standard_deviation"]
#                 df_new_proximity = processed_data_array["df_new_proximity"]
#                 Roll_hr = processed_data_array["Roll_hr"]
#                 df3_raw = processed_data_array["df3_raw"]
#                 t = processed_data_array["t"]
#                 result = processed_data_array["result"]
#                 result_raw_df = processed_data_array["result_raw_df"]
#
#                 save_clock_pkl(self, df_elem, result_raw_df, Roll_hr, folder_path, df_new_proximity_orientat)
#
#                 self.config.print_with_time("Performing clustering to detect defect regions...start at : ")
#                 # find defect region using clustering_filter_pipeline from utils to get start, end ( column , sensor)
#                 df_sorted = find_defect_regions_using_clustering(data_array)
#                 self.config.print_with_time("Performing clustering to detect defect regions...end at : ")
#
#
#                 df_clock_holl_oddo1 = data_x['ODDO1']
#                 oddo1_li = list(oddometer1)
#                 sensor_numbers = list(range(1, len(t.index) + 1))  # 1 to 144
#                 sensor_numbers = sensor_numbers[::-1]  # Reverse the list to go top=0 → bottom=144
#                 # Create a 2D text matrix where each row has the same sensor number
#                 text = np.array([[f"{sensor_no}"] * t.shape[1] for sensor_no in sensor_numbers])
#                 figx112 = go.Figure(data=go.Heatmap(
#                     z=t_raw,
#                     y=t.index,
#                     x=[t.columns, oddo1_li],
#                     text=text,
#                     hovertemplate='Oddo: %{x}<br>Clock:%{y}<br>Value: %{z}, sensor no: %{text}',
#                     zmin=-5,
#                     zmax=18,
#                     colorscale='jet',
#                 ))
#                 figx112.update_yaxes(autorange='reversed')
#
#                 self.config.print_with_time("calculate defect threshold start at : ")
#                 #threshold values calculation
#                 threshold_value, max_of_all = calculate_defect_threshold(df_sorted=df_sorted, result=result,
#                                                                          defect_box_thresh=self.config.defect_box_thresh)
#                 self.config.print_with_time("calculate defect threshold end at : ")
#
#
#                 print("Processing defects with 3-part length classification...")
#
#                 # PROCESS DEFECTS WITH ADAPTIVE REFINEMENT
#                 finial_defect_list = []
#                 defect_counter = 1
#                 submatrices_dict = {}
#                 classification_stats = {
#                     "Very Small (1-10%)": {"count": 0, "total_processed": 0},
#                     "Small (10-20%)": {"count": 0, "total_processed": 0},
#                     "Medium (20-30%)": {"count": 0, "total_processed": 0},
#                     "Large (30-40%)": {"count": 0, "total_processed": 0},
#                     "Very Large (40%+)": {"count": 0, "total_processed": 0},
#                     "Below 1%": {"count": 0, "total_processed": 0}
#                 }
#
#                 self.config.print_with_time("------ start of iteration ------")
#                 result = result.apply(pd.to_numeric, errors='coerce')
#                 config = {
#                     # core numeric config
#                     "l_per_1": self.config.l_per_1,
#                     "w_per_1": self.config.w_per_1,
#                     "pipe_thickness": self.config.pipe_thickness,
#                     "outer_dia": self.config.outer_dia,
#                     "theta_ang1": self.config.theta_ang1,
#                     "theta_ang2": self.config.theta_ang2,
#                     "theta_ang3": self.config.theta_ang3,
#                     "scaling_exponent": self.config.scaling_exponent,
#                     # pipeline-level data
#                     "pipe_len_oddo1_chm": self.pipe_len_oddo1_chm,
#                     "calibration_factor": self.config.calibration_factor,
#                     "min_energy_threshold": self.config.min_energy_threshold,
#                     "positive_sigma_row": self.config.positive_sigma_row,
#                     "div_factor": self.config.div_factor,
#
#                     # IMPORTANT: This is a FUNCTION and it IS picklable
#                     "get_adaptive_sigma_refinement": self.config.get_adaptive_sigma_refinement,
#                 }
#
#
#                 defect_counter = 1
#                 total_iters = 0
#                 total_rows = len(df_sorted)
#                 print(f"column names in df_sorted: {list(df_sorted.columns)}")
#
#                 # for row in df_sorted.itertuples(index=False):
#                 #
#                 #     total_iters += 1
#                 #
#                 #
#                 #     result_item = process_single_defect(
#                 #         self,config, result, df_clock_holl_oddo1, threshold_value,
#                 #         classification_stats, defect_counter,
#                 #         max_of_all, df3_raw, mean1, df_new_proximity, Roll_hr, t,
#                 #         submatrices_dict, finial_defect_list,
#                 #         pipe_id, runid, wall_thickness, figx112, row
#                 #     )
#                 #
#                 #     # If function returns None → skip
#                 #     if result_item is None:
#                 #         continue
#                 #
#                 #     # If defect was accepted → increment the counter
#                 #     if result_item is True:
#                 #         defect_counter += 1
#
#
#
#                 # print(f"total_rows in df_sorted before defect calculation loop: {total_rows}")
#                 config = {
#                     # core numeric config
#                     "l_per_1": self.config.l_per_1,
#                     "w_per_1": self.config.w_per_1,
#                     "pipe_thickness": self.config.pipe_thickness,
#                     "outer_dia": self.config.outer_dia,
#                     "theta_ang1": self.config.theta_ang1,
#                     "theta_ang2": self.config.theta_ang2,
#                     "theta_ang3": self.config.theta_ang3,
#                     "scaling_exponent": self.config.scaling_exponent,
#                     # pipeline-level data
#                     "pipe_len_oddo1_chm": self.pipe_len_oddo1_chm,
#                     "calibration_factor": self.config.calibration_factor,
#                     "min_energy_threshold": self.config.min_energy_threshold,
#                     "positive_sigma_row": self.config.positive_sigma_row,
#                     "div_factor": self.config.div_factor,
#
#                     # IMPORTANT: This is a FUNCTION and it IS picklable
#                     "get_adaptive_sigma_refinement": self.config.get_adaptive_sigma_refinement,
#                 }
#
#                 self.config.print_with_time("starting defect loop : ")
#                 for row in df_sorted.itertuples(index=False):
#
#                     total_iters += 1
#
#                     self.config.print_with_time(f" current id -- {total_iters} started at : ")
#                     res = compute_defect_data(
#                         config, result, df_clock_holl_oddo1, threshold_value,
#                         max_of_all, df3_raw, mean1,
#                         df_new_proximity, Roll_hr, t,
#                         pipe_id, runid, wall_thickness,
#                         row, pipe_len_oddo1_chm
#                     )
#                     self.config.print_with_time(f" current id -- {total_iters} ending at : ")
#
#                     defect_counter = apply_defect_result(
#                         self,
#                         res,
#                         classification_stats,
#                         defect_counter,
#                         submatrices_dict,
#                         finial_defect_list,
#                         figx112
#                     )
#
#                 self.config.print_with_time("ending defect loop : ")
#
#
#
#                 # #-------------------with cores only--------------------------------
#                 # config = {
#                 #     # core numeric config
#                 #     "l_per_1": self.config.l_per_1,
#                 #     "w_per_1": self.config.w_per_1,
#                 #     "pipe_thickness": self.config.pipe_thickness,
#                 #     "outer_dia": self.config.outer_dia,
#                 #     "theta_ang1": self.config.theta_ang1,
#                 #     "theta_ang2": self.config.theta_ang2,
#                 #     "theta_ang3": self.config.theta_ang3,
#                 #     "scaling_exponent": self.config.scaling_exponent,
#                 #     # pipeline-level data
#                 #     "pipe_len_oddo1_chm": self.pipe_len_oddo1_chm,
#                 #     "calibration_factor": self.config.calibration_factor,
#                 #     "min_energy_threshold": self.config.min_energy_threshold,
#                 #     "positive_sigma_row": self.config.positive_sigma_row,
#                 #     "div_factor": self.config.div_factor,
#                 #     "get_adaptive_sigma_refinement": self.config.get_adaptive_sigma_refinement,
#                 # }
#                 #
#                 # # ────────────────────────────────
#                 # # Manual CPU workers (you choose)
#                 # # ────────────────────────────────
#                 # threshold_workers = 7  # <--- set number of cores to use
#                 # length_index = len(t.index)
#                 #
#                 # # ---- Build small lightweight task list ----
#                 # tasks = [
#                 #     (row.start_row, row.end_row, row.start_col, row.end_col)
#                 #     for row in df_sorted.itertuples(index=False)
#                 # ]
#                 #
#                 # print(f"Total defects to process: {len(tasks)}")
#                 # from multiprocessing import Pool
#                 # # ---- Run multiprocessing with global-shared data ----
#                 # self.config.print_with_time("starting pool")
#                 # with Pool(
#                 #         processes=threshold_workers,
#                 #         initializer=init_defect_worker,
#                 #         initargs=(
#                 #                 config,
#                 #                 result,
#                 #                 df_clock_holl_oddo1,
#                 #                 threshold_value,
#                 #                 max_of_all,
#                 #                 df3_raw,
#                 #                 mean1,
#                 #                 df_new_proximity,
#                 #                 Roll_hr,
#                 #                 pipe_id,
#                 #                 runid,
#                 #                 wall_thickness,
#                 #                 pipe_len_oddo1_chm,
#                 #                 length_index,
#                 #         ),
#                 # ) as pool:
#                 #
#                 #     results = pool.map(compute_defect_data_multicore, tasks)
#                 #
#                 # self.config.print_with_time("pool completed")
#                 #
#                 # # ---- Post-processing ----
#                 # accepted_count = sum(1 for r in results if r.get("accepted"))
#                 # print("Accepted defects returned by workers:", accepted_count)
#                 #
#                 # # ────────────────────────────────
#                 # # Apply results (ORDER PRESERVED)
#                 # # ────────────────────────────────
#                 # defect_counter = 1
#                 # self.config.print_with_time("starting result adding ")
#                 # for res in results:
#                 #     defect_counter = apply_defect_result(
#                 #         self,
#                 #         res,
#                 #         classification_stats,
#                 #         defect_counter,
#                 #         submatrices_dict,
#                 #         finial_defect_list,
#                 #         figx112
#                 #     )
#                 # self.config.print_with_time("ending result adding ")
#
#
#                 #------------------WITH CORE AND BATCHES---------------------------------------
#                 # tasks = [
#                 #     (row.start_row, row.end_row, row.start_col, row.end_col)
#                 #     for row in df_sorted.itertuples(index=False)
#                 # ]
#                 #
#                 # total_defects = len(tasks)
#                 # print(f"Total defects to process: {total_defects}")
#                 #
#                 # # --------------------------------------------
#                 # # BATCHING FOR REAL SPEEDUP
#                 # # --------------------------------------------
#                 # num_workers = threshold_workers
#                 # batches = chunk_list(tasks, num_workers)
#                 #
#                 # self.config.print_with_time(
#                 #     f"Starting pool with {num_workers} workers, {total_defects} defects, {len(batches)} batches")
#                 #
#                 # from multiprocessing import Pool
#                 #
#                 # with Pool(
#                 #         processes=num_workers,
#                 #         initializer=init_defect_worker,
#                 #         initargs=(
#                 #                 config,
#                 #                 result,
#                 #                 df_clock_holl_oddo1,
#                 #                 threshold_value,
#                 #                 max_of_all,
#                 #                 df3_raw,
#                 #                 mean1,
#                 #                 df_new_proximity,
#                 #                 Roll_hr,
#                 #                 pipe_id,
#                 #                 runid,
#                 #                 wall_thickness,
#                 #                 pipe_len_oddo1_chm,
#                 #                 length_index,
#                 #         ),
#                 # ) as pool:
#                 #
#                 #     # Map batches to workers
#                 #     batch_results = pool.map(process_batch, batches)
#                 #
#                 # self.config.print_with_time("Pool completed")
#                 #
#                 # # --------------------------------------------
#                 # # FLATTEN BATCH RESULTS BACK TO SINGLE LIST
#                 # # --------------------------------------------
#                 # results = [res for batch in batch_results for res in batch]
#                 #
#                 # # --------------------------------------------
#                 # # POST-PROCESSING SAME AS BEFORE
#                 # # --------------------------------------------
#                 # accepted_count = sum(1 for r in results if r.get("accepted"))
#                 # print("Accepted defects returned by workers:", accepted_count)
#                 #
#                 # # Preserve order, apply results
#                 # defect_counter = 1
#                 # self.config.print_with_time("starting result adding")
#                 #
#                 # for res in results:
#                 #     defect_counter = apply_defect_result(
#                 #         self,
#                 #         res,
#                 #         classification_stats,
#                 #         defect_counter,
#                 #         submatrices_dict,
#                 #         finial_defect_list,
#                 #         figx112
#                 #     )
#                 #
#                 # self.config.print_with_time("ending result adding")
#
#                 print(f"total_rows in df_sorted after defect calculation loop: {total_rows}")
#                 # print(f"total iters in defect calculation loop = {total_iters}")
#
#
#                 self.config.print_with_time("------ end of iteration ------")
#
#
#
#                 print(f"\nTotal submatrices stored: {len(submatrices_dict)}")
#
#                 project_name = self.parent.project_name
#                 print(f"project name :  {project_name}")
#                 output_dir = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'submatrix_generated',
#                                           project_name) + '/'
#                 manage_directory(output_dir)
#                 save_submatrices(submatrices_dict, output_dir)
#                 print(f"\n=== DEFECT CLASSIFICATION SUMMARY ===")
#                 print(f"Total defects found: {len(finial_defect_list)}")
#                 defect_summary(finial_defect_list, classification_stats)
#
#                 # DATABASE INSERTION
#                 self.config.print_with_time("start of insertion in database")
#                 try:
#                     print("\nInserting defects into database...")
#                     # insert_defects_to_db_bb_new(self.config.connection, finial_defect_list, submatrices_dict)
#                     insert_defects_to_db_defect_clock_hm(self.config.connection, finial_defect_list, submatrices_dict)
#                 except Exception as e:
#                     print(f"error data: {e}")
#                 self.config.print_with_time("end of insertion in database")
#
#
#
#                 #width_final calculation
#                 self.config.print_with_time("starting ml width calc: ")
#                 ML_width_calc(self, output_dir, runid, pipe_id)
#                 self.config.print_with_time("ending ml width calc: ")
#                 print(
#                     f"\nProcessing complete! Found {len(finial_defect_list)} total defects using 3-part classification.")
#
#
#                 # FINAL VISUALIZATION
#                 self.config.print_with_time("Displaying visualization...")
#                 figx112.update_layout(
#                     # title='Heatmap with 3-Part Adaptive Length Classification (purple: 1-10%, Red : 10-20%, Orange: 20-30%, Yellow : 30-40%, Blue: 40%+)',
#                     xaxis_title='Odometer(m)',
#                     yaxis_title='Orientation'
#                 )
#
#                 # figx112.show()
#                 fig = figx112
#                 self.fig_plot = fig
#
#                 self.config.print_with_time("plotinng complete and now saving ")
#                 html_path = gmfl_path("heatmap_new.html")
#                 self.config.print_with_time(f"saving complete and temp html path: {html_path}")
#
#                 self.config.print_with_time("doing plotly offline")
#                 plotly.offline.plot(fig, filename=html_path, auto_open=False)
#                 self.config.print_with_time("rendring m_output ")
#                 # self.m_output.load(QUrl.fromLocalFile(html_path))
#                 self.config.print_with_time("rendring m_output completed")
#
#
#                 save_as_img(self, self.fig_plot, self.parent.project_name, self.Weld_id_tab9)
#                 self.config.print_with_time("End of conversion at : ")
#
#     return html_path
#
#                 # # Show web engine, hide canvas
#                 # self.m_output.setVisible(True)
#                 # self.canvas_tab9.setVisible(False)
#                 # self.reset_btn_tab9.setVisible(True)
#                 # self.all_box_selection1.setVisible(True)
#
#         # print("hiiii")
#         # QMessageBox.about(self, 'Pipe Analysis', 'Data Analysed Successfully')
#
#         # with self.config.connection.cursor() as cursor:
#         #     Fetch_weld_detail = "select id,pipe_id,`WT(mm)`,absolute_distance,upstream,defect_type,dimension_classification,orientation,length,Width_final,depth_new from defect_clock_hm where runid='%s' and pipe_id='%s'"
#         #     cursor.execute(Fetch_weld_detail, (self.runid, self.Weld_id_tab9))
#         #     self.myTableWidget_tab9.setRowCount(0)
#         #     allSQLRows = cursor.fetchall()
#         #     try:
#         #         if allSQLRows:
#         #             for row_number, row_data in enumerate(allSQLRows):
#         #                 self.myTableWidget_tab9.insertRow(row_number)
#         #                 for column_num, data in enumerate(row_data):
#         #                     self.myTableWidget_tab9.setItem(row_number, column_num,
#         #                                                     QtWidgets.QTableWidgetItem(str(data)))
#         #             # self.myTableWidget_tab9.setEditTriggers(QAbstractItemView.NoEditTriggers)
#         #             self.myTableWidget_tab9.setContextMenuPolicy(Qt.CustomContextMenu)
#         #             self.myTableWidget_tab9.customContextMenuRequested.connect(lambda: open_context_menu_ori_tab9(self))
#         #             # Check canvas visibility before adding the double-click functionality
#         #             if self.canvas_tab9.isVisible():
#         #                 self.myTableWidget_tab9.doubleClicked.connect(lambda: handle_table_double_click_chm(self))
#         #                 # Single row-click selects defect_no and absolute_distance
#         #             self.myTableWidget_tab9.clicked.connect(lambda idx: handle_row_click_tab9(self, idx))
#         #
#         #
#         #
#         #     except pymysql.Error as e:
#         #         print(f"MySQL Error: {e}")


def tab9_heatmap(self, status_callback, progress_callback, cancel_check):
    credentials = self.config.credentials
    project_id = self.config.project_id
    client = bigquery.Client(credentials=credentials, project=project_id)
    self.config.print_with_time("Pre graph analysis called")
    runid = self.parent.runid
    self.runid = self.parent.runid
    Weld_id_tab9 = self.combo_tab9.currentText()
    self.Weld_id_tab9 = int(Weld_id_tab9)
    wall_thickness = self.config.pipe_thickness
    pipe_id = self.Weld_id_tab9
    with self.config.connection.cursor() as cursor:
        # query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
        query = "SELECT start_index, end_index,start_oddo1,end_oddo1 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"
        cursor.execute(query, (self.runid, self.Weld_id_tab9, self.runid, self.Weld_id_tab9))
        result = cursor.fetchall()
        start_oddo1 = result[0][2]
        end_oddo1 = result[1][3]
        self.pipe_len_oddo1_chm = round(end_oddo1 - start_oddo1, 2)
        pipe_len_oddo1_chm = self.pipe_len_oddo1_chm

        if not result:
            self.config.print_with_time("No data found for this pipe ID : ")
        else:
            """
            pkl file is found in local path 
            """
            path = self.config.clock_pkl + self.parent.project_name + '/' + str(self.Weld_id_tab9) + '.pkl'

            if os.path.isfile(path):
                self.config.print_with_time("File exist")
                df_clock_holl = pd.read_pickle(path)
                [f"{h:02}:{int(m):02}" for h in range(12) for m in np.arange(0, 60, self.config.minute)]
                # val_ori_sensVal = df_clock_holl[[f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]]
                val_ori_sensVal = df_clock_holl[[f"{h:02}:{int(m):02}" for h in range(12) for m in np.arange(0, 60, self.config.minute)]]
                # self.map_ori_sens_ind = df_clock_holl[[f"{h:02}:{m:02}_x" for h in range(12) for m in range(0, 60, 5)]]
                self.map_ori_sens_ind = df_clock_holl[[f"{h:02}:{int(m):02}_x" for h in range(12) for m in np.arange(0, 60, self.config.minute)]]
                self.map_ori_sens_ind.columns = self.map_ori_sens_ind.columns.str.rstrip('_x')
                self.clock_col = val_ori_sensVal
                self.clock_data_col = val_ori_sensVal.values.tolist()
                self.mean_clock_data = val_ori_sensVal.mean().tolist()

                df3 = ((val_ori_sensVal - self.mean_clock_data) / self.mean_clock_data) * 100

                self.figure_tab9.clear()  # Clear the previous figure
                ax2 = self.figure_tab9.add_subplot(111)
                ax2.figure.subplots_adjust(bottom=0.151, left=0.060, top=0.820, right=1.000)
                d1 = df3.transpose().astype(float)
                #
                heat_map_obj = sns.heatmap(
                    d1,
                    cmap='jet',
                    ax=ax2,
                    vmin=-5, vmax=18,
                    square=False,
                    cbar_kws={'shrink': 0.8, 'pad': 0.005}
                )
                #
                # # Optional manual nudge
                cbar = heat_map_obj.collections[0].colorbar
                cbar.ax.set_position([0.955, 0.12, 0.02, 0.76])
                #
                # heat_map_obj.set(xlabel="Index", ylabel="Clock")

                """
                Pipewise ranges have been set
                """

                heat_map_obj.set(xlabel="Index", ylabel="Clock")

                self.oddo1_li_chm = df_clock_holl['ODDO1'].tolist()
                index_hm = list(df_clock_holl['index'])
                self.index_chm = index_hm
                # print("index_chm", self.index_chm)

                ax2.set_xticklabels(ax2.get_xticklabels(), size=9)
                ax2.set_yticklabels(ax2.get_yticklabels(), size=9)
                ax3 = ax2.twiny()
                oddo_val = [round(elem / 1000, 2) for elem in self.oddo1_li_chm]
                num_ticks1 = len(ax2.get_xticks())  # Adjust the number of ticks based on your preference
                # print(num_ticks1)
                tick_positions1 = [int(i) for i in np.linspace(0, len(oddo_val) - 1, num_ticks1)]
                # print(tick_positions1)
                ax3.set_xticks(tick_positions1)
                ax3.set_xticklabels([f'{oddo_val[i]:.2f}' for i in tick_positions1], rotation=90, size=9)
                ax3.set_xlabel("Absolute Distance (m)", size=9)

                def on_hover(event):
                    if event.xdata is not None and event.ydata is not None:
                        try:
                            x = int(event.xdata)
                            y = int(event.ydata)
                            index_value = index_hm[x]
                            clock_val = list(val_ori_sensVal.columns)[y]  ### It shows clock_column values ###
                            clock = self.map_ori_sens_ind.transpose().iloc[
                                y, x]  ### It shows real time values, like clock values at particular point ###
                            value = d1.iloc[y, x]
                            z = self.oddo1_li_chm[x]
                            self.canvas_tab9.toolbar.set_message(
                                f'Index={index_value:.0f},Abs.distance(m)={z / 1000:.3f},Clock={clock_val},'
                                f'Value={value:.1f}')
                        except (IndexError, ValueError):
                            # Print a user-friendly message instead of showing an error
                            print("Hovering outside valid data range. No data available.")

                self.figure_tab9.canvas.mpl_connect('motion_notify_event', on_hover)

                self.canvas_tab9.draw()  # Update the canvas with the new plot
                rs = RectangleSelector(self.figure_tab9.gca(), lambda eclick, erelease: line_select_callback_chm(self, eclick, erelease), useblit=True)
                plt.connect('key_press_event', rs)
                self.config.print_with_time("Plotted...")

                # # Show canvas, hide web engine
                # self.canvas_tab9.setVisible(True)
                # self.reset_btn_tab9.setVisible(True)
                # self.all_box_selection1.setVisible(True)
                # self.m_output.setVisible(False)
                return "__USE_LOCAL_PKL__"

            else:
                """
                pkl file is not found than data fetch from GCP and save pkl file in local path
                """
                if status_callback: status_callback.emit("Analysis started..")
                if progress_callback: self.smooth_progress(progress_callback, 0)

                # folder_path = self.config.clock_pkl + self.project_name
                folder_path1 = self.config.weld_pipe_pkl + self.parent.project_name
                folder_path = self.config.clock_pkl + self.parent.project_name
                Wall_thickness = self.config.pipe_thickness
                # print(folder_path)
                self.config.print_with_time("File not exist")

                #create folder if doesnt exist
                create_folders(self, folder_path, folder_path1)

                start_index, end_index = result[0][0], result[1][1]
                print(self.Weld_id_tab9)
                print(start_index, end_index)
                self.start_pipe_tab9, self.end_pipe_tab9 = start_index, end_index
                if cancel_check():
                    return "__CANCELLED__"

                if status_callback: status_callback.emit("Loading PKL / GCP data…")
                if progress_callback: self.smooth_progress(progress_callback, 10)
                if cancel_check():
                    return "__CANCELLED__"

                #fetch and save data from gcp
                out = fetch_and_save_tab9_data(self, client, start_index, end_index, folder_path1, self.Weld_id_tab9)
                df_elem = out["df_elem"]
                df_new_proximity_orientat = out["df_new_proximity_orientat"]
                if cancel_check():
                    return "__CANCELLED__"

                if status_callback: status_callback.emit("Processing Data Array")
                if progress_callback: self.smooth_progress(progress_callback, 20)
                # Process data_array which gives inputs for finding defect region using clustering and heatmap data and
                #name of function needs to be adjusted
                if cancel_check():
                    return "__CANCELLED__"

                processed_data_array = process_weld_data_to_create_data_array_for_clustering(self, folder_path1, self.Weld_id_tab9)


                #value extraction from the processed_data_array pipeline
                visited = set()
                bounding_boxes = []
                data_array = processed_data_array["data_array"]
                oddometer1 = processed_data_array["oddometer1"]
                data_x = processed_data_array["data_x"]
                t_raw = processed_data_array["t_raw"]
                mean1 = processed_data_array["mean1"]
                standard_deviation = processed_data_array["standard_deviation"]
                df_new_proximity = processed_data_array["df_new_proximity"]
                Roll_hr = processed_data_array["Roll_hr"]
                df3_raw = processed_data_array["df3_raw"]
                t = processed_data_array["t"]
                result = processed_data_array["result"]
                result_raw_df = processed_data_array["result_raw_df"]

                save_clock_pkl(self, df_elem, result_raw_df, Roll_hr, folder_path, df_new_proximity_orientat)
                if cancel_check():
                    return "__CANCELLED__"

                if status_callback: status_callback.emit("defect region using clustering")
                if progress_callback: self.smooth_progress(progress_callback, 30)

                self.config.print_with_time("Performing clustering to detect defect regions...start at : ")
                if cancel_check():
                    return "__CANCELLED__"
                # find defect region using clustering_filter_pipeline from utils to get start, end ( column , sensor)
                df_sorted = find_defect_regions_using_clustering(data_array)
                self.config.print_with_time("Performing clustering to detect defect regions...end at : ")


                df_clock_holl_oddo1 = data_x['ODDO1']
                oddo1_li = list(oddometer1)
                sensor_numbers = list(range(1, len(t.index) + 1))  # 1 to 144
                sensor_numbers = sensor_numbers[::-1]  # Reverse the list to go top=0 → bottom=144
                # Create a 2D text matrix where each row has the same sensor number
                text = np.array([[f"{sensor_no}"] * t.shape[1] for sensor_no in sensor_numbers])
                figx112 = go.Figure(data=go.Heatmap(
                    z=t_raw,
                    y=t.index,
                    x=[t.columns, oddo1_li],
                    text=text,
                    hovertemplate='Oddo: %{x}<br>Clock:%{y}<br>Value: %{z}, sensor no: %{text}',
                    zmin=-5,
                    zmax=18,
                    colorscale='jet',
                ))
                figx112.update_yaxes(autorange='reversed')
                if cancel_check():
                    return "__CANCELLED__"
                if status_callback: status_callback.emit("calculating threshold value...")
                if progress_callback: self.smooth_progress(progress_callback, 40)
                if cancel_check():
                    return "__CANCELLED__"

                self.config.print_with_time("calculate defect threshold start at : ")
                #threshold values calculation
                threshold_value, max_of_all = calculate_defect_threshold(df_sorted=df_sorted, result=result,
                                                                         defect_box_thresh=self.config.defect_box_thresh)
                self.config.print_with_time("calculate defect threshold end at : ")


                print("Processing defects with 3-part length classification...")

                # PROCESS DEFECTS WITH ADAPTIVE REFINEMENT
                finial_defect_list = []
                defect_counter = 1
                submatrices_dict = {}
                classification_stats = {
                    "Very Small (1-10%)": {"count": 0, "total_processed": 0},
                    "Small (10-20%)": {"count": 0, "total_processed": 0},
                    "Medium (20-30%)": {"count": 0, "total_processed": 0},
                    "Large (30-40%)": {"count": 0, "total_processed": 0},
                    "Very Large (40%+)": {"count": 0, "total_processed": 0},
                    "Below 1%": {"count": 0, "total_processed": 0}
                }

                self.config.print_with_time("------ start of iteration ------")
                result = result.apply(pd.to_numeric, errors='coerce')
                config = {
                    # core numeric config
                    "l_per_1": self.config.l_per_1,
                    "w_per_1": self.config.w_per_1,
                    "pipe_thickness": self.config.pipe_thickness,
                    "outer_dia": self.config.outer_dia,
                    "theta_ang1": self.config.theta_ang1,
                    "theta_ang2": self.config.theta_ang2,
                    "theta_ang3": self.config.theta_ang3,
                    "scaling_exponent": self.config.scaling_exponent,
                    # pipeline-level data
                    "pipe_len_oddo1_chm": self.pipe_len_oddo1_chm,
                    "calibration_factor": self.config.calibration_factor,
                    "min_energy_threshold": self.config.min_energy_threshold,
                    "positive_sigma_row": self.config.positive_sigma_row,
                    "div_factor": self.config.div_factor,

                    # IMPORTANT: This is a FUNCTION and it IS picklable
                    "get_adaptive_sigma_refinement": self.config.get_adaptive_sigma_refinement,
                }


                defect_counter = 1
                total_iters = 0
                total_rows = len(df_sorted)
                print(f"column names in df_sorted: {list(df_sorted.columns)}")

                # for row in df_sorted.itertuples(index=False):
                #
                #     total_iters += 1
                #
                #
                #     result_item = process_single_defect(
                #         self,config, result, df_clock_holl_oddo1, threshold_value,
                #         classification_stats, defect_counter,
                #         max_of_all, df3_raw, mean1, df_new_proximity, Roll_hr, t,
                #         submatrices_dict, finial_defect_list,
                #         pipe_id, runid, wall_thickness, figx112, row
                #     )
                #
                #     # If function returns None → skip
                #     if result_item is None:
                #         continue
                #
                #     # If defect was accepted → increment the counter
                #     if result_item is True:
                #         defect_counter += 1



                # print(f"total_rows in df_sorted before defect calculation loop: {total_rows}")
                config = {
                    # core numeric config
                    "l_per_1": self.config.l_per_1,
                    "w_per_1": self.config.w_per_1,
                    "pipe_thickness": self.config.pipe_thickness,
                    "outer_dia": self.config.outer_dia,
                    "theta_ang1": self.config.theta_ang1,
                    "theta_ang2": self.config.theta_ang2,
                    "theta_ang3": self.config.theta_ang3,
                    "scaling_exponent": self.config.scaling_exponent,
                    # pipeline-level data
                    "pipe_len_oddo1_chm": self.pipe_len_oddo1_chm,
                    "calibration_factor": self.config.calibration_factor,
                    "min_energy_threshold": self.config.min_energy_threshold,
                    "positive_sigma_row": self.config.positive_sigma_row,
                    "div_factor": self.config.div_factor,

                    # IMPORTANT: This is a FUNCTION and it IS picklable
                    "get_adaptive_sigma_refinement": self.config.get_adaptive_sigma_refinement,
                }
                total = len(df_sorted)
                loop_start = 40
                loop_end = 60

                self.config.print_with_time("starting defect loop : ")
                total = len(df_sorted)

                self.config.print_with_time("starting defect loop : ")
                if cancel_check():
                    return "__CANCELLED__"

                for idx, row in enumerate(df_sorted.itertuples(index=False), start=1):
                    if cancel_check():
                        self.config.print_with_time("Cancelled by user.")
                        return "__CANCELLED__"

                    if progress_callback:
                        pct = loop_start + int((idx / total) * (loop_end - loop_start))
                        progress_callback.emit(pct)

                    if status_callback:
                        status_callback.emit(f"Processing row {idx} / {total}…")

                    total_iters += 1

                    self.config.print_with_time(f" current id -- {total_iters} started at : ")
                    res = compute_defect_data(
                        config, result, df_clock_holl_oddo1, threshold_value,
                        max_of_all, df3_raw, mean1,
                        df_new_proximity, Roll_hr, t,
                        pipe_id, runid, wall_thickness,
                        row, pipe_len_oddo1_chm
                    )
                    self.config.print_with_time(f" current id -- {total_iters} ending at : ")

                    defect_counter = apply_defect_result(
                        self,
                        res,
                        classification_stats,
                        defect_counter,
                        submatrices_dict,
                        finial_defect_list,
                        figx112
                    )

                self.config.print_with_time("ending defect loop : ")



                # #-------------------with cores only--------------------------------
                # config = {
                #     # core numeric config
                #     "l_per_1": self.config.l_per_1,
                #     "w_per_1": self.config.w_per_1,
                #     "pipe_thickness": self.config.pipe_thickness,
                #     "outer_dia": self.config.outer_dia,
                #     "theta_ang1": self.config.theta_ang1,
                #     "theta_ang2": self.config.theta_ang2,
                #     "theta_ang3": self.config.theta_ang3,
                #     "scaling_exponent": self.config.scaling_exponent,
                #     # pipeline-level data
                #     "pipe_len_oddo1_chm": self.pipe_len_oddo1_chm,
                #     "calibration_factor": self.config.calibration_factor,
                #     "min_energy_threshold": self.config.min_energy_threshold,
                #     "positive_sigma_row": self.config.positive_sigma_row,
                #     "div_factor": self.config.div_factor,
                #     "get_adaptive_sigma_refinement": self.config.get_adaptive_sigma_refinement,
                # }
                #
                # # ────────────────────────────────
                # # Manual CPU workers (you choose)
                # # ────────────────────────────────
                # threshold_workers = 7  # <--- set number of cores to use
                # length_index = len(t.index)
                #
                # # ---- Build small lightweight task list ----
                # tasks = [
                #     (row.start_row, row.end_row, row.start_col, row.end_col)
                #     for row in df_sorted.itertuples(index=False)
                # ]
                #
                # print(f"Total defects to process: {len(tasks)}")
                # from multiprocessing import Pool
                # # ---- Run multiprocessing with global-shared data ----
                # self.config.print_with_time("starting pool")
                # with Pool(
                #         processes=threshold_workers,
                #         initializer=init_defect_worker,
                #         initargs=(
                #                 config,
                #                 result,
                #                 df_clock_holl_oddo1,
                #                 threshold_value,
                #                 max_of_all,
                #                 df3_raw,
                #                 mean1,
                #                 df_new_proximity,
                #                 Roll_hr,
                #                 pipe_id,
                #                 runid,
                #                 wall_thickness,
                #                 pipe_len_oddo1_chm,
                #                 length_index,
                #         ),
                # ) as pool:
                #
                #     results = pool.map(compute_defect_data_multicore, tasks)
                #
                # self.config.print_with_time("pool completed")
                #
                # # ---- Post-processing ----
                # accepted_count = sum(1 for r in results if r.get("accepted"))
                # print("Accepted defects returned by workers:", accepted_count)
                #
                # # ────────────────────────────────
                # # Apply results (ORDER PRESERVED)
                # # ────────────────────────────────
                # defect_counter = 1
                # self.config.print_with_time("starting result adding ")
                # for res in results:
                #     defect_counter = apply_defect_result(
                #         self,
                #         res,
                #         classification_stats,
                #         defect_counter,
                #         submatrices_dict,
                #         finial_defect_list,
                #         figx112
                #     )
                # self.config.print_with_time("ending result adding ")


                #------------------WITH CORE AND BATCHES---------------------------------------
                # tasks = [
                #     (row.start_row, row.end_row, row.start_col, row.end_col)
                #     for row in df_sorted.itertuples(index=False)
                # ]
                #
                # total_defects = len(tasks)
                # print(f"Total defects to process: {total_defects}")
                #
                # # --------------------------------------------
                # # BATCHING FOR REAL SPEEDUP
                # # --------------------------------------------
                # num_workers = threshold_workers
                # batches = chunk_list(tasks, num_workers)
                #
                # self.config.print_with_time(
                #     f"Starting pool with {num_workers} workers, {total_defects} defects, {len(batches)} batches")
                #
                # from multiprocessing import Pool
                #
                # with Pool(
                #         processes=num_workers,
                #         initializer=init_defect_worker,
                #         initargs=(
                #                 config,
                #                 result,
                #                 df_clock_holl_oddo1,
                #                 threshold_value,
                #                 max_of_all,
                #                 df3_raw,
                #                 mean1,
                #                 df_new_proximity,
                #                 Roll_hr,
                #                 pipe_id,
                #                 runid,
                #                 wall_thickness,
                #                 pipe_len_oddo1_chm,
                #                 length_index,
                #         ),
                # ) as pool:
                #
                #     # Map batches to workers
                #     batch_results = pool.map(process_batch, batches)
                #
                # self.config.print_with_time("Pool completed")
                #
                # # --------------------------------------------
                # # FLATTEN BATCH RESULTS BACK TO SINGLE LIST
                # # --------------------------------------------
                # results = [res for batch in batch_results for res in batch]
                #
                # # --------------------------------------------
                # # POST-PROCESSING SAME AS BEFORE
                # # --------------------------------------------
                # accepted_count = sum(1 for r in results if r.get("accepted"))
                # print("Accepted defects returned by workers:", accepted_count)
                #
                # # Preserve order, apply results
                # defect_counter = 1
                # self.config.print_with_time("starting result adding")
                #
                # for res in results:
                #     defect_counter = apply_defect_result(
                #         self,
                #         res,
                #         classification_stats,
                #         defect_counter,
                #         submatrices_dict,
                #         finial_defect_list,
                #         figx112
                #     )
                #
                # self.config.print_with_time("ending result adding")

                print(f"total_rows in df_sorted after defect calculation loop: {total_rows}")
                # print(f"total iters in defect calculation loop = {total_iters}")


                self.config.print_with_time("------ end of iteration ------")



                print(f"\nTotal submatrices stored: {len(submatrices_dict)}")

                project_name = self.parent.project_name
                print(f"project name :  {project_name}")
                output_dir = os.path.join(os.getcwd(), 'backend_data', 'data_generated', 'submatrix_generated',
                                          project_name) + '/'
                manage_directory(output_dir)
                save_submatrices(submatrices_dict, output_dir)
                print(f"\n=== DEFECT CLASSIFICATION SUMMARY ===")
                print(f"Total defects found: {len(finial_defect_list)}")
                defect_summary(finial_defect_list, classification_stats)
                if cancel_check():
                    return "__CANCELLED__"

                if status_callback: status_callback.emit("inserting into database...")
                if progress_callback: self.smooth_progress(progress_callback, 60)
                if cancel_check():
                    return "__CANCELLED__"

                # DATABASE INSERTION
                self.config.print_with_time("start of insertion in database")
                try:
                    print("\nInserting defects into database...")
                    # insert_defects_to_db_bb_new(self.config.connection, finial_defect_list, submatrices_dict)
                    insert_defects_to_db_defect_clock_hm(self.config.connection, finial_defect_list, submatrices_dict)
                except Exception as e:
                    print(f"error data: {e}")
                self.config.print_with_time("end of insertion in database")

                if cancel_check():
                    return "__CANCELLED__"

                if status_callback: status_callback.emit("Ml Width calculation and insertion...")
                if progress_callback: self.smooth_progress(progress_callback, 70)
                #width_final calculation
                self.config.print_with_time("starting ml width calc: ")
                ML_width_calc(self, output_dir, runid, pipe_id)
                self.config.print_with_time("ending ml width calc: ")
                print(
                    f"\nProcessing complete! Found {len(finial_defect_list)} total defects using 3-part classification.")
                if cancel_check(): return ""

                if status_callback: status_callback.emit("html generation...")
                if progress_callback: self.smooth_progress(progress_callback, 85)
                # FINAL VISUALIZATION
                self.config.print_with_time("Displaying visualization...")
                figx112.update_layout(
                    # title='Heatmap with 3-Part Adaptive Length Classification (purple: 1-10%, Red : 10-20%, Orange: 20-30%, Yellow : 30-40%, Blue: 40%+)',
                    xaxis_title='Odometer(m)',
                    yaxis_title='Orientation'
                )

                # figx112.show()
                fig = figx112
                self.fig_plot = fig

                self.config.print_with_time("plotinng complete and now saving ")
                html_path = gmfl_path("heatmap_new.html")
                self.config.print_with_time(f"saving complete and temp html path: {html_path}")

                self.config.print_with_time("doing plotly offline")
                plotly.offline.plot(fig, filename=html_path, auto_open=False)
                # self.config.print_with_time("rendring m_output ")
                # self.m_output.load(QUrl.fromLocalFile(html_path))
                # self.config.print_with_time("rendring m_output completed")


                save_as_img(self, self.fig_plot, self.parent.project_name, self.Weld_id_tab9)
                self.config.print_with_time("End of conversion at : ")
                if cancel_check():
                    return "__CANCELLED__"

                if status_callback: status_callback.emit("Completed.")
                if progress_callback: self.smooth_progress(progress_callback, 100)

                return html_path

                # # Show web engine, hide canvas
                # self.m_output.setVisible(True)
                # self.canvas_tab9.setVisible(False)
                # self.reset_btn_tab9.setVisible(True)
                # self.all_box_selection1.setVisible(True)

        # print("hiiii")
        # QMessageBox.about(self, 'Pipe Analysis', 'Data Analysed Successfully')

        # with self.config.connection.cursor() as cursor:
        #     Fetch_weld_detail = "select id,pipe_id,`WT(mm)`,absolute_distance,upstream,defect_type,dimension_classification,orientation,length,Width_final,depth_new from defect_clock_hm where runid='%s' and pipe_id='%s'"
        #     cursor.execute(Fetch_weld_detail, (self.runid, self.Weld_id_tab9))
        #     self.myTableWidget_tab9.setRowCount(0)
        #     allSQLRows = cursor.fetchall()
        #     try:
        #         if allSQLRows:
        #             for row_number, row_data in enumerate(allSQLRows):
        #                 self.myTableWidget_tab9.insertRow(row_number)
        #                 for column_num, data in enumerate(row_data):
        #                     self.myTableWidget_tab9.setItem(row_number, column_num,
        #                                                     QtWidgets.QTableWidgetItem(str(data)))
        #             # self.myTableWidget_tab9.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #             self.myTableWidget_tab9.setContextMenuPolicy(Qt.CustomContextMenu)
        #             self.myTableWidget_tab9.customContextMenuRequested.connect(lambda: open_context_menu_ori_tab9(self))
        #             # Check canvas visibility before adding the double-click functionality
        #             if self.canvas_tab9.isVisible():
        #                 self.myTableWidget_tab9.doubleClicked.connect(lambda: handle_table_double_click_chm(self))
        #                 # Single row-click selects defect_no and absolute_distance
        #             self.myTableWidget_tab9.clicked.connect(lambda idx: handle_row_click_tab9(self, idx))
        #
        #
        #
        #     except pymysql.Error as e:
        #         print(f"MySQL Error: {e}")

def handle_row_click_tab9(self, index):
    row = index.row()

    # Column 0 → defect no
    defect_no_item = self.myTableWidget_tab9.item(row, 0)

    # Column 3 → absolute_distance
    abs_dist_item = self.myTableWidget_tab9.item(row, 3)

    if defect_no_item and abs_dist_item:
        self.selected_defect_no = defect_no_item.text()
        self.selected_abs_distance = abs_dist_item.text()
        self.digsheet_btn.setEnabled(True)

        print("🔍 CLICK SELECTED")
        print("   Defect No:", self.selected_defect_no)
        print("   Absolute Distance:", self.selected_abs_distance)



