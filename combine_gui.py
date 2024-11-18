import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Combine script files
def combine_script_files(directory, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8', errors='ignore') as outfile:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.startswith('script_'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                                content = infile.read()
                                outfile.write(f"--- Start of {file} ---\n")
                                outfile.write(content)
                                outfile.write(f"\n--- End of {file} ---\n\n")
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

# Function to select output file
def select_output_file():
    output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if output_file:
        output_file_var.set(output_file)

# Function to run the file combination process
def run_combination():
    input_folder = input_folder_var.get()
    output_file = output_file_var.get()

    if not input_folder or not os.path.isdir(input_folder):
        messagebox.showerror("Error", "올바른 스크립트가 있는 경로를 선택하세요.")
        return
    if not output_file:
        messagebox.showerror("Error", "올바른 출력 경로를 선택하세요.")
        return

    combine_script_files(input_folder, output_file)

# Create the GUI window
root = tk.Tk()
root.title("던파 모바일 스크립트 합체기 by 청두헌터즈")
root.geometry("640x360")

# Input folder label and button
input_folder_var = tk.StringVar()
tk.Label(root, text=r"스크립트가 있는 폴더:").pack(pady=5)
tk.Label(root, text=r"(보통은 C:\Program Files\Nexon\DNFM\DNFM_Data\StreamingAssets\bundles)").pack(pady=5)
tk.Entry(root, textvariable=input_folder_var, width=50).pack(pady=5)
tk.Button(root, text="탐색", command=select_directory).pack(pady=5)

# Output file label and button
output_file_var = tk.StringVar()
tk.Label(root, text="통합 스크립트를 저장할 폴더 및 스크립트 이름 지정 (원하는 곳, 원하는 이름):").pack(pady=5)
tk.Entry(root, textvariable=output_file_var, width=50).pack(pady=5)
tk.Button(root, text="탐색", command=select_output_file).pack(pady=5)

# Run button to start the file combination
tk.Button(root, text="파일 합체", command=run_combination).pack(pady=20)

# Run the GUI loop
root.mainloop()
