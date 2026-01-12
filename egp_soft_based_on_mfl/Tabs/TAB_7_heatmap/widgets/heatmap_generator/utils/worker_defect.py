
import math

from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.pipelines.depth_calculation_pipeline import \
    compute_depth
from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.pipelines.dimension_classification import \
    dimension_class
from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.pipelines.internal_or_external import \
    internal_or_external
from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.pipelines.interpolate_data import \
    process_csv_interpolate
from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.pipelines.length_calculation_pipeline import \
    calculate_length_percent
from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.pipelines.orientation_pipeline import \
    get_orientation
from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.pipelines.width_calculation_pipeline import \
    breadth, process_submatrix
# from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.utils.utils import replace_first_column, \
#     get_first_last_integer_column



# ==========================
# GLOBALS FOR MULTIPROCESSING
# ==========================
from egp_soft_based_on_mfl.Tabs.TAB_7_heatmap.widgets.heatmap_generator.utils.utils import replace_first_column

G_CONFIG = None
G_RESULT = None
G_DF_CLOCK = None
G_THRESHOLD = None
G_MAX_OF_ALL = None
G_DF3_RAW = None
G_MEAN1 = None
G_DF_NEW_PROX = None
G_ROLL_HR = None
G_PIPE_ID = None
G_RUNID = None
G_WALL_THICKNESS = None
G_PIPE_LEN = None
G_LENGTH_INDEX = None



def init_defect_worker(
    config,
    result, df_clock_holl_oddo1, threshold_value,
    max_of_all, df3_raw, mean1,
    df_new_proximity, Roll_hr,
    pipe_id, runid, wall_thickness,
    pipe_len_oddo1_chm, length_index,
):
    global G_CONFIG, G_RESULT, G_DF_CLOCK, G_THRESHOLD,G_MAX_OF_ALL, G_DF3_RAW, G_MEAN1, G_DF_NEW_PROX, G_ROLL_HR, G_PIPE_ID, G_RUNID, G_WALL_THICKNESS,G_PIPE_LEN, G_LENGTH_INDEX

    G_CONFIG = config
    G_RESULT = result
    G_DF_CLOCK = df_clock_holl_oddo1
    G_THRESHOLD = threshold_value
    G_MAX_OF_ALL = max_of_all
    G_DF3_RAW = df3_raw
    G_MEAN1 = mean1
    G_DF_NEW_PROX = df_new_proximity
    G_ROLL_HR = Roll_hr
    G_PIPE_ID = pipe_id
    G_RUNID = runid
    G_WALL_THICKNESS = wall_thickness
    G_PIPE_LEN = pipe_len_oddo1_chm
    G_LENGTH_INDEX = length_index



def compute_defect_data_multicore(row_tuple):
    """
    Worker that processes a single defect using globally shared objects.
    Only receives a small row_tuple: (start_sensor, end_sensor, start_reading, end_reading)
    """

    # global (G_CONFIG, G_RESULT, G_DF_CLOCK, G_THRESHOLD,
    #         G_MAX_OF_ALL, G_DF3_RAW, G_MEAN1,
    #         G_DF_NEW_PROX, G_ROLL_HR,
    #         G_PIPE_ID, G_RUNID, G_WALL_THICKNESS,
    #         G_PIPE_LEN, G_LENGTH_INDEX)
    global G_CONFIG, G_RESULT, G_DF_CLOCK, G_THRESHOLD,G_MAX_OF_ALL, G_DF3_RAW, G_MEAN1, G_DF_NEW_PROX, G_ROLL_HR, G_PIPE_ID, G_RUNID, G_WALL_THICKNESS,G_PIPE_LEN, G_LENGTH_INDEX


    try:
        (start_sensor, end_sensor, start_reading, end_reading) = row_tuple

        if start_sensor == end_sensor:
            return {"accepted": False}

        # Short-hands for speed + readability
        config           = G_CONFIG
        result           = G_RESULT
        df_clock_holl_oddo1 = G_DF_CLOCK
        threshold_value  = G_THRESHOLD
        max_of_all       = G_MAX_OF_ALL
        df3_raw          = G_DF3_RAW
        mean1            = G_MEAN1
        df_new_proximity = G_DF_NEW_PROX
        Roll_hr          = G_ROLL_HR
        pipe_id          = G_PIPE_ID
        runid            = G_RUNID
        wall_thickness   = G_WALL_THICKNESS
        pipe_len_oddo1_chm = G_PIPE_LEN
        length_index     = G_LENGTH_INDEX

        # ---------------------------------------------------------
        # SUBMATRIX
        submatrix = result.iloc[start_reading:end_reading + 1,
                                start_sensor:end_sensor + 1]

        max_value = submatrix.max().max()
        positive_vals = submatrix[submatrix > 0]
        min_positive = positive_vals.min().min()

        # ---------------------------------------------------------
        # LENGTH %
        length_percent, start, end, length = calculate_length_percent(
            df_clock_holl_oddo1=df_clock_holl_oddo1,
            start_reading=start_reading,
            end_reading=end_reading,
            l_per_1=config["l_per_1"]
        )

        # ---------------------------------------------------------
        # ADAPTIVE SIGMA
        sigma_multiplier, refinement_factor, classification = \
            config["get_adaptive_sigma_refinement"](length_percent)

        adjusted_threshold = threshold_value * sigma_multiplier
        threshold_pass = (adjusted_threshold <= max_value <= max_of_all)

        # Prep
        df_copy_submatrix = None
        width = None
        width_1_only = None
        orientation = None
        internal_external = None
        base_value = None

        if threshold_pass:
            depth_old = (max_value - min_positive) / min_positive * 100

            # DEPTH
            depth_val1, df_copy_submatrix = compute_depth(
                config,
                df_raw=df3_raw,
                start_reading=start_reading,
                end_reading=end_reading,
                start_sensor=start_sensor,
                end_sensor=end_sensor,
                pipe_thickness=config["pipe_thickness"],
            )

            # MAX INDEX
            max_column = submatrix.max().idxmax()
            max_index = submatrix.columns.get_loc(max_column)

            start_oddo1 = df_clock_holl_oddo1[start_reading]
            end_oddo1   = df_clock_holl_oddo1[end_reading] / 1000
            time_sec    = end_reading / 1500
            speed       = end_oddo1 / time_sec

            base_value = mean1[max_index]

            internal_external = internal_or_external(df_new_proximity, max_index)

            absolute_distance = df_clock_holl_oddo1[start_reading]
            upstream = df_clock_holl_oddo1[start_reading] - df_clock_holl_oddo1[0]

            # WIDTH (initial)
            width = breadth(config, start_sensor, end_sensor)
            dimension_classification = dimension_class(
                config["pipe_thickness"], length, width
            )

            # ---------------------------------------------------------
            # ORIENTATION
            center_offset = (end_sensor - start_sensor) / 2
            center = start_sensor + center_offset
            w_factor = center_offset * config["w_per_1"]

            start1_1 = int(center - w_factor) - 1
            end1_1   = int(center + w_factor) - 1

            orientation = get_orientation(
                Roll_hr, start, end, start1_1, end1_1
            )

            # PIPE GEOMETRY
            inner_diameter = config["outer_dia"] - 2 * config["pipe_thickness"]
            radius = inner_diameter / 2

            x1 = round(radius * math.radians(config["theta_ang1"]), 1)
            y1 = round(radius * math.radians(config["theta_ang2"]), 1)
            z1 = round(radius * math.radians(config["theta_ang3"]), 1)

            # MODIFY DF
            df_duplicate = replace_first_column(
                df_copy_submatrix, start_sensor, end_sensor
            )
            df_duplicate.columns = df_duplicate.columns.astype(str)

            modified_df = process_csv_interpolate(config, df_duplicate, x1, y1, z1)

            trimmed_matrix, width_1_only, width_0_yes, \
            new_start_sensor, new_end_sensor = process_submatrix(
                config, modified_df, start1_1, end1_1
            )

            # new_start_sensor, new_end_sensor = \
            #     get_first_last_integer_column(trimmed_matrix.columns)

            mapped_start_sensor = length_index - start_sensor
            mapped_end_sensor   = length_index - end_sensor
            if mapped_end_sensor < mapped_start_sensor:
                mapped_start_sensor, mapped_end_sensor = \
                    mapped_end_sensor, mapped_start_sensor

            width = breadth(config, mapped_start_sensor, mapped_end_sensor)

            # FINAL DEPTH
            try:
                depth_val = round(
                    (((length / width) * (max_value / base_value)) * 100)
                    / config["pipe_thickness"]
                )
            except:
                depth_val = 0

            final_accept = (
                threshold_pass and depth_val > 1 and width > 1 and length > 1
            )

        else:
            final_accept = False
            absolute_distance = upstream = None
            dimension_classification = None
            orientation = None
            internal_external = None
            depth_val1 = depth_old = None
            speed = None
            start_oddo1 = None
            end_oddo1 = None
            modified_df = None

        print("ACCEPT? =", final_accept,
              "| max_value =", max_value,
              "| adjusted_threshold =", adjusted_threshold,
              "| length =", length,
              "| width =", width)
        # ---------------------------------------------------------
        return {
            "accepted": final_accept,
            "classification": classification,
            "start_sensor": start_sensor,
            "end_sensor": end_sensor,
            "start_reading": start_reading,
            "end_reading": end_reading,
            "absolute_distance": absolute_distance,
            "upstream": upstream,
            "length": length,
            "length_percent": length_percent,
            "breadth": width,
            "width_new2": None if width_1_only is None else round(width_1_only, 0),
            "orientation": orientation,
            "defect_type": internal_external,
            "dimension_classification": dimension_classification,
            "depth": depth_val1,
            "depth_old": depth_old,
            "start_oddo1": start_oddo1,
            "end_oddo1": end_oddo1,
            "speed": speed,
            "Min_Val": min_positive,
            "Max_Val": max_value,
            "pipe_id": pipe_id,
            "runid": runid,
            "wall_thickness": wall_thickness,
            "pipe_length": pipe_len_oddo1_chm,
            "modified_df": modified_df,
        }

    except Exception as e:
        return {"accepted": False, "error": str(e)}



def apply_defect_result(
    self,
    res,
    classification_stats,
    defect_counter,
    submatrices_dict,
    finial_defect_list,
    figx112
):
    if "classification" in res and res["classification"]:
        classification_stats[res["classification"]]["total_processed"] += 1

    if not res["accepted"]:
        return defect_counter

    classification = res["classification"]
    classification_stats[classification]["count"] += 1

    start_sensor = res["start_sensor"]
    end_sensor = res["end_sensor"]
    start_reading = res["start_reading"]
    end_reading = res["end_reading"]
    modified_df = res["modified_df"]

    # SAVE MATRIX
    submatrices_dict[
        (defect_counter, start_sensor, end_sensor)
    ] = modified_df

    # APPEND DEFECT
    finial_defect_list.append({
        "pipe_id": res["pipe_id"],
        "runid": res["runid"],
        "defect_id": defect_counter,
        "start_reading": start_reading,
        "end_reading": end_reading,
        "start_sensor": start_sensor,
        "end_sensor": end_sensor,
        "absolute_distance": res["absolute_distance"],
        "upstream": res["upstream"],
        "length": res["length"],
        "length_percent": res["length_percent"],
        "breadth": res["breadth"],
        "width_new2": res["width_new2"],
        "orientation": res["orientation"],
        "defect_type": res["defect_type"],
        "dimension_classification": res["dimension_classification"],
        "depth": res["depth"],
        "depth_old": res["depth_old"],
        "start_oddo1": res["start_oddo1"],
        "end_oddo1": res["end_oddo1"],
        "speed": res["speed"],
        "Min_Val": res["Min_Val"],
        "Max_Val": res["Max_Val"],
        "wall_thickness": res["wall_thickness"],
        "pipe_length": res["pipe_length"]
    })

    # COLOR EXACT SAME LOGIC
    if classification == "Very Small (1-10%)":
        color = 'purple'
    elif classification == "Small (10-20%)":
        color = 'red'
    elif classification == "Medium (20-30%)":
        color = 'orange'
    elif classification == "Large (30-40%)":
        color = 'yellow'
    elif classification == "Very Large (40%+)":
        color = 'blue'
    else:
        color = 'gray'

    figx112.add_shape(
        type='rect',
        x0=start_reading - 0.5,
        x1=end_reading + 0.5,
        y0=start_sensor - 0.5,
        y1=end_sensor + 0.5,
        line=dict(color=color, width=2),
        fillcolor=f'rgba(255, 0, 0, 0.2)'
    )

    figx112.add_annotation(
        x=(start_reading + end_reading) / 2,
        y=start_sensor - 1,
        text=f"{defect_counter}({classification.split()[0]})",
        showarrow=False,
        font=dict(color=color, size=10),
        bgcolor="white",
        bordercolor="black",
        borderwidth=1
    )

    return defect_counter + 1