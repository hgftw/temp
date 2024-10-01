import cv2
from ultralytics import YOLO
import torch
import os

# 初始化视频捕获
cap = cv2.VideoCapture('05222024rightdown_crop.mp4')
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# 初始化YOLO模型
model = YOLO("runs/detect/train5/weights/best.pt")  # 加载自定义模型

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
center_line = frame_width // 2

detection_count = 0
noobject_count = 0
flag = False

# 创建保存图像和标签的目录
output_image_folder = 'right_detected_images_own'
output_label_folder = 'right_detected_labels_own'
os.makedirs(output_image_folder, exist_ok=True)
os.makedirs(output_label_folder, exist_ok=True)

frame_number = 0  # 用于生成唯一的文件名

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video.")
        break

    frame_number += 1
    
    # 预测图像中的物体
    results = model.predict(source=frame, conf=0.3, stream=True)
    
    if results is None:
        print("No results from model prediction.")
        continue

    for result in results:
        boxes = result.boxes
        if boxes is None or len(boxes) == 0:
            print("No boxes detected.")
            noobject_count += 1
            if noobject_count == 4:  # 如果有5帧没有检测到物体，则认为是空隙
                print("Ready for next tree to come.")
                flag = False
            continue

        noobject_count = 0  # 重置计数器
        tree_trunks = boxes.xyxy  # [x1, y1, x2, y2] 格式
        tree_conf = boxes.conf
        print("Tree trunks:", tree_trunks)
        print("Confidence:", tree_conf)

        if len(tree_conf) > 0:
            best_value, best_index = torch.max(tree_conf, dim=0)
            id_best = best_index.item()
            best_trunk = tree_trunks[id_best]
            
            print("Best trunk:", best_trunk)
            x1 = int(best_trunk[0])
            y1 = int(best_trunk[1])
            x2 = int(best_trunk[2])
            y2 = int(best_trunk[3])
            if x1 < center_line < x2 and flag == False:
                detection_count += 1
                flag = True  # 标记为已检测到物体
                print("Flag:", flag)
                print("Detection count:", detection_count)
                
                # 保存图像
                image_filename = os.path.join(output_image_folder, f'image_{frame_number}.png')
                cv2.imwrite(image_filename, frame)
                
                # 保存标签
                label_filename = os.path.join(output_label_folder, f'label_{frame_number}.txt')
                with open(label_filename, 'w') as f:
                    f.write(f'{x1} {y1} {x2} {y2}\n')
                print(f'Saved image and label for frame {frame_number}')

print("Total detection count:", detection_count)
cap.release()
cv2.destroyAllWindows()
