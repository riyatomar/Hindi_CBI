import os

def rename_files_in_folder(folder_path):
    try:
        # Get the list of files in the folder
        files = os.listdir(folder_path)
        
        for file_name in files:
            # Check if it's a .txt file
            if file_name.endswith('.txt'):
                # Extract the number part and zero-pad it
                base_name, ext = os.path.splitext(file_name)
                if base_name.isdigit():  # Ensure the filename contains only numbers
                    new_name = f"sentence_{int(base_name):04d}{ext}"
                    
                    # Full paths for renaming
                    old_file_path = os.path.join(folder_path, file_name)
                    new_file_path = os.path.join(folder_path, new_name)
                    
                    # Rename the file
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed: {file_name} -> {new_name}")
    except Exception as e:
        print(f"Error: {e}")

# Specify the folder containing the files
folder_path = "clause_output"  # Replace with your folder path

# Call the function
rename_files_in_folder(folder_path)
