import cv2
from PIL import Image
from ultralytics import YOLO

model = YOLO("runs/detect/train5/weights/best.pt")
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
results = model.predict(source="05_22_2024_test_crop/output_05222024rightdown_crop", save=True, save_txt=True, conf = 0.1)  # Display preds. Accepts all YOLO predict arguments


