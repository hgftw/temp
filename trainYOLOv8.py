
from ultralytics import YOLO


# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

model.train(data="data.yaml", epochs=300) 
metrics = model.val()  # evaluate model performance on the validation set
