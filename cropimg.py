from PIL import Image
import os

def crop_images(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith((".png", ".jpg", ".jpeg")):  # 检查文件是否是图片
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)
            
            # 获取图片尺寸
            width, height = img.size
            
            # 计算左下四分之一的区域
            left = 0
            top = height / 2
            right = width / 2
            bottom = height
            
            # 裁剪图片
            img_cropped = img.crop((left, top, right, bottom))
            
            # 保存裁剪后的图片
            output_path = os.path.join(output_folder, filename)
            img_cropped.save(output_path)
    
    print("All images have been cropped and saved.")

# 使用示例
input_folder = '05_22_2024_test_crop/output_05222024rightdown'
output_folder = '05_22_2024_test_crop/output_05222024rightdown_crop'
crop_images(input_folder, output_folder)
