import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import webbrowser

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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

# Create the GUI window
root = tk.Tk()
root.title("던파 모바일 스크립트 합체기")
root.geometry("640x320")
# root.iconbitmap('assets/icon/script.ico')

# Input folder label and button
input_folder_var = tk.StringVar()
tk.Label(root, text=r"스크립트가 있는 폴더를 찾아 선택해주세요.").pack(pady=10)
tk.Label(root, text=r"(보통은 C:\Program Files\Nexon\DNFM\DNFM_Data\StreamingAssets\bundles)").pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)
tk.Entry(frame, textvariable=input_folder_var, width=70).pack(side=tk.LEFT, padx=10)
tk.Button(frame, text="탐색", command=select_directory).pack(side=tk.LEFT)

# Run button to start the file combination
tk.Button(root, text="파일 합체", command=run_combination).pack(pady=10)

tk.Label(root, text=r"합쳐진 스크립트는 Visual Studio Code를 설치하여 열람하세요").pack(pady=10)
download_label=tk.Label(root, text=r"다운로드: https://code.visualstudio.com/", fg="blue", cursor="hand2", font="Helvetica 10 underline")
download_label.pack(pady=10)
download_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://code.visualstudio.com/"))
tk.Label(root, text=r"Made by 청두헌터즈").pack(pady=10)

# Run the GUI loop
root.mainloop()