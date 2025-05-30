import os
from PIL import Image

def detect_and_crop_seal(pil_img, base_name, output_dir):
    width, height = pil_img.size
    # Crop bottom-right 200x200 pixels (adjust if needed)
    cropped = pil_img.crop((width - 200, height - 200, width, height))
    path = os.path.join(output_dir, f"{base_name}_seal.png")
    cropped.save(path)
    return True, path
