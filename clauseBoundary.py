import re
from constant.connectives import CONNNECTIVES1, CONNNECTIVES2, RELATIVE_PRONOUNS

def extract_and_modify_tagged_data(filename):
    # Read the input file
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read()
    
    # Extract sentences tagged with <sent_id=...>...</sent_id>
    sentences = re.findall(r"(<sent_id=[^>]+>)(.*?)</sent_id>", data, re.DOTALL)
    
    modified_sentences = []
    
    # Process each sentence
    for sent_id, sentence_content in sentences:
        first_word_list = []
        # Split sentence content by lines and prepare to modify each line
        lines = sentence_content.strip().splitlines()
        # Extract and print the first word of the first 3 rows
        for i in range(min(3, len(lines))):  # Ensure we don't go out of bounds if there are fewer than 3 lines
            first_word = lines[i].split('\t')[0]  # Get the first word (before tab)
            first_word_list.append(first_word)
        starting_words = ' '.join(first_word_list)
        

        # Check if the starting_words are in CONNNECTIVES2
        matching_connective = None
        for connective in CONNNECTIVES2:
            if connective in starting_words:
                matching_connective = connective
                
        
        if matching_connective:
           # Add '\tO' to the first elements based on the length of matching_connective
            matching_length = len(matching_connective.split())  # Length of the connective
            for i in range(min(matching_length, len(lines))):
                parts = lines[i].split('\t')
                if len(parts) > 1:
                    parts.append('O')
                    lines[i] = '\t'.join(parts)
            

        sentence_length = len(lines)
        modified_lines = []

        set_next_vm_vaux_to_e = False

        for i, line in enumerate(lines):
            parts = line.split('\t')
            update_previous = False  # Track if the previous line was modified
            # print(i)
            if len(parts) >= 2:
                # Check the previous word for 'VM' or 'VAUX' if current word is in RELATIVE_PRONOUNS or 'SYM'
                if i > 0:
                    prev_word_parts = lines[i - 1].split('\t')
                    next_word_parts = lines[i + 1].split('\t') if i + 1 < sentence_length else None
                    # print(next_word_parts)
                    
                    # if prev_word_parts[1] in ['VM', 'VAUX'] and (not next_word_parts or next_word_parts[0] in RELATIVE_PRONOUNS and parts[1] == 'SYM'):
                        
                    #     prev_word_parts.append('E')
                    #     lines[i - 1] = '\t'.join(prev_word_parts)
                    #     update_previous = True  # Mark that we modified the previous line
                    
                    # Condition to append 'E' if previous word is VM/VAUX and current word is in RELATIVE_PRONOUNS
                    if prev_word_parts[1] in ['VM', 'VAUX'] and parts[0] in RELATIVE_PRONOUNS:
                        prev_word_parts.append('E')
                        lines[i - 1] = '\t'.join(prev_word_parts)
                        update_previous = True
                    
                    # Existing condition for handling 'SYM' when surrounded by certain tags
                    if prev_word_parts[1] in ['VM', 'VAUX'] and (
                        not next_word_parts or next_word_parts[0] in RELATIVE_PRONOUNS and parts[1] == 'SYM'):
                        prev_word_parts.append('E')
                        lines[i - 1] = '\t'.join(prev_word_parts)
                        update_previous = True  # Mark that we modified the previous line

                # Handle the first word in the sentence
                if i == 0:
                    # if parts[0].strip() not in CONNNECTIVES1 and 'CC' not in parts[1]:
                    #     print(parts)
                    #     parts.append('S')
                    if parts[0] == 'तो' and 'CC' in parts[1]:
                        parts.append('S')  # Set tag as 'S' instead of 'O'
                    elif parts[0].strip() not in CONNNECTIVES1 and 'CC' not in parts[1]: 
                        # Check if there's already a tag at parts[2]
                        if len(parts) < 3 or parts[2] not in ['S', 'O', 'E', 'I']:
                            parts.append('S')
                        else:
                            # Look ahead to find the next line without a tag
                            for j in range(1, sentence_length):
                                next_parts = lines[j].split('\t')
                                # Append 'S' if this line doesn't have a tag
                                if len(next_parts) < 3 or next_parts[2] not in ['S', 'O', 'E', 'I']:
                                    next_parts.append('S')
                                    lines[j] = '\t'.join(next_parts)
                                    break
                    else:
                    # elif parts[0] in CONNNECTIVES1:
                        # print(parts)
                        parts.append('O')
                        if sentence_length > 1:
                            next_word_parts = lines[i + 1].split('\t')
                            if len(next_word_parts) < 3:
                                lines[i + 1] = lines[i + 1] + "\tS"
                
                # Handle SYM based on position and following word
                elif parts[1] == 'SYM':
                    # print(prev_word_parts[1])
                    if (i + 1 < sentence_length and lines[i + 1].split('\t')[0] in RELATIVE_PRONOUNS and prev_word_parts[1] in ['VM', 'VAUX']) or i == sentence_length - 1:
                        parts.append('O')  # Tag as 'O' if followed by a RELATIVE_PRONOUN or at sentence end
                    elif len(parts) < 3:
                        parts.append('I')  # Otherwise, tag as 'I'
                
                # Handle the last word if not SYM
                elif i == sentence_length - 2 and parts[1] != 'SYM':
                    parts.append('E')
                
                # Handle middle words in the sentence
                else:
                    # Check if the word is in RELATIVE_PRONOUNS
                    if parts[0].strip() in RELATIVE_PRONOUNS:
                        # print(parts)
                        parts.append('S')
                        set_next_vm_vaux_to_e = True
                        if len(parts) > 3:
                            parts.pop()
                    
                    elif parts[1].strip() == 'VAUX':
                        # print(parts[1])
                        if set_next_vm_vaux_to_e:
                            parts.append('E')
                            set_next_vm_vaux_to_e = False
                        elif len(parts) < 3:
                            parts.append('I')
                    
                    elif len(parts) < 3 or parts[2] not in ['S', 'O', 'E', 'I']:
                        parts.append('I')

                # Append modified previous line if it was updated
                if update_previous and modified_lines:
                    modified_lines[-1] = lines[i - 1]
                
                modified_lines.append('\t'.join(parts))

        # Join modified lines back into a sentence structure
        modified_sentences.append(f"{sent_id}\n" + '\n'.join(modified_lines) + "\n</sent_id>")

    # Join all modified sentences with a double newline separator
    result_data = '\n\n'.join(modified_sentences)

    # Write result_data to an output file
    with open('data/clause_bounded_output.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(result_data)


extract_and_modify_tagged_data("data/tagged_output.txt")


