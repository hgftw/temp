from ultralytics import YOLO

model = YOLO("yolov8n-cls.yaml").load("yolov8n-cls.pt")  # build from YAML and transfer weights

# Train the model
# results = model.train(data="datasets/3class_Agrosense_Density_Classification", epochs=500, imgsz=640)
results = model.train(data="datasets/5class_Density_Classification", epochs=500, imgsz=640)