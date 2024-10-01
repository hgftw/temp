from ultralytics import YOLO


model = YOLO("train17/weights/best.pt")  # load a custom model

# Predict with the model
results = model("tree_height/leftdown_out", save=True)  # predict on an image