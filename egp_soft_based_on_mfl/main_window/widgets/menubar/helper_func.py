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