############################# Menubar ########################################
menubar = """
    QMenuBar {
        background-color: #ffffff;
        color: #333333;
        font-weight: bold;
    }
    QMenuBar::item {
        background: transparent;
        padding: 6px 12px;
    }
    QMenuBar::item:selected {
        background: #f0f0f0;
        border-radius: 4px;
    }
    QMenu {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #cccccc;
    }
    QMenu::item:selected {
        background-color: #e6f0fa;
        color: #005a9e;
    }
"""

##############################################################################
# right_tabWidget = """
#     QTabWidget::pane {
#         background: #f9f9f9;
#         border: 1px solid #cccccc;
#         border-radius: 6px;
#     }
#     QTabBar::tab {
#         background: #eaeaea;
#         padding: 8px 14px;
#         border-radius: 4px;
#         margin: 2px;
#     }
#     QTabBar::tab:selected {
#         background: #0078d7;
#         color: white;
#     }
# """

tab_bar_style = """
QTabWidget::pane {
    border: 1px solid #d0d0d0;
    background: #ffffff;
    border-radius: 6px;
}

QTabBar::tab {
    background: #f1f1f1;
    color: #333333;
    padding: 8px 18px;
    margin: 2px;
    border: 1px solid #cccccc;
    border-radius: 6px;
    font-size: 10.5px;
    min-width: 195px;   
    font-weight: bold;

}

QTabBar::tab:hover {
    background: #e6e6e6;
    border: 1px solid #bbbbbb;
}

QTabBar::tab:selected {
    background: #0078d7;
    color: white;
    border: 1px solid #005a9e;
    font-weight: bold;
}

QTabBar::tab:!selected {
    margin-top: 4px; /* makes selected tab look raised */
}
"""


##############################################################################
tab_update = """
    background-color: #ffffff;
"""

#################### Left sidebar ###########################################
# list_grid_style = """
#     QListWidget::item {
#         padding: 12px 10px;
#         font-size: 14px;
#         border-bottom: 1px solid #e0e0e0;
#     }
#     QListWidget::item:selected {
#         background-color: #e6f0fa;
#         color: #005a9e;
#         border-radius: 4px;
#     }
#     QListView {
#         outline: 0;
#         font-size: 14px;
#         color: #333333;
#     }
# """


list_grid_style = """
QListWidget::item {
    padding: 12px 10px;
    font-size: 14px;
    border-bottom: 1px solid #e0e0e0;
    
    color: #333333;
}

QListWidget::item:selected {
    background-color: #0078d7;   /* same blue as Load Data */
    color: white;                /* white text */
    border-radius: 6px;
    font-weight: bold;           /* emphasised text */
    margin: 2px;                 /* spacing around selection */
}

QListWidget {
    outline: 0;
    font-size: 14px;
    color: #333333;
    border: none;
}
"""


#################### Primary Button ##########################################
btn_type_primary = """
QPushButton {
    background-color: #0078d7;
    color: white;
    padding: 8px 14px;
    font-size: 14px;
    border: none;
    border-radius: 6px;
}
QPushButton:hover {
    background-color: #005a9e;
}
QPushButton:pressed {
    background-color: #004578;
}
"""

#################### Back Button ############################################
btn_back = """
QPushButton {
    background-color: #000000;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #333333;
}
QPushButton:pressed {
    background-color: #111111;
}
QPushButton:disabled {
    background-color: #555555;
    color: #bbbbbb;
}
"""

#################### Secondary Button #######################################
btn_type_secondary = """
QPushButton {
    background-color: #6c757d;
    color: white;
    padding: 8px 14px;
    font-size: 14px;
    border: none;
    border-radius: 6px;
}
QPushButton:hover {
    background-color: #5a6268;
}
QPushButton:pressed {
    background-color: #444b50;
}
"""

#################### Danger Button ##########################################
btn_type_danger = """
QPushButton {
    background-color: #dc3545;
    color: white;
    padding: 8px 14px;
    font-size: 14px;
    border: none;
    border-radius: 6px;
}
QPushButton:hover {
    background-color: #b52a37;
}
QPushButton:pressed {
    background-color: #8e1f2b;
}
"""

# #################### Form Input Box #########################################
# form_input_box = """
# QLineEdit {
#     font-size: 14px;
#     padding: 8px 10px;
#     border: 1px solid #ccc;
#     border-radius: 6px;
#     margin: 6px 0;
# }
# QLineEdit:focus {
#     border: 1px solid #0078d7;
#     background-color: #f0f8ff;
# }
# """
#
# #################### Attach Button ##########################################
# attach_btn = """
# QPushButton {
#     background-color: #17a2b8;
#     color: white;
#     border-radius: 6px;
#     padding: 8px 16px;
#     font-size: 13px;
# }
# QPushButton:hover {
#     background-color: #138496;
# }
# QPushButton:pressed {
#     background-color: #0f6674;
# }
# """
#
# #################### Update Button ##########################################
# update_btn = """
# QPushButton {
#     background-color: #28a745;
#     color: white;
#     padding: 10px 16px;
#     font-size: 14px;
#     border: none;
#     border-radius: 18px;
# }
# QPushButton:hover {
#     background-color: #218838;
# }
# QPushButton:pressed {
#     background-color: #1e7e34;
# }
# """


# form_input_box = """
#     QWidget {
#         font-family: 'Segoe UI';
#         font-size: 14px;
#     }
#     QLineEdit {
#         padding: 6px;
#         border: 1px solid #ccc;
#         border-radius: 4px;
#         background-color: #fafafa;
#     }
#     QLineEdit:focus {
#         border: 1px solid #0078d7;
#         background-color: #ffffff;
#     }
#     QLabel {
#         margin-bottom: 4px;
#         font-weight: bold;
#     }
# """

# attach_btn = """
#     QPushButton {
#         background-color: #f78f8f;
#         border-radius: 10px;
#         padding: 10px;
#         font-size: 14px;
#         font-weight: bold;
#         color: white;
#     }
#     QPushButton:hover {
#         background-color: #f56c6c;
#     }
# """
#
# update_btn = """
#     QPushButton {
#         background-color: #f78f8f;
#         border-radius: 10px;
#         padding: 10px;
#         font-size: 14px;
#         font-weight: bold;
#         color: white;
#     }
#     QPushButton:hover {
#         background-color: #f56c6c;
#     }
# """



shared_button_style = """
QPushButton {
    background-color: #f1f1f1;
    border-radius: 10px;
    padding: 10px;
    font-size: 14px;
    font-weight: bold;
    color: #333333;
    border: 1px solid #cccccc;
}

QPushButton:hover {
    background-color: #e6e6e6;
    color: #000000;
    border: 1px solid #aaaaaa;
}

QPushButton:pressed, QPushButton:checked {
    background-color: #0078d7;
    color: white;
    border: 1px solid #005a9e;
}
"""
# form_input_box = """
# QWidget {
#     font-family: 'Segoe UI';
#     font-size: 14px;
# }
#
# QLineEdit {
#     padding: 8px 10px;
#     border: 1px solid #cccccc;
#     border-radius: 6px;
#     background-color: #f9f9f9;
#     color: #333333;
# }
#
# QLineEdit:focus {
#     border: 1px solid #0078d7;
#     background-color: #e6f0fa;  /* light bluish focus */
#     color: #000000;
# }
#
# QLabel {
#     margin-bottom: 4px;
#     font-weight: bold;
#     color: #333333;
# }
# """


# form_input_box = """
# QWidget {
#     background-color: #ffffff;
#     border-radius: 12px;
#     padding: 20px;
#     border: 1px solid #ccc;
# }
#
# /* Input fields */
# QLineEdit {
#     padding: 10px;
#     border: 1px solid black;
#     border-radius: 6px;
#     background-color: #ffffff;
# }
# QLineEdit:focus {
#     border: 2px solid black;
#     background-color: #f9f9f9;
#     box-shadow: 0 0 6px rgba(0, 0, 0, 0.2);
# }
#
# /* Buttons */
# QPushButton {
#     border: 1px solid black;
#     border-radius: 6px;
#     padding: 10px 16px;
#     font-weight: bold;
#     background-color: #f5f5f5;
# }
# QPushButton:hover {
#     background-color: #e0e0e0;
# }
# QPushButton:pressed {
#     background-color: #d0d0d0;
# }
#
# /* Primary button (Update) */
# QPushButton#update_data {
#     background-color: #0078d7;
#     color: white;
#     border: 1px solid black;
# }
# QPushButton#update_data:hover {
#     background-color: #005a9e;
# }
# QPushButton#update_data:pressed {
#     background-color: #004377;
# }
# """


form_input_box = """
/* Input fields */
QLineEdit {
    padding: 10px;
    border: 1px solid black;
    border-radius: 6px;
    background-color: #ffffff;
}
QLineEdit:focus {
    border: 2px solid black;
    background-color: #f9f9f9;
    box-shadow: 0 0 6px rgba(0, 0, 0, 0.2);
}

/* Buttons */
QPushButton {
    border: 1px solid black;
    border-radius: 6px;
    padding: 10px 16px;
    font-weight: bold;
    background-color: #f5f5f5;
}
QPushButton:hover {
    background-color: #e0e0e0;
}
QPushButton:pressed {
    background-color: #d0d0d0;
}

/* Primary button (Update) */
QPushButton#update_data {
    background-color: #0078d7;
    color: white;
    border: 1px solid black;
}
QPushButton#update_data:hover {
    background-color: #005a9e;
}
QPushButton#update_data:pressed {
    background-color: #004377;
}
"""

###################################


