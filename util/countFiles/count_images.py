import os

def count_images(folder_path):
    image_counts = {}
    for root, dirs, files in os.walk(folder_path):
        parent_folder = os.path.basename(os.path.dirname(root))
        image_count = sum(1 for file in files if file.lower().endswith('.jpg'))
        if image_count > 0:
            if parent_folder not in image_counts:
                image_counts[parent_folder] = 0
            image_counts[parent_folder] += image_count

    for folder, count in image_counts.items():
        print(f"Folder: {folder} count: {count}")
import os

def count_images_total(folder_path):
    count = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.jpg'):
                count += 1

    print(f"total image files : {count}")

if __name__ == "__main__":
    import sys
    folder_path = sys.argv[1]
    count_images(folder_path)
    count_images_total(folder_path)
