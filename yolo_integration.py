
import os
from ultralytics import YOLO
import time
import shutil
import numpy as np

# Load the YOLO model
model = YOLO(r'D:\pothole_detection\runs\detect\train4\weights\best.pt')

def detect_pothole(image_path, output_dir):
    # Check if the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Example: Create a unique subdirectory for each detection
    detection_folder = os.path.join(output_dir, f"detection_results_{int(time.time())}")
    os.makedirs(detection_folder, exist_ok=True)

    # Perform detection
    results = model.predict(source=image_path, save=True, save_txt=False, project=output_dir, name='detection_results_orginal1')
    print("Detection results:", results[0].boxes)
    
    # Get bounding boxes from the detection results
    detected_boxes = results[0].boxes.data.cpu().numpy() if len(results) > 0 else []
    box_count = len(detected_boxes)

    # Extract bounding box data from results
    if len(results) > 0:
        detected_boxes = results[0].boxes.data.cpu().numpy()  
    else:
        detected_boxes = []

    # Extract confidence scores
    if len(results) > 0 and results[0].boxes is not None:
        detected_boxes = results[0].boxes  

        # Extract confidence scores from the 'conf' attribute
        confidence_scores = detected_boxes.conf.cpu().numpy()  
        print("Confidence Scores:", confidence_scores)

        average_confidence = max(confidence_scores) if len(confidence_scores) > 0 else 0.0
        print("Average Confidence:", average_confidence)
    else:
        print("No detections found!")
        confidence_scores = []
        average_confidence = 0.0

    # Save the processed image
    detected_image_path = os.path.join(detection_folder, "detected_image.jpg")
    shutil.copy(image_path, detected_image_path)

    return detection_folder, box_count , average_confidence
