from PyQt5.QtWidgets import QInputDialog, QMessageBox
import egp_soft_based_on_mfl.Components.AddWeld as AddWeld


#DIMENSION_CLASSIFICATION
def Typeofdefect(self):
    try:
        runid = self.runid
        try:
            self.thickness_pipe, okPressed = QInputDialog.getText(self, "Get integer", "thickness_pipe")
            if okPressed:
                pass
                thickness_pipe = float(self.thickness_pipe)
                if thickness_pipe < 10.0:
                    geometrical_parameter = 10
                else:
                    geometrical_parameter = thickness_pipe
                get_type_defect(geometrical_parameter, runid)

        except:
            # logger.log_error("thickness_pipe is not found")
            pass
    except:
        QMessageBox.about(self, 'Info', 'Please select the runid')

def get_type_defect(self, geometrical_parameter, runid):
    print(geometrical_parameter, runid)
    with self.config.connection.cursor() as cursor:
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
                dimension_classification(self, type_of_defect, runid, defect_id)
        except:
            # logger.log_error("type of defect is not permissiable value")
            pass


def dimension_classification(self, type_of_defect, runid, defect_id):
    print(type_of_defect, runid)
    query = f'UPDATE finaldefect SET  Dimensions_classification="{type_of_defect}" WHERE runid="{runid}" and id={defect_id}'
    with self.config.connection.cursor() as cursor:
        cursor.execute(query)
        self.config.connection.commit()
######################################




#ADD_WELD
def AddWeld(self):
    try:
        self.AddData = AddWeld.AddWeldDetail(self.runid)
    except:
        QMessageBox.about(self, 'Info', 'Please select the runid')
######################



#CREATE PIPE
from PyQt5.QtWidgets import QMessageBox


def Create_pipe(self):
    try:
        runid = self.runid
        print(f"inside create pipe: {self.config.pipe_thickness}")
        # print(runid)
        with self.config.connection.cursor() as cursor:
            fetch_last_row = "select runid,start_index,end_index,type,analytic_id,sensitivity,length,start_oddo1,end_oddo1,start_oddo2,end_oddo2 from temp_welds where runid='%s' order by start_index"
            # Execute query.
            f_data = []
            cursor.execute(fetch_last_row, (int(runid)))
            allSQLRows = cursor.fetchall()
            for i, row in enumerate(allSQLRows):
                temp = {"start_index": row[1], "end_index": row[2], "weld_number": i + 1,
                        "type": row[3], "analytic_id": row[4], "sensitivity": row[5], "length": row[6],
                        "start_oddo1": row[7], "end_oddo1": row[8], "start_oddo2": row[9], "end_oddo2": row[10],
                        "runid": runid}

                f_data.append(temp)
                insert_weld_to_db(self, temp)
            last_index = 0
            last_oddo = 0
            pipes = []
            self.config.print_with_time("Generating Pipe")
            last_weld = f_data[-1]
            # print(f_data)
            for row in f_data:
                oddo = row["start_oddo1"] if row["start_oddo1"] > row["start_oddo2"] else row["start_oddo2"]
                length = oddo - last_oddo
                obj = {"start_index": last_index, "end_index": row["start_index"], "length": length,
                       "analytic_id": row["analytic_id"], "runid": runid}
                # print("obj...",obj)
                pipes.append(obj)
                last_index = row["end_index"]
                last_oddo = row["end_oddo1"] if row["end_oddo1"] > row["end_oddo2"] else row["end_oddo2"]
                insert_pipe_to_db(self, obj)
            last_pipe = get_last_pipe(self, runid, last_weld, last_weld['analytic_id'])
            insert_pipe_to_db(self, last_pipe)
            self.config.print_with_time("Pipe Generation completed")
            self.config.print_with_time("process end at : ")

        return
    except:
        QMessageBox.about(self, 'Info', 'Please select the runid')


def insert_pipe_to_db(self, pipe_obj):
    """
        This will insert pipe_obj to mysql database
        :param pipe_obj : object will value of runid,analytic_id,length,start_index and end_index
    """
    try:
        query = "INSERT INTO Pipes (runid,analytic_id,length,start_index,end_index) VALUE(%s,%s," \
                "%s,%s,%s) "
        with self.config.connection.cursor() as cursor:
            cursor.execute(query,
                           (pipe_obj["runid"], pipe_obj["analytic_id"], pipe_obj["length"], pipe_obj["start_index"],
                            pipe_obj["end_index"]))
            self.config.connection.commit()
        return
    except:
        print("Error While Inserting weld for runid ")


def get_last_pipe(self, runid, weld_obj, analytic_id):
    """
        This will return the last pipe object to insert into mysql db
        :param runid: Id of the Project
    """
    query = "SELECT index,oddo1,oddo2 FROM `" + self.config.table_name + "` order by index desc LIMIT 1 "
    query_job = self.config.client.query(query)
    results = query_job.result()
    for row in results:
        length = row['oddo1'] - weld_obj['end_oddo1']
        end_index = row['index']
        start_index = weld_obj['end_index']
        end_index = row['index']
        obj = {"start_index": start_index, "end_index": end_index, "length": length, "analytic_id": analytic_id,
               "runid": runid}
        return obj

def insert_weld_to_db(self,temp):
    #print("weld_obj", temp)
    """
        This will insert weld object to mysql database
        :param weld_obj : Object with value of  runid,analytic_id,sensitivity,start_index,end_index,start_oddo1,end_oddo1,start_oddo2,end_oddo2,length and weld_number
    """
    try:
        query_weld_insert = "INSERT INTO welds (weld_number,runid,start_index,end_index,type,analytic_id,sensitivity,length,start_oddo1,end_oddo1,start_oddo2,end_oddo2) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # print(runid, analytic_id, Sensitivity, start_file, end_file, start_sno, end_sno)
        with self.config.connection.cursor() as cursor:
            cursor.execute(query_weld_insert, (temp["weld_number"], temp["runid"], temp["start_index"], temp["end_index"], temp["type"], temp["analytic_id"], temp["sensitivity"], temp["length"], temp["start_oddo1"], temp["end_oddo1"], temp["start_oddo2"], temp["end_oddo2"]))
            self.config.connection.commit()
        return
    except:
        print("Error While Inserting weld for runid ")

#########################



#final defect
def update_defect1(self):
    print("hii")
    runid = self.runid
    with self.config.connection.cursor() as cursor:
        """
        oddo1
        """
        fetch_row="select runid,start_observation,end_observation,absolute_distance_oddo1,pipe_id,sensor_no,upstream_oddo1,pipe_length,defect_type,type,defect_classification,angle_hr_m,pipe_thickness,length_odd1,breadth,depth,latitude,latitude from defect_sensor_hm where runid='%s' and depth>'%s'  order by absolute_distance_oddo1"
        """
        oddo2
        """
        # fetch_row = "select runid,absolute_distance,pipe_id,sensor_no,upstream_oddo2,pipe_length,defect_type,type,defect_classification,angle_hr_m,pipe_thickness,length,breadth,depth,latitude,longitude from defect_sensor_hm where runid='%s' and depth>'%s'  order by absolute_distance"
        cursor.execute(fetch_row, (int(runid), 0))
        allSQLRows = cursor.fetchall()
        print(allSQLRows)
        for i in allSQLRows:
            #print(i[0])
            Query1="INSERT INTO finaldefect (runid,start_observation,end_observation,Absolute_distance,Pipe_number,Sensor_number,Distance_to_Upstream,Pipe_length,Feature_type,Feature_identification,Dimensions_classification,Orientation_clock,WT,Length,Width,Depth,Latitude,Longitude) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17])
            cursor.execute(Query1)
        self.config.connection.commit()
        self.config.connection.close()


#erf calculation
def Erf(self):
    length_of_defect_L = 24
    od_of_pipe_D = 323
    pipe_thickness_T = 6.35
    depth_of_defect_d = 2.8575
    specified_minimum_yield_strength_of_material_at_ambient_condition_SMYS = 2498.3
    flow_stress = 1.1 * specified_minimum_yield_strength_of_material_at_ambient_condition_SMYS
    print("Sflow", flow_stress)

    z_factor = (length_of_defect_L * length_of_defect_L) / (od_of_pipe_D * pipe_thickness_T)
    print("Z_factor", z_factor)

    x = 1 + 0.8 * z_factor
    Building_stress_magmification_factor_M = pow(x, 1 / 2)
    print("Building_stress_magmification_factor_M", Building_stress_magmification_factor_M)
    y = 1 - 2 / 3 * depth_of_defect_d / pipe_thickness_T
    z = 1 - 2 / 3 * depth_of_defect_d / pipe_thickness_T / Building_stress_magmification_factor_M
    k = y / z
    print(y)
    print(z)
    print(k)

    if z_factor <= 20:
        Estimated_failure_stress_level_SF = flow_stress * k
        print("estimated_failure_stress", Estimated_failure_stress_level_SF)
    else:
        Estimated_failure_stress_level_SF = flow_stress * (1 - depth_of_defect_d / pipe_thickness_T)
        print("estimated_failure_stress", Estimated_failure_stress_level_SF)
    estimate_failure_pressure = (2 * Estimated_failure_stress_level_SF * pipe_thickness_T) / od_of_pipe_D
    print("estimate_failure_pressure", estimate_failure_pressure)
    safety_factor_SF = 1.39
    safe_operating_pressure_of_corroded_area_Ps = estimate_failure_pressure / safety_factor_SF
    print("safe_operating_pressure_of_corroded_area_Ps", safe_operating_pressure_of_corroded_area_Ps)
    MAOP = 11
    ERF = MAOP / safe_operating_pressure_of_corroded_area_Ps
    print("Estimate Repair Factor", ERF)