import json
from google.cloud import bigquery
import Components.config as Config

connection = Config.connection
credentials = Config.credentials
project_id = Config.project_id
client = bigquery.Client(credentials=credentials, project=project_id)
config = json.loads(open('./utils/sensor_value - Copy.json').read())

class Query_flow():
    def __init__(self, runid, sensitivity):
        """
                    This will return a query(string type) for bigquery that will fetch welds raw-data
                    :sensitivity : Sensitivity of the Weld
                    :runid : Id of the Project
                """
        self.runid = runid
        self.sensitivity = float(sensitivity)

        self.F1P1 =self.sensitivity * float(config["proximity1"])

        self.F2P2 =self.sensitivity * float(config["proximity2"])

        self.F3P3 = self.sensitivity * float(config["proximity3"])

        self.F4P4 = self.sensitivity * float(config["proximity4"])

        self.F5P1 = self.sensitivity * float(config["proximity5"])

        self.F6P2 = self.sensitivity * float(config["proximity6"])

        self.F7P3 = self.sensitivity * float(config["proximity7"])

        self.F8P4 = self.sensitivity * float(config["proximity8"])

        self.F9P1 = self.sensitivity * float(config["proximity9"])

        self.F10P2 = self.sensitivity * float(config["proximity10"])

        self.F11P3 = self.sensitivity * float(config["proximity11"])

        self.F12P4 = self.sensitivity * float(config["proximity12"])

        self.F13P1 = self.sensitivity * float(config["proximity13"])

        self.F14P2 = self.sensitivity * float(config["proximity14"])

        self.F15P3 = self.sensitivity * float(config["proximity15"])

        self.F16P4 = self.sensitivity * float(config["proximity16"])

        self.F17P1 = self.sensitivity * float(config["proximity17"])

        self.F18P2 = self.sensitivity * float(config["proximity18"])

        self.query_flow()

    def query_flow(self):
        sensitivity = self.sensitivity
        runid = self.runid
        print("start of fetching weld record from bigquery")
        query = 'SELECT ODDO1,ODDO2,index FROM ' + Config.table_name + ' WHERE  (select countif(condition) from unnest([proximity1>{} , proximity2>{} , proximity3>{} , proximity4>{}  , proximity5>{} , proximity6>{} , proximity7>{} , proximity8>{} , proximity9>{} , proximity10>{} , proximity11>{} , proximity12>{}  , proximity13>{} , proximity14>{} , proximity15>{} , proximity16>{}  , proximity17>{} , proximity18>{},runid>{}]) condition) >= 9 ORDER BY index'

        query_to_run = query.format(self.F1P1, self.F2P2, self.F3P3, self.F4P4, self.F5P1, self.F6P2, self.F7P3, self.F8P4, self.F9P1, self.F10P2, self.F11P3, self.F12P4, self.F13P1,
                                    self.F14P2, self.F15P3, self.F16P4, self.F17P1, self.F18P2, runid)

        #print("hi")
        query_job = client.query(query_to_run)
        results = query_job.result()
        #results = query_to_run.result()  # Waits for job to complete.
        print("End of fetching weld record from bigquery")
        print(results)
        if results.total_rows == 0:
            Config.no_weld_indicator = True
            Config.warning_msg("NO weld record Found", "")
            return
        else:
            Config.no_weld_indicator = False
            Config.print_with_time("weld record found")
            indexes = []
            oddo1 = []
            oddo2 = []
            Config.print_with_time("creating list of indexes")
            print(results)
            for row in results:
                oddo1.append(row[0])
                oddo2.append(row[1])
                indexes.append(row[2])


            # print("indexes",indexes)
            # print("oddo1",oddo1)
            # print("oddo2",oddo2)
            Config.print_with_time("list of indexes created")
            p_data = ranges(indexes)
            f_data = []
            analytic_id = get_analytic_id(runid, sensitivity)
            Config.print_with_time("Analytic Id is " + str(analytic_id))
            Config.print_with_time("Generating Welds")
            for i, row in enumerate(p_data):
                index1 = indexes.index(row[0])
                index2 = indexes.index(row[1])
                start_oddo1 = oddo1[index1]
                end_oddo1 = oddo1[index2]
                start_oddo2 = oddo2[index1]
                end_oddo2 = oddo2[index2]
                weld_length = end_oddo1 - start_oddo1 if end_oddo1 >= end_oddo2 else end_oddo2 - start_oddo2
                temp = {"start_index": row[0], "end_index": row[1], "start_oddo1": start_oddo1, "end_oddo1": end_oddo1,
                        "start_oddo2": start_oddo2, "end_oddo2": end_oddo2, "weld_number": i + 1,
                        "analytic_id": analytic_id,
                        "length": weld_length, "sensitivity": sensitivity, "runid": runid}
                f_data.append(temp)
                #print(f_data)
                insert_weld_to_db(temp)
            Config.print_with_time("Weld Generation completed")


# =======================================================================================================
# -----------------------------------Starting of helping module for Weld---------------------------------
# ========================================================================================================
def ranges(arr):
    """"
    This will merge the continues indexes and return a list that will contain list of start_index and end_index
        :param arr : List of indexes to merge
    """
    try:
        nums = sorted(set(arr))
        gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s+2500 < e] #### old change s+1<e
        edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
        return list(zip(edges, edges))
    except:
        print("Error while Grouping Weld Range")


# ===========================================================================================================

def insert_weld_to_db(weld_obj):
    print("weld_obj",weld_obj)
    """
        This will insert weld object to mysql database
        :param weld_obj : Object with value of  runid,analytic_id,sensitivity,start_index,end_index,start_oddo1,end_oddo1,start_oddo2,end_oddo2,length and weld_number
    """
    try:

        query_weld_insert = "INSERT INTO temp_welds (runid,analytic_id,sensitivity,start_index,end_index,start_oddo1,end_oddo1,start_oddo2,end_oddo2,length,weld_number) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # print(runid, analytic_id, Sensitivity, start_file, end_file, start_sno, end_sno)
        with connection.cursor() as cursor:
            cursor.execute(query_weld_insert, (
            weld_obj["runid"], weld_obj["analytic_id"], weld_obj["sensitivity"], weld_obj["start_index"],
            weld_obj["end_index"], weld_obj["start_oddo1"], weld_obj["end_oddo1"], weld_obj["start_oddo2"],
            weld_obj["end_oddo2"], weld_obj["length"], weld_obj["weld_number"]))
            connection.commit()
        return
    except:
        print("Error While Inserting weld for runid ")


# ===============================================================================================================


# ===============================================================================================================

def get_analytic_id(runid, sensitivity):
    """
        This will return a New Analytic Id
        : param runid: Id of the Project
        : param sensitivity : Sensitivity of the Weld
    """
    with connection.cursor() as cursor:
        query_to_check_analyticsid = "SELECT runid,analytic_id,Sensitivity FROM welds ORDER BY id DESC LIMIT 1"
        cursor.execute(query_to_check_analyticsid)
        result_analytics_query = cursor.fetchone()
        if not result_analytics_query:
            return 1
        elif runid == result_analytics_query[0] and sensitivity != result_analytics_query[2]:
            return result_analytics_query[1] + 1
        elif runid != result_analytics_query[0]:
            return 1
        else:
            return result_analytics_query[1] + 1


# ============================================================================================================

# =======================================================================================================
# -----------------------------------Ending of helping module for Weld Generation----------------
# ========================================================================================================
