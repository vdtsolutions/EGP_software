def filter_defects_by_adaptive_threshold(
    submatrix,
    start_sensor,
    end_sensor,
    mean1,
    standard_deviation,
    sigma_multiplier,
    classification_stats,
    classification
):
    """
    Filter defects using adaptive sigma-based thresholds.

    For each sensor column in the defect region:
    - Calculates adaptive threshold = mean + (sigma_multiplier * std)
    - Counts how many columns exceed that threshold
    - Rejects the defect if fewer than 30% of columns pass
    - Updates classification statistics (total processed count)

    Parameters
    ----------
    submatrix : pandas.DataFrame
        Data slice corresponding to the defect region.
    start_sensor : int
        Starting column index for the defect region.
    end_sensor : int
        Ending column index for the defect region.
    mean1 : list or np.ndarray
        Column-wise mean values for adaptive thresholding.
    standard_deviation : list or np.ndarray
        Column-wise standard deviation values for adaptive thresholding.
    sigma_multiplier : float
        Multiplier applied to the standard deviation.
    threshold_value : float
        Base global threshold.
    classification_stats : dict
        Dictionary tracking processed defect counts per class.
    classification : str
        The current defect's classification label (e.g., "Medium (20-30%)").

    Returns
    -------
    tuple
        (adjusted_threshold, valid_columns)
        adjusted_threshold : float
            Scaled threshold used for this validation.
        valid_columns : int
            Number of columns exceeding adaptive threshold.
    """


    valid_columns = 0

    for col_idx in range(start_sensor, end_sensor + 1):
        adaptive_sigma = mean1[col_idx] + (sigma_multiplier * standard_deviation[col_idx])
        if submatrix.iloc[:, col_idx - start_sensor].max() > adaptive_sigma:
            valid_columns += 1
        if valid_columns / (end_sensor - start_sensor + 1) < 0.3:
            print(f"✗ Defect rejected: Only {valid_columns} columns passed adaptive threshold")
            continue

    classification_stats[classification]["total_processed"] += 1
    return  valid_columns
