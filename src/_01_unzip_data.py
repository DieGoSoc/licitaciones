import os
import zipfile


def unzip_data(folder, unziped_files_folder):
    if not os.path.exists(folder):
        print(f'The folder named {folder} does not exist')
    if not os.path.exists(unziped_files_folder):
        os.makedirs(unziped_files_folder)
    files = os.listdir(folder)
    for file in files:
        file_path = os.path.join(folder, file)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(unziped_files_folder))
