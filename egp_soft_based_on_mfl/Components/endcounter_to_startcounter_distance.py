from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import egp_soft_based_on_mfl.Components.Configs.config_old as Config
from google.cloud import bigquery
connection = Config.connection
credentials = Config.credentials
project_id = Config.project_id
client = bigquery.Client(credentials=credentials, project=project_id)

class CalDistance(QWidget):
    def __init__(self, runid):
        self.runid = runid
        super().__init__()
        self.setWindowTitle("Calculate Distance")
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
          background-color:#0078d7;
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
        query_for_start = 'SELECT ODDO1,ODDO2 FROM ' + Config.table_name + ' WHERE index={} AND runid={}'
        query_job = client.query(query_for_start.format(int(start_index), runid))
        results = query_job.result()
        #print("start",results)
        oddo1_start=[]
        oddo2_start=[]
        for i in results:
            oddo1_start.append(i['ODDO1'])
            oddo2_start.append(i['ODDO2'])

        query_for_start1 = 'SELECT ODDO1,ODDO2 FROM ' + Config.table_name + ' WHERE index={} AND runid={}'
        query_job1 = client.query(query_for_start1.format(int(end_index), runid))
        results1 = query_job1.result()
        # print("end",results1)
        oddo1_end = []
        oddo2_end = []
        for j in results1:
            oddo1_end.append(j['ODDO1'])
            oddo2_end.append(j['ODDO2'])

        print("oddo1_start", oddo1_start[0])
        print("oddo2_start", oddo2_start[0])
        print("oddo1_end", oddo1_end[0])
        print("oddo2_end", oddo2_end[0])
        distance=oddo2_end[0]-oddo2_start[0]
        msgbox = QMessageBox(QMessageBox.Information, "End_to_Start_Observation_distance", "Value: %s" % distance, QMessageBox.Ok)
        msgbox.exec_()
        self.hide()


