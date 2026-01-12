import sys
import json
from google.cloud import bigquery
import Components.config as Config

connection = Config.connection
credentials = Config.credentials
project_id = Config.project_id
client = bigquery.Client(credentials=credentials, project=project_id)
config = json.loads(open('../utils/sensor_value.json').read())


class Query():
    def __init__(self, runid, analytic_id):
        self.runid = runid
        print(Config.no_weld_indicator)
        # analytic_id which will be provided from user
        self.analytic_id = analytic_id
        if Config.no_weld_indicator:
            print("here 1")
            query_for_first_record = 'SELECT filename,Serialno FROM ' + Config.table_name + ' where runid={} ORDER BY index  LIMIT 1'
            query_job_for_first = client.query(query_for_first_record.format(runid))
            print(query_job_for_first)
            result_of_first_record = query_job_for_first.result()
            print(result_of_first_record)
            query_for_last = 'SELECT filename,Serialno FROM ' + Config.table_name + ' where runid={} ORDER BY index DESC LIMIT 1'
            query_for_last_record = client.query(query_for_last.format(runid))
            result_of_last_record = query_for_last_record.result()
            print(result_of_last_record)
            query_pipe_insert_start = "INSERT INTO pipedetail (runid, analytic_id, pipe_start_filename, pipe_start_serialno ) VALUE(%s,%s,%s,%s) "
            query_pipe_insert_end = "UPDATE pipedetail set pipe_end_filename='%s',pipe_end_serialno='%s' where pipe_id=LAST_INSERT_ID()"
            print("here 3")
            # Execute query.
            # print(int(runid), int(analytic_id), float(1), int(result_of_first_record[0][0]))
            for row in result_of_first_record:
                print(row)
                with connection.cursor() as cursor:
                    cursor.execute(query_pipe_insert_start, (
                        int(runid), int(analytic_id), int(row[0]),
                        int(row[1])))
                    connection.commit()
                    print(result_of_first_record)
            for row in result_of_last_record:
                print(row)
                with connection.cursor() as cursor:
                    cursor.execute(query_pipe_insert_end, (int(row[0]), int(row[1])))
                    connection.commit()
            print("here 4")
        else:
            print("here 2")
            self.fetch_weld_record()
            self.weld_to_pipe_from_BQ()

    def fetch_weld_record(self):
        runid = self.runid
        analytic_id = self.analytic_id
        # Fetch the record from given runid and analytic_id from weld table
        with connection.cursor() as cursor:
            Fetch_weld_record = "select runid,analytic_id,Sensitivity,weld_id,weld_start_filename,weld_start_serialno,weld_end_filename,weld_end_serialno from welddetail where runid='%s' and analytic_id='%s' "

            # Execute query.
            cursor.execute(Fetch_weld_record, (int(runid), int(analytic_id)))
            self.fetched_data = cursor.fetchall()
            print(self.fetched_data)
            connection.commit()
        # return fetched_data
        # print(len(fetched_data[0]))

    # runid=1
    def weld_to_pipe_from_BQ(self):
        weld_record = self.fetched_data

        # query to get the first record filename, Serialno as it will act as start of pipe
        query_for_first_record = 'SELECT filename,Serialno FROM ' + Config.table_name + ' where runid={} LIMIT 1'
        query_job_for_first = client.query(query_for_first_record.format(weld_record[0][0]))
        result_of_first_record = query_job_for_first.result()
        # Entry of first BQ filename, Serialno record as start of pipe in pipedetail
        for row in result_of_first_record:
            with connection.cursor() as cursor:
                # SQL
                query_pipe_insert = "INSERT INTO pipedetail (runid, analytic_id,pipe_start_filename, pipe_start_serialno) VALUE(%s,%s,%s,%s) "

                # Execute query.
                cursor.execute(query_pipe_insert, (
                    int(weld_record[0][0]), int(weld_record[0][1]), int(row[0]), int(row[1])))
                connection.commit()
        print("start of pipe inserted in sql")
        i = 0
        while i <= (len(weld_record) - 1):
            # Fetching weld Start for previous record to mark the end of pipe
            query = 'WITH previous_order AS (SELECT *, LAG(filename) over(PARTITION BY runid ORDER BY filename,Serialno) AS prev_filename,LAG(Serialno)' \
                    'over(PARTITION BY runid ORDER BY filename,Serialno) AS prev_Serialno FROM ' + Config.table_name + ')' \
                    'SELECT prev_filename,prev_Serialno FROM previous_order WHERE filename={} AND Serialno={} AND runid={}'
            query_job = client.query(query.format(weld_record[i][4], weld_record[i][5], weld_record[i][0]))
            results = query_job.result()  # Waits for job to complete.
            print("End of fetching pipe start record from bigquery")
            if results.total_rows == 0:
                sys.exit("No record found, Check the runid ")
            for row in results:
                pipe_end_filename = row[0]
                pipe_end_serialno = row[1]

            # Fetching weld end for next record to mark the start of next pipe
            query = 'WITH next_order AS (SELECT *, LEAD(filename) over(PARTITION BY runid ORDER BY filename,Serialno) AS next_filename,LEAD(Serialno)' \
                    'over(PARTITION BY runid ORDER BY filename,Serialno) AS next_Serialno FROM ' + Config.table_name + ')' \
                    'SELECT next_filename,next_Serialno FROM next_order WHERE filename={} AND Serialno={} AND runid={}'
            query_job = client.query(query.format(weld_record[i][6], weld_record[i][7], weld_record[i][0]))
            results = query_job.result()  # Waits for job to complete.
            print("End of fetching pipe end record from bigquery")
            if results.total_rows == 0:
                sys.exit("No record found, Check the runid ")
            for row in results:
                pipe_start_filename = row[0]
                pipe_start_serialno = row[1]
            with connection.cursor() as cursor:
                # SQL
                query_pipe_end_update = "UPDATE pipedetail set pipe_end_filename='%s',pipe_end_serialno='%s' where pipe_id=LAST_INSERT_ID() "

                # Execute query.
                cursor.execute(query_pipe_end_update, (int(pipe_end_filename), int(pipe_end_serialno)))
                connection.commit()
                # i=i+1
                print("end pipe record inserted")
            with connection.cursor() as cursor:
                # SQL
                query_pipe_insert = "INSERT INTO pipedetail (runid, analytic_id, pipe_start_filename, pipe_start_serialno) VALUE(%s,%s,%s,%s) "

                # Execute query.
                cursor.execute(query_pipe_insert, (
                    int(weld_record[i][0]), int(weld_record[i][1]), int(pipe_start_filename),
                    int(pipe_start_serialno)))
                connection.commit()
                print("start of new pipe record inserted")
            i = i + 1
        # now the last record of data inserted from BQ to pipedetail as it will end here
        query_for_last_record = 'SELECT filename,Serialno FROM ' + Config.table_name + ' where runid={} order by  filename DESC,Serialno DESC LIMIT 1'
        query_job_for_last = client.query(query_for_last_record.format(weld_record[i - 1][0]))
        result_of_last_record = query_job_for_last.result()
        # Entry of last BQ filename, Serialno record as start of pipe in pipedetail
        for row in result_of_last_record:
            with connection.cursor() as cursor:
                # SQL
                query_pipe_update_last = "update pipedetail set pipe_end_filename='%s', pipe_end_serialno='%s' where pipe_id=LAST_INSERT_ID() "

                # Execute query.
                cursor.execute(query_pipe_update_last, (int(row[0]), int(row[1])))
                connection.commit()
                print("hii")

    # weld_fetched_data = Fetch_weld_record(runid)
    # print(weld_fetched_data)
    # weld_to_pipe_from_BQ(weld_fetched_data)

    def merge_pipe(self, runid):
        with connection.cursor() as cursor:
            Fetch_pipe_record = "select pipe_length,pipe_id,pipe_start_filename," \
                                "pipe_end_filename from pipedetail where runid='%s'"
            cursor.execute(Fetch_pipe_record, (int(runid)))
            fetched_data = cursor.fetchall()
            for i, elem in enumerate(fetched_data):
                print(elem)
