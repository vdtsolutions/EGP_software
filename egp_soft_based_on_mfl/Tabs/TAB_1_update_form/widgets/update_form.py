
from PyQt5 import QtWidgets, QtCore
from egp_soft_based_on_mfl.Components import style1 as Style
import egp_soft_based_on_mfl.Components.Upload_data as Upload
from egp_soft_based_on_mfl.Components import logger

# from egp_soft_based_on_mfl.Components.self.configs import self.config as self.config
class UpdateForm(QtWidgets.QWidget):
    """Modular Update Form (safe, self-contained)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.config = self.parent.config
        # === Base styling ===
        self.setStyleSheet("background-color: #EDF6FF;")

        # === Build main layout ===
        outer_layout = QtWidgets.QVBoxLayout(self)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)

        # === Form container ===
        self.formLayoutWidget = QtWidgets.QWidget(self)
        self.formLayoutWidget.setStyleSheet(Style.form_input_box)

        self.form_layout_inside_tab = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.form_layout_inside_tab.setContentsMargins(20, 20, 20, 20)
        self.form_layout_inside_tab.setSpacing(15)

        # === Title ===
        title = QtWidgets.QLabel("Update Project Details", self)
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        self.form_layout_inside_tab.setWidget(0, QtWidgets.QFormLayout.SpanningRole, title)

        # === Input fields ===
        self.projectNameLineEdit = self._create_lineedit("Enter Project Name", disabled=True)
        self.pipeLineOwnerLineEdit = self._create_lineedit("Enter Client Name")
        self.pipeLineNameLineEdit = self._create_lineedit("Enter Pipeline Name")
        self.launchLineEdit = self._create_lineedit("Launch")
        self.RecieveLineEdit = self._create_lineedit("Receive")
        self.diemeterLineEdit = self._create_lineedit("Diameter")
        self.lengthLineEdit = self._create_lineedit("Length")
        self.steel_gradeLineEdit = self._create_lineedit("Steel Grade")
        self.Nominal_wallLineEdit = self._create_lineedit("Nominal Wall")
        self.pipe_typeLineEdit = self._create_lineedit("Pipe Type")
        self.MAOP_entryLineEdit = self._create_lineedit("MAOP Entry")
        self.design_pressureLineEdit = self._create_lineedit("Design Pressure")
        self.defect_assessmentLineEdit = self._create_lineedit("Defect Assessment")
        self.year_of_commissioningLineEdit = self._create_lineedit("Year of Commissioning")
        self.inspection_historyLineEdit = self._create_lineedit("Inspection History")
        self.pipeline_productLineEdit = self._create_lineedit("Pipeline Product")

        # === Place fields in grid ===
        fields = [
            (self.projectNameLineEdit, self.pipeLineOwnerLineEdit),
            (self.pipeLineNameLineEdit, self.launchLineEdit),
            (self.RecieveLineEdit, self.diemeterLineEdit),
            (self.lengthLineEdit, self.steel_gradeLineEdit),
            (self.Nominal_wallLineEdit, self.pipe_typeLineEdit),
            (self.MAOP_entryLineEdit, self.design_pressureLineEdit),
            (self.defect_assessmentLineEdit, self.year_of_commissioningLineEdit),
            (self.inspection_historyLineEdit, self.pipeline_productLineEdit),
        ]

        for i, (left, right) in enumerate(fields, start=1):
            self.form_layout_inside_tab.setWidget(i, 0, left)
            self.form_layout_inside_tab.setWidget(i, 1, right)

        # === Buttons ===
        self.pushButton = QtWidgets.QPushButton("Attach File", self)
        self.pushButton.setStyleSheet(Style.btn_type_secondary)
        self.pushButton.setFixedWidth(500)
        self.pushButton.clicked.connect(self.upload_data)

        self.btn1 = QtWidgets.QPushButton("Update", self)
        self.btn1.setStyleSheet(Style.btn_type_primary)
        self.btn1.setFixedWidth(500)
        self.btn1.clicked.connect(self.update_data)

        self.form_layout_inside_tab.setWidget(len(fields) + 1, 0, self.pushButton)
        self.form_layout_inside_tab.setWidget(len(fields) + 1, 1, self.btn1)

        hbox.addWidget(self.formLayoutWidget)
        hbox.addStretch(1)
        outer_layout.addLayout(hbox)

        # === Internal data vars ===
        self.company = None
        self.runid = None


    # -------------------------------------------------------------------------
    # Utility: create a pre-styled QLineEdit
    # -------------------------------------------------------------------------
    def _create_lineedit(self, placeholder, disabled=False):
        le = QtWidgets.QLineEdit(self.formLayoutWidget)
        le.setPlaceholderText(placeholder)
        le.setFixedWidth(500)
        le.setDisabled(disabled)
        return le

    # -------------------------------------------------------------------------
    # Set values from database
    # -------------------------------------------------------------------------
    def set_previous_form_data(self, company_name):
        self.company = company_name
        with self.config.connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT `runid`,`Pipeline_owner`,`Pipeline_Name`,`Launch`,`Receive`,`Diameter`,`Length`,
                `Steel_grade`,`Nominal_wall`,`Pipe_type`,`MAOP_entry`,`Design_pressure`,`Defect_Assessment`,
                `Year_of_commissioning`,`Inspection_history`,`Pipeline_product`
                FROM projectdetail WHERE ProjectName='{company_name}'"""
            )
            rows = cursor.fetchall()

            if not rows:
                self.config.warning_msg("No records found", "")
                return

            (self.runid,
             Pipeline_owner, Pipeline_Name, Launch, Receive, Diameter, Length, Steel_grade,
             Nominal_wall, Pipe_type, MAOP_entry, Design_pressure, Defect_Assessment,
             Year_of_commissioning, Inspection_history, Pipeline_product) = rows[0]

        # Populate UI fields
        self.projectNameLineEdit.setText(company_name)
        self.pipeLineOwnerLineEdit.setText(Pipeline_owner)
        self.pipeLineNameLineEdit.setText(Pipeline_Name)
        self.launchLineEdit.setText(Launch)
        self.RecieveLineEdit.setText(Receive)
        self.diemeterLineEdit.setText(str(Diameter))
        self.lengthLineEdit.setText(str(Length))
        self.steel_gradeLineEdit.setText(Steel_grade)
        self.Nominal_wallLineEdit.setText(Nominal_wall)
        self.pipe_typeLineEdit.setText(Pipe_type)
        self.MAOP_entryLineEdit.setText(MAOP_entry)
        self.design_pressureLineEdit.setText(Design_pressure)
        self.defect_assessmentLineEdit.setText(Defect_Assessment)
        self.year_of_commissioningLineEdit.setText(Year_of_commissioning)
        self.inspection_historyLineEdit.setText(Inspection_history)
        self.pipeline_productLineEdit.setText(Pipeline_product)

        return self.runid

    # -------------------------------------------------------------------------
    # Update database
    # -------------------------------------------------------------------------
    def update_data(self):
        company_name = self.company
        if not company_name:
            self.config.warning_msg("No company loaded", "")
            return

        fields = {
            "Pipeline_owner": self.pipeLineOwnerLineEdit.text(),
            "Pipeline_Name": self.pipeLineNameLineEdit.text(),
            "Launch": self.launchLineEdit.text(),
            "Receive": self.RecieveLineEdit.text(),
            "Diameter": self.diemeterLineEdit.text(),
            "Length": self.lengthLineEdit.text(),
            "Steel_grade": self.steel_gradeLineEdit.text(),
            "Nominal_wall": self.Nominal_wallLineEdit.text(),
            "Pipe_type": self.pipe_typeLineEdit.text(),
            "MAOP_entry": self.MAOP_entryLineEdit.text(),
            "Design_pressure": self.design_pressureLineEdit.text(),
            "Defect_Assessment": self.defect_assessmentLineEdit.text(),
            "Year_of_commissioning": self.year_of_commissioningLineEdit.text(),
            "Inspection_history": self.inspection_historyLineEdit.text(),
            "Pipeline_product": self.pipeline_productLineEdit.text(),
        }

        # Validation
        if not all(fields.values()):
            self.config.warning_msg("Some fields are empty", "")
            return

        query = (
            "UPDATE projectdetail SET " +
            ", ".join(f"{k}='{v}'" for k, v in fields.items()) +
            f" WHERE ProjectName='{company_name}'"
        )

        try:
            with self.config.connection.cursor() as cursor:
                cursor.execute(query)
                self.config.connection.commit()
                self.config.info_msg("Form has been updated successfully", "")
                logger.log_info(f"Form updated for {company_name}")
        except Exception as e:
            logger.log_error(f"Form update failed for {company_name}: {e}")
            self.config.warning_msg("Form update failed", str(e))

    # -------------------------------------------------------------------------
    # Upload file
    # -------------------------------------------------------------------------
    def upload_data(self):
        try:
            runid = self.runid
            directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Upload Folder")
            if directory:
                Upload.upload_data(directory, runid)
        except Exception as e:
            self.config.warning_msg("Error uploading data", str(e))
