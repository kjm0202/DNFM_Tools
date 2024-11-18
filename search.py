import os

def list_script_files_with_event_index(directory):
    # List to store filenames that contain "event index"
    files_with_event_index = []

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file name starts with 'script_'
            if file.startswith('script_'):
                # Construct the full file path
                file_path = os.path.join(root, file)

                # Try to open the file and ignore encoding errors
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Check if "event index" is in the file content
                        if "Arcade" in content:
                            files_with_event_index.append(file)
                except Exception as e:
                    print(f"Could not read file {file_path}: {e}")

    return files_with_event_index

# Directory path
directory_path = r'C:\Users\kjm19\Documents\AssetStudio.net472_v0.16.53\DNFM\DNFM_Data\StreamingAssets\bundles'

# Get the list of script files containing "event index"
files = list_script_files_with_event_index(directory_path)

# Print the results
for file in files:
    print(file)
