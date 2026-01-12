from google.cloud import bigquery
import json
from pathlib import Path
import os
import pandas as pd
import plotly.io as pio
import plotly.graph_objs as go
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


def Velocity(self, pipe_id):
    # print("hii")
    # weld_id_1 = self.parent.combo_graph.currentText()
    weld_id_1 = pipe_id
    self.weld_id_1 = int(weld_id_1)
    runid = self.parent.parent.runid
    self.runid = self.parent.parent.runid
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
        query_for_start = 'SELECT index,ODDO1,ODDO2 FROM ' + self.config.table_name + ' WHERE index>{} AND index<{} order by index'
        query_job = self.config.client.query(query_for_start.format(start_index, end_index))
        results = query_job.result().to_dataframe()

        results['ODDO1'] = (results['ODDO1'] - self.config.oddo1) / 1000
        self.config.print_with_time("End fetching at : ")

        # filtered_df = results[(results['index'] >= start_index) & (results['index'] <= end_index)].copy()
        results['Seconds'] = ((results['index'] - start_index) // 150) + 1

        unique_seconds = results['Seconds'].unique()
        velocity_results = []

        for sec in unique_seconds:
            rows = results[results['Seconds'] == sec]
            # print(rows)
            if not rows.empty:
                start = rows.iloc[0]['ODDO1']
                end = rows.iloc[-1]['ODDO1']
                occurrences = len(rows)
                velo_result = (end - start) / (0.1)
                velocity_results.append(
                    {'Seconds': sec, 'Start_oddo1': start, 'End_oddo1': end, 'Occurrences': occurrences,
                     'Result': velo_result})

        velocity_results_df = pd.DataFrame(velocity_results)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[velocity_results_df.index, round(velocity_results_df['Start_oddo1'], 3)],
                                 y=velocity_results_df['Result'], mode='lines', line=dict(color='blue')))

        # k = []
        # for i in range(len(results['ODDO1']) - 1):
        #     t = results['ODDO1'][i + 1] - results['ODDO1'][i]
        #     speed = t / 0.000666667
        #     k.append(speed)
        # last_value = k[-1]
        # k.append(last_value)
        # results['speed'] = k
        # oddometer = results['ODDO1'].round(2)
        # fig = go.Figure()
        # fig.add_trace(go.Scatter(x=[results.index, oddometer], y=results['speed'],line=dict(shape='spline')))

        fig.update_xaxes(
            tickfont=dict(size=11),
            dtick=5,
            title_text="Absolute Distance(m)",
            # showgrid=False,
            tickangle=0, showticklabels=True, ticklen=0
        )
        fig.update_yaxes(
            # range=[0,4],
            title_text="Speed(m/s)",
            # showgrid=False,
        )
        fig.update_layout(
            # dragmode='select',
            # width=1500,  # Set the width of the figure
            # height=400,  # Set the height of the figure
            title='Velocity Profile',
            xaxis=dict(title='Absolute Distance(m)'),
            yaxis=dict(title='Velocity (m/s)', range=[0, 3]),
        )

        # pio.write_html(fig, file='h_velocity.html', auto_open=False)
        # file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "h_velocity.html"))
        # self.m_output_graph.load(QUrl.fromLocalFile(file_path))
        self.config.print_with_time("End of conversion at : ")
        html_path = gmfl_path("h_velocity.html")
        print(f"velocity path : {html_path}")
        pio.write_html(fig, file=html_path, auto_open=False)
        # self.m_output_graph.load(QUrl.fromLocalFile(html_path))

        return html_path