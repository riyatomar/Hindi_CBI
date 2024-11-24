from scripts.file_utils import update_cnx_value

def integrate_ner_annotations(ner_output, parser_output, ne_count, new_entries):
    """Integrate NER annotations into the parser output."""
    ner_annotations = {ann["word"]: ann["annotation"] for ann in ner_output["data"][0]["annotation"]}
    in_ne_sequence = False
    ne_index = None  # Initialize outside to avoid unbound variable errors

    for item in parser_output:
        original_word = item.get("original_word", "")
        annotation = ner_annotations.get(original_word, "O")
        ner_value = annotation.split('-')[0]

        if annotation.startswith("B-"):
            if in_ne_sequence:
                ne_count += 1
            in_ne_sequence = True
            ne_index = len(parser_output) + len(new_entries) + 1
            update_cnx_value(item, f'{ne_index}:{ner_value}')

            new_entries.append({
                'index': ne_index,
                'original_word': f'[ne_{ne_count}]',
                'wx_word': f'[ne_{ne_count}]',
            })
        elif annotation.startswith("I-") and in_ne_sequence:
            update_cnx_value(item, f'{ne_index}:{ner_value}')
        else:
            in_ne_sequence = False

    return parser_output, ne_count, new_entries
