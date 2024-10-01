def class_name_to_id(class_name):
    # 创建一个字典来映射类别名称到YOLO的类别索引
    class_mapping = {
        'trunk': 0,  # 假设'trunk'是类别0
        # 添加更多类别和对应的索引
        'leaf': 1,
        'fruit': 2
    }
    return class_mapping.get(class_name, -1)  # 如果类别未定义，返回-1

import json

def json_to_yolo(json_file_path, yolo_file_path, image_width, image_height):
    # 读取JSON文件
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    # 创建一个列表，用于存放YOLO格式的标签
    yolo_labels = []

    # 遍历JSON中的每个形状
    for shape in data['shapes']:
        if shape['shape_type'] == 'rectangle':
            # 获取类别名称并转换为YOLO类别索引
            class_id = class_name_to_id(shape['label'])

            # 获取边界框坐标
            x1, y1 = shape['points'][0]
            x2, y2 = shape['points'][1]

            # 计算中心点和宽高
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2
            width = x2 - x1
            height = y2 - y1

            # 归一化坐标
            x_center /= image_width
            y_center /= image_height
            width /= image_width
            height /= image_height

            # 格式化为YOLO格式并添加到列表
            yolo_label = f"{class_id} {x_center} {y_center} {width} {height}"
            yolo_labels.append(yolo_label)

    # 写入YOLO格式的文件
    with open(yolo_file_path, 'w') as yolo_file:
        for label in yolo_labels:
            yolo_file.write(label + "\n")

# 示例调用
json_to_yolo('right12imagejson/327.json', '327.txt', 480, 640)
