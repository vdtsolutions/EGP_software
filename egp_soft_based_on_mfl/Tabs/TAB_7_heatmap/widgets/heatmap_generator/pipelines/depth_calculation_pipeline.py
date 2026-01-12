import numpy as np
from scipy.ndimage import gaussian_filter




def compute_depth(
    config,
    df_raw,
    start_reading,
    end_reading,
    start_sensor,
    end_sensor,
    pipe_thickness
):
    """
    Compute the defect depth using an energy-based method on a target
    submatrix and its reference region.

    Parameters
    ----------
    df_raw : pandas.DataFrame
        The full sensor data matrix.
    start_reading : int
        Start row index of the defect region.
    end_reading : int
        End row index of the defect region.
    start_sensor : int
        Start column index of the defect region.
    end_sensor : int
        End column index of the defect region.
    pipe_thickness : float
        Pipe thickness value used for energy-depth calculation.
    calculate_energy_based_depth_func : callable
        Function used to calculate depth, e.g., `calculate_energy_based_depth(submatrix, ref_matrix, pipe_thickness)`.

    Returns
    -------
    float
        Calculated depth percentage (0–100), clamped to 100.
    """

    # Extract defect submatrix
    df_copy_submatrix = df_raw.iloc[start_reading:end_reading + 1,
                                    start_sensor:end_sensor + 1]

    # Define reference region before the defect region
    ref_start = max(0, start_reading - (end_reading - start_reading))
    ref_end = start_reading - 1
    reference_matrix = df_raw.iloc[ref_start:ref_end + 1,
                                   start_sensor:end_sensor + 1]

    # Compute energy-based depth
    depth_val = calculate_energy_based_depth(
        df_copy_submatrix,
        reference_matrix,
        config["pipe_thickness"],
        config["scaling_exponent"],
        config["calibration_factor"],
        config["min_energy_threshold"]
    )

    # Clamp to 100%
    depth_val = min(depth_val, 100)
    return depth_val, df_copy_submatrix


def calculate_energy_based_depth(defect_matrix, reference_matrix, pipe_thickness,
                                 scaling_exponent, calibration_factor,
                                 min_energy_threshold, debug=False):
    """
    Improved and robust defect depth estimation based on energy ratio method.
    """
    try:
        if defect_matrix.empty or reference_matrix.empty:
            return 0.0

        # Convert to numpy arrays
        defect_arr = defect_matrix.to_numpy().astype(float)
        ref_arr = reference_matrix.to_numpy().astype(float)

        # Apply Gaussian filter to smooth data
        defect_arr = gaussian_filter(defect_arr, sigma=1.0)
        ref_arr = gaussian_filter(ref_arr, sigma=1.0)

        # Energy calculation
        energy_defect = np.sum(np.square(defect_arr))
        energy_ref = np.sum(np.square(ref_arr))

        if debug:
            print(f"Energy (defect): {energy_defect:.4f}, Energy (ref): {energy_ref:.4f}")

        # Avoid division by zero or too small reference energy
        if energy_ref < min_energy_threshold:
            return 0.0

        # Compute energy ratio
        ratio = energy_defect / energy_ref

        if debug:
            print(f"Energy ratio: {ratio:.4f}")

        # Depth estimation formula
        print(f" values: pipe_thickness: {pipe_thickness} : scaling : {scaling_exponent}")
        depth = ((ratio ** scaling_exponent) * 100 / pipe_thickness) * calibration_factor

        # Clamp between 0 and 100
        depth = max(min(depth, 100), 0)

        return round(depth, 2)

    except Exception as e:
        print("Error in depth calculation:", e)
        return 0.0

