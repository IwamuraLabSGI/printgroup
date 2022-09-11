import os


def list_img_paths_in_dir(dir_path: str) -> list:
    files_and_dirs = os.listdir(dir_path)
    files = [item for item in files_and_dirs if os.path.isfile(os.path.join(dir_path, item))]
    target_file_paths = list(map(lambda item: os.path.join(dir_path, item), files))
    target_file_paths = list(filter(
        lambda item: item.endswith('.png') or item.endswith('.jpg') or item.endswith('.JPG'),
        target_file_paths
    ))
    return target_file_paths
