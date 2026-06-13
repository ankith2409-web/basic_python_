import os
import shutil
import sys

def organize_files(directory_path):
    """
    Organizes files in the specified directory into subfolders based on their file extensions.
    """
    if not os.path.exists(directory_path):
        print(f"Error: The directory '{directory_path}' does not exist.")
        return

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
            
        # Get the file extension
        _, extension = os.path.splitext(filename)
        extension = extension[1:].lower() # Remove the dot and convert to lowercase
        
        if not extension:
            extension = "others"
            
        # Create a folder for the extension if it doesn't exist
        folder_path = os.path.join(directory_path, extension)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        # Move the file to the corresponding folder
        destination_path = os.path.join(folder_path, filename)
        try:
            shutil.move(file_path, destination_path)
            print(f"Moved '{filename}' to '{extension}/'")
        except Exception as e:
            print(f"Failed to move '{filename}': {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_directory = sys.argv[1]
    else:
        target_directory = input("Enter the path of the directory to organize: ")
    organize_files(target_directory)
