import customtkinter as ctk
import os
import sys
from tkinter import filedialog, messagebox
from pathlib import Path
import webbrowser

# Fluent Design Colors
FLUENT_COLORS = {
    "primary": "#0078D4",  # Microsoft Blue
    "primary_hover": "#106EBE",
    "primary_pressed": "#005A9E",
    "background": "#FFFFFF",
    "surface": "#F5F5F5",
    "border": "#E1E1E1",
    "text": "#323130",
    "text_secondary": "#FFFFFF"
}

class FluentFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            fg_color=FLUENT_COLORS["background"],
            corner_radius=8,
            border_width=1,
            border_color=FLUENT_COLORS["border"]
        )

class FluentButton(ctk.CTkButton):
    def __init__(self, *args, primary=False, **kwargs):
        colors = {
            "fg_color": FLUENT_COLORS["primary"] if primary else "transparent",
            "text_color": "#FFFFFF" if primary else FLUENT_COLORS["text"],
            "hover_color": FLUENT_COLORS["primary_hover"] if primary else "#F5F5F5",
            "border_color": FLUENT_COLORS["primary"] if primary else FLUENT_COLORS["border"],
        }
        super().__init__(
            *args,
            **colors,
            border_width=1 if not primary else 0,
            corner_radius=4,
            height=36,
            **kwargs
        )

class FluentEntry(ctk.CTkEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            fg_color=FLUENT_COLORS["background"],
            border_color=FLUENT_COLORS["border"],
            text_color=FLUENT_COLORS["text"],
            corner_radius=4,
            height=36,
            **kwargs
        )

class FluentTabView(ctk.CTkTabview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            fg_color=FLUENT_COLORS["background"],
            segmented_button_fg_color=FLUENT_COLORS["surface"],
            segmented_button_selected_color=FLUENT_COLORS["primary"],
            segmented_button_selected_hover_color=FLUENT_COLORS["primary_hover"],
            segmented_button_unselected_color=FLUENT_COLORS["surface"],
            segmented_button_unselected_hover_color=FLUENT_COLORS["border"]
        )

class FluentHyperlinkLabel(ctk.CTkLabel):
    def __init__(self, *args, url=None, **kwargs):
        super().__init__(
            *args,
            text_color=FLUENT_COLORS["primary"],
            font=ctk.CTkFont(size=12, underline=True),
            cursor="hand2",
            **kwargs
        )
        if url:
            self.bind("<Button-1>", lambda e: webbrowser.open_new(url))

class ScriptTool(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("스크립트 도구")
        self.geometry("700x500")
        self.configure(fg_color=FLUENT_COLORS["background"])

        # Initialize variables
        self.input_folder_var = ctk.StringVar()
        self.file1_var = ctk.StringVar()
        self.file2_var = ctk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Create tab view
        self.tabview = FluentTabView(self)
        self.tabview.pack(expand=True, fill="both", padx=20, pady=20)

        # Add tabs
        self.tabview.add("스크립트 합체")
        self.tabview.add("스크립트 비교(베타)")
        self.tabview.add("정보")

        # Configure tabs
        self.setup_combine_tab()
        self.setup_compare_tab()
        self.setup_about_tab()

    def setup_combine_tab(self):
        combine_frame = self.tabview.tab("스크립트 합체")

        # Main instructions
        ctk.CTkLabel(
            combine_frame,
            text="스크립트가 있는 폴더를 찾아 선택해주세요.",
            font=ctk.CTkFont(size=14),
            text_color=FLUENT_COLORS["text"]
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            combine_frame,
            text="(보통은 C:\\Program Files\\Nexon\\DNFM\\DNFM_Data\\StreamingAssets\\bundles)",
            font=ctk.CTkFont(size=12),
            text_color=FLUENT_COLORS["text_secondary"]
        ).pack(pady=(0, 0))

        # Directory selection frame
        dir_frame = FluentFrame(combine_frame)
        dir_frame.pack(fill="x", padx=20, pady=10)

        entry = FluentEntry(dir_frame, textvariable=self.input_folder_var, width=500)
        entry.pack(side="left", padx=(10, 10), pady=10)

        browse_btn = FluentButton(
            dir_frame,
            text="탐색",
            width=80,
            command=self.select_directory
        )
        browse_btn.pack(side="left", padx=(0, 10), pady=10)

        # Combine button
        FluentButton(
            combine_frame,
            text="파일 합체",
            command=self.run_combination,
            primary=True
        ).pack(pady=20)

        # VSCode instructions
        ctk.CTkLabel(
            combine_frame,
            text="합쳐진 스크립트는 Visual Studio Code를 설치하여 열람하세요",
            font=ctk.CTkFont(size=12),
            text_color=FLUENT_COLORS["text"]
        ).pack(pady=(20, 5))

        FluentHyperlinkLabel(
            combine_frame,
            text="다운로드: https://code.visualstudio.com/",
            url="https://code.visualstudio.com/"
        ).pack(pady=(0, 20))

    def setup_compare_tab(self):
        compare_frame = self.tabview.tab("스크립트 비교(베타)")

        # Old version file selection
        ctk.CTkLabel(
            compare_frame,
            text="구버전의 통합 스크립트 파일을 선택하세요:",
            font=ctk.CTkFont(size=14),
            text_color=FLUENT_COLORS["text"]
        ).pack(pady=(20, 5))

        old_frame = FluentFrame(compare_frame)
        old_frame.pack(fill="x", padx=20, pady=(0, 20))

        FluentEntry(
            old_frame,
            textvariable=self.file1_var,
            width=500
        ).pack(side="left", padx=(10, 10), pady=10)

        FluentButton(
            old_frame,
            text="탐색",
            width=80,
            command=self.select_file1
        ).pack(side="left", padx=(0, 10), pady=10)

        # New version file selection
        ctk.CTkLabel(
            compare_frame,
            text="신버전의 통합 스크립트 파일을 선택하세요:",
            font=ctk.CTkFont(size=14),
            text_color=FLUENT_COLORS["text"]
        ).pack(pady=(0, 5))

        new_frame = FluentFrame(compare_frame)
        new_frame.pack(fill="x", padx=20, pady=(0, 20))

        FluentEntry(
            new_frame,
            textvariable=self.file2_var,
            width=500
        ).pack(side="left", padx=(10, 10), pady=10)

        FluentButton(
            new_frame,
            text="탐색",
            width=80,
            command=self.select_file2
        ).pack(side="left", padx=(0, 10), pady=10)

        # Compare button
        FluentButton(
            compare_frame,
            text="추가된 문구 찾기",
            command=self.run_comparison,
            primary=True
        ).pack(pady=20)

    def setup_about_tab(self):
        about_frame = self.tabview.tab("정보")

        ctk.CTkLabel(
            about_frame,
            text="스크립트 도구 v0.1",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=FLUENT_COLORS["text"]
        ).pack(pady=(40, 20))

        ctk.CTkLabel(
            about_frame,
            text="이 도구는 던전앤파이터 모바일의 스크립트를 합치고 비교하는 기능을 제공합니다.",
            font=ctk.CTkFont(size=14),
            text_color=FLUENT_COLORS["text"]
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            about_frame,
            text="Made by 청두헌터즈",
            font=ctk.CTkFont(size=12),
            text_color=FLUENT_COLORS["text_secondary"]
        ).pack(pady=(0, 20))

        FluentHyperlinkLabel(
            about_frame,
            text="던전앤파이터 M 갤러리로 가기",
            url="https://gall.dcinside.com/mgallery/board/lists?id=dnfm"
        ).pack(pady=(0, 20))

    # Helper functions
    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.input_folder_var.set(directory)

    def select_file1(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file1_var.set(file_path)

    def select_file2(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file2_var.set(file_path)

    def run_combination(self):
        input_folder = self.input_folder_var.get()
        output_file = str(Path.home() / "Downloads" / "merged_dnfm_scripts.txt")

        if not input_folder or not os.path.isdir(input_folder):
            self.show_error("잘못된 경로", "올바른 스크립트가 있는 경로를 선택하세요.")
            return

        combine_script_files(input_folder, output_file)

    def run_comparison(self):
        file1_path = self.file1_var.get()
        file2_path = self.file2_var.get()
        output_path = str(Path.home() / "Downloads" / "unique_contents_in_new_script.txt")

        if not file1_path or not os.path.isfile(file1_path):
            self.show_error("선택 안 됨", "유효한 구버전 스크립트를 선택하세요.")
            return

        if not file2_path or not os.path.isfile(file2_path):
            self.show_error("선택 안 됨", "유효한 신버전 스크립트를 선택하세요.")
            return

        file1_content = read_file_ignore_errors(file1_path)
        file2_content = read_file_ignore_errors(file2_path)
        unique_content = get_unique_content(file1_content, file2_content)

        try:
            with open(output_path, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(unique_content)
            self.show_info("완료", f"{output_path} 파일 저장 완료")
        except Exception as e:
            self.show_error("오류", f"{output_path}에 파일을 저장할 수 없습니다: {e}")

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_info(self, title, message):
        messagebox.showinfo(title, message)

# Keep the original helper functions
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
        messagebox.showinfo("완료", f"다음 파일명으로 성공적으로 합쳐졌습니다: {output_file}")
    except Exception as e:
        messagebox.showerror("오류", f"합체에 실패했습니다: {e}")

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
    unique_lines = file2_lines - file1_lines
    return "\n".join(unique_lines)

if __name__ == "__main__":
    ctk.set_appearance_mode("system")  # 시스템 테마에 따라 자동으로 다크/라이트 모드 설정
    app = ScriptTool()
    app.mainloop()