import os
import json

def class_name_to_id(class_name):
    # 映射类别名称到YOLO的类别索引
    class_mapping = {
        'trunk': 0,
        # 添加更多类别和对应的索引
    }
    return class_mapping.get(class_name, -1)  # 如果类别未定义，返回-1

def json_to_yolo(json_file_path, yolo_file_path, image_width, image_height):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    yolo_labels = []
    for shape in data['shapes']:
        if shape['shape_type'] == 'rectangle':
            class_id = class_name_to_id(shape['label'])
            x1, y1 = shape['points'][0]
            x2, y2 = shape['points'][1]

            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2
            width = x2 - x1
            height = y2 - y1

            x_center /= image_width
            y_center /= image_height
            width /= image_width
            height /= image_height

            yolo_label = f"{class_id} {x_center} {y_center} {width} {height}"
            yolo_labels.append(yolo_label)

    with open(yolo_file_path, 'w') as yolo_file:
        for label in yolo_labels:
            yolo_file.write(label + "\n")

# 遍历文件夹并处理每个JSON文件
json_folder = 'trainingdata2/valid/newjson'  # JSON文件所在的文件夹路径
yolo_folder = 'trainingdata2/valid/newlab'  # YOLO输出文件夹路径
image_width, image_height = 240, 320  # 图片尺寸

if not os.path.exists(yolo_folder):
    os.makedirs(yolo_folder)

for json_filename in os.listdir(json_folder):
    if json_filename.endswith('.json'):
        json_file_path = os.path.join(json_folder, json_filename)
        yolo_filename = os.path.splitext(json_filename)[0] + '.txt'
        yolo_file_path = os.path.join(yolo_folder, yolo_filename)

        json_to_yolo(json_file_path, yolo_file_path, image_width, image_height)
