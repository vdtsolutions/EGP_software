from statistics import mean

# def internal_or_external(df_new_proximity, x):
#     sensor_number = x + 1
#     if sensor_number % 4 == 0:
#         flapper_no = int(sensor_number / 4)
#     else:
#         flapper_no = int(sensor_number / 4) + 1
#     proximity_no = flapper_no % 4
#     if proximity_no == 0:
#         proximity_no = 4
#     proximity_index = 'F' + str(flapper_no) + 'P' + str(proximity_no)
#     print("Proximity_index", proximity_index)
#     maximum_depth_proximity_sensor = df_new_proximity[proximity_index]
#
#     c = maximum_depth_proximity_sensor.tolist()
#     minimum_value_proximity = min(c)
#     mean_value_proximtiy = mean(c)
#
#     print("mean_value_proximtiy", mean_value_proximtiy)
#     print("minimum value of proximity", minimum_value_proximity)
#
#     difference_mean = mean_value_proximtiy - minimum_value_proximity
#
#     print("difference_minimum2", difference_mean)
#     if difference_mean > 18000:
#         type = "Internal"
#         return type
#     else:
#         type = "External"
#         return type


def internal_or_external(df_new_proximity, x):
    # sensor number
    sensor_number = x + 1
    flapper_no = (sensor_number - 1) // 4 + 1
    proximity_no = ((flapper_no - 1) % 4) + 1

    # proximity sensor index
    proximity_index = f'F{flapper_no}P{proximity_no}'

    # get sensor values
    values = df_new_proximity[proximity_index].tolist()

    mean_val = mean(values)
    min_val = min(values)

    diff = mean_val - min_val

    # DYNAMIC THRESHOLD (7% drop indicates internal)
    dynamic_threshold = mean_val * 0.07

    if diff > dynamic_threshold:
        return "Internal"
    else:
        return "External"