import os

# 设置文件夹路径
label_folder_path = 'trainingdata2/valid/labels'
new_label_folder_path = 'trainingdata2/valid/newlab'

# 原始图像和裁剪后图像的尺寸
original_width = 480
original_height = 640
cropped_width = 240
cropped_height = 320

# 创建新的标签文件夹，如果不存在
if not os.path.exists(new_label_folder_path):
    os.makedirs(new_label_folder_path)

# 获取文件夹中的所有txt文件
label_files = [f for f in os.listdir(label_folder_path) if f.endswith('.txt')]

for label_file in label_files:
    # 读取原始标签文件
    with open(os.path.join(label_folder_path, label_file), 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 5:
            continue
        
        class_id, x_center, y_center, width, height = parts
        x_center = float(x_center)
        y_center = float(y_center)
        width = float(width)
        height = float(height)

        # 转换为原始图像中的像素坐标
        x_center_pixel = x_center * original_width
        y_center_pixel = y_center * original_height
        width_pixel = width * original_width
        height_pixel = height * original_height

        x_min = x_center_pixel - (width_pixel/2)
        y_min = y_center_pixel - (height_pixel/2)
        x_max = x_center_pixel + (width_pixel/2)
        y_max = y_center_pixel + (height_pixel/2)

        if x_min >= 240:
            continue

        elif x_min < 240 and y_min>=320:
            if x_max<240:
                new_x_min = x_min
                new_x_max = x_max
                new_y_min = y_min - 320
                new_y_max = y_max - 320
            elif x_max>=240:
                new_x_min = x_min
                new_x_max = 240
                new_y_min = y_min - 320
                new_y_max = y_max - 320
        elif x_min < 240 and y_min <320:
            if x_max < 240 and y_max >= 320:
                new_x_min = x_min
                new_x_max = x_max
                new_y_min = 0
                new_y_max = y_max - 320
            elif x_max < 240 and y_max < 320:
                continue
            elif x_max > 240 and y_max > 320:
                new_x_min = x_min
                new_x_max = 240
                new_y_min = 0
                new_y_max = y_max - 320
            elif x_max > 240 and y_max < 320:
                continue

        new_x_center_pixel = (new_x_min + new_x_max) / 2
        new_y_center_pixel = (new_y_min + new_y_max) / 2
        new_width_pixel = new_x_max - new_x_min
        new_height_pixel = new_y_max - new_y_min


        # 转换为新的图像比例坐标
        new_x_center = new_x_center_pixel / cropped_width
        new_y_center = new_y_center_pixel / cropped_height
        new_width = width_pixel / cropped_width
        new_height = height_pixel / cropped_height

        # 添加新的标签行
        new_lines.append(f"{class_id} {new_x_center} {new_y_center} {new_width} {new_height}\n")

    # 写入新的标签文件
    new_label_file_path = os.path.join(new_label_folder_path, label_file)
    with open(new_label_file_path, 'w') as file:
        file.writelines(new_lines)
    

print("标签文件修改完成")
