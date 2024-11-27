from scripts.file_utils import update_cnx_value

def handle_pof_rvks_rbk(parser_output, new_entries, cp_count):
    nc_cnx_index = None
    for item in parser_output:
        if item.get('dependency_relation') in ['pof', 'rvks', 'rbk']:
            cp_index = len(parser_output) + len(new_entries) + 1
            update_cnx_value(item, f'{cp_index}:kriyAmUla')

            if isinstance(item['cnx_value'], list):
                nc_cnx_index = item['cnx_value'][0].split(':')[0]
                item['cnx_value'] = item['cnx_value'][0]

            new_cp_entry = {
                'index': cp_index,
                'original_word': f'[CP_{cp_count}]',
                'wx_word': f'[CP_{cp_count}]',
            }
            new_entries.append(new_cp_entry)
            cp_count += 1

            if nc_cnx_index is not None:
                for entry in new_entries:
                    if int(entry.get('index', -1)) == int(nc_cnx_index):
                        update_cnx_value(entry, f'{cp_index}:kriyAmUla')

            head_index = int(item.get('head_index', -1))
            for target_item in parser_output:
                if int(target_item.get('index', -1)) == head_index:
                    update_cnx_value(target_item, f'{cp_index}:verbalizer_B')

                    for j in range(parser_output.index(target_item) + 1, len(parser_output)):
                        next_item = parser_output[j]
                        if next_item.get('pos_tag') == 'VAUX':
                            update_cnx_value(next_item, f'{cp_index}:verbalizer_I')
                        else:
                            break
    return cp_count