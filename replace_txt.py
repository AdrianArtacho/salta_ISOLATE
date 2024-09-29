import shutil
import os

def main(source_path, destination_path):    # copy_and_rename_file
    # Check if the destination directory exists, create it if it doesn't
    destination_dir = os.path.dirname(destination_path)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    # Copy the source file to the new destination with the new name
    shutil.copy2(source_path, destination_path)

    print(f"File copied and renamed from {source_path} to {destination_path}.")

if __name__ == "__main__":
    source_path = 'OUTPUT/rectangles_positions.txt'
    destination_path = 'OUTPUT/exp9f-noEA.txt'
    main(source_path, destination_path)