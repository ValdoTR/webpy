import os
from PIL import Image

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
MAX_SIZE_KB = 200
MAX_WIDTH_PX = 1280
MAX_ITERATIONS = 5
DEFAULT_QUALITY = 100

def convert_to_webp(input_path, output_path):
    quality = DEFAULT_QUALITY
    iteration = 1
    
    while iteration <= MAX_ITERATIONS:
        im = Image.open(input_path)
        
        # Resize image if width exceeds MAX_WIDTH_PX while preserving aspect ratio
        if MAX_WIDTH_PX and im.width > MAX_WIDTH_PX:
            aspect_ratio = im.width / im.height
            new_height = int(MAX_WIDTH_PX / aspect_ratio)
            im = im.resize((MAX_WIDTH_PX, new_height))
        
        im.save(output_path, "webp", quality=quality)
        
        new_size = os.path.getsize(output_path)
        
        if new_size <= MAX_SIZE_KB * 1024 or iteration >= MAX_ITERATIONS:
            original_size = os.path.getsize(input_path)
            optimization_percentage = ((original_size - new_size) / original_size) * 100
            original_size_readable = format_size(original_size)
            new_size_readable = format_size(new_size)
            print(f"Converted \033[90m'{input_path}'\033[0m. Gained \033[92m{optimization_percentage:.2f}%\033[0m ({original_size_readable} -> {new_size_readable})")
            break
        else:
            iteration += 1
            quality -= 10

# Function to convert bytes to human-readable format
def format_size(size_in_bytes):
    size_kb = size_in_bytes / 1024
    if size_kb < 1024:
        return f"{size_kb:.2f} KB"
    else:
        size_mb = size_kb / 1024
        return f"{size_mb:.2f} MB"

# Function to traverse folders and process images
def process_images():
    total_size_gained = 0

    for root, _, files in os.walk(INPUT_DIR):
        for file in files:
            input_path = os.path.join(root, file)
            relative_path = os.path.relpath(input_path, INPUT_DIR)
            output_path = os.path.join(OUTPUT_DIR, relative_path)
            output_dir = os.path.dirname(output_path)

            # Create output directory if necessary
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Check if the file is an image
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                # Convert to WebP
                output_path = os.path.splitext(output_path)[0] + ".webp"
                convert_to_webp(input_path, output_path)

                # Calculate size gained
                original_size = os.path.getsize(input_path)
                new_size = os.path.getsize(output_path)
                total_size_gained += original_size - new_size

    total_size_gained_readable = format_size(total_size_gained)
    print(f"Total size gained: {total_size_gained_readable}")


if __name__ == '__main__':
    try:
        print(f"Running script with the following requirements per image:")
        print(f"> Max size: {MAX_SIZE_KB} KB")
        print(f"> Max width: {MAX_WIDTH_PX} px")
        print(f"> Default quality: {DEFAULT_QUALITY}\n")
        process_images()
        print("\033[92mConversion completed.\033[0m")
    except KeyboardInterrupt:
        print("\033[91mScript cancelled by user\033[0m")
    except Exception as e:
        print(f"\033[91mError occurred: {e}\033[0m")
