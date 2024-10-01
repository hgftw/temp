import os
from PIL import Image

def rotate_images_in_folder(folder_path):
    # 获取文件夹中的所有文件
    file_list = os.listdir(folder_path)

    # 循环处理每个文件
    for file_name in file_list:
        # 检查文件是否是图像文件
        if file_name.endswith('.jpg') or file_name.endswith('.png'):
            # 拼接文件的完整路径
            file_path = os.path.join(folder_path, file_name)

            # 打开图像文件
            image = Image.open(file_path)

            # 将图像旋转180度
            rotated_image = image.rotate(180)

            # 保存旋转后的图像
            rotated_image.save(file_path)

            print(f"旋转并保存文件: {file_name}")

# 指定要处理的文件夹路径
folder_path = '05_22_2024_test/output_05222024rightup/'  

# 调用函数批量处理图像
rotate_images_in_folder(folder_path)



