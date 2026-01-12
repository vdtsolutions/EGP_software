import pandas as pd
from typing import Optional, Tuple

def calculate_defect_threshold(
    df_sorted: pd.DataFrame,
    result: pd.DataFrame,
    defect_box_thresh: float,
    verbose: bool = True
) -> Optional[Tuple[float, float]]:
    """
    Calculate an adaptive threshold for defect validation based on
    submatrix stats from candidate defect bounding boxes.

    Parameters
    ----------
    df_sorted : pd.DataFrame
        DataFrame of bounding boxes with columns:
            'start_row', 'end_row', 'start_col', 'end_col'
    result : pd.DataFrame
        Full 2D sensor data matrix from which submatrices are sliced.
    defect_box_thresh : float
        Interpolation factor between global min and max.
    verbose : bool
        If True, prints progress info and final threshold.

    Returns
    -------
    (threshold_value, max_of_all) : tuple(float, float)
        threshold_value = interpolated threshold (rounded to nearest int)
        max_of_all = global maximum value across all valid submatrices
        Returns None if no valid submatrices are found.
    """

    if verbose:
        print("Calculating threshold values for defect validation...")

    max_submatrix_list = []
    min_submatrix_list = []

    for _, row in df_sorted.iterrows():
        start_sensor = int(row['start_row'])
        end_sensor = int(row['end_row'])
        start_reading = int(row['start_col'])
        end_reading = int(row['end_col'])

        if start_sensor == end_sensor:
            continue

        try:
            submatrix = result.iloc[
                start_reading:end_reading + 1,
                start_sensor:end_sensor + 1
            ]
        except Exception as e:
            if verbose:
                print(f"Skipping box due to bad index ranges: {e}")
            continue

        submatrix = submatrix.apply(pd.to_numeric, errors='coerce')
        if submatrix.isnull().values.any():
            continue

        try:
            max_value = submatrix.max().max()
            flat_vals = submatrix.values.ravel()
            positive_vals = [x for x in flat_vals if x > 0]
            if not positive_vals:
                continue

            min_positive = min(positive_vals)
            max_submatrix_list.append(max_value)
            min_submatrix_list.append(min_positive)

        except Exception as e:
            if verbose:
                print(f"Skipping box due to numeric issue: {e}")
            continue

    if not max_submatrix_list or not min_submatrix_list:
        if verbose:
            print("No valid submatrices found. Threshold cannot be computed.")
        return None

    max_of_all = max(max_submatrix_list)
    min_of_all = min(min_submatrix_list)

    threshold_value = round(
        min_of_all + (max_of_all - min_of_all) * defect_box_thresh
    )

    if verbose:
        print(f"Base threshold calculated: {threshold_value}")
        # print(f"Global max across submatrices: {max_of_all}")

    return threshold_value, max_of_all
