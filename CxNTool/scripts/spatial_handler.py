from scripts.file_utils import update_cnx_value

def handle_spatial_relations(parser_output, new_entries, spatial_count):
    # Handling NN/NNP and k7p relation with 'main'
    for i in range(len(parser_output)):
        item = parser_output[i]

        if i + 1 < len(parser_output):
            next_item = parser_output[i + 1]

        # Check if the word has pos_tag as 'NN' or 'NNP' and relation as 'k7p'
        if item.get('pos_tag') in ['NN', 'NNP'] and item.get('dependency_relation') == 'k7p' and next_item.get('pos_tag') == 'PSP':
            head_index = int(item.get('head_index', -1))
      
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
                                'original_word': f'[SPATIAL_{spatial_count}]',
                                'wx_word': f'[SPATIAL_{spatial_count}]'
                            }
                            new_entries.append(new_entry)

                            update_cnx_value(item, f'{spatial_index}:whole')
                            update_cnx_value(next_item, f'{spatial_index}:part')
                            spatial_count += 1
                            break
                    break

    # New Rule: Handling 'r6' relation with 'k7p' and 'main'
    for item in parser_output:
        if i + 1 < len(parser_output):
            next_item = parser_output[i + 1]
        if item.get('pos_tag') in ['NN', 'NNP'] and item.get('dependency_relation') == 'r6' and  next_item.get('pos_tag') == 'PSP':
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
                                'original_word': f'[SPATIAL_{spatial_count}]',
                                'wx_word': f'[SPATIAL_{spatial_count}]'
                            }
                            new_entries.append(new_entry)

                            update_cnx_value(item, f'{spatial_index}:whole')
                            update_cnx_value(k7p_item, f'{spatial_index}:part')
                            spatial_count += 1
                            break

    return spatial_count