# import os

# # Input and output folder paths
# input_folder_path = "review_sentences"  # Folder containing input files
# output_folder_path = "clause_output"    # Folder to store output files

# # Ensure the output folder exists
# os.makedirs(output_folder_path, exist_ok=True)

# # Process each file in the input folder
# for input_filename in os.listdir(input_folder_path):
#     input_file_path = os.path.join(input_folder_path, input_filename)

#     # Skip directories and process only files
#     if not os.path.isfile(input_file_path):
#         continue

#     # Construct the output file path
#     output_file_path = os.path.join(output_folder_path, input_filename)

#     # Read the input file
#     with open(input_file_path, "r", encoding="utf-8") as file:
#         lines = file.readlines()

#     # Extract the first column values
#     first_column_values = [line.split("\t")[0] for line in lines if line.strip()]

#     # Form a sentence from the first column values
#     sentence = " ".join(first_column_values).strip('#')
#     sentence = sentence + '\n\n' + sentence

#     # Write the sentence to the output file
#     with open(output_file_path, "w", encoding="utf-8") as file:
#         file.write(sentence)

#     # print(f"Processed '{input_filename}' -> '{output_file_path}'")


import os

# Input folder paths
input_folders = ["review_sentences", "invalid_labelled_data"]

# Output folder path
output_folder_path = "clause_output"

# Ensure the output folder exists
os.makedirs(output_folder_path, exist_ok=True)

# Process files from both input folders
for input_folder in input_folders:
    for input_filename in os.listdir(input_folder):
        input_file_path = os.path.join(input_folder, input_filename)

        # Skip directories and process only files
        if not os.path.isfile(input_file_path):
            continue

        # Construct a unique output file path
        output_file_name = f"{os.path.basename(input_folder)}_{input_filename}"
        output_file_path = os.path.join(output_folder_path, output_file_name)

        # Read the input file
        with open(input_file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Extract the first column values
        first_column_values = [line.split("\t")[0] for line in lines if line.strip()]

        # Form a sentence from the first column values
        sentence = " ".join(first_column_values).strip('#')
        sentence = sentence + '\n\n' + sentence

        # Write the sentence to the output file
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(sentence)

        # print(f"Processed '{input_file_path}' -> '{output_file_path}'")
