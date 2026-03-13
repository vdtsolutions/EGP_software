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