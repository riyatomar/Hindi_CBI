import json

def convert_to_tsv(data):
    headers = ['index', 'original_word', 'wx_word', 'pos_tag', 'dependency_relation', 'head_index', 'cnx_value']
    tsv_data = []
    
    # Loop through each sentence in the response
    for response in data['response']:
        parser_output = response['parser_output']
        
        # tsv_data.append("\t".join(headers))
        
        for word_data in parser_output:
            row = []
            for header in headers:
                row.append(str(word_data.get(header, '-')))
            tsv_data.append("\t".join(row))
    
    return "\n".join(tsv_data)

input_file = 'IO/cxn_json_out.txt'  
output_file = 'IO/cxn_tsv_out.tsv' 

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

tsv_output = convert_to_tsv(data)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(tsv_output)

