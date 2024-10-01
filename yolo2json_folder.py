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
        'imagePath': json_image_path,
        'imageData': None,
        'imageHeight': image_size[0],
        'imageWidth': image_size[1]
    }
    for obj in data:
        dx = obj['bbox'][0]
        dy = obj['bbox'][1]
        dw = obj['bbox'][2]
        dh = obj['bbox'][3]

        w = eval(dw) * image_size[1]
        h = eval(dh) * image_size[0]
        center_x = eval(dx) * image_size[1]
        center_y = eval(dy) * image_size[0]
        x1 = center_x - w/2
        y1 = center_y - h/2
        x2 = center_x + w/2
        y2 = center_y + h/2

        if obj['class_name'] == '0': #判断对应的标签名称，写入json文件中
            label = str('trunk')
        else:
            label = obj['class_name']
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

# 设置文件夹路径和输出文件夹路径
txt_folder = 'trainingdata2/valid/newlab'  # 存放LabelImg标注的txt文件的文件夹路径
output_folder = 'trainingdata2/valid/newjson'  # 输出LabelMe标注的json文件的文件夹路径
img_folder = 'trainingdata2/valid/newimg'  #存放对应标签的图片文件夹路径

# 创建输出文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历txt文件夹中的所有文件
for filename in os.listdir(txt_folder):
    if filename.endswith('.txt'):
        # 生成对应的输出文件名
        output_filename = os.path.splitext(filename)[0] + '.json'

        # 读取txt文件
        txt_file = os.path.join(txt_folder, filename)
        data = read_txt_file(txt_file)

        # 设置图片路径和尺寸
        image_filename = os.path.splitext(filename)[0] + '.png'  # 图片文件名与txt文件名相同，后缀为.jpg
        image_path = os.path.join(img_folder, image_filename)
        # image_size = (1280, 720)  # 根据实际情况修改
        json_image_path = image_path.split('\\')[-1]
        image_size = cv2.imread(image_path).shape

        # 转化为LabelMe格式
        labelme_data = convert_to_labelme(data, image_path, image_size)

        # 保存为LabelMe JSON文件
        output_file = os.path.join(output_folder, output_filename)
        save_labelme_json(labelme_data, image_path, output_file)
