import os
import json
import base64
import cv2

def read_txt_file(txt_file):
    with open(txt_file, 'r') as f:
        lines = f.readlines()
    data = []
    for line in lines:
        line = line.strip().split()
        class_name = line[0]
        bbox = [coord for coord in line[1:]]
        data.append({'class_name': class_name, 'bbox': bbox})
    return data

def convert_to_labelme(data, image_path, image_size):
    labelme_data = {
        'version': '4.5.6',
        'flags': {},
        'shapes': [],
        'imagePath': image_path.split(os.sep)[-1],  # Ensure cross-platform compatibility
        'imageData': None,
        'imageHeight': image_size[0],
        'imageWidth': image_size[1]
    }
    for obj in data:
        dx, dy, dw, dh = map(float, obj['bbox'])

        w = dw * image_size[1]
        h = dh * image_size[0]
        center_x = dx * image_size[1]
        center_y = dy * image_size[0]
        x1 = center_x - w/2
        y1 = center_y - h/2
        x2 = center_x + w/2
        y2 = center_y + h/2

        label = 'grape' if obj['class_name'] == '0' else obj['class_name']
        shape_data = {
            'label': label,
            'points': [[x1, y1], [x2, y2]],
            'group_id': None,
            'shape_type': 'rectangle',
            'flags': {}
        }
        labelme_data['shapes'].append(shape_data)
    return labelme_data

def save_labelme_json(labelme_data, image_path, output_file):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    labelme_data['imageData'] = base64.b64encode(image_data).decode('utf-8')

    with open(output_file, 'w') as f:
        json.dump(labelme_data, f, indent=4)

# 指定单个txt文件和图片路径
txt_file = '05202024_rightdown_1st2row/330.txt'
image_file = '05202024_rightdown_1st2row/330.png'
output_file = '05202024_rightdown_1st2row/330.json'

# 读取txt文件
data = read_txt_file(txt_file)

# 获取图片尺寸
image_size = cv2.imread(image_file).shape  # (height, width, channels)

# 转化为LabelMe格式
labelme_data = convert_to_labelme(data, image_file, image_size)

# 保存为LabelMe JSON文件
save_labelme_json(labelme_data, image_file, output_file)
