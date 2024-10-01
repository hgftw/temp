from ultralytics import YOLO

# Load a model
model = YOLO("runs/detect/train5/weights/best.pt")  # load a custom model
# model = YOLO("yolov8m.pt")  


# Track with the model
# results = model.track(source="05222024rightdown_crop.mp4", show=True, save=True, save_txt=True, save_conf=True, tracker="botsort.yaml", conf=0.4, iou =0.5)  # botsort

 
results = model.track(source="05222024leftdown_crop.mp4", show=True, save=True, save_txt=True, save_conf=True, tracker="bytetrack.yaml", conf=0.4, iou = 0.5)  # bytetrack


id_list = []
for result in results:
    obj_id = result.boxes.id
    id_list.append(obj_id)
    
print(id_list)
