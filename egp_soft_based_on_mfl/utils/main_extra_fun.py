class WatermarkWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #f2f2f2;")  # grey background
        self.watermark = QtGui.QPixmap(r"F:\work_new\backend_software\GMFL_12_Inch_Desktop\utils\Picture1.png")  # apne image ka path daalo

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.08)  # transparency (adjust karo)

        # Center me watermark draw karo
        x = (self.width() - self.watermark.width()) / 2
        y = (self.height() - self.watermark.height()) / 2
        painter.drawPixmap(int(x), int(y), self.watermark)

def insert_weld_to_db(temp):
    #print("weld_obj", temp)
    """
        This will insert weld object to mysql database
        :param weld_obj : Object with value of  runid,analytic_id,sensitivity,start_index,end_index,start_oddo1,end_oddo1,start_oddo2,end_oddo2,length and weld_number
    """
    try:
        query_weld_insert = "INSERT INTO welds (weld_number,runid,start_index,end_index,type,analytic_id,sensitivity,length,start_oddo1,end_oddo1,start_oddo2,end_oddo2) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # print(runid, analytic_id, Sensitivity, start_file, end_file, start_sno, end_sno)
        with connection.cursor() as cursor:
            cursor.execute(query_weld_insert, (temp["weld_number"], temp["runid"], temp["start_index"], temp["end_index"], temp["type"], temp["analytic_id"], temp["sensitivity"], temp["length"], temp["start_oddo1"], temp["end_oddo1"], temp["start_oddo2"], temp["end_oddo2"]))
            connection.commit()
        return
    except:
        print("Error While Inserting weld for runid ")


def insert_pipe_to_db(pipe_obj):
    """
        This will insert pipe_obj to mysql database
        :param pipe_obj : object will value of runid,analytic_id,length,start_index and end_index
    """
    try:
        query = "INSERT INTO Pipes (runid,analytic_id,length,start_index,end_index) VALUE(%s,%s," \
                "%s,%s,%s) "
        with connection.cursor() as cursor:
            cursor.execute(query,
                           (pipe_obj["runid"], pipe_obj["analytic_id"], pipe_obj["length"], pipe_obj["start_index"],
                            pipe_obj["end_index"]))
            connection.commit()
        return
    except:
        print("Error While Inserting weld for runid ")


def get_last_pipe(runid, weld_obj, analytic_id):
    """
        This will return the last pipe object to insert into mysql db
        :param runid: Id of the Project
    """
    query = "SELECT index,oddo1,oddo2 FROM `" + config.table_name + "` order by index desc LIMIT 1 "
    query_job = client.query(query)
    results = query_job.result()
    for row in results:
        length = row['oddo1'] - weld_obj['end_oddo1']
        end_index = row['index']
        start_index = weld_obj['end_index']
        end_index = row['index']
        obj = {"start_index": start_index, "end_index": end_index, "length": length, "analytic_id": analytic_id,
               "runid": runid}
        return obj


def ranges(nums):
    #print("nums",nums)
    """"
       This will merge the continues indexes and return a list that will contain list of start_index and end_index
           :param arr : List of indexes to merge
       """
    # gaps_bw_two_value=3
    # sequences = np.split(nums, np.array(np.where(np.diff(nums) > gaps_bw_two_value)[0]) + 1)
    # l = []
    # for s in sequences:
    #     if len(s) > 1:
    #         l.append((np.min(s), np.max(s)))
    #     else:
    #         pass
    #         #l.append(s[0])
    # return l

    try:
        gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s + 1 < e]
        edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
        return list(zip(edges, edges))
    except:
        print("Error while Grouping Index Range for defect")


def index_of_occurrences(arr, value):
    #print(arr)
    for i, data in enumerate(arr):
        if i == 128:
            arr[i] = 0
        elif i == 129:
            arr[i] = 0
        elif i == 130:
            arr[i] = 0
        elif i == 131:
            arr[i] = 0
    #print(arr)
    return [i for i, x in enumerate(arr) if x != 0]


def dimension_classification(type_of_defect, runid, defect_id):
    print(type_of_defect, runid)
    query = f'UPDATE finaldefect SET  Dimensions_classification="{type_of_defect}" WHERE runid="{runid}" and id={defect_id}'
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()

def get_type_defect(geometrical_parameter, runid):
    print(geometrical_parameter, runid)
    with connection.cursor() as cursor:
        try:
            Fetch_defect_detail = "select Length, Width, id from finaldefect where runid='%s'"
            cursor.execute(Fetch_defect_detail, (int(runid)))
            allSQLRows = cursor.fetchall()
            print("dhhdhf", allSQLRows)
            for i in allSQLRows:
                length_defect = i[0]
                width_defect = i[1]
                defect_id = i[2]
                L_ratio_W = length_defect / width_defect
                if width_defect >= 3 * geometrical_parameter and length_defect >= 3 * geometrical_parameter:
                    type_of_defect = 'GENERAL'
                elif (
                        6 * geometrical_parameter > width_defect >= 1 * geometrical_parameter and 6 * geometrical_parameter > length_defect >= 1 * geometrical_parameter) and (
                        0.5 < (L_ratio_W) < 2) and not (
                        width_defect >= 3 * geometrical_parameter and length_defect >= 3 * geometrical_parameter):
                    type_of_defect = 'PITTING'
                elif (1 * geometrical_parameter <= width_defect < 3 * geometrical_parameter) and (L_ratio_W >= 2):
                    type_of_defect = 'AXIAL GROOVING'
                elif L_ratio_W <= 0.5 and 3 * geometrical_parameter > length_defect >= 1 * geometrical_parameter:
                    type_of_defect = 'CIRCUMFERENTIAL GROOVING'
                elif 0 < width_defect < 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
                    type_of_defect = 'PINHOLE'
                elif 0 < width_defect < 1 * geometrical_parameter and length_defect >= 1 * geometrical_parameter:
                    type_of_defect = 'AXIAL SLOTTING'
                elif width_defect >= 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
                    type_of_defect = 'CIRCUMFERENTIAL SLOTTING'
                dimension_classification(type_of_defect, runid, defect_id)
        except:
            # logger.log_error("type of defect is not permissiable value")
            pass

def extract_raw_defects(arr):
    #print(arr)
    list_of_raw_defect = []
    temp_list = []
    for i, row in enumerate(arr):
        #print(row)
        if len(row) > 0:
            temp_list.append(i)
        elif len(temp_list) > 0:
            list_of_raw_defect.append({"start": temp_list[0], "end": temp_list[-1]})
            temp_list = []

    if len(temp_list) > 0:
        list_of_raw_defect.append({"start": temp_list[0], "end": temp_list[-1]})
        temp_list = []
    return list_of_raw_defect


def calculate_defect(raw_defects, pipe_data, number_of_sensor=144):
    # TODO pass number of sensor
    start = raw_defects["start"]
    end = raw_defects["end"]
    sensor_index = []
    for i in range(number_of_sensor):
        flag = False
        for row in pipe_data[start:end + 1]:
            if (row[i] != 0 and row[i]>0):
                flag = True
                break
        if flag:
            sensor_index.append(i)
    defects = []
    index_list = ranges(sensor_index)
    #print(index_list)
    for row in index_list:
        defects.append(
            {"start_observation": start, "end_observation": end, "start_sensor": row[0], "end_sensor": row[1]})
    return defects
    #print("hii")


def defect_length_calculator(df_new_proximity, data, defects, oddo1, oddo2, roll, runid, column_means):
    finial_defect_list = []
    defect_angle = []
    for i, defect in enumerate(defects):
        start, end, start_sensor, end_sensor = defect["start_observation"], defect["end_observation"], defect["start_sensor"], defect["end_sensor"]
        """
        Calculate in 12 inch MFL Tool
        """
        if start_sensor == end_sensor:
            pass
        else:
            print("..................................................")
            print("start-end observation",start,end)
            print("start-end sensor", start_sensor, end_sensor)

            """
            Calculate Upstream of the defect
            """
            upstream_odd2 = oddo2[end]-oddo2[0]
            #print("upstream_odd2....", upstream_odd2)

            upstream_odd1 = oddo1[end]-oddo1[0]
            #print("upstream_odd1....", upstream_odd1)


            """
            Calculate length and absolute distance of the defect
            """

            length = oddo2[end] - oddo2[start]

            absolute_length = oddo2[start]
            #print("absolute_distance_oddo2....", absolute_length)

            length1 = oddo1[end]-oddo1[start]
            absolute_length_1 = oddo1[start]
            #print("absolute_length_oddo1....", absolute_length_1)

            """
            Calculate latitude and longitude 
            """
            long, lat = lat_long(absolute_length_1, runid)
            print("latitude", lat)
            print("longitude", long)

            """
            Calculate Pipe_Thickness 
            """
            # pipethickness = pipethick(config)

            pipethickness = config.pipe_thickness

            """
            Calculate breadth of the defect
            """

            # def breadth():
            #     start_sensor1 = start_sensor+1
            #     end_sensor1 = end_sensor+1
            #     if start_sensor1 > end_sensor1:
            #         bredth = 0
            #         return bredth
            #
            #     else:
            #         if start_sensor1 == end_sensor1:
            #             bredth = 0
            #             return bredth
            #         else:
            #             outer_diameter_1 = 324  ############## outer_diametere 324 for 12 inch GMFL
            #             thickness_1 = 7.1  ################# each pipe thickness can be change old thickness 7.1 ############
            #             inner_diameter_1 = outer_diameter_1 - 2 * (thickness_1)
            #             radius_1 = inner_diameter_1 / 2
            #
            #             theta_2 = 1.74 ############ sensor to sensor  angle = 1.96 #########
            #             c_1 = math.radians(theta_2)  ########### c in calculated in radians ########
            #             theta_3 = 5.63  ########## flapper to flapper angle =10.61 ########
            #             d_1 = math.radians(theta_3)  ########### d in calculated in radians #####
            #
            #             x1 = radius_1 * c_1
            #             y1 = radius_1 * d_1
            #             count = 0
            #             if start_sensor1 == end_sensor1:
            #                 bredth = 0
            #                 return bredth
            #             else:
            #                 for i in range(start_sensor1, end_sensor1):
            #                     if i % 16 == 0:
            #                         count = count + 1
            #                         k = (y1 - x1) * count
            #                     else:
            #                         pass
            #                 try:
            #                     l = (end_sensor1 - start_sensor1) * x1
            #                     bredth = k + l
            #                     return bredth
            #                 except:
            #                     k = 0
            #                     l = (end_sensor1 - start_sensor1) * x1
            #                     bredth = k + l
            #                     return bredth


            """
            Calculate depth of the defect
            """
            if (absolute_length > 0):
                max_value_list, data_observation, data1, a, b = defect_max(data, start, end, start_sensor, end_sensor)
                #print("data_observation",data_observation)
                print("max_value_list....", max_value_list)
                #print("data observation",data_observation[0])
                """
                First row get start observation to end observation
                """
                #initial_observation_1 = data_observation[0]
                # initial_observation = []
                # for b in initial_observation_1:
                #     initial_observation.append(abs(b))
                # print("initial_observation", initial_observation)
                initial_observation_1 = [0 if k1 < 0 else k1 for k1 in data_observation[0]]
                #
                #
                # kx = []
                # for i2 in range(0, 128):
                #     if i2 >= a and i2 <= b:
                #         kx.append(initial_observation_1[i2])
                #     else:
                #         kx.append(0)
                #print("initial_observation", kx)

                """
                Difference between max_value_list and initial_observation
                """
                zip_object = zip(max_value_list, initial_observation_1)
                difference_list = []
                for list1_i, list2_i in zip_object:
                    difference_list.append(list1_i - list2_i)

                difference_list_1 = [0 if k2 < 0 else k2 for k2 in difference_list]
                print("difference_list1", difference_list_1)
                """
                Get max_value_difference_value
                """

                max_value_difference_value = max(difference_list_1)
                if max_value_difference_value == 0:
                    max_value = max(max_value_list)
                    max_value_difference_index = max_value_list.index(max_value)
                    print("max_value", max_value)
                    print("max_value_index", max_value_difference_index)
                else:
                    """
                    Get index max_value_difference_value
                    """
                    max_value_difference_index = difference_list.index(max_value_difference_value)
                    print("max_value_index", max_value_difference_index)
                    """
                    Check max_value_list inside the index and get max_value
                    """
                    max_value = max_value_list[max_value_difference_index]
                    print("max_value", max_value)

                    result = []
                    for sub_list in data1:
                        try:
                            result.append(sub_list[max_value_difference_index])
                        except IndexError:
                            result.append(None)
                    print("result....", result)


                    q1, q3 = np.percentile(result, [25, 25])
                    print("q1 q3", q1, q3)
                    start_point = np.argmax(result > q1)
                    end_point = len(result) - np.argmax(result[::-1] > q3) - 1

                    index_left_center = start_point + start
                    index_right_center = end_point + start
                    oddo_updated_left = oddo1[index_left_center]
                    oddo_updated_right = oddo1[index_right_center]

                    print("start_point", start_point)
                    print("end_point", end_point)
                    print("index_left_center", index_left_center)
                    print("index_right_center", index_right_center)
                    print("oddo_updated_left", oddo_updated_left)
                    print("oddo_updated_right", oddo_updated_right)

                    length = oddo_updated_right - oddo_updated_left
                    print("length_latest", length)

                    left_value = result[start_point]
                    right_value = result[end_point]
                    new_value = min(left_value, right_value)

                    def width_new():
                        first_sensor = None
                        last_sensor = None
                        for index in range(start_sensor, end_sensor + 1):
                            if new_value < max_value_list[index]:
                                first_sensor = index if first_sensor is None else first_sensor
                                last_sensor = index

                        print("left_value", left_value)
                        print("right_value", right_value)
                        print("new_value", new_value)
                        print("first_sensor", first_sensor)
                        print("last_sensor", last_sensor)

                        outer_diameter_1 = 324  ############## outer_diametere 324 for 12 inch GMFL
                        thickness_1 = config.pipe_thickness  ################# each pipe thickness can be change old thickness 7.1 ############
                        inner_diameter_1 = outer_diameter_1 - 2 * (thickness_1)
                        radius_1 = inner_diameter_1 / 2

                        theta_2 = 1.73 ############ sensor to sensor  angle = 1.73 #########
                        c_1 = math.radians(theta_2)  ########### c in calculated in radians ########
                        theta_3 = 4.52  ########## flapper to flapper angle = 4.52 ########
                        d_1 = math.radians(theta_3)  ########### d in calculated in radians #####

                        x1 = radius_1 * c_1
                        y1 = radius_1 * d_1
                        count = 0
                        if first_sensor == last_sensor:
                            breadth = 0
                            return breadth

                        else:
                            for i in range(first_sensor, last_sensor):
                                if i % 4 == 0:
                                    count = count + 1
                                    k = (y1 - x1) * count
                                else:
                                    pass
                            try:
                                l = (last_sensor - first_sensor) * x1
                                breadth = k + l
                                return breadth
                            except:
                                k = 0
                                l = (last_sensor - first_sensor) * x1
                                breadth = k + l
                                return breadth

                    """
                    Calculate new_depth of the defect

                    """
                    print("column_means", column_means)
                    base_value = column_means[max_value_difference_index]
                    try:
                        depth_val = (length / width_new()) * (max_value / base_value)

                        ############ For pipe thickness 7.5 #############
                        depth = round(((depth_val * 100) / config.pipe_thickness), 2)

                        ############ For pipe thickness 12.7 #############
                        # depth = round(((depth_val * 100)/12.7), 2)

                    except:
                        depth = float(0)

                    print("base_value", base_value)
                    print("depth", depth)

                    # def evaluate_polynomial(coefficients, x):
                    #     degree = len(coefficients) - 1
                    #     result_len = 0
                    #     for i in range(degree + 1):
                    #         result_len += coefficients[i] * (x ** (degree - i))
                    #     return int(result_len)

                    # ans_len = 0
                    # bredth = width_new()
                    # new_width = 0
                    # ans_depth = 0
                    #
                    ############# Coefficients of LENGTH for pipe thickness 7.4 ###############
                    # if int(length) <= 40 and int(length) >= 5:
                    #     coefficients = [4.72105390e-03, -3.47983873e-01, 8.09750603e+00, -2.56608581e+01]
                    #     # coefficients = [-1.11935387e-04, 1.13040083e-02, -4.15230050e-01, 6.81264193e+00, -4.67619456e+01, 1.18910052e+02]
                    #     ans_len =evaluate_polynomial(coefficients, int(length))
                    # elif int(length) > 40:
                    #     coefficients = [-2.28129067e-04, 4.01204794e-02, -1.31715742e+00, 3.78883022e+01]
                    #     # coefficients = [9.25350782e-10, 1.28969128e-07, 1.73778075e-05, 2.21800972e-03, 2.51147511e-01, 2.25391375e+01]
                    #     ans_len =evaluate_polynomial(coefficients, int(length))
                    # else:
                    #     ans_len = int(length)

                    ############# Coefficients of LENGTH for pipe thickness 12.7 ##############
                    # if int(length) <= 40 and int(length) >= 5:
                    #     coefficients = [4.72105390e-03, -3.47983873e-01, 8.09750603e+00, -2.56608581e+01]
                    #     # coefficients = [-1.11935387e-04, 1.13040083e-02, -4.15230050e-01, 6.81264193e+00, -4.67619456e+01, 1.18910052e+02]
                    #     ans_len =evaluate_polynomial(coefficients, int(length))
                    # elif int(length) > 40:
                    #     coefficients = [-2.28129067e-04, 4.01204794e-02, -1.31715742e+00, 3.78883022e+01]
                    #     # coefficients = [9.25350782e-10, 1.28969128e-07, 1.73778075e-05, 2.21800972e-03, 2.51147511e-01, 2.25391375e+01]
                    #     ans_len =evaluate_polynomial(coefficients, int(length))
                    # else:
                    #     ans_len = int(length)


                    ############# Coefficients of WIDTH for pipe thickness 7.4 ###############
                    # if int(bredth) <= 40 and int(bredth) >= 5:
                    #     coefficients = [4.72105390e-03, -3.47983873e-01, 8.09750603e+00, -2.56608581e+01]
                    #     # coefficients = [-1.11935387e-04, 1.13040083e-02, -4.15230050e-01, 6.81264193e+00, -4.67619456e+01, 1.18910052e+02]
                    #     new_width =evaluate_polynomial(coefficients, int(bredth))
                    # elif int(bredth) > 40:
                    #     coefficients = [-2.28129067e-04, 4.01204794e-02, -1.31715742e+00, 3.78883022e+01]
                    #     # coefficients = [9.25350782e-10, 1.28969128e-07, 1.73778075e-05, 2.21800972e-03, 2.51147511e-01, 2.25391375e+01]
                    #     new_width =evaluate_polynomial(coefficients, int(bredth))
                    # else:
                    #     new_width = int(bredth)

                    ############# Coefficients of WIDTH for pipe thickness 12.7 ##############
                    # if int(bredth) <= 40 and int(bredth) >= 5:
                    #     coefficients = [4.72105390e-03, -3.47983873e-01, 8.09750603e+00, -2.56608581e+01]
                    #     # coefficients = [-1.11935387e-04, 1.13040083e-02, -4.15230050e-01, 6.81264193e+00, -4.67619456e+01, 1.18910052e+02]
                    #     new_width =evaluate_polynomial(coefficients, int(bredth))
                    # elif int(length) > 40:
                    #     coefficients = [-2.28129067e-04, 4.01204794e-02, -1.31715742e+00, 3.78883022e+01]
                    #     # coefficients = [9.25350782e-10, 1.28969128e-07, 1.73778075e-05, 2.21800972e-03, 2.51147511e-01, 2.25391375e+01]
                    #     new_width =evaluate_polynomial(coefficients, int(bredth))
                    # else:
                    #     new_width = int(bredth)


                    ############# Coefficients of DEPTH for pipe thickness 7.4 ###############
                    # if int(depth) <= 40 and int(depth) >= 5:
                    #     coefficients = [4.72105390e-03, -3.47983873e-01, 8.09750603e+00, -2.56608581e+01]
                    #     # coefficients = [-1.11935387e-04, 1.13040083e-02, -4.15230050e-01, 6.81264193e+00, -4.67619456e+01, 1.18910052e+02]
                    #     ans_depth =evaluate_polynomial(coefficients, int(depth))
                    # elif int(depth) > 40:
                    #     coefficients = [-2.28129067e-04, 4.01204794e-02, -1.31715742e+00, 3.78883022e+01]
                    #     # coefficients = [9.25350782e-10, 1.28969128e-07, 1.73778075e-05, 2.21800972e-03, 2.51147511e-01, 2.25391375e+01]
                    #     ans_depth =evaluate_polynomial(coefficients, int(depth))
                    # else:
                    #     ans_depth = int(depth)

                    ############# Coefficients of DEPTH for pipe thickness 12.7 ##############
                    # if int(depth) <= 40 and int(depth) >= 5:
                    #     coefficients = [4.72105390e-03, -3.47983873e-01, 8.09750603e+00, -2.56608581e+01]
                    #     # coefficients = [-1.11935387e-04, 1.13040083e-02, -4.15230050e-01, 6.81264193e+00, -4.67619456e+01, 1.18910052e+02]
                    #     ans_depth =evaluate_polynomial(coefficients, int(depth))
                    # elif int(depth) > 40:
                    #     coefficients = [-2.28129067e-04, 4.01204794e-02, -1.31715742e+00, 3.78883022e+01]
                    #     # coefficients = [9.25350782e-10, 1.28969128e-07, 1.73778075e-05, 2.21800972e-03, 2.51147511e-01, 2.25391375e+01]
                    #     ans_depth =evaluate_polynomial(coefficients, int(depth))
                    # else:
                    #     ans_depth = int(depth)


                    # print("new length", ans_len)
                    # print("new width", new_width)
                    # print("new depth", ans_depth)


                each_holl_sensor = []
                for i in range(len(data1)):
                    """
                    Retrieving column data using sensor no or max_value_difference_index
                    """
                    each_holl_sensor.append(abs(data1[i][max_value_difference_index]))

                """
                Match index list
                """
                max_value_observation_index = []
                for j, match_data_value in enumerate(each_holl_sensor):
                    """
                    Retrieving index match the max_value and match_data_value
                    """
                    if match_data_value == max_value:
                        max_value_observation_index.append(j)
                    """
                    Index list get first index
                    """
                # print("max_value_observation_index",max_value_observation_index[0])
                depth_percentage_higher_value = max_value
                print("depth_percentage_higher_value", depth_percentage_higher_value)
                roll_position = roll[max_value_observation_index[0]]
                # print(depth_percentage_higher_value)
                print("roll position", roll_position)

                #################### sensor number ##########
                sensor_number = max_value_difference_index
                sensor_number = sensor_number + 1
                #print("start sensor: end sensor", a, b)
                #print("maxiumum depth of the sensor", sensor_number)

                """
                Internal and External defect calculation
                """
                mean_of_pipe_wise = df_new_proximity.mean()
                #print("mean_of_pipe_wise.......",mean_of_pipe_wise)
                average_value_list = mean_of_pipe_wise.values.tolist()
                average_value_list = [float(s) for s in average_value_list]
                #print("average_value_list", average_value_list)
                list_2d = df_new_proximity.values.tolist()
                index_1 = 0
                compare_list_mean = []
                while (index_1 < len(list_2d[0])):
                    x2 = []
                    for j, value in enumerate(list_2d):
                        if list_2d[j][index_1] <= average_value_list[index_1]:
                            x2.append(list_2d[j][index_1])
                    index_1 = index_1 + 1
                    #print("greater than aur equel average value",x2)
                    mean_value_of_compare_list = mean(x2)
                    compare_list_mean.append(mean_value_of_compare_list)
                print("compare_list_of_mean", compare_list_mean)

                """
                Noise difference each proximity sensor
                """
                zip_object_2 = zip(average_value_list, compare_list_mean)
                noise_difference_list = []
                for list1_4, list2_5 in zip_object_2:
                    noise_difference_list.append(list1_4 - list2_5)
                print("noise_difference list", noise_difference_list)

                if sensor_number % 4 == 0:
                    flapper_no = int(sensor_number/4)
                else:
                    flapper_no = int(sensor_number/4)+1
                proximity_no = flapper_no % 4
                if proximity_no == 0:
                    proximity_no = 4
                proximity_index = 'F'+str(flapper_no)+'P'+str(proximity_no)
                #print("proximity_index",proximity_index)
                b = df_new_proximity[start:end]
                #print("start_end_dataframe",b)
                proximity_one_column = b[proximity_index]
                c = proximity_one_column.values.tolist()
                # initial=c[0]
                # print("initial",initial)
                minimum_value_proximity = min(c)
                #print("minimum_value_proximity",minimum_value_proximity)

                single_proximity_average_value = compare_list_mean[int(flapper_no-1)]
                #print("single_proximity_average_value",single_proximity_average_value)

                if single_proximity_average_value > minimum_value_proximity:
                    type = "Internal"
                else:
                    type = "External"
                """
                End of Internal and External Defect
                """

                """
                Calculate orienatation hr:min:sec
                """
                sensor = sensor_number
                x = 1.59  ###### sensor to sensor angle between(x) 2.52 ex:1-2,2-3,3-4,5-6,6-7,7-8 ######
                y = 1.44  ######### flapper first sensor to flapper second first sensor ex:4-5,8-9,12-13,16-17 #####
                z = 2.71  ######## second flapper to 3 flapper angle ###########
                a = 9.08  ##### arm to arm angle ##############################
                b = int(sensor / 16)
                c = b * a
                d = int(sensor / 8)
                e = d - b
                f = e * z
                g = int(sensor / 4)
                h = g - (b + e)
                k = h * y
                l = sensor * x

                initial_calculation_of_each_sensor = (c + f + k + l)

                if roll_position > 0:
                    roll_position = roll_position + initial_calculation_of_each_sensor
                    if roll_position > 360:
                        roll_position = roll_position % 360
                else:
                    roll_position = 360 + roll_position
                    roll_position = roll_position + initial_calculation_of_each_sensor
                    if roll_position > 360:
                        roll_position = roll_position % 360
                    # angle = initial_calculation_of_each_sensor + roll_position
                    # print("angle rotation",angle)
                # print("angle", roll_position)
                h = roll_position / 30
                k = int(h)
                m = roll_position % 30
                minute = round(m)
                g = ':'
                angle_hr_min = str(k) + g + str(minute)
                # print(angle_hr_min)
                """
                End of Orientation
                """
                finial_defect_list.append({**defect, "start_index_q1": index_left_center, "end_index_q2": index_right_center,
                                           "angle": roll_position, "depth": depth, "defect_type": type,
                                           "length": length, "breadth": width_new(), "absolute_distance": absolute_length,
                                           "length_odd1": length1, "absolute_distance_oddo1": absolute_length_1,
                                           "sensor_no": sensor_number, "angle_hr_m": angle_hr_min, "defect_classification": "ex",
                                           "latitude": lat, "longitude": long, "pipe_thickness": pipethickness,
                                           "upstream_oddo1": upstream_odd1, "upstream_oddo2": upstream_odd2}) # TODO calculate breadth(same flapper or not)
    return finial_defect_list


def pipethick(config):
    tup1 = (
        "F1H1", "F1H2", "F1H3", "F1H4", "F2H1", "F2H2", "F2H3", "F2H4", "F3H1", "F3H2", "F3H3", "F3H4", "F4H1", "F4H2",
        "F4H3", "F4H4",
        "F5H1", "F5H2", "F5H3", "F5H4", "F6H1", "F6H2", "F6H3", "F6H4", "F7H1", "F7H2", "F7H3", "F7H4", "F8H1", "F8H2",
        "F8H3", "F8H4",
        "F9H1", "F9H2", "F9H3", "F9H4", "F10H1", "F10H2", "F10H3", "F10H4", "F11H1", "F11H2", "F11H3", "F11H4", "F12H1",
        "F12H2", "F12H3", "F12H4",
        "F13H1", "F13H2", "F13H3", "F13H4", "F14H1", "F14H2", "F14H3", "F14H4", "F15H1", "F15H2", "F15H3", "F15H4",
        "F16H1", "F16H2", "F16H3", "F16H4",
        "F17H1", "F17H2", "F17H3", "F17H4", "F18H1", "F18H2", "F18H3", "F18H4", "F19H1", "F19H2", "F19H3", "F19H4",
        "F20H1", "F20H2", "F20H3", "F20H4",
        "F21H1", "F21H2", "F21H3", "F21H4", "F22H1", "F22H2", "F22H3", "F22H4", "F23H1", "F23H2", "F23H3", "F23H4",
        "F24H1", "F24H2", "F24H3", "F24H4",
        "F25H1", "F25H2", "F25H3", "F25H4", "F26H1", "F26H2", "F26H3", "F26H4", "F27H1", "F27H2", "F27H3", "F27H4",
        "F28H1", "F28H2", "F28H3", "F28H4",
        "F29H1", "F29H2", "F29H3", "F29H4", "F30H1", "F30H2", "F30H3", "F30H4", "F31H1", "F31H2", "F31H3", "F31H4",
        "F32H1", "F32H2", "F32H3", "F32H4"
        "F33H1", "F33H2", "F33H3", "F33H4", "F34H1", "F34H2", "F34H3", "F34H4", "F35H1", "F35H2", "F35H3", "F35H4",
        "F36H1", "F36H2", "F36H3", "F36H4")

#########################choose ###############################################################
    f = json.loads(open('E:/MFL_desktop_web/mfl_10_inch_desktop/utils/pipe_60_base.json').read())
    # g = json.loads(open('C:/Users/admin/PycharmProjects/mfl_10_inch_desktop/utils/pipe_198_base.json').read())
    h = json.loads(open('E:/MFL_desktop_web/mfl_10_inch_desktop/utils/pipe_69_base.json').read())
    #print(f,h)
    thick_avg = []
    count = [0, 0]
    #print(f)
    #print(h)
    for i, data in enumerate(f):
        for j, data1 in enumerate(h):
            if i == j:
                a = (round(float(f[data])) + round(float(h[data1]))) / 2
                thick_avg.append(a)
                # print(1,j,data,data1)
                if a <= round(float(config[tup1[i]])):
                    count[0] = count[0] + 1
                else:
                    count[1] = count[1] + 1
                # print(count)
    #print(count)
    if count[0] > count[1]:
        return 6.35
    elif count[0] < count[1]:
        return 9.27
    else:
        return 0

def insert_defect_into_db(finial_defects, runid, pipe_id, lower_sensitivity, upper_sensitivity):
    # print("final_defects", finial_defects)
    with connection.cursor() as cursor:
        same_lw_up_check = cursor.execute('SELECT pipe_id,lower_sensitivity,upper_sensitivity from defect_sensor_hm where pipe_id="' + str(pipe_id) + '" and lower_sensitivity="' + str(lower_sensitivity) + '" and upper_sensitivity="' + str(upper_sensitivity) + '"')
        if same_lw_up_check:
            return 'HII'
    for i in finial_defects:
        start_observation = i['start_observation']
        end_observation = i['end_observation']
        start_index_q1 = i['start_index_q1']
        end_index_q2 = i['end_index_q2']
        start_sensor = i['start_sensor']
        end_sensor = i['end_sensor']
        sensor_no = i['sensor_no']
        angle = i['angle']
        angle_hr_min = i['angle_hr_m']
        length = round(i['length'])
        length_odd1 = round(i['length_odd1'])
        absolute_distance_odd1 = round(i['absolute_distance_oddo1'])
        depth = i['depth']
        defect_type = i['defect_type']
        defect_classification = i['defect_classification']
        breadth = round(i['breadth'])
        absolute_distance = round(i['absolute_distance'])
        pipe_thickness = i['pipe_thickness']
        type = 'system'
        latitude = i['latitude']
        longitude = i['longitude']
        upstream_oddo1 = round(i['upstream_oddo1'])
        upstream_oddo2 = round(i['upstream_oddo2'])
        with connection.cursor() as cursor:
            query_defect_insert = "INSERT into defect_sensor_hm (runid, pipe_id, start_observation, end_observation, start_index_q1, end_index_q2, start_sensor, end_sensor, sensor_no, angle, angle_hr_m, length, breadth, depth,defect_type, type, lower_sensitivity, upper_sensitivity, absolute_distance, defect_classification, length_odd1, absolute_distance_oddo1, latitude, longitude, pipe_thickness,upstream_oddo1,upstream_oddo2) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

            cursor.execute(query_defect_insert, (
                int(runid), pipe_id, start_observation, end_observation, start_index_q1, end_index_q2, start_sensor, end_sensor, sensor_no, angle, angle_hr_min, length,
                breadth, depth, defect_type, type, lower_sensitivity, upper_sensitivity, absolute_distance, defect_classification, length_odd1,
                absolute_distance_odd1, latitude, longitude, pipe_thickness, upstream_oddo1, upstream_oddo2))

            connection.commit()


def lat_long(absolute_length, runid):
    with connection.cursor() as cursor:
        query = """
        SELECT id, runid, pipe_id, start_index, absolute_distance_oddo1, Latitude, Longitude 
        FROM dgps_segment 
        WHERE runid=%s
        ORDER BY absolute_distance_oddo1
        """
        cursor.execute(query, (runid,))
        result = cursor.fetchall()

    if not result:
        print(f"No data found for runid: {runid}")
        return None, None  # Ensures no unpacking error

    # Convert database result into a dictionary
    data_dict = {
        'id': [],
        'runid': [],
        'pipe_id': [],
        'start_index': [],
        'absolute_distance_oddo1': [],
        'Latitude': [],
        'Longitude': []
    }

    for row in result:
        data_dict['id'].append(row[0])
        data_dict['runid'].append(row[1])
        data_dict['pipe_id'].append(row[2])
        data_dict['start_index'].append(row[3])
        data_dict['absolute_distance_oddo1'].append(row[4])
        data_dict['Latitude'].append(row[5])
        data_dict['Longitude'].append(row[6])

    # Now using the same logic with the dynamically fetched data
    absolute_distances = data_dict['absolute_distance_oddo1']

    for j, distance in enumerate(absolute_distances):
        if absolute_length < distance:
            return data_dict['Longitude'][j], data_dict['Latitude'][j]

        elif distance < absolute_length and absolute_distances[j + 1] > absolute_length:
            A = distance
            B = absolute_distances[j + 1]
            C = absolute_length
            m = C - A
            n = B - C

            x1 = ((m * data_dict['Longitude'][j + 1]) + (n * data_dict['Longitude'][j])) / (m + n)
            y1 = ((m * data_dict['Latitude'][j + 1]) + (n * data_dict['Latitude'][j])) / (m + n)

            return x1, y1

        elif absolute_length > absolute_distances[j + 1]:
            if j == len(absolute_distances) - 2:
                return data_dict['Longitude'][j + 1], data_dict['Latitude'][j + 1]

    return None, None  # If no match is found, return (None, None)

def internal_or_external(df_new_proximity, x):
    sensor_number = x+1
    if sensor_number % 4 == 0:
        flapper_no = int(sensor_number / 4)
    else:
        flapper_no = int(sensor_number / 4) + 1

    proximity_no = flapper_no % 4
    if proximity_no == 0:
        proximity_no = 4
    proximity_index = 'F' + str(flapper_no) + 'P' + str(proximity_no)
    print("Proximity_index",proximity_index)
    maximum_depth_proximity_sensor = df_new_proximity[proximity_index]

    c = maximum_depth_proximity_sensor.tolist()
    minimum_value_proximity = min(c)
    mean_value_proximtiy=mean(c)

    print("mean_value_proximtiy", mean_value_proximtiy)
    print("minimum value of proximity",minimum_value_proximity)

    difference_mean = mean_value_proximtiy - minimum_value_proximity

    print("difference_minimum2", difference_mean)
    if difference_mean < 5000:
        type = "Internal"
        return type
    else:
        type = "External"
        return type
    # mean_of_proximity = df_new_proximity.mean()
    # print("mean_of_defect", mean_of_proximity)
    # average_value_list = mean_of_proximity.values.tolist()
    # average_value_list = [float(s) for s in average_value_list]
    # # print("average_value_list", average_value_list)
    # list_2d = df_new_proximity.values.tolist()
    # index_1 = 0
    # compare_list_mean = []
    # while (index_1 < len(list_2d[0])):
    #     x2 = []
    #     for j, value in enumerate(list_2d):
    #         if list_2d[j][index_1] < average_value_list[index_1]:
    #             x2.append(list_2d[j][index_1])
    #     index_1 = index_1 + 1
    #     mean_value_of_compare_list = mean(x2)
    #     compare_list_mean.append(mean_value_of_compare_list)
    # print("compare_list_of_mean", compare_list_mean)
    # ############# noise_difference_each_proximity_sensore ###############
    # zip_object_2 = zip(average_value_list, compare_list_mean)
    # noise_difference_list = []
    # for list1_4, list2_5 in zip_object_2:
    #     noise_difference_list.append(list1_4 - list2_5)
    # print("noise_difference list", noise_difference_list)


def defect_angle_x(roll_x, sensor):
    roll_angle=list(roll_x)
    roll_position=roll_angle[0]
    print("roll_postion and sensor", roll_position, sensor)
    x = 1.73            ################# x 1.73 for 12 inch and 1.74  for 14 inch pipe #################
    y = 3.30            ################# y 3.30 for 12 inch and 3.37 for 14 inch pipe #################
    z = 4.52            ################# z 4.52 for 12 inch and 5.63 for 14 inch pipe #################
    a = 8.2             ################# a 8.2 for 12 inch and 6.5 for 14 inch pipe #################
    b = int(sensor / 16)
    c = b * a

    d = int(sensor / 8)
    e = d - b
    f = e * z

    g = int(sensor / 4)
    h = g - (b + e)
    i = h * y

    j = sensor * x
    # roll_position = 0.15
    initial_calculation_of_each_sensor = c + f + i + j
    print("a", initial_calculation_of_each_sensor)
    if roll_position > 0:
        # print(roll_position)
        roll_position = roll_position + initial_calculation_of_each_sensor
        if roll_position > 360:
            print(roll_position)
            roll_position = roll_position % 360
    else:
        roll_position = 360 + roll_position
        roll_position = roll_position + initial_calculation_of_each_sensor
        if roll_position > 360:
            roll_position = roll_position % 360
            angle = initial_calculation_of_each_sensor + roll_position
            print("angle rotation", angle)
            print("angle", roll_position)
    adsmd = roll_position / 30
    k = int(adsmd)
    m = int(roll_position % 30)
    g = ':'
    angle_hr_min = str(k) + g + str(m)
    return angle_hr_min


def Width_calculation(start_sensor1, end_sensor1):
    start_sensor1, end_sensor1 = start_sensor1+1, end_sensor1+1
    if start_sensor1 > end_sensor1 or start_sensor1 == end_sensor1:
        return 0

    outer_diameter_1 = config.outer_dia  # 12-inch pipe
    thickness_1 = config.pipe_thickness  # Replace with Config.pipe_thickness if using from config
    inner_diameter_1 = outer_diameter_1 - 2 * (thickness_1)
    radius_1 = inner_diameter_1 / 2

    theta_2 = config.width_angle1               # approximate value for both pipes
    c_1 = math.radians(theta_2)
    theta_3 = config.width_angle2               # approximate value for both pipes
    d_1 = math.radians(theta_3)
    theta_4 = config.width_angle3             # 9.97 for thickness 5.5 and 9.53 for thickness 7.1
    e_1 = math.radians(theta_4)  # Convert to radians
    # print("c1, d1", c_1, d_1)

    x1 = round(radius_1 * c_1, 1)
    y1 = round(radius_1 * d_1, 1)
    z1 = round(radius_1 * e_1, 1)  # Distance for sensors at multiples of 16
    print("x1, y1, z1", x1, y1, z1)

    bredth = 0
    i = start_sensor1
    while i < end_sensor1:
        # next_sensor = i + 1
        next_sensor = i
        if next_sensor % 16 == 0 and next_sensor != end_sensor1:
            bredth += z1
            # print(f"{i} → {next_sensor:<10} z1 (because {next_sensor} is a multiple of 16)")
        elif next_sensor % 4 == 0:  # If the next sensor is a multiple of 4 (but not 16)
            bredth += y1
            # print(f"{i} → {next_sensor:<10} (y1 - x1) (because {next_sensor} is a multiple of 4)")
        else:
            bredth += x1
            # print(f"{i} → {next_sensor:<10} x1")
        i += 1  # Move to the next sensor
    return bredth

    # if start_sensor1 > end_sensor1:
    #     bredth = 0
    #     return bredth
    #
    # else:
    #     if start_sensor1 == end_sensor1:
    #         bredth = 0
    #         return bredth
    #     else:
    #         outer_diameter_1 = 324                     ################# outer_diametere 324 for 12 inch and 355 for 14 inch pipe #################
    #         thickness_1 = Config.pipe_thickness        ################# each pipe thickness can be change old thickness 6.4 ############
    #         inner_diameter_1 = outer_diameter_1 - 2 * (thickness_1)
    #         radius_1 = inner_diameter_1 / 2
    #
    #         theta_2 = 1.73              ################# theta_2 1.73 for 12 inch and 1.74 for 14 inch pipe - (sensor to sensor) #################
    #         c_1 = math.radians(theta_2)  ########### c in calculated in radians ########
    #         theta_3 = 3.3              ################# theta_3 4.52 for 12 inch and 5.63 for 14 inch pipe - (flapper to flapper)  #################
    #         d_1 = math.radians(theta_3)  ########### d in calculated in radians #####
    #
    #         x1 = radius_1 * c_1  ###### sensor to sensor angle between(x) 1.58 ex:1-2,2-3,3-4,5-6,6-7,7-8 ######
    #         y1 = radius_1 * d_1
    #         # print("sensor to sensor length", x1)
    #         # print("falpper within sensor to next flapper sensor length", y1)
    #         count = 0
    #         if start_sensor1 == end_sensor1:
    #             bredth = 0
    #             return bredth
    #         else:
    #             for i in range(start_sensor1, end_sensor1):
    #                 if i % 4 == 0:
    #                     count = count + 1
    #                     k = (y1 - x1) * count
    #                 else:
    #                     pass
    #             try:
    #                 l = (end_sensor1 - start_sensor1) * x1
    #                 bredth = k + l
    #                 return bredth
    #             except:
    #                 k = 0
    #                 l = (end_sensor1 - start_sensor1) * x1
    #                 bredth = k + l
    #                 return bredth


def defect_max(data, start, end, a, b):
    data_observation = []
    max = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    data1 = data[start:end]
    # df=pd.DataFrame(data1)
    # df.to_csv('E:/MFL_10_Inch/mfl_10_inch_desktop/a.csv')
    for row in data1:
        data_observation.append(row)
        for y, data2 in enumerate(row):
            """
            Check data range b/w start_sensor=a and end_sensor=b
            """
            if y > a - 1 and y < b + 1:
                if data2 >= max[y]:
                    max[y] = data2
    return (max, data_observation, data1, a, b)

def get_defect_list_from_db(runid, pipe_id):
    # runid = self.runid
    # pipe_id = self.pipe_id
    defects = []
    with connection.cursor() as cursor:
        try:
            Fetch_weld_detail = "select * from defect_sensor_hm where runid='%s' and pipe_id='%s'"
            # Execute query.
            cursor.execute(Fetch_weld_detail, (int(runid), int(pipe_id)))
            allSQLRows = cursor.fetchall()
            for row in allSQLRows:
                # print(row[3])
                defects.append([row[3], row[4], row[5], row[6]])
                # if row[11] == 'manual':
                #     self.reset_defect_pushButton.show()

            return defects
        except:
            # logger.log_error("Error during fetching defects from db for runid = " + runid)
            return []