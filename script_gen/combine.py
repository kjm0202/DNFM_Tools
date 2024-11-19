import os

def combine_script_files(directory, output_file):
    # Open the output file in write mode
    with open(output_file, 'w', encoding='utf-8', errors='ignore') as outfile:
        # Walk through the directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Check if the file name starts with 'script_'
                if file.startswith('script_'):
                    # Construct the full file path
                    file_path = os.path.join(root, file)

                    # Try to open the file and ignore encoding errors
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                            # Read the content of the file and write it to the output file
                            content = infile.read()
                            outfile.write(f"--- Start of {file} ---\n")
                            outfile.write(content)
                            outfile.write(f"\n--- End of {file} ---\n\n")
                    except Exception as e:
                        print(f"Could not read file {file_path}: {e}")

# Directory path
directory_path = r'C:\Users\kjm19\Documents\AssetStudio.net472_v0.16.53\DNFM\DNFM_Data\StreamingAssets\bundles'
# Output file path
output_file_path = r'C:\Users\kjm19\Documents\combined_script_files2.txt'

# Combine the script files into one file
combine_script_files(directory_path, output_file_path)

print(f"Script files have been combined into {output_file_path}")
