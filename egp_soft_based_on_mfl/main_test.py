import sys
from PyQt5 import QtWidgets
import warnings
warnings.filterwarnings('ignore')
import importlib.metadata

if not hasattr(importlib.metadata, "packages_distributions"):
    def packages_distributions():
        return {}
    importlib.metadata.packages_distributions = packages_distributions


if __name__ == "__main__":
    # Install global exception hook for testing ok
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

    # Your normal app startup
    from egp_soft_based_on_mfl.main_window.frontend import Ui_MainWindow
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

