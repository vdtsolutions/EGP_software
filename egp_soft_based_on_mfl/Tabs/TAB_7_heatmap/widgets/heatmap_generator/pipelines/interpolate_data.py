import numpy as np
import pandas as pd
from scipy.interpolate import interp1d




def process_csv_interpolate(config, df_dupe, x1, y1, z1):
    """
    Like the original process_csv, but uses interpolation (linear or cubic)
    instead of duplication for the new columns. Suffixes and column names are
    generated exactly as in the original code, with robust end-case handling.
    """
    new_data = {}
    next_col = None

    # Use your previously computed distances
    base = round(x1 / config["div_factor"])
    c = round(y1 / config["div_factor"])
    dee = round(z1 / config["div_factor"])

    c1 = c // 2
    c2 = c - c1
    dee1 = dee // 2
    dee2 = dee - dee1

    def generate_suffixes(n):
        return [chr(ord('a') + i) for i in range(int(n))]

    base_suffixes = generate_suffixes(int(base))
    c1_suffixes = generate_suffixes(int(c1))
    c2_suffixes = generate_suffixes(int(c2))
    dee1_suffixes = generate_suffixes(int(dee1))
    dee2_suffixes = generate_suffixes(int(dee2))

    for colu in df_dupe.columns:
        col_int = int(colu)
        next_col = str(col_int + 1)

        if next_col in df_dupe.columns:
            col_vals = df_dupe[colu].values
            next_col_vals = df_dupe[next_col].values

            def interpolate_between(a, b, n, kind='cubic'):
                # For short arrays, always use linear
                if n == 0:
                    return np.empty((0, len(a)))
                x = np.array([0, 1])
                arr = np.vstack([a, b]).T
                interpolated = []
                for row in arr:
                    # If both points are the same, just duplicate
                    if np.allclose(row[0], row[1]):
                        interpolated.append(np.full(n, row[0]))
                        continue
                    # Use cubic only if possible, otherwise linear
                    if kind == 'cubic' and n >= 3:
                        try:
                            f = interp1d(x, row, kind='cubic', fill_value="extrapolate")
                        except Exception:
                            f = interp1d(x, row, kind='linear',
                                         fill_value="extrapolate")
                    else:
                        f = interp1d(x, row, kind='linear', fill_value="extrapolate")
                    xs = np.linspace(0, 1, n + 2)[1:-1] if n > 0 else []
                    interpolated.append(f(xs) if len(xs) > 0 else [])
                return np.array(interpolated).T if n > 0 else np.empty((0, len(a)))

            # Special Case 1: Between flappers (multiples of 4, not 16)
            if col_int % 4 == 0 and col_int % 16 != 0:
                c1_interp = interpolate_between(col_vals, next_col_vals,
                                                len(c1_suffixes),
                                                kind='cubic')
                for idx, suffix in enumerate(c1_suffixes):
                    new_data[f"{col_int}{suffix}_extra"] = c1_interp[idx] if \
                        c1_interp.shape[
                            0] > 0 else col_vals
                c2_interp = interpolate_between(next_col_vals, col_vals,
                                                len(c2_suffixes),
                                                kind='cubic')
                for idx, suffix in enumerate(c2_suffixes):
                    new_data[f"{int(next_col)}{suffix}_extra"] = c2_interp[idx] if \
                        c2_interp.shape[0] > 0 else next_col_vals

            # Special Case 2: Between arms (multiples of 16)
            elif col_int % 16 == 0:
                dee1_interp = interpolate_between(col_vals, next_col_vals,
                                                  len(dee1_suffixes),
                                                  kind='cubic')
                for idx, suffix in enumerate(dee1_suffixes):
                    new_data[f"{col_int}{suffix}_extra2"] = dee1_interp[idx] if \
                        dee1_interp.shape[0] > 0 else col_vals
                dee2_interp = interpolate_between(next_col_vals, col_vals,
                                                  len(dee2_suffixes),
                                                  kind='cubic')
                for idx, suffix in enumerate(dee2_suffixes):
                    new_data[f"{int(next_col)}{suffix}_extra2"] = dee2_interp[idx] if \
                        dee2_interp.shape[0] > 0 else next_col_vals

            # Base case: Normal sensor spacing
            else:
                base_interp = interpolate_between(col_vals, next_col_vals,
                                                  len(base_suffixes),
                                                  kind='cubic')
                for idx, suffix in enumerate(base_suffixes):
                    new_data[f"{col_int}{suffix}"] = base_interp[idx] if \
                        base_interp.shape[
                            0] > 0 else col_vals

    new_df_duplicate = pd.DataFrame(new_data, index=df_dupe.index)
    return new_df_duplicate