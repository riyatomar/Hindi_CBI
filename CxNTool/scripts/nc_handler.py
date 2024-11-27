# from scripts.file_utils import update_cnx_value

# def handle_mod_and_head(parser_output, new_entries, nc_count):
#     for i, item in enumerate(parser_output):
#         if item.get('dependency_relation') == 'pof__cn' and item.get('pos_tag') in ['NNC', 'NNPC']:
#             if 'cnx_value' in item and item['cnx_value']:
#                 continue
             
#             nc_index = len(parser_output) + len(new_entries) + 1
#             update_cnx_value(item, f'{nc_index}:mod')
#             # print(item)
#             if isinstance(item['cnx_value'], list):
#                 item['cnx_value'] = item['cnx_value'][0]
#                 # print(item['cnx_value'])
#             new_nc_entry = {
#                 'index': nc_index,
#                 'original_word': f'[NC_{nc_count}]',
#                 'wx_word': f'[NC_{nc_count}]',
#             }
#             new_entries.append(new_nc_entry)
#             nc_count += 1

#             if i + 1 < len(parser_output):
#                 next_item = parser_output[i + 1]
#                 if next_item.get('dependency_relation') == 'pof__cn':
#                     next_item['cnx_value'] = f'{nc_index}:head'
#                     first_cnx_value = next_item.get('cnx_value')
#                     second_cnx_value = f'{nc_index + 1}:mod'
#                     next_item['cnx_value'] = first_cnx_value
#                     new_nc_entry['cnx_value'] = second_cnx_value

#             head_index = int(item.get('head_index', -1))
#             for target_item in parser_output:
#                 if int(target_item.get('index', -1)) == head_index:
#                     target_item['cnx_value'] = f'{nc_index}:head'
#     return nc_count



from scripts.file_utils import update_cnx_value

def handle_mod_and_head(parser_output, new_entries, nc_count, ne_count):
    def is_wx_word_present(word, entries):
        """Check if a wx_word is already present in new_entries."""
        return any(entry.get('original_word') == word for entry in entries)

    for i, item in enumerate(parser_output):
        if item.get('dependency_relation') == 'pof__cn' and item.get('pos_tag') in ['NNC', 'NNPC']:
            if 'cnx_value' in item and item['cnx_value']:
                continue
             
            nc_index = len(parser_output) + len(new_entries) + 1

            # Determine the prefix, counter, and cnx_value structure based on the pos_tag
            if item.get('pos_tag') == 'NNC':
                prefix = 'NC'
                current_count = nc_count
                while is_wx_word_present(f'[{prefix}_{current_count}]', new_entries):
                    current_count += 1  # Ensure uniqueness
                nc_count = current_count + 1
                update_cnx_value(item, f'{nc_index}:mod')
            elif item.get('pos_tag') == 'NNPC':
                prefix = 'NE'
                current_count = ne_count
                while is_wx_word_present(f'[{prefix}_{current_count}]', new_entries):
                    current_count += 1  # Ensure uniqueness
                ne_count = current_count + 1
                update_cnx_value(item, f'{nc_index}:B')

            if isinstance(item['cnx_value'], list):
                item['cnx_value'] = item['cnx_value'][0]

            # Create a new entry with appropriate `wx_word`
            new_nc_entry = {
                'index': nc_index,
                'original_word': f'[{prefix}_{current_count}]',
                'wx_word': f'[{prefix}_{current_count}]',
            }
            new_entries.append(new_nc_entry)

            # Adjust `cnx_value` for the next item in sequence if it matches criteria
            if i + 1 < len(parser_output):
                next_item = parser_output[i + 1]
                if next_item.get('dependency_relation') == 'pof__cn':
                    if item.get('pos_tag') == 'NNC':
                        next_item['cnx_value'] = f'{nc_index}:head'
                    elif item.get('pos_tag') == 'NNPC':
                        next_item['cnx_value'] = f'{nc_index}:I'
                    first_cnx_value = next_item.get('cnx_value')
                    second_cnx_value = f'{nc_index + 1}:mod' if item.get('pos_tag') == 'NNC' else f'{nc_index + 1}:B'
                    next_item['cnx_value'] = first_cnx_value
                    new_nc_entry['cnx_value'] = second_cnx_value

            # Update the `cnx_value` of the target item's head if applicable
            head_index = int(item.get('head_index', -1))
            for target_item in parser_output:
                if int(target_item.get('index', -1)) == head_index:
                    if item.get('pos_tag') == 'NNC':
                        target_item['cnx_value'] = f'{nc_index}:head'
                    elif item.get('pos_tag') == 'NNPC':
                        target_item['cnx_value'] = f'{nc_index}:I'

    return nc_count, ne_count
