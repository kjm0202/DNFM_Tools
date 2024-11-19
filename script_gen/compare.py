import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

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

def select_file1():
    file_path = filedialog.askopenfilename()
    if file_path:
        file1_var.set(file_path)

def select_file2():
    file_path = filedialog.askopenfilename()
    if file_path:
        file2_var.set(file_path)

def run_comparison():
    file1_path = file1_var.get()
    file2_path = file2_var.get()
    output_path = str(Path.home() / "Downloads" / "unique_contents_in_new_script.txt")

    if not file1_path or not os.path.isfile(file1_path):
        messagebox.showerror("Error", "Please select a valid first file.")
        return

    if not file2_path or not os.path.isfile(file2_path):
        messagebox.showerror("Error", "Please select a valid second file.")
        return

    file1_content = read_file_ignore_errors(file1_path)
    file2_content = read_file_ignore_errors(file2_path)
    unique_content = get_unique_content(file1_content, file2_content)

    try:
        with open(output_path, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(unique_content)
        messagebox.showinfo("Success", f"Unique content has been written to {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not write to file {output_path}: {e}")

# Create the GUI window
root = tk.Tk()
root.title("스크립트 비교")
root.geometry("640x240")

# File 1 selection
file1_var = tk.StringVar()
tk.Label(root, text="구버전의 스크립트 파일을 선택하세요: ").pack(pady=5)
frame1 = tk.Frame(root)
frame1.pack(pady=5)
tk.Entry(frame1, textvariable=file1_var, width=60).pack(side=tk.LEFT, padx=5)
tk.Button(frame1, text="탐색", command=select_file1).pack(side=tk.LEFT)

# File 2 selection
file2_var = tk.StringVar()
tk.Label(root, text="신버전의 스크립트 파일을 선택하세요: ").pack(pady=5)
frame2 = tk.Frame(root)
frame2.pack(pady=5)
tk.Entry(frame2, textvariable=file2_var, width=60).pack(side=tk.LEFT, padx=5)
tk.Button(frame2, text="탐색", command=select_file2).pack(side=tk.LEFT)

# Run button to start the comparison
tk.Button(root, text="추가된 문구 찾기", command=run_comparison).pack(pady=20)

# Run the GUI loop
root.mainloop()