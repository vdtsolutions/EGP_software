import os
import shutil


def manage_directory(directory_path):
    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory created: {directory_path}")
    else:
        print(f"Directory already exists: {directory_path}")

    # Delete all existing files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

    print(f"All files deleted from directory: {directory_path}")






def save_submatrices(submatrices_dict, output_dir):
    """
    Saves all submatrices from a dictionary into CSV files.
    """
    print("inside submatrices")
    os.makedirs(output_dir, exist_ok=True)

    for (defect_id, start_sensor, end_sensor), matrix in submatrices_dict.items():
        filename = f"submatrix_ptt-1{defect_id, start_sensor, start_sensor}.csv"
        filepath = os.path.join(output_dir, filename)
        matrix.to_csv(filepath, index=False)
        # try:
        #     matrix.to_csv(filepath, index=False)
        #     print(f"✅ Saved: {filepath}")
        # except Exception as e:
        #     print(f"❌ Error saving {filename}: {e}")
