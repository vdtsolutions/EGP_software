from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import Components.config as Config
connection = Config.connection


class AddProject(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Project")
        self.setWindowIcon(QIcon('icons/project.svg'))
        self.setFixedSize(340, 180)
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.ProjectName = QLineEdit()
        self.ProjectName.setStyleSheet("""
        width: 100%;
        font-size=16px;
         padding: 12px 20px; 
         margin: 8px 0;border: 1px solid #ccc;border-radius: 4px;
        """
                                       )
        self.ProjectName.setPlaceholderText("Enter Project Name")
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.setStyleSheet("""
          width: 100%;
          background-color: #4CAF50;
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
        self.bottomLayout.addRow(self.ProjectName)
        self.bottomLayout.addRow(self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def submit_info(self):
        project=self.ProjectName.text()
        try:
            with connection.cursor() as cursor:
                # Execute query.
                ProjectName=cursor.execute('SELECT * FROM projectdetail where ProjectName="' + str(project) + '"')
                if ProjectName:
                #Check Project Name is already exist in database
                    QMessageBox.about(self, 'Validation', 'ProjectName is already exist')
                else:
                    cursor.execute("INSERT INTO projectdetail(`ProjectName`) VALUES('%s')" % (''.join(project)))
                    connection.commit()
                    QMessageBox.about(self, 'Insert', 'Data Inserted Successfully')

        except:
            QMessageBox.about(self, 'Connection', 'Network Connection is failed')


