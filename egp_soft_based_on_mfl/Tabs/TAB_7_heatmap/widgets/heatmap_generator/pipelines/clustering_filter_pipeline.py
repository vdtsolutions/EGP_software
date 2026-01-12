import pandas as pd

def find_defect_regions_using_clustering(data_array):
    """
    Scan data_array for connected non-zero clusters using dfs(),
    build bounding boxes for each cluster, merge overlaps,
    and return a sorted dataframe of defect regions.
    """

    visited = set()
    bounding_boxes = []

    # Walk entire anomaly matrix
    for i in range(data_array.shape[0]):
        for j in range(data_array.shape[1]):
            if data_array[i, j] != 0 and (i, j) not in visited:
                cluster = []
                dfs(data_array, i, j, visited, cluster)

                if cluster:
                    min_row = min(point[0] for point in cluster)
                    max_row = max(point[0] for point in cluster)
                    min_col = min(point[1] for point in cluster)
                    max_col = max(point[1] for point in cluster)

                    bounding_boxes.append({
                        'start_row': min_row,
                        'end_row': max_row,
                        'start_col': min_col,
                        'end_col': max_col
                    })

    merged_boxes = merge_all_overlapping_boxes(bounding_boxes)

    if len(merged_boxes) == 0:
        # return empty frame with expected columns to avoid downstream KeyError
        return pd.DataFrame(columns=['start_row', 'end_row', 'start_col', 'end_col'])

    df_sorted = pd.DataFrame(merged_boxes).sort_values(by='start_col')
    return df_sorted


def dfs(matrix, x, y, visited, cluster):
    """Perform DFS to find clusters, but only include positive values."""
    stack = [(x, y)]
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        if matrix[cx, cy] <= 0:
            continue
        visited.add((cx, cy))
        cluster.append((cx, cy))
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if (0 <= nx < matrix.shape[0] and 0 <= ny < matrix.shape[1] and
                    matrix[nx, ny] > 0 and (nx, ny) not in visited):
                stack.append((nx, ny))


# Find clusters of connected non-zero values and calculate bounding boxes
def merge_all_overlapping_boxes(boxes, max_distance=3):
    merged = []
    while boxes:
        current = boxes.pop(0)
        overlap_found = True
        while overlap_found:
            overlap_found = False
            i = 0
            while i < len(boxes):
                if do_boxes_overlap_or_close(current, boxes[i], max_distance):
                    current = merge_boxes(current, boxes[i])
                    boxes.pop(i)
                    overlap_found = True
                else:
                    i += 1
        merged.append(current)
    return merged


def do_boxes_overlap_or_close(box1, box2, max_distance=3):
    return do_boxes_overlap(box1, box2) or boxes_are_close(box1, box2, max_distance)


def merge_boxes(box1, box2):
    """Merge two overlapping bounding boxes into one."""
    return {
        'start_row': min(box1['start_row'], box2['start_row']),
        'end_row': max(box1['end_row'], box2['end_row']),
        'start_col': min(box1['start_col'], box2['start_col']),
        'end_col': max(box1['end_col'], box2['end_col'])
    }


def do_boxes_overlap(box1, box2):
    """Check if two bounding boxes overlap."""
    return not (box1['end_row'] < box2['start_row'] or
                box1['start_row'] > box2['end_row'] or
                box1['end_col'] < box2['start_col'] or
                box1['start_col'] > box2['end_col'])


def boxes_are_close(box1, box2, max_distance=3):
    # Compute closest horizontal and vertical distances between boxes
    h_dist = max(0,
                 max(box1['start_col'] - box2['end_col'], box2['start_col'] - box1['end_col']))
    v_dist = max(0,
                 max(box1['start_row'] - box2['end_row'], box2['start_row'] - box1['end_row']))
    return (h_dist + v_dist) <= max_distance