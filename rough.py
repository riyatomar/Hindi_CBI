# # import re
# # from constant.connectives import CONNNECTIVES1, RELATIVE_PRONOUNS

# # def extract_and_modify_tagged_data(filename):
# #     # Read the input file
# #     with open(filename, 'r', encoding='utf-8') as file:
# #         data = file.read()
    
# #     # Extract sentences tagged with <sent_id=...>...</sent_id>
# #     sentences = re.findall(r"(<sent_id=[^>]+>)(.*?)</sent_id>", data, re.DOTALL)
    
# #     modified_sentences = []
    
# #     # Process each sentence
# #     for sent_id, sentence_content in sentences:
# #         # Split sentence content by lines and prepare to modify each line
# #         lines = sentence_content.strip().splitlines()
# #         sentence_length = len(lines)
# #         modified_lines = []

# #         # Initialize a flag to track if we need to tag a VM or VAUX with 'E' after an 'S' assignment
# #         set_next_vm_vaux_to_e = False

# #         for i, line in enumerate(lines):
# #             parts = line.split('\t')
            
# #             if len(parts) >= 2:
# #                 # Handle the first word in the sentence
# #                 if i == 0:
# #                     if parts[0].strip() not in CONNNECTIVES1 and 'CC' not in parts[1]:
# #                         parts.append('S')
# #                     else:
# #                         parts.append('O')
# #                         # Ensure the next word gets 'S' if it’s not already labeled
# #                         if sentence_length > 1:
# #                             next_word_parts = lines[i + 1].split('\t')
# #                             if len(next_word_parts) < 3:
# #                                 lines[i + 1] = lines[i + 1] + "\tS"
                
# #                 # Handle the last word in the sentence
# #                 elif i == sentence_length - 1 and parts[1] == 'SYM':
# #                     parts.append('O')
                
# #                 elif i == sentence_length - 2 and parts[1] != 'SYM':
# #                     parts.append('E')
                
# #                 # Handle middle words in the sentence
# #                 else:
# #                     # Check if the current word is 'SYM' and is preceded by 'VM' or 'VAUX' and followed by a relative pronoun
# #                     if parts[1] == 'SYM':
# #                         if len(parts) < 3:
# #                             parts.append('I')
# #                         # Check the previous word (if it exists) for 'VM' or 'VAUX'
# #                         if i > 0:
# #                             prev_word_parts = lines[i - 1].split('\t')
# #                             if prev_word_parts[1] in ['VM', 'VAUX']:
# #                                 # if len(prev_word_parts) < 3:  # Avoid overwriting existing labels
# #                                 prev_word_parts.append('E')
                                
# #                                 # Update the previous line with this modification
# #                                 lines[i - 1] = '\t'.join(prev_word_parts)
# #                                 print(lines[i-1])
# #                                 # Look ahead to see if the next word is a relative pronoun
# #                                 if i + 1 < sentence_length:
# #                                     next_word_parts = lines[i + 1].split('\t')
# #                                     if next_word_parts[0] in RELATIVE_PRONOUNS:
# #                                         parts.append('O')
# #                                     elif len(parts) < 3:
# #                                         parts.append('I')
                    
# #                     # Check if the word is in RELATIVE_PRONOUNS
# #                     elif parts[0] in RELATIVE_PRONOUNS:
# #                         parts.append('S')
# #                         set_next_vm_vaux_to_e = True  # Activate flag to set next VM/VAUX to 'E'
                    
# #                     elif parts[1] in ['VAUX']:
# #                         if set_next_vm_vaux_to_e:
# #                             parts.append('E')
# #                             set_next_vm_vaux_to_e = False  # Reset the flag
# #                         elif len(parts) < 3:
# #                             parts.append('I')
                    
# #                     # Default to 'I' for other cases if not already tagged
# #                     # elif len(parts) < 3:
# #                     elif len(parts) < 3 or parts[2] not in ['S', 'O', 'E', 'I']:
# #                         parts.append('I')

# #                 modified_lines.append('\t'.join(parts))

# #         # Join modified lines back into a sentence structure
# #         modified_sentences.append(f"{sent_id}\n" + '\n'.join(modified_lines) + "\n</sent_id>")

# #     # Join all modified sentences with a double newline separator
# #     result_data = '\n\n'.join(modified_sentences)

# #     # Write result_data to an output file
# #     with open('data/clause_bounded_output.txt', 'w', encoding='utf-8') as output_file:
# #         output_file.write(result_data)


# # extract_and_modify_tagged_data("data/tagged.txt")


# import re
# from constant.connectives import CONNNECTIVES1, RELATIVE_PRONOUNS

# def extract_and_modify_tagged_data(filename):
#     # Read the input file
#     with open(filename, 'r', encoding='utf-8') as file:
#         data = file.read()
    
#     # Extract sentences tagged with <sent_id=...>...</sent_id>
#     sentences = re.findall(r"(<sent_id=[^>]+>)(.*?)</sent_id>", data, re.DOTALL)
    
#     modified_sentences = []
    
#     # Process each sentence
#     for sent_id, sentence_content in sentences:
#         # Split sentence content by lines and prepare to modify each line
#         lines = sentence_content.strip().splitlines()
#         sentence_length = len(lines)
#         modified_lines = []

#         # Initialize a flag to track if we need to tag a VM or VAUX with 'E' after an 'S' assignment
#         set_next_vm_vaux_to_e = False

#         for i, line in enumerate(lines):
#             parts = line.split('\t')
#             update_previous = False  # Track if the previous line was modified
            
#             if len(parts) >= 2:
#                 # Handle the first word in the sentence
#                 if i == 0:
#                     if parts[0].strip() not in CONNNECTIVES1 and 'CC' not in parts[1]:
#                         parts.append('S')
#                     else:
#                         parts.append('O')
#                         if sentence_length > 1:
#                             next_word_parts = lines[i + 1].split('\t')
#                             if len(next_word_parts) < 3:
#                                 lines[i + 1] = lines[i + 1] + "\tS"
                
#                 # Handle the last word in the sentence
#                 elif i == sentence_length - 1 and parts[1] == 'SYM':
#                     parts.append('O')
                
#                 elif i == sentence_length - 2 and parts[1] != 'SYM':
#                     parts.append('E')
                
#                 # Handle middle words in the sentence
#                 else:
#                     # Check if the current word is 'SYM' and is preceded by 'VM' or 'VAUX' and followed by a relative pronoun
#                     if parts[1] == 'SYM':
#                         if len(parts) < 3:
#                             parts.append('I')
#                         if i > 0:
#                             prev_word_parts = lines[i - 1].split('\t')
#                             if prev_word_parts[1] in ['VM', 'VAUX']:
#                                 prev_word_parts.append('E')
#                                 lines[i - 1] = '\t'.join(prev_word_parts)
#                                 update_previous = True  # Indicate the previous line was modified
#                                 if i + 1 < sentence_length:
#                                     next_word_parts = lines[i + 1].split('\t')
#                                     if next_word_parts[0] in RELATIVE_PRONOUNS:
#                                         parts.append('O')
#                                     elif len(parts) < 3:
#                                         parts.append('I')
                    
#                     # Check if the word is in RELATIVE_PRONOUNS
#                     elif parts[0] in RELATIVE_PRONOUNS:
#                         parts.append('S')
#                         set_next_vm_vaux_to_e = True
                    
#                     elif parts[1] in ['VAUX']:
#                         if set_next_vm_vaux_to_e:
#                             parts.append('E')
#                             set_next_vm_vaux_to_e = False
#                         elif len(parts) < 3:
#                             parts.append('I')
                    
#                     elif len(parts) < 3 or parts[2] not in ['S', 'O', 'E', 'I']:
#                         parts.append('I')

#                 # Append modified previous line if it was updated
#                 if update_previous and modified_lines:
#                     modified_lines[-1] = lines[i - 1]
                
#                 modified_lines.append('\t'.join(parts))

#         # Join modified lines back into a sentence structure
#         modified_sentences.append(f"{sent_id}\n" + '\n'.join(modified_lines) + "\n</sent_id>")

#     # Join all modified sentences with a double newline separator
#     result_data = '\n\n'.join(modified_sentences)

#     # Write result_data to an output file
#     with open('data/clause_bounded_output.txt', 'w', encoding='utf-8') as output_file:
#         output_file.write(result_data)


# extract_and_modify_tagged_data("data/tagged.txt")

