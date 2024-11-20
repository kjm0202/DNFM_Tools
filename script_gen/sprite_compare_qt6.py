import os
import shutil
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox)
from PySide6.QtCore import QDateTime, Qt
from PySide6.QtGui import QFont, QIcon


class FluentButton(QPushButton):
    def __init__(self, text, parent=None, primary=False):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(36)
        self.setProperty("primary", primary)


class FluentLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(36)


class SpriteCompareTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
            }

            QLabel {
                font-size: 14px;
                color: #323130;
                padding: 4px 0;
            }

            FluentLineEdit {
                border: 1px solid #8a8886;
                border-radius: 4px;
                padding: 0 12px;
                background: #ffffff;
                font-size: 14px;
            }

            FluentLineEdit:focus {
                border: 1px solid #0078d4;
                background: #ffffff;
            }

            FluentLineEdit:hover {
                border: 1px solid #323130;
            }

            FluentButton {
                border: 1px solid #8a8886;
                border-radius: 4px;
                background-color: #ffffff;
                color: #323130;
                font-size: 14px;
                padding: 0 20px;
            }

            FluentButton:hover {
                background-color: #f3f2f1;
                border: 1px solid #323130;
            }

            FluentButton:pressed {
                background-color: #edebe9;
                border: 1px solid #323130;
            }

            FluentButton[primary="true"] {
                background-color: #0078d4;
                border: 1px solid #0078d4;
                color: #ffffff;
            }

            FluentButton[primary="true"]:hover {
                background-color: #106ebe;
                border: 1px solid #106ebe;
            }

            FluentButton[primary="true"]:pressed {
                background-color: #005a9e;
                border: 1px solid #005a9e;
            }
        """)

    def initUI(self):
        self.setWindowTitle("Sprite Compare Tool")
        self.setGeometry(100, 100, 640, 380)
        self.setContentsMargins(24, 24, 24, 24)

        layout = QVBoxLayout()
        layout.setSpacing(16)

        # Title
        title = QLabel("Sprite 비교 도구")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: 600;
            color: #323130;
            padding-bottom: 12px;
        """)
        layout.addWidget(title)

        # Old directory section
        layout.addWidget(QLabel("구버전 Sprite 디렉토리"))
        old_dir_layout = QHBoxLayout()
        old_dir_layout.setSpacing(8)

        self.old_dir_var = FluentLineEdit(self)
        self.old_dir_var.setPlaceholderText("디렉토리를 선택하세요")
        old_dir_layout.addWidget(self.old_dir_var)

        old_browse_button = FluentButton("탐색", self)
        old_browse_button.clicked.connect(self.select_old_directory)
        old_browse_button.setFixedWidth(100)
        old_dir_layout.addWidget(old_browse_button)

        layout.addLayout(old_dir_layout)

        # New directory section
        layout.addWidget(QLabel("신버전 Sprite 디렉토리"))
        new_dir_layout = QHBoxLayout()
        new_dir_layout.setSpacing(8)

        self.new_dir_var = FluentLineEdit(self)
        self.new_dir_var.setPlaceholderText("디렉토리를 선택하세요")
        new_dir_layout.addWidget(self.new_dir_var)

        new_browse_button = FluentButton("탐색", self)
        new_browse_button.clicked.connect(self.select_new_directory)
        new_browse_button.setFixedWidth(100)
        new_dir_layout.addWidget(new_browse_button)

        layout.addLayout(new_dir_layout)

        # Add some spacing before the compare button
        layout.addSpacing(8)

        # Compare button
        compare_button = FluentButton("추가된 Sprite 파일 찾기", self, primary=True)
        compare_button.clicked.connect(self.run_comparison)
        layout.addWidget(compare_button)

        # Add stretch to push everything to the top
        layout.addStretch()

        self.setLayout(layout)

    def select_old_directory(self):
        old_directory = QFileDialog.getExistingDirectory(self, "구버전 Sprite 디렉토리 선택")
        if old_directory:
            self.old_dir_var.setText(old_directory)

    def select_new_directory(self):
        new_directory = QFileDialog.getExistingDirectory(self, "신버전 Sprite 디렉토리 선택")
        if new_directory:
            self.new_dir_var.setText(new_directory)

    def run_comparison(self):
        old_directory = self.old_dir_var.text()
        new_directory = self.new_dir_var.text()

        if not old_directory or not new_directory:
            QMessageBox.warning(
                self,
                "입력 오류",
                "두 디렉토리를 모두 선택해주세요.",
                QMessageBox.Ok
            )
            return

        unique_files = find_unique_files(old_directory, new_directory)

        if unique_files:
            today = QDateTime.currentDateTime().toString('yyMMdd')
            output_directory = os.path.join(os.path.expanduser('~'), 'Downloads', f'unique_sprites_{today}')
            copy_unique_files_to_directory(unique_files, new_directory, output_directory)
            QMessageBox.information(
                self,
                "완료",
                f"{len(unique_files)}개의 새로운 파일을 찾았습니다.\n저장 위치: {output_directory}",
                QMessageBox.Ok
            )
        else:
            QMessageBox.information(
                self,
                "알림",
                "새로운 파일을 찾지 못했습니다.",
                QMessageBox.Ok
            )


# Keep the original helper functions
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


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')  # Use Fusion style as base
    ex = SpriteCompareTool()
    ex.show()
    app.exec()