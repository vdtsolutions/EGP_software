##################Menubar ####################################################
menubar = """
    QMenuBar {
        background-color: #000000;
        color: white;
    }

    QMenuBar::item {
        background: transparent;
        color: white;
        padding: 4px 10px;
    }

    QMenuBar::item:selected {
        background: #333333;
        border-radius: 3px;
    }

    QMenuBar::item:pressed {
        background: #555555;
    }

    QMenu {
        background-color: #1a1a1a;
        color: white;
    }

    QMenu::item:selected {
        background-color: #333333;
    }
"""

#############################################################################
right_tabWidget = """
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 lightgray, stop:1 rgba(255, 99,71, 0.6));
                """
#############################################################################

tab_update = """
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 white, stop:1 rgba(255, 99,71, 0.6));
            """

####################Left side bar ##########################################
list_grid_style = """
                         QListWidget::item{
                          padding: 15px 10px;
                          font-size:14px;
                          border-bottom:0.5px solid rgba(255, 99,71, 0.6);
                          border-left:0.5px solid rgba(255, 99,71, 0.6);
                          border-right:0.5px rgba(255, 99,71, 0.6);
                        }
                         QListWidget::item:selected {
                            background-color: rgba(255, 99,71, 0.6));
                            color:rgb(21, 87, 36);
                            outline: 0;
                            border-radius: 4px;
                        }
                        QListView {
                            outline: 0;
                            color:#343a40;
                            font-size:14px;
                        }
                        """

###################load button ############################################
btn_type_primary = """
                     width: 100%;
                     background-color: rgba(255, 99,71, 0.6);
                     color: white;
                     padding: 10px 10px;
                     font-size:14px;
                     margin: 2px 0;
                     border: none;
                     border-radius: 4px;
                    """

################## bck button #############################################
btn_back = """
QPushButton {
    background-color: #000000;  /* black background */
    color: white;               /* white text */
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #333333;  /* dark gray hover */
}
QPushButton:pressed {
    background-color: #111111;  /* darker black when pressed */
}
QPushButton:disabled {
    background-color: #555555;
    color: #bbbbbb;
}
"""

#############buttons in Show data ##########################################
btn_type_secondary = """
                     width: 100%;
                     # background-color: #808000;
                     background-color: black;
                     color: white;
                     padding: 10px 10px;
                     font-size:14px;
                     margin: 2px 0;
                     border: none;
                     border-radius: 4px;
                  """

btn_type_danger = """
                     width: 100%;
                     background-color: #dc3545;
                     color: white;
                     padding: 10px 10px;
                     font-size:14px;
                     margin: 2px 0;
                     border: none;
                     border-radius: 4px;
                  """

form_input_box = """
                    QLineEdit{
                              font-size=18px;
                              padding: 10px 20px;
                              margin: 8px 0;border: 1px solid #ccc;border-radius: 4px;
                              }
                """
####################Attach button ##############################################

attach_btn = """
                                     background-color: rgba(255, 99,71, 0.6);
                                     color:white; border-radius:5px; margin:0px;
                                     padding: 10px 26px;
                                     font-size:11px;
                                     margin: 10px 5px;
                                     border: 1px solid #C0C0C0;
                                     border-radius: 4px;
                                     text-align:center

            """

###############################Update ###########################################
update_btn = """
                                    background-color: rgba(255, 99,71, 0.6);
                                       color: white;
                                       padding: 10px 12px;
                                       font-size:14px;
                                       margin: 8px 0px 0px 0px;
                                       border: none;
                                       border-radius: 18px;
            """
