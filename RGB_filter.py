'''
Use this script to filter the rgb and depth image
'''
import os
import cv2
import numpy as np

def process_images(depth_dir, rgb_dir, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Iterate through all files in the depth image directory
    for depth_filename in os.listdir(depth_dir):
        if depth_filename.endswith('.png'):
            # Construct full path for depth and corresponding RGB images
            depth_image_path = os.path.join(depth_dir, depth_filename)
            rgb_image_path = os.path.join(rgb_dir, depth_filename.replace('_depth', ''))

            # Read depth and RGB images
            depth_image = cv2.imread(depth_image_path, cv2.IMREAD_UNCHANGED)
            rgb_image = cv2.imread(rgb_image_path)

            if depth_image is None or rgb_image is None:
                print(f"Skipping pair: {depth_image_path}, {rgb_image_path}")
                continue

            # Convert depth values to meters (assuming depth values are in millimeters)
            depth_image_meters = depth_image / 1000.0

            # Handle zero depth values by setting them to a large value
            depth_image_meters[depth_image_meters == 0] = 100

            # Create a mask where depth values are greater than 5 meters
            mask = depth_image_meters > 5

            # Set pixel values in RGB image to 0 where mask is True
            rgb_image[mask] = [0, 0, 0]
            
            # rgb_image_rotated = cv2.rotate(rgb_image, cv2.ROTATE_90_CLOCKWISE)
            # # rgb_image_rotated = cv2.rotate(rgb_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

            
            # Save the modified RGB image
            output_image_path = os.path.join(output_dir, os.path.basename(rgb_image_path))
            # cv2.imwrite(output_image_path, rgb_image_rotated)
            cv2.imwrite(output_image_path, rgb_image)
            print(f"Processed and saved: {output_image_path}")

# Define directories
depth_image_dir = 'tree_height/leftdown_depth'
rgb_image_dir = 'tree_height/leftdown_image'
output_image_dir = 'tree_height/leftdown_out'

# Process images
process_images(depth_image_dir, rgb_image_dir, output_image_dir)

