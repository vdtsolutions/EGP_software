# import sys
# import os
# import pandas as pd
# import plotly.io as pio
#
# # Ensure PNG saving using kaleido
# pio.kaleido.scope.default_format = "png"
#
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel,
#     QComboBox, QSizePolicy
# )
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtCore import Qt, QUrl
#
# from erf2 import plot_erf
# from psafe1 import plot_psafe
# from depth_percent import plot_depth
# from orientation import plot_orientation
# from pitting_graph import plot_pitting
# from general import plot_general
# from corr import plot_corrosion
#
#
# class GraphApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.df = None
#         self.setWindowTitle("Pipeline Defect Graph Viewer")
#         self.setGeometry(200, 100, 1100, 800)
#         self.layout = QVBoxLayout()
#
#         self.file_label = QLabel("No file selected")
#         self.layout.addWidget(self.file_label)
#
#         self.load_btn = QPushButton("Load Excel File")
#         self.load_btn.clicked.connect(self.load_file)
#         self.layout.addWidget(self.load_btn)
#
#         # Graph Type Dropdown
#         self.graph_type = QComboBox()
#         self.graph_type.addItems(["", "Defects", "ERF", "Psafe", "Depth", "Orientation"])
#         self.graph_type.setVisible(False)
#         self.graph_type.currentTextChanged.connect(self.on_graph_type_changed)
#         self.layout.addWidget(QLabel("Select Graph Type:"))
#         self.layout.addWidget(self.graph_type)
#
#         # Defect Category Dropdown
#         self.defect_category = QComboBox()
#         self.defect_category.addItems(["", "Corrosion", "General", "Pitting"])
#         self.defect_category.setVisible(False)
#         self.layout.addWidget(QLabel("Select Defect Category:"))
#         self.layout.addWidget(self.defect_category)
#
#         # Surface View Dropdown
#         self.view_type = QComboBox()
#         self.view_type.addItems(["", "Internal", "External", "Both"])
#         self.view_type.setVisible(False)
#         self.layout.addWidget(QLabel("Select Surface View:"))
#         self.layout.addWidget(self.view_type)
#
#         # Plot Button
#         self.plot_btn = QPushButton("Plot Graph")
#         self.plot_btn.clicked.connect(self.plot_graph)
#         self.plot_btn.setVisible(False)
#         self.layout.addWidget(self.plot_btn)
#
#         # Save Button
#         self.save_btn = QPushButton("Save Graph as PNG")
#         self.save_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: #444;
#                 color: white;
#                 padding: 6px 15px;
#                 font-weight: bold;
#                 border-radius: 5px;
#             }
#             QPushButton:hover {
#                 background-color: #666;
#             }
#         """)
#         self.save_btn.setFixedWidth(200)
#         self.save_btn.setVisible(False)
#         self.save_btn.clicked.connect(self.save_graph)
#         self.layout.addWidget(self.save_btn)
#
#         # Browser for displaying graphs
#         self.browser = QWebEngineView()
#         self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.layout.addWidget(self.browser)
#
#         self.setLayout(self.layout)
#
#     def on_graph_type_changed(self, text):
#         if text == "Defects":
#             # Enable defect category dropdown and disable Surface View dropdown
#             self.defect_category.setVisible(True)
#             self.view_type.setVisible(False)
#         elif text in ["ERF", "Psafe", "Depth", "Orientation"]:
#             # Enable Surface View dropdown and disable Defect Category dropdown
#             self.defect_category.setVisible(False)
#             self.view_type.setVisible(True)
#         else:
#             # If no valid graph type is selected, hide both dropdowns
#             self.defect_category.setVisible(False)
#             self.view_type.setVisible(False)
#
#     def load_file(self):
#         path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")
#         if path:
#             self.df = pd.read_excel(path)
#             self.df.columns = self.df.columns.str.strip()
#             self.file_label.setText(f"Loaded: {os.path.basename(path)}")
#             self.graph_type.setVisible(True)
#             self.plot_btn.setVisible(True)
#
#     def plot_graph(self):
#         try:
#             graph_type = self.graph_type.currentText()
#             defect_type = self.defect_category.currentText()
#             view = self.view_type.currentText()
#
#             if graph_type:
#                 if graph_type == "Defects":
#                     if not defect_type:
#                         self.file_label.setText("Please select defect category.")
#                         return
#
#                     if defect_type == "Pitting":
#                         fig, path = plot_pitting(self.df.copy(), return_fig=True)
#                     elif defect_type == "General":
#                         fig, path = plot_general(self.df.copy(), return_fig=True)
#                     elif defect_type == "Corrosion":
#                         fig, path = plot_corrosion(self.df.copy(), return_fig=True)
#                     else:
#                         self.file_label.setText("Invalid defect category.")
#                         return
#
#                     self.current_fig = fig
#                     self.browser.load(QUrl.fromLocalFile(path))
#                     self.save_btn.setVisible(True)
#
#                 else:  # For ERF, Psafe, Depth, Orientation
#                     if not view:
#                         self.file_label.setText("Please select surface view.")
#                         return
#
#                     if graph_type == "ERF":
#                         fig, path = plot_erf(self.df.copy(), view, return_fig=True)
#                     elif graph_type == "Psafe":
#                         fig, path = plot_psafe(self.df.copy(), view, return_fig=True)
#                     elif graph_type == "Depth":
#                         fig, path = plot_depth(self.df.copy(), view, return_fig=True)
#                     elif graph_type == "Orientation":
#                         fig, path = plot_orientation(self.df.copy(), view, return_fig=True)
#                     else:
#                         self.file_label.setText("Invalid graph type.")
#                         return
#
#                     self.current_fig = fig
#                     self.browser.load(QUrl.fromLocalFile(path))
#                     self.save_btn.setVisible(True)
#
#             else:
#                 self.file_label.setText("Please select a graph type.")
#
#         except Exception as e:
#             self.file_label.setText(f"Plot failed: {str(e)}")
#             self.current_fig = None
#
#     def save_graph(self):
#         if hasattr(self, 'current_fig') and self.current_fig is not None:
#             downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
#             default_file = os.path.join(downloads_folder, "graph.png")
#
#             file_path, _ = QFileDialog.getSaveFileName(
#                 self,
#                 "Save Plot as PNG",
#                 default_file,
#                 "PNG Files (*.png);;All Files (*)"
#             )
#
#             if file_path:
#                 try:
#                     if not file_path.lower().endswith(".png"):
#                         file_path += ".png"
#
#                     self.current_fig.write_image(file_path)
#                     self.file_label.setText(f"Graph saved as: {file_path}")
#                 except Exception as e:
#                     self.file_label.setText(f"Failed to save graph: {str(e)}")
#             else:
#                 self.file_label.setText("No file path selected.")
#         else:
#             self.file_label.setText("No graph to save.")
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     viewer = GraphApp()
#     viewer.show()
#     sys.exit(app.exec_())
#
#
#
#
#
#


















import sys
import os
import pandas as pd
import plotly.io as pio
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel,
    QComboBox, QSizePolicy, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
# from PyQt5.QtGui import QPixmap -- company software change 

# Importing the plotting functions
# from erf2 import plot_erf
# from psafe1 import plot_psafe
# from depth_percent import plot_depth
# from orientation import plot_orientation
# Replace imports in `main_gui.py`
from GMFL_12_Inch_Desktop.Tabs.TAB_8_graphs.widgets.graphs_maker import plot_erf, plot_psafe, plot_depth, plot_orientation
from GMFL_12_Inch_Desktop.extras.Defects import (plot_metal_loss, plot_sensor_percentage, plot_temperature)# Metal Loss and Sensor Loss Plot functions

# Ensure PNG saving using kaleido
pio.kaleido.scope.default_format = "png"


class GraphApp(QWidget):
    def __init__(self):
        super().__init__()
        self.df = None
        self.setWindowTitle("Pipeline Defect Graph Viewer")
        self.setGeometry(200, 100, 1100, 800)

        # ---------------- Main Layout ----------------
        self.layout = QVBoxLayout()

        # File load status label
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("font-size: 13px; color: #333;")
        self.layout.addWidget(self.file_label)

        # Load file button
        self.load_btn = QPushButton("Load Excel File")
        self.load_btn.setFixedWidth(180)
        self.load_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                padding: 6px 12px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        self.load_btn.clicked.connect(self.load_file)
        self.layout.addWidget(self.load_btn)

        # ---------------- Controls Section ----------------
        from PyQt5.QtWidgets import QGroupBox, QFormLayout
        controls_box = QGroupBox("Graph Controls")
        controls_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                color: #222;
                border: 1px solid #aaa;
                border-radius: 6px;
                margin-top: 10px;
                background-color: #fafafa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QLabel {
                font-size: 12px;
                color: #333;
            }
            QComboBox {
                padding: 4px;
                border: 1px solid #ccc;
                border-radius: 4px;
                min-width: 180px;
            }
        """)
        form_layout = QFormLayout()

        # Graph Type Dropdown
        self.graph_type_label = QLabel("Select Graph Type:")
        self.graph_type_label.setVisible(False)
        self.graph_type = QComboBox()
        self.graph_type.setFixedWidth(180)
        self.graph_type.addItems(["", "Defects", "ERF", "Psafe", "Depth", "Orientation", "Temperature", "Sensor Loss"])
        self.graph_type.setVisible(False)
        self.graph_type.currentTextChanged.connect(self.on_graph_type_changed)
        form_layout.addRow(self.graph_type_label, self.graph_type)

        # Feature Identification
        self.feature_identification_label = QLabel("Feature Identification:")
        self.feature_identification_label.setVisible(False)
        self.feature_identification = QComboBox()
        self.feature_identification.setFixedWidth(180)
        self.feature_identification.addItems(["", "Corrosion", "MFG", "Both(Corrosion,MFG)"])
        self.feature_identification.setVisible(False)
        self.feature_identification.currentTextChanged.connect(self.on_feature_identification_changed)
        form_layout.addRow(self.feature_identification_label, self.feature_identification)

        # Dimensional Classification
        self.dimension_classification_label = QLabel("Dimensional Classification:")
        self.dimension_classification_label.setVisible(False)
        self.dimension_classification = QComboBox()
        self.dimension_classification.setFixedWidth(180)
        self.dimension_classification.addItems([
            "", "Pitting", "Axial Grooving", "Axial Slotting",
            "Circumferential Grooving", "Circumferential Slotting",
            "Pinhole", "General"
        ])
        self.dimension_classification.setVisible(False)
        form_layout.addRow(self.dimension_classification_label, self.dimension_classification)

        # Surface View
        self.view_type_label = QLabel("Surface View:")
        self.view_type_label.setVisible(False)
        self.view_type = QComboBox()
        self.view_type.setFixedWidth(180)
        self.view_type.addItems(["", "Internal", "External", "Both"])
        self.view_type.setVisible(False)
        form_layout.addRow(self.view_type_label, self.view_type)

        # Plot Button
        self.plot_btn = QPushButton("Plot Graph")
        self.plot_btn.setFixedWidth(150)
        self.plot_btn.setVisible(False)
        self.plot_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 6px 12px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.plot_btn.clicked.connect(self.plot_graph)
        form_layout.addRow(self.plot_btn)

        controls_box.setLayout(form_layout)
        self.layout.addWidget(controls_box)

        # Save Button
        self.save_btn = QPushButton("Save Graph as PNG")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                padding: 6px 15px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        self.save_btn.setFixedWidth(200)
        self.save_btn.setVisible(False)
        self.save_btn.clicked.connect(self.save_graph)
        self.layout.addWidget(self.save_btn)

        # Graph display
        self.browser = QWebEngineView()
        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.browser)

        # Apply Layout
        self.setLayout(self.layout)

    # def on_graph_type_changed(self, text):
    #     if text == "Defects":
    #         # When Metal Loss is selected, show feature identification and dimensional classification dropdowns
    #         self.feature_identification_label.setVisible(True)
    #         self.feature_identification.setVisible(True)
    #         self.dimension_classification_label.setVisible(True)
    #         self.dimension_classification.setVisible(True)
    #         self.view_type_label.setVisible(False)
    #         self.view_type.setVisible(False)
    #     elif text in ["ERF", "Psafe", "Depth", "Orientation"]:
    #         # When any of these are selected, show the surface view dropdown
    #         self.feature_identification_label.setVisible(False)
    #         self.feature_identification.setVisible(False)
    #         self.dimension_classification_label.setVisible(False)
    #         self.dimension_classification.setVisible(False)
    #         self.view_type_label.setVisible(True)
    #         self.view_type.setVisible(True)
    #     elif text == "Sensor Loss":
    #         # When Sensor Loss is selected, hide the feature and dimension dropdowns and the surface view dropdown
    #         self.feature_identification_label.setVisible(False)
    #         self.feature_identification.setVisible(False)
    #         self.dimension_classification_label.setVisible(False)
    #         self.dimension_classification.setVisible(False)
    #         self.view_type_label.setVisible(False)
    #         self.view_type.setVisible(False)
    #
    #     elif text == "Temperature":
    #         # When Sensor Loss is selected, hide the feature and dimension dropdowns and the surface view dropdown
    #         self.feature_identification_label.setVisible(False)
    #         self.feature_identification.setVisible(False)
    #         self.dimension_classification_label.setVisible(False)
    #         self.dimension_classification.setVisible(False)
    #         self.view_type_label.setVisible(False)
    #         self.view_type.setVisible(False)
    #
    #     else:
    #         # If no valid graph type is selected, hide all dropdowns and their titles
    #         self.feature_identification_label.setVisible(False)
    #         self.feature_identification.setVisible(False)
    #         self.dimension_classification_label.setVisible(False)
    #         self.dimension_classification.setVisible(False)
    #         self.view_type_label.setVisible(False)
    #         self.view_type.setVisible(False)

    def on_graph_type_changed(self, text):
        # Clear previous selections when a new graph type is selected
        self.view_type.setCurrentIndex(0)  # Reset the surface view
        self.feature_identification.setCurrentIndex(0)  # Reset the feature identification
        self.dimension_classification.setCurrentIndex(0)  # Reset the dimension classification

        if text == "Defects":
            # When Metal Loss is selected, show feature identification and dimensional classification dropdowns
            self.feature_identification_label.setVisible(True)
            self.feature_identification.setVisible(True)
            self.dimension_classification_label.setVisible(True)
            self.dimension_classification.setVisible(True)
            self.view_type_label.setVisible(False)
            self.view_type.setVisible(False)
        elif text in ["ERF", "Psafe", "Orientation"]:
            # When any of these are selected, show the surface view dropdown
            self.feature_identification_label.setVisible(False)
            self.feature_identification.setVisible(False)
            self.dimension_classification_label.setVisible(False)
            self.dimension_classification.setVisible(False)
            self.view_type_label.setVisible(True)
            self.view_type.setVisible(True)
        elif text in ["Depth"]:
            self.feature_identification_label.setVisible(False)
            self.feature_identification.setVisible(False)
            self.dimension_classification_label.setVisible(False)
            self.dimension_classification.setVisible(False)
            self.view_type_label.setVisible(False)
            self.view_type.setVisible(False)

        elif text == "Sensor Loss":
            # When Sensor Loss is selected, hide the feature and dimension dropdowns and the surface view dropdown
            self.feature_identification_label.setVisible(False)
            self.feature_identification.setVisible(False)
            self.dimension_classification_label.setVisible(False)
            self.dimension_classification.setVisible(False)
            self.view_type_label.setVisible(False)
            self.view_type.setVisible(False)
        elif text == "Temperature":
            # When Temperature is selected, hide the feature and dimension dropdowns and the surface view dropdown
            self.feature_identification_label.setVisible(False)
            self.feature_identification.setVisible(False)
            self.dimension_classification_label.setVisible(False)
            self.dimension_classification.setVisible(False)
            self.view_type_label.setVisible(False)
            self.view_type.setVisible(False)
        else:
            # If no valid graph type is selected, hide all dropdowns and their titles
            self.feature_identification_label.setVisible(False)
            self.feature_identification.setVisible(False)
            self.dimension_classification_label.setVisible(False)
            self.dimension_classification.setVisible(False)
            self.view_type_label.setVisible(False)
            self.view_type.setVisible(False)

    def on_feature_identification_changed(self, text):
        # Reset the Dimensional Classification dropdown whenever Feature Identification changes
        self.dimension_classification.setCurrentIndex(0)  # Reset to the first option (empty)

        # No need to disable Dimensional Classification, keep it always enabled
        self.dimension_classification.setEnabled(True)

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")
        if path:
            self.df = pd.read_excel(path)
            self.df.columns = self.df.columns.str.strip()
            self.file_label.setText(f"Loaded: {os.path.basename(path)}")

            # After the file is loaded, show the Graph Type dropdown and its title
            self.graph_type_label.setVisible(True)
            self.graph_type.setVisible(True)
            self.plot_btn.setVisible(True)

    def plot_graph(self):
        try:
            graph_type = self.graph_type.currentText()
            feature = self.feature_identification.currentText()
            dimension = self.dimension_classification.currentText()
            view = self.view_type.currentText()

            if not graph_type:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Graph Type Not Selected")
                msg.setText("Please select the graph type before plotting.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return

            max_oddo = self.df['Abs. Distance (m)'].max()

            if graph_type == "Defects":
                if not feature and dimension == "":
                    QMessageBox.warning(self, "Selection Missing",
                                        "Please select either Feature Identification or Dimensional Classification.")
                    return

                feature_id = feature if feature else None
                dimension_class = dimension if dimension != "Both" else None

                # ✅ Call plot_metal_loss with tally_max_distance
                fig, path = plot_metal_loss(
                    self.df.copy(),
                    feature_type=feature_id,
                    dimension_class=dimension_class,
                    tally_max_distance=max_oddo,
                    return_fig=True
                )

                self.current_fig = fig
                self.browser.load(QUrl.fromLocalFile(path))
                self.save_btn.setVisible(True)

            # if graph_type == "Defects":
            #     if not feature and dimension == "":
            #         msg = QMessageBox()
            #         msg.setIcon(QMessageBox.Warning)
            #         msg.setWindowTitle("Feature Identification or Dimensional Classification Not Selected")
            #         msg.setText("Please select either Feature Identification or Dimensional Classification.")
            #         msg.setStandardButtons(QMessageBox.Ok)
            #         msg.exec_()
            #         return
            #
            #     feature_id = feature if feature else None
            #     dimension_class = dimension if dimension != "Both" else None
            #
            #     # Plot Metal Loss
            #     fig, path = plot_metal_loss(self.df.copy(), feature_type=feature_id, dimension_class=dimension_class, return_fig=True)
            #     self.current_fig = fig
            #     self.browser.load(QUrl.fromLocalFile(path))
            #     self.save_btn.setVisible(True)

            elif graph_type in ["ERF", "Psafe", "Orientation"]:
                if not view:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setWindowTitle("Surface View Not Selected")
                    msg.setText("Please select Surface View before plotting.")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
                    return

                if graph_type == "ERF":
                    fig, path = plot_erf(self.df.copy(), view, return_fig=True)
                elif graph_type == "Psafe":
                    fig, path = plot_psafe(self.df.copy(), view, return_fig=True)

                elif graph_type == "Orientation":
                    fig, path = plot_orientation(self.df.copy(), view, return_fig=True)

                self.current_fig = fig
                self.browser.load(QUrl.fromLocalFile(path))
                self.save_btn.setVisible(True)

            elif graph_type == "Depth":
                fig, path = plot_depth(self.df.copy(), view, return_fig=True)
                self.current_fig = fig
                self.browser.load(QUrl.fromLocalFile(path))
                self.save_btn.setVisible(True)

            elif graph_type == "Sensor Loss":
                # Plot Sensor Loss
                fig, path = plot_sensor_percentage(self.df.copy(), return_fig=True)  # Fix here by passing only return_fig
                self.current_fig = fig
                self.browser.load(QUrl.fromLocalFile(path))
                self.save_btn.setVisible(True)

            elif graph_type == "Temperature":
                # Plot Sensor Loss
                fig, path = plot_temperature(self.df.copy(), return_fig=True)  # Fix here by passing only return_fig
                self.current_fig = fig
                self.browser.load(QUrl.fromLocalFile(path))
                self.save_btn.setVisible(True)

            else:
                self.file_label.setText("Please select a graph type.")

        except Exception as e:
            self.file_label.setText(f"Plot failed: {str(e)}")
            self.current_fig = None

    def save_graph(self):
        if hasattr(self, 'current_fig') and self.current_fig is not None:
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            default_file = os.path.join(downloads_folder, "graph.png")

            file_path, _ = QFileDialog.getSaveFileName(self, "Save Plot as PNG", default_file, "PNG Files (*.png);;All Files (*)")
            if file_path:
                try:
                    if not file_path.lower().endswith(".png"):
                        file_path += ".png"

                    if hasattr(self.current_fig,"write_image"):
                        self.current_fig.write_image(file_path)
                    elif hasattr(self.current_fig, "savefig"):
                        self.current_fig.savefig(file_path)
                    else:
                        self.file_label.setText("Unrecognized figure format.")
                        return

                    self.file_label.setText(f"Graph saved as: {file_path}")
                except Exception as e:
                    self.file_label.setText(f"Failed to save graph: {str(e)}")
            else:
                self.file_label.setText("No file path selected.")
        else:
            self.file_label.setText("No graph to save.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = GraphApp()
    viewer.show()
    sys.exit(app.exec_())

# import sys
# import os
# import pandas as pd
# import plotly.io as pio
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel,
#     QComboBox, QSizePolicy, QTabWidget
# )
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtCore import Qt, QUrl
#
# # Import your plotting functions
# from graphs import plot_erf, plot_psafe, plot_depth, plot_orientation
# from Defects import plot_metal_loss, plot_sensor_percentage, plot_temperature
#
# # Ensure PNG saving using kaleido
# pio.kaleido.scope.default_format = "png"
#
#
# class GraphApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.df = None
#         self.setWindowTitle("Pipeline Defect Graph Viewer")
#         self.setGeometry(200, 100, 1100, 800)
#
#         # Create a tab widget
#         self.tab_widget = QTabWidget()
#
#         # Create the first tab (empty)
#         self.tab1 = QWidget()
#         self.tab1_layout = QVBoxLayout()
#         self.tab1_layout.addWidget(QLabel("Tab 1 is empty"))
#         self.tab1.setLayout(self.tab1_layout)
#
#         # Create the second tab (your main GUI with graphs)
#         self.tab2 = QWidget()
#         self.tab2_layout = QVBoxLayout()
#
#         # Add your existing main_gui UI elements to tab2
#         self.file_label = QLabel("No file selected")
#         self.tab2_layout.addWidget(self.file_label)
#
#         # Load file button
#         self.load_btn = QPushButton("Load Excel File")
#         self.load_btn.clicked.connect(self.load_file)
#         self.tab2_layout.addWidget(self.load_btn)
#
#         # Graph Type Dropdown
#         self.graph_type_label = QLabel("Select Graph Type:")
#         self.graph_type = QComboBox()
#         self.graph_type.addItems(["", "Defects", "ERF", "Psafe", "Depth", "Orientation", "Temperature", "Sensor Loss"])
#         self.graph_type.currentTextChanged.connect(self.on_graph_type_changed)
#         self.tab2_layout.addWidget(self.graph_type_label)
#         self.tab2_layout.addWidget(self.graph_type)
#
#         # Feature Identification dropdown, initially hidden
#         self.feature_identification_label = QLabel("Select Feature Identification:")
#         self.feature_identification = QComboBox()
#         self.feature_identification.addItems(["", "Corrosion", "MFG", "Both(Corrosion,MFG)"])
#         self.tab2_layout.addWidget(self.feature_identification_label)
#         self.tab2_layout.addWidget(self.feature_identification)
#
#         # Dimensional Classification dropdown, initially hidden
#         self.dimension_classification_label = QLabel("Select Dimensional Classification:")
#         self.dimension_classification = QComboBox()
#         self.dimension_classification.addItems(
#             ["", "Pitting", "Axial Grooving", "Axial Slotting", "Circumferential Grooving", "Circumferential Slotting",
#              "Pinhole", "General"])
#         self.tab2_layout.addWidget(self.dimension_classification_label)
#         self.tab2_layout.addWidget(self.dimension_classification)
#
#         # Surface View dropdown, initially hidden
#         self.view_type_label = QLabel("Select Surface View:")
#         self.view_type = QComboBox()
#         self.view_type.addItems(["", "Internal", "External", "Both"])
#         self.tab2_layout.addWidget(self.view_type_label)
#         self.tab2_layout.addWidget(self.view_type)
#
#         # Plot Button
#         self.plot_btn = QPushButton("Plot Graph")
#         self.plot_btn.clicked.connect(self.plot_graph)
#         self.tab2_layout.addWidget(self.plot_btn)
#
#         # Save Button
#         self.save_btn = QPushButton("Save Graph as PNG")
#         self.save_btn.clicked.connect(self.save_graph)
#         self.tab2_layout.addWidget(self.save_btn)
#
#         # Browser for displaying graphs
#         self.browser = QWebEngineView()
#         self.tab2_layout.addWidget(self.browser)
#
#         self.tab2.setLayout(self.tab2_layout)
#
#         # Add tabs to the tab widget
#         self.tab_widget.addTab(self.tab1, "Tab 1")
#         self.tab_widget.addTab(self.tab2, "Tab 2")
#
#         # Set the layout for the main window
#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.tab_widget)
#         self.setLayout(self.layout)
#
#     def on_graph_type_changed(self, text):
#         # Reset previous selections when a new graph type is selected
#         self.view_type.setCurrentIndex(0)  # Reset the surface view
#         self.feature_identification.setCurrentIndex(0)  # Reset the feature identification
#         self.dimension_classification.setCurrentIndex(0)  # Reset the dimension classification
#
#         if text == "Defects":
#             # When Defects is selected, show the necessary dropdowns
#             self.feature_identification_label.setVisible(True)
#             self.feature_identification.setVisible(True)
#             self.dimension_classification_label.setVisible(True)
#             self.dimension_classification.setVisible(True)
#             self.view_type_label.setVisible(False)
#             self.view_type.setVisible(False)
#         else:
#             # Hide dropdowns if they are not needed
#             self.feature_identification_label.setVisible(False)
#             self.feature_identification.setVisible(False)
#             self.dimension_classification_label.setVisible(False)
#             self.dimension_classification.setVisible(False)
#             self.view_type_label.setVisible(True)
#             self.view_type.setVisible(True)
#
#     def load_file(self):
#         path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")
#         if path:
#             self.df = pd.read_excel(path)
#             self.df.columns = self.df.columns.str.strip()
#             self.file_label.setText(f"Loaded: {os.path.basename(path)}")
#
#     def plot_graph(self):
#         graph_type = self.graph_type.currentText()
#         feature = self.feature_identification.currentText()
#         dimension = self.dimension_classification.currentText()
#         view = self.view_type.currentText()
#
#         try:
#             if graph_type == "Defects":
#                 if not feature and not dimension:
#                     self.file_label.setText("Please select Feature Identification or Dimensional Classification.")
#                     return
#
#                 # Plot Metal Loss or other types based on the feature and dimension
#                 fig, path = plot_metal_loss(self.df.copy(), feature_type=feature, dimension_class=dimension,
#                                             return_fig=True)
#                 self.browser.load(QUrl.fromLocalFile(path))
#
#             elif graph_type == "ERF":
#                 fig, path = plot_erf(self.df.copy(), view, return_fig=True)
#                 self.browser.load(QUrl.fromLocalFile(path))
#
#             elif graph_type == "Psafe":
#                 fig, path = plot_psafe(self.df.copy(), view, return_fig=True)
#                 self.browser.load(QUrl.fromLocalFile(path))
#
#             elif graph_type == "Temperature":
#                 fig, path = plot_temperature(self.df.copy(), return_fig=True)
#                 self.browser.load(QUrl.fromLocalFile(path))
#
#             # Add more cases for other graph types (Sensor Loss, etc.)
#
#         except Exception as e:
#             self.file_label.setText(f"Plot failed: {str(e)}")
#
#     def save_graph(self):
#         if hasattr(self, 'current_fig') and self.current_fig is not None:
#             downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
#             default_file = os.path.join(downloads_folder, "graph.png")
#             file_path, _ = QFileDialog.getSaveFileName(self, "Save Plot as PNG", default_file,
#                                                        "PNG Files (*.png);;All Files (*)")
#             if file_path:
#                 try:
#                     if not file_path.lower().endswith(".png"):
#                         file_path += ".png"
#                     self.current_fig.write_image(file_path)
#                     self.file_label.setText(f"Graph saved as: {file_path}")
#                 except Exception as e:
#                     self.file_label.setText(f"Failed to save graph: {str(e)}")
#             else:
#                 self.file_label.setText("No file path selected.")
#         else:
#             self.file_label.setText("No graph to save.")
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = GraphApp()
#     window.show()
#     sys.exit(app.exec_())

########################################################################################################################################################
# def __init__(self):
#     super().__init__()
#     self.df = None
#     self.setWindowTitle("Pipeline Defect Graph Viewer")
#     self.setGeometry(200, 100, 1100, 800)
#
#     # ---------------- Main Layout ----------------
#     self.layout = QVBoxLayout()
#
#     # File load status label
#     self.file_label = QLabel("No file selected")
#     self.file_label.setStyleSheet("font-size: 13px; color: #333;")
#     self.layout.addWidget(self.file_label)
#
#     # Load file button
#     self.load_btn = QPushButton("Load Excel File")
#     self.load_btn.setFixedWidth(180)
#     self.load_btn.setStyleSheet("""
#         QPushButton {
#             background-color: #0078d7;
#             color: white;
#             padding: 6px 12px;
#             font-weight: bold;
#             border-radius: 5px;
#         }
#         QPushButton:hover {
#             background-color: #005a9e;
#         }
#     """)
#     self.load_btn.clicked.connect(self.load_file)
#     self.layout.addWidget(self.load_btn)
#
#     # ---------------- Controls Section ----------------
#     from PyQt5.QtWidgets import QGroupBox, QFormLayout
#     controls_box = QGroupBox("Graph Controls")
#     controls_box.setStyleSheet("""
#         QGroupBox {
#             font-weight: bold;
#             font-size: 13px;
#             color: #222;
#             border: 1px solid #aaa;
#             border-radius: 6px;
#             margin-top: 10px;
#             background-color: #fafafa;
#         }
#         QGroupBox::title {
#             subcontrol-origin: margin;
#             left: 10px;
#             padding: 0 3px;
#         }
#         QLabel {
#             font-size: 12px;
#             color: #333;
#         }
#         QComboBox {
#             padding: 4px;
#             border: 1px solid #ccc;
#             border-radius: 4px;
#             min-width: 180px;
#         }
#     """)
#     form_layout = QFormLayout()
#
#     # Graph Type Dropdown
#     self.graph_type_label = QLabel("Select Graph Type:")
#     self.graph_type_label.setVisible(False)
#     self.graph_type = QComboBox()
#     self.graph_type.setFixedWidth(180)
#     self.graph_type.addItems(["", "Defects", "ERF", "Psafe", "Depth", "Orientation", "Temperature", "Sensor Loss"])
#     self.graph_type.setVisible(False)
#     self.graph_type.currentTextChanged.connect(self.on_graph_type_changed)
#     form_layout.addRow(self.graph_type_label, self.graph_type)
#
#     # Feature Identification
#     self.feature_identification_label = QLabel("Feature Identification:")
#     self.feature_identification_label.setVisible(False)
#     self.feature_identification = QComboBox()
#     self.feature_identification.setFixedWidth(180)
#     self.feature_identification.addItems(["", "Corrosion", "MFG", "Both(Corrosion,MFG)"])
#     self.feature_identification.setVisible(False)
#     self.feature_identification.currentTextChanged.connect(self.on_feature_identification_changed)
#     form_layout.addRow(self.feature_identification_label, self.feature_identification)
#
#     # Dimensional Classification
#     self.dimension_classification_label = QLabel("Dimensional Classification:")
#     self.dimension_classification_label.setVisible(False)
#     self.dimension_classification = QComboBox()
#     self.dimension_classification.setFixedWidth(180)
#     self.dimension_classification.addItems([
#         "", "Pitting", "Axial Grooving", "Axial Slotting",
#         "Circumferential Grooving", "Circumferential Slotting",
#         "Pinhole", "General"
#     ])
#     self.dimension_classification.setVisible(False)
#     form_layout.addRow(self.dimension_classification_label, self.dimension_classification)
#
#     # Surface View
#     self.view_type_label = QLabel("Surface View:")
#     self.view_type_label.setVisible(False)
#     self.view_type = QComboBox()
#     self.view_type.setFixedWidth(180)
#     self.view_type.addItems(["", "Internal", "External", "Both"])
#     self.view_type.setVisible(False)
#     form_layout.addRow(self.view_type_label, self.view_type)
#
#     # Plot Button
#     self.plot_btn = QPushButton("Plot Graph")
#     self.plot_btn.setFixedWidth(150)
#     self.plot_btn.setVisible(False)
#     self.plot_btn.setStyleSheet("""
#         QPushButton {
#             background-color: #28a745;
#             color: white;
#             padding: 6px 12px;
#             border-radius: 5px;
#             font-weight: bold;
#         }
#         QPushButton:hover {
#             background-color: #218838;
#         }
#     """)
#     self.plot_btn.clicked.connect(self.plot_graph)
#     form_layout.addRow(self.plot_btn)
#
#     controls_box.setLayout(form_layout)
#     self.layout.addWidget(controls_box)
#
#     # Save Button
#     self.save_btn = QPushButton("Save Graph as PNG")
#     self.save_btn.setStyleSheet("""
#         QPushButton {
#             background-color: #444;
#             color: white;
#             padding: 6px 15px;
#             font-weight: bold;
#             border-radius: 5px;
#         }
#         QPushButton:hover {
#             background-color: #666;
#         }
#     """)
#     self.save_btn.setFixedWidth(200)
#     self.save_btn.setVisible(False)
#     self.save_btn.clicked.connect(self.save_graph)
#     self.layout.addWidget(self.save_btn)
#
#     # Graph display
#     self.browser = QWebEngineView()
#     self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#     self.layout.addWidget(self.browser)
#
#     # Apply Layout
#     self.setLayout(self.layout)
