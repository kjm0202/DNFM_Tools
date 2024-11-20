import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

def get_files_in_directory(directory):
    try:
        return os.listdir(directory)
    except Exception as e:
        print(f"Could not read directory {directory}: {e}")
        return []

def get_base_file_name(file_name):
    return file_name.split('#')[0].replace(" ", "") if '#' in file_name else file_name.replace(" ", "")

def find_unique_files(src_directory, dst_directory):
    src_files = get_files_in_directory(src_directory)
    dst_files = get_files_in_directory(dst_directory)
    src_base_files = {get_base_file_name(file) for file in src_files}
    dst_base_files = {get_base_file_name(file) for file in dst_files}
    unique_files = dst_base_files - src_base_files
    return [file for file in dst_files if get_base_file_name(file) in unique_files]

def copy_unique_files_to_directory(unique_files, src_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for file in unique_files:
        src_file_path = os.path.join(src_directory, file)
        dst_file_path = os.path.join(output_directory, file)
        try:
            shutil.copy2(src_file_path, dst_file_path)
            print(f"Copied {file} to {output_directory}")
        except Exception as e:
            print(f"Could not copy {file} to {output_directory}: {e}")

def select_src_directory():
    src_directory = filedialog.askdirectory()
    src_dir_var.set(src_directory)

def select_dst_directory():
    dst_directory = filedialog.askdirectory()
    dst_dir_var.set(dst_directory)

def run_comparison():
    src_directory = src_dir_var.get()
    dst_directory = dst_dir_var.get()
    if not src_directory or not dst_directory:
        messagebox.showerror("Error", "Both directories must be selected.")
        return
    unique_files = find_unique_files(src_directory, dst_directory)
    if unique_files:
        today = datetime.today().strftime('%y%m%d')
        output_directory = os.path.join(os.path.expanduser('~'), 'Downloads', f'unique_sprites_{today}')
        copy_unique_files_to_directory(unique_files, dst_directory, output_directory)
        messagebox.showinfo("Success", f"Found {len(unique_files)} unique files. Copied to {output_directory}.")
    else:
        messagebox.showinfo("Info", "No unique files found in the second folder.")

root = tk.Tk()
root.title("Sprite Compare Tool")

src_dir_var = tk.StringVar()
dst_dir_var = tk.StringVar()

tk.Label(root, text="구버전 디렉토리를 선택하세요:").pack(pady=5)
tk.Entry(root, textvariable=src_dir_var, width=50).pack(pady=5)
tk.Button(root, text="탐색", command=select_src_directory).pack(pady=5)

tk.Label(root, text="신버전 디렉토리를 선택하세요:").pack(pady=5)
tk.Entry(root, textvariable=dst_dir_var, width=50).pack(pady=5)
tk.Button(root, text="탐색", command=select_dst_directory).pack(pady=5)

tk.Button(root, text="추가된 파일 찾기", command=run_comparison).pack(pady=20)

root.mainloop()