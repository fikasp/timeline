import os
from PIL import Image
# pip install Pillow

# Input folder path
input_folder = 'b:/Prywatne/Lifebook/Timeline/2024/'

# Subfolder for webp
webp_folder = os.path.join(input_folder, 'webp')

# Ensure the webp folder exists
if not os.path.exists(webp_folder):
  os.makedirs(webp_folder)

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

        print(f'Converted: {filename} -> {webp_filename}')
      except Exception as e:
        print(f"Error converting {filename}: {e}")
    else:
      print(f'Skipping: {webp_filename} already exists.')

print('Conversion done...')