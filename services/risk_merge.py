def merge_risks(master, incoming):
    seen = {(r["description"], r["source_quote"]) for r in master}

    for r in incoming:
        key = (r["description"], r["source_quote"])
        if key not in seen:
            master.append(r)
            seen.add(key)

    return master
