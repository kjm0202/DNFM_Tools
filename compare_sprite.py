import os
import shutil

def get_files_in_directory(directory):
    try:
        return os.listdir(directory)
    except Exception as e:
        print(f"Could not read directory {directory}: {e}")
        return []

def get_base_file_name(file_name):
    return file_name.split('#')[0].strip() if '#' in file_name else file_name

def copy_unique_files(src_directory, dst_directory, output_directory):
    # Get the list of files in each directory
    src_files = get_files_in_directory(src_directory)
    dst_files = get_files_in_directory(dst_directory)

    # Create a set of base file names for comparison
    src_base_files = {get_base_file_name(file) for file in src_files}
    dst_base_files = {get_base_file_name(file) for file in dst_files}

    # Find base file names that are in dst_directory but not in src_directory
    unique_base_files = dst_base_files - src_base_files

    # Find the actual file names in dst_directory that correspond to the unique base file names
    unique_files = [file for file in dst_files if get_base_file_name(file) in unique_base_files]

    # Copy unique files to the output directory
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for file in unique_files:
        src_file_path = os.path.join(dst_directory, file)
        dst_file_path = os.path.join(output_directory, file)

        try:
            shutil.copy2(src_file_path, dst_file_path)
            print(f"Copied {file} to {output_directory}")
        except Exception as e:
            print(f"Could not copy {file} to {output_directory}: {e}")

# Directories
src_directory = r'C:\Users\kjm19\Documents\AssetStudio.net472_v0.16.53\exported_240808\Sprite'
dst_directory = r'C:\Users\kjm19\Documents\AssetStudio.net472_v0.16.53\exported_2408081\Sprite'
output_directory = r'C:\Users\kjm19\Documents\unique_files'

# Copy unique files
copy_unique_files(src_directory, dst_directory, output_directory)
