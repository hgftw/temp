import os

# 设置文件夹的路径
folder_path = '05202024_rightdown_2nd4row_image'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 检查文件名是否符合修改条件
    if not filename.startswith("05202024_rightdown_2nd4row_"):
        # 原文件的完整路径
        old_file = os.path.join(folder_path, filename)
        # 新文件名
        new_filename = "05202024_rightdown_2nd4row_" + filename
        # 新文件的完整路径
        new_file = os.path.join(folder_path, new_filename)
        # 重命名文件
        os.rename(old_file, new_file)
        print(f"Renamed '{old_file}' to '{new_file}'")
