import os
import shutil
from datetime import datetime
import customtkinter as ctk

# Fluent Design Colors
FLUENT_COLORS = {
    "primary": "#0078D4",  # Microsoft Blue
    "primary_hover": "#106EBE",
    "primary_pressed": "#005A9E",
    "background": "#FFFFFF",
    "surface": "#F5F5F5",
    "border": "#E1E1E1",
    "text": "#323130",
    "text_secondary": "#605E5C"
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


class SpriteCompareTool(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Sprite Compare Tool")
        self.geometry("640x400")
        self.configure(fg_color=FLUENT_COLORS["background"])

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Sprite 비교 도구",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=FLUENT_COLORS["text"]
        )
        title_label.grid(row=0, column=0, padx=24, pady=(24, 16), sticky="w")

        # Old directory section
        old_dir_label = ctk.CTkLabel(
            self,
            text="구버전 Sprite 디렉토리",
            font=ctk.CTkFont(size=14),
            text_color=FLUENT_COLORS["text"]
        )
        old_dir_label.grid(row=1, column=0, padx=24, pady=(0, 8), sticky="w")

        old_dir_frame = FluentFrame(self)
        old_dir_frame.grid(row=2, column=0, padx=24, pady=(0, 16), sticky="ew")
        old_dir_frame.grid_columnconfigure(0, weight=1)

        self.old_dir_var = FluentEntry(
            old_dir_frame,
            placeholder_text="디렉토리를 선택하세요"
        )
        self.old_dir_var.grid(row=0, column=0, padx=(8, 8), pady=8, sticky="ew")

        old_browse_button = FluentButton(
            old_dir_frame,
            text="탐색",
            width=100,
            command=self.select_old_directory
        )
        old_browse_button.grid(row=0, column=1, padx=(0, 8), pady=8)

        # New directory section
        new_dir_label = ctk.CTkLabel(
            self,
            text="신버전 Sprite 디렉토리",
            font=ctk.CTkFont(size=14),
            text_color=FLUENT_COLORS["text"]
        )
        new_dir_label.grid(row=3, column=0, padx=24, pady=(0, 8), sticky="w")

        new_dir_frame = FluentFrame(self)
        new_dir_frame.grid(row=4, column=0, padx=24, pady=(0, 16), sticky="ew")
        new_dir_frame.grid_columnconfigure(0, weight=1)

        self.new_dir_var = FluentEntry(
            new_dir_frame,
            placeholder_text="디렉토리를 선택하세요"
        )
        self.new_dir_var.grid(row=0, column=0, padx=(8, 8), pady=8, sticky="ew")

        new_browse_button = FluentButton(
            new_dir_frame,
            text="탐색",
            width=100,
            command=self.select_new_directory
        )
        new_browse_button.grid(row=0, column=1, padx=(0, 8), pady=8)

        # Compare button
        compare_button = FluentButton(
            self,
            text="추가된 Sprite 파일 찾기",
            command=self.run_comparison,
            primary=True
        )
        compare_button.grid(row=5, column=0, padx=24, pady=(8, 24), sticky="ew")

    def select_old_directory(self):
        directory = ctk.filedialog.askdirectory(title="구버전 Sprite 디렉토리 선택")
        if directory:
            self.old_dir_var.delete(0, 'end')
            self.old_dir_var.insert(0, directory)

    def select_new_directory(self):
        directory = ctk.filedialog.askdirectory(title="신버전 Sprite 디렉토리 선택")
        if directory:
            self.new_dir_var.delete(0, 'end')
            self.new_dir_var.insert(0, directory)

    def run_comparison(self):
        old_directory = self.old_dir_var.get()
        new_directory = self.new_dir_var.get()

        if not old_directory or not new_directory:
            self.show_message("입력 오류", "두 디렉토리를 모두 선택해주세요.", "warning")
            return

        unique_files = find_unique_files(old_directory, new_directory)

        if unique_files:
            today = datetime.now().strftime('%y%m%d')
            output_directory = os.path.join(os.path.expanduser('~'), 'Downloads', f'unique_sprites_{today}')
            copy_unique_files_to_directory(unique_files, new_directory, output_directory)
            self.show_message("완료", f"{len(unique_files)}개의 새로운 파일을 찾았습니다.\n저장 위치: {output_directory}")
        else:
            self.show_message("알림", "새로운 파일을 찾지 못했습니다.", "info")

    def show_message(self, title, message, message_type="info"):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.grab_set()  # Make the dialog modal

        # Center the dialog on the main window
        dialog.geometry(f"+{self.winfo_x() + 120}+{self.winfo_y() + 100}")

        frame = FluentFrame(dialog)
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        message_label = ctk.CTkLabel(
            frame,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=350
        )
        message_label.pack(pady=(20, 30))

        ok_button = FluentButton(
            frame,
            text="확인",
            command=dialog.destroy,
            primary=True,
            width=100
        )
        ok_button.pack(pady=(0, 20))


def get_files_in_directory(directory):
    try:
        return os.listdir(directory)
    except Exception as e:
        print(f"Could not read directory {directory}: {e}")
        return []


def get_base_file_name(file_name):
    return file_name.split('#')[0].replace(" ", "") if '#' in file_name else file_name.replace(" ", "")


def find_unique_files(old_directory, new_directory):
    old_files = get_files_in_directory(old_directory)
    new_files = get_files_in_directory(new_directory)
    old_base_files = {get_base_file_name(file) for file in old_files}
    new_base_files = {get_base_file_name(file) for file in new_files}
    unique_files = new_base_files - old_base_files
    return [file for file in new_files if get_base_file_name(file) in unique_files]


def copy_unique_files_to_directory(unique_files, old_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for file in unique_files:
        old_file_path = os.path.join(old_directory, file)
        new_file_path = os.path.join(output_directory, file)
        try:
            shutil.copy2(old_file_path, new_file_path)
            print(f"Copied {file} to {output_directory}")
        except Exception as e:
            print(f"Could not copy {file} to {output_directory}: {e}")


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = SpriteCompareTool()
    app.mainloop()