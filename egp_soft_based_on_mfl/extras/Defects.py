# # import pandas as pd
# # import plotly.graph_objects as go
# # import os
# #
# # def plot_metal_loss(df, feature_type=None, dimension_class=None, return_fig=False):
# #     df.columns = df.columns.str.strip()
# #     df['Feature Identification'] = df['Feature Identification'].astype(str).str.strip()
# #     df['Dimension Classification'] = df['Dimension Classification'].astype(str).str.strip()
# #
# #     # Filter Metal Loss rows
# #     df = df[df['Feature Type'].str.contains('Metal Loss', case=False, na=False)].copy()
# #
# #     # Filter based on Feature Identification
# #     if feature_type == "Corrosion":
# #         df = df[df['Feature Identification'].str.contains('Corrosion', case=False, na=False)]
# #     elif feature_type == "MFG":
# #         df = df[df['Feature Identification'].str.contains('MFG', case=False, na=False)]
# #     # If feature_type is None or 'Both', we keep all metal loss records
# #
# #     # Filter based on Dimensional Classification
# #     if dimension_class and dimension_class != "ALL":
# #         df = df[df['Dimension Classification'].str.contains(dimension_class, case=False, na=False)]
# #
# #     if df.empty:
# #         print("No matching defects found in the file.")
# #         return None
# #
# #     # Group by bins for the graph
# #     bin_size = 500
# #     max_distance = df['Abs. Distance (m)'].max()
# #     bins = list(range(0, int(max_distance) + bin_size, bin_size))
# #     df.loc[:, 'Distance Bin'] = pd.cut(df['Abs. Distance (m)'], bins=bins, right=True)
# #
# #     bin_counts = df.groupby('Distance Bin', observed=False).size().reset_index(name='Metal Loss Count')
# #     bin_counts['Bin Label'] = bin_counts['Distance Bin'].apply(lambda x: int(x.right))
# #
# #
# #     # Set dynamic titles and labels based on selected feature and dimensional classification
# #     if feature_type == "Corrosion":
# #         # title = "Distribution of Corrosion Metal Loss Defects Throughout the Pipeline Length"
# #         yaxis_title = "Number of Corrosion Metal Loss Defects"
# #     elif feature_type == "MFG":
# #         # title = "Distribution of MFG Metal Loss Defects Throughout the Pipeline Length"
# #         yaxis_title = "Number of MFG Metal Loss Defects"
# #     else:
# #         # title = "Distribution of Metal Loss Defects Throughout the Pipeline Length"
# #         yaxis_title = "Number of Metal Loss Defects"
# #
# #     # Update title and labels based on Dimensional Classification
# #     if dimension_class:
# #         if dimension_class == "Pitting":
# #             # title += " - Pitting Classification"
# #             yaxis_title = "Number of Pitting Metal Loss Defects"
# #         elif dimension_class == "Axial Grooving":
# #             # title += " - Axial Grooving Classification"
# #             yaxis_title = "Number of Axial Grooving Metal Loss Defects"
# #         elif dimension_class == "Axial Slotting":
# #             # title += " - Axial Slotting Classification"
# #             yaxis_title = "Number of Axial Slotting Metal Loss Defects"
# #         elif dimension_class == "Circumferential Grooving":
# #             # title += " - Circumferential Grooving Classification"
# #             yaxis_title = "Number of Circumferential Grooving Metal Loss Defects"
# #         elif dimension_class == "Circumferential Slotting":
# #             # title += " - Circumferential Slotting Classification"
# #             yaxis_title = "Number of Circumferential Slotting Metal Loss Defects"
# #         elif dimension_class == "Pinhole":
# #             # title += " - Pinhole Classification"
# #             yaxis_title = "Number of Pinhole Metal Loss Defects"
# #         elif dimension_class == "General":
# #             # title += " - General Classification"
# #             yaxis_title = "Number of General Metal Loss Defects"
# #         elif dimension_class == "Both":
# #             # title += " - All Classification"
# #             yaxis_title = "Total Number of Metal Loss Defects"
# #     print(f"[DEBUG] Final bin counts:\n{bin_counts}")
# #     # Plotting the graph
# #     fig = go.Figure()
# #     fig.add_trace(go.Bar(
# #         x=bin_counts['Bin Label'],
# #         y=bin_counts['Metal Loss Count'],
# #         width=[bin_size * 0.8] * len(bin_counts),
# #         marker_color='steelblue',
# #         hovertemplate='Distance Bin: 0 - %{x} m<br>Metal Loss Count: %{y}<extra></extra>',
# #         name=f'{feature_type} Metal Loss Defects' if feature_type else 'Metal Loss Defects'
# #     ))
# #
# #     fig.update_layout(
# #         # title=title,
# #         xaxis=dict(
# #             title='Distance from Launcher (ODDO) in meters',
# #             tickmode='linear',
# #             dtick=500,
# #             tickformat='d',
# #             gridcolor='lightgray'
# #         ),
# #         yaxis=dict(
# #             title=yaxis_title,
# #             tick0=0,
# #             dtick=5,
# #             gridcolor='lightgray'
# #         ),
# #         height=700,
# #         width=1600,
# #         template='plotly_white'
# #     )
# #
# #     # Save the plot as an HTML file
# #     html_path = os.path.abspath('metal_loss_graph.html')
# #     fig.write_html(html_path)
# #
# #     if return_fig:
# #         return fig, html_path
# #     else:
# #         return html_path
#
#
#
#
#
#
#
# import pandas as pd
# import plotly.graph_objects as go
# import os
#
# def plot_metal_loss(df, feature_type=None, dimension_class=None, return_fig=False):
#     df.columns = df.columns.str.strip()
#     print(f"[DEBUG] Initial dataframe shape: {df.shape}")
#
#     # Filter only Metal Loss records
#     df = df[df['Feature Type'].str.strip().str.lower() == 'metal loss']
#     print(f"[DEBUG] After filtering Metal Loss: {df.shape}")
#
#     # Standardize strings
#     df['Feature Identification'] = df['Feature Identification'].astype(str).str.strip()
#     df['Dimension Classification'] = df['Dimension Classification'].astype(str).str.strip()
#
#     print(f"[DEBUG] Unique Feature Identifications: {df['Feature Identification'].unique()}")
#     print(f"[DEBUG] Unique Dimension Classifications: {df['Dimension Classification'].unique()}")
#
#     # Filter by Feature Identification if specified
#     if feature_type:
#         if feature_type == "Corrosion":
#             df = df[df['Feature Identification'].str.contains('Corrosion', case=False, na=False)]
#             print(f"[DEBUG] After filtering Feature Identification (Corrosion): {df.shape}")
#         elif feature_type == "MFG":
#             df = df[df['Feature Identification'].str.contains('MFG', case=False, na=False)]
#             print(f"[DEBUG] After filtering Feature Identification (MFG): {df.shape}")
#
#     # Filter by Dimension Classification if specified
#     if dimension_class and dimension_class != "ALL":
#         df = df[df['Dimension Classification'].str.contains(dimension_class, case=False, na=False)]
#         print(f"[DEBUG] After filtering Dimension Classification ({dimension_class}): {df.shape}")
#
#     if df.empty:
#         print("No matching defects found in the file.")
#         return None
#
#     # Define bins
#     bin_size = 500
#     max_distance = df['Abs. Distance (m)'].max()
#     bins = list(range(0, int(max_distance) + bin_size, bin_size))
#
#     # Assign bins
#     df.loc[:, 'Distance Bin'] = pd.cut(df['Abs. Distance (m)'], bins=bins, right=True)
#
#     # Count records per bin
#     bin_counts = df.groupby('Distance Bin', observed=False).size().reset_index(name='Metal Loss Count')
#     bin_counts['Bin Start'] = bin_counts['Distance Bin'].apply(lambda x: int(x.left))
#     bin_counts['Bin End'] = bin_counts['Distance Bin'].apply(lambda x: int(x.right))
#     bin_counts['Bin Mid'] = bin_counts['Distance Bin'].apply(lambda x: (x.left + x.right) / 2)
#
#     print(f"[DEBUG] Final bin counts:\n{bin_counts}")
#
#     # Build bar plot
#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         x=bin_counts['Bin Mid'],
#         y=bin_counts['Metal Loss Count'],
#         width=[bin_size * 0.8] * len(bin_counts),
#         marker_color='steelblue',
#         hovertemplate='Distance Bin: %{customdata[0]} - %{customdata[1]} m<br>Metal Loss Count: %{y}<extra></extra>',
#         customdata=bin_counts[['Bin Start', 'Bin End']],
#         name='Metal Loss Defects'
#     ))
#
#     # Dynamic Y-axis title
#     y_axis_title = "Number of"
#     if feature_type:
#         y_axis_title += f" {feature_type}"
#     if dimension_class:
#         y_axis_title += f" {dimension_class}"
#     y_axis_title += " Metal Loss Defects"
#
#     # Final layout
#     fig.update_layout(
#         xaxis=dict(
#             title='Distance from Launcher (ODDO) in meters',
#             tickmode='linear',
#             dtick=500,
#             tickformat='d',
#             gridcolor='lightgray'
#         ),
#         yaxis=dict(
#             title=y_axis_title,
#             tick0=0,
#             dtick=5,
#             gridcolor='lightgray'
#         ),
#         height=700,
#         width=1600,
#         template='plotly_white'
#     )
#
#     # Save HTML
#     html_path = os.path.abspath('metal_loss_graph.html')
#     fig.write_html(html_path)
#
#     if return_fig:
#         return fig, html_path
#     else:
#         return html_path
#
#
# def plot_sensor_percentage(df, return_fig=False):
#     df.columns = df.columns.str.strip()
#
#     # Debug to ensure correct columns
#     print(f"[DEBUG] DataFrame Columns: {df.columns.tolist()}")
#
#     # If Sensor % column does not exist, you can simulate or prompt the user to check
#     # if 'Sensor %' not in df.columns:
#     #     print("[INFO] 'Sensor %' column not found. Creating random sensor data.")
#     #     import numpy as np
#     #     np.random.seed(0)
#     #     df['Sensor %'] = np.random.uniform(low=70, high=100, size=len(df))
#
#     df.sort_values(by='Abs. Distance (m)', inplace=True)
#
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(
#         x=df['Abs. Distance (m)'],
#         y=df['Sensor %'],
#         mode='lines',
#         name='Sensor %',
#         line=dict(color='green', width=2)
#     ))
#
#     fig.update_layout(
#         title='Sensor % vs. Absolute Distance',
#         xaxis=dict(title='Absolute Distance (m)', gridcolor='lightgray', dtick=2000),
#         yaxis=dict(
#             title='Sensor %',
#             gridcolor='lightgray',
#             range=[0, 100],  # 👉 Fixed Y-axis range
#             dtick=20         # 👉 Y-axis ticks at 0, 20, 40, ..., 100
#         ),
#         height=700,
#         width=1600,
#         template='plotly_white'
#     )
#
#     html_path = os.path.abspath('sensor_percentage_plot.html')
#     fig.write_html(html_path)
#
#     if return_fig:
#         return fig, html_path
#     else:
#         return html_path
#
#
#
#











import pandas as pd
import plotly.graph_objects as go
import os
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Polygon


# Updated Metal Loss Plot function
# def plot_metal_loss(df, feature_type=None, dimension_class=None, return_fig=False):
#     df.columns = df.columns.str.strip()
#     print(f"[DEBUG] Initial dataframe shape: {df.shape}")
#
#     # Filter only Metal Loss records
#     df = df[df['Feature Type'].str.strip().str.lower() == 'metal loss']
#     print(f"[DEBUG] After filtering Metal Loss: {df.shape}")
#
#     # Filter by Feature Identification if specified
#     if feature_type:
#         if feature_type == "Corrosion":
#             df = df[df['Feature Identification'].str.contains('Corrosion', case=False, na=False)]
#         elif feature_type == "MFG":
#             df = df[df['Feature Identification'].str.contains('MFG', case=False, na=False)]
#
#     # Filter by Dimension Classification if specified
#     if dimension_class and dimension_class != "ALL":
#         df = df[df['Dimension Classification'].str.contains(dimension_class, case=False, na=False)]
#
#     if df.empty:
#         print("No matching defects found in the file.")
#         return None
#
#     # Define bins
#     bin_size = 500
#     max_distance = df['Abs. Distance (m)'].max()
#     bins = list(range(0, int(max_distance) + bin_size, bin_size))
#
#     # Assign bins
#     df.loc[:, 'Distance Bin'] = pd.cut(df['Abs. Distance (m)'], bins=bins, right=True)
#
#     # Count records per bin
#     bin_counts = df.groupby('Distance Bin', observed=False).size().reset_index(name='Metal Loss Count')
#     bin_counts['Bin Start'] = bin_counts['Distance Bin'].apply(lambda x: int(x.left))
#     bin_counts['Bin End'] = bin_counts['Distance Bin'].apply(lambda x: int(x.right))
#     bin_counts['Bin Mid'] = bin_counts['Distance Bin'].apply(lambda x: (x.left + x.right) / 2)
#
#     # # Set dynamic Y-axis title based on Feature Identification and Dimension Classification
#     # if feature_type == "Corrosion":
#     #     yaxis_title = "Number of Corrosion Metal Loss Defects"
#     # elif feature_type == "MFG":
#     #     yaxis_title = "Number of MFG Metal Loss Defects"
#     # else:
#     #     yaxis_title = "Number of Metal Loss Defects"
#     #
#     # # Update title based on Dimension Classification
#     # if dimension_class:
#     #     if dimension_class == "Pitting":
#     #         yaxis_title = "Number of Pitting Metal Loss Defects"
#     #     elif dimension_class == "Axial Grooving":
#     #         yaxis_title = "Number of Axial Grooving Metal Loss Defects"
#     #     elif dimension_class == "Axial Slotting":
#     #         yaxis_title = "Number of Axial Slotting Metal Loss Defects"
#     #     elif dimension_class == "Circumferential Grooving":
#     #         yaxis_title = "Number of Circumferential Grooving Metal Loss Defects"
#     #     elif dimension_class == "Circumferential Slotting":
#     #         yaxis_title = "Number of Circumferential Slotting Metal Loss Defects"
#     #     elif dimension_class == "Pinhole":
#     #         yaxis_title = "Number of Pinhole Metal Loss Defects"
#     #     elif dimension_class == "General":
#     #         yaxis_title = "Number of General Metal Loss Defects"
#
#
#     # Plotting the graph
#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         x=bin_counts['Bin Mid'],
#         y=bin_counts['Metal Loss Count'],
#         width=[bin_size * 0.8] * len(bin_counts),
#         marker_color='steelblue',
#         hovertemplate="Distance Bin: %{customdata[0]} - %{customdata[1]} m<br>Metal Loss Count: %{y}<extra></extra>",
#         customdata=bin_counts[['Bin Start','Bin End']],
#         name=f'{feature_type} Metal Loss Defects' if feature_type else 'Metal Loss Defects'
#     ))
#
#
#     yaxis_title="Number of"
#     if feature_type:
#         yaxis_title += f" {feature_type}"
#     if dimension_class:
#         yaxis_title += f" {dimension_class}"
#     yaxis_title += f" Metal Loss Defects"
#
#     # Final layout
#     fig.update_layout(
#         xaxis=dict(
#             title='Distance from Launcher (ODDO) in meters',
#             tickmode='linear',
#             dtick=500,
#             tickformat='d',
#             gridcolor='lightgray'
#         ),
#         yaxis=dict(
#             title=yaxis_title,  # Dynamic title based on feature and classification
#             tick0=0,
#             dtick=5,
#             gridcolor='lightgray'
#         ),
#         height=700,
#         width=1600,
#         template='plotly_white'
#     )
#
#     # Save the plot as an HTML file
#     html_path = os.path.abspath('metal_loss_graph.html')
#     fig.write_html(html_path)
#
#     if return_fig:
#         return fig, html_path
#     else:
#         return html_path



# def draw_3d_bar(ax, x, height, width=0.4, depth=0.3, face_colors=('#4F81BD', '#4F81BD', '#385D8A')):
#     # Front face
#     front = [[x, 0], [x, height], [x + width, height], [x + width, 0]]
#     ax.add_patch(Polygon(front, closed=True, facecolor=face_colors[0]))
#
#     # Top face
#     top = [[x, height], [x + depth, height + depth], [x + width + depth, height + depth], [x + width, height]]
#     ax.add_patch(Polygon(top, closed=True, facecolor=face_colors[1]))
#
#     # Side face
#     side = [[x + width, 0], [x + width, height], [x + width + depth, height + depth], [x + width + depth, depth]]
#     ax.add_patch(Polygon(side, closed=True, facecolor=face_colors[2]))
#
# def plot_metal_loss(df, feature_type=None, dimension_class=None, return_fig=False):
#     df.columns = df.columns.str.strip()
#     print(f"[DEBUG] Initial dataframe shape: {df.shape}")
#
#     df = df[df['Feature Type'].str.strip().str.lower() == 'metal loss']
#     print(f"[DEBUG] After filtering Metal Loss: {df.shape}")
#
#     if feature_type:
#         if feature_type == "Corrosion":
#             df = df[df['Feature Identification'].str.contains('Corrosion', case=False, na=False)]
#         elif feature_type == "MFG":
#             df = df[df['Feature Identification'].str.contains('MFG', case=False, na=False)]
#
#     if dimension_class and dimension_class != "ALL":
#         df = df[df['Dimension Classification'].str.contains(dimension_class, case=False, na=False)]
#
#     if df.empty:
#         print("No matching defects found in the file.")
#         return None
#
#     bin_size = 500
#     max_distance = df['Abs. Distance (m)'].max()
#     bins = list(range(0, int(max_distance) + bin_size, bin_size))
#     df['Distance Bin'] = pd.cut(df['Abs. Distance (m)'], bins=bins, right=True)
#
#     bin_counts = df.groupby('Distance Bin', observed=False).size().reset_index(name='Metal Loss Count')
#     bin_counts['Bin Start'] = bin_counts['Distance Bin'].apply(lambda x: int(x.left))
#     bin_counts['Label'] = bin_counts['Bin Start'].astype(str)
#
#     # Plotting
#     fig, ax = plt.subplots(figsize=(20, 6))  # wider to fit more bars
#
#     values = bin_counts['Metal Loss Count'].tolist()
#     x_labels = bin_counts['Label'].tolist()
#
#     for i, val in enumerate(values):
#         draw_3d_bar(ax, i, val, face_colors=('#4F81BD', '#4F81BD', '#385D8A'))
#
#     ax.set_xticks(np.arange(len(x_labels)) + 0.3)
#     ax.set_xticklabels(x_labels)
#     ax.set_xlabel('Distance from Launcher (m)')
#
#     yaxis_title = "No. of"
#     if feature_type:
#         yaxis_title += f" {feature_type}"
#     if dimension_class:
#         yaxis_title += f" {dimension_class}"
#     yaxis_title += " Metal Losses"
#     ax.set_ylabel(yaxis_title)
#     ax.set_title('Distribution of Metal Loss Defects')
#     ax.set_xlim(-0.5, len(values))
#     ax.set_ylim(0, max(values) + 2)
#     ax.grid(False)
#
#     plt.tight_layout()
#
#     # Save as PNG
#     image_path = os.path.abspath('metal_loss_3d_look_plot.png')
#     fig.savefig(image_path)
#
#     if return_fig:
#         return fig, image_path
#     else:
#         return image_path


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def draw_3d_bar(ax, x, height, width=0.4, depth=0.3, face_colors=('#4F81BD', '#4F81BD', '#385D8A')):
    front = [[x, 0], [x, height], [x + width, height], [x + width, 0]]
    ax.add_patch(Polygon(front, closed=True, facecolor=face_colors[0]))

    top = [[x, height], [x + depth, height + depth], [x + width + depth, height + depth], [x + width, height]]
    ax.add_patch(Polygon(top, closed=True, facecolor=face_colors[1]))

    side = [[x + width, 0], [x + width, height], [x + width + depth, height + depth], [x + width + depth, depth]]
    ax.add_patch(Polygon(side, closed=True, facecolor=face_colors[2]))

def plot_metal_loss(df, tally_max_distance=None, bin_size=500, feature_type=None, dimension_class=None, return_fig=False):
    df.columns = df.columns.str.strip()
    df = df[df['Feature Type'].str.lower().str.strip() == 'metal loss']

    # Optional filtering

    if feature_type:
        if feature_type == "Corrosion":
            df = df[df['Feature Identification'].str.contains('Corrosion', case=False, na=False)]
        elif feature_type == "MFG":
            df = df[df['Feature Identification'].str.contains('MFG', case=False, na=False)]

    if dimension_class and dimension_class.upper() != "ALL":
        df = df[df['Dimension Classification'].str.contains(dimension_class, case=False, na=False)]

    # ✅ Calculate full bin range using max ODDO
    if tally_max_distance is None:
        tally_max_distance = df['Abs. Distance (m)'].max()

    max_distance = int(((tally_max_distance // bin_size) + 1) * bin_size)
    bins = list(range(0, max_distance + bin_size, bin_size))
    bin_labels = [str(b) for b in bins[:-1]]

    # Predefine all bins with 0
    interval_index = pd.IntervalIndex.from_breaks(bins, closed='left')
    bin_counts = pd.Series(0, index=interval_index)

    # Count actual bins
    df['Distance Bin'] = pd.cut(df['Abs. Distance (m)'], bins=interval_index)
    actual_counts = df['Distance Bin'].value_counts()
    bin_counts.update(actual_counts)

    values = bin_counts.tolist()

    # Plotting
    fig, ax = plt.subplots(figsize=(20, 6))
    for i, val in enumerate(values):
        draw_3d_bar(ax, i, val)

    ax.set_xticks(np.arange(len(bin_labels)) + 0.3)
    ax.set_xticklabels(bin_labels, rotation=45)
    ax.set_xlabel('Distance from Launcher (m)')

    yaxis_title = "No. of"
    if feature_type:
        yaxis_title += f" {feature_type}"
    if dimension_class:
        yaxis_title += f" {dimension_class}"
    yaxis_title += " Metal Losses"

    ax.set_ylabel(yaxis_title)
    ax.set_title('Distribution of Metal Loss Defects')
    ax.set_xlim(-0.5, len(bin_labels) - 0.5)
    ax.set_ylim(0, max(values) + 2)
    ax.grid(False)
    plt.tight_layout()

    image_path = os.path.abspath(f'metal_loss_3d_look_plot_{feature_type or "all"}.png')
    fig.savefig(image_path)

    if return_fig:
        return fig, image_path
    else:
        return image_path









# Updated Sensor Loss Plot function
def plot_sensor_percentage(df, return_fig=False):
    df.columns = df.columns.str.strip()

    # Sort values based on distance for better visualization
    df.sort_values(by='Abs. Distance (m)', inplace=True)
    x_tick_vals = np.arange(0, df['Abs. Distance (m)'].max() + 1, 2000)
    x_tick_text = [str(int(val)) for val in x_tick_vals]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Abs. Distance (m)'],
        y=df['Sensor %'],
        mode='lines',
        name='Sensor %',
        line=dict(color='green', width=2)
    ))

    fig.update_layout(
        # title='Sensor % vs. Absolute Distance',
        title={
            'text': 'Sensor Loss%',
            'x': 0.5,  # Center the title
            'xanchor': 'center',
            'font': {
                'size': 20,
                'color': 'black',
                'family': 'Arial',

            }
        },

        xaxis=dict(title='Absolute Distance (m)', gridcolor='lightgray', dtick=2000,tickformat=','),
        yaxis=dict(
            title='Sensor Loss%',
            gridcolor='lightgray',
            range=[0, 100],  # Fixed Y-axis range
            dtick=20         # Y-axis ticks at 0, 20, 40, ..., 100
        ),
        height=700,
        width=1600,
        template='plotly_white'
    )

    html_path = os.path.abspath('sensor_percentage_plot.html')
    fig.write_html(html_path)

    if return_fig:
        return fig, html_path
    else:
        return html_path

def plot_temperature(df, return_fig=False):
    df.columns = df.columns.str.strip()
    df.sort_values(by='Abs. Distance (m)', inplace=True)
    if 'Temperature (°C)' not in df.columns:
        temperature_profile = np.linspace(55, 50, len(df))
        noise=np.random.uniform(low=-0.5,high=0.5, size=len(df))

        df['Temperature (°C)'] = temperature_profile + noise

        # x_tick_vals = np.arange(0, df['Abs. Distance (m)'].max() + 1, 2000)
        # x_tick_text = [str(int(val)) for val in x_tick_vals]
    # Calculate dynamic y-axis range
    # y_min = df['Temperature (°C)'].min() - 5
    # y_max = df['Temperature (°C)'].max() + 5

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Abs. Distance (m)'],
        y=df['Temperature (°C)'],
        mode='lines',
        name='Temperature Profile',
        line=dict(color='blue', width=2)
    ))

    fig.update_layout(
        # title='Temperature Level Profile',
        title={
        'text': 'Temperature Plot',
        'x': 0.5,  # Center the title
        'xanchor': 'center',
        'font': {
            'size': 20,
            'color': 'black',
            'family': 'Arial',

        }
    },
        xaxis=dict(title='Absolute Distance (m)', gridcolor='lightgray', dtick=2000,tickformat=','),

        yaxis=dict(
            title='Temperature (°C)',
            gridcolor='lightgray',
            range=[0, 100],
            dtick=10
        ),
        height=700,
        width=1600,
        template='plotly_white'
    )

    html_path = os.path.abspath('temperature_plot.html')
    fig.write_html(html_path)

    if return_fig:
        return fig, html_path
    else:
        return html_path