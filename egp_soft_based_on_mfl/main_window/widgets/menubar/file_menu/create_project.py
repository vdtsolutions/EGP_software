from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# import GMFL_12_Inch_Desktop.Components.Configs.config_old as Config
# connection = Config.connection
from egp_soft_based_on_mfl.Components.Configs.gcp_and_db_config import create_db_connection


class AddProject(QDialog):
    project_created = pyqtSignal()
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
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
        self.bottomLayout.addRow(self.ProjectName)
        self.bottomLayout.addRow(self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def submit_info(self):
        project = self.ProjectName.text()

        try:
            with self.config.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM projectdetail WHERE ProjectName=%s",
                    (project,)
                )
                if cursor.fetchone():
                    QMessageBox.about(self, 'Validation', 'Project already exists')
                else:
                    cursor.execute(
                        "INSERT INTO projectdetail (ProjectName) VALUES (%s)",
                        (project,)
                    )
                    self.config.connection.commit()

                    QMessageBox.about(self, 'Success', 'Project Created Successfully')

                    self.project_created.emit()  # 🔥 notify parent
                    self.accept()  # close dialog

        except Exception as e:
            QMessageBox.about(self, 'Connection', 'Network Connection Failed')
            print("error in create project:", e)


def create_project(self):
    dialog = AddProject(
        config=self.config,
        parent=self
    )

    dialog.project_created.connect(lambda : refresh_project_list(self))  # 👈 connect
    dialog.exec_()


def refresh_project_list(self):
    print("Refreshing project list...")

    if not hasattr(self, "config") or self.config is None:
        print("⚠️ Config not loaded yet.")
        return

    # Ensure DB still alive
    # self.config.init_db_connection(self.config.db_mysql)
    create_db_connection(self)
    # Only reload projects
    load_project_list(self)


def load_project_list(self):
    try:
        with self.config.connection.cursor() as cursor:
            cursor.execute(
                "SELECT `ProjectName` FROM projectdetail ORDER BY runid DESC"
            )
            projects = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print("DB error:", e)
        projects = ["Demo A", "Demo B", "Demo C"]

    self.combo_project.setEnabled(True)
    self.new_project_btn.setEnabled(True)

    self.combo_project.blockSignals(True)
    self.combo_project.clear()

    self.combo_project.addItem("Select Project")
    self.combo_project.model().item(0).setEnabled(False)
    self.combo_project.model().item(0).setForeground(QtGui.QColor("#888"))

    for p in projects:
        self.combo_project.addItem(p)

    self.combo_project.setCurrentIndex(0)
    self.combo_project.blockSignals(False)

    self.btn_apply.setEnabled(False)