import numpy as np
import pandas as pd


# def fetch_and_save_tab9_data(self, client, start_index, end_index, folder_path1, Weld_id_tab9):
#     """
#     Optimized — uses BigQuery Storage API.
#     Naming, logic, output = IDENTICAL to old code.
#     """
#     credentials = service_account.Credentials.from_service_account_file(
#         "./utils/Authorization.json",
#         scopes=[
#             "https://www.googleapis.com/auth/cloud-platform",
#             "https://www.googleapis.com/auth/bigquery",
#             "https://www.googleapis.com/auth/bigquery.readonly",
#         ]
#     )
#
#     # -----------------------------------------------------------
#     # Init Storage API client ONCE (reuses client each call)
#     # -----------------------------------------------------------
#     self.config.print_with_time("Start of conversion at : ")
#     if not hasattr(self, "_bqstorage_client") or self._bqstorage_client is None:
#         self._bqstorage_client = BigQueryReadClient()
#
#
#     bqstorage_client = bigquery_storage_v1.BigQueryReadClient(credentials=credentials)
#
#     # -----------------------------------------------------------
#     # 1️⃣ FIRST QUERY — using Storage API
#     # -----------------------------------------------------------
#     self.config.print_with_time("⏳[1] Start building first-query SQL")
#
#     query_for_start = (
#         "SELECT index, ROLL, ODDO1, ODDO2, ["
#         + self.config.sensor_str_hall +
#         "] AS HALL_DATA, PITCH, YAW "
#         "FROM " + self.config.table_name + " "
#         "WHERE index>{} AND index<{}"
#     )
#
#     self.config.print_with_time("🚀[2] Start sending first query (Storage API)")
#     query_job = client.query(query_for_start.format(start_index, end_index))
#
#     self.config.print_with_time("📥[3] Start to_dataframe() for first query")
#     results = query_job.to_dataframe(bqstorage_client=bqstorage_client)
#     self.config.print_with_time(f"📤[4] results fetched → {len(results)} rows")
#
#     # df_main starts as copied results (same naming convention)
#     self.config.print_with_time("🧱[5] Creating df_main")
#     df_main = results.copy()
#     # 🔧 Ensure same ordering as old BigQuery Iterator
#     df_main = df_main.sort_values("index").reset_index(drop=True)
#     # -----------------------------------------------------------
#     # Expand HALL_DATA array → F1H1...F36H4
#     # -----------------------------------------------------------
#     self.config.print_with_time("🧩[6] Expanding HALL_DATA")
#
#     hall_cols = [
#         f'F{i}H{j}'
#         for i in range(1, self.config.F_columns + 1)
#         for j in range(1, 5)
#     ]
#
#     df_hall = pd.DataFrame(df_main["HALL_DATA"].tolist(), columns=hall_cols)
#
#     df_main = pd.concat([df_main.drop(columns=["HALL_DATA"]), df_hall], axis=1)
#
#     # -----------------------------------------------------------
#     # Reference subtraction (same logic as before)
#     # -----------------------------------------------------------
#     self.config.print_with_time("🧮[7] Applying reference subtraction")
#
#     df_main["ODDO1"] -= self.config.oddo1
#     df_main["ODDO2"] -= self.config.oddo2
#     df_main["ROLL"] -= self.config.roll_value
#     df_main["PITCH"] -= self.config.pitch_value
#     df_main["YAW"] -= self.config.yaw_value
#
#     self.config.print_with_time("📘[8] First-query data prepared")
#
#     # -----------------------------------------------------------
#     # 2️⃣ SECOND QUERY — using Storage API
#     # -----------------------------------------------------------
#     self.config.print_with_time("⏳[9] Start building prox-query SQL")
#
#     query_for_start = (
#         "SELECT index, ["
#         + self.config.sensor_str_prox +
#         "] AS PROX_DATA "
#         "FROM " + self.config.table_name + " "
#         "WHERE index>{} AND index<{}"
#     )
#
#     self.config.print_with_time("🚀[10] Start sending prox query (Storage API)")
#     query_job = client.query(query_for_start.format(start_index, end_index))
#
#     self.config.print_with_time("📥[11] Start to_dataframe() for prox query")
#     results_1 = query_job.to_dataframe(bqstorage_client=bqstorage_client)
#     self.config.print_with_time(f"📤[12] results_1 fetched → {len(results_1)} rows")
#
#     # -----------------------------------------------------------
#     # Expand PROX_DATA array → prox sensor columns
#     # -----------------------------------------------------------
#     self.config.print_with_time("🧩[13] Expanding PROX_DATA")
#
#     prox_df = pd.DataFrame(
#         results_1["PROX_DATA"].tolist(),
#         columns=self.config.sensor_columns_prox
#     )
#     prox_df.insert(0, "index", results_1["index"])
#     # 🔧 Ensure proximities are in correct index order
#     prox_df = prox_df.sort_values("index").reset_index(drop=True)
#
#     self.config.print_with_time("📘[14] Proximity expansion complete")
#
#     # -----------------------------------------------------------
#     # Keep original variable conventions
#     # -----------------------------------------------------------
#     self.config.print_with_time("🔁[15] Restoring original variables")
#
#     index_tab9 = df_main["index"].tolist()
#     index_hm_orientation = results_1["index"].tolist()
#
#     df_elem = df_main[["index", "ODDO1", "ROLL", "PITCH", "YAW"]].copy()
#
#     self_df_new_proximity_orientat = prox_df[self.config.sensor_columns_prox].copy()
#
#     # -----------------------------------------------------------
#     # Merge (same logic)
#     # -----------------------------------------------------------
#     self.config.print_with_time("🔗[16] Merging df_main + prox_df")
#
#     df_pipe = df_main.merge(prox_df, on="index", how="inner")
#
#     self.config.print_with_time("📘[17] Merge complete")
#
#     # -----------------------------------------------------------
#     # Save pickle (same output as before)
#     # -----------------------------------------------------------
#     self.config.print_with_time("💾[18] Saving pickle file")
#
#     file_path = folder_path1 + '/' + str(Weld_id_tab9) + '.pkl'
#     df_pipe.to_pickle(file_path)
#
#     self.config.print_with_time(f"✅[19] Saved → {file_path}")
#
#     # -----------------------------------------------------------
#     # Return structure identical to old code
#     # -----------------------------------------------------------
#     return {
#         "file_path": file_path,
#         "df_pipe": df_pipe,
#         "index_tab9": index_tab9,
#         "index_hm_orientation": index_hm_orientation,
#         "df_elem": df_elem,
#         "df_new_proximity_orientat": self_df_new_proximity_orientat,
#     }

def plot_heatmap(self, df_clock_holl):
    clock_cols = [f"{h:02}:{int(m):02}" for h in range(12) for m in np.arange(0, 60, 15)]
    clock_x_cols = [c + "_x" for c in clock_cols]

    val_ori_sensVal = df_clock_holl[clock_cols].reset_index(drop=True)

    self.map_ori_sens_ind = df_clock_holl[clock_x_cols].reset_index(drop=True)
    self.map_ori_sens_ind.columns = self.map_ori_sens_ind.columns.str.rstrip('_x')

    self.clock_col = val_ori_sensVal
    self.clock_data_col = val_ori_sensVal.values.tolist()

    self.mean_clock_data = val_ori_sensVal.mean().values
    df3 = ((val_ori_sensVal - self.mean_clock_data) / self.mean_clock_data) * 100

    # ------------------- Plot -------------------

    self.figure_tab8.clear()
    ax2 = self.figure_tab8.add_subplot(111)
    ax2.figure.subplots_adjust(bottom=0.151, left=0.060, top=0.820, right=1.000)

    d1 = df3.T.astype(float)

    heat_map_obj = sns.heatmap(
        d1, cmap='jet', ax=ax2, vmin=-5, vmax=18, square=False,
        cbar_kws={'shrink': 0.8, 'pad': 0.005}
    )

    heat_map_obj.set(xlabel="Index", ylabel="Clock")

    cbar = heat_map_obj.collections[0].colorbar
    cbar.ax.set_position([0.955, 0.12, 0.02, 0.76])

    # ------------------- Axes -------------------

    self.oddo1_li_chm = df_clock_holl['ODDO1'].values.tolist()
    self.index_chm = df_clock_holl['index'].values.tolist()

    ax2.set_xticklabels(ax2.get_xticklabels(), size=9)
    ax2.set_yticklabels(ax2.get_yticklabels(), size=9)

    ax3 = ax2.twiny()
    oddo_val = [round(elem / 1000, 2) for elem in self.oddo1_li_chm]

    tick_positions1 = np.linspace(0, len(oddo_val) - 1, len(ax2.get_xticks())).astype(int)
    ax3.set_xticks(tick_positions1)
    ax3.set_xticklabels([f'{oddo_val[i]:.2f}' for i in tick_positions1], rotation=90, size=9)
    ax3.set_xlabel("Absolute Distance (m)", size=9)


    # ------------------- Hover -------------------

    def on_hover(event):
        if event.xdata is None or event.ydata is None:
            return
        x = int(event.xdata)
        y = int(event.ydata)
        if x < 0 or y < 0 or x >= len(self.index_chm) or y >= len(clock_cols):
            return

        index_value = self.index_chm[x]
        clock_val = clock_cols[y]
        clock = self.map_ori_sens_ind.T.iloc[y, x]
        value = d1.iloc[y, x]
        z = self.oddo1_li_chm[x]

        self.canvas_tab8.toolbar.set_message(
            f'Index={index_value}, Abs.distance(m)={z / 1000:.3f}, Clock={clock_val}, Value={value:.1f}'
        )


    self.index_tab8 = self.index_chm

    self.figure_tab8.canvas.mpl_connect('motion_notify_event', on_hover)
    self.canvas_tab8.draw()

    rs = RectangleSelector(self.figure_tab8.gca(), self.line_select_callback_t8, useblit=True)
    plt.connect('key_press_event', rs)

    Config.print_with_time("Plotted...")