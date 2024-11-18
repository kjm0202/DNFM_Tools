import os
import shutil

def get_files_in_directory(directory):
    try:
        return os.listdir(directory)
    except Exception as e:
        print(f"Could not read directory {directory}: {e}")
        return []

def get_base_file_name(file_name):
    # 파일명에서 # 이전 부분만 추출하고, 띄어쓰기를 모두 제거하여 반환
    return file_name.split('#')[0].replace(" ", "") if '#' in file_name else file_name.replace(" ", "")

def find_unique_files(src_directory, dst_directory):
    # 첫 번째 및 두 번째 경로의 파일명 목록을 가져옴
    src_files = get_files_in_directory(src_directory)
    dst_files = get_files_in_directory(dst_directory)

    # 각 디렉토리의 파일명에서 # 이전 부분만 추출한 후 집합으로 변환
    src_base_files = {get_base_file_name(file) for file in src_files}
    dst_base_files = {get_base_file_name(file) for file in dst_files}

    # 두 번째 경로에는 있지만 첫 번째 경로에는 없는 파일명을 찾음
    unique_files = dst_base_files - src_base_files

    # 실제 파일명을 추출하여 반환
    return [file for file in dst_files if get_base_file_name(file) in unique_files]

def copy_unique_files_to_directory(unique_files, src_directory, output_directory):
    # 복사할 경로가 존재하지 않으면 생성
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 고유 파일들을 출력 디렉토리로 복사
    for file in unique_files:
        src_file_path = os.path.join(src_directory, file)
        dst_file_path = os.path.join(output_directory, file)

        try:
            shutil.copy2(src_file_path, dst_file_path)
            print(f"Copied {file} to {output_directory}")
        except Exception as e:
            print(f"Could not copy {file} to {output_directory}: {e}")

# 디렉토리 경로
src_directory = r'C:\Users\kjm19\Documents\AssetStudio.net472_v0.16.53\exported_240808\Sprite'
dst_directory = r'C:\Users\kjm19\Documents\AssetStudio.net472_v0.16.53\exported_240822\Sprite'
output_directory = r'C:\Users\kjm19\Documents\cmp'

# 고유 파일을 찾음
unique_files = find_unique_files(src_directory, dst_directory)

# 고유 파일을 복사
if unique_files:
    print(f"Found {len(unique_files)} unique files. Copying to {output_directory}...")
    copy_unique_files_to_directory(unique_files, dst_directory, output_directory)
else:
    print("No unique files found in the second folder.")
