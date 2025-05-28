import os
from PIL import Image
# pip install Pillow

# variables
year = 2017

print("📷 JPG to WEBP converter:")

# Input folder path
input_folder = f'b:/Prywatne/Lifebook/Timeline/{year}/'

# Subfolder for webp
webp_folder = os.path.join(input_folder, 'webp')

# Ensure the webp folder exists
if not os.path.exists(webp_folder):
  os.makedirs(webp_folder)

# Get list of JPG files
jpg_files = {
  os.path.splitext(filename)[0]
  for filename in os.listdir(input_folder)
  if filename.lower().endswith(('.jpg', '.jpeg'))
}

# Loop through all files in the input folder
for filename in sorted(os.listdir(input_folder)):
  if filename.endswith('.jpg') or filename.endswith('.jpeg'):
    # Full path to the JPG file
    input_path = os.path.join(input_folder, filename)

    # Generate the WebP filename based on the JPG file
    webp_filename = os.path.splitext(filename)[0] + '.webp'
    output_path = os.path.join(webp_folder, webp_filename)

    # Check if the WebP file already exists
    if not os.path.exists(output_path):
      try:
        # Open the JPG file
        image = Image.open(input_path)

        # Resize the image
        new_image = image.resize((240, 180))

        # Save as WebP with 60% quality
        new_image.save(output_path, "WEBP", quality=60)

        print(f'🟢 Converted: {filename} -> {webp_filename}')
      except Exception as e:
        print(f"Error converting {filename}: {e}")
    else:
      print(f'🟡 Skipping: {webp_filename} already exists.')

# 🗑️ Remove WebP files that have no corresponding JPG
for webp_filename in os.listdir(webp_folder):
  if webp_filename.lower().endswith('.webp'):
    webp_name = os.path.splitext(webp_filename)[0]
    if webp_name not in jpg_files:
      webp_path = os.path.join(webp_folder, webp_filename)
      try:
        os.remove(webp_path)
        print(f'🔴 Deleted: {webp_filename} has no corresponding JPG.')
      except Exception as e:
        print(f'Error deleting {webp_filename}: {e}')

print('🏆 Conversion done!')