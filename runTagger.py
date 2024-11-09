# import os
# os.system("isc-tagger -i data/sentences.txt -o data/tagged_output.txt") 

import subprocess
import csv

tsv_file = 'data/processed_sentences.txt'
output_file = 'data/tagged_output.txt'

# Open and read the TSV file
with open(tsv_file, 'r', encoding='utf-8') as file, open(output_file, 'w', encoding='utf-8') as out_file:
    reader = csv.reader(file, delimiter='\t')
    
    # Process each row
    for row in reader:
        if len(row) < 2:
            continue 
        id_col = row[0]       
        sentence = row[1]     
        
        # Run the command and capture the output
        result = subprocess.run(
            f'echo "{sentence}" | isc-tagger', 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        
        # Strip any extra newline characters
        tagged_output = result.stdout.strip()

        # Write ID and tagged output to file
        out_file.write(f"<sent_id={id_col}>\n")
        out_file.write(f"{tagged_output}\n</sent_id>\n\n")
