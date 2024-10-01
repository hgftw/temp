import cv2
from ultralytics import YOLO
import numpy as np
import torch

# Load the image
img = cv2.imread('./test/20240207_160851870_iOS_jpg.rf.da37b572eb6da65a3c7a1463b76e3e50.jpg')

# Initialize the YOLO model
model = YOLO('./test/best.pt')

# Predict objects in the image
results = model.predict(source=img, max_det=1, save=True, save_txt=False, stream=True)
for result in results:
    # Get array results
    masks = result.masks.data
    boxes = result.boxes.data
    # Extract classes
    clss = boxes[:, 5]
    
    for box in boxes:
        x_min, y_min, x_max, y_max = box[:4]  # Extracting x, y values from the bounding box
        # Draw bounding box rectangle on the image
        cv2.rectangle(img, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)

        # Connect left and right pixels with a line
        left_x = int(x_min)
        left_y = int((y_min + y_max) / 2)  # Calculate the middle point vertically
        right_x = int(x_max)
        right_y = left_y

        cv2.line(img, (left_x, left_y), (right_x, right_y), (255, 0, 0), 2)  # Draw a line

        # Get indices of results where class is 0 (trunk indice)
        trunk_indices = torch.where(clss == 0)
        # Use these indices to extract the relevant masks
        trunk_masks = masks[trunk_indices]
        # Scale for visualizing results
        trunk_mask = torch.any(trunk_masks, dim=0).int() * 255
        trunk_mask_array = trunk_mask.cpu().numpy()  # Create trunk_mask_array

        # Find intersection points between the line and the trunk_mask_array
        line_mask = np.zeros_like(trunk_mask_array, dtype=np.uint8)
        cv2.line(line_mask, (left_x, left_y), (right_x, right_y), 255, 1)  # Draw the line on the mask
        intersection_points = np.where(np.logical_and(line_mask, trunk_mask_array))  # Find intersection points

        # Find the most left and most right side points
        if intersection_points[1].size > 0:
            most_left_point = (np.min(intersection_points[1]), intersection_points[0][np.argmin(intersection_points[1])])
            most_right_point = (np.max(intersection_points[1]), intersection_points[0][np.argmax(intersection_points[1])])

            # Print the coordinates of the most left and most right side points
            print("Most Left Point Coordinates:", most_left_point)
            print("Most Right Point Coordinates:", most_right_point)

            # Visualize the most left and most right side points on the image
            cv2.circle(img, most_left_point, 5, (0, 0, 255), -1)  # Red circle for most left point
            cv2.circle(img, most_right_point, 5, (0, 255, 255), -1)  # Yellow circle for most right point

# Save the image with bounding boxes
cv2.imwrite(str(model.predictor.save_dir / 'merged_segs_with_boxes.jpg'), img)

