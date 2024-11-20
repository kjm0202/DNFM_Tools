import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import webbrowser
import shutil
from datetime import datetime

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Combine script files
def combine_script_files(directory, output_file):
    try:
        script_files = [os.path.join(root, file) for root, _, files in os.walk(directory) for file in files if file.startswith('script_')]
        if not script_files:
            messagebox.showerror("스크립트 발견 불가", "선택한 경로에서 스크립트 파일을 찾을 수 없습니다.")
            return
        with open(output_file, 'w', encoding='utf-8', errors='ignore') as outfile:
            for file_path in script_files:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                    outfile.write(f"--- Start of {os.path.basename(file_path)} ---\n")
                    outfile.write(infile.read())
                    outfile.write(f"\n--- End of {os.path.basename(file_path)} ---\n\n")
        messagebox.showinfo("석섹스", f"다음 파일명으로 성공적으로 합쳐졌습니다: {output_file}")
    except Exception as e:
        messagebox.showerror("오류", f"합체에 실패했습니다: {e}")

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        input_folder_var.set(directory)

def run_combination():
    input_folder = input_folder_var.get()
    output_file = str(Path.home() / "Downloads" / "merged_dnfm_scripts.txt")
    if not input_folder or not os.path.isdir(input_folder):
        messagebox.showerror("잘못된 경로", "올바른 스크립트가 있는 경로를 선택하세요.")
        return
    combine_script_files(input_folder, output_file)

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
    try:
        with open(file1_path, 'r', encoding='utf-8', errors='ignore') as f1, open(file2_path, 'r', encoding='utf-8', errors='ignore') as f2:
            file1_lines = set(f1.readlines())
            file2_lines = set(f2.readlines())
            unique_lines = file2_lines - file1_lines
        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.writelines(unique_lines)
        messagebox.showinfo("Success", f"Unique content has been written to {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not process files: {e}")

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

def run_sprite_comparison():
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


# Main GUI
root = tk.Tk()
root.title("스크립트 도구")
root.geometry("720x480")
root.configure(bg="#f0f0f0")  # Fluent UI 느낌의 부드러운 배경색

# Style configuration
style = ttk.Style()
style.configure("TNotebook", background="#f0f0f0")
style.configure("TNotebook.Tab", font=("Segoe UI", 10), padding=(10, 5))
style.configure("TLabel", background="#f0f0f0", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10), padding=5)
style.map("TButton", background=[("active", "#d6d6d6")])

# Notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Combine tab
combine_frame = ttk.Frame(notebook, style="TFrame")
notebook.add(combine_frame, text="스크립트 합체")

input_folder_var = tk.StringVar()
ttk.Label(combine_frame, text="스크립트가 있는 폴더를 선택하세요.").pack(pady=10)
folder_frame = ttk.Frame(combine_frame)
folder_frame.pack(pady=10)
ttk.Entry(folder_frame, textvariable=input_folder_var, width=60).pack(side=tk.LEFT, padx=10)
ttk.Button(folder_frame, text="탐색", command=select_directory).pack(side=tk.LEFT)
ttk.Button(combine_frame, text="파일 합체", command=run_combination).pack(pady=20)

tk.Label(combine_frame, text=r"합쳐진 스크립트는 Visual Studio Code를 설치하여 열람하세요.").pack(pady=10)
download_label = tk.Label(combine_frame, text=r"다운로드: https://code.visualstudio.com/", fg="blue", cursor="hand2", font="Helvetica 10 underline")
download_label.pack(pady=10)
download_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://code.visualstudio.com/"))

# Compare tab
compare_frame = ttk.Frame(notebook)
notebook.add(compare_frame, text="스크립트 비교")

file1_var = tk.StringVar()
file2_var = tk.StringVar()
ttk.Label(compare_frame, text="구버전 통합 스크립트 파일:").pack(pady=5)
file1_frame = ttk.Frame(compare_frame)
file1_frame.pack(pady=5)
ttk.Entry(file1_frame, textvariable=file1_var, width=60).pack(side=tk.LEFT, padx=10)
ttk.Button(file1_frame, text="탐색", command=select_file1).pack(side=tk.LEFT)

ttk.Label(compare_frame, text="신버전 통합 스크립트 파일:").pack(pady=5)
file2_frame = ttk.Frame(compare_frame)
file2_frame.pack(pady=5)
ttk.Entry(file2_frame, textvariable=file2_var, width=60).pack(side=tk.LEFT, padx=10)
ttk.Button(file2_frame, text="탐색", command=select_file2).pack(side=tk.LEFT)

ttk.Button(compare_frame, text="추가된 문구 찾기", command=run_comparison).pack(pady=20)

# Sprite Compare tab
sprite_frame = ttk.Frame(notebook)
notebook.add(sprite_frame, text="Sprite 비교")

src_dir_var = tk.StringVar()
dst_dir_var = tk.StringVar()

ttk.Label(sprite_frame, text="구버전 디렉토리를 선택하세요:").pack(pady=5)
ttk.Entry(sprite_frame, textvariable=src_dir_var, width=50).pack(pady=5)
ttk.Button(sprite_frame, text="탐색", command=select_src_directory).pack(pady=5)

ttk.Label(sprite_frame, text="신버전 디렉토리를 선택하세요:").pack(pady=5)
ttk.Entry(sprite_frame, textvariable=dst_dir_var, width=50).pack(pady=5)
ttk.Button(sprite_frame, text="탐색", command=select_dst_directory).pack(pady=5)

ttk.Button(sprite_frame, text="추가된 파일 찾기", command=run_sprite_comparison).pack(pady=20)

# About tab
about_frame = ttk.Frame(notebook)
notebook.add(about_frame, text="프로그램 정보")

tk.Label(about_frame, text="스크립트 도구 v0.1").pack(pady=10)
tk.Label(about_frame, text="이 도구는 던전앤파이터 모바일의 스크립트를 합치고 비교하는 기능을 제공합니다.").pack(pady=10)
tk.Label(about_frame, text="Made by 청두헌터즈").pack(pady=10)
gall_label = tk.Label(about_frame, text=r"던전앤파이터 M 갤러리로 가기", fg="blue", cursor="hand2", font="Helvetica 10 underline")
gall_label.pack(pady=10)
gall_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://gall.dcinside.com/mgallery/board/lists?id=dnfm"))

# Run
root.mainloop()