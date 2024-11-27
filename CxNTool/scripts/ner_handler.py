from scripts.file_utils import update_cnx_value

def handle_ner_annotations(ner_output, parser_output, ne_count, new_entries):
    """Integrate NER annotations into the parser output."""
    ner_annotations = {ann["word"]: ann["annotation"] for ann in ner_output["data"][0]["annotation"]}
    in_ne_sequence = False
    current_entity_type = None  # Tracks the current entity type in sequence
    ne_index = None
    entity_count = {"PER": 0, "LOC": 0, "ORG": 0}  # Keeps track of counts for each entity type

    for item in parser_output:
        original_word = item.get("original_word", "")
        annotation = ner_annotations.get(original_word, "O")
        ner_value = annotation.split('-')[0]

        if annotation.startswith("B-"):
            # Close the previous sequence, if any
            if in_ne_sequence:
                ne_count += 1

            # Start a new entity sequence
            in_ne_sequence = True
            current_entity_type = annotation.split('-')[1]  # Extract entity type (e.g., PER, LOC)
            
            # Increment the count for the new B- entity
            entity_count[current_entity_type] += 1
            ne_index = len(parser_output) + len(new_entries) + 1
            ne_count += 1 # for ne_1, ne_2, ne_3, etc
            wx_word = f'{current_entity_type}_{entity_count[current_entity_type]}'  # Generate wx_word like PER_1, LOC_1, etc.
            update_cnx_value(item, f'{ne_index}:{ner_value}')

            new_entries.append({
                'index': ne_index,
                'original_word': f'[NE_{ne_count}]',
                'wx_word': wx_word,
            })

        elif annotation.startswith("I-"):
            # Handle continuation or transition between types
            entity_type = annotation.split('-')[1]
            if in_ne_sequence and entity_type == current_entity_type:
                # Continuation of the same entity
                update_cnx_value(item, f'{ne_index}:{ner_value}')
            elif in_ne_sequence and entity_type != current_entity_type:
                # Transition to a new entity type
                ne_count += 1
                current_entity_type = entity_type
                entity_count[current_entity_type] += 1
                ne_index = len(parser_output) + len(new_entries) + 1

                wx_word = f'{current_entity_type}_{entity_count[current_entity_type]}'
                update_cnx_value(item, f'{ne_index}:B')

                new_entries.append({
                    'index': ne_index,
                    'original_word': f'[NE_{ne_count}]',
                    'wx_word': wx_word,
                })
            else:
                # Invalid sequence; reset
                in_ne_sequence = False
                current_entity_type = None
        else:
            # Reset sequence if not part of an entity
            in_ne_sequence = False
            current_entity_type = None

    return parser_output, ne_count, new_entries


