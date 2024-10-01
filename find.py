import os

# Path to the directory containing the files
directory_path = 'strawberry_yield/GCREC_data/20231211/data_cl_2'  # Replace with your actual directory path

# Collecting all PNG and TXT files
png_files = set()
txt_files = set()

# Loop through files in the directory
for file in os.listdir(directory_path):
    if file.endswith('.jpg'):
        png_files.add(file[:-4])  # Remove the extension
    elif file.endswith('.json'):
        txt_files.add(file[:-4])  # Remove the extension

# Find files that are not paired
unpaired_png = png_files - txt_files
unpaired_txt = txt_files - png_files

# Print out the unpaired file names with their original extensions
print("Unpaired jpg files:")
for file in unpaired_png:
    print(f"{file}.jpg")

print("Unpaired json files:")
for file in unpaired_txt:
    print(f"{file}.json")
