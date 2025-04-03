import os
import argparse
from PIL import Image, ExifTags

def calculate_height(original_width, original_height, target_width):
    aspect_ratio = original_width / original_height
    target_height = int(target_width / aspect_ratio)
    return target_height

def fix_orientation(image):
    try:
        # Check if the image has EXIF data
        if hasattr(image, '_getexif') and image._getexif() is not None:
            exif = dict(image._getexif().items())

            # Look for the orientation tag
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    if orientation in exif:
                        # Rotate the image based on the orientation tag
                        if exif[orientation] == 3:
                            image = image.rotate(180, expand=True)
                        elif exif[orientation] == 6:
                            image = image.rotate(270, expand=True)
                        elif exif[orientation] == 8:
                            image = image.rotate(90, expand=True)
                        break
    except Exception as e:
        print(f"Error occurred while fixing orientation: {str(e)}")
    
    return image

def convert_to_webp(input_dir, output_dir, quality, width):
    config = {'quality': quality}

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            img = Image.open(os.path.join(input_dir, filename))

            img = fix_orientation(img)  # Fix the image orientation if needed

            if width != 0:
                original_width, original_height = img.size

                target_width = width

                target_height = calculate_height(original_width, original_height, target_width)

                img = img.resize((width, target_height))  # Resize the image to the desired size
            else:
                target_width = img.size[0]
                target_height = img.size[1]

            filename_without_ext = os.path.splitext(filename)[0]
            output_filename = f"{filename_without_ext}_q{quality}_{target_width}x{target_height}.webp"
            output_file = os.path.join(output_dir, output_filename)
            img.save(output_file, "webp", **config)

def main():
    parser = argparse.ArgumentParser(description='Convert .jpg and .png files to .webp format.')
    parser.add_argument('-i', '--input', type=str, required=True, help='The input directory path')
    parser.add_argument('-o', '--output', type=str, required=True, help='The output directory path')
    parser.add_argument('-q', '--quality', type=int, default=80, help='The quality of the output image, default is 80')
    parser.add_argument('-w', '--width', type=int, required=True, help='The desired output image width, 0 for no resize')

    args = parser.parse_args()

    convert_to_webp(args.input, args.output, args.quality, args.width)

if __name__ == "__main__":
    main()
