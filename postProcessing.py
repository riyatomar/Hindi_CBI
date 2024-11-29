import re

def read_file(file_path):
    """Reads the file and returns its content as a string."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# def extract_sentences(data):
#     """Extracts sentence IDs and content, returning a dictionary with combined sentences by base ID."""
#     sentences = {}
#     matches = re.findall(r'<sent_id=(Geo_nios_[0-9]*ch_[0-9]*[a-zA-Z]?)>\n(.*?)\n</sent_id>', data, re.DOTALL)

#     for sent_id, content in matches:
#         # base_id = re.match(r'(Geo_nios_[0-9]*ch_[0-9]*)', sent_id).group(1)
#         base_id = re.match(r'\d+[a-zA-Z]?', sent_id).group(0)
#         if base_id in sentences:
#             sentences[base_id] += " " + '\n' + content
#         else:
#             sentences[base_id] = content
#     return sentences/

def extract_sentences(data):
    """
    Extracts sentence IDs and their content from the input data.
    Groups sentences by their base IDs, combining their content.
    
    Base IDs are numeric with optional trailing alphabetic characters (e.g., 1002a, 45, 999b).
    Sentences with the same numeric part are grouped together.
    """
    sentences = {}
    # Adjusted regex for numeric base IDs with optional trailing characters
    matches = re.findall(r'<sent_id=(\d+[a-zA-Z]?)>\n(.*?)\n</sent_id>', data, re.DOTALL)

    for sent_id, content in matches:
        # Extract the numeric base ID (e.g., "1002" from "1002a")
        base_id_match = re.match(r'(\d+)', sent_id)
        if base_id_match:
            base_id = base_id_match.group(1)
            # Combine content for sentences with the same base ID
            if base_id in sentences:
                sentences[base_id] += " \n" + content
            else:
                sentences[base_id] = content

    return sentences


def clean_intermediate_sym(content):
    """
    Removes intermediate '।	SYM O' occurrences along with the entire line, keeping only the last one.
    """
    # Remove intermediate '।	SYM O' lines entirely
    cleaned_content = re.sub(r'।\tSYM\tO \n', '', content)
    
    # Check if the last '।	SYM O' is present, if not, add it to the end
    if not cleaned_content.endswith('।\tSYM\tO'):
        cleaned_content += '\n।\tSYM\tO'
    
    return cleaned_content.strip()

def process_sentences(sentences):
    """Processes each combined sentence, cleaning up intermediate '।	SYM O' entries."""
    processed_sentences = {}
    for base_id, combined_content in sentences.items():
        processed_sentences[base_id] = clean_intermediate_sym(combined_content)
    return processed_sentences

def write_file(output_path, processed_sentences):
    """Writes the processed sentences to a file in the specified format."""
    with open(output_path, 'w', encoding='utf-8') as output_file:
        for base_id, combined_content in processed_sentences.items():
            output_file.write(f"<sent_id={base_id}>\n{combined_content}\n</sent_id>\n\n")

def main(input_file, output_file):
    """Main function to read, process, and write sentences."""
    data = read_file(input_file)
    combined_sentences = extract_sentences(data)
    processed_sentences = process_sentences(combined_sentences)
    write_file(output_file, processed_sentences)
    
# Run the main function
main('data/clause_bounded_output.txt', 'data/final_output.txt')
 

