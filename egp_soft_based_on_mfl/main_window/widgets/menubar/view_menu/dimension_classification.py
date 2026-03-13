from PyQt5.QtWidgets import QInputDialog, QMessageBox


def Typeofdefect(self):
    try:
        runid = self.runid
        try:
            self.thickness_pipe, okPressed = QInputDialog.getText(self, "Get integer", "thickness_pipe")
            if okPressed:
                pass
                thickness_pipe = float(self.thickness_pipe)
                if thickness_pipe < 10.0:
                    geometrical_parameter = 10
                else:
                    geometrical_parameter = thickness_pipe
                get_type_defect(geometrical_parameter, runid)

        except:
            # logger.log_error("thickness_pipe is not found")
            pass
    except:
        QMessageBox.about(self, 'Info', 'Please select the runid')


def get_type_defect(self, geometrical_parameter, runid):
    print(geometrical_parameter, runid)
    with self.config.connection.cursor() as cursor:
        try:
            Fetch_defect_detail = "select Length, Width, id from finaldefect where runid='%s'"
            cursor.execute(Fetch_defect_detail, (int(runid)))
            allSQLRows = cursor.fetchall()
            print("dhhdhf", allSQLRows)
            for i in allSQLRows:
                length_defect = i[0]
                width_defect = i[1]
                defect_id = i[2]
                L_ratio_W = length_defect / width_defect
                if width_defect >= 3 * geometrical_parameter and length_defect >= 3 * geometrical_parameter:
                    type_of_defect = 'GENERAL'
                elif (
                        6 * geometrical_parameter > width_defect >= 1 * geometrical_parameter and 6 * geometrical_parameter > length_defect >= 1 * geometrical_parameter) and (
                        0.5 < (L_ratio_W) < 2) and not (
                        width_defect >= 3 * geometrical_parameter and length_defect >= 3 * geometrical_parameter):
                    type_of_defect = 'PITTING'
                elif (1 * geometrical_parameter <= width_defect < 3 * geometrical_parameter) and (L_ratio_W >= 2):
                    type_of_defect = 'AXIAL GROOVING'
                elif L_ratio_W <= 0.5 and 3 * geometrical_parameter > length_defect >= 1 * geometrical_parameter:
                    type_of_defect = 'CIRCUMFERENTIAL GROOVING'
                elif 0 < width_defect < 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
                    type_of_defect = 'PINHOLE'
                elif 0 < width_defect < 1 * geometrical_parameter and length_defect >= 1 * geometrical_parameter:
                    type_of_defect = 'AXIAL SLOTTING'
                elif width_defect >= 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
                    type_of_defect = 'CIRCUMFERENTIAL SLOTTING'
                dimension_classification(self, type_of_defect, runid, defect_id)
        except:
            # logger.log_error("type of defect is not permissiable value")
            pass


def dimension_classification(self, type_of_defect, runid, defect_id):
    print(type_of_defect, runid)
    query = f'UPDATE finaldefect SET  Dimensions_classification="{type_of_defect}" WHERE runid="{runid}" and id={defect_id}'
    with self.config.connection.cursor() as cursor:
        cursor.execute(query)
        self.config.connection.commit()