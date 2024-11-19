import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pathlib import Path
import webbrowser

# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#
#     return os.path.join(base_path, relative_path)

# Combine script files
def combine_script_files(directory, output_file):
    try:
        script_files = [os.path.join(root, file) for root, dirs, files in os.walk(directory) for file in files if
                        file.startswith('script_')]

        if not script_files:
            messagebox.showerror("스크립트 발견 불가", "선택한 경로에서 스크립트 파일을 찾을 수 없습니다.")
            return

        with open(output_file, 'w', encoding='utf-8', errors='ignore') as outfile:
            for file_path in script_files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                        content = infile.read()
                        outfile.write(f"--- Start of {os.path.basename(file_path)} ---\n")
                        outfile.write(content)
                        outfile.write(f"\n--- End of {os.path.basename(file_path)} ---\n\n")
                except Exception as e:
                    print(f"Could not read file {file_path}: {e}")
        messagebox.showinfo("석섹스", f"다음 파일명으로 성공적으로 합쳐졌습니다: {output_file}")
    except Exception as e:
        messagebox.showerror("오류", f"합체에 실패했습니다: {e}")

# Function to select directory
def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        input_folder_var.set(directory)

# Function to run the file combination process
def run_combination():
    input_folder = input_folder_var.get()
    output_file = str(Path.home() / "Downloads" / "merged_dnfm_scripts.txt")

    if not input_folder or not os.path.isdir(input_folder):
        messagebox.showerror("잘못된 경로", "올바른 스크립트가 있는 경로를 선택하세요.")
        return

    combine_script_files(input_folder, output_file)

# Read file ignoring errors
def read_file_ignore_errors(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Could not read file {file_path}: {e}")
        return ""

# Get unique content
def get_unique_content(file1_content, file2_content):
    file1_lines = set(file1_content.splitlines())
    file2_lines = set(file2_content.splitlines())

    # Find lines that are in file2 but not in file1
    unique_lines = file2_lines - file1_lines
    return "\n".join(unique_lines)

# Select file 1
def select_file1():
    file_path = filedialog.askopenfilename()
    if file_path:
        file1_var.set(file_path)

# Select file 2
def select_file2():
    file_path = filedialog.askopenfilename()
    if file_path:
        file2_var.set(file_path)

# Run comparison
def run_comparison():
    file1_path = file1_var.get()
    file2_path = file2_var.get()
    output_path = str(Path.home() / "Downloads" / "unique_contents_in_new_script.txt")

    if not file1_path or not os.path.isfile(file1_path):
        messagebox.showerror("선택 안 됨", "유효한 구버전 스크립트를 선택하세요.")
        return

    if not file2_path or not os.path.isfile(file2_path):
        messagebox.showerror("선택 안 됨", "유효한 신버전 스크립트를 선택하세요.")
        return

    file1_content = read_file_ignore_errors(file1_path)
    file2_content = read_file_ignore_errors(file2_path)
    unique_content = get_unique_content(file1_content, file2_content)

    try:
        with open(output_path, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(unique_content)
        messagebox.showinfo("Success", f"{output_path} 파일 저장 완료")
    except Exception as e:
        messagebox.showerror("Error", f"{output_path}에 파일을 저장할 수 없습니다: {e}")

# Create the main GUI window
root = tk.Tk()
root.title("스크립트 도구")
root.geometry("640x320")

# Create a notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Create the combine tab
combine_frame = ttk.Frame(notebook)
notebook.add(combine_frame, text="합체")

# Create the compare tab
compare_frame = ttk.Frame(notebook)
notebook.add(compare_frame, text="비교(베타)")

# Create the about tab
about_frame = ttk.Frame(notebook)
notebook.add(about_frame, text="정보")

# Combine tab UI elements
input_folder_var = tk.StringVar()
tk.Label(combine_frame, text=r"스크립트가 있는 폴더를 찾아 선택해주세요.").pack(pady=10)
tk.Label(combine_frame, text=r"(보통은 C:\Program Files\Nexon\DNFM\DNFM_Data\StreamingAssets\bundles)").pack(pady=10)

frame = tk.Frame(combine_frame)
frame.pack(pady=10)
tk.Entry(frame, textvariable=input_folder_var, width=60).pack(side=tk.LEFT, padx=10)
tk.Button(frame, text="탐색", command=select_directory).pack(side=tk.LEFT)

tk.Button(combine_frame, text="파일 합체", command=run_combination).pack(pady=10)

tk.Label(combine_frame, text=r"합쳐진 스크립트는 Visual Studio Code를 설치하여 열람하세요").pack(pady=10)
download_label = tk.Label(combine_frame, text=r"다운로드: https://code.visualstudio.com/", fg="blue", cursor="hand2", font="Helvetica 10 underline")
download_label.pack(pady=10)
download_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://code.visualstudio.com/"))

# Compare tab UI elements
file1_var = tk.StringVar()
file2_var = tk.StringVar()

tk.Label(compare_frame, text="구버전의 통합 스크립트 파일을 선택하세요: ").pack(pady=5)
frame1 = tk.Frame(compare_frame)
frame1.pack(pady=5)
tk.Entry(frame1, textvariable=file1_var, width=60).pack(side=tk.LEFT, padx=5)
tk.Button(frame1, text="탐색", command=select_file1).pack(side=tk.LEFT)

tk.Label(compare_frame, text="신버전의 통합 스크립트 파일을 선택하세요: ").pack(pady=5)
frame2 = tk.Frame(compare_frame)
frame2.pack(pady=5)
tk.Entry(frame2, textvariable=file2_var, width=60).pack(side=tk.LEFT, padx=5)
tk.Button(frame2, text="탐색", command=select_file2).pack(side=tk.LEFT)

tk.Button(compare_frame, text="추가된 문구 찾기", command=run_comparison).pack(pady=20)

# About tab UI elements
tk.Label(about_frame, text="스크립트 도구 v0.1").pack(pady=10)
tk.Label(about_frame, text="이 도구는 던전앤파이터 모바일의 스크립트를 합치고 비교하는 기능을 제공합니다.").pack(pady=10)
tk.Label(about_frame, text="Made by 청두헌터즈").pack(pady=10)
gall_label = tk.Label(about_frame, text=r"던전앤파이터 M 갤러리로 가기", fg="blue", cursor="hand2", font="Helvetica 10 underline")
gall_label.pack(pady=10)
gall_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://gall.dcinside.com/mgallery/board/lists?id=dnfm"))

# Run the GUI loop
root.mainloop()