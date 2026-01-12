from google.cloud import bigquery
import json
from pathlib import Path
import os
import pandas as pd
import plotly.io as pio
import plotly.graph_objs as go
# from GMFL_12_Inch_Desktop.Components.Configs import config as config
#
#
# connection = config.connection
# company_list = []  # list of companies
# credentials = config.credentials
# project_id = config.project_id
# client = bigquery.Client(credentials=credentials, project=project_id)
# config = json.loads(open(r'D:\Anubhav\vdt_backend\GMFL_12_Inch_Desktop\utils\proximity_base_value.json').read())

# Dynamically locate the GMFL root (2 levels above this file)
GMFL_ROOT = Path(__file__).resolve().parents[3]


def gmfl_path(relative):
    """Return absolute path inside GMFL backend_data/temp folder."""
    temp_dir = GMFL_ROOT / "backend_data" / "data_generated" / "temp"
    os.makedirs(temp_dir, exist_ok=True)  # make sure folder exists
    return str(temp_dir / relative)


def Magnetization(self, pipe_id):
    # weld_id_1 = self.combo_graph.currentText()
    weld_id_1 = pipe_id
    self.weld_id_1 = int(weld_id_1)
    runid = self.parent.parent.runid
    self.runid = self.parent.parent.runid
    print("inside magne")
    with self.config.connection.cursor() as cursor:
        # query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
        query = "SELECT start_index, end_index,start_oddo1,end_oddo1 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"
        cursor.execute(query, (self.runid, self.weld_id_1, self.runid, self.weld_id_1))
        result = cursor.fetchall()
        start_oddo1 = result[0][2]
        end_oddo1 = result[1][3]

        start_index, end_index = result[0][0], result[1][1]
        print(start_index, end_index)
        # Config.print_with_time("Start fetching at : ")

        # query_for_start = 'SELECT index,ODDO1,ODDO2,[F1H1, F1H2, F1H3, F1H4, F2H1, F2H2, F2H3, F2H4,F3H1, F3H2, F3H3, F3H4, F4H1, F4H2, F4H3,F4H4, F5H1, F5H2, F5H3, F5H4, F6H1, F6H2, F6H3, F6H4,F7H1, F7H2, F7H3, F7H4, F8H1, F8H2, F8H3, F8H4, F9H1, F9H2, F9H3, F9H4, F10H1,F10H2, F10H3, F10H4,F11H1, F11H2, F11H3, F11H4, F12H1, F12H2, F12H3, F12H4, F13H1, F13H2, F13H3,F13H4, F14H1, F14H2, F14H3, F14H4,F15H1, F15H2, F15H3, F15H4, F16H1, F16H2, F16H3, F16H4, F17H1, F17H2, F17H3,F17H4, F18H1, F18H2, F18H3, F18H4,F19H1, F19H2, F19H3, F19H4, F20H1, F20H2, F20H3, F20H4, F21H1, F21H2, F21H3,F21H4, F22H1, F22H2, F22H3, F22H4,F23H1, F23H2, F23H3, F23H4, F24H1, F24H2, F24H3, F24H4, F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4, F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, F33H1, F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4] FROM ' + Config.table_name + ' WHERE index>{} AND index<{} order by index'
        query_for_start = (
                "SELECT index, ODDO1, ODDO2, ["
                + self.config.sensor_str_hall +
                "] FROM "
                + self.config.table_name +
                " WHERE index>{} AND index<{} ORDER BY index"
        )
        query_job = self.config.client.query(query_for_start.format(start_index, end_index))
        results = query_job.result()
        data = []
        self.index_tab_m = []
        oddo_x = []
        oddo_y = []
        data1 = []

        self.config.print_with_time("Start of conversion at : ")
        for row in results:
            self.index_tab_m.append(row[0])
            oddo_x.append(row[1])
            oddo_y.append(row[2])
            data1.append(row[3])

        self.oddo1_tab_m = []
        self.oddo2_tab_m = []

        """
        Reference value will be consider 
        """
        for odometer1 in oddo_x:
            od1 = odometer1 - self.config.oddo1  ###16984.2 change According to run
            self.oddo1_tab_m.append(od1)
        for odometer2 in oddo_y:
            od2 = odometer2 - self.config.oddo2  ###17690.36 change According to run
            self.oddo2_tab_m.append(od2)

        oddometer = [round(x / 1000, 3) for x in self.oddo1_tab_m]
        df_new_tab9 = pd.DataFrame(data1, columns=[f'F{i}H{j}' for i in range(1, self.config.F_columns + 1) for j in range(1, 5)])
        mean_row_wise_dataframe = df_new_tab9.mean(axis=1)
        sensor_max_value = 65535  # maximum value of any sensor
        sensor_voltage_level = 3.3  # 3.3volt (currently fixed)
        # Senstivity of the sensor: miliTesla(mT) [this is variable and changed everytime when sensor are changed]
        sensor_senstivity = 50  # This senstivity value is 731 sensor used

        # 1mT = 10 Gauss
        # mT = mT * 10 Gauss
        # Gauss to magnetization: Gauss * 0.079

        multiply_by_factor_magnetization = (((( mean_row_wise_dataframe / sensor_max_value) * sensor_voltage_level) / sensor_senstivity) * 10) * 0.079

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[self.index_tab_m, oddometer], y=multiply_by_factor_magnetization))
        fig.update_xaxes(
            tickfont=dict(size=11),
            dtick=500,
            title_text="Absolute Distance(m))",
            tickangle=0, showticklabels=True, ticklen=0)
        fig.update_yaxes(
            title_text="Magnetization",
        )
        fig.update_layout(
            # dragmode='select',
            # width=1300,  # Set the width of the figure
            # height=300,  # Set the height of the figure
            title='Magnetization Graph'
        )

        self.config.print_with_time("End of conversion at : ")
        html_path = gmfl_path("h_magnetization.html")
        print(f"magnwtizatoion path : {html_path}")
        pio.write_html(fig, file=html_path, auto_open=False)
        # self.m_output_graph.load(QUrl.fromLocalFile(html_path))

        return html_path