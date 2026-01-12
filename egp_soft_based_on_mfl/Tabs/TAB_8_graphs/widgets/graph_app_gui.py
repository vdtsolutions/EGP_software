

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
from pyqt5_plugins.examplebutton import QtWidgets

from egp_soft_based_on_mfl.Tabs.TAB_8_graphs.widgets.graphs_maker import plot_erf, plot_psafe, plot_depth, plot_orientation
from egp_soft_based_on_mfl.extras.Defects import (plot_metal_loss, plot_sensor_percentage, plot_temperature)# Metal Loss and Sensor Loss Plot functions
from .magnetization import Magnetization
from .velocity import Velocity

# Ensure PNG saving using kaleidoT
pio.kaleido.scope.default_format = "png"


class GraphApp(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.config = self.parent.config
        self.df = None
        self.runid = self.parent.parent.runid
        # print(f"runid: {self.runid}")
        # self.weld_id = self.parent.parent.weld_id
        # print(f"weld_io: {self.weld_id}")
        self.setWindowTitle("Pipeline Defect Graph Viewer")
        self.setGeometry(200, 100, 1100, 800)

        # ---------------- Main Layout ----------------
        self.layout = QVBoxLayout()

        # File load status label
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("font-size: 13px; color: #333;")
        self.layout.addWidget(self.file_label)

        # Load file button
        # self.load_btn = QPushButton("Load Excel File")
        # self.load_btn.setFixedWidth(180)
        # self.load_btn.setStyleSheet("""
        #     QPushButton {
        #         background-color: #0078d7;
        #         color: white;
        #         padding: 6px 12px;
        #         font-weight: bold;
        #         border-radius: 5px;
        #     }
        #     QPushButton:hover {
        #         background-color: #005a9e;
        #     }
        # """)
        # self.load_btn.clicked.connect(self.load_file)
        # self.layout.addWidget(self.load_btn)

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
        self.graph_type.addItems(["", "Defects", "ERF", "Psafe", "Depth", "Orientation", "Temperature", "Sensor Loss", "Velocity", "Magnetization"])
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

        # --- Pipe ID Dropdown ---
        self.pipe_id_label = QLabel("Select Pipe ID:")
        self.pipe_id_label.setVisible(False)

        self.pipe_id_dropdown = QComboBox()
        self.pipe_id_dropdown.setFixedWidth(180)
        self.pipe_id_dropdown.setVisible(False)

        # Get items from parent combo_graph (assuming it’s already populated)
        pipe_ids = getattr(self.parent.parent, "pipe_ids", [])
        self.pipe_id_dropdown.addItems([""] + pipe_ids)

        # Optional: connect change event
        self.pipe_id_dropdown.currentTextChanged.connect(self.on_pipe_id_changed)

        # Add to layout
        form_layout.addRow(self.pipe_id_label, self.pipe_id_dropdown)

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


    def on_pipe_id_changed(self, pipe_id):
        if pipe_id:
            print(f"Selected Pipe ID: {pipe_id}")
        else:
            print("No pipe selected")

    def on_graph_type_changed(self, text):
        # Clear previous selections when a new graph type is selected
        self.view_type.setCurrentIndex(0)  # Reset the surface view
        self.feature_identification.setCurrentIndex(0)  # Reset the feature identification
        self.dimension_classification.setCurrentIndex(0)  # Reset the dimension classification

        if text == "Defects":
            # When Metal Loss is selected, show feature identification and dimensional classification dropdowns
            self.pipe_id_label.setVisible(False)
            self.pipe_id_dropdown.setVisible(False)
            self.feature_identification_label.setVisible(True)
            self.feature_identification.setVisible(True)
            self.dimension_classification_label.setVisible(True)
            self.dimension_classification.setVisible(True)
            self.view_type_label.setVisible(False)
            self.view_type.setVisible(False)
        elif text in ["ERF", "Psafe", "Orientation"]:
            # When any of these are selected, show the surface view dropdown
            self.pipe_id_label.setVisible(False)
            self.pipe_id_dropdown.setVisible(False)
            self.feature_identification_label.setVisible(False)
            self.feature_identification.setVisible(False)
            self.dimension_classification_label.setVisible(False)
            self.dimension_classification.setVisible(False)
            self.view_type_label.setVisible(True)
            self.view_type.setVisible(True)
        elif text in ["Depth"]:
            self.pipe_id_label.setVisible(False)
            self.pipe_id_dropdown.setVisible(False)
            self.feature_identification_label.setVisible(False)
            self.feature_identification.setVisible(False)
            self.dimension_classification_label.setVisible(False)
            self.dimension_classification.setVisible(False)
            self.view_type_label.setVisible(False)
            self.view_type.setVisible(False)

        elif text == "Sensor Loss":
            # When Sensor Loss is selected, hide the feature and dimension dropdowns and the surface view dropdown
            self.pipe_id_label.setVisible(False)
            self.pipe_id_dropdown.setVisible(False)
            self.feature_identification_label.setVisible(False)
            self.feature_identification.setVisible(False)
            self.dimension_classification_label.setVisible(False)
            self.dimension_classification.setVisible(False)
            self.view_type_label.setVisible(False)
            self.view_type.setVisible(False)
        elif text in ["Temperature" ]:
            # When Temperature is selected, hide the feature and dimension dropdowns and the surface view dropdown
            self.pipe_id_label.setVisible(False)
            self.pipe_id_dropdown.setVisible(False)
            self.feature_identification_label.setVisible(False)
            self.feature_identification.setVisible(False)
            self.dimension_classification_label.setVisible(False)
            self.dimension_classification.setVisible(False)
            self.view_type_label.setVisible(False)
            self.view_type.setVisible(False)

        elif text in ["Magnetization", "Velocity"]:
            # Show Pipe ID dropdown for these graph types
            self.pipe_id_label.setVisible(True)
            self.pipe_id_dropdown.setVisible(True)
            self.feature_identification_label.setVisible(False)
            self.feature_identification.setVisible(False)
            self.dimension_classification_label.setVisible(False)
            self.dimension_classification.setVisible(False)
            self.view_type_label.setVisible(False)
            self.view_type.setVisible(False)
            # Optional: repopulate from combo_graph each time
            self.pipe_id_dropdown.clear()
            pipe_ids = [self.parent.combo_graph.itemText(i) for i in range(self.parent.combo_graph.count())]
            self.pipe_id_dropdown.addItems([""] + pipe_ids)
        else:
            # If no valid graph type is selected, hide all dropdowns and their titles
            self.pipe_id_label.setVisible(False)
            self.pipe_id_dropdown.setVisible(False)
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
        path = self.parent.parent.pipetally  # <<< GET GLOBAL PIPETALLY
        if not path:
            QMessageBox.warning(self, "Error", "Please load Pipetally from File → Load Pipetally")
            return

        self.df = pd.read_excel(path)
        self.df.columns = self.df.columns.str.strip()
        self.file_label.setText(f"Loaded: {os.path.basename(path)}")

        # Show graph options
        self.graph_type_label.setVisible(True)
        self.graph_type.setVisible(True)
        self.plot_btn.setVisible(True)

    def plot_graph(self):
        selected_pipe_id = self.pipe_id_dropdown.currentText()
        # self.df = self.load_file()
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

            elif graph_type == "Magnetization":
                try:
                    html_path = Magnetization(self, selected_pipe_id)  # call the function, it should return HTML path
                    if html_path and os.path.exists(html_path):
                        self.browser.load(QUrl.fromLocalFile(html_path))
                        self.save_btn.setVisible(True)
                    else:
                        self.file_label.setText("Magnetization: HTML not generated or missing.")
                except Exception as e:
                    self.file_label.setText(f"Magnetization failed: {e}")

            elif graph_type == "Velocity":
                try:
                    html_path = Velocity(self, selected_pipe_id)  # same logic for velocity
                    if html_path and os.path.exists(html_path):
                        self.browser.load(QUrl.fromLocalFile(html_path))
                        self.save_btn.setVisible(True)
                    else:
                        self.file_label.setText("Velocity: HTML not generated or missing.")
                except Exception as e:
                    self.file_label.setText(f"Velocity failed: {e}")


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
    import traceback


    def global_exception_hook(exctype, value, tb):
        """Catches all uncaught exceptions and shows them in an enlarged dialog."""
        error_text = "".join(traceback.format_exception(exctype, value, tb))
        print("\n--- Uncaught Exception ---")
        print(error_text)
        print("---------------------------\n")

        try:
            # Create larger dialog box
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("⚠️ Unexpected Error")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText(str(value))

            # Expandable details section (full traceback)
            msg.setDetailedText(error_text)

            # Force bigger window
            msg.setStyleSheet("""
                    QMessageBox {
                        min-width: 900px;
                        min-height: 600px;
                        font-size: 12pt;
                    }
                    QMessageBox QLabel {
                        font-size: 12pt;
                    }
                    QPushButton {
                        padding: 8px 20px;
                        font-size: 11pt;
                    }
                """)

            msg.exec_()
        except Exception:
            pass


    sys.excepthook = global_exception_hook
    app = QApplication(sys.argv)
    viewer = GraphApp()
    viewer.show()
    sys.exit(app.exec_())

