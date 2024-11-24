import os

# Function to get filenames in ascending order
def list_files_in_ascending_order(folder_path):
    try:
        # Get all files and directories in the folder
        files = os.listdir(folder_path)
        # Sort the filenames in ascending order
        sorted_files = sorted(files)
        return sorted_files
    except FileNotFoundError:
        print(f"The folder {folder_path} does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Main function
if __name__ == "__main__":
    # Specify the folder path
    folder_path = 'clause_output'
    
    # Get the sorted list of filenames
    sorted_filenames = list_files_in_ascending_order(folder_path)
    
    if sorted_filenames:
        print("\nFiles in ascending order:")
        for filename in sorted_filenames:
            print(filename)
    else:
        print("No files found or an error occurred.")
