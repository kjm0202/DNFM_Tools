def read_file_ignore_errors(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Could not read file {file_path}: {e}")
        return ""

def get_unique_content(file1_content, file2_content):
    file1_lines = set(file1_content.splitlines())
    file2_lines = set(file2_content.splitlines())

    # Find lines that are in file2 but not in file1
    unique_lines = file2_lines - file1_lines
    return "\n".join(unique_lines)

# File paths
file1_path = r'C:\Users\kjm19\Documents\combined_script_files.txt'
file2_path = r'C:\Users\kjm19\Documents\combined_script_files1.txt'
output_path = r'C:\Users\kjm19\Documents\unique_content.txt'

# Read the files
file1_content = read_file_ignore_errors(file1_path)
file2_content = read_file_ignore_errors(file2_path)

# Get the unique content
unique_content = get_unique_content(file1_content, file2_content)

# Write the unique content to the output file
try:
    with open(output_path, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(unique_content)
    print(f"Unique content has been written to {output_path}")
except Exception as e:
    print(f"Could not write to file {output_path}: {e}")
