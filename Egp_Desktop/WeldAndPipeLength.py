from google.cloud import bigquery
import Components.config as Config

connection = Config.connection
credentials = Config.credentials
project_id = Config.project_id
client = bigquery.Client(credentials=credentials, project=project_id)


class WeldPipeLength():
    def __init__(self, runid):
        self.runid = runid
        print(runid)
        # self.get_length_of_weld()
        self.get_length_of_pipe()

    def get_length_of_weld(self):
        print("get_length_of_weld called")
        runid = self.runid

        with connection.cursor() as cursor:
            # SQL
            query = "select weld_start_filename,weld_start_serialno,weld_end_filename," \
                    "weld_end_serialno,analytic_id from welddetail where analytic_id=(select max(analytic_id) from welddetail);"

            # Execute query.
            cursor.execute(query)
            start_end_weld = cursor.fetchall()
            print("start_end_weld", start_end_weld)

        for i in range(len(start_end_weld)):
            #print("here1")
            query_for_start = 'SELECT ODDO1,ODDO2 FROM ' + Config.table_name + ' WHERE filename={} AND Serialno={} AND runid={}'
            query_job = client.query(query_for_start.format(start_end_weld[i][0], start_end_weld[i][1], runid))
            results_start = query_job.result()
            #print("here2")

            query_for_end = 'SELECT ODDO1,ODDO2 FROM ' + Config.table_name + ' WHERE filename={} AND Serialno={} AND runid={}'
            query_job = client.query(query_for_end.format(start_end_weld[i][2], start_end_weld[i][3], runid))
            results_end = query_job.result()

            #print("here3")

            for row in results_start:
                print("result_start",row)
                missing_value_ind = False
                print("here4")
                try:
                    if row[0] > row[1]:
                        oddo_start_position = row[0]
                    else:
                        oddo_start_position = row[1]
                except:
                    missing_value_ind = True
            for row in results_end:
                print("result_end",row)
                missing_value_ind = False
                print("here5", row[0], row[1])

                try:
                    if row[0] > row[1]:
                        oddo_end_position = row[0]
                    else:
                        oddo_end_position = row[1]
                except:
                    missing_value_ind = True
            if missing_value_ind:
                weld_width = 20000
            else:
                weld_width = oddo_end_position - oddo_start_position

            print("weld_width", weld_width)
            with connection.cursor() as cursor:

                # SQL
                query_weld_length_update = "UPDATE welddetail set weld_length='%s' where weld_start_filename='%s' and weld_start_serialno='%s' and " \
                                           "weld_end_filename='%s' and weld_end_serialno='%s' and analytic_id='%s';"

                # Execute query.
                cursor.execute(query_weld_length_update,
                               (int(weld_width), int(start_end_weld[i][0]), int(start_end_weld[i][1]), \
                                int(start_end_weld[i][2]), int(start_end_weld[i][3]), int(start_end_weld[i][4])))
                connection.commit()

    def get_length_of_pipe(self):
        runid = self.runid
        #print(runid)
        with connection.cursor() as cursor:
            # SQL
            query = "select pipe_start_filename,pipe_start_serialno,pipe_end_filename," \
                    "pipe_end_serialno,analytic_id from pipedetail where analytic_id=(select max(analytic_id) from pipedetail);"

            # Execute query.
            cursor.execute(query.format(runid))
            start_end_pipe = cursor.fetchall()
            print("start_end_pipe", start_end_pipe)

        for i in range(len(start_end_pipe)):
            query_for_start = 'SELECT ODDO1,ODDO2 FROM ' + Config.table_name + ' WHERE filename={} AND Serialno={} AND runid={}'
            query_job = client.query(query_for_start.format(start_end_pipe[i][0], start_end_pipe[i][1], runid))
            results_start = query_job.result()

            query_for_end = 'SELECT ODDO1,ODDO2 FROM ' + Config.table_name + ' WHERE filename={} AND Serialno={} AND runid={}'
            query_job = client.query(query_for_end.format(start_end_pipe[i][2], start_end_pipe[i][3], runid))
            results_end = query_job.result()

            for row in results_start:
                print(row)
                if row[0] > row[1]:
                    oddo_start_position = row[0]
                else:
                    oddo_start_position = row[1]
            for row in results_end:
                if row[0] > row[1]:
                    oddo_end_position = row[0]
                else:
                    oddo_end_position = row[1]
            pipe_width = oddo_end_position - oddo_start_position
            print("pipe_width", pipe_width)
            with connection.cursor() as cursor:
                # SQL
                query_pipe_length_update = "UPDATE pipedetail set pipe_length='%s' where pipe_start_filename='%s' and " \
                                           "pipe_start_serialno='%s' and " \
                                           "pipe_end_filename='%s' and pipe_end_serialno='%s' and analytic_id='%s';"

                # Execute query.
                cursor.execute(query_pipe_length_update,(int(pipe_width), int(start_end_pipe[i][0]), int(start_end_pipe[i][1]), \
                 int(start_end_pipe[i][2]), int(start_end_pipe[i][3]), int(start_end_pipe[i][4])))
                connection.commit()
    # get_length_of_weld()
    # get_length_of_pipe()
