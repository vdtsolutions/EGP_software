def dimension_class(pipe_thickness, length, width):
    length = length
    width = width
    geometrical_parameter = pipe_thickness

    dimension_classification = get_type_defect_1(geometrical_parameter, length, width)

    return dimension_classification






def get_type_defect_1(geometrical_parameter, length_defect, width_defect):
    L_ratio_W = length_defect / width_defect
    if width_defect > 3 * geometrical_parameter and length_defect > 3 * geometrical_parameter:
        type_of_defect = 'GENERAL'
        return type_of_defect
    elif (
            6 * geometrical_parameter >= width_defect >= 1 * geometrical_parameter and 6 * geometrical_parameter >= length_defect >= 1 * geometrical_parameter) and (
            0.5 < (L_ratio_W) < 2) and not (
            width_defect >= 3 * geometrical_parameter and length_defect >= 3 * geometrical_parameter):
        type_of_defect = 'PITTING'
        return type_of_defect
    elif (1 * geometrical_parameter <= width_defect < 3 * geometrical_parameter) and (
            L_ratio_W >= 2):
        type_of_defect = 'AXIAL GROOVING'
        return type_of_defect
    elif L_ratio_W <= 0.5 and 3 * geometrical_parameter > length_defect >= 1 * geometrical_parameter:
        type_of_defect = 'CIRCUMFERENTIAL GROOVING'
        return type_of_defect
    elif 0 < width_defect < 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
        type_of_defect = 'PINHOLE'
        return type_of_defect
    elif 0 < width_defect < 1 * geometrical_parameter and length_defect >= 1 * geometrical_parameter:
        type_of_defect = 'AXIAL SLOTTING'
        return type_of_defect
    elif width_defect >= 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
        type_of_defect = 'CIRCUMFERENTIAL SLOTTING'
        return type_of_defect