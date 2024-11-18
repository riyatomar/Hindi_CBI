import json
from wxconv import WXC
import re

def read_json_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def devanagari_to_wx(word):
    wxc = WXC()
    wx_text = wxc.convert(word)
    return wx_text

def update_cnx_value(item, new_value):
    """Update the cnx_value field, converting it to a list if necessary."""
    if 'cnx_value' in item:
        if isinstance(item['cnx_value'], str):
            # If it's a string, convert to list and add the new value
            item['cnx_value'] = [item['cnx_value'], new_value]
        elif isinstance(item['cnx_value'], list):
            # If it's already a list, append the new value
            item['cnx_value'].append(new_value)
    else:
        # If cnx_value doesn't exist, just assign the new value as a string
        item['cnx_value'] = new_value

def modify_json_data(json_data):
    span_count = 1  # Initialize the span counter
    cp_count = 1    # Initialize the cp counter
    meas_count = 1  # Initialize the measurement counter
    calendaric_count = 1
    nc_count = 1
    spatial_count = 1  # Counter for spatial cases
    start_stack = []  # Stack to track start positions
    span_indexes = {}  # Dictionary to track span indexes
    units = ["kilomItara", "mItara", "kilo", "seMtImItara", "milImItara", "lItara"]  # List of measuring units
    calendaric_unit = ['agaswa']

    # Traverse the 'response' array
    for response in json_data.get('response', []):
        parser_output = response.get('parser_output', [])
        new_entries = []  # To store newly created entries

        # First step: Convert all 'original_word' to WX format
        for i, item in enumerate(parser_output):
            original_word = item.get('original_word', '')
            wx_word = devanagari_to_wx(original_word)  # Convert Devanagari to WX
            item['wx_word'] = wx_word  # Assign the WX form to 'wx_word'

        
        # Handling 'nc' construction and consecutive 'pof__cn' cases
        for i, item in enumerate(parser_output):
            if item.get('dependency_relation') == 'pof__cn' and item.get('pos_tag') in ['NNPC', 'NNC']  and 'cnx_value' not in item:
                # print(item)
                nc_index = len(parser_output) + len(new_entries) + 1
                # Update cnx_value with 'mod' for the first occurrence
                item['cnx_value'] = f'{nc_index}:mod'
                # print(item)
                # update_cnx_value(item, f'{nc_index}:mod')
                new_nc_entry = {
                    'index': nc_index,
                    'original_word': f'[nc_{nc_count}]',
                    'wx_word': f'[nc_{nc_count}]',
                }
                new_entries.append(new_nc_entry)
                nc_count += 1
                # print(f'{nc_index}:mod')

                # Check the next item to see if it's also 'pof__cn'
                if i + 1 < len(parser_output):
                    next_item = parser_output[i + 1]
                    if next_item.get('dependency_relation') == 'pof__cn':
                        next_item['cnx_value'] = f'{nc_index}:head'
                        # update_cnx_value(next_item, f'{nc_index}:head')

                # Find the head for the current item
                head_index = int(item.get('head_index', -1))
                for target_item in parser_output:
                    if int(target_item.get('index', -1)) == head_index:
                        print(target_item)
                        target_item['cnx_value'] = f'{nc_index}:head'
                        # update_cnx_value(target_item, f'{nc_index}:head')


        # Check for both 'से' and 'तक'
        for i, item in enumerate(parser_output):
            original_word = item.get('original_word', '')
            wx_word = item.get('wx_word', '')


            # Handling spans for 'से' and 'तक'
            if item.get('original_word') == 'से':
                head_index = int(item.get('head_index', -1))
                start_stack.append({
                    'index': int(item.get('index', -1)),
                    'head_index': head_index
                })
                
            elif item.get('original_word') == 'तक':
                head_index = int(item.get('head_index', -1))
                if start_stack:
                    start_item = start_stack.pop()  # Get the most recent start
                    for target_item in parser_output:
                        if (
                            int(target_item.get('index', -1)) == head_index and
                            target_item.get('dependency_relation') in ['k7t', 'k7p']
                        ):
                            span_index = len(parser_output) + len(new_entries) + 1
                            new_entry = {
                                'index': span_index,
                                'original_word': f'[span_{span_count}]',
                                'wx_word': f'[span_{span_count}]'
                            }
                            new_entries.append(new_entry)

                            span_indexes[f'[span_{span_count}]'] = span_index
                            # target_item['cnx_value'] = f'{span_index}:end'
                            update_cnx_value(target_item, f'{span_index}:end')
                            for item_to_update in parser_output:
                                if int(item_to_update.get('index', -1)) == start_item['index']:
                                    # item_to_update['cnx_value'] = f'{span_index}:start'
                                    update_cnx_value(item_to_update, f'{span_index}:start')
                            span_count += 1
                            break

        # Handling 'pof', 'rvks', 'rbk'
        for item in parser_output:
            if item.get('dependency_relation') in ['pof', 'rvks', 'rbk']:
                cp_index = len(parser_output) + len(new_entries) + 1
                # item['cnx_value'] = f'{cp_index}:kriyAmUla'
                update_cnx_value(item, f'{cp_index}:kriyAmUla')
                new_cp_entry = {
                    'index': cp_index,
                    'original_word': f'[cp_{cp_count}]',
                    'wx_word': f'[cp_{cp_count}]',
                }
                new_entries.append(new_cp_entry)
                cp_count += 1

                head_index = int(item.get('head_index', -1))
                for target_item in parser_output:
                    if int(target_item.get('index', -1)) == head_index:
                        # target_item['cnx_value'] = f'{cp_index}:verbalizer'
                        update_cnx_value(target_item, f'{cp_index}:verbalizer')

        

        # Handling measurement units
        for i, item in enumerate(parser_output):
            wx_word = item.get('wx_word', '').strip()

            # Check if the current wx_word contains a measuring unit
            if any(unit in wx_word for unit in units):
                
                # Check the previous item (if available) for a numeric wx_word
                if i > 0:
                    prev_item = parser_output[i - 1]
                    prev_word = prev_item.get('wx_word', '')

                    # If the previous word contains digits
                    if re.search(r'\d', prev_word):
                        meas_index = len(parser_output) + len(new_entries) + 1
                        # item['cnx_value'] = f'{meas_index}:unit'
                        update_cnx_value(item, f'{meas_index}:unit')
                        # prev_item['cnx_value'] = f'{meas_index}:count'
                        update_cnx_value(prev_item, f'{meas_index}:count')
                        meas_entry = {
                            'index': meas_index,
                            'original_word': f'[meas_{meas_count}]',
                            'wx_word': f'[meas_{meas_count}]'
                        }
                        new_entries.append(meas_entry)
                        meas_count += 1

        # Handling calendaric units
        for i, item in enumerate(parser_output):
            wx_word = item.get('wx_word', '').strip()

            if any(unit in wx_word for unit in calendaric_unit):
                # Check the previous item (if available) for a numeric wx_word
                if i > 0:
                    prev_item = parser_output[i - 1]
                    prev_word = prev_item.get('wx_word', '')
                    next_item = parser_output[i + 1]
                    next_word = next_item.get('wx_word', '')

                    # If the previous word contains digits
                    if re.search(r'\d', prev_word):
                        calendaric_index = len(parser_output) + len(new_entries) + 1
                        # item['cnx_value'] = f'{calendaric_index}:component_of'
                        update_cnx_value(item, f'{calendaric_index}:component_of')
                        # prev_item['cnx_value'] = f'{calendaric_index}:component_of'
                        update_cnx_value(prev_item, f'{calendaric_index}:component_of')
                        meas_entry = {
                            'index': calendaric_index,
                            'original_word': f'[calender_{calendaric_count}]',
                            'wx_word': f'[calender_{calendaric_count}]'
                        }
                        new_entries.append(meas_entry)
                        calendaric_count += 1

                        if re.search(r'\d', next_word):
                            # next_item['cnx_value'] = f'{calendaric_index}:component_of'
                            update_cnx_value(next_item, f'{calendaric_index}:component_of')

        # Handling NN/NNP and k7p relation with 'main'
        for i in range(len(parser_output)):
            item = parser_output[i]

            # Check if the word has pos_tag as 'NN' or 'NNP' and relation as 'k7p'
            if item.get('pos_tag') in ['NN', 'NNP'] and item.get('dependency_relation') == 'k7p':
                head_index = int(item.get('head_index', -1))
                # print('head_index-->', head_index)

                # Search for the next word that matches the conditions
                for j in range(i + 1, len(parser_output)):
                    next_item = parser_output[j]

                    if (
                        next_item.get('pos_tag') in ['NN', 'NNP'] and
                        next_item.get('dependency_relation') == 'k7p' and
                        int(next_item.get('head_index', -1)) == head_index
                    ):
                        # Check if the head_index points to a 'main' dependency
                        for head_item in parser_output:
                            if int(head_item.get('index', -1)) == head_index and head_item.get('dependency_relation') == 'main':
                                spatial_index = len(parser_output) + len(new_entries) + 1
                                new_entry = {
                                    'index': spatial_index,
                                    'original_word': f'[spatial_{spatial_count}]',
                                    'wx_word': f'[spatial_{spatial_count}]'
                                }
                                new_entries.append(new_entry)

                                # item['cnx_value'] = f'{spatial_index}:whole'
                                # next_item['cnx_value'] = f'{spatial_index}:part'
                                update_cnx_value(item, f'{spatial_index}:whole')
                                update_cnx_value(next_item, f'{spatial_index}:part')
                                spatial_count += 1
                                break
                        break

        # New Rule: Handling 'r6' relation with 'k7p' and 'main'
        for item in parser_output:
            if item.get('pos_tag') in ['NN', 'NNP'] and item.get('dependency_relation') == 'r6':
                head_index = int(item.get('head_index', -1))

                # Find the word with index equal to this head_index and 'k7p' relation
                for k7p_item in parser_output:
                    if (
                        int(k7p_item.get('index', -1)) == head_index and
                        k7p_item.get('dependency_relation') == 'k7p'
                    ):
                        # Check if the 'k7p' head_index points to 'main'
                        main_head_index = int(k7p_item.get('head_index', -1))
                        for main_item in parser_output:
                            if (
                                int(main_item.get('index', -1)) == main_head_index and
                                main_item.get('dependency_relation') == 'main'
                            ):
                                spatial_index = len(parser_output) + len(new_entries) + 1
                                new_entry = {
                                    'index': spatial_index,
                                    'original_word': f'[spatial_{spatial_count}]',
                                    'wx_word': f'[spatial_{spatial_count}]'
                                }
                                new_entries.append(new_entry)

                                # item['cnx_value'] = f'{spatial_index}:whole'
                                # k7p_item['cnx_value'] = f'{spatial_index}:part'
                                update_cnx_value(item, f'{spatial_index}:whole')
                                update_cnx_value(k7p_item, f'{spatial_index}:part')
                                spatial_count += 1
                                break

        # Append the new entries to parser_output
        parser_output.extend(new_entries)


# Specify the path to your JSON file
file_path = 'IO/input.txt'

# Read the JSON data
json_data = read_json_from_file(file_path)

# Modify the JSON data based on the condition
modify_json_data(json_data)

# Optionally write the modified data back to a file if needed
with open('IO/cxn_json_out.txt', 'w', encoding='utf-8') as file:
    json.dump(json_data, file, ensure_ascii=False, indent=4)
