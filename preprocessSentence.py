import re

def process_line(line):
    # Split the line by tab to separate the sentence ID and sentence
    parts = line.strip().split('\t', 1)
    # Check if the line has both sentence ID and sentence
    if len(parts) != 2:
        print(f"Warning: Line skipped due to incorrect format: {line.strip()}")
        return None  # Skip lines without proper format
    
    sentence_id, sentence = parts
    
    # Use regex to add spaces around special symbols, including । and excluding hyphen
    processed_sentence = re.sub(r'([!@#$%^&*()_+={}[\];"\'<>,.?/~`|\\।])', r' \1 ', sentence)
    
    # Remove extra whitespace that might have appeared, replacing multiple spaces with a single space
    processed_sentence = re.sub(r'\s+', ' ', processed_sentence).strip()
    
    # Check if the sentence ends with '।', '?' or '!', and add '।' if it does not
    if not processed_sentence.endswith(('।', '?', '!')):
        processed_sentence += ' ।'
    
    return f"{sentence_id}\t{processed_sentence}"

# Read from file and process
input_file = 'data/sentences.txt'
output_file = 'data/processed_sentences.txt'
output_lines = []

with open(input_file, 'r', encoding='utf-8') as file:
    for line in file:
        processed_line = process_line(line)
        if processed_line:  # Only add lines that were successfully processed
            output_lines.append(processed_line)

# Write output to the specified file
with open(output_file, 'w', encoding='utf-8') as file:
    for output_line in output_lines:
        file.write(output_line + '\n')

# import re

# def process_line(line):
#     # Split the line by tab to separate the sentence ID and sentence
#     parts = line.strip().split('\t', 1)
#     # Check if the line has both sentence ID and sentence
#     if len(parts) != 2:
#         print(f"Warning: Line skipped due to incorrect format: {line.strip()}")
#         return None  # Skip lines without proper format
    
#     sentence_id, sentence = parts
    
#     # Use regex to add spaces around special symbols (excluding hyphen) 
#     # only if there’s exactly one space on either side, otherwise skip.
#     processed_sentence = re.sub(
#         r'(?<=\s)([!@#$%^&*()_+={}[\]:;"\'<>,.?/~`|\\।])(?=\S)|(?<=\S)([!@#$%^&*()_+={}[\]:;"\'<>,.?/~`|\\।])(?=\s)',
#         r' \1\2 ',
#         sentence
#     )
    
#     # Remove extra whitespace that might have appeared, replacing multiple spaces with a single space
#     processed_sentence = re.sub(r'\s+', ' ', processed_sentence).strip()
    
#     # Check if the sentence ends with '।', '?' or '!', and add '।' if it does not
#     if not processed_sentence.endswith(('।', '?', '!')):
#         processed_sentence += ' ।'
    
#     return f"{sentence_id}\t{processed_sentence}"


# # Read from file and process
# input_file = 'data/sentences.txt'
# output_file = 'data/processed_sentences.txt'
# output_lines = []

# with open(input_file, 'r', encoding='utf-8') as file:
#     for line in file:
#         processed_line = process_line(line)
#         if processed_line:  # Only add lines that were successfully processed
#             output_lines.append(processed_line)

# # Write output to the specified file
# with open(output_file, 'w', encoding='utf-8') as file:
#     for output_line in output_lines:
#         file.write(output_line + '\n')