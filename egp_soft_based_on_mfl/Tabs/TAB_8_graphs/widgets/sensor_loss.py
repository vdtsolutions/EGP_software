from google.cloud import bigquery
import json
from pathlib import Path
import os
import plotly.io as pio
import plotly.graph_objs as go
from PyQt5.QtCore import QUrl
# from GMFL_12_Inch_Desktop.Components.self.configs import self.config as self.config
#
#
# connection = self.config.connection
# company_list = []  # list of companies
# credentials = self.config.credentials
# project_id = self.config.project_id
# client = bigquery.Client(credentials=credentials, project=project_id)
# self.config = json.loads(open(r'D:\Anubhav\vdt_backend\GMFL_12_Inch_Desktop\utils\proximity_base_value.json').read())

# Dynamically locate the GMFL root (2 levels above this file)
GMFL_ROOT = Path(__file__).resolve().parents[3]


def gmfl_path(relative):
    """Return absolute path inside GMFL backend_data/temp folder."""
    temp_dir = GMFL_ROOT / "backend_data" / "data_generated" / "temp"
    os.makedirs(temp_dir, exist_ok=True)  # make sure folder exists
    return str(temp_dir / relative)


def Sensor_loss(self):
    print("hii")
    weld_id_1 = self.combo_graph.currentText()
    self.weld_id_1 = int(weld_id_1)
    runid = self.parent.runid
    self.runid = self.parent.runid
    with self.config.connection.cursor() as cursor:
        # query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
        query = "SELECT start_index, end_index,start_oddo1,end_oddo1 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"
        cursor.execute(query, (self.runid, self.weld_id_1, self.runid, self.weld_id_1))
        result = cursor.fetchall()
        start_oddo1 = result[0][2]
        end_oddo1 = result[1][3]

        start_index, end_index = result[0][0], result[1][1]
        print(start_index, end_index)

        self.config.print_with_time("Start fetching at : ")
        query_for_start = 'SELECT ODDO1 FROM ' + self.config.table_name + ' WHERE index>{} AND index<{} order by index'
        query_job = self.config.client.query(query_for_start.format(start_index, end_index))
        results = query_job.result().to_dataframe()

        results['ODDO1'] = ((results['ODDO1'] - self.config.oddo1) / 1000).round(3)
        self.config.print_with_time("End fetching at : ")

        x_labels = results['ODDO1'].astype(str)
        fig = go.Figure()

        # Add a blank trace
        fig.add_trace(go.Scatter(x=x_labels, y=[None] * len(x_labels), mode='lines'))

        # Update x and y axes
        fig.update_xaxes(
            tickfont=dict(size=11),
            title_text="Absolute Distance(m)",
            tickangle=270, showticklabels=True, ticklen=0,
            showgrid=False,
            # dtick=300
        )
        fig.update_yaxes(
            tickfont=dict(size=11),
            title_text="Signal Loss (%)",
            range=[0, 100],
            dtick=10,
            # showgrid=False,
        )

        # Update layout
        fig.update_layout(
            # width=1300,  # Set the width of the figure
            # height=300,  # Set the height of the figure
            title="Sensor Loss Profile"
        )

        # pio.write_html(fig, file='h_sensor_loss.html', auto_open=False)
        # file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "h_sensor_loss.html"))
        # self.m_output_graph.load(QUrl.fromLocalFile(file_path))

        self.config.print_with_time("End of conversion at : ")
        html_path = gmfl_path("h_sensor_loss.html")
        print(f"sensor loss path : {html_path}")
        pio.write_html(fig, file=html_path, auto_open=False)
        self.m_output_graph.load(QUrl.fromLocalFile(html_path))