import cv2
from pytorchyolo import detect, models

# Load the YOLO model
model = models.load_model(
  "yolov3-320.cfg", 
  "C:\models\yolov3.weights")
