from send2trash import send2trash
import os
import shutil
import winshell
import win32con

download_path = "C:/Users/smbar/Downloads"

# Walk through the directory structure
for folder, folders, files in os.walk(download_path):
    # Remove directories found under download_path
    for subfolder in folders:
        folder_path = os.path.abspath(os.path.join(folder, subfolder))
        try:
            print('Removing directory: ', folder_path)
            shutil.rmtree(folder_path)  # Recursively delete the directory
        except Exception as e:
            print(f"Error removing directory {folder_path}: {e}")

    # Process files in the current folder
    for file in files:
        file_path = os.path.abspath(os.path.join(folder, file))
        
        # Send specific files to trash
        if file.endswith('.exe') or file.endswith('.txt') or file.endswith('.msi') or file.endswith('.pdf'):
            try:
                print('Deleted file: ', file_path)
                send2trash(file_path)
            except Exception as e:
                print(f"Error sending file {file_path} to trash: {e}")
        
        # Handle .zip files
        elif file.endswith('.zip'):
            try:
                print('Deleted file: ', file_path)
                send2trash(file_path)
            except Exception as e:
                print(f"Error sending file {file_path} to trash: {e}")

# Optional: Inform when script finishes
print("Script finished checking files and directories.")

answer = input("Would you like to clear the trash bin?\n")

if answer == "yes":
    try:
        winshell.recycle_bin().empty(confirm = False, show_progress=False, sound=True)
        print("Recycle Bin has been emptied!")
    except:
        print("Recycle Bin is not emptied!")
