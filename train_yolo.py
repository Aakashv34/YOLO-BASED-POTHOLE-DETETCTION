import os
from ultralytics import YOLO

# Set environment variable to allow duplicate OpenMP library loading
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# Load the YOLO model
model = YOLO('yolov8s.pt')  # You can use other YOLOv8 variants like 'yolov8m.pt' or 'yolov8l.pt'

# Train the model on the dataset
model.train(
    data='D:/Pothole/Pothole_Segmentation_YOLOv8/pothole.yaml',  # Path to the YAML file
    epochs=35,  # Number of epochs for training
    imgsz=640,  # Image size
    batch=16,  # Batch size (adjust based on your system's memory)
    save=True  # Save the model automatically
)

# Save the trained model
best_model_path = 'runs/detect/train/weights/best.pt'  # Change this based on your run location
last_model_path = 'runs/detect/train/weights/last.pt'  # Path to the final model

print(f"Best model saved at: {best_model_path}")
print(f"Last model saved at: {last_model_path}")
