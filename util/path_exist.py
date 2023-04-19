import os


# 查看是否存在该文件路径，不存在则创建
def path_exists_or_create(file_path):
    if not os.path.exists(file_path):
        print("【util/str_utils/path_exist.py】不存在该路径   ", file_path)
        os.makedirs(file_path)
    print("【util/str_utils/path_exist.py】已有该路径   ", file_path)


