from google.cloud import bigquery
from PyQt5 import QtWidgets
import json
# from GMFL_12_Inch_Desktop.Components.Configs import config as config


# connection = config.connection
# credentials = config.credentials
# project_id = config.project_id
# client = bigquery.Client(credentials=credentials, project=project_id)
# config = json.loads(open('./utils/proximity_base_value.json').read())





def basevalue(self):
    # Ensure a rectangle has been drawn
    if self.rect_start_1 is None or self.rect_end_1 is None:
        QtWidgets.QMessageBox.warning(
            self.tab_line1, 'Invalid Input',
            'Select RectangleSelection of Marking, then press the button for base value'
        )
        return

    # Convert float coords -> integer indices, normalize order
    i0 = int(round(self.rect_start_1[0]))
    i1 = int(round(self.rect_end_1[0]))
    if i0 > i1:
        i0, i1 = i1, i0

    # Clamp to valid range
    index_chart = self.index.tolist()
    n = len(index_chart)
    if n == 0:
        QtWidgets.QMessageBox.warning(self.tab_line1, 'No Data', 'Index array is empty.')
        return

    i0 = max(0, min(n - 1, i0))
    i1 = max(0, min(n - 1, i1))
    if i0 == i1:
        QtWidgets.QMessageBox.warning(self.tab_line1, 'Invalid Selection', 'Selection is too small.')
        return

    start_counter = index_chart[i0]
    end_counter = index_chart[i1]

    runid = self.parent.runid
    weld_id = self.parent.weld_id

    # Query mean of all F*H* columns across the selected window
    # query_for_start = (
    #         'SELECT F1H1, F1H2, F1H3, F1H4, F2H1, F2H2, F2H3, F2H4, '
    #         'F3H1, F3H2, F3H3, F3H4, F4H1, F4H2, F4H3, F4H4, '
    #         'F5H1, F5H2, F5H3, F5H4, F6H1, F6H2, F6H3, F6H4, '
    #         'F7H1, F7H2, F7H3, F7H4, F8H1, F8H2, F8H3, F8H4, '
    #         'F9H1, F9H2, F9H3, F9H4, F10H1, F10H2, F10H3, F10H4, '
    #         'F11H1, F11H2, F11H3, F11H4, F12H1, F12H2, F12H3, F12H4, '
    #         'F13H1, F13H2, F13H3, F13H4, F14H1, F14H2, F14H3, F14H4, '
    #         'F15H1, F15H2, F15H3, F15H4, F16H1, F16H2, F16H3, F16H4, '
    #         'F17H1, F17H2, F17H3, F17H4, F18H1, F18H2, F18H3, F18H4, '
    #         'F19H1, F19H2, F19H3, F19H4, F20H1, F20H2, F20H3, F20H4, '
    #         'F21H1, F21H2, F21H3, F21H4, F22H1, F22H2, F22H3, F22H4, '
    #         'F23H1, F23H2, F23H3, F23H4, F24H1, F24H2, F24H3, F24H4, '
    #         'F25H1, F25H2, F25H3, F25H4, F26H1, F26H2, F26H3, F26H4, '
    #         'F27H1, F27H2, F27H3, F27H4, F28H1, F28H2, F28H3, F28H4, '
    #         'F29H1, F29H2, F29H3, F29H4, F30H1, F30H2, F30H3, F30H4, '
    #         'F31H1, F31H2, F31H3, F31H4, F32H1, F32H2, F32H3, F32H4, '
    #         'F33H1, F33H2, F33H3, F33H4, F34H1, F34H2, F34H3, F34H4, '
    #         'F35H1, F35H2, F35H3, F35H4, F36H1, F36H2, F36H3, F36H4 '
    #         "FROM " + Config.table_name + " WHERE index>{} AND index<{} ORDER BY index"
    # )
    query_for_start = (
            "SELECT "
            + self.config.sensor_str_hall +
            " FROM "
            + self.config.table_name +
            " WHERE index>{} AND index<{} ORDER BY index"
    )
    query_job = self.config.client.query(query_for_start.format(start_counter, end_counter))
    # mean over window -> Series of length 144 (36*4)
    results = query_job.result().to_dataframe().mean()

    if results is None or results.empty:
        QtWidgets.QMessageBox.warning(self.tab_line1, 'No Data', 'No rows found in the selected range.')
        return

    base_value_each_pipe = results.to_list()
    if len(base_value_each_pipe) != self.config.num_of_sensors:
        QtWidgets.QMessageBox.warning(
            self.tab_line1, 'Unexpected Shape',
            f'Expected {self.config.num_of_sensors} values, got {len(base_value_each_pipe)}.'
        )
        return

    # Build INSERT programmatically so columns == values (no 1136 error)
    # Columns order matches the SELECT above: F1H1..F36H4
    cols_list = [f"F{i}H{h}" for i in range(1, self.config.F_columns + 1) for h in range(1, 5)]
    insert_cols = ["runid", "pipe_id"] + cols_list
    params = [runid, weld_id] + base_value_each_pipe

    placeholders = ", ".join(["%s"] * len(insert_cols))
    insert_sql = f"INSERT INTO base_value ({', '.join(insert_cols)}) VALUES ({placeholders})"

    try:
        with self.config.connection.cursor() as cursor:
            cursor.execute(insert_sql, params)
        self.config.connection.commit()
    except Exception as e:
        QtWidgets.QMessageBox.critical(
            self.tab_line1, 'DB Error',
            f'Failed to insert base values:\n{e}'
        )
        return

    QtWidgets.QMessageBox.information(self.tab_line1, 'Success', 'Data saved')