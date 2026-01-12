from matplotlib.patches import Rectangle
from matplotlib.widgets import RectangleSelector
import seaborn as sns
import matplotlib.pyplot as plt
import os
# from GMFL_12_Inch_Desktop.Components.Configs import config as Config
from PIL import Image
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter


def generate_heat_map(self, canvas, full_screen_function, df_new_tab8,
                      line_select_callback, company_name, Weld_id, figure, lower_sensitivity, upper_sensitivity, oddo1, index_hm):
    """"
    Generate heap map is a function that will generate Heat map using following params
        :param layout : Layout object in which graph is going to display
        :param full_screen_function : A method that will remove list and make chart visible to full screen
        :param defect_list : List of Defect
        :param df_hue : Data frame to show Heat-map
        :param line_select_callback : A method that will call after every rectangle selection
        :param company_name : A String that will contain Company name
        :param pipe_id : Current Pipe ID
        :param figure : Figure a object of canvas
    """

    df_new_tab8 = df_new_tab8.apply(pd.to_numeric, errors='coerce')

    sensor_columns = [f'F{i}H{j}' for i in range(1, self.config.F_columns + 1) for j in range(1, 5)]
    df1 = df_new_tab8[[f'F{i}H{j}' for i in range(1, self.config.F_columns + 1) for j in range(1, 5)]]
    df3 = df1.copy()

    window_length = 15
    polyorder = 2

    for col in sensor_columns:
        data = df1[col].values
        time_index = np.arange(len(df1))
        coefficients = np.polyfit(time_index, data, polyorder)
        trend = np.polyval(coefficients, time_index)
        data_dettrended = data - trend
        data_denoised = savgol_filter(data_dettrended, window_length, polyorder)
        df_new_tab8.loc[:len(df1), col] = data_denoised

    # df_new_tab9.to_csv("C:/Users/Shradha Agarwal/Desktop/bpcl clock/data_denoised.csv")

    # column_means = df_new_tab8.abs().mean()
    # # print("column_means", column_means)
    #
    # sensor_mean = [int(i_x) for i_x in column_means]
    #
    # standard_deviation = df_new_tab8.std(axis=0, skipna=True).tolist()
    #
    # """
    # To Calculate upper thersold Value
    # """
    # mean_plus_1sigma = []
    # for i, data1 in enumerate(sensor_mean):
    #     sigma1 = data1 + (Config.positive_threshold) * standard_deviation[i]
    #     mean_plus_1sigma.append(sigma1)
    # # print("sigma1_positive",mean_plus_1sigma)
    #
    # """
    # To Calculate lower thersold value
    # """
    # mean_negative_3sigma = []
    # for i_2, data_3 in enumerate(sensor_mean):
    #     sigma_3 = data_3 - (Config.negative_threshold) * standard_deviation[i_2]
    #     mean_negative_3sigma.append(sigma_3)
    # # print("sigma3_negative",mean_negative_3sigma)
    #
    # """
    # Values above the upper threshold are considered as 1,
    # values below the lower threshold are considere
    # d as 1,
    # and values between the upper and lower thresholds are considered as 0.
    # """
    #
    # for col, data in enumerate(df_new_tab8.columns):
    #     df_new_tab8[data] = df_new_tab8[data].apply(
    #         lambda x: 1 if x > mean_plus_1sigma[col] else (-1 if x < mean_negative_3sigma[col] else 0)
    #     )
    #
    # test_val = df_new_tab8
    # test_val['ODDO'] = oddo1
    # test_val['row_sum'] = ((test_val.sum(axis=1))/144*100).round(2)
    #
    # filtered_df1 = test_val[[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)]]
    #
    # df3.columns = filtered_df1.columns
    # df1_aligned = filtered_df1.reindex(df3.index)
    # result = df1_aligned * df3
    # result = result.dropna()
    # result.reset_index(drop=True, inplace=True)
    # print("result",result)
    # df_new_8 = result.transpose()

    df_new_8 = df_new_tab8.transpose()

    figure.clear()
    ax2 = figure.add_subplot(111)
    full_screen_function()
    ax2.figure.subplots_adjust(bottom=0.221, left=0.060, top=0.835, right=0.990)
    # figure.set_size_inches(20, 6)

    # color_ranges = [
    #         (-100, -90), (-90, -80), (-80, -70), (-70, -60), (-60, -50), (-50, -40), (-40, -30), (-30, -20),
    #         (-20, -10), (-10, 0),
    #         (0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 90),
    #         (90, 100)]
    #
    # color_values = ['#3d045a', '#4f355c', '#CD1076', '#8E236B', '#0530ad', '#6205db', '#8f39ff',
    #                 '#016fff', '#74b0ff', '#82ffff',
    #                 '#82ffff', '#00CD00', '#008000', '#fd8f00', '#D98719', '#CD661D', '#EE4000',
    #                 '#FF0000', '#820202', '#000000']
    #
    # custom_palette = sns.color_palette(color_values)
    # bounds = [r[0] for r in color_ranges] + [color_ranges[-1][1]]
    # cmap = ListedColormap(color_values)
    # norm = BoundaryNorm(bounds, cmap.N)

    # heat_map_obj = sns.heatmap(df_hue, cmap=cmap, ax=ax2, norm=norm)

    # heat_map_obj = sns.heatmap(df_new_8, cmap='jet', ax=ax2, vmin=-10000,vmax=18000)
    heat_map_obj = sns.heatmap(df_new_8, cmap='jet', ax=ax2)
    ax2.set_xticklabels(ax2.get_xticklabels(), size=9)
    ax2.set_yticklabels(ax2.get_yticklabels(), size=9)

    # print("df_hue...", df_hue)
    oddo1_li = [round(elem / 1000, 3) for elem in oddo1]

    ax3 = ax2.twiny()
    oddo_val = list(oddo1_li)
    num_ticks1 = len(ax2.get_xticks())  # Adjust the number of ticks based on your preference
    # print(num_ticks1)
    tick_positions1 = [int(i) for i in np.linspace(0, len(oddo_val) - 1, num_ticks1)]
    # print(tick_positions1)

    ax3.set_xticks(tick_positions1)
    ax3.set_xticklabels([f'{oddo_val[i]:.3f}' for i in tick_positions1], rotation=90, size=9)
    ax3.set_xlabel("Absolute Distance (m)", size=9)

    def on_hover(event):
        if event.xdata is not None and event.ydata is not None:
            try:
                x = int(event.xdata)
                y = int(event.ydata)
                index_value = index_hm[x]
                value = df_new_8.iloc[y, x]
                z = oddo1_li[x]
                canvas.toolbar.set_message(f'Index={index_value:.0f},Abs.distance(m)={z},Sensor_no={y:.0f},Value={value}')
            except (IndexError, ValueError):
                # Print a user-friendly message instead of showing an error
                print("Hovering outside valid data range. No data available.")

    figure.canvas.mpl_connect('motion_notify_event', on_hover)
    heat_map_obj.set(xlabel="Number of Observation", ylabel="Sensors")

    rs = RectangleSelector(figure.gca(), line_select_callback,
                           useblit=True)
    plt.connect('key_press_event', rs)

    #plt.plot(index,odd1,oddo2)
    # save_as_img(heat_map_obj, company_name, Weld_id, lower_sensitivity, upper_sensitivity)
      # to fix the index overlapping
    plt.tight_layout()
    canvas.draw()


def save_as_img(heat_map_obj, company_name, pipe_id, lower_sensitivity, upper_sensitivity):
    """
    This will save the plotted chat as a image format
        :param heat_map_obj:object of seaborn heatmap
        :param company_name:company name used to create folder
        :param pipe_id:Image of graph will be saved as pipe Id
    """
    print(heat_map_obj)
    print(company_name)
    print(pipe_id)
    figure = heat_map_obj.get_figure()
    print("here1")
    # img_path = os.getcwd() + '/Charts/' + company_name +'/' + str(pipe_id)
    # #img_name = str(pipe_id) + '.png'
    # img_name = str(lower_sensitivity+upper_sensitivity) + '.png'
    #
    # try:
    #     os.makedirs(img_path)
    # except OSError as error:
    #     pass
    # print("path", img_path + img_name)
    # figure.savefig(img_path + '/' + img_name, dpi=400)
    # print("here 2")
    # im = Image.open(img_path + '/' + img_name)
    # im1 = im.rotate(360, expand=1)
    # im1.save(img_path + '/' + img_name)
    # # Setting the points for cropped image
    # left = 200
    # top = 100
    # right = 3400
    # bottom = 6000
    #
    # im = Image.open(img_path + '/' + img_name)
    # #im1 = im.crop((left, top, right, bottom))
    # im1.save(img_path + '/' + img_name)
