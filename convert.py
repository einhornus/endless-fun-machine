import os
from PIL import Image
import sys


def convert_to_png(directory="comics"):
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    files = os.listdir(directory)
    converted = 0

    for filename in files:
        file_path = os.path.join(directory, filename)

        if os.path.isdir(file_path):
            continue

        if filename.lower().endswith('.png'):
            continue

        try:
            with Image.open(file_path) as img:
                name, _ = os.path.splitext(filename)
                new_filename = f"{name}.png"
                new_path = os.path.join(directory, new_filename)
                img.save(new_path, "PNG")
                converted += 1
                print(f"Converted: {filename} → {new_filename}")
        except Exception as e:
            print(f"Could not convert {filename}: {e}")

    print(f"Conversion complete. {converted} files converted to PNG.")


def remove_non_png_files(directory="comics"):
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    files = os.listdir(directory)

    removed = 0

    for filename in files:
        file_path = os.path.join(directory, filename)

        if os.path.isdir(file_path):
            continue

        if filename.lower().endswith('.png'):
            continue

        try:
            os.remove(file_path)
            removed += 1
            print(f"Removed: {filename}")
        except Exception as e:
            print(f"Could not remove {filename}: {e}")

    print(f"Cleanup complete. {removed} non-PNG files removed.")


if __name__ == "__main__":
    directory = "data"
    if len(sys.argv) > 1:
        directory = sys.argv[1]

    convert_to_png(directory)
    remove_non_png_files(directory)
