import os
import argparse
from PIL import Image

def convert_to_webp(input_dir, output_dir, quality):
    config = {'quality': quality}

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img = Image.open(os.path.join(input_dir, filename))
            filename_without_ext = os.path.splitext(filename)[0]
            output_file = os.path.join(output_dir, f"{filename_without_ext}.webp")
            img.save(output_file, "webp", **config)

def main():
    parser = argparse.ArgumentParser(description='Convert .jpg and .png files to .webp format.')
    parser.add_argument('-i', '--input', type=str, required=True, help='The input directory path')
    parser.add_argument('-o', '--output', type=str, required=True, help='The output directory path')
    parser.add_argument('-q', '--quality', type=int, default=80, help='The quality of the output image, default is 80')
    
    args = parser.parse_args()

    convert_to_webp(args.input, args.output, args.quality)

if __name__ == "__main__":
    main()