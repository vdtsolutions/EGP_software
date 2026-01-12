def calculate_length_percent(df_clock_holl_oddo1, start_reading, end_reading, l_per_1):
    """
    Calculate the length percentage (difference in ODDO1 readings)
    between two sensor indices, scaled using a linear factor.

    This function computes a centered region between the given
    start and end readings, determines a scaled window around the
    midpoint using the provided scaling factor (l_per_1), and
    returns the difference in ODDO1 values between those bounds.

    """
    counter_difference = end_reading - start_reading
    divid = int(counter_difference / 2)
    center = start_reading + divid
    factor = divid * l_per_1
    start = int(center - factor)
    end = int(center + factor)
    length_percent = df_clock_holl_oddo1[end] - df_clock_holl_oddo1[start]
    length = (df_clock_holl_oddo1[end_reading] - df_clock_holl_oddo1[start_reading])
    return length_percent, start, end , length
