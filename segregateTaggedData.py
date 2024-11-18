import os

input_file = '/home/riya/Hindi_CBI/data/final_output.txt' 
output_folder = 'segregated_data' 

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

with open(input_file, 'r', encoding='utf-8') as file:
    data = file.read()

sentences = data.strip().split('</sent_id>')
for sentence in sentences:
    if '<sent_id=' in sentence:
        # Extract the sent_id
        start_tag = sentence.find('<sent_id=') + len('<sent_id=')
        end_tag = sentence.find('>')
        sent_id = sentence[start_tag:end_tag].strip()

        # Clean up the sentence content
        sentence_content = sentence[end_tag + 1:].strip()
        output_file_path = os.path.join(output_folder, f"{sent_id}.txt")

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(sentence_content)

print(f"Sentences successfully saved in '{output_folder}' folder.")
