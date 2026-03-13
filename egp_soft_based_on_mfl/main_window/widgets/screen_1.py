# #
# import egp_soft_based_on_mfl.Components.style1 as Style
# from PyQt5 import QtCore, QtWidgets
# from egp_soft_based_on_mfl.Components.Configs.pipe_inch import pipe_inch
# from PyQt5 import QtCore, QtWidgets, QtGui
#
#
# def build_screen1(self):
#     self.screen1 = QtWidgets.QWidget()
#     layout = QtWidgets.QVBoxLayout(self.screen1)
#     layout.setAlignment(QtCore.Qt.AlignCenter)
#
#     # Adjustable card size
#     CARD_WIDTH = 500
#     CARD_HEIGHT = 420
#
#     # Dark Material Card
#     card = QtWidgets.QFrame()
#     card.setObjectName("selectionCard")
#     card.setFixedWidth(CARD_WIDTH)
#     card.setFixedHeight(CARD_HEIGHT)
#
#     card.setStyleSheet("""
#         QFrame#selectionCard {
#             background-color: #1F222A;
#             border-radius: 18px;
#             border: 1px solid #2E323C;
#         }
#     """)
#
#     shadow = QtWidgets.QGraphicsDropShadowEffect(card)
#     shadow.setBlurRadius(40)
#     shadow.setOffset(0, 12)
#     shadow.setColor(QtGui.QColor(0, 0, 0, 160))
#     card.setGraphicsEffect(shadow)
#
#     card_layout = QtWidgets.QVBoxLayout(card)
#     card_layout.setContentsMargins(32, 28, 32, 28)
#     card_layout.setSpacing(22)
#     card_layout.setAlignment(QtCore.Qt.AlignTop)
#
#     # Header
#     header_layout = QtWidgets.QHBoxLayout()
#     header_layout.setSpacing(10)
#
#     icon_label = QtWidgets.QLabel(" ")
#     icon_label.setStyleSheet("font: 20pt 'Segoe UI';")
#     header_layout.addWidget(icon_label)
#
#     title_label = QtWidgets.QLabel("Pipeline Selection")
#     title_label.setStyleSheet("""
#         QLabel { font: 600 17pt 'Segoe UI'; color: #FFFFFF; }
#     """)
#     header_layout.addWidget(title_label)
#     header_layout.addStretch(1)
#     card_layout.addLayout(header_layout)
#
#     subtitle = QtWidgets.QLabel("Choose the pipeline inch and project to continue.")
#     subtitle.setStyleSheet("font: 9.5pt 'Segoe UI'; color: #A0A4B0;")
#     card_layout.addWidget(subtitle)
#
#     # ─────────────────────────────────────────────
#     # INCH DROPDOWN (with placeholder)
#     # ─────────────────────────────────────────────
#     inch_block = QtWidgets.QVBoxLayout()
#     inch_label = QtWidgets.QLabel("Project Inch")
#     inch_label.setStyleSheet("font: 10.5pt 'Segoe UI'; color: #D5D8E3;")
#     inch_block.addWidget(inch_label)
#
#     self.combo_inch = QtWidgets.QComboBox()
#
#     self.combo_inch.addItem("Select Project Inch")
#     self.combo_inch.model().item(0).setEnabled(False)
#     self.combo_inch.model().item(0).setForeground(QtGui.QColor("#888"))
#
#     for inch in pipe_inch:
#         self.combo_inch.addItem(inch)
#
#     self.combo_inch.setStyleSheet("""
#         QComboBox {
#             background-color: #272B35;
#             color: #E5E7F0;
#             padding: 8px 10px;
#             font: 10.5pt 'Segoe UI';
#             border-radius: 10px;
#             border: 1px solid #3A3F4D;
#         }
#         QComboBox::drop-down { border: none; width: 30px; }
#         QComboBox::down-arrow {
#             image: url(:/qt-project.org/styles/commonstyle/images/arrowdown.png);
#             width: 14px; height: 14px;
#         }
#         QComboBox:hover { border: 1px solid #4C8DFF; }
#     """)
#
#     self.combo_inch.currentIndexChanged.connect(lambda index: on_inch_changed(self, index))
#     inch_block.addWidget(self.combo_inch)
#     card_layout.addLayout(inch_block)
#
#     # ─────────────────────────────────────────────
#     # PROJECT DROPDOWN (with placeholder)
#     # ─────────────────────────────────────────────
#     project_block = QtWidgets.QVBoxLayout()
#     project_label = QtWidgets.QLabel("Project")
#     project_label.setStyleSheet("font: 10.5pt 'Segoe UI'; color: #D5D8E3;")
#     project_block.addWidget(project_label)
#
#     self.combo_project = QtWidgets.QComboBox()
#     self.combo_project.setEnabled(False)
#
#     self.combo_project.addItem("Select Project")
#     self.combo_project.model().item(0).setEnabled(False)
#     self.combo_project.model().item(0).setForeground(QtGui.QColor("#888"))
#
#     self.combo_project.setStyleSheet("""
#         QComboBox {
#             background-color: #272B35;
#             color: #E5E7F0;
#             padding: 8px 10px;
#             font: 10.5pt 'Segoe UI';
#             border-radius: 10px;
#             border: 1px solid #3A3F4D;
#         }
#         QComboBox::drop-down { border: none; width: 30px; }
#         QComboBox::down-arrow {
#             image: url(:/qt-project.org/styles/commonstyle/images/arrowdown.png);
#             width: 14px; height: 14px;
#         }
#         QComboBox:disabled {
#             background-color: #20232C;
#             color: #777B88;
#             border: 1px solid #323642;
#         }
#     """)
#
#     self.combo_project.currentIndexChanged.connect(lambda index: on_project_changed(self, index))
#     project_block.addWidget(self.combo_project)
#     card_layout.addLayout(project_block)
#
#     # ─────────────────────────────────────────────
#     # BUTTONS
#     # ─────────────────────────────────────────────
#     btn_layout = QtWidgets.QHBoxLayout()
#     btn_layout.addStretch(1)
#
#     self.btn_apply = QtWidgets.QPushButton("Apply & Load")
#     self.btn_apply.setEnabled(False)
#     self.btn_apply.setFixedHeight(38)
#     self.btn_apply.setStyleSheet("""
#         QPushButton {
#             background-color: #4C8DFF;
#             color: white;
#             font: 10.5pt 'Segoe UI';
#             padding: 6px 18px;
#             border-radius: 10px;
#         }
#         QPushButton:hover:!disabled { background-color: #3C78E0; }
#         QPushButton:disabled {
#             background-color: #324D7D;
#             color: #AEB8E5;
#         }
#     """)
#
#     self.btn_apply.clicked.connect(lambda: on_apply_clicked(self))
#
#     self.btn_reset = QtWidgets.QPushButton("Reset")
#     self.btn_reset.setFixedHeight(38)
#     self.btn_reset.setStyleSheet("""
#         QPushButton {
#             background-color: #272B35;
#             color: #D5D8E3;
#             font: 10.5pt 'Segoe UI';
#             padding: 6px 18px;
#             border-radius: 10px;
#             border: 1px solid #3A3F4D;
#         }
#         QPushButton:hover { background-color: #303543; }
#     """)
#
#     self.btn_reset.clicked.connect(lambda: reset_selection(self))
#
#     btn_layout.addWidget(self.btn_apply)
#     btn_layout.addSpacing(10)
#     btn_layout.addWidget(self.btn_reset)
#     card_layout.addLayout(btn_layout)
#
#     layout.addWidget(card, alignment=QtCore.Qt.AlignCenter)
#
# def on_apply_clicked(self):
#     """Load the selected project when Apply is pressed."""
#     selected_project = self.combo_project.currentText()
#     if not selected_project:
#         QtWidgets.QMessageBox.warning(
#             self, "Missing Selection", "Please select a project."
#         )
#         return
#
#     print("Loading project:", selected_project)
#     self.project_name = selected_project
#     load_selected_project(self, selected_project)  # your existing function
#
# def on_inch_changed(self, index):
#     if index <= 0:
#         return   # ignore placeholder
#     apply_inch_selection_direct(self)
#
#
# def apply_inch_selection_direct(self):
#     from egp_soft_based_on_mfl.Components.Configs.config_loader import (
#         get_inch_config, set_config
#     )
#
#     self.selected_inch = self.combo_inch.currentText()
#     print("Selected inch:", self.selected_inch)
#
#     self.config = get_inch_config(self.selected_inch)
#     set_config(self.config)
#     self.config.init_runtime()
#
#     #Fetch project list
#     try:
#         with self.config.connection.cursor() as cursor:
#             cursor.execute("SELECT `ProjectName` FROM projectdetail ORDER BY runid DESC")
#             projects = [row[0] for row in cursor.fetchall()]
#     except Exception as e:
#         print("DB error:", e)
#         projects = ["Demo A", "Demo B", "Demo C"]
#
#
#     self.combo_project.setEnabled(True)
#
#     # Reset project dropdown with placeholder
#     self.combo_project.blockSignals(True)
#     self.combo_project.clear()
#     self.combo_project.addItem("Select Project")
#     self.combo_project.model().item(0).setEnabled(False)
#     self.combo_project.model().item(0).setForeground(QtGui.QColor("#888"))
#
#     for p in projects:
#         self.combo_project.addItem(p)
#
#     self.combo_project.setCurrentIndex(0)
#     self.combo_project.blockSignals(False)
#
#     self.btn_apply.setEnabled(False)
#
#
# def on_project_changed(self, index):
#     if index <= 0:
#         self.btn_apply.setEnabled(False)
#     else:
#         self.btn_apply.setEnabled(True)
#
#
#
# def reset_selection(self):
#     print("Resetting selections...")
#
#     # Reset inch dropdown
#     self.combo_inch.blockSignals(True)
#     self.combo_inch.setCurrentIndex(0)
#     self.combo_inch.blockSignals(False)
#
#     # Reset project dropdown
#     self.combo_project.blockSignals(True)
#     self.combo_project.clear()
#     self.combo_project.addItem("Select Project")
#     self.combo_project.model().item(0).setEnabled(False)
#     self.combo_project.model().item(0).setForeground(QtGui.QColor("#888"))
#     self.combo_project.setEnabled(False)
#     self.combo_project.blockSignals(False)
#
#     self.btn_apply.setEnabled(False)
#
#     # Hide menubar if used
#     if hasattr(self, "menubar"):
#         self.menubar.setVisible(False)
#
#
# def load_selected_project(self, project_name):
#     print(f"📂 Loading project: {project_name}")
#     self.project_name = project_name
#
#     # Build all tabs inside Screen2
#     self.init_tab()
#
#     # Load previous form data for update tab
#     self.runid = self.tab_update.set_previous_form_data(project_name)
#     print(f"selected run id : {self.runid}")
#
#     # Set tab names (optional)
#     self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_update), "🔄 Pipeline Detail")
#     self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_weld_selection), "⚙️ Weld Selection")
#     self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_showData), "📊 Data Table")
#     self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_line1.tab_line1),
#                                     "📈 Linechart - Counter vs Sensor")
#     self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_line_orientation),
#                                     "Linechart - Absolute vs Orientation")
#     self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_visualize),
#                                     "🌐 Pipe Visualization")
#     self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.continue_heatmap_tab),
#                                     "Heatmap - Abs vs Orientation")
#     self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.Graph1), "📉 Graph")
#
#     # 👉 SWITCH TO MAIN APPLICATION SCREEN
#     self.stack.setCurrentIndex(1)
#
#     # 👉 SHOW MENUBAR
#     self.menubar.setVisible(True)




from PyQt5 import QtCore, QtWidgets, QtGui

from egp_soft_based_on_mfl.Components.Configs.gcp_and_db_config import init_gcp_backend, create_db_connection
from egp_soft_based_on_mfl.Components.Configs.pipe_inch import pipe_inch
from egp_soft_based_on_mfl.main_window.widgets.menubar.file_menu.create_project import create_project


def build_screen1(self):
    self.screen1 = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(self.screen1)
    layout.setAlignment(QtCore.Qt.AlignCenter)

    # Adjustable card size
    CARD_WIDTH = 500
    CARD_HEIGHT = 470

    # Dark Material Card
    card = QtWidgets.QFrame()
    card.setObjectName("selectionCard")
    card.setFixedWidth(CARD_WIDTH)
    card.setFixedHeight(CARD_HEIGHT)

    card.setStyleSheet("""
        QFrame#selectionCard {
            background-color: #1F222A;
            border-radius: 18px;
            border: 1px solid #2E323C;
        }
    """)

    shadow = QtWidgets.QGraphicsDropShadowEffect(card)
    shadow.setBlurRadius(40)
    shadow.setOffset(0, 12)
    shadow.setColor(QtGui.QColor(0, 0, 0, 160))
    card.setGraphicsEffect(shadow)

    card_layout = QtWidgets.QVBoxLayout(card)
    card_layout.setContentsMargins(32, 28, 32, 28)
    card_layout.setSpacing(22)
    card_layout.setAlignment(QtCore.Qt.AlignTop)

    # Header
    header_layout = QtWidgets.QHBoxLayout()
    header_layout.setSpacing(10)

    icon_label = QtWidgets.QLabel(" ")
    icon_label.setStyleSheet("font: 20pt 'Segoe UI';")
    header_layout.addWidget(icon_label)

    title_label = QtWidgets.QLabel("Pipeline Selection")
    title_label.setStyleSheet("""
        QLabel { font: 600 17pt 'Segoe UI'; color: #FFFFFF; }
    """)
    header_layout.addWidget(title_label)
    header_layout.addStretch(1)
    card_layout.addLayout(header_layout)

    subtitle = QtWidgets.QLabel("Choose the pipeline inch and project to continue.")
    subtitle.setStyleSheet("font: 9.5pt 'Segoe UI'; color: #A0A4B0;")
    card_layout.addWidget(subtitle)

    # ─────────────────────────────────────────────
    # INCH DROPDOWN (with placeholder)
    # ─────────────────────────────────────────────
    inch_block = QtWidgets.QVBoxLayout()
    inch_label = QtWidgets.QLabel("Project Inch")
    inch_label.setStyleSheet("font: 10.5pt 'Segoe UI'; color: #D5D8E3;")
    inch_block.addWidget(inch_label)

    self.combo_inch = QtWidgets.QComboBox()

    self.combo_inch.addItem("Select Project Inch")
    self.combo_inch.model().item(0).setEnabled(False)
    self.combo_inch.model().item(0).setForeground(QtGui.QColor("#888"))

    for inch in pipe_inch:
        self.combo_inch.addItem(inch)

    self.combo_inch.setStyleSheet("""
        QComboBox {
            background-color: #272B35;
            color: #E5E7F0;
            padding: 8px 10px;
            font: 10.5pt 'Segoe UI';
            border-radius: 10px;
            border: 1px solid #3A3F4D;
        }
        QComboBox::drop-down { border: none; width: 30px; }
        QComboBox::down-arrow {
            image: url(:/qt-project.org/styles/commonstyle/images/arrowdown.png);
            width: 14px; height: 14px;
        }
        QComboBox:hover { border: 1px solid #4C8DFF; }
    """)

    self.combo_inch.currentIndexChanged.connect(lambda index: on_inch_changed(self, index))

    self.new_project_btn = QtWidgets.QPushButton(" Create Project")
    self.new_project_btn.setEnabled(False)
    self.new_project_btn.setFixedHeight(38)
    self.new_project_btn.setStyleSheet("""
                QPushButton {
                    background-color: #272B35;
                    color: #D5D8E3;
                    font: 10.5pt 'Segoe UI';
                    padding: 6px 18px;
                    border-radius: 10px;
                    border: 1px solid #3A3F4D;
                }
                QPushButton:hover { background-color: #303543; }
            """)
    self.new_project_btn.clicked.connect(lambda: create_project(self))

    inch_block.addWidget(self.combo_inch)
    # Button layout (so it doesn’t stretch full width)
    new_btn_layout = QtWidgets.QHBoxLayout()
    new_btn_layout.addStretch(1)  # push button to right like Reset
    new_btn_layout.addWidget(self.new_project_btn)

    inch_block.addLayout(new_btn_layout)
    card_layout.addLayout(inch_block)

    # ─────────────────────────────────────────────
    # PROJECT DROPDOWN (with placeholder)
    # ─────────────────────────────────────────────
    project_block = QtWidgets.QVBoxLayout()
    project_label = QtWidgets.QLabel("Project")
    project_label.setStyleSheet("font: 10.5pt 'Segoe UI'; color: #D5D8E3;")
    project_block.addWidget(project_label)

    self.combo_project = QtWidgets.QComboBox()
    self.combo_project.setEnabled(False)

    self.combo_project.addItem("Select Project")
    self.combo_project.model().item(0).setEnabled(False)
    self.combo_project.model().item(0).setForeground(QtGui.QColor("#888"))

    self.combo_project.setStyleSheet("""
        QComboBox {
            background-color: #272B35;
            color: #E5E7F0;
            padding: 8px 10px;
            font: 10.5pt 'Segoe UI';
            border-radius: 10px;
            border: 1px solid #3A3F4D;
        }
        QComboBox::drop-down { border: none; width: 30px; }
        QComboBox::down-arrow {
            image: url(:/qt-project.org/styles/commonstyle/images/arrowdown.png);
            width: 14px; height: 14px;
        }
        QComboBox:disabled {
            background-color: #20232C;
            color: #777B88;
            border: 1px solid #323642;
        }
    """)

    self.combo_project.currentIndexChanged.connect(lambda index: on_project_changed(self, index))
    project_block.addWidget(self.combo_project)
    card_layout.addLayout(project_block)

    # ─────────────────────────────────────────────
    # BUTTONS
    # ─────────────────────────────────────────────
    btn_layout = QtWidgets.QHBoxLayout()
    btn_layout.addStretch(1)

    self.btn_apply = QtWidgets.QPushButton("Apply & Load")
    self.btn_apply.setEnabled(False)
    self.btn_apply.setFixedHeight(38)
    self.btn_apply.setStyleSheet("""
        QPushButton {
            background-color: #4C8DFF;
            color: white;
            font: 10.5pt 'Segoe UI';
            padding: 6px 18px;
            border-radius: 10px;
        }
        QPushButton:hover:!disabled { background-color: #3C78E0; }
        QPushButton:disabled {
            background-color: #324D7D;
            color: #AEB8E5;
        }
    """)

    self.btn_apply.clicked.connect(lambda: on_apply_clicked(self))

    self.btn_reset = QtWidgets.QPushButton("Reset")
    self.btn_reset.setFixedHeight(38)
    self.btn_reset.setStyleSheet("""
        QPushButton {
            background-color: #272B35;
            color: #D5D8E3;
            font: 10.5pt 'Segoe UI';
            padding: 6px 18px;
            border-radius: 10px;
            border: 1px solid #3A3F4D;
        }
        QPushButton:hover { background-color: #303543; }
    """)

    self.btn_reset.clicked.connect(lambda: reset_selection(self))



    btn_layout.addWidget(self.btn_apply)
    btn_layout.addSpacing(10)
    btn_layout.addWidget(self.btn_reset)

    card_layout.addLayout(btn_layout)


    layout.addWidget(card, alignment=QtCore.Qt.AlignCenter)

def on_apply_clicked(self):
    selected_project = self.combo_project.currentText()

    if selected_project == "Select Project":
        QtWidgets.QMessageBox.warning(
            self, "Missing Selection", "Please select a project."
        )
        return

    # Ensure inch was selected first
    if not hasattr(self, "selected_inch"):
        QtWidgets.QMessageBox.warning(
            self, "Missing Inch", "Please select pipe inch first."
        )
        return

    self.project_name = selected_project

    # 🔥 Ensure DB exists
    # self.config.init_db_connection(self.config.db_mysql)
    create_db_connection(self)
    # 1️⃣ Fetch runid
    try:
        with self.config.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT runid
                FROM projectdetail
                WHERE ProjectName = %s
                ORDER BY runid DESC
                LIMIT 1
                """,
                (selected_project,)
            )
            result = cursor.fetchone()
    except Exception as e:
        print("RunID fetch error:", e)
        return

    if not result:
        print("No runid found")
        return

    runid = result[0]
    print("Found runid:", runid)

    # 2️⃣ Extract inch number safely
    import re
    inch_match = re.findall(r'\d+', self.selected_inch)
    if not inch_match:
        print("Invalid inch format")
        return

    inch = inch_match[0]

    # 3️⃣ Build table id
    self.config.source_table_id = f"Egp_{inch}_copy_x{runid}"
    self.config.table_name = (
        f"{self.config.project_id}."
        f"{self.config.source_dataset_id}."
        f"{self.config.source_table_id}"
    )

    print("Using table dynamically: ", self.config.table_name)

    # 4️⃣ Start heavy runtime
    # self.config.init_runtime()
    init_gcp_backend(self)
    # 5️⃣ Load project
    load_selected_project(self, selected_project)



def on_inch_changed(self, index):
    if index <= 0:
        return   # ignore placeholder
    setup_inch_environment(self)



def setup_inch_environment(self):
    from egp_soft_based_on_mfl.Components.Configs.config_loader import (
        get_inch_config
    )

    self.selected_inch = self.combo_inch.currentText()
    print("Selected inch:", self.selected_inch)

    # Load config
    self.config = get_inch_config(self.selected_inch)
    # set_config(self.config)

    # Ensure DB is ready
    # self.config.init_db_connection(self.config.db_mysql)
    create_db_connection(self)
    # Load projects
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


def on_project_changed(self, index):
    if index <= 0:
        self.btn_apply.setEnabled(False)
    else:
        self.btn_apply.setEnabled(True)



def reset_selection(self):
    print("Resetting selections...")

    # Reset inch dropdown
    self.combo_inch.blockSignals(True)
    self.combo_inch.setCurrentIndex(0)
    self.combo_inch.blockSignals(False)

    # Reset project dropdown
    self.combo_project.blockSignals(True)
    self.combo_project.clear()
    self.combo_project.addItem("Select Project")
    self.combo_project.model().item(0).setEnabled(False)
    self.combo_project.model().item(0).setForeground(QtGui.QColor("#888"))
    self.combo_project.setEnabled(False)
    self.new_project_btn.setEnabled(False)
    self.combo_project.blockSignals(False)

    self.btn_apply.setEnabled(False)

    # Hide menubar if used
    if hasattr(self, "menubar"):
        self.menubar.setVisible(False)


def load_selected_project(self, project_name):
    print(f"📂 Loading project: {project_name}")
    self.project_name = project_name

    # Build all tabs inside Screen2
    self.init_tab()

    # Load previous form data for update tab
    self.runid = self.tab_update.set_previous_form_data(project_name)
    print(f"selected run id : {self.runid}")

    # Set tab names (optional)
    self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_update), "🔄 Update")
    self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_weld_selection), "⚙️ Weld Selection")
    self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_showData), "📊 Data Table")
    self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_line1.tab_line1),
                                    "📈 Linechart - Counter vs Sensor")
    self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_line_orientation),
                                    "Linechart - Absolute vs Orientation")
    self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_visualize),
                                    "🌐 Pipe Visualization")
    self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.continue_heatmap_tab),
                                    "Heatmap - Abs vs Orientation")
    self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.Graph1), "📉 Graph")

    # 👉 SWITCH TO MAIN APPLICATION SCREEN
    self.stack.setCurrentIndex(1)

    # 👉 SHOW MENUBAR
    self.menubar.setVisible(True)