import os
import shutil
import random

# Directory containing the paired image and TXT files
source_directory = 'together'  # Replace with your actual source directory

# Directories for the train, test, and validation splits
train_directory = 'trainingdata/train'  # Replace with your actual train directory
test_directory = 'trainingdata/test'    # Replace with your actual test directory
valid_directory = 'trainingdata/valid'  # Replace with your actual validation directory

# Ensure the subdirectories for images and labels exist
for directory in [train_directory, test_directory, valid_directory]:
    os.makedirs(os.path.join(directory, 'images'), exist_ok=True)
    os.makedirs(os.path.join(directory, 'labels'), exist_ok=True)

# Collect all paired files
files = [f[:-4] for f in os.listdir(source_directory) if f.endswith(('.png', '.jpg'))]
random.shuffle(files)

# Split files into train, test, and validation sets
num_files = len(files)
train_end = int(num_files * 0.8)
test_end = train_end + int(num_files * 0.1)

train_files = files[:train_end]
test_files = files[train_end:test_end]
valid_files = files[test_end:]

def copy_files(file_list, destination):
    for file in file_list:
        # Copy image files
        for extension in ['.png', '.jpg']:
            image_path = os.path.join(source_directory, f"{file}{extension}")
            if os.path.exists(image_path):
                shutil.copy(image_path, os.path.join(destination, 'images', f"{file}{extension}"))
        # Copy text files
        txt_path = os.path.join(source_directory, f"{file}.txt")
        if os.path.exists(txt_path):
            shutil.copy(txt_path, os.path.join(destination, 'labels', f"{file}.txt"))

# Copy files to respective directories
copy_files(train_files, train_directory)
copy_files(test_files, test_directory)
copy_files(valid_files, valid_directory)

print("Files have been copied to train, test, and validation directories.")