import os
import shutil

# Define the set of verb POS tags
VERB_POS_TAGS = {'VM', 'VAUX'}

def read_sentence(file_path):
    """
    Reads a sentence file and returns a list of word information dictionaries.
    Each dictionary contains 'word', 'pos', and 'label'.
    """
    word_infos = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) != 3:
                continue  # Skip invalid lines
            word, pos, label = parts
            word_infos.append({'word': word, 'pos': pos, 'label': label})
    return word_infos

def check_rule_2(word_infos, verb_pos_tags):
    """
    Checks if rule 2 applies to the sentence.
    If a clause identified with S & E lacks a verb, changes the E label to I.
    Returns True if rule 2 applies, otherwise False.
    """
    stack = []
    rule_2_applies = False
    for i, word_info in enumerate(word_infos):
        label = word_info['label']
        if label == 'S' or label == 'I':
            stack.append((label, i))
        elif label == 'E':
            clause_start = None
            while stack:
                popped_label, popped_index = stack.pop()
                if popped_label == 'S':
                    clause_start = popped_index
                    break
            if clause_start is not None:
                clause_words = word_infos[clause_start:i + 1]
                has_verb = any(w['pos'] in verb_pos_tags for w in clause_words)
                if not has_verb:
                    # Rule 2 applies: change E to I
                    word_infos[i]['label'] = 'I'
                    rule_2_applies = True
    return rule_2_applies

def check_rule_1(word_infos):
    """
    Checks if rule 1 is satisfied: the number of 'S' and 'E' labels are equal.
    Returns True if equal, False otherwise.
    """
    s_count = sum(1 for w in word_infos if w['label'] == 'S')
    e_count = sum(1 for w in word_infos if w['label'] == 'E')
    return s_count == e_count

def mark_sentence_as_review(word_infos):
    """
    Marks the sentence as reviewed by prefixing the first word with '#'.
    """
    if word_infos:
        word_infos[0]['word'] = '#' + word_infos[0]['word']
    return word_infos

def generate_clauses(word_infos):
    """
    Generates candidate clauses based on the labels using a stack.
    Adds words with 'O' label before 'S' to the clause if their POS tag is not 'SYM'.
    Returns a list of clause strings.
    """
    stack = []
    clauses = []
    i = 0

    while i < len(word_infos):
        word_info = word_infos[i]
        label = word_info['label']
        
        if label == 'S' or label == 'I':
            # Collect preceding 'O' words (excluding 'SYM' POS)
            clause_start = i
            while clause_start > 0 and word_infos[clause_start - 1]['label'] == 'O' and word_infos[clause_start - 1]['pos'] != 'SYM':
                clause_start -= 1
            
            # Add to stack
            stack.append((label, clause_start))
        
        elif label == 'E':
            clause_start = None
            while stack:
                popped_label, popped_index = stack.pop()
                if popped_label == 'S':
                    clause_start = popped_index
                    break
            if clause_start is not None:
                clause_words = [w['word'] for w in word_infos[clause_start:i + 1]]
                clause = ' '.join(clause_words)
                clauses.append(clause)
        
        i += 1

    return clauses


def save_clauses(clauses, clause_file_path, word_infos):
    """
    Saves the original sentence and the list of clauses to the specified file.
    Each clause is written on a new line.
    """
    with open(clause_file_path, 'w', encoding='utf-8') as f:
        # Write the original sentence
        original_sentence = ' '.join(w['word'] for w in word_infos)
        f.write(f"{original_sentence}\n\n")
        
        # Write the clauses
        # f.write("Generated Clauses:\n")
        for clause in clauses:
            f.write(clause + '\n')

def save_sentence(word_infos, file_path):
    """
    Saves the modified sentence to the specified file.
    Each word info is written on a new line with tab separation.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        for w in word_infos:
            f.write(f"{w['word']}\t{w['pos']}\t{w['label']}\n")

def process_sentences(input_dir, clauses_output_dir, invalid_dir, review_dir):
    """
    Processes all sentence files in the input directory.
    Generates candidate clauses for valid sentences and organizes sentences based on linguistic rules.
    """
    # Create output directories if they don't exist
    os.makedirs(clauses_output_dir, exist_ok=True)
    os.makedirs(invalid_dir, exist_ok=True)
    os.makedirs(review_dir, exist_ok=True)
    
    # Iterate over each file in the input directory
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        
        # Ensure it's a file
        if not os.path.isfile(file_path):
            continue
        
        # Read the sentence
        word_infos = read_sentence(file_path)
        
        # Check rule 2
        rule_2 = check_rule_2(word_infos, VERB_POS_TAGS)
        
        if rule_2:
            # Mark the sentence as reviewed
            word_infos = mark_sentence_as_review(word_infos)
            # Save to review directory
            review_file_path = os.path.join(review_dir, filename)
            save_sentence(word_infos, review_file_path)
            continue  # Skip further processing
        
        # Check rule 1
        rule_1 = check_rule_1(word_infos)
        
        if not rule_1:
            # Mark the filename with '*' and move to invalid directory
            invalid_filename = f"*{filename}"
            invalid_file_path = os.path.join(invalid_dir, invalid_filename)
            shutil.copy(file_path, invalid_file_path)
            continue  # Skip further processing
        
        # If passed both rules, generate candidate clauses
        clauses = generate_clauses(word_infos)
        
        # Save the clauses and the original sentence to the clauses_output_dir
        sentence_id = os.path.splitext(filename)[0]
        clause_filename = f"{sentence_id}_clause.txt"
        clause_file_path = os.path.join(clauses_output_dir, clause_filename)
        save_clauses(clauses, clause_file_path, word_infos)

def main():
    # Define directories
    input_directory = "/home/riya/Hindi_CBI/segregated_data"
    clauses_output_directory = "clause_output"
    invalid_sentences_directory = "invalid_labelled_data"
    review_sentences_directory = "review_sentences"
    
    # Process the sentences
    process_sentences(
        input_dir=input_directory,
        clauses_output_dir=clauses_output_directory,
        invalid_dir=invalid_sentences_directory,
        review_dir=review_sentences_directory
    )
    print("Processing completed.")

if __name__ == "__main__":
    main()

