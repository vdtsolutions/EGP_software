def get_orientation(Roll_hr, start, end, start1_1, end1_1):
    """
    Calculate the orientation value from Roll_hr dataframe
    using the midpoint of provided start/end indices.

    Args:
        Roll_hr (pd.DataFrame): The dataframe containing roll/orientation data.
        start (int): Starting row index.
        end (int): Ending row index.
        start1_1 (int): Starting column index.
        end1_1 (int): Ending column index.

    Returns:
        float: The orientation value from the computed midpoint.
    """
    avg_counter = round((start + end) / 2)
    avg_sensor = round((start1_1 + end1_1) / 2)
    orientation = Roll_hr.iloc[avg_counter, avg_sensor]
    return orientation
