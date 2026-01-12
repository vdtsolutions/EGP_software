from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import egp_soft_based_on_mfl.Components.Configs.config_old as Config
from google.cloud import bigquery
connection = Config.connection
credentials = Config.credentials
project_id = Config.project_id
client = bigquery.Client(credentials=credentials, project=project_id)

class AddWeldDetail(QWidget):
    def __init__(self, runid):
        self.runid = runid
        super().__init__()
        self.setWindowTitle("Add Weld")
        self.setWindowIcon(QIcon('icons/project.svg'))
        self.setFixedSize(300, 300)
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.start_index = QLineEdit()
        self.start_index.setStyleSheet("""
        width: 100%;
        font-size=16px;
         padding: 12px 20px; 
         margin: 8px 0;border: 1px solid #ccc;border-radius: 4px;
        """
                                       )
        self.start_index.setPlaceholderText("Start_index")
        self.end_index = QLineEdit()
        self.end_index.setStyleSheet("""
                width: 100%;
                font-size=16px;
                 padding: 12px 20px; 
                 margin: 8px 0;border: 1px solid #ccc;border-radius: 4px;
                """
                                     )
        self.end_index.setPlaceholderText("end_index")
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.setStyleSheet("""
          width: 100%;
          background-color:  #0078d7;
          color: white;
          padding: 14px 20px;
          font-size:14px;
          margin: 8px 0;
          border: none;
          border-radius: 4px;
         """)
        self.submitBtn.clicked.connect(self.submit_info)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.bottomFrame = QFrame()
        self.bottomLayout.addRow(self.start_index)
        self.bottomLayout.addRow(self.end_index)
        self.bottomLayout.addRow(self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def submit_info(self):
        start_index = self.start_index.text()
        end_index = self.end_index.text()
        runid = self.runid
        print(runid)
        query_for_start = 'SELECT ODDO1, ODDO2 FROM ' + Config.table_name + ' WHERE index>{} AND index<{} AND runid={} order by index'
        query_job = client.query(query_for_start.format(int(start_index), int(end_index), runid))
        results = query_job.result()
        oddo1 = []
        oddo2 = []
        for row in results:
            oddo1.append(row[0])
            oddo2.append(row[1])
        print(oddo1)
        print(oddo2)
        start_oddo1 = oddo1[0]
        end_oddo1 = oddo1[-1]
        start_oddo2 = oddo2[0]
        end_oddo2 = oddo2[-1]
        weld_length = end_oddo1 - start_oddo1 if end_oddo1 >= end_oddo2 else end_oddo2 - start_oddo2
        with connection.cursor() as cursor:
            fetch_last_row = "select * from temp_welds where runid='%s' order by temp_weld_id DESC LIMIT 1"
            # Execute query.
            cursor.execute(fetch_last_row, (int(runid)))
            allSQLRows = cursor.fetchall()
            print(allSQLRows)
            type = 'manual'
            weld_number = allSQLRows[0][1]+1
            analytic_id = allSQLRows[0][3]
            sensitivity = allSQLRows[0][4]
            query_weld_insert = "INSERT INTO temp_welds (weld_number,runid,analytic_id,sensitivity,start_index,end_index,type,start_oddo1,end_oddo1,start_oddo2,end_oddo2,length) VALUES({},'{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}')".format(weld_number,runid,analytic_id,sensitivity,start_index,end_index,type,start_oddo1,end_oddo1,start_oddo2,end_oddo2,weld_length)

            # Execute query.
            b = cursor.execute(query_weld_insert)
            connection.commit()
            if b:
                QMessageBox.about(self, 'Insert', 'Data Inserted Successfully')
                self.hide()
            else:
                print("data is not inserted successfully")
