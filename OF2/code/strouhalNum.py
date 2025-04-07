import os
import numpy as np

# Define folder paths (Replace with actual paths)
folder_paths = [
    "/meshB/", "folder2", "folder3",
    "folder4", "folder5", "folder6"
]

# Function to process a single file
def process_file(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if not line.startswith("#"):  # Skip headers
                values = line.split()  # Split line into columns
                data.append([float(v) for v in values])  # Convert to float

    # Convert list to NumPy array
    data = np.array(data)

    # Extract columns 1, 2, 3 (0-based indexing in NumPy)
    time = data[:, 0]  # First column (time)
    col1, col2, col3 = data[:, 1], data[:, 2], data[:, 3]  # Data columns

    return time, col1, col2, col3

# Process files from each folder
results = {}

for folder in folder_paths:
    files = sorted(os.listdir(folder))  # Sort files for consistency
    if len(files) < 2:
        print(f"Warning: Less than 2 files in {folder}. Skipping.")
        continue

    file1_path = os.path.join(folder, files[0])
    file2_path = os.path.join(folder, files[1])

    print(f"Processing: {file1_path} and {file2_path}")

    # Process both files
    time1, col1_1, col2_1, col3_1 = process_file(file1_path)
    time2, col1_2, col2_2, col3_2 = process_file(file2_path)

    # Store results in dictionary
    results[folder] = {
        "file1": {"time": time1, "col1": col1_1, "col2": col2_1, "col3": col3_1},
        "file2": {"time": time2, "col1": col1_2, "col2": col2_2, "col3": col3_2},
    }

# Print example output
for folder, data in results.items():
    print(f"\nFolder: {folder}")
    print(f"File 1 - Time: {data['file1']['time'][:5]}")
    print(f"File 1 - Col1: {data['file1']['col1'][:5]}")
    print(f"File 1 - Col2: {data['file1']['col2'][:5]}")
    print(f"File 1 - Col3: {data['file1']['col3'][:5]}")

    print(f"File 2 - Time: {data['file2']['time'][:5]}")
    print(f"File 2 - Col1: {data['file2']['col1'][:5]}")
    print(f"File 2 - Col2: {data['file2']['col2'][:5]}")
    print(f"File 2 - Col3: {data['file2']['col3'][:5]}")

