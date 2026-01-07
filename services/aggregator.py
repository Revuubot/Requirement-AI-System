def merge_list_items(existing_list, new_list):
    """
    Avoid duplicates by comparing value + source_quote.
    """
    seen = {(item["value"], item["source_quote"]) for item in existing_list}

    for item in new_list:
        key = (item["value"], item["source_quote"])
        if key not in seen and item["value"].strip():
            existing_list.append(item)
            seen.add(key)

    return existing_list


def merge_extractions(master, incoming):
    """
    Merge structured extraction results chunk-by-chunk.
    """

    for field in master.keys():

        # skip fields that are not lists
        if not isinstance(master[field], list):
            continue

        new_items = incoming.get(field, [])

        merge_list_items(master[field], new_items)

    return master
