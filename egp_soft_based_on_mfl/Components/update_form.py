from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
import os
import Components.style1 as Style
import Components.config as Config
import Components.logger as logger
import Components.Upload_data as Upload
from PyQt5 import QtCore


class UpdateForm:
    def __init__(self):
        pass

    # def _init_form_layout(self,tab_update, tab_updatelayout):
    #     self.formLayoutWidget = QtWidgets.QWidget()
    #     self.formLayoutWidget.setContentsMargins(180, 20, 0, 0)
    #     self.formLayoutWidget.setStyleSheet(Style.form_input_box)
    #     self.formLayoutWidget.setObjectName("formLayoutWidget")
    #     self.form_layout_inside_tab = QtWidgets.QFormLayout(self.formLayoutWidget)
    #     self.form_layout_inside_tab.setContentsMargins(0, 0, 0, 0)
    #     self.form_layout_inside_tab.setObjectName("form_layout_inside_tab")
    #
    #     self.projectNameLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
    #     self.projectNameLineEdit.setObjectName("projectNameLineEdit")
    #     self.projectNameLineEdit.setFixedWidth(500)
    #     self.projectNameLineEdit.setDisabled(1)
    #     self.projectNameLineEdit.setPlaceholderText("Enter Project Name")
    #     self.form_layout_inside_tab.setWidget(0, 0, self.projectNameLineEdit)
    #     self.pipeLineOwnerLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
    #     self.pipeLineOwnerLineEdit.setObjectName("pipeLineOwnerLineEdit")
    #     self.pipeLineOwnerLineEdit.setPlaceholderText("Enter pipeLine Owner Name")
    #     self.pipeLineOwnerLineEdit.setFixedWidth(500)
    #     self.form_layout_inside_tab.setWidget(0, 1, self.pipeLineOwnerLineEdit)
    #
    #     self.pipeLineNameLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
    #     self.pipeLineNameLineEdit.setObjectName("pipeLineNameLineEdit")
    #     self.pipeLineNameLineEdit.setPlaceholderText("Enter Pipeline  Name")
    #     self.pipeLineNameLineEdit.setFixedWidth(500)
    #     self.form_layout_inside_tab.setWidget(1, 0, self.pipeLineNameLineEdit)
    #
    #     self.launchLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
    #     self.launchLineEdit.setObjectName("launchLineEdit")
    #     self.launchLineEdit.setPlaceholderText("Launch")
    #     self.launchLineEdit.setFixedWidth(500)
    #     self.form_layout_inside_tab.setWidget(1, 1, self.launchLineEdit)
    #
    #     self.RecieveLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
    #     self.RecieveLineEdit.setObjectName("RecieveLineEdit")
    #     self.RecieveLineEdit.setPlaceholderText("Recieve")
    #     self.RecieveLineEdit.setFixedWidth(500)
    #     self.form_layout_inside_tab.setWidget(2, 0, self.RecieveLineEdit)
    #
    #     self.diemeterLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
    #     self.diemeterLineEdit.setObjectName("diemeterLineEdit")
    #     self.diemeterLineEdit.setPlaceholderText("Diamenter")
    #     self.diemeterLineEdit.setFixedWidth(500)
    #     self.form_layout_inside_tab.setWidget(2, 1, self.diemeterLineEdit)
    #
    #     self.lengthLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
    #     self.lengthLineEdit.setObjectName("lengthLineEdit")
    #     self.lengthLineEdit.setPlaceholderText("Length")
    #     self.lengthLineEdit.setFixedWidth(500)
    #     self.form_layout_inside_tab.setWidget(3, 0, self.lengthLineEdit)
    #
    #     self.steel_gradeLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
    #     self.steel_gradeLineEdit.setObjectName("steel_gradeLineEdit")
    #     self.steel_gradeLineEdit.setPlaceholderText("Steel Grade")
    #     self.steel_gradeLineEdit.setFixedWidth(500)
    #     self.form_layout_inside_tab.setWidget(3, 1, self.steel_gradeLineEdit)
    #
    #     self.Nominal_wallLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
    #     self.Nominal_wallLineEdit.setObjectName("Nominal_wallLineEdit")
    #     self.Nominal_wallLineEdit.setPlaceholderText("Nominal Wall")
    #     self.Nominal_wallLineEdit.setFixedWidth(500)
    #     self.form_layout_inside_tab.setWidget(4, 0, self.Nominal_wallLineEdit)
    #
    #     self.pipe_typeLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
    #     self.pipe_typeLineEdit.setObjectName("pipe_typeLineEdit")
    #     self.pipe_typeLineEdit.setPlaceholderText("Pipe Type")
    #     self.pipe_typeLineEdit.setFixedWidth(500)
    #     self.form_layout_inside_tab.setWidget(4, 1, self.pipe_typeLineEdit)
    #
    #     self.MAOP_entryLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
    #     self.MAOP_entryLineEdit.setObjectName("MAOP_entryLineEdit")
    #     self.MAOP_entryLineEdit.setPlaceholderText("MAOP Entry")
    #     self.MAOP_entryLineEdit.setFixedWidth(500)
    #     self.form_layout_inside_tab.setWidget(5, 0, self.MAOP_entryLineEdit)
    #
    #     self.design_pressureLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
    #     self.design_pressureLineEdit.setObjectName("design_pressureLineEdit")
    #     self.design_pressureLineEdit.setPlaceholderText("Design Pressure")
    #     self.design_pressureLineEdit.setFixedWidth(500)
    #     self.form_layout_inside_tab.setWidget(5, 1, self.design_pressureLineEdit)
    #
    #     self.defect_assessmentLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
    #     self.defect_assessmentLineEdit.setObjectName("defect_assessmentLineEdit")
    #     self.defect_assessmentLineEdit.setPlaceholderText("Defect Assessment")
    #     self.defect_assessmentLineEdit.setFixedWidth(500)
    #     self.form_layout_inside_tab.setWidget(6, 0, self.defect_assessmentLineEdit)
    #
    #     self.year_of_commissioningLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
    #     self.year_of_commissioningLineEdit.setObjectName("year_of_commissioningLineEdit")
    #     self.year_of_commissioningLineEdit.setPlaceholderText("Year of Commissioning")
    #     self.year_of_commissioningLineEdit.setFixedWidth(500)
    #     self.form_layout_inside_tab.setWidget(6, 1, self.year_of_commissioningLineEdit)
    #
    #     self.inspection_historyLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
    #     self.inspection_historyLineEdit.setObjectName("inspection_historyLineEdit")
    #     self.inspection_historyLineEdit.setPlaceholderText("Inspection History")
    #     self.inspection_historyLineEdit.setFixedWidth(500)
    #     self.form_layout_inside_tab.setWidget(7, 0, self.inspection_historyLineEdit)
    #
    #     self.pipeline_productLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
    #     self.pipeline_productLineEdit.setObjectName("pipeline_productLineEdit")
    #     self.pipeline_productLineEdit.setPlaceholderText("PipeLine Product")
    #     self.pipeline_productLineEdit.setFixedWidth(500)
    #     self.form_layout_inside_tab.setWidget(7, 1, self.pipeline_productLineEdit)
    #
    #     self.pushButton = QtWidgets.QPushButton(self.formLayoutWidget)
    #     self.pushButton.setObjectName("upload_file")
    #     self.pushButton.setText("Attach File")
    #     self.pushButton.clicked.connect(self.upload_data)
    #     self.form_layout_inside_tab.setWidget(8, 0, self.pushButton)
    #     self.pushButton.setFixedWidth(500)
    #     self.pushButton.setStyleSheet(Style.shared_button_style)
    #
    #     self.btn1 = QtWidgets.QPushButton(self.formLayoutWidget)
    #     self.btn1.setObjectName("update_data")
    #     self.btn1.setText("Update")
    #     self.btn1.clicked.connect(self.update_data)
    #     self.form_layout_inside_tab.setWidget(8, 1, self.btn1)
    #     self.btn1.setFixedWidth(500)
    #     self.btn1.setStyleSheet(Style.shared_button_style)
    #
    #     tab_updatelayout.addWidget(self.formLayoutWidget)
    #     tab_update.setLayout(tab_updatelayout)

    def _init_form_layout(self, tab_update, tab_updatelayout):
        # Outer widget for the form
        self.formLayoutWidget = QtWidgets.QWidget()
        self.formLayoutWidget.setStyleSheet(Style.form_input_box)
        self.formLayoutWidget.setObjectName("formLayoutWidget")

        # Form layout inside
        self.form_layout_inside_tab = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.form_layout_inside_tab.setContentsMargins(20, 20, 20, 20)
        self.form_layout_inside_tab.setSpacing(15)
        self.form_layout_inside_tab.setObjectName("form_layout_inside_tab")

        # --- Header title ---
        title = QtWidgets.QLabel("Update Project Details")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        self.form_layout_inside_tab.setWidget(0, QtWidgets.QFormLayout.SpanningRole, title)

        # --- Input fields ---
        self.projectNameLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.projectNameLineEdit.setObjectName("projectNameLineEdit")
        self.projectNameLineEdit.setFixedWidth(500)
        self.projectNameLineEdit.setDisabled(1)
        self.projectNameLineEdit.setPlaceholderText("Enter Project Name")
        self.form_layout_inside_tab.setWidget(1, 0, self.projectNameLineEdit)

        self.pipeLineOwnerLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.pipeLineOwnerLineEdit.setObjectName("pipeLineOwnerLineEdit")
        self.pipeLineOwnerLineEdit.setPlaceholderText("Enter Pipeline Owner Name")
        self.pipeLineOwnerLineEdit.setFixedWidth(500)
        self.form_layout_inside_tab.setWidget(1, 1, self.pipeLineOwnerLineEdit)

        self.pipeLineNameLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.pipeLineNameLineEdit.setObjectName("pipeLineNameLineEdit")
        self.pipeLineNameLineEdit.setPlaceholderText("Enter Pipeline Name")
        self.pipeLineNameLineEdit.setFixedWidth(500)
        self.form_layout_inside_tab.setWidget(2, 0, self.pipeLineNameLineEdit)

        self.launchLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.launchLineEdit.setObjectName("launchLineEdit")
        self.launchLineEdit.setPlaceholderText("Launch")
        self.launchLineEdit.setFixedWidth(500)
        self.form_layout_inside_tab.setWidget(2, 1, self.launchLineEdit)

        self.RecieveLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.RecieveLineEdit.setObjectName("RecieveLineEdit")
        self.RecieveLineEdit.setPlaceholderText("Receive")
        self.RecieveLineEdit.setFixedWidth(500)
        self.form_layout_inside_tab.setWidget(3, 0, self.RecieveLineEdit)

        self.diemeterLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.diemeterLineEdit.setObjectName("diemeterLineEdit")
        self.diemeterLineEdit.setPlaceholderText("Diameter")
        self.diemeterLineEdit.setFixedWidth(500)
        self.form_layout_inside_tab.setWidget(3, 1, self.diemeterLineEdit)

        self.lengthLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lengthLineEdit.setObjectName("lengthLineEdit")
        self.lengthLineEdit.setPlaceholderText("Length")
        self.lengthLineEdit.setFixedWidth(500)
        self.form_layout_inside_tab.setWidget(4, 0, self.lengthLineEdit)

        self.steel_gradeLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.steel_gradeLineEdit.setObjectName("steel_gradeLineEdit")
        self.steel_gradeLineEdit.setPlaceholderText("Steel Grade")
        self.steel_gradeLineEdit.setFixedWidth(500)
        self.form_layout_inside_tab.setWidget(4, 1, self.steel_gradeLineEdit)

        self.Nominal_wallLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Nominal_wallLineEdit.setObjectName("Nominal_wallLineEdit")
        self.Nominal_wallLineEdit.setPlaceholderText("Nominal Wall")
        self.Nominal_wallLineEdit.setFixedWidth(500)
        self.form_layout_inside_tab.setWidget(5, 0, self.Nominal_wallLineEdit)

        self.pipe_typeLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.pipe_typeLineEdit.setObjectName("pipe_typeLineEdit")
        self.pipe_typeLineEdit.setPlaceholderText("Pipe Type")
        self.pipe_typeLineEdit.setFixedWidth(500)
        self.form_layout_inside_tab.setWidget(5, 1, self.pipe_typeLineEdit)

        self.MAOP_entryLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.MAOP_entryLineEdit.setObjectName("MAOP_entryLineEdit")
        self.MAOP_entryLineEdit.setPlaceholderText("MAOP Entry")
        self.MAOP_entryLineEdit.setFixedWidth(500)
        self.form_layout_inside_tab.setWidget(6, 0, self.MAOP_entryLineEdit)

        self.design_pressureLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.design_pressureLineEdit.setObjectName("design_pressureLineEdit")
        self.design_pressureLineEdit.setPlaceholderText("Design Pressure")
        self.design_pressureLineEdit.setFixedWidth(500)
        self.form_layout_inside_tab.setWidget(6, 1, self.design_pressureLineEdit)

        self.defect_assessmentLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.defect_assessmentLineEdit.setObjectName("defect_assessmentLineEdit")
        self.defect_assessmentLineEdit.setPlaceholderText("Defect Assessment")
        self.defect_assessmentLineEdit.setFixedWidth(500)
        self.form_layout_inside_tab.setWidget(7, 0, self.defect_assessmentLineEdit)

        self.year_of_commissioningLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.year_of_commissioningLineEdit.setObjectName("year_of_commissioningLineEdit")
        self.year_of_commissioningLineEdit.setPlaceholderText("Year of Commissioning")
        self.year_of_commissioningLineEdit.setFixedWidth(500)
        self.form_layout_inside_tab.setWidget(7, 1, self.year_of_commissioningLineEdit)

        self.inspection_historyLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.inspection_historyLineEdit.setObjectName("inspection_historyLineEdit")
        self.inspection_historyLineEdit.setPlaceholderText("Inspection History")
        self.inspection_historyLineEdit.setFixedWidth(500)
        self.form_layout_inside_tab.setWidget(8, 0, self.inspection_historyLineEdit)

        self.pipeline_productLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.pipeline_productLineEdit.setObjectName("pipeline_productLineEdit")
        self.pipeline_productLineEdit.setPlaceholderText("Pipeline Product")
        self.pipeline_productLineEdit.setFixedWidth(500)
        self.form_layout_inside_tab.setWidget(8, 1, self.pipeline_productLineEdit)

        # --- Buttons ---
        self.pushButton = QtWidgets.QPushButton(self.formLayoutWidget)
        self.pushButton.setObjectName("upload_file")
        self.pushButton.setText("Attach File")
        self.pushButton.clicked.connect(self.upload_data)
        self.pushButton.setFixedWidth(500)
        self.pushButton.setStyleSheet(Style.btn_type_secondary)  # grey style
        self.form_layout_inside_tab.setWidget(9, 0, self.pushButton)

        self.btn1 = QtWidgets.QPushButton(self.formLayoutWidget)
        self.btn1.setObjectName("update_data")
        self.btn1.setText("Update")
        self.btn1.clicked.connect(self.update_data)
        self.btn1.setFixedWidth(500)
        self.btn1.setStyleSheet(Style.btn_type_primary)  # blue style
        self.form_layout_inside_tab.setWidget(9, 1, self.btn1)

        # --- Center the whole form horizontally ---
        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.formLayoutWidget)
        hbox.addStretch(1)

        tab_updatelayout.addLayout(hbox)
        tab_update.setLayout(tab_updatelayout)
        tab_update.setStyleSheet("background-color: #EDF6FF;")

    def set_previous_form_data(self, company_name):
        self.company = company_name
        with Config.connection.cursor() as cursor:
            cursor.execute(
                "SELECT `runid`,`Pipeline_owner`,`Pipeline_Name`,`Launch`,`Receive`,`Diameter`,`Length`,`Steel_grade`,`Nominal_wall`,`Pipe_type`,`MAOP_entry`,`Design_pressure`,`Defect_Assessment`,`Year_of_commissioning`,`Inspection_history`,`Pipeline_product` FROM projectdetail WHERE ProjectName='" + str(
                    company_name) + "'")
            self.allSQLRows = cursor.fetchall()
            print(self.allSQLRows)
            self.runid = self.allSQLRows[0][0]
            self.Pipeline_owner = self.allSQLRows[0][1]
            self.Pipeline_Name = self.allSQLRows[0][2]
            self.Launch = self.allSQLRows[0][3]
            self.Receive = self.allSQLRows[0][4]
            self.Diameter = self.allSQLRows[0][5]
            self.Length = self.allSQLRows[0][6]
            self.Steel_grade = self.allSQLRows[0][7]
            self.Nominal_wall = self.allSQLRows[0][8]
            self.Pipe_type = self.allSQLRows[0][9]
            self.MAOP_entry = self.allSQLRows[0][10]
            self.Design_pressure = self.allSQLRows[0][11]
            self.Defect_Assessment = self.allSQLRows[0][12]
            self.Year_of_commissioning = self.allSQLRows[0][13]
            self.Inspection_history = self.allSQLRows[0][14]
            self.Pipeline_product = self.allSQLRows[0][15]

        self.projectNameLineEdit.setText(str(company_name))
        self.pipeLineOwnerLineEdit.setText(self.Pipeline_owner)
        self.pipeLineNameLineEdit.setText(self.Pipeline_Name)
        self.launchLineEdit.setText(self.Launch)
        self.RecieveLineEdit.setText(self.Receive)
        self.diemeterLineEdit.setText(str(self.Diameter))
        self.lengthLineEdit.setText(str(self.Length))
        self.steel_gradeLineEdit.setText(self.Steel_grade)
        self.Nominal_wallLineEdit.setText(self.Nominal_wall)
        self.pipe_typeLineEdit.setText(self.Pipe_type)
        self.MAOP_entryLineEdit.setText(self.MAOP_entry)
        self.design_pressureLineEdit.setText(self.Design_pressure)
        self.defect_assessmentLineEdit.setText(self.Defect_Assessment)
        self.year_of_commissioningLineEdit.setText(self.Year_of_commissioning)
        self.inspection_historyLineEdit.setText(self.Inspection_history)
        self.pipeline_productLineEdit.setText(self.Pipeline_product)
        return self.runid


    def update_data(self):
        company_name = self.company
        Pipeline_owner = self.pipeLineOwnerLineEdit.text()
        Pipeline_Name = self.pipeLineNameLineEdit.text()
        Launch = self.launchLineEdit.text()
        Receive = self.RecieveLineEdit.text()
        Diameter = self.diemeterLineEdit.text()
        Length = self.lengthLineEdit.text()
        Steel_grade = self.steel_gradeLineEdit.text()
        Nominal_wall = self.Nominal_wallLineEdit.text()
        Pipe_type = self.pipe_typeLineEdit.text()
        MAOP_entry = self.MAOP_entryLineEdit.text()
        Design_pressure = self.design_pressureLineEdit.text()
        Defect_Assessment = self.defect_assessmentLineEdit.text()
        Year_of_commissioning = self.year_of_commissioningLineEdit.text()
        Inspection_history = self.inspection_historyLineEdit.text()
        Pipeline_product = self.pipeline_productLineEdit.text()

        try:
            with Config.connection.cursor() as cursor:
                if (
                        company_name and Pipeline_owner and Pipeline_Name and Launch and Receive and Diameter and Length and Steel_grade and Nominal_wall
                        and Pipe_type and MAOP_entry and Design_pressure and Defect_Assessment and Year_of_commissioning and Inspection_history and Pipeline_product != ""):
                    query = 'UPDATE projectdetail SET  Pipeline_owner="' + str(
                        Pipeline_owner) + '", Pipeline_Name="' + str(Pipeline_Name) + '", Launch="' + str(
                        Launch) + '", Receive="' + str(Receive) + '",' \
                                                                  'Diameter="' + str(
                        Diameter) + '",Length="' + str(Length) + '",Steel_grade="' + str(
                        Steel_grade) + '",Nominal_wall="' + str(Nominal_wall) + '",Pipe_type="' + str(
                        Pipe_type) + '",MAOP_entry="' + str(MAOP_entry) + '",Design_pressure="' + str(
                        Design_pressure) + '",' \
                                           'Defect_Assessment="' + str(
                        Defect_Assessment) + '", Year_of_commissioning="' + str(
                        Year_of_commissioning) + '", Inspection_history="' + str(
                        Inspection_history) + '", Pipeline_product="' + str(
                        Pipeline_product) + '" WHERE ProjectName="' + str(company_name) + '"'

                    print(query)
                    print(cursor.execute(query))
                    Config.connection.commit()
                    Config.info_msg("Form has been updated successfully", "")
                    logger.log_info("Form has been updated successfully for " + company_name)
                else:
                    Config.warning_msg("Some field a"
                                       "re empty","")
        except:
            logger.log_error('Form updation failed for ' + company_name)
            Config.warning_msg('Form updation failed for ' + company_name, "")

    def upload_data(self):
        try:
            runid=self.runid
            dir = QFileDialog.getExistingDirectory()
            Upload.upload_data(dir, runid)

        except:
            Config.warning_msg('runid is not found')

    # def folder_location(self, a, bucket_name, gcs_folder):
    #     print(a,bucket_name,gcs_folder)
    #     try:
    #         os.mkdir(a + "\\runid")
    #     except:
    #         print("file has been created")
    #     runid = self.runid
    #     print(runid)
    #     new_runid = "," + str(runid)
    #     #print("new_runid",new_runid)
    #     fin = open("runid.txt","rt")
    #     print("1 here")
    #     data = fin.read()
    #     data = data.replace(',1', new_runid)
    #     fin.close()
    #     fin = open(a + "\\runid\\runid.txt", "wt")
    #     fin.write(data)
    #     fin.close()
    #     print("reached")
    #     storage_client = Config.storage_client
    #     bucket = storage_client.bucket(bucket_name)
    #     assert os.path.isdir(a)
    #     for local_folder in os.listdir(a):
    #         for local_file in os.listdir(a + '/' + local_folder):
    #             remote_path = gcs_folder + '/' + local_folder + '/' + local_file
    #             blob = bucket.blob(remote_path)
    #             file_location = a + '/' + local_folder + '/' + local_file
    #             blob.upload_from_filename(file_location)
    #     Config.info_msg("Data is uploaded Successfully", "")
    #
    # def upload_data(self):
    #     try:
    #         b = QFileDialog.getExistingDirectory()
    #         self.folder_location(b, 'tempbucket_for_bigquery', self.company)
    #     except:
    #         Config.warning_msg("Internet speed is slow or Folder hierarchy is invalid", "")
    #         logger.log_error("Internet speed is slow or Folder hierarchy is invalid")
