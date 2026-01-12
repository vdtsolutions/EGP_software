from PyQt5.QtWidgets import QMessageBox


def error_msg(Title, Description):
    """
    Method that will show a alert box for Error
    :param Title: Title of the Box
    :param Description: Description of the Box
    :return: void type
    """
    set_msg_body(Title, Description, QMessageBox.Critical, "Critical")


def info_msg(Title, Description):
    set_msg_body(Title, Description, QMessageBox.Information, "Information")


def warning_msg(Title, Description):
    set_msg_body(Title, Description, QMessageBox.Warning, "Warning")


def set_msg_body(Title, Description, icon, WindowTitle):
    try:
        msg.setIcon(icon)
        msg.setText(Title)
        msg.setInformativeText(Description)
        msg.setWindowTitle(WindowTitle)
        msg.exec_()
        app.exec_()
    except OSError as error:
        # logger.log_error(error or "Set_msg_body method failed with unknown Error")
        pass

def print_with_time(msg):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(msg, dt_string)