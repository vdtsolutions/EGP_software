def Sensor_loss(self):
    print("hii")
    weld_id_1 = self.combo_graph.currentText()
    self.weld_id_1 = int(weld_id_1)
    runid = self.runid
    with connection.cursor() as cursor:
        # query = "SELECT start_index,end_index FROM pipes where runid=" + str(runid) + " and id=" + str(pipe_id)
        query = "SELECT start_index, end_index,start_oddo1,end_oddo1 FROM welds WHERE runid=%s AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)) ORDER BY id"
        cursor.execute(query, (self.runid, self.weld_id_1, self.runid, self.weld_id_1))
        result = cursor.fetchall()
        start_oddo1 = result[0][2]
        end_oddo1 = result[1][3]

        start_index, end_index = result[0][0], result[1][1]
        print(start_index, end_index)

        config.print_with_time("Start fetching at : ")
        query_for_start = 'SELECT ODDO1 FROM ' + config.table_name + ' WHERE index>{} AND index<{} order by index'
        query_job = client.query(query_for_start.format(start_index, end_index))
        results = query_job.result().to_dataframe()

        results['ODDO1'] = ((results['ODDO1'] - config.oddo1) / 1000).round(3)
        config.print_with_time("End fetching at : ")

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

        pio.write_html(fig, file='h_sensor_loss.html', auto_open=False)
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "h_sensor_loss.html"))
        self.m_output_graph.load(QUrl.fromLocalFile(file_path))

def Temperature_profile(self):
    print("hi")



def degrees_to_hours_minutes(self, degrees):
    if (degrees < 0):
        degrees = degrees % 360
    elif degrees >= 360:
        degrees %= 360
    degrees_per_second = 360 / (12 * 60 * 60)
    total_seconds = degrees / degrees_per_second
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{hours:02d}:{minutes:02d}"

def Roll_Calculation(self, df_hall, roll):
    first_key_values = roll
    roll_dictionary = {'1': first_key_values}
    angle = [round(i*2.5, 1) for i in range(0, 144)]

    for i in range(2, 145):
        current_values = [round((value + angle[i - 1]), 2) for value in first_key_values]
        roll_dictionary['{}'.format(i)] = current_values

    clock_dictionary = {}
    for key in roll_dictionary:
        clock_dictionary[key] = [self.degrees_to_hours_minutes(value) for value in roll_dictionary[key]]

    Roll_hr = pd.DataFrame(clock_dictionary)
    df_hall.reset_index(inplace=True, drop=True)
    # df_hall.reset_index(inplace=True, drop=True)
    k=(df_hall.transpose()).astype(float)
    k.reset_index(inplace=True, drop=True)

    # Roll_hr = Roll_hr.rename(columns=dict(zip(Roll_hr.columns, df_hall.columns)))

    time_list = [timedelta(minutes=i * 5) for i in range(144)]
    time_ranges_2 = [(datetime.min + t).strftime('%H:%M') for t in time_list]

    def create_time_dict():
        time_dict = {key: [] for key in time_ranges_2}
        return time_dict

    def check_time_range(time_str):
        start_time = time_ranges_2[0]
        end_time_dt = datetime.strptime(time_ranges_2[1], '%H:%M') - timedelta(seconds=1)
        end_time = end_time_dt.strftime('%H:%M')

        time_to_check = datetime.strptime(time_str, '%H:%M')
        start_time_dt = datetime.strptime(start_time, '%H:%M')

        if start_time_dt <= time_to_check <= end_time_dt:
            return True
        else:
            return False

    time_dict_1 = create_time_dict()
    rang = list(time_dict_1.keys())

    for index, row in Roll_hr.iterrows():
        xl = list(row)
        xd = dict(row)
        xkeys = list(xd.keys())
        c = 0
        for s, d in xd.items():
            if check_time_range(d):
                # print(s,d)
                ind = xl.index(d)
                # print(ind)
                y = xl[ind:] + xl[:ind]
                break

        curr = ind
        # ck = xkeys[curr]
        while True:
            ck = xkeys[curr]
            time_dict_1[rang[c]].append((curr, ck, xd[ck]))
            c += 1
            curr = (curr + 1) % len(xkeys)
            if curr == ind:
                break

    map_ori_sens_ind = pd.DataFrame(time_dict_1)
    # print(map_ori_sens_ind)
    val_ori_sensVal = map_ori_sens_ind.copy()

    def extract_string(cell):
        return cell[1]

    val_ori_sensVal = val_ori_sensVal.applymap(extract_string)

    for r, e in val_ori_sensVal.iterrows():
        c = 0
        for col_name, tup_value in e.items():
            # print(r,col_name,tup_value)
            # cell_v = df_hall.at[r, tup_value]
            # print(cell_v)
            val_ori_sensVal.iloc[r, c] = tup_value
            c += 1
    return map_ori_sens_ind, val_ori_sensVal



def generate_report(self):
    Report.generate(self.project_name, self.runid)


def add_to_list(self):
    for i in company_list:
        self.left_listWidget.addItem(i)

def reset_defect(self):
    runid = self.runid
    self.defect_list = []
    self.GenerateGraph()

def add_defect(self):
    print("defect_list", self.defect_list)


def insert_and_update_defect_to_db(self, d_list, runid, pipe_id):
    for defect in d_list:
        print(defect)
        with config.connection.cursor() as cursor:
            query_weld_insert = "INSERT INTO defectdetail (runid, pipe_id, defect_length, defect_breadth, defect_angle,defect_depth,type,x,y,category,min,max) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

            # Execute query.
            b = cursor.execute(query_weld_insert, (
                int(runid), int(pipe_id), int(defect[2]), int(defect[3]), 0, 0, 'manual', int(defect[0]),
                int(defect[1]), 'unknown', 0.0, 0.0))
            if b:
                print("data is inserted successfully")
            else:
                print("data is not inserted successfully")
            config.connection.commit()
    return


def pip_info(self):
    try:
        config.print_with_time("pipe info method called")
        runid = str(self.runid)
        self.pipe_id = self.pipeLineNumberLineEdit.text()
        # # get the pipe_id from user and save that pipe_id for global use to be use by other functions and there value should be updated accordingly
        with connection.cursor() as cursor:
            # SQL
            Fetch_pipe_record = "select runid,analytic_id,pipe_id,pipe_start_filename,pipe_start_serialno," \
                                "pipe_end_filename,pipe_end_serialno from pipedetail where runid='%s' and " \
                                "pipe_id='%s' "
            # Execute query.
            cursor.execute(Fetch_pipe_record, (int(runid), int(self.pipe_id)))
            fetched_data = cursor.fetchall()
            print(fetched_data)
            connection.commit()
            if fetched_data:
                path = './Data Frames/' + self.project_name + '/' + self.pipe_id + '.pkl'
                print(path)
                if os.path.isfile(path):
                    config.print_with_time("File exist")
                    self.df_pipe = pd.read_pickle(path)
                else:
                    config.print_with_time("File not exist")
                    try:
                        os.mkdir('./Data Frames/' + self.project_name)
                    except:
                        config.print_with_time("Folder already exists")

                    pipe_start_file = fetched_data[0][3]
                    pipe_start_serial = fetched_data[0][4]
                    pipe_end_file = fetched_data[0][5]
                    pipe_end_serial = fetched_data[0][6]
                    query = 'select * from ' + config.table_name + ' where filename>={} and Serialno>={} and filename<={} and Serialno<={} and runid={} ORDER BY filename, Serialno'
                    query_job = client.query(
                        query.format(pipe_start_file, pipe_start_serial, pipe_end_file, pipe_end_serial, runid))
                    print(query.format(pipe_start_file, pipe_start_serial, pipe_end_file, pipe_end_serial, runid))
                    self.df_pipe = query_job.to_dataframe()
                    config.print_with_time("conversion to data frame is done")
                    self.df_pipe.to_pickle(path)
                    config.print_with_time("successfully  saved to pickle")
                # self.df_pipe.to_csv('recods.csv)
                config.info_msg("Data Successfully Loaded", "")
                # self.pre_graph_analysis()
            else:
                config.warning_msg("Data not Found", "")
    except OSError as error:
        config.warning_msg(OSError or "Network speed is very slow or invalid Pipe id", "")
        # logger.log_error(error or "Set_msg_body method failed with unknown Error")
        pass


def merge_pipe(self, runid):
    with connection.cursor() as cursor:
        Fetch_pipe_record = "select pipe_length,pipe_id,pipe_start_filename," \
                            "pipe_end_filename from pipes where runid='%s'"
        cursor.execute(Fetch_pipe_record, (int(runid)))
        fetched_data = cursor.fetchall()
        for i, elem in enumerate(fetched_data):
            pass