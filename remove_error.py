import os

# 指定要处理的文件夹路径
folder_path = 'trainingdata_crop/test/labels'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # if filename.endswith(".jpg"):
    if filename.endswith(".txt"):
        # 查找第一个png之前的内容
        new_name = filename.split('_png')[0] + ".txt"
        
        # 获取旧文件的完整路径
        old_file = os.path.join(folder_path, filename)
        
        # 获取新文件的完整路径
        new_file = os.path.join(folder_path, new_name)
        
        # 重命名文件
        os.rename(old_file, new_file)
        print(f'Renamed: {old_file} to {new_file}')
