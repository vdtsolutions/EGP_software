#
import egp_soft_based_on_mfl.Components.style1 as Style
from PyQt5 import QtCore, QtWidgets
from egp_soft_based_on_mfl.Components.Configs.pipe_inch import pipe_inch

#
# # ----------------------------------------------------------------------
# # builds the main landing screen of inch and project selection
# # ----------------------------------------------------------------------
# # def build_screen1(self):
# #     self.screen1 = QtWidgets.QWidget()
# #     layout = QtWidgets.QVBoxLayout(self.screen1)
# #     layout.setAlignment(QtCore.Qt.AlignCenter)
# #
# #     card = QtWidgets.QFrame()
# #     card.setStyleSheet("""
# #            background-color: #FFFFFF;
# #            border-radius: 15px;
# #            padding: 30px;
# #            border: 2px solid #D0D9E8;
# #        """)
# #     card.setMinimumWidth(350)
# #
# #     card_layout = QtWidgets.QVBoxLayout(card)
# #     card_layout.setSpacing(25)
# #     card_layout.setAlignment(QtCore.Qt.AlignCenter)
# #
# #     # Select Inch
# #     self.select_inch_btn = QtWidgets.QPushButton("Select Project Inch")
# #     self.select_inch_btn.setStyleSheet(Style.btn_type_primary)
# #     self.select_inch_btn.clicked.connect(lambda: open_inch_dialog(self))
# #     card_layout.addWidget(self.select_inch_btn)
# #
# #     # Load Data
# #     self.load_list_pushButton = QtWidgets.QPushButton("Load Data")
# #     self.load_list_pushButton.setStyleSheet(Style.btn_type_primary)
# #     self.load_list_pushButton.setEnabled(False)
# #     self.load_list_pushButton.clicked.connect(lambda: load_list(self))
# #     card_layout.addWidget(self.load_list_pushButton)
# #
# #     layout.addWidget(card)
#
# # def build_screen1(self):
# #     self.screen1 = QtWidgets.QWidget()
# #     layout = QtWidgets.QVBoxLayout(self.screen1)
# #     layout.setAlignment(QtCore.Qt.AlignCenter)
# #
# #     # ===== GLASS CARD =====
# #     card = QtWidgets.QFrame()
# #     card.setStyleSheet("""
# #         QFrame {
# #             background: rgba(255, 255, 255, 0.55);
# #             border-radius: 20px;
# #             padding: 30px;
# #             border: 1px solid rgba(255, 255, 255, 0.3);
# #             backdrop-filter: blur(25px);
# #         }
# #     """)
# #     card.setMinimumWidth(420)
# #
# #     card_layout = QtWidgets.QVBoxLayout(card)
# #     card_layout.setSpacing(22)
# #     card_layout.setAlignment(QtCore.Qt.AlignCenter)
# #
# #     # ===== Title =====
# #     title = QtWidgets.QLabel("📁 Pipeline Selection")
# #     title.setStyleSheet("""
# #         font: 600 18pt 'Segoe UI';
# #         color: #1a1a1a;
# #         margin-bottom: 10px;
# #     """)
# #     card_layout.addWidget(title)
# #
# #     # ===== Section: Inch =====
# #     inch_label = QtWidgets.QLabel("Select Project Inch")
# #     inch_label.setStyleSheet("font: 11pt 'Segoe UI'; color: #333;")
# #
# #     self.combo_inch = QtWidgets.QComboBox()
# #     self.combo_inch.addItems(pipe_inch)
# #     self.combo_inch.setStyleSheet("""
# #         QComboBox {
# #             padding: 10px;
# #             font: 11pt 'Segoe UI';
# #             border-radius: 12px;
# #             border: 1px solid #d0d0d0;
# #             background: white;
# #         }
# #         QComboBox:hover {
# #             border-color: #6aa9ff;
# #         }
# #     """)
# #     self.combo_inch.currentIndexChanged.connect(lambda: self.apply_inch_selection_direct())
# #
# #     card_layout.addWidget(inch_label)
# #     card_layout.addWidget(self.combo_inch)
# #
# #     # ===== Section: Project =====
# #     project_label = QtWidgets.QLabel("Select Project")
# #     project_label.setStyleSheet("font: 11pt 'Segoe UI'; color: #333;")
# #
# #     self.combo_project = QtWidgets.QComboBox()
# #     self.combo_project.setEnabled(False)
# #     self.combo_project.setStyleSheet("""
# #         QComboBox {
# #             padding: 10px;
# #             font: 11pt 'Segoe UI';
# #             border-radius: 12px;
# #             border: 1px solid #d0d0d0;
# #             background: white;
# #         }
# #         QComboBox:disabled {
# #             background: #f0f0f0;
# #             color: #aaa;
# #         }
# #     """)
# #
# #     card_layout.addWidget(project_label)
# #     card_layout.addWidget(self.combo_project)
# #
# #     # ===== BUTTON BAR =====
# #     btn_layout = QtWidgets.QHBoxLayout()
# #
# #     # Apply Button
# #     self.btn_apply = QtWidgets.QPushButton("Apply & Load")
# #     self.btn_apply.setEnabled(False)
# #     self.btn_apply.setFixedHeight(40)
# #     self.btn_apply.setStyleSheet("""
# #         QPushButton {
# #             background-color: #4a90e2;
# #             color: white;
# #             font: 11pt 'Segoe UI';
# #             padding: 10px 18px;
# #             border-radius: 12px;
# #         }
# #         QPushButton:hover {
# #             background-color: #3d7ac4;
# #         }
# #         QPushButton:disabled {
# #             background-color: #aac7ee;
# #         }
# #     """)
# #     self.btn_apply.clicked.connect(lambda: on_apply_clicked(self))
# #
# #     # Reset Button
# #     self.btn_reset = QtWidgets.QPushButton("Reset")
# #     self.btn_reset.setFixedHeight(40)
# #     self.btn_reset.setStyleSheet("""
# #         QPushButton {
# #             background-color: #ffffff;
# #             color: #444;
# #             font: 11pt 'Segoe UI';
# #             padding: 10px 18px;
# #             border-radius: 12px;
# #             border: 1px solid #ccc;
# #         }
# #         QPushButton:hover {
# #             background-color: #f2f2f2;
# #         }
# #     """)
# #     self.btn_reset.clicked.connect(lambda: reset_selection(self))
# #
# #     btn_layout.addWidget(self.btn_apply)
# #     btn_layout.addWidget(self.btn_reset)
# #     card_layout.addLayout(btn_layout)
# #
# #     layout.addWidget(card)
from PyQt5 import QtCore, QtWidgets, QtGui
# from egp_soft_based_on_mfl.Components.Configs.pipe_inch import pipe_inch
#
#
# # def build_screen1(self):
# #     self.screen1 = QtWidgets.QWidget()
# #     layout = QtWidgets.QVBoxLayout(self.screen1)
# #     layout.setAlignment(QtCore.Qt.AlignCenter)
# #
# #     # ─────────────────────────────────────────
# #     # Dark Material Card
# #     # ─────────────────────────────────────────
# #     card = QtWidgets.QFrame()
# #     card.setObjectName("selectionCard")
# #     card.setMinimumWidth(460)
# #     card.setStyleSheet("""
# #         QFrame#selectionCard {
# #             background-color: #1F222A;        /* dark charcoal */
# #             border-radius: 18px;
# #             border: 1px solid #2E323C;
# #         }
# #     """)
# #
# #     # Soft shadow (looks great on bright bg)
# #     shadow = QtWidgets.QGraphicsDropShadowEffect(card)
# #     shadow.setBlurRadius(40)
# #     shadow.setOffset(0, 12)
# #     shadow.setColor(QtGui.QColor(0, 0, 0, 160))
# #     card.setGraphicsEffect(shadow)
# #
# #     card_layout = QtWidgets.QVBoxLayout(card)
# #     card_layout.setContentsMargins(32, 28, 32, 28)
# #     card_layout.setSpacing(22)
# #     card_layout.setAlignment(QtCore.Qt.AlignTop)
# #
# #     # ─────────────────────────────────────────
# #     # Header
# #     # ─────────────────────────────────────────
# #     header_layout = QtWidgets.QHBoxLayout()
# #     header_layout.setSpacing(10)
# #
# #     icon_label = QtWidgets.QLabel("🧭")
# #     icon_label.setStyleSheet("font: 20pt 'Segoe UI';")
# #     header_layout.addWidget(icon_label, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
# #
# #     title_label = QtWidgets.QLabel("Pipeline Selection")
# #     title_label.setStyleSheet("""
# #         QLabel {
# #             font: 600 17pt 'Segoe UI';
# #             color: #FFFFFF;
# #         }
# #     """)
# #     header_layout.addWidget(title_label, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
# #     header_layout.addStretch(1)
# #
# #     card_layout.addLayout(header_layout)
# #
# #     # Sub-title
# #     subtitle = QtWidgets.QLabel("Choose the pipeline inch and project to continue.")
# #     subtitle.setStyleSheet("""
# #         QLabel {
# #             font: 9.5pt 'Segoe UI';
# #             color: #A0A4B0;
# #         }
# #     """)
# #     card_layout.addWidget(subtitle)
# #
# #     # ─────────────────────────────────────────
# #     # Inch Selector
# #     # ─────────────────────────────────────────
# #     inch_block = QtWidgets.QVBoxLayout()
# #     inch_label = QtWidgets.QLabel("Project Inch")
# #     inch_label.setStyleSheet("font: 10.5pt 'Segoe UI'; color: #D5D8E3;")
# #     inch_block.addWidget(inch_label)
# #
# #     self.combo_inch = QtWidgets.QComboBox()
# #     self.combo_inch.addItems(pipe_inch)
# #     self.combo_inch.setStyleSheet("""
# #         QComboBox {
# #             background-color: #272B35;
# #             color: #E5E7F0;
# #             padding: 8px 10px;
# #             font: 10.5pt 'Segoe UI';
# #             border-radius: 10px;
# #             border: 1px solid #3A3F4D;
# #         }
# #         QComboBox::drop-down {
# #             border: none;
# #             width: 24px;
# #         }
# #         QComboBox:hover {
# #             border: 1px solid #4C8DFF;
# #         }
# #     """)
# #     self.combo_inch.currentIndexChanged.connect(lambda index: on_inch_changed(self, index))
# #     inch_block.addWidget(self.combo_inch)
# #     card_layout.addLayout(inch_block)
# #
# #     # ─────────────────────────────────────────
# #     # Project Selector
# #     # ─────────────────────────────────────────
# #     project_block = QtWidgets.QVBoxLayout()
# #     project_label = QtWidgets.QLabel("Project")
# #     project_label.setStyleSheet("font: 10.5pt 'Segoe UI'; color: #D5D8E3;")
# #     project_block.addWidget(project_label)
# #
# #     self.combo_project = QtWidgets.QComboBox()
# #     self.combo_project.setEnabled(False)
# #     self.combo_project.setStyleSheet("""
# #         QComboBox {
# #             background-color: #272B35;
# #             color: #E5E7F0;
# #             padding: 8px 10px;
# #             font: 10.5pt 'Segoe UI';
# #             border-radius: 10px;
# #             border: 1px solid #3A3F4D;
# #         }
# #         QComboBox::drop-down {
# #             border: none;
# #             width: 24px;
# #         }
# #         QComboBox:disabled {
# #             background-color: #20232C;
# #             color: #777B88;
# #             border: 1px solid #323642;
# #         }
# #         QComboBox:hover:!disabled {
# #             border: 1px solid #4C8DFF;
# #         }
# #     """)
# #     self.combo_project.currentIndexChanged.connect(lambda index: on_project_changed(self, index))
# #     project_block.addWidget(self.combo_project)
# #     card_layout.addLayout(project_block)
# #
# #     # ─────────────────────────────────────────
# #     # Buttons Row
# #     # ─────────────────────────────────────────
# #     btn_layout = QtWidgets.QHBoxLayout()
# #     btn_layout.addStretch(1)
# #
# #     self.btn_apply = QtWidgets.QPushButton("Apply & Load")
# #     self.btn_apply.setEnabled(False)
# #     self.btn_apply.setFixedHeight(38)
# #     self.btn_apply.setStyleSheet("""
# #         QPushButton {
# #             background-color: #4C8DFF;
# #             color: white;
# #             font: 10.5pt 'Segoe UI';
# #             padding: 6px 18px;
# #             border-radius: 10px;
# #             border: none;
# #         }
# #         QPushButton:hover:!disabled {
# #             background-color: #3C78E0;
# #         }
# #         QPushButton:disabled {
# #             background-color: #324D7D;
# #             color: #AEB8E5;
# #         }
# #     """)
# #     self.btn_apply.clicked.connect(lambda: on_apply_clicked(self))
# #
# #     self.btn_reset = QtWidgets.QPushButton("Reset")
# #     self.btn_reset.setFixedHeight(38)
# #     self.btn_reset.setStyleSheet("""
# #         QPushButton {
# #             background-color: #272B35;
# #             color: #D5D8E3;
# #             font: 10.5pt 'Segoe UI';
# #             padding: 6px 18px;
# #             border-radius: 10px;
# #             border: 1px solid #3A3F4D;
# #         }
# #         QPushButton:hover {
# #             background-color: #303543;
# #         }
# #     """)
# #     self.btn_reset.clicked.connect(lambda: reset_selection(self))
# #
# #     btn_layout.addWidget(self.btn_apply)
# #     btn_layout.addSpacing(10)
# #     btn_layout.addWidget(self.btn_reset)
# #
# #     card_layout.addSpacing(10)
# #     card_layout.addLayout(btn_layout)
# #
# #     layout.addWidget(card)
#
#
# def build_screen1(self):
#     self.screen1 = QtWidgets.QWidget()
#     layout = QtWidgets.QVBoxLayout(self.screen1)
#     layout.setAlignment(QtCore.Qt.AlignCenter)
#
#     # ─────────────────────────────────────────
#     # Adjustable Card Size (Tweak Freely)
#     # ─────────────────────────────────────────
#     CARD_WIDTH = 500      # You can change this anytime (e.g. 420, 480, 520)
#     CARD_HEIGHT = 420     # Change height if needed
#
#     # ─────────────────────────────────────────
#     # Dark Material Card
#     # ─────────────────────────────────────────
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
#     # Drop shadow for premium look
#     shadow = QtWidgets.QGraphicsDropShadowEffect(card)
#     shadow.setBlurRadius(40)
#     shadow.setOffset(0, 12)
#     shadow.setColor(QtGui.QColor(0, 0, 0, 160))
#     card.setGraphicsEffect(shadow)
#
#     # ─────────────────────────────────────────
#     # Card Layout
#     # ─────────────────────────────────────────
#     card_layout = QtWidgets.QVBoxLayout(card)
#     card_layout.setContentsMargins(32, 28, 32, 28)
#     card_layout.setSpacing(22)
#     card_layout.setAlignment(QtCore.Qt.AlignTop)
#
#     # ─────────────────────────────────────────
#     # Header Section
#     # ─────────────────────────────────────────
#     header_layout = QtWidgets.QHBoxLayout()
#     header_layout.setSpacing(10)
#
#     icon_label = QtWidgets.QLabel("🧭")
#     icon_label.setStyleSheet("font: 20pt 'Segoe UI';")
#     header_layout.addWidget(icon_label)
#
#     title_label = QtWidgets.QLabel("Pipeline Selection")
#     title_label.setStyleSheet("""
#         QLabel {
#             font: 600 17pt 'Segoe UI';
#             color: #FFFFFF;
#         }
#     """)
#     header_layout.addWidget(title_label)
#     header_layout.addStretch(1)
#
#     card_layout.addLayout(header_layout)
#
#     # Subtitle
#     subtitle = QtWidgets.QLabel("Choose the pipeline inch and project to continue.")
#     subtitle.setStyleSheet("""
#         QLabel {
#             font: 9.5pt 'Segoe UI';
#             color: #A0A4B0;
#         }
#     """)
#     card_layout.addWidget(subtitle)
#
#     # ─────────────────────────────────────────
#     # Inch Selector Block
#     # ─────────────────────────────────────────
#     inch_block = QtWidgets.QVBoxLayout()
#     inch_label = QtWidgets.QLabel("Project Inch")
#     inch_label.setStyleSheet("font: 10.5pt 'Segoe UI'; color: #D5D8E3;")
#     inch_block.addWidget(inch_label)
#
#     self.combo_inch = QtWidgets.QComboBox()
#     self.combo_inch.addItems(pipe_inch)
#     self.combo_inch.setStyleSheet("""
#         QComboBox {
#             background-color: #272B35;
#             color: #E5E7F0;
#             padding: 8px 10px;
#             font: 10.5pt 'Segoe UI';
#             border-radius: 10px;
#             border: 1px solid #3A3F4D;
#         }
#         QComboBox::drop-down {
#             border: none;
#             width: 30px;
#         }
#         QComboBox::down-arrow {
#             image: url(:/qt-project.org/styles/commonstyle/images/arrowdown.png);
#             width: 14px;
#             height: 14px;
#         }
#         QComboBox:hover {
#             border: 1px solid #4C8DFF;
#         }
#     """)
#
#     self.combo_inch.currentIndexChanged.connect(lambda index: on_inch_changed(self, index))
#     inch_block.addWidget(self.combo_inch)
#     card_layout.addLayout(inch_block)
#
#     # ─────────────────────────────────────────
#     # Project Selector Block
#     # ─────────────────────────────────────────
#     project_block = QtWidgets.QVBoxLayout()
#     project_label = QtWidgets.QLabel("Project")
#     project_label.setStyleSheet("font: 10.5pt 'Segoe UI'; color: #D5D8E3;")
#     project_block.addWidget(project_label)
#
#     self.combo_project = QtWidgets.QComboBox()
#     self.combo_project.setEnabled(False)
#     self.combo_project.setStyleSheet("""
#         QComboBox {
#             background-color: #272B35;
#             color: #E5E7F0;
#             padding: 8px 10px;
#             font: 10.5pt 'Segoe UI';
#             border-radius: 10px;
#             border: 1px solid #3A3F4D;
#         }
#         QComboBox:disabled {
#             background-color: #20232C;
#             color: #777B88;
#             border: 1px solid #323642;
#         }
#         QComboBox:hover:!disabled {
#             border: 1px solid #4C8DFF;
#         }
#     """)
#     self.combo_project.currentIndexChanged.connect(lambda index: on_project_changed(self, index))
#     project_block.addWidget(self.combo_project)
#     card_layout.addLayout(project_block)
#
#     # ─────────────────────────────────────────
#     # Buttons Row
#     # ─────────────────────────────────────────
#     btn_layout = QtWidgets.QHBoxLayout()
#     btn_layout.addStretch(1)
#
#     # Apply Button
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
#             border: none;
#         }
#         QPushButton:hover:!disabled {
#             background-color: #3C78E0;
#         }
#         QPushButton:disabled {
#             background-color: #324D7D;
#             color: #AEB8E5;
#         }
#     """)
#     self.btn_apply.clicked.connect(lambda: on_apply_clicked(self))
#
#     # Reset Button
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
#         QPushButton:hover {
#             background-color: #303543;
#         }
#     """)
#     self.btn_reset.clicked.connect(lambda: reset_selection(self))
#
#     btn_layout.addWidget(self.btn_apply)
#     btn_layout.addSpacing(10)
#     btn_layout.addWidget(self.btn_reset)
#
#     card_layout.addSpacing(10)
#     card_layout.addLayout(btn_layout)
#
#     # IMPORTANT: Center card and prevent stretch
#     layout.addWidget(card, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
#
#
#
# """
# helper fucntions for screen_1 starts here
# """
#
# def project_selected_direct(self):
#     project = self.combo_project.currentText()
#     if not project:
#         return
#
#     print("Selected project:", project)
#     load_selected_project(self, project)
#
#
# # ----------------------------------------------------------------------
# # Selecting the inch of project
# # ----------------------------------------------------------------------
# def open_inch_dialog(self):
#     print(f"inside setup_ui")
#     dialog = QtWidgets.QDialog(self)
#     dialog.setWindowTitle("Select Project Inch")
#     dialog.setWindowFlags(
#         QtCore.Qt.WindowCloseButtonHint |
#         QtCore.Qt.Dialog |
#         QtCore.Qt.MSWindowsFixedSizeDialogHint
#     )
#     dialog.setModal(True)
#     dialog.setFixedSize(320, 180)
#     dialog.setStyleSheet("""
#         QDialog {
#             background-color: #F0F8FF;
#         }
#         QLabel {
#             font: 11pt 'Segoe UI';
#             margin-bottom: 8px;
#         }
#         QComboBox {
#             font: 10pt 'Segoe UI';
#             padding: 5px;
#         }
#     """)
#
#     layout = QtWidgets.QVBoxLayout(dialog)
#     label = QtWidgets.QLabel("Choose project inch:")
#     layout.addWidget(label)
#
#     # Dropdown
#     self.combo_inch = QtWidgets.QComboBox(dialog)
#     self.combo_inch.addItems(pipe_inch)
#     layout.addWidget(self.combo_inch)
#
#     # Buttons
#     btn_box = QtWidgets.QDialogButtonBox()
#     btn_apply = QtWidgets.QPushButton("Apply")
#     btn_cancel = QtWidgets.QPushButton("Cancel")
#     btn_box.addButton(btn_apply, QtWidgets.QDialogButtonBox.AcceptRole)
#     btn_box.addButton(btn_cancel, QtWidgets.QDialogButtonBox.RejectRole)
#     layout.addWidget(btn_box)
#
#     # Connect signals manually (important)
#     btn_apply.clicked.connect(lambda _, d=dialog: apply_inch_selection(self, d))
#     btn_cancel.clicked.connect(dialog.reject)
#
#     dialog.exec_()
#
# def apply_inch_selection(self, dialog):
#     """Handle Apply click — save inch, load config, enable load, and close dialog."""
#     from egp_soft_based_on_mfl.Components.Configs.config_loader import get_inch_config, set_config
#
#     # 1️⃣ Save selected inch
#     self.selected_inch = self.combo_inch.currentText()
#     self.select_inch_btn.setText(f"Project Inch: {self.selected_inch}")
#
#     # 2️⃣ Load the config for that inch
#     self.config = get_inch_config(self.selected_inch)
#     if self.config:
#         set_config(self.config)
#         print(f"✅ Config loaded for {self.selected_inch}: {self.config}")
#         self.config.init_runtime()
#     else:
#         QtWidgets.QMessageBox.critical(self, "Config Error",
#                                        f"Configuration for {self.selected_inch} not found.")
#         dialog.reject()
#         return
#
#     # 3️⃣ Enable 'Load Data' safely
#     if hasattr(self, "load_list_pushButton") and self.load_list_pushButton is not None:
#         QtCore.QTimer.singleShot(100, lambda: self.load_list_pushButton.setEnabled(True))
#         print("✅ Load Data button enabled.")
#     else:
#         print("⚠️ Load button not found!")
#
#     # 4️⃣ Close the dialog
#     print(f"✅ Selected Project Inch: {self.selected_inch}")
#     show_menubar_if_ready(self)
#     dialog.accept()
#
# def apply_inch_selection_direct(self):
#     from egp_soft_based_on_mfl.Components.Configs.config_loader import get_inch_config, set_config
#
#     self.selected_inch = self.combo_inch.currentText()
#     print("Selected inch:", self.selected_inch)
#
#     # Load config for inch
#     self.config = get_inch_config(self.selected_inch)
#     set_config(self.config)
#     self.config.init_runtime()
#
#     # Enable project dropdown
#     self.combo_project.setEnabled(True)
#
#     # Load project list WITHOUT triggering selection
#     try:
#         with self.config.connection.cursor() as cursor:
#             cursor.execute("SELECT `ProjectName` FROM projectdetail ORDER BY runid DESC")
#             projects = [row[0] for row in cursor.fetchall()]
#     except:
#         projects = ["Demo Project A", "Demo Project B", "Demo Project C"]
#
#     self.combo_project.blockSignals(True)
#     self.combo_project.clear()
#     self.combo_project.addItems(projects)
#     self.combo_project.setCurrentIndex(-1)  # nothing selected
#     self.combo_project.blockSignals(False)
#
#     # Enable Apply button only after project is manually selected
#     self.combo_project.currentIndexChanged.connect(lambda: self.btn_apply.setEnabled(True))
#
# def reset_selection(self):
#     self.selected_inch = None
#     self.project_name = None
#
#     # Reset dropdowns
#     self.combo_inch.setCurrentIndex(0)
#     self.combo_project.blockSignals(True)
#     self.combo_project.clear()
#     self.combo_project.setEnabled(False)
#     self.combo_project.blockSignals(False)
#
#     # Disable apply
#     self.btn_apply.setEnabled(False)
#
#     # Hide menubar
#     self.menubar.setVisible(False)
#
#     print("Selections reset!")
#
# def on_apply_clicked(self):
#     selected_project = self.combo_project.currentText()
#
#     if not selected_project:
#         QtWidgets.QMessageBox.warning(self, "Missing Selection", "Please select a project.")
#         return
#
#     print("Loading project:", selected_project)
#     load_selected_project(self, selected_project)
#
#
# def show_menubar_if_ready(self):
#     if self.selected_inch and self.project_name:
#         self.menubar.setVisible(True)
#
#
# # ----------------------------------------------------------------------
# # selecting the project from list dialog
# # ----------------------------------------------------------------------
#
# def load_list(self):
#     """Open dialog to select project, then load it."""
#     print("🔹 Load Data clicked!")
#
#     # Ensure inch selected first
#     if not self.selected_inch:
#         QtWidgets.QMessageBox.warning(self, "Select Project Inch", "Please select a project inch first.")
#         return
#
#     try:
#         with self.config.connection.cursor() as cursor:
#             cursor.execute("SELECT `ProjectName` FROM projectdetail ORDER BY runid DESC")
#             all_projects = [row[0] for row in cursor.fetchall()]
#             print("✅ Projects fetched:", all_projects)
#     except Exception as e:
#         print(f"⚠️ Database error: {e}")
#         all_projects = ["Demo Project A", "Demo Project B", "Demo Project C"]
#
#     if not all_projects:
#         QtWidgets.QMessageBox.information(self, "No Projects Found", "No projects available in the database.")
#         return
#
#     # ---- Create dialog box ----
#     dialog = QtWidgets.QDialog(self)
#     dialog.setWindowTitle("Select Project")
#     dialog.setModal(True)
#     dialog.setFixedSize(350, 200)
#     dialog.setStyleSheet("""
#         QDialog { background-color: #F0F8FF; }
#         QLabel { font: 11pt 'Segoe UI'; margin-bottom: 8px; }
#         QComboBox { font: 10pt 'Segoe UI'; padding: 5px; }
#     """)
#
#     layout = QtWidgets.QVBoxLayout(dialog)
#     label = QtWidgets.QLabel("Choose a project:")
#     layout.addWidget(label)
#
#     combo_projects = QtWidgets.QComboBox(dialog)
#     combo_projects.addItems(all_projects)
#     layout.addWidget(combo_projects)
#
#     btn_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
#     layout.addWidget(btn_box)
#
#     # --- Logic when user clicks OK ---
#     def apply_selection():
#         selected_project = combo_projects.currentText()
#         print(f"✅ Selected Project: {selected_project}")
#         dialog.accept()
#         load_selected_project(self, selected_project)  # 🔹 identical logic to old list_clicked()
#
#     btn_box.accepted.connect(apply_selection)
#     btn_box.rejected.connect(dialog.reject)
#     dialog.exec_()
#
# # ----------------------------------------------------------------------
# # After selecting project (Go to Main App Screen) -- screen_2
# # ----------------------------------------------------------------------
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
#
#     # Set tab names (optional)
#     self.right_tabWidget.setTabText(self.right_tabWidget.indexOf(self.tab_update), "🔄 Update")
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
#
#
# def on_inch_changed(self, index):
#     """Triggered when inch dropdown changes."""
#     if index < 0:
#         return
#     apply_inch_selection_direct(self)
#
#
# def apply_inch_selection_direct(self):
#     """Load config for selected inch and populate project list."""
#     from egp_soft_based_on_mfl.Components.Configs.config_loader import (
#         get_inch_config, set_config
#     )
#
#     self.selected_inch = self.combo_inch.currentText()
#     print("Selected inch:", self.selected_inch)
#
#     # Load inch config
#     self.config = get_inch_config(self.selected_inch)
#     if not self.config:
#         QtWidgets.QMessageBox.critical(
#             self, "Config Error",
#             f"Configuration for {self.selected_inch} not found."
#         )
#         return
#
#     set_config(self.config)
#     self.config.init_runtime()
#
#     # Enable project dropdown
#     self.combo_project.setEnabled(True)
#
#     # Fetch projects from DB
#     try:
#         with self.config.connection.cursor() as cursor:
#             cursor.execute("SELECT `ProjectName` FROM projectdetail ORDER BY runid DESC")
#             projects = [row[0] for row in cursor.fetchall()]
#             print("Projects fetched:", projects)
#     except Exception as e:
#         print("DB error while fetching projects:", e)
#         projects = ["Demo Project A", "Demo Project B", "Demo Project C"]
#
#     # Fill projects without firing change logic weirdly
#     self.combo_project.blockSignals(True)
#     self.combo_project.clear()
#     self.combo_project.addItems(projects)
#     self.combo_project.setCurrentIndex(-1)   # force user to choose
#     self.combo_project.blockSignals(False)
#
#     # Until project explicitly chosen, keep Apply disabled
#     self.btn_apply.setEnabled(False)
#
#
# def on_project_changed(self, index):
#     """Enable Apply only when a valid project is selected."""
#     if index >= 0:
#         self.btn_apply.setEnabled(True)
#     else:
#         self.btn_apply.setEnabled(False)
#
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
#
# def reset_selection(self):
#     """Reset both dropdowns and hide menubar/app state."""
#     print("Resetting inch & project selections")
#
#     self.selected_inch = None
#     self.project_name = None
#
#     # Reset dropdowns
#     self.combo_inch.setCurrentIndex(0)
#
#     self.combo_project.blockSignals(True)
#     self.combo_project.clear()
#     self.combo_project.setEnabled(False)
#     self.combo_project.blockSignals(False)
#
#     # Disable Apply
#     self.btn_apply.setEnabled(False)
#
#     # Hide menubar & go back to first screen if needed
#     if hasattr(self, "menubar"):
#         self.menubar.setVisible(False)
#     if hasattr(self, "stack"):
#         self.stack.setCurrentIndex(0)


def build_screen1(self):
    self.screen1 = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(self.screen1)
    layout.setAlignment(QtCore.Qt.AlignCenter)

    # Adjustable card size
    CARD_WIDTH = 500
    CARD_HEIGHT = 420

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
    inch_block.addWidget(self.combo_inch)
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
    """Load the selected project when Apply is pressed."""
    selected_project = self.combo_project.currentText()
    if not selected_project:
        QtWidgets.QMessageBox.warning(
            self, "Missing Selection", "Please select a project."
        )
        return

    print("Loading project:", selected_project)
    self.project_name = selected_project
    load_selected_project(self, selected_project)  # your existing function

def on_inch_changed(self, index):
    if index <= 0:
        return   # ignore placeholder
    apply_inch_selection_direct(self)


def apply_inch_selection_direct(self):
    from egp_soft_based_on_mfl.Components.Configs.config_loader import (
        get_inch_config, set_config
    )

    self.selected_inch = self.combo_inch.currentText()
    print("Selected inch:", self.selected_inch)

    self.config = get_inch_config(self.selected_inch)
    set_config(self.config)
    self.config.init_runtime()

    #Fetch project list
    try:
        with self.config.connection.cursor() as cursor:
            cursor.execute("SELECT `ProjectName` FROM projectdetail ORDER BY runid DESC")
            projects = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print("DB error:", e)
        projects = ["Demo A", "Demo B", "Demo C"]


    self.combo_project.setEnabled(True)

    # Reset project dropdown with placeholder
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